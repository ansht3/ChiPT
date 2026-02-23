"""
Unified Milvus connection and vector database management module.

All Milvus operations go through ``get_client_object()`` from the cache layer
so that every knowledge base is backed by exactly one ``MilvusClient`` instance
shared across the RAG query path and the document-management path.
"""

import argparse
import os
import logging
import time
import uuid
from typing import List, Optional, Union
from dataclasses import dataclass

from pymilvus import connections, Collection, db, MilvusClient, DataType
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from openai import OpenAI
from chromadb.utils import embedding_functions
from chunking_evaluation.chunking import ClusterSemanticChunker
from tqdm import tqdm

try:
    from .pdf_utils import extract_text_marker
except ImportError:
    from pdf_utils import extract_text_marker

from config import (
    LOCAL_MILVUS, MILVUS_RAG_DOCS_DB_NAME, MILVUS_RAG_DOCS_DB_PATH,
    MILVUS_URI, RAG_DOCS_COLLECTION_NAME, RAG_DOCS_MILVUS_PORT,
    RAG_DOCS_MILVUS_HOST
)

# Re-export everything from the cache layer so existing callers keep working
from .milvus_client_cache import (          # noqa: F401 – re-exports
    get_client_object, _ensure_db_unlocked,
    VEC_FIELD, TEXT_FIELD, TITLE_FIELD, DOCID_FIELD, FILE_UUID_FIELD,
    PATH_FIELD, SOURCE_FILE_FIELD,
    COLLECTION_NAME_DEFAULT, DEFAULT_OPENAI_BASE_URL, DEFAULT_OPENAI_API_KEY,
    DEFAULT_EMBED_MODEL, MAX_TOKEN_LIMIT, PROCESSED_DOCS_DIR, DATA_DIR,
    get_kb_path, list_knowledge_bases, create_kb_dir,
)

logger = logging.getLogger(__name__)

# Tracks which KB names have already passed collection + index verification
# so we only pay the cost once per process lifetime.
_verified_kbs: set = set()


# ═════════════════════════════════════════════════════════════════════════════
#  One-time verification (collection exists + index present)
# ═════════════════════════════════════════════════════════════════════════════

def _verify_and_cache(client: MilvusClient, kb_name: str,
                      collection_name: str = None):
    """Check collection existence and vector index, but only once per KB.

    After the first successful check the *kb_name* is added to
    ``_verified_kbs`` and all subsequent calls are no-ops.
    """
    key = kb_name or "__default__"
    if key in _verified_kbs:
        return

    col = collection_name or RAG_DOCS_COLLECTION_NAME
    collections = client.list_collections()
    if col not in collections:
        raise ValueError(
            f"Collection '{col}' does not exist in the database"
        )

    # Verify / create vector index
    try:
        collection_info = client.describe_collection(col)
        has_index = any(
            idx.get('field_name') == VEC_FIELD
            for idx in collection_info.get('indexes', [])
        )
        if not has_index:
            logger.info("[Milvus] Creating index on field '%s'", VEC_FIELD)
            index_params = client.prepare_index_params()
            index_params.add_index(
                field_name=VEC_FIELD,
                index_type="AUTOINDEX",
                metric_type=os.environ.get("MILVUS_METRIC", "COSINE"),
            )
            client.create_index(
                collection_name=col,
                index_params=index_params,
            )
            logger.info("[Milvus] Index created successfully")
    except Exception as e:
        logger.warning("Could not verify/create index: %s", e)

    stats = client.get_collection_stats(collection_name=col)
    logger.info("[Milvus] KB '%s' verified – collection='%s', rows=%s",
                key, col, stats.get('row_count', 'unknown'))

    _verified_kbs.add(key)


# ═════════════════════════════════════════════════════════════════════════════
#  MilvusConnection – thin wrapper for the RAG query path
# ═════════════════════════════════════════════════════════════════════════════

