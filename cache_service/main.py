"""
Q&A Cache Service with Semantic Search
Uses Milvus for vector similarity search to find cached answers
"""
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import httpx
import logging
import sys
import os

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pymilvus import (
    connections,
    Collection,
    CollectionSchema,
    FieldSchema,
    DataType,
    utility
)
import numpy as np
from contextlib import asynccontextmanager
from config import (
    MILVUS_HOST, QA_DOCS_MILVUS_PORT, QA_DOCS_COLLECTION_NAME, 
    QA_DOCS_EMBEDDING_MODEL, REWRITE_MODEL, OPENAI_BASE_URL, 
    OPENAI_API_KEY, LOCAL_MILVUS, MILVUS_RAG_DOCS_DB_PATH
)
from milvus_utils import MilvusConnection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
# MILVUS_HOST = "localhost"
# MILVUS_PORT = "19531"  # Using alternate port to avoid conflicts with existing Milvus
# COLLECTION_NAME = "qa_cache"
EMBEDDING_DIM = 4096  # qwen3-embedding:8b-q8_0 dimension (was 1536 for OpenAI ada-002)
SIMILARITY_THRESHOLD = 0.85  # Minimum similarity score to consider a match

# OpenAI configuration for embeddings and query rewriting
# See config.py for OPENAI_BASE_URL and OPENAI_API_KEY settings
REQUEST_TIMEOUT = 120.0  # Increased for large models (was 30.0)



class ContextPair(BaseModel):
    q: str
    a: str


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=10000)
    context: List[ContextPair] = Field(default_factory=list)    


class SearchResponse(BaseModel):
    found: bool
    answer: Optional[str] = None


def build_context_from_list(context: List[ContextPair]) -> str:
    """Build the context strict for the AI context."""
    context_parts = []

    if context:
        for i, pair in enumerate(context, 1):
            context_parts.append(f"\nQ{i}: {pair.q}")
            context_parts.append(f"A{i}: {pair.a}")
    #else:
    #    context_parts.append("")

    return "\n".join(context_parts)


async def get_embedding(text: str) -> List[float]:
    """Get embedding vector from OpenAI API."""
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{OPENAI_BASE_URL}/embeddings",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
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
                logger.info(f"Generated embedding with {len(embedding)} dimensions")
                
                # Check if embedding is all zeros (potential issue)
                if all(x == 0 for x in embedding):
                    logger.error("WARNING: Embedding is all zeros!")
                
                return embedding
            else:
                logger.error(f"Unexpected embedding API response: {data}")
                return None
                
    except Exception as e:
        logger.error(f"Error getting embedding: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None


async def rewrite_query(query: str, context: List[ContextPair]) -> List[str]:
    """
    Generate alternative phrasings of the query for better matching.
    Returns list of query variations including the original.
    """
    variations = [query]
    
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            system_content = (
                "You are a query rewriting assistant. Your goal is to rewrite the 'Current User Query' "
                "into a standalone version using the provided 'Conversation History'. "
                "The rewritten query must be specific, include all relevant entities, "
                "and be answerable without any extra context. "
                "Output 2 alternative versions, one per line."
            )

            context_str = build_context_from_list(context)

            user_content = f"""
CONVERSATION HISTORY:
{context_str}

CURRENT USER QUERY:
{query}

STANDALONE REWRITES:
"""
            response = await client.post(
                f"{OPENAI_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {OPENAI_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": REWRITE_MODEL,
                    "messages": [
                        {
                            "role": "system",
                            "content": system_content
                        },
                        {
                            "role": "user",
                            "content": user_content
                        }
                    ],
                    "temperature": 0.5,
                    "max_tokens": 200
                }
            ) 
            response.raise_for_status()
            data = response.json()
            
            if "choices" in data and len(data["choices"]) > 0:
                rewritten = data["choices"][0]["message"]["content"].strip()
                # Split by newlines and clean up
                new_variations = [v.strip() for v in rewritten.split('\n') if v.strip()]
                variations.extend(new_variations[:2])  # Add up to 2 variations
                
    except Exception as e:
        logger.warning(f"Query rewriting failed, using original query only: {str(e)}")
    
    logger.info(f"Query variations: {len(variations)}")
    return variations


