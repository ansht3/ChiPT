import httpx
import logging
from typing import Optional, List, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from database import Question, Message, User
from pymilvus import Collection, connections, utility
import numpy as np
from config import CACHE_API_URL, AI_API_URL, MILVUS_HOST, QA_DOCS_MILVUS_PORT, QA_DOCS_COLLECTION_NAME, QA_DOCS_EMBEDDING_API_URL, QA_DOCS_EMBEDDING_MODEL, AI_SERVICE_URL

logger = logging.getLogger(__name__)

# CACHE_API_URL = "http://localhost:8902/search"
# AI_API_URL = "http://localhost:8901/generate"
REQUEST_TIMEOUT = 300.0  # Increased for large models (includes cache + AI processing time)

# # Milvus configuration (same as cache service)
# MILVUS_HOST = "localhost"
# MILVUS_PORT = "19531"
# COLLECTION_NAME = "qa_cache"
# EMBEDDING_API_URL = "http://localhost:11434/v1/embeddings"
# EMBEDDING_MODEL = "qwen3-embedding:8b-q8_0"


async def check_cached_answer(question: str, context: List[Dict[str,str]]) -> Optional[str]:
    """
    Check if there's a cached answer for the question.
    
    Args:
        question: The question text to search for
        context: List of previous Q&A pairs [{"q": str, "a": str}, ...]
        
    Returns:
        The cached answer if found, None otherwise
    """
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                CACHE_API_URL,
                json={"query": question,
                      "context": context}
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get("found", False) and data.get("answer"):
                return data["answer"]
            return None
            
    except httpx.TimeoutException:
        logger.warning(f"Timeout while checking cached answer for question")
        return None
    except httpx.ConnectError:
        logger.warning(f"Connection error while checking cached answer")
        return None
    except Exception as e:
        logger.warning(f"Error checking cached answer: {str(e)}")
        return None


async def generate_ai_answer(question: str, context: List[Dict[str, str]], kb_name: str = None) -> str:
    """
    Generate an AI answer for the question using context.
    
    Args:
        question: The question text
        context: List of previous Q&A pairs [{"q": str, "a": str}, ...]
        
    Returns:
        The generated answer, or error message if generation fails
    """
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                AI_API_URL,
                json={
                    "question": question,
                    "context": context,
                    "kb_name": kb_name
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if "answer" in data and data["answer"]:
                return data["answer"]
            return "Unable to generate suggestion. Please write manually."
            
    except httpx.TimeoutException:
        logger.warning(f"Timeout while generating AI answer")
        return "Unable to generate suggestion. Please write manually."
    except httpx.ConnectError:
        logger.warning(f"Connection error while generating AI answer")
        return "Unable to generate suggestion. Please write manually."
    except Exception as e:
        logger.error(f"Error generating AI answer: {str(e)}")
        return "Unable to generate suggestion. Please write manually."


async def get_user_context(db: AsyncSession, user_id: int, query_id: int, limit: int = 5) -> List[Dict[str, str]]:
    """
    Get the last N answered questions for a user as context.
    
    Args:
        db: Database session
        user_id: User ID to get context for
        query_id: Query ID to get context for
        limit: Maximum number of Q&A pairs to return
        
    Returns:
        List of dicts with "q" and "a" keys
    """
    # Get questions with messages from instructors
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.messages))
        .where(Question.user_id == user_id)
        .where(Question.id == query_id)
        .order_by(Question.created_at.desc())
        .limit(limit)
    )
    
    questions = result.scalars().all()
    context = []

    old_student_content = ""
    
    for question in questions:
        # Get the first instructor message as the answer
        old_student_content = student_content = question.content
        if question.messages:
            in_cnt = st_cnt = 0
            for msg in question.messages:
                msg_role = msg.role if isinstance(msg.role, str) else msg.role.value
                if msg_role == "instructor":
                    answer_content = msg.content if (msg.content and msg.content.strip()) else past_answer_content
                    context.append({
                        "q": student_content,
                        "a": answer_content
                    })
                    past_answer_content = answer_content
                    old_student_content = student_content
                    student_content = " "
                    in_cnt += 1
                if msg_role == "student":
                    student_content += msg.content+"\n"
                    st_cnt += 1
                    #break  # Only take the first instructor response
    
    student_content = student_content if (student_content and student_content.strip()) else old_student_content

    return (student_content,context)

async def rewrite_query_context(initial_query, conversation_data):
    """
    Processes a list of conversation turns and generates a target query and a 
    conversation history prompt for an LLM for later rewriting the last ambiguous 
    query into a standalone one.
    """
    history_lines = []
    target_query = initial_query
    
    # 1. Parse history and identify target
    # Logic: Find the most recent 'q' entry to rewrite
    for i, entry in enumerate(conversation_data):
        for key, value in entry.items():
            is_q = key.startswith('q')
            is_a = key.startswith('a')
            
            if is_q: # Target query is the last user query
                target_query = value
            
            # Build the history string
            prefix = "User: " if is_q else "Assistant: "
            history_lines.append(f"{prefix}{value}")

    # 2. Build the LLM Context
    history_context = "\n".join(history_lines[:-1]) if target_query else "\n".join(history_lines)
    
    # Rewrite the following 'Current Query' into a standalone question based on the 'History'.

    return history_context


