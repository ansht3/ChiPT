# Complete Q&A System - Setup Guide

Complete architecture with main Q&A application, AI service, and cache service.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Main Q&A System                        │
│                    (port 8000/8909)                         │
│  - Student Interface: Ask questions, view answers           │
│  - Instructor Interface: Review, answer questions           │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──────────────┐
             ▼              ▼
    ┌────────────────┐  ┌──────────────┐
    │ Cache Service  │  │ AI Service   │
    │  (port 8902)   │  │ (port 8901)  │
    │                │  │              │
    │ - Milvus DB    │  │ - OpenAI API │
    │ - Embeddings   │  │ - GLM-4.5    │
    │ - Similarity   │  │ - Context    │
    └────────────────┘  └──────────────┘
             │
             ▼
    ┌────────────────┐
    │ OpenAI API     │
    │ (port 14345)   │
    │ - Embeddings   │
    │ - Completions  │
    └────────────────┘
```

## Directory Structure

```
.
├── project/              # Main Q&A application
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── services.py
│   ├── schemas.py
│   ├── templates/
│   ├── static/
│   └── requirements.txt
│
├── ai_service/          # AI answer generation
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
│
└── cache_service/       # Semantic search cache
    ├── main.py
    ├── docker-compose.yml
    ├── requirements.txt
    └── README.md
```

## Prerequisites

1. **Python 3.11+**
2. **Docker & Docker Compose** (for Milvus)
3. **OpenAI-compatible API** running at `localhost:14345`

## Complete Setup

### Step 1: Start Milvus (Cache Service Dependency)

**Option A: Use your existing Milvus v2.6.1**

If you already have Milvus running on port 19530, update `cache_service/main.py`:
```python
MILVUS_HOST = "localhost"
MILVUS_PORT = "19530"  # Your existing Milvus port
```
Then skip to Step 2.

**Option B: Start a separate Milvus instance (recommended to avoid conflicts)**

The included docker-compose uses alternate ports to avoid conflicts:
```bash
cd cache_service
docker-compose up -d

# Verify Milvus is running
docker-compose ps
# Should show: chipt-milvus-standalone, chipt-milvus-etcd, chipt-milvus-minio (all healthy)
```

**Ports used by the ChiPT Milvus instance:**
- Milvus gRPC: `19531` (vs standard 19530)
- Milvus Health: `9092` (vs standard 9091)
- MinIO API: `9002` (vs standard 9000)
- MinIO Console: `9003` (vs standard 9001)

### Step 2: Install Dependencies

```bash
# AI Service
cd ai_service
pip install -r requirements.txt

# Cache Service
cd ../cache_service
pip install -r requirements.txt

