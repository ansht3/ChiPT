import argparse
import os
import shutil
import logging
import time
import glob
from typing import List, Dict, Optional, Tuple
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
from pymilvus import MilvusClient, DataType
from openai import OpenAI
from chromadb.utils import embedding_functions
from chunking_evaluation.chunking import ClusterSemanticChunker
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants (Default values, can be overridden via env vars or args)
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "http://aiforge.cs.purdue.edu:8001/v1")
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "aiforge-65H3xnZtz757QJUJnGTARKaHmgb8_iMFAmS4T5VJup8")
DEFAULT_EMBED_MODEL = "qwen3-embedding:8b-fp16"
MAX_TOKEN_LIMIT = 15000
PROCESSED_DOCS_DIR = "processed_docs" # Deprecated, keeping for backward compat if needed
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge-bases")

# Milvus Constants
COLLECTION_NAME_DEFAULT = "test_knowledge"
VEC_FIELD = "embedding"
TEXT_FIELD = "text"
TITLE_FIELD = "title"
DOCID_FIELD = "doc_id"
PATH_FIELD = "path"
SOURCE_FILE_FIELD = "source_file" # New field for tracking original file

class VectorDatabaseManager:
    def __init__(self, db_path: str, collection_name: str = COLLECTION_NAME_DEFAULT):
        self.db_path = db_path
        self.collection_name = collection_name
        self.client = None
        
        # Determine the processed_docs directory based on the DB file location
        # If db_path is "ai_service/rag_api/knowledge-bases/my_kb/my_kb.db", 
        # then processed_docs should be "ai_service/rag_api/knowledge-bases/my_kb/processed_docs"
        db_dir = os.path.dirname(os.path.abspath(db_path))
        self.processed_docs_dir = os.path.join(db_dir, PROCESSED_DOCS_DIR)
        
        # Ensure processed docs directory exists
        os.makedirs(self.processed_docs_dir, exist_ok=True)
        
        # Initialize OpenAI client for embeddings (used by manual embedding calls if needed)
        self.openai_client = OpenAI(
            base_url=DEFAULT_OPENAI_BASE_URL,
            api_key=DEFAULT_OPENAI_API_KEY
        )

        # Initialize Embedding Function for ClusterSemanticChunker
        # Fallback to dummy key if not set, required for some libraries even with local base_url
        effective_api_key = DEFAULT_OPENAI_API_KEY or "dummy-key"
        
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=effective_api_key,
            model_name=DEFAULT_EMBED_MODEL,
            api_base=DEFAULT_OPENAI_BASE_URL
        )

    def _ensure_db_unlocked(self, max_wait: int = 5):
        """Ensure the database file is not locked."""
        # This is a simplified version of the lock check from the notebook
        db_file = os.path.abspath(self.db_path)
        if not os.path.exists(db_file):
            return

        for attempt in range(max_wait):
            try:
                test_file = f"{db_file}.lock_test_{int(time.time())}"
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                return
            except (IOError, PermissionError, OSError):
                if attempt < max_wait - 1:
                    logger.info(f"Waiting for DB lock... ({attempt + 1}/{max_wait})")
                    time.sleep(1)
                else:
                    logger.warning(f"Database {self.db_path} might be locked.")

    def connect(self):
        """Connect to the Milvus Lite database."""
        self._ensure_db_unlocked()
        os.makedirs(os.path.dirname(os.path.abspath(self.db_path)), exist_ok=True)
        self.client = MilvusClient(self.db_path)
        logger.info(f"Connected to Milvus Lite at {self.db_path}")

    def create_database(self):
        """Create the database schema and index if it doesn't exist."""
        if not self.client:
            self.connect()

        if self.client.has_collection(self.collection_name):
            logger.info(f"Collection '{self.collection_name}' already exists.")
            return

        # Create schema
        schema = self.client.create_schema(
            auto_id=True,
            enable_dynamic_field=False,
        )
        
        # Add fields
        schema.add_field(field_name=DOCID_FIELD, datatype=DataType.INT64, is_primary=True, auto_id=True)
        schema.add_field(field_name=TITLE_FIELD, datatype=DataType.VARCHAR, max_length=256)
        schema.add_field(field_name=TEXT_FIELD, datatype=DataType.VARCHAR, max_length=20000) # Increased limit slightly
        schema.add_field(field_name=PATH_FIELD, datatype=DataType.VARCHAR, max_length=1024)
        schema.add_field(field_name=SOURCE_FILE_FIELD, datatype=DataType.VARCHAR, max_length=1024) # New field
        schema.add_field(field_name=VEC_FIELD, datatype=DataType.FLOAT_VECTOR, dim=4096) 

        # Create index params
        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name=VEC_FIELD,
            index_type="AUTOINDEX",
            metric_type="COSINE",
        )

        # Create collection
        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )
        logger.info(f"Created collection '{self.collection_name}'")

    def _count_tokens(self, text: str) -> int:
        """Count tokens using cl100k_base encoding."""
        encoder = tiktoken.get_encoding("cl100k_base")
        return len(encoder.encode(text))

    def _split_large_file(self, file_path: str) -> List[str]:
        """
        Check if file is too large. If so, split into smaller files 
        and save them to PROCESSED_DOCS_DIR.
        Returns list of paths to process (either original or split parts).
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            logger.error(f"Failed to read {file_path}: {e}")
            return []

        token_count = self._count_tokens(text)
        
        if token_count <= MAX_TOKEN_LIMIT:
            return [file_path]
        
        logger.info(f"File {file_path} has {token_count} tokens (Limit: {MAX_TOKEN_LIMIT}). Splitting...")
        
        # Split text
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name="gpt-4",
            chunk_size=MAX_TOKEN_LIMIT,
            chunk_overlap=200 # Small overlap for continuity
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
            
        logger.info(f"Split {file_path} into {len(new_file_paths)} parts.")
        return new_file_paths

    def _embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of texts using OpenAI API with retry logic."""
        embeddings = []
        batch_size = 8
        max_retries = 10  # Increased from 5
        base_delay = 1    # Start faster

        import openai

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            retries = 0
            while retries < max_retries:
                try:
                    response = self.openai_client.embeddings.create(
                        input=batch,
                        model=DEFAULT_EMBED_MODEL
                    )
                    embeddings.extend([d.embedding for d in response.data])
                    break # Success, exit retry loop
                except (openai.APIConnectionError, openai.APIStatusError, openai.RateLimitError) as e:
                    retries += 1
                    if retries >= max_retries:
                        logger.error(f"Embedding failed for batch {i} after {max_retries} retries: {e}")
                        raise e
                    
                    # Exponential backoff with jitter or cap? 
                    # Cap at 30s
                    delay = min(base_delay * (2 ** (retries - 1)), 30)
                    logger.warning(f"Embedding error (attempt {retries}/{max_retries}): {e}. Retrying in {delay}s...")
                    time.sleep(delay)
                except Exception as e:
                    # Non-retryable error? Or just retry anyway?
                    # Generally unknown errors should probably not be retried indefinitely, 
                    # but for stability let's retry a few times?
                    # Actually, if it's a code error (ValueError), retrying won't help.
                    # If it's network, it's covered above.
                    logger.error(f"Unexpected embedding error: {e}")
                    raise e
                    
        return embeddings

    def add_documents(self, file_paths: List[str]):
        """
        Process and add documents to the Knowledge Base.
        Handles checking duplication or recreating? 
        Current logic: Just inserts. Deletion should be called before if update is needed.
        """
        if not self.client:
            self.connect()
            self.create_database() # Ensure DB exists

        processed_files_map = {} # Map original path to list of processed paths

        # 1. Pre-process files (Split if needed)
        final_files_to_process = []
        for fp in file_paths:
            if not os.path.exists(fp):
                logger.warning(f"File not found: {fp}")
                continue
            
            # Duplicate detection
            file_name = os.path.basename(fp)
            # Check if file is already in DB
            # Use query with count or similar. Milvus Lite supports query.
            # We filter by source_path (absolute) or title? Title (basename) is safer if user moves files.
            # But let's use TITLE_FIELD match.
            existing = self.client.query(
                collection_name=self.collection_name,
                filter=f"{TITLE_FIELD} == '{file_name}'",
                output_fields=[DOCID_FIELD],
                limit=1
            )
            if existing:
                logger.info(f"Skipping {file_name} (already exists in KB).")
                continue

            # This returns either [original_path] or [split_path_1, split_path_2, ...]
            resulting_paths = self._split_large_file(fp)
            
            # Verify paths are absolute
            resulting_paths = [os.path.abspath(p) for p in resulting_paths]
            
            # Map original file (input arg) to the actual files being inserted
            # We store the ORIGINAL file path in the 'source_file' field
            # So we can delete all chunks related to 'fp' later
            for p in resulting_paths:
                final_files_to_process.append({
                    "process_path": p,
                    "source_path": os.path.abspath(fp),
                    "is_split": len(resulting_paths) > 1
                })

        # 2. Chunking and Embedding
        # ClusterSemanticChunker configuration
        cluster_chunker = ClusterSemanticChunker(
            self.embedding_function, 
            max_chunk_size=2000, # As per notebook usage
            min_chunk_size=100
        )

        data_to_insert = []

        for item in tqdm(final_files_to_process, desc="Processing files"):
            fpath = item["process_path"]
            source_path = item["source_path"]
            
            logger.info(f"Processing {fpath}...")
            
            try:
                loader = UnstructuredMarkdownLoader(fpath)
                docs = loader.load()
            except Exception as e:
                logger.error(f"Failed to load {fpath}: {e}")
                continue

            for doc in docs:
                # Semantic Chunking
                chunk_texts = cluster_chunker.split_text(doc.page_content)
                
                if not chunk_texts:
                    continue

                # Embed chunks
                embeddings = self._embed_texts(chunk_texts)
                
                # Prepare data for insertion
                for i, text in enumerate(chunk_texts):
                    data_to_insert.append({
                        TITLE_FIELD: os.path.basename(source_path), # Use original filename as title
                        TEXT_FIELD: text,
                        PATH_FIELD: fpath, # Point to the actual file (split or original)
                        SOURCE_FILE_FIELD: source_path, # Critical for deletion
                        VEC_FIELD: embeddings[i]
                    })

        # 3. Insert into Milvus
        if data_to_insert:
            logger.info(f"Inserting {len(data_to_insert)} chunks into {self.collection_name}...")
            self.client.insert(self.collection_name, data=data_to_insert)
            logger.info("Insertion complete.")
        else:
            logger.warning("No data to insert.")

    def remove_document(self, filename: str):
        """
        Remove a document from the database by its source filename.
        Also cleans up any split files in PROCESSED_DOCS_DIR.
        """
        if not self.client:
            self.connect()

        abs_path = os.path.abspath(filename)
        
        # 1. Query to find entries with this source_file
        # Note: Milvus delete by expression is supported in recent versions
        filter_expr = f'{SOURCE_FILE_FIELD} == "{abs_path}"'
        
        # Verify if exists first (optional, but good for logging)
        res = self.client.query(
            collection_name=self.collection_name,
            filter=filter_expr,
            output_fields=[PATH_FIELD],
            limit=10000 
        )
        
        if not res:
            logger.warning(f"No documents found for source: {abs_path}")
            return

        # Identify physical files to delete (split parts)
        files_to_delete = set()
        for item in res:
            p = item.get(PATH_FIELD)
            if p and p.startswith(os.path.abspath(self.processed_docs_dir)):
                files_to_delete.add(p)

        # 2. Delete from Milvus
        logger.info(f"Deleting entries for {abs_path}...")
        self.client.delete(
            collection_name=self.collection_name,
            filter=filter_expr
        )
        logger.info(f"Deletion from DB complete.")

        # 3. Cleanup split files
        for p in files_to_delete:
            if os.path.exists(p):
                try:
                    os.remove(p)
                    logger.info(f"Removed split file: {p}")
                except OSError as e:
                    logger.warning(f"Failed to remove {p}: {e}")

    def get_file_list(self) -> List[str]:
        """Return list of unique source files in the DB."""
        if not self.client:
            self.connect()
            
        # This might be expensive on huge DBs, but for <10k docs it's fine
        # Milvus doesn't support "distinct" directly efficiently in all versions
        # querying all source_files is one way
        
        results = self.client.query(
            collection_name=self.collection_name,
            filter="doc_id >= 0", # Select all
            output_fields=[SOURCE_FILE_FIELD]
        )
        
        sources = set()
        for res in results:
            if SOURCE_FILE_FIELD in res:
                sources.add(res[SOURCE_FILE_FIELD])
                
        return list(sources)