@dataclass
class MilvusConnection:
    """Abstraction over local ``MilvusClient`` and remote ``Collection``.

    This wrapper is used exclusively by the **query** path
    (``_milvus_connect`` → ``rag_answer``).  Collection and index
    verification happens once in ``_milvus_connect`` via
    ``_verify_and_cache``, so there is no work done in ``__post_init__``.
    """
    client: Union[MilvusClient, Collection]
    is_local: bool
    collection_name: str

    # ── search ───────────────────────────────────────────────────────────

    def search(
        self,
        query_embedding: List[float],
        top_k: int = 30,
        output_fields: List[str] = None,
    ) -> List:
        if output_fields is None:
            output_fields = [DOCID_FIELD, TITLE_FIELD, TEXT_FIELD]

        if self.is_local:
            search_params = {
                "metric_type": os.environ.get("MILVUS_METRIC", "COSINE"),
                "params": {},
            }
            results = self.client.search(
                collection_name=self.collection_name,
                data=[query_embedding],
                limit=top_k,
                output_fields=output_fields,
                search_params=search_params,
            )
            return results[0] if results else []

        search_params = {
            "metric_type": os.environ.get("MILVUS_METRIC", "IP"),
            "params": {"nprobe": 10},
        }
        results = self.client.search(
            data=[query_embedding],
            anns_field=VEC_FIELD,
            param=search_params,
            limit=top_k,
            output_fields=output_fields,
        )
        return results[0] if results else []

    # ── load ─────────────────────────────────────────────────────────────

    def load(self):
        if not self.is_local:
            try:
                self.client.load()
            except Exception as e:
                logger.debug("Collection load failed or not needed: %s", e)

    # ── query ────────────────────────────────────────────────────────────

    def query(self, expr: str, output_fields: List[str] = None, limit: int = 1):
        if output_fields is None:
            output_fields = [DOCID_FIELD, TITLE_FIELD, TEXT_FIELD]

        if self.is_local:
            return self.client.query(
                collection_name=self.collection_name,
                filter=expr,
                output_fields=output_fields,
                limit=limit,
            )
        return self.client.query(
            expr=expr,
            output_fields=output_fields,
            limit=limit,
        )


# ═════════════════════════════════════════════════════════════════════════════
#  _milvus_connect – factory for the RAG query path (uses cache)
# ═════════════════════════════════════════════════════════════════════════════

def _milvus_connect(kb_name: str = None) -> MilvusConnection:
    """Return a ``MilvusConnection`` backed by a cached client.

    Collection and index verification happens **once per KB** via
    ``_verify_and_cache``; subsequent calls skip straight to returning
    the cached wrapper.
    """
    if LOCAL_MILVUS:
        client = get_client_object(kb_name)
        _verify_and_cache(client, kb_name)
        return MilvusConnection(
            client=client, is_local=True,
            collection_name=RAG_DOCS_COLLECTION_NAME,
        )

    # Remote Milvus connection with URI → host:port fallback
    try:
        if MILVUS_URI:
            logger.info("Attempting to connect via URI: %s", MILVUS_URI)
            connections.connect(alias="default", uri=MILVUS_URI)
        else:
            logger.info("Attempting to connect via host:port (%s:%s)",
                        RAG_DOCS_MILVUS_HOST, RAG_DOCS_MILVUS_PORT)
            connections.connect(alias="default",
                                host=RAG_DOCS_MILVUS_HOST,
                                port=RAG_DOCS_MILVUS_PORT)

        if MILVUS_RAG_DOCS_DB_NAME and db is not None:
            try:
                db.using_database(MILVUS_RAG_DOCS_DB_NAME)
            except Exception as e:
                logger.warning("Could not switch to database %s: %s",
                               MILVUS_RAG_DOCS_DB_NAME, e)

        collection = Collection(RAG_DOCS_COLLECTION_NAME)
        return MilvusConnection(
            client=collection, is_local=False,
            collection_name=RAG_DOCS_COLLECTION_NAME,
        )

    except Exception as e:
        logger.error("Error connecting to Milvus: %s", e)

        if MILVUS_URI:
            try:
                logger.info("URI failed – falling back to host:port (%s:%s)",
                            RAG_DOCS_MILVUS_HOST, RAG_DOCS_MILVUS_PORT)
                connections.connect(alias="default",
                                    host=RAG_DOCS_MILVUS_HOST,
                                    port=RAG_DOCS_MILVUS_PORT)

                if MILVUS_RAG_DOCS_DB_NAME and db is not None:
                    try:
                        db.using_database(MILVUS_RAG_DOCS_DB_NAME)
                    except Exception as db_err:
                        logger.warning("Could not switch to database %s: %s",
                                       MILVUS_RAG_DOCS_DB_NAME, db_err)

                collection = Collection(RAG_DOCS_COLLECTION_NAME)
                return MilvusConnection(
                    client=collection, is_local=False,
                    collection_name=RAG_DOCS_COLLECTION_NAME,
                )
            except Exception as fallback_err:
                logger.error("Fallback connection also failed: %s", fallback_err)
                raise
        else:
            raise


