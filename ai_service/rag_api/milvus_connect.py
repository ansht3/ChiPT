# Vector database imports
from pymilvus import connections, Collection, db
import os
from typing import List

# ---- Milvus Lite ----
from pymilvus import (
    MilvusClient, DataType
)
import time
import logging

from config import (LOCAL_MILVUS, MILVUS_RAG_DOCS_DB_NAME, MILVUS_RAG_DOCS_DB_PATH, MILVUS_URI, 
                    RAG_DOCS_COLLECTION_NAME, RAG_DOCS_MILVUS_PORT, RAG_DOCS_MILVUS_HOST
                   )

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# LOCAL_MILVUS = os.environ.get("LOCAL_MILVUS", "true").lower() == "true"

# # Configuration from environment variables
# MILVUS_URI  = os.environ.get("MILVUS_URI", "").strip()
# MILVUS_HOST = os.environ.get("MILVUS_HOST", "127.0.0.1")
# MILVUS_PORT = os.environ.get("MILVUS_PORT", "19530")
# MILVUS_DB   = os.environ.get("MILVUS_DB_NAME", "thousandDocuments.db")
# MILVUS_DB_FILE   = os.environ.get("MILVUS_DB_FILE", "/.gavea/store/chipt/chipt_v2/ChiPT/ai_service/rag_api/knowledge-bases/milvus_docs/thousandDocuments.db") #Will need to change to a permenant location when we are ready to use.
# COLLECTION  = os.environ.get("MILVUS_COLLECTION", "test_knowledge")

# Field names (override via env if needed)
VEC_FIELD   = os.environ.get("MILVUS_VECTOR_FIELD", "embedding")
TEXT_FIELD  = os.environ.get("MILVUS_TEXT_FIELD", "text")
TITLE_FIELD = os.environ.get("MILVUS_TITLE_FIELD", "title")
DOCID_FIELD = os.environ.get("MILVUS_DOCID_FIELD", "doc_id")

# ---- Process management (optional, for lock detection) ----
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


if LOCAL_MILVUS:
    from pymilvus import MilvusClient



# ------------------------------
# Milvus Lite Connection (File-based with MilvusClient)
# ------------------------------