async def init_milvus_collection():
    """Initialize Milvus collection for Q&A cache."""
    try:
        if LOCAL_MILVUS:
            from pymilvus import MilvusClient
            logger.info(f"Using Milvus Lite at: {MILVUS_RAG_DOCS_DB_PATH}")
            if not os.path.exists(os.path.dirname(MILVUS_RAG_DOCS_DB_PATH)):
                 os.makedirs(os.path.dirname(MILVUS_RAG_DOCS_DB_PATH), exist_ok=True)

            client = MilvusClient(MILVUS_RAG_DOCS_DB_PATH)
            
            # Check if collection exists
            if not client.has_collection(QA_DOCS_COLLECTION_NAME):
                 logger.info(f"Creating collection '{QA_DOCS_COLLECTION_NAME}'")
                 client.create_collection(
                     collection_name=QA_DOCS_COLLECTION_NAME,
                     dimension=EMBEDDING_DIM,
                     metric_type="IP", 
                     auto_id=True,
                     primary_field_name="id",
                     vector_field_name="embedding"
                 )
                 
                 # Seed data
                 collection_wrapper = MilvusConnection(client=client, is_local=True, collection_name=QA_DOCS_COLLECTION_NAME)
                 await seed_sample_data(collection_wrapper)
            else:
                 logger.info(f"Collection '{QA_DOCS_COLLECTION_NAME}' already exists")
            
            return MilvusConnection(client=client, is_local=True, collection_name=QA_DOCS_COLLECTION_NAME)

        else:
            connections.connect(
                alias="default",
                host=MILVUS_HOST,
                port=QA_DOCS_MILVUS_PORT
            )
            logger.info("Connected to Milvus")
            
            # Check if collection exists
            collection_exists = utility.has_collection(QA_DOCS_COLLECTION_NAME)
            
            if collection_exists:
                logger.info(f"Collection '{QA_DOCS_COLLECTION_NAME}' already exists")
                collection = Collection(QA_DOCS_COLLECTION_NAME)
                
                # Force release and reload to ensure it's properly loaded
                try:
                    collection.release()
                    logger.info("Released existing collection")
                except:
                    pass
                
                collection.load()
                logger.info("Collection loaded successfully")
                
                # Check if collection has data
                num_entities = collection.num_entities
                logger.info(f"Collection has {num_entities} entities")
                
                if num_entities == 0:
                    logger.info("Collection is empty, seeding sample data...")
                    collection_wrapper = MilvusConnection(client=collection, is_local=False, collection_name=QA_DOCS_COLLECTION_NAME)
                    await seed_sample_data(collection_wrapper)
                    # Reload after seeding
                    collection.load()
                    logger.info(f"After seeding: {collection.num_entities} entities")
                
                return MilvusConnection(client=collection, is_local=False, collection_name=QA_DOCS_COLLECTION_NAME)
            
            # Create collection schema
            fields = [
                FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
                FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=10000),
                FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=50000),
                FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM)
            ]
            
            schema = CollectionSchema(
                fields=fields,
                description="Q&A cache with semantic search"
            )
            
            collection = Collection(
                name=QA_DOCS_COLLECTION_NAME,
                schema=schema
            )
            
            # Create IVF_FLAT index for vector search
            index_params = {
                "metric_type": "IP",  # Inner product (cosine similarity for normalized vectors)
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128}
            }
            
            collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            
            collection.load()
            logger.info(f"Created and loaded collection '{QA_DOCS_COLLECTION_NAME}'")
            
            # Try to add sample Q&A pairs, but don't fail if OpenAI API is unavailable
            try:
                collection_wrapper = MilvusConnection(client=collection, is_local=False, collection_name=QA_DOCS_COLLECTION_NAME)
                await seed_sample_data(collection_wrapper)
            except Exception as e:
                logger.warning(f"Could not seed sample data (OpenAI API may be unavailable): {str(e)}")
                logger.warning("Collection created successfully but is empty. You can add data later via /add endpoint.")
            
            return MilvusConnection(client=collection, is_local=False, collection_name=QA_DOCS_COLLECTION_NAME)
        
    except Exception as e:
        logger.error(f"Failed to initialize Milvus: {str(e)}")
        # import traceback
        # logger.error(traceback.format_exc())
        return None