# Main Q&A System
cd ../project
pip install -r requirements.txt
```

### Step 3: Start All Services

**Terminal 1 - Cache Service:**
```bash
cd cache_service
python main.py
# Runs on http://localhost:8902
```

**Terminal 2 - AI Service:**
```bash
cd ai_service
python main.py
# Runs on http://localhost:8901
```

**Terminal 3 - Main Q&A System:**
```bash
cd project
uvicorn main:app --reload --port 8000
# Or for remote access:
# uvicorn main:app --host 0.0.0.0 --reload --port 8909
```

### Step 4: Access the System

Open browser to: **http://localhost:8000** (or your configured port)

**Test Accounts:**
- **Student**: student@purdue / 123456
- **Instructor**: instructor@purdue / 123456

Or register a new account as student or instructor.

## How It Works

### Student Flow

1. Student logs in
2. Asks a question
3. Question is stored in database with status "pending"
4. Student sees the question in their dashboard

### Instructor Flow

1. Instructor logs in
2. Views all pending questions from all students
3. Clicks "Get AI Suggestion" on a question:
   
   **a. Cache Check (Fast Path - ~200ms)**
   ```
   Question → Cache Service → Query Rewriting → Vector Search → Cache Hit?
   ```
   - If similar question found (≥85% similarity): Return cached answer
   - Source: "cached"
   
   **b. AI Generation (Slow Path - ~2-5s)**
   ```
   Question → AI Service → Get student context → Build prompt → OpenAI → Answer
   ```
   - Fetches student's previous 5 Q&A pairs for context
   - Generates personalized answer
   - Source: "ai"

4. Instructor reviews and optionally edits the suggestion
5. Sends answer to student
6. Answer is stored with source tracking (ai/cached/manual)

### Answer Suggestion Logic (services.py)

```python
async def get_suggested_answer(question_id):
    1. Fetch question from database
    2. Check cache_service (POST http://localhost:8902/search)
    3. If found: return {"suggested_answer": ..., "source": "cached"}
    4. Else: 
       - Get student's last 5 Q&A pairs
       - Call AI service (POST http://localhost:8901/generate)
       - Return {"suggested_answer": ..., "source": "ai"}
```

## Testing the Integration

### Test Cache Service

```bash
curl -X POST http://localhost:8902/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'

# Expected: {"found": true, "answer": "Machine learning is..."}
```

### Test AI Service

```bash
curl -X POST http://localhost:8901/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How do neural networks learn?",
    "context": [
      {"q": "What is a neural network?", "a": "A computational model..."}
    ]
  }'

# Expected: {"answer": "Neural networks learn through..."}
```

### Test Full Flow

1. Login as student@test.com
2. Ask: "What is machine learning?"
3. Login as instructor@test.com
4. View the question
5. Click "Get AI Suggestion"
6. Observe:
   - First time: Uses AI service (source: "ai"), takes ~3-5 seconds
   - Second student asks similar question: Uses cache (source: "cached"), takes ~200ms

## Configuration Summary

| Service | Port | Purpose | Dependencies |
|---------|------|---------|--------------|
| Main Q&A | 8000/8909 | Web interface | SQLite, Cache Service, AI Service |
| AI Service | 8901 | Answer generation | OpenAI API (14345) |
| Cache Service | 8902 | Semantic search | Milvus (19531), OpenAI API (14345) |
| Milvus (ChiPT) | 19531 | Vector database | Etcd, MinIO |
| Milvus Health | 9092 | Health checks | - |
| MinIO API | 9002 | Object storage | - |
| MinIO Console | 9003 | MinIO UI | - |
| OpenAI API | 14345 | LLM & Embeddings | - |

**Note:** The ChiPT Milvus instance uses port `19531` to avoid conflicts with existing Milvus installations on the standard port `19530`.

**Using a different Milvus host/port?**
Edit `cache_service/main.py`:
```python
MILVUS_HOST = "your-milvus-host"  # Default: "localhost"
MILVUS_PORT = "19531"             # Default: "19531" (or "19530" for existing)
```

## Monitoring

### Check Service Health

```bash
# Main Q&A
curl http://localhost:8000/api/me

# AI Service
curl http://localhost:8901/health

# Cache Service
curl http://localhost:8902/health
curl http://localhost:8902/stats
```

### View Logs

```bash
# Milvus logs
cd cache_service
docker-compose logs -f milvus-standalone

# Service logs - check terminal outputs
```

## Troubleshooting

### Milvus Won't Start

```bash
cd cache_service
docker-compose down
docker-compose up -d
docker-compose logs -f chipt-milvus-standalone
```

### Cache Service Can't Connect to Milvus

```bash
# Check Milvus is running
docker ps | grep chipt-milvus

# Check port 19531 is available (ChiPT Milvus)
netstat -an | grep 19531

# If using existing Milvus on port 19530
netstat -an | grep 19530
```

### AI Service Can't Generate Answers

- Verify OpenAI API is running at `localhost:14345`
- Check API key is "nada"
- Test manually:
  ```bash
  curl http://localhost:14345/v1/models
  ```

### External API Errors in Main System

The main Q&A system handles external service failures gracefully:
- Cache timeout: Falls back to AI service
- AI timeout: Returns "Unable to generate suggestion. Please write manually."
- Both fail: Instructor can still write manual answer

## Performance Tuning

### Cache Hit Rate

```bash
# Add common questions to cache
curl -X POST "http://localhost:8902/add?question=YOUR_QUESTION&answer=YOUR_ANSWER"
```

### Adjust Similarity Threshold

Edit `cache_service/main.py`:
```python
SIMILARITY_THRESHOLD = 0.80  # Lower = more lenient matching
```

### AI Generation Speed

- Uses streaming: Not implemented (could be added)
- Timeout: 30 seconds (configurable)
- Context size: Last 5 Q&A pairs (configurable)

## Production Considerations

1. **Security**:
   - Change all API keys
   - Use environment variables
   - Add authentication to AI/Cache services
   - Enable HTTPS

2. **Scalability**:
   - Use PostgreSQL instead of SQLite
   - Deploy Milvus cluster
   - Add Redis for session management
   - Load balance with multiple service instances

3. **Monitoring**:
   - Add Prometheus metrics
   - Set up logging aggregation
   - Monitor cache hit rates
   - Track API latencies

4. **Backup**:
   - Backup SQLite database
   - Backup Milvus data: `./cache_service/volumes/milvus`
   - Export Q&A pairs periodically

## Development Tips

- AI Service responses can be mocked for testing
- Cache service can run without OpenAI (using dummy embeddings)
- Main system has comprehensive error handling
- All services have health check endpoints

## Quick Stop All Services

```bash
# Stop main Q&A (Ctrl+C in terminal)
# Stop AI service (Ctrl+C in terminal)
# Stop cache service (Ctrl+C in terminal)

# Stop Milvus
cd cache_service
docker-compose down
```

## Next Steps

1. Add more Q&A pairs to cache for better hit rates
2. Customize AI prompts in `ai_service/main.py`
3. Adjust similarity threshold in `cache_service/main.py`
4. Add subject-specific question routing
5. Implement answer quality feedback loop
