"""
Standalone FastAPI Milvus API service.

One process owns all MilvusClient connections and the .db file locks.
All Milvus operations are exposed as HTTP endpoints.

Run from ai_service/:
    uvicorn rag_api.milvus_api:app --host 0.0.0.0 --port 8902
"""

import os
import sys
import logging
import time
import uuid
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymilvus import MilvusClient, DataType
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from openai import OpenAI
from chromadb.utils import embedding_functions
from chunking_evaluation.chunking import ClusterSemanticChunker
from tqdm import tqdm

try:
    from .pdf_utils import extract_text_marker
except ImportError:
    from pdf_utils import extract_text_marker

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from config import RAG_DOCS_COLLECTION_NAME

logger = logging.getLogger(__name__)

# ═════════════════════════════════════════════════════════════════════════════
#  FastAPI app
# ═════════════════════════════════════════════════════════════════════════════

app = FastAPI(title="Milvus API Service")

# ═════════════════════════════════════════════════════════════════════════════
#  Constants
# ═════════════════════════════════════════════════════════════════════════════

VEC_FIELD = os.environ.get("MILVUS_VECTOR_FIELD", "embedding")
TEXT_FIELD = os.environ.get("MILVUS_TEXT_FIELD", "text")
TITLE_FIELD = os.environ.get("MILVUS_TITLE_FIELD", "title")
DOCID_FIELD = os.environ.get("MILVUS_DOCID_FIELD", "doc_id")
FILE_UUID_FIELD = os.environ.get("MILVUS_FILE_UUID_FIELD", "file_uuid")
PATH_FIELD = "path"
SOURCE_FILE_FIELD = "source_file"

COLLECTION_NAME_DEFAULT = RAG_DOCS_COLLECTION_NAME

DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_EMBED_MODEL = "qwen3-embedding:8b-fp16"
MAX_TOKEN_LIMIT = 15000
PROCESSED_DOCS_DIR = "processed_docs"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge-bases")

_DEFAULT_CACHE_KEY = "__default__"

# ═════════════════════════════════════════════════════════════════════════════
#  Client cache
# ═════════════════════════════════════════════════════════════════════════════

_client_cache: Dict[str, MilvusClient] = {}


def _get_kb_path(name: str) -> str:
    return os.path.join(DATA_DIR, name, f"{name}.db")


def _get_client(kb_name: Optional[str] = None,
                create_if_missing: bool = False) -> MilvusClient:
    """Return a cached MilvusClient for the given KB."""
    from config import MILVUS_RAG_DOCS_DB_PATH

    cache_key = kb_name or _DEFAULT_CACHE_KEY
    if cache_key in _client_cache:
        return _client_cache[cache_key]

    db_path = _get_kb_path(kb_name) if kb_name else MILVUS_RAG_DOCS_DB_PATH

    if create_if_missing:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    elif not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found: {db_path}")

    client = MilvusClient(db_path)
    _client_cache[cache_key] = client
    logger.info("Created MilvusClient for '%s' at %s", cache_key, db_path)
    return client


# ═════════════════════════════════════════════════════════════════════════════
#  KB path utilities
# ═════════════════════════════════════════════════════════════════════════════

# ═════════════════════════════════════════════════════════════════════════════
#  Collection management
# ═════════════════════════════════════════════════════════════════════════════

def _ensure_collection(client: MilvusClient, collection_name: str):
    """Create the collection schema and vector index if they don't already exist."""
    if client.has_collection(collection_name):
        return

    schema = client.create_schema(auto_id=True, enable_dynamic_field=False)
    schema.add_field(field_name=DOCID_FIELD, datatype=DataType.INT64,
                     is_primary=True, auto_id=True)
    schema.add_field(field_name=TITLE_FIELD, datatype=DataType.VARCHAR, max_length=256)
    schema.add_field(field_name=TEXT_FIELD, datatype=DataType.VARCHAR, max_length=20000)
    schema.add_field(field_name=PATH_FIELD, datatype=DataType.VARCHAR, max_length=1024)
    schema.add_field(field_name=SOURCE_FILE_FIELD, datatype=DataType.VARCHAR, max_length=1024)
    schema.add_field(field_name=FILE_UUID_FIELD, datatype=DataType.VARCHAR, max_length=128)
    schema.add_field(field_name=VEC_FIELD, datatype=DataType.FLOAT_VECTOR, dim=4096)

    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name=VEC_FIELD,
        index_type="AUTOINDEX",
        metric_type="COSINE",
    )

    client.create_collection(
        collection_name=collection_name,
        schema=schema,
        index_params=index_params,
    )
    logger.info("Created collection '%s'", collection_name)