async def seed_sample_data(collection: MilvusConnection):
    """Add sample Q&A pairs to the cache."""
    sample_qa = [
        {
            "question": "What is machine learning?",
            "answer": "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed. It focuses on developing algorithms that can access data and learn patterns from it."
        },
        {
            "question": "How does backpropagation work?",
            "answer": "Backpropagation is an algorithm used to train neural networks. It works by calculating the gradient of the loss function with respect to each weight by propagating errors backward through the network, from output to input layers, using the chain rule of calculus."
        },
        {
            "question": "What is the difference between supervised and unsupervised learning?",
            "answer": "Supervised learning uses labeled data where the correct output is known, training the model to predict outputs for new inputs. Unsupervised learning works with unlabeled data, finding patterns and structures without predefined outputs."
        },
        {
            "question": "What is overfitting in machine learning?",
            "answer": "Overfitting occurs when a model learns the training data too well, including its noise and outliers, resulting in poor generalization to new, unseen data. It happens when the model is too complex relative to the amount and noisiness of the training data."
        },
        {
            "question": "How do you prevent overfitting?",
            "answer": "Common techniques to prevent overfitting include: using more training data, reducing model complexity, applying regularization (L1/L2), using dropout in neural networks, early stopping, and cross-validation to assess model performance."
        }
    ]
    
    try:
        questions = []
        answers = []
        embeddings = []
        
        for qa in sample_qa:
            embedding = await get_embedding(qa["question"])
            if embedding:
                questions.append(qa["question"])
                answers.append(qa["answer"])
                embeddings.append(embedding)
        
        if embeddings:
            # Normalize embeddings for cosine similarity
            embeddings = normalize_embeddings(embeddings)
            
            entities = [
                questions,
                answers,
                embeddings
            ]
            
            collection.insert(entities)
            # collection.flush() # Wrapper handles flush if needed
            logger.info(f"Seeded {len(questions)} sample Q&A pairs")
            
            # Verify the data was inserted
            # collection.load() # Wrapper handles load if needed
            # num_after = collection.num_entities
            # logger.info(f"Verification: Collection now has {num_after} entities")
            
    except Exception as e:
        logger.error(f"Failed to seed sample data: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())


def normalize_embeddings(embeddings: List[List[float]]) -> List[List[float]]:
    """Normalize embeddings to unit length for cosine similarity."""
    normalized = []
    for emb in embeddings:
        emb_array = np.array(emb)
        norm = np.linalg.norm(emb_array)
        if norm > 0:
            normalized.append((emb_array / norm).tolist())
        else:
            normalized.append(emb)
    return normalized


async def search_similar_qa(collection: MilvusConnection, query_embedding: List[float], top_k: int = 3) -> List[Dict]:
    """Search for similar questions in the cache."""
    try:
        # Wrapper handles load
        # collection.load()
        
        # Normalize query embedding
        query_emb = normalize_embeddings([query_embedding])[0]
        
        logger.info(f"Searching with embedding dimension: {len(query_emb)}")
        logger.info(f"Searching for top {top_k} results")
        
        # Use wrapper search
        results = collection.search(
            query_embedding=query_emb,
            top_k=top_k,
            output_fields=["question", "answer"]
        )
        
        matches = []
        if results:
            # Results is already a list of hits (or list of dicts for Lite)
            logger.info(f"Found {len(results)} results")
            for hit in results:
                # Handle both object (Hit) and dict access depending on what wrapper returns
                # Wrapper uses MilvusClient for local, which returns list of dicts
                # Wrapper uses Collection for remote, which returns Hits object (iterable of Hit)
                
                if isinstance(hit, dict):
                    # Local MilvusClient return style
                    score = hit.get("distance")
                    # Entity fields might be flat in the dict or in 'entity' key?
                    # MilvusClient search returns: [{'id': 1, 'distance': 0.8, 'entity': {'question': '...'}}]
                    entity = hit.get("entity", {})
                    question = entity.get("question")
                    answer = entity.get("answer")
                else:
                    # Remote Collection/Hit style
                    score = hit.distance
                    question = hit.entity.get("question")
                    answer = hit.entity.get("answer")
                
                logger.info(f"Match: score={score:.3f}, question={question[:50] if question else 'None'}...")
                matches.append({
                    "question": question,
                    "answer": answer,
                    "score": score
                })
        else:
            logger.warning("No results returned from search")
        
        return matches
        
    except Exception as e:
        error_msg = str(e).lower()
        logger.error(f"Search failed: {str(e)}")
        
        if "collection not found" not in error_msg:
            import traceback
            logger.error(traceback.format_exc())
        else:
            logger.warning("Collection not found error - will be recovered by endpoint")
        
        return []


# Global collection reference
milvus_collection = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize Milvus on startup."""
    global milvus_collection
    milvus_collection = await init_milvus_collection()
    yield
    # Cleanup on shutdown
    if milvus_collection:
        try:
            connections.disconnect("default")
            logger.info("Disconnected from Milvus")
        except:
            pass


app = FastAPI(title="Q&A Cache Service", lifespan=lifespan)


@app.post("/search", response_model=SearchResponse)
async def search_cache(request: SearchRequest):
    """
    Search for a cached answer using semantic similarity.
    
    Uses query rewriting to generate variations and searches for
    the most similar previously answered question.
    
    Args:
        request: Contains the query string
        
    Returns:
        found: True if a similar question was found above threshold
        answer: The cached answer if found, None otherwise
    """
    global milvus_collection
    
    if not milvus_collection:
        logger.error("Milvus collection not initialized")
        return SearchResponse(found=False, answer=None)
    
    # Verify collection exists in Milvus
    # Using wrapper checks or re-init instead of global utility which often fails for Lite
    if not milvus_collection:
         milvus_collection = await init_milvus_collection()
         if not milvus_collection:
             return SearchResponse(found=False, answer=None)

    # Verify collection is still valid
    try:
        num_entities = milvus_collection.num_entities
        logger.info(f"Collection status: {num_entities} entities available")
    except Exception as e:
        logger.error(f"Collection status check failed: {e}")
        # Try to reconnect
        try:
            logger.info("Attempting to reconnect to collection...")
            milvus_collection = await init_milvus_collection()
            if not milvus_collection:
                 return SearchResponse(found=False, answer=None)

            logger.info("Reconnected to existing collection")
        except Exception as reconnect_error:
            logger.error(f"Failed to reconnect: {reconnect_error}")
            return SearchResponse(found=False, answer=None)
    
    logger.info(f"Searching cache for: {request.query[:100]}...")
    
    # Step 1: Rewrite query to get variations
    query_variations = await rewrite_query(request.query, request.context)
    
    # Step 2: Search with each variation
    best_match = None
    best_score = 0.0
    
    for variation in query_variations:
        # Get embedding for this variation
        embedding = await get_embedding(variation)
        if not embedding:
            continue
        
        # Search for similar questions
        matches = await search_similar_qa(milvus_collection, embedding, top_k=1)
        
        if matches and len(matches) > 0:
            match = matches[0]
            if match["score"] > best_score:
                best_score = match["score"]
                best_match = match
    
    # Step 3: Check if best match exceeds threshold
    if best_match and best_score >= SIMILARITY_THRESHOLD:
        logger.info(f"Cache HIT! Score: {best_score:.3f}, Question: {best_match['question'][:100]}...")
        return SearchResponse(
            found=True,
            answer=best_match["answer"]
        )
    else:
        logger.info(f"Cache MISS. Best score: {best_score:.3f}")
        return SearchResponse(found=False, answer=None)


@app.post("/add")
async def add_to_cache(question: str = Query(..., min_length=1), answer: str = Query(..., min_length=1)):
    """
    Add a new Q&A pair to the cache.
    
    Args:
        question: The question text
        answer: The answer text
        
    Returns:
        Status message
    """
    if not milvus_collection:
        raise HTTPException(status_code=503, detail="Cache service not available")
    
    try:
        # Get embedding
        embedding = await get_embedding(question)
        if not embedding:
            raise HTTPException(status_code=500, detail="Failed to generate embedding")
        
        # Normalize embedding
        embedding = normalize_embeddings([embedding])[0]
        
        # Insert into collection
        entities = [
            [question],
            [answer],
            [embedding]
        ]
        
        milvus_collection.insert(entities)
        milvus_collection.flush()
        
        logger.info(f"Added Q&A to cache: {question[:100]}...")
        return {"status": "success", "message": "Q&A pair added to cache"}
        
    except Exception as e:
        logger.error(f"Failed to add to cache: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    milvus_ok = milvus_collection is not None
    return {
        "status": "healthy" if milvus_ok else "degraded",
        "service": "qa-cache",
        "milvus_connected": milvus_ok
    }


@app.get("/stats")
async def get_stats():
    """Get cache statistics."""
    if not milvus_collection:
        return {"error": "Milvus not connected"}
    
    try:
        num_entities = milvus_collection.num_entities
        return {
            "total_qa_pairs": num_entities,
            "collection_name": QA_DOCS_COLLECTION_NAME,
            "similarity_threshold": SIMILARITY_THRESHOLD
        }
    except Exception as e:
        return {"error": str(e)}


@app.post("/reseed")
async def reseed_collection():
    """Reseed the collection with sample data (for debugging)."""
    if not milvus_collection:
        raise HTTPException(status_code=503, detail="Cache service not available")
    
    try:
        logger.info("Reseeding collection with sample data...")
        await seed_sample_data(milvus_collection)
        num_entities = milvus_collection.num_entities
        return {
            "status": "success",
            "message": f"Collection reseeded. Total entities: {num_entities}"
        }
    except Exception as e:
        logger.error(f"Failed to reseed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    import sys
    
    # Allow custom port via command line argument
    port = 8902
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port: {sys.argv[1]}, using default 8902")
    
    print(f"Starting Q&A Cache Service on port {port}...")
    print(f"Milvus: {MILVUS_HOST}:{QA_DOCS_MILVUS_PORT}")
    print(f"OpenAI API: {OPENAI_BASE_URL}")
    uvicorn.run(app, host="0.0.0.0", port=port)

