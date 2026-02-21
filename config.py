# config.py
import os
from dotenv import load_dotenv

# Load .env file explicitly from the same directory as this file, and override any existing env vars
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, '.env')
load_dotenv(dotenv_path, override=True)

# -----------------------------
# Shared Milvus Configuration
# -----------------------------
LOCAL_MILVUS = os.getenv("LOCAL_MILVUS", "true").lower() == "true"
MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")

# -----------------------------
# RAG Docs Milvus Configuration
# -----------------------------
MILVUS_URI = os.getenv("MILVUS_URI", "").strip()
RAG_DOCS_MILVUS_PORT = os.getenv("RAG_DOCS_MILVUS_PORT", "19530")
RAG_DOCS_MILVUS_HOST = os.getenv("RAG_DOCS_MILVUS_HOST", "127.0.0.1")
MILVUS_RAG_DOCS_DB_NAME = os.getenv("MILVUS_RAG_DOCS_DB_NAME", "thousandDocuments.db")
MILVUS_RAG_DOCS_DB_PATH = os.getenv(
    "MILVUS_RAG_DOCS_DB_PATH",
    "/.gavea/store/chipt/chipt_v2/ChiPT/ai_service/rag_api/knowledge-bases/milvus_docs/thousandDocuments.db"
)
RAG_DOCS_COLLECTION_NAME = os.getenv("RAG_DOCS_COLLECTION_NAME", "test_knowledge")
RAG_DOCS_EMBEDDING_MODEL = os.getenv("RAG_DOCS_EMBEDDING_MODEL", "qwen3-embedding:8b")

# -----------------------------
# OpenAI / AI Service Config
# -----------------------------
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://aiforge.cs.purdue.edu:8001/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
REWRITE_MODEL = os.getenv("REWRITE_MODEL", "gpt-oss:120b")
CHAT_COMPLETION_MODEL = os.getenv("CHAT_COMPLETION_MODEL", "gpt-oss:120b")

# -----------------------------
# Cache / QA Service Config
# -----------------------------
QA_DOCS_MILVUS_PORT = os.getenv("QA_DOCS_MILVUS_PORT", "19531")
QA_DOCS_COLLECTION_NAME = os.getenv("QA_DOCS_COLLECTION_NAME", "qa_cache")
QA_DOCS_EMBEDDING_API_URL = os.getenv("QA_DOCS_EMBEDDING_API_URL", "http://localhost:11434/v1/embeddings")
QA_DOCS_EMBEDDING_MODEL = os.getenv("QA_DOCS_EMBEDDING_MODEL", "qwen3-embedding:8b-q8_0")

CACHE_SERVICE_URL = os.getenv("CACHE_SERVICE_URL", "http://localhost:8902")
CACHE_API_URL = os.getenv("CACHE_API_URL", "http://localhost:8902/search")
AI_API_URL = os.getenv("AI_API_URL", "http://localhost:8901/generate")

# -----------------------------
# Database Config
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./qa_system.db")

# -----------------------------
# Other Services
# -----------------------------
MAIN_QA_URL = os.getenv("MAIN_QA_URL", "http://localhost:8000")
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL", "http://127.0.0.1:8901")