# ═════════════════════════════════════════════════════════════════════════════
#  Ingestion helpers
# ═════════════════════════════════════════════════════════════════════════════

def _count_tokens(text: str) -> int:
    encoder = tiktoken.get_encoding("cl100k_base")
    return len(encoder.encode(text))


def _split_large_file(file_path: str, processed_docs_dir: str) -> List[str]:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        logger.error("Failed to read %s: %s", file_path, e)
        return []

    token_count = _count_tokens(text)
    if token_count <= MAX_TOKEN_LIMIT:
        return [file_path]

    logger.info("File %s has %d tokens (limit %d) -- splitting",
                file_path, token_count, MAX_TOKEN_LIMIT)

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        model_name="gpt-4",
        chunk_size=MAX_TOKEN_LIMIT,
        chunk_overlap=200,
    )
    chunks = text_splitter.split_text(text)

    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    new_file_paths = []
    for i, chunk_content in enumerate(chunks):
        new_filename = f"{name}_{i+1}{ext}"
        new_path = os.path.join(processed_docs_dir, new_filename)
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(chunk_content)
        new_file_paths.append(new_path)

    logger.info("Split %s into %d parts.", file_path, len(new_file_paths))
    return new_file_paths


def _embed_texts(texts: List[str]) -> List[List[float]]:
    import openai as _openai

    client = OpenAI(
        base_url=DEFAULT_OPENAI_BASE_URL,
        api_key=DEFAULT_OPENAI_API_KEY,
    )

    embeddings_out: List[List[float]] = []
    batch_size = 8
    max_retries = 10
    base_delay = 1

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        retries = 0
        while retries < max_retries:
            try:
                response = client.embeddings.create(
                    input=batch, model=DEFAULT_EMBED_MODEL,
                )
                embeddings_out.extend([d.embedding for d in response.data])
                break
            except (_openai.APIConnectionError, _openai.APIStatusError,
                    _openai.RateLimitError) as e:
                retries += 1
                if retries >= max_retries:
                    raise
                delay = min(base_delay * (2 ** (retries - 1)), 30)
                logger.warning("Embedding error (attempt %d/%d): %s -- retrying in %ds",
                               retries, max_retries, e, delay)
                time.sleep(delay)
            except Exception:
                raise

    return embeddings_out


# ═════════════════════════════════════════════════════════════════════════════
#  Pydantic request / response models
# ═════════════════════════════════════════════════════════════════════════════

class SearchRequest(BaseModel):
    kb_name: Optional[str] = None
    vector: List[float]
    limit: int = 30
    output_fields: List[str] = Field(
        default_factory=lambda: ["doc_id", "title", "text"],
    )
    collection_name: Optional[str] = None


class QueryRequest(BaseModel):
    kb_name: Optional[str] = None
    filter_expr: str
    output_fields: List[str] = Field(
        default_factory=lambda: ["doc_id", "title", "text"],
    )
    limit: int = 1
    collection_name: Optional[str] = None


class AddDocumentsRequest(BaseModel):
    kb_name: str
    file_paths: List[str]
    collection_name: Optional[str] = None


class CreateCollectionRequest(BaseModel):
    kb_name: str
    collection_name: Optional[str] = None


class CreateKBRequest(BaseModel):
    name: str
    collection_name: Optional[str] = None


class RemoveDocumentRequest(BaseModel):
    kb_name: str
    filename: str
    collection_name: Optional[str] = None


# ═════════════════════════════════════════════════════════════════════════════
#  Endpoints
# ═════════════════════════════════════════════════════════════════════════════

