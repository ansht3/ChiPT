"""
AI Answer Generation Service
Connects to OpenAI API to generate answers with context
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse
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
    get_kb_path, 
    list_knowledge_bases,
    COLLECTION_NAME_DEFAULT,
    FILE_UUID_FIELD
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
    if not (file.filename.endswith(".txt") or file.filename.endswith(".md") or file.filename.endswith(".pdf")):
         raise HTTPException(status_code=400, detail="Only .txt, .md, and .pdf files are supported")

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

@app.get("/kbs/{name}/docs/{file_uuid}")
async def get_kb_document(name: str, file_uuid: str):
    logger.info(f"Attempting to retrieve document: KB='{name}', UUID='{file_uuid}'")
    try:
        db_path = get_kb_path(name)
        logger.info(f"Resolved DB path: {db_path}")
        
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        
        source_path = manager.get_file_path_by_uuid(file_uuid)
        logger.info(f"Resolved source path from DB: {source_path}")
        
        if not source_path:
             logger.error(f"UUID '{file_uuid}' not found in DB '{name}'")
             raise HTTPException(status_code=404, detail="Document UUID not found in database")
             
        if not os.path.exists(source_path):
            logger.error(f"File not found on disk: {source_path}")
            # Fallback: check if it's in the KB directory
            kb_dir = os.path.dirname(db_path)
            potential_path = os.path.join(kb_dir, os.path.basename(source_path))
            logger.info(f"Checking fallback path: {potential_path}")
            if os.path.exists(potential_path):
                source_path = potential_path
                logger.info(f"Found at fallback path: {source_path}")
            else:
                raise HTTPException(status_code=404, detail=f"Document file not found: {source_path}")
            
        return FileResponse(source_path)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieval document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kbs/{name}/docs/{file_uuid}/view")
async def get_kb_document_view(name: str, file_uuid: str):
    print(f"DEBUG: Viewing document: KB='{name}', UUID='{file_uuid}'")
    try:
        db_path = get_kb_path(name)
        print(f"DEBUG: DB Path: {db_path}")
        
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        
        source_path = manager.get_file_path_by_uuid(file_uuid)
        print(f"DEBUG: Resolved source path: {source_path}")
        
        if not source_path:
             print("DEBUG: UUID not found in DB")
             raise HTTPException(status_code=404, detail="Document UUID not found")
             
        if not os.path.exists(source_path):
             print(f"DEBUG: File not found at {source_path}")
             # Try fallback
             kb_dir = os.path.dirname(db_path)
             potential_path = os.path.join(kb_dir, os.path.basename(source_path))
             print(f"DEBUG: Checking fallback: {potential_path}")
             
             if os.path.exists(potential_path):
                 source_path = potential_path
                 print(f"DEBUG: Found at fallback: {source_path}")
             else:
                 print("DEBUG: Fallback failed")
                 raise HTTPException(status_code=404, detail="File not found")

        # Check for PDF
        # Check for PDF
        if source_path.lower().endswith('.pdf'):
             download_url = f"/kbs/{name}/docs/{file_uuid}/download"
             inline_url = f"/kbs/{name}/docs/{file_uuid}/inline"
             # Use the same styling as the markdown view but with an iframe
             html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Document View - {os.path.basename(source_path)}</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
                <style>
                    :root {{
                        --primary: #2D5A7B;
                        --primary-dark: #1E3A52;
                        --accent: #E8915C;
                        --bg-main: #FAFAF8;
                        --bg-panel: #FFFFFF;
                        --text-primary: #1A1A1A;
                        --text-secondary: #6B7280;
                        --border: #E5E7EB;
                    }}
    
                    body {{
                        font-family: 'DM Sans', sans-serif;
                        line-height: 1.6;
                        color: var(--text-primary);
                        background-color: var(--bg-main);
                        margin: 0;
                        padding: 0;
                        height: 100vh;
                        display: flex;
                        flex-direction: column;
                    }}
    
                    .navbar {{
                        background: rgba(255, 255, 255, 0.8);
                        backdrop-filter: blur(12px);
                        border-bottom: 1px solid var(--border);
                        padding: 1rem 2rem;
                        position: sticky;
                        top: 0;
                        z-index: 100;
                    }}
    
                    .nav-content {{
                        max-width: 1200px;
                        margin: 0 auto;
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                    }}
    
                    .logo {{
                        font-family: 'Crimson Pro', serif;
                        font-size: 1.5rem;
                        font-weight: 700;
                        color: var(--primary-dark);
                        text-decoration: none;
                    }}
    
                    .main-container {{
                        flex: 1;
                        padding: 2rem;
                        max-width: 1200px;
                        margin: 0 auto;
                        width: 100%;
                        box-sizing: border-box;
                        display: flex;
                        flex-direction: column;
                    }}
    
                    .document-card {{
                        background: var(--bg-panel);
                        border-radius: 16px;
                        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                        border: 1px solid var(--border);
                        display: flex;
                        flex-direction: column;
                        flex-grow: 1;
                        overflow: hidden;
                    }}
    
                    .doc-header {{
                        padding: 1.5rem 2rem;
                        border-bottom: 1px solid var(--border);
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background: #FAFAF8;
                    }}
    
                    .doc-title {{
                        font-family: 'Crimson Pro', serif;
                        font-size: 1.25rem;
                        font-weight: 600;
                        color: var(--primary-dark);
                        display: flex;
                        align-items: center;
                        gap: 0.5rem;
                    }}
    
                    .download-btn {{
                        background-color: var(--primary);
                        color: white;
                        padding: 0.4rem 0.8rem;
                        border-radius: 6px;
                        text-decoration: none;
                        font-weight: 500;
                        font-size: 0.875rem;
                    }}
    
                    iframe {{
                        flex-grow: 1;
                        width: 100%;
                        border: none;
                    }}
                </style>
            </head>
            <body>
                <nav class="navbar glass-panel">
                    <div class="nav-content">
                        <div class="logo">ChiPT</div>
                        <div style="font-size: 0.875rem; color: var(--text-secondary);">Document Viewer</div>
                    </div>
                </nav>
    
                <div class="main-container">
                    <div class="document-card">
                        <div class="doc-header">
                            <div class="doc-title">
                                <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                                </svg>
                                {os.path.basename(source_path)}
                            </div>
                            <a href="{download_url}" class="download-btn">Download Raw</a>
                        </div>
                        <iframe src="/static/pdfjs/web/viewer.html?file={inline_url}" type="text/html"></iframe>
                    </div>
                </div>
            </body>
            </html>
            """
             return HTMLResponse(content=html_content)

        # Read content
        content = ""
        try:
             with open(source_path, "r", encoding="utf-8", errors="replace") as f:
                 content = f.read()
        except Exception as e:
             content = f"Error reading file: {e}"
        
        # Simple HTML wrapper with Markdown support and App Styling
        import json
        json_content = json.dumps(content)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Document View - {os.path.basename(source_path)}</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            
            <!-- Fonts -->
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;600;700&family=JetBrains+Mono:wght@400;500&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
            
            <!-- Tailwind (for utility classes if needed, but we'll use custom CSS to keep it self-contained) -->
            <script src="https://cdn.tailwindcss.com"></script>

            <!-- Markdown -->
            <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/github-markdown-css/github-markdown.min.css">
            
            <!-- KaTeX for Math -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
            <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
            
            <style>
                :root {{
                    --primary: #2D5A7B;
                    --primary-dark: #1E3A52;
                    --accent: #E8915C;
                    --bg-main: #FAFAF8;
                    --bg-panel: #FFFFFF;
                    --text-primary: #1A1A1A;
                    --text-secondary: #6B7280;
                    --border: #E5E7EB;
                }}

                body {{
                    font-family: 'DM Sans', -apple-system, sans-serif;
                    background-color: var(--bg-main);
                    color: var(--text-primary);
                    margin: 0;
                    padding: 0;
                    min-height: 100vh;
                }}

                .glass-panel {{
                    background: rgba(255, 255, 255, 0.9);
                    backdrop-filter: blur(10px);
                    border-bottom: 1px solid rgba(229, 231, 235, 0.5);
                }}

                .navbar {{
                    position: sticky;
                    top: 0;
                    z-index: 50;
                    padding: 1rem 1.5rem;
                }}

                .nav-content {{
                    max-width: 900px;
                    margin: 0 auto;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}

                .logo {{
                    font-family: 'Crimson Pro', serif;
                    font-weight: 700;
                    font-size: 1.5rem;
                    background: linear-gradient(135deg, var(--primary), var(--accent));
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }}

                .main-container {{
                    max-width: 900px;
                    margin: 2rem auto;
                    padding: 0 1.5rem;
                }}

                .document-card {{
                    background: var(--bg-panel);
                    border-radius: 16px;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
                    overflow: hidden;
                    border: 1px solid var(--border);
                }}

                .doc-header {{
                    background: #f8fafc;
                    padding: 1.5rem 2rem;
                    border-bottom: 1px solid var(--border);
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }}

                .doc-title {{
                    font-family: 'Crimson Pro', serif;
                    font-size: 1.25rem;
                    font-weight: 600;
                    color: var(--primary-dark);
                    display: flex;
                    align-items: center;
                    gap: 0.5rem;
                }}

                .download-btn {{
                    background-color: var(--primary);
                    color: white;
                    padding: 0.5rem 1rem;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 500;
                    font-size: 0.875rem;
                    transition: all 0.2s;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.05);
                }}

                .download-btn:hover {{
                    background-color: var(--primary-dark);
                    transform: translateY(-1px);
                }}

                .markdown-body {{
                    padding: 3rem;
                    background: transparent;
                    font-family: 'DM Sans', sans-serif;
                    color: var(--text-primary);
                }}
                
                /* Styled Tables - Force Light Theme Overrides */
                .markdown-body table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 1em 0;
                    border-radius: 8px;
                    overflow: hidden;
                    box-shadow: 0 0 0 1px var(--border);
                    background-color: #ffffff !important;
                }}
                
                .markdown-body table th {{
                    background-color: #f8fafc !important;
                    color: var(--text-primary) !important;
                    font-weight: 600;
                    text-align: left;
                    padding: 0.75rem 1rem;
                    border-bottom: 1px solid var(--border) !important;
                    border-top: none !important;
                }}
                
                .markdown-body table td {{
                    padding: 0.75rem 1rem;
                    border-bottom: 1px solid var(--border) !important;
                    border-top: none !important;
                    color: var(--text-primary) !important;
                    background-color: #ffffff !important;
                }}
                
                .markdown-body table tr {{
                    background-color: #ffffff !important;
                }}
                
                .markdown-body table tr:nth-child(even) td {{
                    background-color: #f8fafc !important;
                }}
                
                 .markdown-body table tr:nth-child(even) {{
                    background-color: #f8fafc !important;
                }}

                /* Styled Code Blocks */
                .markdown-body pre {{
                    background-color: #1e293b !important; /* Dark slate */
                    border-radius: 8px;
                    padding: 1rem;
                    color: #e2e8f0;
                    overflow-x: auto;
                    margin-bottom: 1rem;
                }}

                .markdown-body code {{
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 0.9em;
                }}
                
                .markdown-body p code, .markdown-body li code, .markdown-body table code {{
                    background-color: rgba(0,0,0,0.05);
                    padding: 0.2em 0.4em;
                    border-radius: 4px;
                    color: var(--text-primary);
                }}
                
                .markdown-body pre code {{
                    background-color: transparent;
                    padding: 0;
                    color: inherit;
                    white-space: pre;
                }}

                /* Override headers */
                .markdown-body h1, .markdown-body h2, .markdown-body h3 {{
                    font-family: 'Crimson Pro', serif;
                    border-bottom-color: var(--border);
                    color: var(--primary-dark);
                }}
            </style>
        </head>
        <body>
            <!-- Navbar -->
            <nav class="navbar glass-panel">
                <div class="nav-content">
                    <div class="logo">ChiPT</div>
                    <div style="font-size: 0.875rem; color: var(--text-secondary);">Document Viewer</div>
                </div>
            </nav>

            <div class="main-container">
                <div class="document-card">
                    <div class="doc-header">
                        <div class="doc-title">
                            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                            </svg>
                            {os.path.basename(source_path)}
                        </div>
                        <a href="/kbs/{name}/docs/{file_uuid}/download" class="download-btn">
                            Download Raw
                        </a>
                    </div>
                    <div id="content" class="markdown-body"></div>
                </div>
            </div>

            <script>
                const rawContent = {json_content};

                function renderMarkdown(content) {{
                    // 1. Protect Math: Replace $...$ and $$...$$ with placeholders
                    // We use a specific placeholder format that marked() won't touch.
                    const mathBlocks = [];
                    
                    // Regex for:
                    // 1. Display math $$...$$
                    // 2. Display math \\[...\\] (standard LaTeX)
                    // 3. Inline math \\(...\\) (standard LaTeX)
                    // 4. Inline math $...$
                    // 5. Display math [ ... ] (variant sometimes seen, ensure it contains backslash to avoid false positives with links)
                    
                    const regex = /\\$\\$([\\s\\S]*?)\\$\\$|\\\\\\[([\\s\\S]*?)\\\\\\]|\\[(\\s*\\\\[\\s\\S]*?)\\]|\\\\\\(([\\s\\S]*?)\\\\\\)|\\$([^$\\n]*?)\\$/g;
                    
                    let protectedContent = content.replace(regex, function(match, m1, m2, m3, m4, m5) {{
                        const id = `MATH_BLOCK_${{mathBlocks.length}}`;
                        // Normalize to $$...$$ or $...$ depending on the match type
                        // m1: $$...$$ content
                        // m2: \\[...\\] content
                        // m3: [ ... ] content (our special case)
                        // m4: \\(...\\) content
                        // m5: $...$ content
                        
                        // We want to store the *normalized* version for restoration
                        if (m1 !== undefined) mathBlocks.push(`$$${{m1}}$$`); // Already $$
                        else if (m2 !== undefined) mathBlocks.push(`$$${{m2}}$$`); // Convert \\[ to $$
                        else if (m3 !== undefined) mathBlocks.push(`$$${{m3}}$$`); // Convert [ ] with backslash to $$
                        else if (m4 !== undefined) mathBlocks.push(`$${{m4}}$`);  // Convert \\( to $
                        else if (m5 !== undefined) mathBlocks.push(`$${{m5}}$`);  // Already $
                        else mathBlocks.push(match); // Fallback
                        
                        return id;
                    }});

                    // 2. Configure marked
                    const renderer = new marked.Renderer();
                    const linkRenderer = renderer.link;
                    renderer.link = (href, title, text) => {{
                        const html = linkRenderer.call(renderer, href, title, text);
                        return html.replace(/^<a /, '<a target="_blank" rel="noopener noreferrer" ');
                    }};

                    // 3. Parse markdown
                    let html = marked.parse(protectedContent, {{ renderer: renderer }});
                    
                    // 4. Restore Math
                    mathBlocks.forEach((match, index) => {{
                        const id = `MATH_BLOCK_${{index}}`;
                        html = html.replace(id, match);
                    }});
                    
                    // 5. Create temp element for math rendering
                    const temp = document.createElement('div');
                    temp.innerHTML = html;
                    
                    // 6. Render math equations
                    if (window.renderMathInElement) {{
                        renderMathInElement(temp, {{
                            delimiters: [
                                {{left: '$$', right: '$$', display: true}},
                                {{left: '$', right: '$', display: false}},
                                {{left: '\\\\(', right: '\\\\)', display: false}},
                                {{left: '\\\\[', right: '\\\\]', display: true}}
                            ],
                            throwOnError: false
                        }});
                    }}
                    
                    return temp.innerHTML;
                }}

                document.getElementById('content').innerHTML = renderMarkdown(rawContent);
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html_content)
    except HTTPException:
        raise
    except Exception as e:
        print(f"DEBUG: Exception: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kbs/{name}/docs/{file_uuid}/download")
