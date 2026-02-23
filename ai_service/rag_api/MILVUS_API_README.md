# Milvus API Service

Standalone FastAPI microservice that owns **all** direct `MilvusClient` interactions.
Every other service in the system (the main AI service, the RAG pipeline, etc.) talks to
Milvus exclusively through HTTP calls to this API.

## Why a separate service?

ChiPT uses **Milvus Lite**, which stores each knowledge base as a local `.db` file.
Milvus Lite holds a file-level lock on these databases — only one process can open a
given `.db` at a time. By funneling every Milvus operation through a single process we:

1. **Eliminate file-lock contention** — no two processes fight over the same `.db` file.
2. **Cache connections** — one `MilvusClient` per KB, reused across all requests.
3. **Centralise schema management** — collection schemas and indexes are defined in one
   place rather than scattered across multiple modules.

---

## Running the service

```bash
cd ai_service
uvicorn rag_api.milvus_api:app --host 0.0.0.0 --port 8903
```

The port is configurable via the `MILVUS_API_URL` variable in `config.py`
(default `http://localhost:8903`).

---

## Endpoints and why each one exists

### `POST /search`

**What it does:** Approximate-nearest-neighbour (ANN) vector similarity search.

**Why it's here:** Calls `client.search()`, which requires an open `MilvusClient`
connection and access to the vector index inside the `.db` file. This cannot be
replaced by a filesystem operation.

| Field | Type | Description |
|-------|------|-------------|
| `kb_name` | `str?` | Knowledge base name (omit for the default DB) |
| `vector` | `list[float]` | Query embedding (4096-dim) |
| `limit` | `int` | Max results (default 30) |
| `output_fields` | `list[str]` | Fields to return per hit |
| `collection_name` | `str?` | Override the default collection |

---

### `POST /query`

**What it does:** Scalar-filter query — like a SQL `WHERE` clause against Milvus
metadata fields (e.g. `title == "report.pdf"`).

**Why it's here:** Calls `client.query()`. Metadata filters run inside Milvus, not on
the filesystem. You can't replicate this with `os.listdir()` because the metadata
(titles, UUIDs, source paths) lives inside the vector database, not as filenames on
disk.

| Field | Type | Description |
|-------|------|-------------|
| `kb_name` | `str?` | Knowledge base name |
| `filter_expr` | `str` | Milvus filter expression |
| `output_fields` | `list[str]` | Fields to return |
| `limit` | `int` | Max results (default 1) |
| `collection_name` | `str?` | Override the default collection |

---

### `POST /add_documents`

**What it does:** Full ingestion pipeline — takes raw file paths (PDF or markdown) and:

1. Converts PDFs to markdown (`extract_text_marker`)
2. Splits large files that exceed the token limit
3. Semantically chunks the text (`ClusterSemanticChunker`)
4. Embeds each chunk (OpenAI-compatible endpoint)
5. Inserts the resulting vectors + metadata into Milvus

**Why it's here:** The final step is `client.insert()`. The entire pipeline is
co-located so that all write operations happen in the one process that holds the
file lock. Splitting this across services would mean either passing large embedding
arrays over HTTP or having two processes open the same `.db`.

| Field | Type | Description |
|-------|------|-------------|
| `kb_name` | `str` | Target knowledge base |
| `file_paths` | `list[str]` | Absolute paths to source files |
| `collection_name` | `str?` | Override the default collection |

---

### `POST /create_collection`

**What it does:** Creates the collection schema (fields, data types, vector index)
inside an existing KB's `.db` file, if it doesn't already exist.

**Why it's here:** Calls `client.create_schema()`, `client.create_collection()`, and
`client.prepare_index_params()` — all direct Milvus SDK operations.

| Field | Type | Description |
|-------|------|-------------|
| `kb_name` | `str` | Knowledge base name |
| `collection_name` | `str?` | Override the default collection |

---

### `POST /create_kb`

**What it does:** Creates a brand-new knowledge base end-to-end:

1. Creates the KB directory on disk
2. Instantiates a new `MilvusClient`, which creates the `.db` file
3. Creates the collection schema + vector index inside it