# ═════════════════════════════════════════════════════════════════════════════
#  VectorDatabaseManager – KB CRUD & ingestion (uses cached client)
# ═════════════════════════════════════════════════════════════════════════════

class VectorDatabaseManager:
    """Manages document ingestion, deletion and lookup for a single KB.

    The underlying ``MilvusClient`` is obtained from ``get_client_object()``
    so that all callers operating on the same KB share one connection.

    Parameters
    ----------
    kb_name : str
        Knowledge-base name (e.g. ``"physics"``).
    collection_name : str
        Milvus collection to operate on.
    create_if_missing : bool
        * ``True``  – create the ``.db`` file **and** the collection schema
          if they don't exist.  Use for **write** endpoints (file upload).
        * ``False`` (default) – expect the DB to already exist.  Use for
          **read** endpoints (list files, UUID lookup, download).
    """

    def __init__(self, kb_name: str,
                 collection_name: str = COLLECTION_NAME_DEFAULT,
                 create_if_missing: bool = False):
        self.kb_name = kb_name
        self.collection_name = collection_name
        self.db_path = get_kb_path(kb_name)

        db_dir = os.path.dirname(os.path.abspath(self.db_path))
        self.processed_docs_dir = os.path.join(db_dir, PROCESSED_DOCS_DIR)
        os.makedirs(self.processed_docs_dir, exist_ok=True)

        self.client: MilvusClient = get_client_object(
            kb_name, create_if_missing=create_if_missing,
        )

        if create_if_missing:
            self._ensure_collection()

        self.openai_client = OpenAI(
            base_url=DEFAULT_OPENAI_BASE_URL,
            api_key=DEFAULT_OPENAI_API_KEY,
        )

        effective_api_key = DEFAULT_OPENAI_API_KEY or "dummy-key"
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=effective_api_key,
            model_name=DEFAULT_EMBED_MODEL,
            api_base=DEFAULT_OPENAI_BASE_URL,
        )

    # ── collection creation (idempotent) ─────────────────────────────────

    def _ensure_collection(self):
        """Create the collection schema and vector index if they don't exist."""
        if self.client.has_collection(self.collection_name):
            return

        schema = self.client.create_schema(auto_id=True, enable_dynamic_field=False)
        schema.add_field(field_name=DOCID_FIELD, datatype=DataType.INT64,
                         is_primary=True, auto_id=True)
        schema.add_field(field_name=TITLE_FIELD, datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name=TEXT_FIELD, datatype=DataType.VARCHAR, max_length=20000)
        schema.add_field(field_name=PATH_FIELD, datatype=DataType.VARCHAR, max_length=1024)
        schema.add_field(field_name=SOURCE_FILE_FIELD, datatype=DataType.VARCHAR, max_length=1024)
        schema.add_field(field_name=FILE_UUID_FIELD, datatype=DataType.VARCHAR, max_length=128)
        schema.add_field(field_name=VEC_FIELD, datatype=DataType.FLOAT_VECTOR, dim=4096)

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name=VEC_FIELD,
            index_type="AUTOINDEX",
            metric_type="COSINE",
        )

        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params,
        )
        logger.info("Created collection '%s'", self.collection_name)

    # ── ingestion helpers ────────────────────────────────────────────────

    def _count_tokens(self, text: str) -> int:
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

    def _split_large_file(self, file_path: str) -> List[str]:
        """Split a file that exceeds MAX_TOKEN_LIMIT into smaller parts."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.error("Failed to read %s: %s", file_path, e)
            return []

        token_count = self._count_tokens(text)
        if token_count <= MAX_TOKEN_LIMIT:
            return [file_path]

        logger.info("File %s has %d tokens (limit %d) – splitting…",
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
            new_path = os.path.join(self.processed_docs_dir, new_filename)
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(chunk_content)
            new_file_paths.append(new_path)

        logger.info("Split %s into %d parts.", file_path, len(new_file_paths))
        return new_file_paths

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed texts using the OpenAI-compatible API with exponential backoff."""
        import openai

        embeddings: List[List[float]] = []
        batch_size = 8
        max_retries = 10
        base_delay = 1

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            retries = 0
            while retries < max_retries:
                try:
                    response = self.openai_client.embeddings.create(
                        input=batch, model=DEFAULT_EMBED_MODEL,
                    )
                    embeddings.extend([d.embedding for d in response.data])
                    break
                except (openai.APIConnectionError, openai.APIStatusError,
                        openai.RateLimitError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error("Embedding failed for batch %d after %d retries: %s",
                                     i, max_retries, e)
                        raise
                    delay = min(base_delay * (2 ** (retries - 1)), 30)
                    logger.warning("Embedding error (attempt %d/%d): %s – retrying in %ds…",
                                   retries, max_retries, e, delay)
                    time.sleep(delay)
                except Exception as e:
                    logger.error("Unexpected embedding error: %s", e)
                    raise

        return embeddings

    # ── document CRUD ────────────────────────────────────────────────────

    def add_documents(self, file_paths: List[str]):
        """Process files (PDF conversion, splitting, chunking, embedding) and insert.

        The collection is guaranteed to exist because ``__init__`` was called
        with ``create_if_missing=True`` which runs ``_ensure_collection()``.
        """
        final_files_to_process: List[dict] = []
        for fp in file_paths:
            if not os.path.exists(fp):
                logger.warning("File not found: %s", fp)
                continue

            file_name = os.path.basename(fp)
            existing = self.client.query(
                collection_name=self.collection_name,
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
                md_path = os.path.join(self.processed_docs_dir, md_filename)
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(md_text)
                processing_path = md_path
                logger.info("Saved converted markdown to %s", processing_path)

            resulting_paths = self._split_large_file(processing_path)
            resulting_paths = [os.path.abspath(p) for p in resulting_paths]
            file_uuid = str(uuid.uuid4())

            for p in resulting_paths:
                final_files_to_process.append({
                    "process_path": p,
                    "source_path": os.path.abspath(fp),
                    "file_uuid": file_uuid,
                    "is_split": len(resulting_paths) > 1,
                })

        cluster_chunker = ClusterSemanticChunker(
            self.embedding_function,
            max_chunk_size=2000,
            min_chunk_size=100,
        )

        data_to_insert: List[dict] = []
        for item in tqdm(final_files_to_process, desc="Processing files"):
            fpath = item["process_path"]
            source_path = item["source_path"]
            file_uuid = item["file_uuid"]

            logger.info("Processing %s…", fpath)
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

                chunk_embeddings = self._embed_texts(chunk_texts)
                for i, text in enumerate(chunk_texts):
                    data_to_insert.append({
                        TITLE_FIELD: os.path.basename(source_path),
                        TEXT_FIELD: text,
                        PATH_FIELD: fpath,
                        SOURCE_FILE_FIELD: source_path,
                        FILE_UUID_FIELD: file_uuid,
                        VEC_FIELD: chunk_embeddings[i],
                    })

        if data_to_insert:
            logger.info("Inserting %d chunks into %s…",
                        len(data_to_insert), self.collection_name)
            self.client.insert(self.collection_name, data=data_to_insert)
            logger.info("Insertion complete.")
        else:
            logger.warning("No data to insert.")

    def remove_document(self, filename: str):
        """Remove all chunks for a source document and clean up split files."""
        abs_path = os.path.abspath(filename)
        filter_expr = f'{SOURCE_FILE_FIELD} == "{abs_path}"'

        res = self.client.query(
            collection_name=self.collection_name,
            filter=filter_expr,
            output_fields=[PATH_FIELD],
            limit=10000,
        )

        if not res:
            logger.warning("No documents found for source: %s", abs_path)
            return

        files_to_delete = {
            item.get(PATH_FIELD) for item in res
            if item.get(PATH_FIELD, "").startswith(
                os.path.abspath(self.processed_docs_dir))
        }

        logger.info("Deleting entries for %s…", abs_path)
        self.client.delete(collection_name=self.collection_name,
                           filter=filter_expr)
        logger.info("Deletion from DB complete.")

        for p in files_to_delete:
            if os.path.exists(p):
                try:
                    os.remove(p)
                    logger.info("Removed split file: %s", p)
                except OSError as e:
                    logger.warning("Failed to remove %s: %s", p, e)

    def get_file_list(self) -> List[str]:
        """Return unique source-file paths stored in the collection."""
        results = self.client.query(
            collection_name=self.collection_name,
            filter="doc_id >= 0",
            output_fields=[SOURCE_FILE_FIELD],
        )
        sources = {r[SOURCE_FILE_FIELD] for r in results if SOURCE_FILE_FIELD in r}
        return list(sources)

    def get_file_path_by_uuid(self, file_uuid: str) -> Optional[str]:
        """Look up the source file path for a given file UUID."""
        results = self.client.query(
            collection_name=self.collection_name,
            filter=f'{FILE_UUID_FIELD} == "{file_uuid}"',
            output_fields=[SOURCE_FILE_FIELD],
            limit=1,
        )
        if results:
            return results[0].get(SOURCE_FILE_FIELD)
        return None


# ═════════════════════════════════════════════════════════════════════════════
#  CLI entry point
# ═════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Vector Database Management Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--kb-name", required=True,
                               help="Knowledge base name (e.g. my_kb)")
    parent_parser.add_argument("--collection", default=COLLECTION_NAME_DEFAULT,
                               help=f"Collection name (default: {COLLECTION_NAME_DEFAULT})")

    subparsers.add_parser("create", parents=[parent_parser],
                          help="Create a new empty database")

    add_parser = subparsers.add_parser("add", parents=[parent_parser],
                                       help="Add documents to the database")
    add_parser.add_argument("--files", nargs="+", required=True,
                            help="List of files to add")

    remove_parser = subparsers.add_parser("remove", parents=[parent_parser],
                                          help="Remove a document from the database")
    remove_parser.add_argument("--file", required=True,
                               help="Original document path to remove")

    subparsers.add_parser("list", parents=[parent_parser],
                          help="List source files in the database")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    is_write = args.command in ("create", "add", "remove")
    manager = VectorDatabaseManager(
        args.kb_name, args.collection, create_if_missing=is_write,
    )

    if args.command == "create":
        print(f"Database for KB '{args.kb_name}' created successfully.")
    elif args.command == "add":
        print(f"Adding {len(args.files)} files...")
        manager.add_documents(args.files)
        print("Done.")
    elif args.command == "remove":
        print(f"Removing {args.file}...")
        manager.remove_document(args.file)
        print("Done.")
    elif args.command == "list":
        files = manager.get_file_list()
        print("\nSource Files in Database:")
        for f in files:
            print(f"- {f}")


if __name__ == "__main__":
    main()