def list_knowledge_bases() -> List[str]:
    """List available knowledge bases in the DATA_DIR."""
    if not os.path.exists(DATA_DIR):
        return []
        
    kbs = []
    for name in os.listdir(DATA_DIR):
        kb_path = os.path.join(DATA_DIR, name)
        if os.path.isdir(kb_path):
             # Check if it has a DB file (optional, or just list dirs)
             # We assume any dir here is a KB
             kbs.append(name)
    return sorted(kbs)

def get_kb_path(name: str) -> str:
    """Get the absolute path to the Milvus DB file for a given KB name."""
    # Structure: rag_api/knowledge-bases/{name}/{name}.db
    return os.path.join(DATA_DIR, name, f"{name}.db")

def create_kb_dir(name: str) -> str:
    """Create directory for a new KB."""
    kb_dir = os.path.join(DATA_DIR, name)
    os.makedirs(kb_dir, exist_ok=True)
    return get_kb_path(name)


def main():
    parser = argparse.ArgumentParser(description="Vector Database Management Utility")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Common args
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("--db-name", required=True, help="Name/Path of the Milvus DB file (e.g. data/my_kb.db)")
    parent_parser.add_argument("--collection", default=COLLECTION_NAME_DEFAULT, help=f"Collection name (default: {COLLECTION_NAME_DEFAULT})")

    # Create Command
    create_parser = subparsers.add_parser("create", parents=[parent_parser], help="Create a new empty database")

    # Add Command
    add_parser = subparsers.add_parser("add", parents=[parent_parser], help="Add documents to the database")
    add_parser.add_argument("--files", nargs="+", required=True, help="List of files to add")

    # Remove Command
    remove_parser = subparsers.add_parser("remove", parents=[parent_parser], help="Remove a document from the database")
    remove_parser.add_argument("--file", required=True, help="Original document path to remove")

    # List Command
    list_parser = subparsers.add_parser("list", parents=[parent_parser], help="List source files in the database")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize Manager
    # db_name argument is treated as the path relative to CWD if not absolute
    # If the user provides just a name, we might want to default it to a data dir? 
    # For now, let's respect the input path.
    manager = VectorDatabaseManager(args.db_name, args.collection)

    if args.command == "create":
        manager.create_database()
        print(f"Database {args.db_name} created successfully.")

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