async def get_suggested_answer(db: AsyncSession, question_id: int, kb_name: str = None) -> Dict[str, str]:
    """
    Get a suggested answer for a question.
    
    Tries cached answer first, then generates AI answer with user context.
    
    Args:
        db: Database session
        question_id: ID of the question to answer
        
    Returns:
        Dict with "suggested_answer" and "source" keys
    """
    result = await db.execute(
        select(Question).where(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    
    if not question:
        raise ValueError(f"Question {question_id} not found")
    
    target_query, history_context = await get_user_context(db, question.user_id, question.id, limit=5)

    #llm_history_context = await rewrite_query_context(target_query,history_context)

    logger.info(f"get_suggested_answer: question \"{target_query.strip()}\" \n question context: \"{history_context}\"")

    cached_answer = await check_cached_answer(target_query, history_context)
    if cached_answer:
        return {
            "suggested_answer": cached_answer,
            "source": "cached"
        }
    
    ai_answer = await generate_ai_answer(target_query, history_context, kb_name=kb_name)
    
    return {
        "suggested_answer": ai_answer,
        "source": "ai"
    }


async def get_embedding_for_cache(text: str) -> Optional[List[float]]:
    """
    Get embedding vector for text from LLM API.
    
    Args:
        text: The text to embed
        
    Returns:
        Embedding vector or None if failed
    """
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                QA_DOCS_EMBEDDING_API_URL,
                headers={
                    "Authorization": "Bearer nada",
                    "Content-Type": "application/json"
                },
                json={
                    "model": QA_DOCS_EMBEDDING_MODEL,
                    "input": text
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            if "data" in data and len(data["data"]) > 0:
                embedding = data["data"][0]["embedding"]
                return embedding
            else:
                logger.error(f"Unexpected embedding API response: {data}")
                return None
                
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        return None


def normalize_embedding(embedding: List[float]) -> List[float]:
    """Normalize embedding vector to unit length for cosine similarity."""
    emb_array = np.array(embedding, dtype=np.float32)
    norm = np.linalg.norm(emb_array)
    if norm == 0:
        return embedding
    return (emb_array / norm).tolist()


async def add_to_cache(question: str, answer: str) -> bool:
    """
    Add a Q&A pair directly to Milvus cache.
    
    This is much faster than HTTP-based insertion and handles unlimited text length.
    
    Args:
        question: The question text
        answer: The answer text
        
    Returns:
        True if successfully added, False otherwise
    """
    try:
        # Connect to Milvus FIRST
        try:
            connections.connect(
                alias="cache_insert",
                host=MILVUS_HOST,
                port=QA_DOCS_MILVUS_PORT
            )
            logger.debug("Connected to Milvus for cache insertion")
        except Exception as conn_error:
            # Connection might already exist, check if we can use it
            error_msg = str(conn_error).lower()
            if "already exist" not in error_msg and "connected" not in error_msg:
                logger.error(f"Failed to connect to Milvus: {conn_error}")
                return False
            logger.debug(f"Using existing Milvus connection: {conn_error}")
        
        # Now check if collection exists
        if not utility.has_collection(QA_DOCS_COLLECTION_NAME, using="cache_insert"):
            logger.error(f"Collection '{QA_DOCS_COLLECTION_NAME}' not found")
            return False
        
        # Get embedding for the question
        embedding = await get_embedding_for_cache(question)
        if not embedding:
            logger.error("Failed to generate embedding for cache")
            return False
        
        # Normalize embedding
        normalized_emb = normalize_embedding(embedding)
        
        # Get collection
        collection = Collection(QA_DOCS_COLLECTION_NAME, using="cache_insert")
        
        # Insert data
        entities = [
            [question],  # questions
            [answer],    # answers
            [normalized_emb]  # embeddings
        ]
        
        collection.insert(entities)
        collection.flush()
        
        logger.info(f"Successfully added Q&A to Milvus cache (direct insertion): {question[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Error adding to cache (direct insertion): {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False


# --- Knowledge Base Management Proxies ---

async def get_knowledge_bases() -> List[str]:
    """Get list of available knowledge bases from AI service."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{AI_SERVICE_URL}/kbs")
            response.raise_for_status()
            return response.json().get("kbs", [])
    except Exception as e:
        logger.error(f"Error getting KBs: {e}")
        return []

async def create_knowledge_base(name: str) -> bool:
    """Create a new knowledge base."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/kbs",
                json={"name": name}
            )
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Error creating KB: {e}")
        return False

async def get_kb_details(name: str) -> Dict:
    """Get details (files) of a knowledge base."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{AI_SERVICE_URL}/kbs/{name}")
            response.raise_for_status()
            return response.json()
    except Exception as e:
        logger.error(f"Error getting KB details: {e}")
        return {"name": name, "files": []}

async def upload_file_to_kb(name: str, filename: str, content: bytes) -> bool:
    """Upload a file to a knowledge base."""
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            files = {'file': (filename, content)}
            response = await client.post(
                f"{AI_SERVICE_URL}/kbs/{name}/files",
                files=files
            )
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Error uploading file to KB: {e}")
        raise e # Propagate error to controller for feedback

async def delete_file_from_kb(name: str, filename: str) -> bool:
    """Remove a file from a knowledge base."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # We'll use request.query_params or body? 
            # AI Service implementation: KBFileDeleteRequest body
            response = await client.request(
                "DELETE",
                f"{AI_SERVICE_URL}/kbs/{name}/files",
                json={"filename": filename}
            )
            response.raise_for_status()
            return True
    except Exception as e:
        logger.error(f"Error deleting file from KB: {e}")
        return False