**Why it's here:** Creating the `.db` file is itself a Milvus operation
(`MilvusClient(path)` initialises the SQLite-backed Milvus Lite database). The
directory creation is bundled here so that the KB is fully usable in a single call
rather than requiring the caller to do filesystem setup and then a separate
`/create_collection` call.

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | New knowledge base name |
| `collection_name` | `str?` | Override the default collection |

---

### `DELETE /remove_document`

**What it does:** Removes all vector chunks belonging to a source document, then
cleans up any intermediate split files from `processed_docs/`.

**Why it's here:** Calls `client.query()` to find matching chunks and
`client.delete()` to remove them. The filesystem cleanup of processed files is
secondary — the authoritative delete is from the Milvus collection.

| Field | Type | Description |
|-------|------|-------------|
| `kb_name` | `str` | Knowledge base name |
| `filename` | `str` | Source file path to remove |
| `collection_name` | `str?` | Override the default collection |

---

### `GET /list_files/{kb_name}`

**What it does:** Returns the unique set of source-file paths that have been
**successfully ingested** into the vector database.

**Why it's here and not just `os.listdir()`:** The KB directory contains a mix of
files — the `.db` database, a `processed_docs/` folder with intermediate splits, and
the original uploads. `os.listdir()` would return all of them with no way to know
which ones are actually indexed. This endpoint queries `client.query()` for the
distinct `source_file` values, which answers the question *"what documents are
searchable?"* — not *"what files happen to be on disk?"*. A file could also fail
during ingestion (bad PDF, embedding error) and sit on disk without being indexed.

| Parameter | Type | Description |
|-----------|------|-------------|
| `kb_name` | path | Knowledge base name |
| `collection_name` | query, optional | Override the default collection |

---

### `GET /file_by_uuid/{kb_name}/{file_uuid}`

**What it does:** Resolves a file UUID to its source-file path on disk.

**Why it's here:** The UUID-to-path mapping is stored as metadata inside the Milvus
collection (`file_uuid` field). There is no filesystem equivalent — UUIDs are assigned
at ingestion time and only exist in the vector database. This endpoint calls
`client.query()` with a filter on the UUID field.

| Parameter | Type | Description |
|-----------|------|-------------|
| `kb_name` | path | Knowledge base name |
| `file_uuid` | path | Document UUID |
| `collection_name` | query, optional | Override the default collection |

---

## What is NOT in this service

**`list_kbs`** — Listing knowledge bases is a pure filesystem operation
(`os.listdir()` on the `knowledge-bases/` directory). It doesn't touch Milvus at all,
so it stays in `main.py` as a local helper.

---

## Collection schema

Every KB collection uses this fixed schema:

| Field | Type | Notes |
|-------|------|-------|
| `doc_id` | INT64 | Primary key, auto-increment |
| `title` | VARCHAR(256) | Original source filename |
| `text` | VARCHAR(20000) | Chunk text content |
| `path` | VARCHAR(1024) | Path to the processed file |
| `source_file` | VARCHAR(1024) | Path to the original uploaded file |
| `file_uuid` | VARCHAR(128) | UUID grouping all chunks from one upload |
| `embedding` | FLOAT_VECTOR(4096) | Vector embedding (COSINE metric) |

---

## Environment variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MILVUS_VECTOR_FIELD` | `embedding` | Name of the vector field |
| `MILVUS_TEXT_FIELD` | `text` | Name of the text field |
| `MILVUS_TITLE_FIELD` | `title` | Name of the title field |
| `MILVUS_DOCID_FIELD` | `doc_id` | Name of the primary key field |
| `MILVUS_FILE_UUID_FIELD` | `file_uuid` | Name of the UUID field |
| `MILVUS_METRIC` | `COSINE` | Distance metric for ANN search |
| `OPENAI_BASE_URL` | — | Embedding API base URL |
| `OPENAI_API_KEY` | — | Embedding API key |
| `MILVUS_API_URL` | `http://localhost:8903` | URL where this service runs (used by callers) |
