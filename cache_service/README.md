# Q&A Cache Service with Semantic Search

Intelligent caching service that uses Milvus vector database and semantic similarity to retrieve previously answered questions.

## Overview

This service provides:
- **Semantic Search**: Finds similar questions even with different wording
- **Query Rewriting**: Generates alternative phrasings for better matching
- **Vector Similarity**: Uses embeddings and cosine similarity for matching
- **Milvus Integration**: Scalable vector database for fast similarity search

## Prerequisites

### Milvus Installation

**If you already have Milvus v2.6.1 running:**

The service can connect to your existing Milvus instance. Update `main.py`:
```python
MILVUS_HOST = "localhost"  # Your Milvus host
MILVUS_PORT = "19530"      # Your existing Milvus port
```

**If you need a separate Milvus instance (to avoid conflicts):**

The included `docker-compose.yml` uses **alternate ports**:
- Milvus: `19531` (instead of 19530)
- Health: `9092` (instead of 9091)
- MinIO API: `9002` (instead of 9000)
- MinIO Console: `9003` (instead of 9001)

```bash
# Use the included docker-compose.yml file
cd cache_service

# Start Milvus v2.6.1 on alternate ports
docker-compose up -d

# Check status
docker-compose ps
# Should show: chipt-milvus-standalone, chipt-milvus-etcd, chipt-milvus-minio (all healthy)
```

**Option 2: Standalone Binary**
Visit: https://milvus.io/docs/install_standalone-docker.md

### OpenAI API

The service requires an OpenAI-compatible API at `http://localhost:14345` for:
- Generating embeddings (text-embedding-ada-002)
- Query rewriting (unsloth/GLM-4.5-Air)

## Configuration

- **Milvus**: `localhost:19531` (using alternate port to avoid conflicts)
- **OpenAI API**: `http://localhost:14345/v1`
- **API Key**: `nada`
- **Port**: `8902`
- **Similarity Threshold**: `0.85` (85% similarity required for cache hit)

**Port Mapping:**
- Milvus gRPC: `19531` (host) → `19530` (container)
- Milvus Health: `9092` (host) → `9091` (container)
- MinIO API: `9002` (host) → `9000` (container)
- MinIO Console: `9003` (host) → `9001` (container)

**Note:** If you need different ports or are connecting to an existing Milvus instance, update the constants in `main.py`:
```python
MILVUS_HOST = "localhost"  # Change if Milvus is on different host
MILVUS_PORT = "19531"      # Change if using different port (default: 19531)
```

## API Endpoints

### POST /search

Search for a cached answer using semantic similarity.

**Request:**
```json
{
  "query": "What's the difference between supervised and unsupervised ML?"
}
```

**Response (Cache Hit):**
```json
{
  "found": true,
  "answer": "Supervised learning uses labeled data where the correct output is known..."
}
```

**Response (Cache Miss):**
```json
{
  "found": false,
  "answer": null
}
```

### POST /add

Add a new Q&A pair to the cache.

**Request:**
```json
{
  "question": "What is deep learning?",
  "answer": "Deep learning is a subset of machine learning..."
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Q&A pair added to cache"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "qa-cache",
  "milvus_connected": true
}
```

### GET /stats

Get cache statistics.

**Response:**
```json
{
  "total_qa_pairs": 42,
  "collection_name": "qa_cache",
  "similarity_threshold": 0.85
}
```

## Installation

### For UV Users (Recommended)

```bash
# Clean install to avoid dependency conflicts
uv pip uninstall -y pymilvus marshmallow environs

# Install in correct order
uv pip install "marshmallow>=3.20.0"
uv pip install pymilvus==2.4.0
uv pip install -r requirements.txt

# Or use the install script
chmod +x install.sh
./install.sh
```

### For Pip Users

```bash
# Clean install to avoid dependency conflicts
pip uninstall -y pymilvus marshmallow environs

# Install in correct order
pip install --upgrade pip setuptools wheel
pip install "marshmallow>=3.20.0"
pip install pymilvus==2.4.0
pip install -r requirements.txt
```

**Note**: If you get `AttributeError: module 'marshmallow' has no attribute '__version_info__'`, make sure to install marshmallow>=3.20.0 first.

## Running the Service

```bash
# Make sure Milvus is running first
docker-compose ps

# Start the cache service
python main.py

# Or with uvicorn
uvicorn main:app --host 0.0.0.0 --port 8902
```

## How It Works

### 1. Query Rewriting

When a search request comes in, the service:
- Generates 2 alternative phrasings of the question using unsloth/GLM-4.5-Air
- Creates a total of 3 query variations (original + 2 rewrites)
- Example:
  - Original: "How does backprop work?"
  - Rewrite 1: "Can you explain the backpropagation algorithm?"
  - Rewrite 2: "What is the mechanism behind backpropagation?"

### 2. Embedding Generation

Each query variation is converted to a 1536-dimension vector using OpenAI's `text-embedding-ada-002` model.

### 3. Similarity Search

- Embeddings are normalized to unit length for cosine similarity
- Milvus performs fast vector search using IVF_FLAT index
- Returns top matches with similarity scores

### 4. Threshold Filtering

- Only matches with similarity ≥ 0.85 are returned
- This ensures high-quality matches while allowing some variation in wording

## Sample Data

The service automatically seeds 5 sample Q&A pairs on startup:
1. What is machine learning?
2. How does backpropagation work?
3. What is the difference between supervised and unsupervised learning?
4. What is overfitting in machine learning?
5. How do you prevent overfitting?

## Testing

```bash
# Search for a question
curl -X POST http://localhost:8902/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ML?"}'

# Add a new Q&A
curl -X POST "http://localhost:8902/add?question=What%20is%20ReLU?&answer=ReLU%20is%20a%20activation%20function"

# Check stats
curl http://localhost:8902/stats
```

## Configuration Options

Edit constants in `main.py`:

```python
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"
COLLECTION_NAME = "qa_cache"
EMBEDDING_DIM = 1536
SIMILARITY_THRESHOLD = 0.85  # Adjust for stricter/looser matching
```

## Architecture

```
Query → Query Rewriting → Embedding Generation → Vector Search → Threshold Check → Result
         (GPT-4)          (text-embedding-ada-002)   (Milvus)       (≥0.85)
```

## Troubleshooting

### Milvus Connection Failed

```bash
# Check if Milvus is running
docker-compose ps

# Check Milvus logs
docker-compose logs chipt-milvus-standalone

# Restart Milvus
docker-compose restart
```

### Embedding Generation Failed

- Verify OpenAI API is running at `http://localhost:14345`
- Check API key is correct
- Ensure `text-embedding-ada-002` model is available

### Low Cache Hit Rate

- Lower `SIMILARITY_THRESHOLD` (e.g., to 0.75)
- Add more Q&A pairs to the cache
- Check query rewriting is working with `/search` logs

## Performance

- **Search Speed**: ~100-200ms per query (with 3 variations)
- **Storage**: ~6KB per Q&A pair (with embedding)
- **Scalability**: Milvus can handle millions of vectors efficiently

## Integration

This service is used by the Q&A system's instructor panel:
1. Instructor requests AI suggestion for a question
2. System first checks cache service
3. If cache hit (found=true), return cached answer (fast, consistent)
4. If cache miss (found=false), call AI service to generate new answer
5. New answers can be added to cache for future reuse
