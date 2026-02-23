#!/usr/bin/env python3
"""
Smoke tests for the Milvus API microservice.

Verifies that:
  1. All modules import without errors
  2. The Milvus API endpoints work (/search, /query, /list_files, etc.)
  3. /create_kb initializes a .db file + collection (Milvus operation)
  4. Filesystem helpers in main.py work (list KBs, KB dirs)
  5. rag_main_kdocs.py has no old direct-Milvus imports
  6. main.py has no VectorDatabaseManager imports

Requires the Milvus API to be running:
    cd ai_service && ../ai_service/chipt-venv/bin/python -m uvicorn rag_api.milvus_api:app --port 8903

Then run:
    ./ai_service/chipt-venv/bin/python run_test.py
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "ai_service"))

PASS = 0
FAIL = 0

from config import MILVUS_API_URL


def report(name: str, passed: bool, detail: str = ""):
    global PASS, FAIL
    status = "PASS" if passed else "FAIL"
    if passed:
        PASS += 1
    else:
        FAIL += 1
    msg = f"  [{status}] {name}"
    if detail:
        msg += f"  --  {detail}"
    print(msg)


# ═════════════════════════════════════════════════════════════════════════════
#  1. Import Tests
# ═════════════════════════════════════════════════════════════════════════════

def test_imports():
    print("\n=== 1. Import Tests ===")

    try:
        import config
        report("import config", True)
    except Exception as e:
        report("import config", False, str(e))

    try:
        from config import MILVUS_API_URL
        report("MILVUS_API_URL in config", True, MILVUS_API_URL)
    except Exception as e:
        report("MILVUS_API_URL in config", False, str(e))

    try:
        from rag_api import milvus_api
        report("import milvus_api", True)
    except Exception as e:
        report("import milvus_api", False, str(e))

    try:
        from rag_api.milvus_api import app, _get_client, _get_kb_path
        report("import milvus_api internals", True)
    except Exception as e:
        report("import milvus_api internals", False, str(e))

    # Verify rag_main_kdocs no longer imports from final_milvus_connection
    try:
        import importlib
        spec = importlib.util.find_spec("rag_api.rag_main_kdocs")
        if spec and spec.origin:
            with open(spec.origin, "r") as f:
                source = f.read()
            has_old = "final_milvus_connection" in source or "_milvus_connect" in source
            report("rag_main_kdocs: no old Milvus imports",
                   not has_old,
                   "still references final_milvus_connection" if has_old else "clean")
        else:
            report("rag_main_kdocs: no old Milvus imports", False, "module not found")
    except Exception as e:
        report("rag_main_kdocs: no old Milvus imports", False, str(e))

    # Verify main.py no longer imports VectorDatabaseManager
    try:
        main_path = os.path.join(PROJECT_ROOT, "ai_service", "main.py")
        with open(main_path, "r") as f:
            source = f.read()
        has_old = "VectorDatabaseManager" in source or "final_milvus_connection" in source
        report("main.py: no old Milvus imports",
               not has_old,
               "still references old modules" if has_old else "clean")
    except Exception as e:
        report("main.py: no old Milvus imports", False, str(e))

    # Verify main.py list_kbs uses local filesystem, not HTTP
    try:
        main_path = os.path.join(PROJECT_ROOT, "ai_service", "main.py")
        with open(main_path, "r") as f:
            source = f.read()
        has_local = "_list_knowledge_bases()" in source
        report("main.py: list_kbs uses local filesystem", has_local)
    except Exception as e:
        report("main.py: list_kbs uses local filesystem", False, str(e))


# ═════════════════════════════════════════════════════════════════════════════
#  2. Milvus API endpoint audit
# ═════════════════════════════════════════════════════════════════════════════

def test_endpoint_audit():
    """Verify only Milvus-related endpoints exist in milvus_api.py."""
    print("\n=== 2. Endpoint Audit ===")

    try:
        api_path = os.path.join(PROJECT_ROOT, "ai_service", "rag_api", "milvus_api.py")
        with open(api_path, "r") as f:
            source = f.read()

        # These SHOULD be in milvus_api (they use MilvusClient)
        milvus_endpoints = ["/search", "/query", "/add_documents",
                            "/create_collection", "/create_kb",
                            "/remove_document", "/list_files", "/file_by_uuid"]
        for ep in milvus_endpoints:
            report(f"milvus_api has {ep}", f'"{ep}"' in source or f"'{ep}'" in source or ep in source)

        # /list_kbs should NOT be in milvus_api (pure filesystem)
        has_list_kbs = 'def list_kbs' in source
        report("milvus_api does NOT have /list_kbs", not has_list_kbs,
               "still present" if has_list_kbs else "correctly absent")

    except Exception as e:
        report("endpoint audit", False, str(e))


# ═════════════════════════════════════════════════════════════════════════════
#  3. Live API Tests (requires running Milvus API)
# ═════════════════════════════════════════════════════════════════════════════

def test_live_api():
    print("\n=== 3. Live API Tests ===")
    import httpx

    # Check if API is running
    try:
        resp = httpx.get(f"{MILVUS_API_URL}/docs", timeout=3.0)
        api_up = resp.status_code == 200
    except Exception:
        api_up = False

    if not api_up:
        print(f"  [SKIP] Milvus API not running at {MILVUS_API_URL}")
        print(f"         Start it with: cd ai_service && python -m uvicorn rag_api.milvus_api:app --port 8903")
        return

    report("Milvus API is reachable", True, MILVUS_API_URL)

    # Find a test KB with a .db file
    from rag_api.milvus_api import _get_kb_path, DATA_DIR
    test_kb = None
    if os.path.exists(DATA_DIR):
        for name in sorted(os.listdir(DATA_DIR)):
            if os.path.isdir(os.path.join(DATA_DIR, name)):
                if os.path.exists(_get_kb_path(name)):
                    test_kb = name
                    break

    if not test_kb:
        report("Skipped live tests (no KB with .db file)", False)
        return

    report(f"Test KB found: {test_kb}", True)

    # /list_files
    try:
        resp = httpx.get(f"{MILVUS_API_URL}/list_files/{test_kb}", timeout=10.0)
        files = resp.json()["files"]
        report(f"/list_files/{test_kb}", resp.status_code == 200, f"{len(files)} files")
    except Exception as e:
        report(f"/list_files/{test_kb}", False, str(e))

    # /list_files 404 for missing KB
    try:
        resp = httpx.get(f"{MILVUS_API_URL}/list_files/__nonexistent__", timeout=10.0)
        report("/list_files 404 for missing KB", resp.status_code == 404)
    except Exception as e:
        report("/list_files 404 for missing KB", False, str(e))

    # /query
    try:
        resp = httpx.post(
            f"{MILVUS_API_URL}/query",
            json={"kb_name": test_kb, "filter_expr": "doc_id >= 0",
                  "output_fields": ["source_file"], "limit": 3},
            timeout=10.0,
        )
        results = resp.json()["results"]
        report(f"/query on {test_kb}", resp.status_code == 200, f"{len(results)} results")
    except Exception as e:
        report(f"/query on {test_kb}", False, str(e))

    # /search with zero vector (smoke test)
    try:
        resp = httpx.post(
            f"{MILVUS_API_URL}/search",
            json={"kb_name": test_kb, "vector": [0.0] * 4096,
                  "limit": 3, "output_fields": ["title", "text"]},
            timeout=30.0,
        )
        hits = resp.json()["results"]
        report(f"/search on {test_kb}", resp.status_code == 200, f"{len(hits)} hits")
    except Exception as e:
        report(f"/search on {test_kb}", False, str(e))

    # /file_by_uuid 404 for fake UUID
    try:
        resp = httpx.get(
            f"{MILVUS_API_URL}/file_by_uuid/{test_kb}/00000000-0000-0000-0000-000000000000",
            timeout=10.0,
        )
        report("/file_by_uuid 404 for fake UUID", resp.status_code == 404)
    except Exception as e:
        report("/file_by_uuid 404 for fake UUID", False, str(e))

    # /create_kb → creates dir + .db + collection
    import shutil
    from rag_api.milvus_api import _client_cache
    temp_kb = "__test_temp_kb__"
    temp_dir = os.path.join(DATA_DIR, temp_kb)

    try:
        resp = httpx.post(
            f"{MILVUS_API_URL}/create_kb",
            json={"name": temp_kb},
            timeout=15.0,
        )
        report("/create_kb", resp.status_code == 200, resp.json().get("message"))

        db_file = _get_kb_path(temp_kb)
        report("create_kb produced .db file", os.path.exists(db_file), db_file)
    except Exception as e:
        report("/create_kb", False, str(e))
    finally:
        _client_cache.pop(temp_kb, None)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)


# ═════════════════════════════════════════════════════════════════════════════
#  Main
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    test_imports()
    test_endpoint_audit()
    test_live_api()

    print(f"\n{'='*60}")
    print(f"  RESULTS:  {PASS} passed,  {FAIL} failed")
    print(f"{'='*60}")

    sys.exit(1 if FAIL > 0 else 0)