def _ensure_db_unlocked(db_path: str, max_wait: int = 5):
    """Ensure the database file is not locked by waiting or cleaning up."""
    import pathlib
    import glob
    
    db_file = pathlib.Path(db_path)
    
    # If the file doesn't exist, raise error
    if not db_file.exists():
        raise FileNotFoundError(f"Database file does not exist: {db_path}")
    
    # Check for processes using this file (if psutil available)
    if HAS_PSUTIL:
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                # Check if this process has the database file open
                for item in proc.open_files():
                    if db_path in item.path:
                        print(f"[WARNING] Process {proc.info['pid']} ({proc.info['name']}) is using {db_path}")
                        print(f"[WARNING] Command: {' '.join(proc.info['cmdline'] or [])}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    
    # Wait briefly for any locks to release
    for attempt in range(max_wait):
        try:
            # Try to open in exclusive mode to check if locked
            test_file = db_file.parent / f".lock_test_{int(time.time())}"
            test_file.touch()
            test_file.unlink()
            return  # Can write to directory, likely OK
        except (IOError, PermissionError, OSError):
            if attempt < max_wait - 1:
                print(f"[INFO] Waiting for database lock to release... ({attempt + 1}/{max_wait})")
                time.sleep(1)
                continue
            # If still locked after waiting, remove the database
            print(f"[WARNING] Database file {db_path} is locked after {max_wait}s wait.")
            print(f"[WARNING] Attempting to force cleanup...")
            
            # Force cleanup
            for f in glob.glob(str(db_file.parent / f"{db_file.stem}*")):
                try:
                    pathlib.Path(f).unlink()
                    print(f"[CLEANUP] Removed locked file: {f}")
                except Exception as e:
                    print(f"[ERROR] Could not remove {f}: {e}")
            
            return  # Continue after cleanup


def connect_milvus_lite(db_file: str = None, retry_on_lock: bool = True) -> tuple:
    """
    Connect to an existing Milvus Lite database using MilvusClient.
    
    Args:
        db_file: Path to the database file. If None, uses MILVUS_DB_FILE.
        retry_on_lock: Whether to retry if database is locked.
    
    Returns:
        tuple: (client, actual_db_path)
    
    Raises:
        FileNotFoundError: If the database file doesn't exist.
        RuntimeError: If unable to connect to the database.
    """
    if db_file is None:
        db_file = MILVUS_RAG_DOCS_DB_PATH
    
    # Check if database exists
    if not os.path.exists(db_file):
        raise FileNotFoundError(
            f"Database file not found: {db_file}\n"
            f"Please ensure the database has been created first."
        )
    
    # Check if database is locked and handle it
    if retry_on_lock:
        _ensure_db_unlocked(db_file)
    
    # Connect to the existing database
    try:
        client = MilvusClient(db_file)
        print(f"[Milvus] Connected to existing database: {db_file}")
        
        # Verify the collection exists
        collections = client.list_collections()
        if RAG_DOCS_COLLECTION_NAME not in collections:
            raise ValueError(
                f"Collection '{RAG_DOCS_COLLECTION_NAME}' not found in database.\n"
                f"Available collections: {collections}"
            )
        
        print(f"[Milvus] Using collection: '{RAG_DOCS_COLLECTION_NAME}'")
        return client
        
    except Exception as e:
        print(f"[ERROR] Failed to connect to {db_file}: {e}")
        print(f"[WARNING] Make sure the database file is valid and on local storage")
        raise RuntimeError(f"Unable to connect to Milvus Lite at {db_file}: {e}")


# ------------------------------
# Collection verification
# ------------------------------

def verify_collection(client: MilvusClient) -> dict:
    """
    Verify that the collection exists and return its statistics.
    
    Returns:
        dict: Collection statistics including row count and schema info.
    """
    collections = client.list_collections()
    
    if RAG_DOCS_COLLECTION_NAME not in collections:
        raise ValueError(f"Collection '{RAG_DOCS_COLLECTION_NAME}' does not exist in the database")
    
    # Get collection stats
    stats = client.get_collection_stats(collection_name=RAG_DOCS_COLLECTION_NAME)
    
    print(f"[Milvus] Collection '{RAG_DOCS_COLLECTION_NAME}' verified")
    print(f"[Milvus] Row count: {stats.get('row_count', 'unknown')}")
    
    return stats


from typing import Union
from dataclasses import dataclass

@dataclass
class MilvusConnection:
    """Unified wrapper for both local and remote Milvus connections"""
    client: Union[MilvusClient, Collection]
    is_local: bool
    collection_name: str
    
    def __post_init__(self):
        """Ensure index exists after initialization"""
        if self.is_local:
            self._ensure_index()
    
    def _ensure_index(self):
        """Ensure vector index exists for local Milvus"""
        try:
            # Check if index exists
            collection_info = self.client.describe_collection(self.collection_name)
            
            # Look for existing index on embedding field
            has_index = False
            if 'indexes' in collection_info:
                for idx in collection_info['indexes']:
                    if idx.get('field_name') == VEC_FIELD:
                        has_index = True
                        logger.info(f"[Milvus] Index already exists on field '{VEC_FIELD}'")
                        break
            
            if not has_index:
                logger.info(f"[Milvus] Creating index on field '{VEC_FIELD}'")
                index_params = self.client.prepare_index_params()
                index_params.add_index(
                    field_name=VEC_FIELD,
                    index_type="AUTOINDEX",
                    metric_type=os.environ.get("MILVUS_METRIC", "COSINE"),
                )
                
                self.client.create_index(
                    collection_name=self.collection_name,
                    index_params=index_params
                )
                logger.info("[Milvus] Index created successfully")
                
        except Exception as e:
            logger.warning(f"Could not verify/create index: {e}")
    
    def search(
        self, 
        query_embedding: List[float], 
        top_k: int = 30,
        output_fields: List[str] = None
    ) -> List:
        """Unified search interface"""
        if output_fields is None:
            output_fields = [DOCID_FIELD, TITLE_FIELD, TEXT_FIELD]
            
        if self.is_local:
            # MilvusClient API
            search_params = {
                "metric_type": os.environ.get("MILVUS_METRIC", "COSINE"),
                "params": {}
            }
            results = self.client.search(
                collection_name=self.collection_name,
                data=[query_embedding],
                limit=top_k,
                output_fields=output_fields,
                search_params=search_params
            )
            return results[0] if results else []
        else:
            # Collection API
            search_params = {
                "metric_type": os.environ.get("MILVUS_METRIC", "IP"), 
                "params": {"nprobe": 10}
            }
            results = self.client.search(
                data=[query_embedding],
                anns_field=VEC_FIELD,
                param=search_params,
                limit=top_k,
                output_fields=output_fields
            )
            return results[0] if results else []
    
    def load(self):
        """Load collection (no-op for local)"""
        if not self.is_local:
            try:
                self.client.load()
            except Exception as e:
                logger.debug(f"Collection load failed or not needed: {e}")
    
    def query(self, expr: str, output_fields: List[str] = None, limit: int = 1):
        """Unified query interface"""
        if output_fields is None:
            output_fields = [DOCID_FIELD, TITLE_FIELD, TEXT_FIELD]
            
        if self.is_local:
            return self.client.query(
                collection_name=self.collection_name,
                filter=expr,
                output_fields=output_fields,
                limit=limit
            )
        else:
            return self.client.query(
                expr=expr,
                output_fields=output_fields,
                limit=limit
            )
    def insert(self, data: List[dict]):
        """Unified insert interface"""
        if not data:
            logger.warning("Insert called with no data.")
            return
    
        logger.info(f"Inserting {len(data)} records into '{self.collection_name}'...")
    
        # The MilvusClient API is the same for local and remote now
        res = self.client.insert(
            collection_name=self.collection_name,
            data=data
        )
    
        # Flushing ensures the data is written to disk and indexed
        self.client.flush(self.collection_name)
        logger.info("Insertion complete and data flushed.")
        return res


def _milvus_connect(db_path: str = None) -> MilvusConnection:
    """
    Connect to Milvus with unified interface.
    
    Returns:
        MilvusConnection: Unified wrapper that works for both local and remote
    """
    if LOCAL_MILVUS:
        # Connect to Milvus Lite
        target_path = db_path if db_path else MILVUS_RAG_DOCS_DB_PATH
        client = connect_milvus_lite(target_path)
        verify_collection(client)
        logger.info("[Milvus] Connected to local Milvus Lite")
        return MilvusConnection(client=client, is_local=True, collection_name=RAG_DOCS_COLLECTION_NAME)
    
    # Remote Milvus connection with fallback
    try:
        if MILVUS_URI:
            logger.info(f"Attempting to connect via URI: {MILVUS_URI}")
            connections.connect(alias="default", uri=MILVUS_URI)
            logger.info("Successfully connected via URI")
        else:
            logger.info(f"Attempting to connect via host:port ({RAG_DOCS_MILVUS_HOST}:{RAG_DOCS_MILVUS_PORT})")
            connections.connect(alias="default", host=RAG_DOCS_MILVUS_HOST, port=RAG_DOCS_MILVUS_PORT)
            logger.info("Successfully connected via host:port")
        
        # Switch database if specified
        if MILVUS_RAG_DOCS_DB_NAME and db is not None:
            try:
                db.using_database(MILVUS_RAG_DOCS_DB_NAME)
                logger.info(f"Switched to database: {MILVUS_RAG_DOCS_DB_NAME}")
            except Exception as e:
                logger.warning(f"Could not switch to database {MILVUS_RAG_DOCS_DB_NAME}: {e}")
        
        collection = Collection(RAG_DOCS_COLLECTION_NAME)
        logger.info("[Milvus] Connected to remote Milvus")
        return MilvusConnection(client=collection, is_local=False, collection_name=RAG_DOCS_COLLECTION_NAME)
        
    except Exception as e:
        logger.error(f"Error connecting to Milvus: {e}")
        
        # Fallback to host:port if URI failed
        if MILVUS_URI:
            try:
                logger.info(f"URI connection failed. Falling back to host:port ({RAG_DOCS_MILVUS_HOST}:{RAG_DOCS_MILVUS_PORT})")
                connections.connect(alias="default", host=RAG_DOCS_MILVUS_HOST, port=RAG_DOCS_MILVUS_PORT)
                logger.info("Successfully connected via host:port fallback")
                
                if MILVUS_RAG_DOCS_DB_NAME and db is not None:
                    try:
                        db.using_database(MILVUS_RAG_DOCS_DB_NAME)
                        logger.info(f"Switched to database: {MILVUS_RAG_DOCS_DB_NAME}")
                    except Exception as db_err:
                        logger.warning(f"Could not switch to database {MILVUS_RAG_DOCS_DB_NAME}: {db_err}")
                
                collection = Collection(RAG_DOCS_COLLECTION_NAME)
                return MilvusConnection(client=collection, is_local=False, collection_name=RAG_DOCS_COLLECTION_NAME)
                
            except Exception as fallback_err:
                logger.error(f"Fallback connection also failed: {fallback_err}")
                raise
        else:
            raise
