"""
Milvus client connection cache.

Provides a singleton MilvusClient per knowledge base so that every caller
(RAG queries, document management, file lookups) shares one connection
instead of creating duplicates.

Usage::

    from .milvus_client_cache import get_client_object

    client = get_client_object("physics")          # query path (must exist)
    client = get_client_object("new_kb", create_if_missing=True)  # mgmt path
"""

import os
import time
import pathlib
import glob as glob_module
import logging
from typing import Dict, List

from pymilvus import MilvusClient

from config import MILVUS_RAG_DOCS_DB_PATH

# ── Logging ──────────────────────────────────────────────────────────────────

logger = logging.getLogger(__name__)

# ── Optional psutil for lock detection ───────────────────────────────────────

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

# ── Field name constants (env-overridable) ───────────────────────────────────

VEC_FIELD = os.environ.get("MILVUS_VECTOR_FIELD", "embedding")
TEXT_FIELD = os.environ.get("MILVUS_TEXT_FIELD", "text")
TITLE_FIELD = os.environ.get("MILVUS_TITLE_FIELD", "title")
DOCID_FIELD = os.environ.get("MILVUS_DOCID_FIELD", "doc_id")
FILE_UUID_FIELD = os.environ.get("MILVUS_FILE_UUID_FIELD", "file_uuid")
PATH_FIELD = "path"
SOURCE_FILE_FIELD = "source_file"

# ── VectorDatabaseManager constants ──────────────────────────────────────────

COLLECTION_NAME_DEFAULT = "test_knowledge"
DEFAULT_OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
DEFAULT_OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_EMBED_MODEL = "qwen3-embedding:8b-fp16"
MAX_TOKEN_LIMIT = 15000
PROCESSED_DOCS_DIR = "processed_docs"
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge-bases")

# ═════════════════════════════════════════════════════════════════════════════
#  Singleton cache
# ═════════════════════════════════════════════════════════════════════════════

_client_cache: Dict[str, MilvusClient] = {}
_DEFAULT_KEY = "__default__"

# ═════════════════════════════════════════════════════════════════════════════
#  Lock helper
# ═════════════════════════════════════════════════════════════════════════════

def _ensure_db_unlocked(db_path: str, max_wait: int = 5):
    """Wait for a Milvus Lite database file to become unlocked.

    Checks for processes holding the file open (when psutil is available),
    waits up to *max_wait* seconds for directory write-ability, and forces
    cleanup of stale lock artefacts as a last resort.
    """
    db_file = pathlib.Path(db_path)

    if not db_file.exists():
        return

    if HAS_PSUTIL:
        import psutil as _psutil
        for proc in _psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                for item in proc.open_files():
                    if db_path in item.path:
                        logger.warning(
                            "Process %s (%s) is using %s  cmd=%s",
                            proc.info['pid'], proc.info['name'], db_path,
                            ' '.join(proc.info['cmdline'] or [])
                        )
            except (_psutil.NoSuchProcess, _psutil.AccessDenied, _psutil.ZombieProcess):
                pass

    for attempt in range(max_wait):
        try:
            test_file = db_file.parent / f".lock_test_{int(time.time())}"
            test_file.touch()
            test_file.unlink()
            return
        except (IOError, PermissionError, OSError):
            if attempt < max_wait - 1:
                logger.info("Waiting for database lock to release… (%d/%d)",
                            attempt + 1, max_wait)
                time.sleep(1)
                continue

            logger.warning("Database file %s still locked after %ds – forcing cleanup",
                           db_path, max_wait)
            for f in glob_module.glob(str(db_file.parent / f"{db_file.stem}*")):
                try:
                    pathlib.Path(f).unlink()
                    logger.info("Removed locked artefact: %s", f)
                except Exception as e:
                    logger.error("Could not remove %s: %s", f, e)
            return

# ═════════════════════════════════════════════════════════════════════════════
#  Knowledge-base path utilities
# ═════════════════════════════════════════════════════════════════════════════

def get_kb_path(name: str) -> str:
    """Return the absolute path to the Milvus DB file for a given KB name."""
    return os.path.join(DATA_DIR, name, f"{name}.db")


def list_knowledge_bases() -> List[str]:
    """List available knowledge-base directories under DATA_DIR."""
    if not os.path.exists(DATA_DIR):
        return []
    return sorted(
        name for name in os.listdir(DATA_DIR)
        if os.path.isdir(os.path.join(DATA_DIR, name))
    )


def create_kb_dir(name: str) -> str:
    """Create the directory for a new knowledge base and return its DB path."""
    kb_dir = os.path.join(DATA_DIR, name)
    os.makedirs(kb_dir, exist_ok=True)
    return get_kb_path(name)

# ═════════════════════════════════════════════════════════════════════════════
#  get_client_object — the central cache function
# ═════════════════════════════════════════════════════════════════════════════

def get_client_object(
    kb_name: str = None,
    create_if_missing: bool = False,
) -> MilvusClient:
    """Return a singleton ``MilvusClient`` for the given knowledge base.

    On the first call for a given *kb_name* the client is created and stored
    in the module-level ``_client_cache`` dictionary.  Every subsequent call
    with the same *kb_name* returns the **same** object, avoiding duplicate
    connections to the same underlying database file.

    Parameters
    ----------
    kb_name : str or None
        Knowledge-base name (e.g. ``"physics"``).  When ``None`` the default
        database path from config (``MILVUS_RAG_DOCS_DB_PATH``) is used.
    create_if_missing : bool
        * ``False`` (default) — raise ``FileNotFoundError`` if the DB file
          does not exist.  Use this on the **query** path.
        * ``True`` — create the parent directory (and let ``MilvusClient``
          create the file) if it does not exist.  Use this on the
          **management / ingestion** path.

    Returns
    -------
    MilvusClient
        A cached client instance shared by all callers for this KB.
    """
    cache_key = kb_name or _DEFAULT_KEY

    if cache_key in _client_cache:
        logger.debug("Cache hit for KB '%s'", cache_key)
        return _client_cache[cache_key]

    db_path = get_kb_path(kb_name) if kb_name else MILVUS_RAG_DOCS_DB_PATH

    if create_if_missing:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
    elif not os.path.exists(db_path):
        raise FileNotFoundError(
            f"Database file not found: {db_path}\n"
            f"Please ensure the knowledge base has been created first."
        )

    _ensure_db_unlocked(db_path)

    client = MilvusClient(db_path)
    _client_cache[cache_key] = client
    logger.info("Created and cached MilvusClient for KB '%s' at %s", cache_key, db_path)
    return client