@app.post("/search")
def search(req: SearchRequest):
    """Vector similarity search (ANN)."""
    try:
        client = _get_client(req.kb_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    col = req.collection_name or COLLECTION_NAME_DEFAULT
    search_params = {
        "metric_type": os.environ.get("MILVUS_METRIC", "COSINE"),
        "params": {},
    }

    try:
        results = client.search(
            collection_name=col,
            data=[req.vector],
            limit=req.limit,
            output_fields=req.output_fields,
            search_params=search_params,
        )
        hits = results[0] if results else []
        return {"results": hits}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
def query(req: QueryRequest):
    """Scalar filter query (like SQL WHERE)."""
    try:
        client = _get_client(req.kb_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    col = req.collection_name or COLLECTION_NAME_DEFAULT

    try:
        results = client.query(
            collection_name=col,
            filter=req.filter_expr,
            output_fields=req.output_fields,
            limit=req.limit,
        )
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/add_documents")
def add_documents(req: AddDocumentsRequest):
    """Full ingestion pipeline: PDF -> markdown -> split -> chunk -> embed -> insert."""
    try:
        client = _get_client(req.kb_name, create_if_missing=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    col = req.collection_name or COLLECTION_NAME_DEFAULT
    _ensure_collection(client, col)

    db_path = _get_kb_path(req.kb_name)
    db_dir = os.path.dirname(os.path.abspath(db_path))
    processed_docs_dir = os.path.join(db_dir, PROCESSED_DOCS_DIR)
    os.makedirs(processed_docs_dir, exist_ok=True)

    effective_api_key = DEFAULT_OPENAI_API_KEY or "dummy-key"
    emb_fn = embedding_functions.OpenAIEmbeddingFunction(
        api_key=effective_api_key,
        model_name=DEFAULT_EMBED_MODEL,
        api_base=DEFAULT_OPENAI_BASE_URL,
    )

    final_files: List[dict] = []
    for fp in req.file_paths:
        if not os.path.exists(fp):
            logger.warning("File not found: %s", fp)
            continue

        file_name = os.path.basename(fp)
        existing = client.query(
            collection_name=col,
            filter=f"{TITLE_FIELD} == '{file_name}'",
            output_fields=[DOCID_FIELD],
            limit=1,
        )
        if existing:
            logger.info("Skipping %s (already exists in KB).", file_name)
            continue

        processing_path = fp
        if fp.lower().endswith('.pdf'):
            logger.info("Converting PDF to Markdown: %s", fp)
            md_text = extract_text_marker(fp)
            if not md_text:
                logger.warning("Failed to extract text from %s", fp)
                continue
            md_filename = os.path.splitext(file_name)[0] + ".md"
            md_path = os.path.join(processed_docs_dir, md_filename)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_text)
            processing_path = md_path

        resulting_paths = _split_large_file(processing_path, processed_docs_dir)
        resulting_paths = [os.path.abspath(p) for p in resulting_paths]
        file_uuid = str(uuid.uuid4())

        for p in resulting_paths:
            final_files.append({
                "process_path": p,
                "source_path": os.path.abspath(fp),
                "file_uuid": file_uuid,
                "is_split": len(resulting_paths) > 1,
            })

    cluster_chunker = ClusterSemanticChunker(
        emb_fn,
        max_chunk_size=2000,
        min_chunk_size=100,
    )

    data_to_insert: List[dict] = []
    for item in tqdm(final_files, desc="Processing files"):
        fpath = item["process_path"]
        source_path = item["source_path"]
        file_uuid_val = item["file_uuid"]

        try:
            loader = UnstructuredMarkdownLoader(fpath)
            docs = loader.load()
        except Exception as e:
            logger.error("Failed to load %s: %s", fpath, e)
            continue

        for doc in docs:
            chunk_texts = cluster_chunker.split_text(doc.page_content)
            if not chunk_texts:
                continue

            chunk_embeddings = _embed_texts(chunk_texts)
            for i, text in enumerate(chunk_texts):
                data_to_insert.append({
                    TITLE_FIELD: os.path.basename(source_path),
                    TEXT_FIELD: text,
                    PATH_FIELD: fpath,
                    SOURCE_FILE_FIELD: source_path,
                    FILE_UUID_FIELD: file_uuid_val,
                    VEC_FIELD: chunk_embeddings[i],
                })

    chunks_inserted = 0
    if data_to_insert:
        client.insert(col, data=data_to_insert)
        chunks_inserted = len(data_to_insert)
        logger.info("Inserted %d chunks into %s", chunks_inserted, col)

    return {"status": "success", "chunks_inserted": chunks_inserted}


@app.post("/create_collection")
def create_collection(req: CreateCollectionRequest):
    """Explicitly create a collection schema + index for a KB."""
    try:
        client = _get_client(req.kb_name, create_if_missing=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    col = req.collection_name or COLLECTION_NAME_DEFAULT
    _ensure_collection(client, col)
    return {"status": "success", "message": f"Collection '{col}' ready"}


@app.post("/create_kb")
def create_kb(req: CreateKBRequest):
    """Create a new KB: directory + .db file + collection schema."""
    kb_dir = os.path.join(DATA_DIR, req.name)
    os.makedirs(kb_dir, exist_ok=True)

    col = req.collection_name or COLLECTION_NAME_DEFAULT
    try:
        client = _get_client(req.name, create_if_missing=True)
        _ensure_collection(client, col)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success", "message": f"KB '{req.name}' created with collection '{col}'"}


@app.delete("/remove_document")
def remove_document(req: RemoveDocumentRequest):
    """Remove all chunks for a source document and clean up split files."""
    try:
        client = _get_client(req.kb_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    col = req.collection_name or COLLECTION_NAME_DEFAULT
    abs_path = os.path.abspath(req.filename)
    filter_expr = f'{SOURCE_FILE_FIELD} == "{abs_path}"'

    db_path = _get_kb_path(req.kb_name)
    db_dir = os.path.dirname(os.path.abspath(db_path))
    processed_docs_dir = os.path.join(db_dir, PROCESSED_DOCS_DIR)

    res = client.query(
        collection_name=col,
        filter=filter_expr,
        output_fields=[PATH_FIELD],
        limit=10000,
    )

    if not res:
        return {"status": "success", "message": "No matching documents found"}

    files_to_delete = {
        item.get(PATH_FIELD) for item in res
        if item.get(PATH_FIELD, "").startswith(os.path.abspath(processed_docs_dir))
    }

    client.delete(collection_name=col, filter=filter_expr)

    for p in files_to_delete:
        if os.path.exists(p):
            try:
                os.remove(p)
            except OSError as e:
                logger.warning("Failed to remove %s: %s", p, e)

    return {"status": "success", "message": f"Removed document '{req.filename}'"}


@app.get("/list_files/{kb_name}")
def list_files(kb_name: str, collection_name: Optional[str] = None):
    """List unique source-file paths stored in a KB's collection."""
    try:
        client = _get_client(kb_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    col = collection_name or COLLECTION_NAME_DEFAULT

    try:
        results = client.query(
            collection_name=col,
            filter="doc_id >= 0",
            output_fields=[SOURCE_FILE_FIELD],
        )
        sources = list({r[SOURCE_FILE_FIELD] for r in results if SOURCE_FILE_FIELD in r})
        return {"files": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/file_by_uuid/{kb_name}/{file_uuid}")
def file_by_uuid(kb_name: str, file_uuid: str,
                 collection_name: Optional[str] = None):
    """Look up the source file path for a given file UUID."""
    try:
        client = _get_client(kb_name)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    col = collection_name or COLLECTION_NAME_DEFAULT

    results = client.query(
        collection_name=col,
        filter=f'{FILE_UUID_FIELD} == "{file_uuid}"',
        output_fields=[SOURCE_FILE_FIELD],
        limit=1,
    )

    if results:
        return {"source_path": results[0].get(SOURCE_FILE_FIELD)}
    raise HTTPException(status_code=404, detail=f"UUID '{file_uuid}' not found")


# ═════════════════════════════════════════════════════════════════════════════
#  Standalone runner
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8903)