async def download_kb_document(name: str, file_uuid: str):
    """Download a document file (Always Attachment)."""
    try:
        db_path = get_kb_path(name)
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        
        source_path = manager.get_file_path_by_uuid(file_uuid)
        print(f"DEBUG: Download requested for UUID {file_uuid}")
        
        if not source_path:
             raise HTTPException(status_code=404, detail="Document UUID not found")

        # Fallback logic
        if not os.path.exists(source_path):
             kb_dir = os.path.dirname(db_path)
             potential_path = os.path.join(kb_dir, os.path.basename(source_path))
             if os.path.exists(potential_path):
                 source_path = potential_path
             else:
                 raise HTTPException(status_code=404, detail="Document not found")
            
        return FileResponse(
            source_path, 
            filename=os.path.basename(source_path),
            content_disposition_type="attachment"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/kbs/{name}/docs/{file_uuid}/inline")
async def get_kb_document_inline(name: str, file_uuid: str):
    """Serve document inline (for iframe viewing)."""
    try:
        db_path = get_kb_path(name)
        manager = VectorDatabaseManager(db_path, collection_name=COLLECTION_NAME_DEFAULT)
        
        source_path = manager.get_file_path_by_uuid(file_uuid)
        
        if not source_path:
             raise HTTPException(status_code=404, detail="Document UUID not found")

        # Fallback logic
        if not os.path.exists(source_path):
             kb_dir = os.path.dirname(db_path)
             potential_path = os.path.join(kb_dir, os.path.basename(source_path))
             if os.path.exists(potential_path):
                 source_path = potential_path
             else:
                 raise HTTPException(status_code=404, detail="Document not found")

        # Force inline display
        return FileResponse(
            source_path, 
            media_type='application/pdf',
            filename=os.path.basename(source_path),
            content_disposition_type="inline"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error serving inline document: {e}")
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
