"""
AI Answer Generation Service
Connects to OpenAI API to generate answers with context
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import httpx
import logging
from dotenv import load_dotenv
import sys
import shutil
import os

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from rag_api.rag_main_kdocs import rag_answer
from rag_api.vector_database_handling import (
    VectorDatabaseManager, 
    create_kb_dir, 
    get_kb_path, 
    list_knowledge_bases,
    COLLECTION_NAME_DEFAULT
)
from config import OPENAI_BASE_URL, OPENAI_API_KEY, CHAT_COMPLETION_MODEL

# Load environment varaibles from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Answer Service")

# See config.py for OPENAI_BASE_URL and OPENAI_API_KEY settings
REQUEST_TIMEOUT = 120.0  # Increased for large models


class ContextPair(BaseModel):
    q: str
    a: str


class GenerateRequest(BaseModel):
    question: str = Field(min_length=1,max_length=10000)
    context: List[ContextPair] = Field(default_factory=list)
    kb_name: Optional[str] = None


class GenerateResponse(BaseModel):
    answer: str

class KBListResponse(BaseModel):
    kbs: List[str]

class KBCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9_-]+$")

class KBDetailsResponse(BaseModel):
    name: str
    files: List[str]

class KBFileDeleteRequest(BaseModel):
    filename: str

def build_prev_qa_pairs(question: str, context: List[ContextPair]) -> str:
    """Combine all relevant Q&A pairs into a single prompt for the AI."""
    prompt_parts = []
    if context:
        prompt_parts.append("\nStart of previous Q&A pairs from this student for context:")
        for i, pair in enumerate(context, 1):
            prompt_parts.append(f"\nQ{i}: {pair.q}")
            prompt_parts.append(f"A{i}: {pair.a}")
        prompt_parts.append("\nEnd of previous Q&A pairs from this student for context.")
        return "\n".join(prompt_parts)
    else:
        return "No previous Q&A pairs provided."

def build_prompt(question: str, context: List[ContextPair]) -> str:
    """Build the prompt for the AI with context."""
    prompt_parts = [
        "You are a helpful teaching assistant answering student questions.",
        "Provide clear, concise, and educational answers.",
    ]
    
    if context:
        prompt_parts.append("\nHere are some previous Q&A pairs from this student for context:")
        for i, pair in enumerate(context, 1):
            prompt_parts.append(f"\nQ{i}: {pair.q}")
            prompt_parts.append(f"A{i}: {pair.a}")
        prompt_parts.append("\nBased on the student's history, answer the following question:")
    else:
        prompt_parts.append("\nAnswer the following question:")
    
    prompt_parts.append(f"\n\nQuestion: {question}")
    prompt_parts.append("\nAnswer:")
    
    return "\n".join(prompt_parts)


async def call_openai_api(prompt: str) -> str:
    """Call the OpenAI API to generate an answer."""
    try:
        print('Post requested!')

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": CHAT_COMPLETION_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a knowledgeable and helpful teaching assistant."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            )

            print('Post completed!')
            
            response.raise_for_status()
            data = response.json()

            print('Data received!')
            
            if "choices" in data and len(data["choices"]) > 0:
                answer = data["choices"][0]["message"]["content"].strip()
                return answer
            else:
                logger.error(f"Unexpected API response format: {data}")
                return "Unable to generate answer at this time."
                
    except httpx.TimeoutException:
        logger.error("OpenAI API request timed out")
        return "Request timed out. Please try again."
    except httpx.HTTPStatusError as e:
        logger.error(f"OpenAI API returned error: {e.response.status_code} - {e.response.text}")
        return "Unable to generate answer due to API error."
    except httpx.ConnectError:
        logger.error("Failed to connect to OpenAI API")
        return "Unable to connect to AI service. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error calling OpenAI API: {str(e)}")
        return "An unexpected error occurred while generating the answer."


@app.post("/generate", response_model=GenerateResponse)
async def generate_answer(request: GenerateRequest):
    """
    Generate an AI answer for a question with optional context.
    
    Args:
        request: Contains question and optional context from previous Q&A pairs
        
    Returns:
        Generated answer from the AI
    """
    logger.info(f"Generating answer for question: {request.question[:100]}...")
    logger.info(f"Context pairs provided: {len(request.context)}")
    
    #prompt = build_prompt(request.question, request.context)
    qa_context = build_prev_qa_pairs(request.question, request.context)
    answer = rag_answer(request.question, qa_context=qa_context, kb_name=request.kb_name)
    
    logger.info(f"Generated answer length: {len(answer)} characters")
    logger.info(answer)
    return GenerateResponse(answer=answer)

# --- Knowledge Base Management Endpoints ---

@app.get("/kbs", response_model=KBListResponse)
async def list_kbs():
    """List available knowledge bases."""
    kbs = list_knowledge_bases()
    return KBListResponse(kbs=kbs)

@app.post("/kbs", status_code=201)
async def create_kb(request: KBCreateRequest):
    """Create a new knowledge base."""
    try:
        # Check if already exists
        if request.name in list_knowledge_bases():
             raise HTTPException(status_code=400, detail="Knowledge Base already exists")
        
        create_kb_dir(request.name)
        return {"message": f"Knowledge Base '{request.name}' created successfully"}
    except Exception as e:
        logger.error(f"Error creating KB: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kbs/{name}", response_model=KBDetailsResponse)
async def get_kb_details(name: str):
    """Get details of a knowledge base (list files)."""
    try:
        db_path = get_kb_path(name)
        # We need to construct the manager to list files
        # Alternatively, we could read from the file system if we just want raw files?
        # But 'add_documents' copies them to processed_docs or just chunks them. 
        # The DB keeps track of source files. Let's use the DB as source of truth.
        
        # NOTE: This connects to the DB, which might be slow or lock if in use.
        # But VectorDatabaseManager handles connection and locking.
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        # We might need to handle case where DB file doesn't exist yet (empty KB)
        if not os.path.exists(db_path):
             return KBDetailsResponse(name=name, files=[])

        files = manager.get_file_list()
        return KBDetailsResponse(name=name, files=files)
    except Exception as e:
        logger.error(f"Error reading KB details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/kbs/{name}/files", status_code=201)
async def upload_file_to_kb(name: str, file: UploadFile = File(...)):
    """Upload a file to a knowledge base."""
    # check valid file extension
    if not (file.filename.endswith(".txt") or file.filename.endswith(".md")):
         raise HTTPException(status_code=400, detail="Only .txt and .md files are supported")

    try:
        # Verify KB exists
        if name not in list_knowledge_bases():
             raise HTTPException(status_code=404, detail="Knowledge Base not found")
        
        db_path = get_kb_path(name)
        kb_dir = os.path.dirname(db_path)
        
        # Save file temporarily to disk (in the KB folder so it persists as 'source')
        # User requirement: "inside should have all of the files"
        # So we save the original file to ai_service/rag_api/knowledge-bases/{name}/{filename}
        
        file_path = os.path.join(kb_dir, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Update Vector DB
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        manager.add_documents([file_path])
        
        return {"message": f"File '{file.filename}' added to KB '{name}'"}
    except Exception as e:
        logger.error(f"Error adding file to KB: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/kbs/{name}/files")
async def delete_file_from_kb(name: str, request: KBFileDeleteRequest):
    """Remove a file from a knowledge base."""
    try:
        db_path = get_kb_path(name)
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        
        # remove_document expects absolute path, but we might store relative or absolute?
        # In upload, we saved to `kb_dir/filename` and passed that absolute path.
        # So manager has the absolute path.
        # We need to reconstruct the path from the filename.
        
        kb_dir = os.path.dirname(db_path)
        file_path = os.path.join(kb_dir, request.filename)
        
        manager.remove_document(file_path)
        
        # Also remove the physical source file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return {"message": f"File '{request.filename}' removed from KB '{name}'"}
    except Exception as e:
        logger.error(f"Error removing file from KB: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ai-generator"}


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Allow custom port via command line argument
    port = 8901
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default 8901")
    
    print(f"Starting AI Answer Generation Service on port {port}...")
    print(f"OpenAI API: {OPENAI_BASE_URL}")
    print(f"Model: {CHAT_COMPLETION_MODEL}")
    uvicorn.run(app, host="0.0.0.0", port=port)
