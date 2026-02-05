# Service Startup Order & Dependencies

## Quick Reference: Which Service Am I Running?

```bash
# In ai_service directory:
python main.py
# Output: "Starting AI Answer Generation Service on port 8901..."

# In cache_service directory:
python main.py  
# Output: "Starting Q&A Cache Service on port 8902..."

# In project directory:
uvicorn main:app --reload --port 8000
# Output: Uvicorn running on http://0.0.0.0:8000
```

## Dependency Chain

```
┌─────────────────────────────────────────────┐
│ 1. OpenAI API (localhost:14345)             │ ← Start FIRST
│    - Required by: AI Service, Cache Service │
└─────────────────────────────────────────────┘
                    │
                    ├──────────────────┬─────────────────┐
                    ▼                  ▼                 ▼
┌──────────────────────┐  ┌───────────────────┐  ┌──────────────────┐
│ 2. Milvus (19531)    │  │ 3. Cache Service  │  │ 4. AI Service    │
│    - Via Docker      │  │    (port 8902)    │  │    (port 8901)   │
└──────────────────────┘  └───────────────────┘  └──────────────────┘
                                    │                      │
                                    └──────────┬───────────┘
                                               ▼
                                    ┌──────────────────────┐
                                    │ 5. Main Q&A System   │
                                    │    (port 8000/8909)  │
                                    └──────────────────────┘
```

## Correct Startup Order

### Step 1: Start OpenAI API (REQUIRED)

```bash
# Your OpenAI-compatible API must be running on port 14345
# This is external to this project - make sure it's running first!

# Test if it's running:
curl http://localhost:14345/v1/models
```

**If OpenAI API is not running, both AI and Cache services will have errors.**

### Step 2: Start Milvus (for Cache Service)

```bash
cd cache_service
docker-compose up -d

# Verify it's running:
docker-compose ps
# Should show: chipt-milvus-standalone (healthy)
```

### Step 3: Start Cache Service

```bash
cd cache_service
python main.py

# Expected output:
# Starting Q&A Cache Service on port 8902...
# Milvus: localhost:19531
# OpenAI API: http://localhost:14345/v1
# Connected to Milvus
# Created and loaded collection 'qa_cache'
# Seeded 5 sample Q&A pairs
```

**If you see "All connection attempts failed":**
- Your OpenAI API at localhost:14345 is not running
- The service will still start but won't have sample data
- You can add data later via the `/add` endpoint

### Step 4: Start AI Service

```bash
cd ai_service
python main.py

# Expected output:
# Starting AI Answer Generation Service on port 8901...
# OpenAI API: http://localhost:14345/v1
# Model: gpt-4
```

### Step 5: Start Main Q&A System

```bash
cd project
uvicorn main:app --reload --port 8000

# Expected output:
# Seed data created: instructor@test.com and student@test.com
# Application startup complete
```

## What Each Service Needs

| Service | Port | Needs | Optional |
|---------|------|-------|----------|
| OpenAI API | 14345 | Nothing | - |
| Milvus | 19531 | Nothing | - |
| Cache Service | 8902 | Milvus, OpenAI API | OpenAI for seeding only |
| AI Service | 8901 | OpenAI API | - |
| Main Q&A | 8000 | Cache Service, AI Service | Can run without, but won't get suggestions |

## Running Without OpenAI API

If your OpenAI API is not available:

### Cache Service
- ✅ Will start successfully
- ✅ Will connect to Milvus
- ⚠️ Won't seed sample data
- ⚠️ Search will fail (needs embeddings)
- ✅ Can add data later when OpenAI API is available

### AI Service
- ⚠️ Will start but can't generate answers
- ❌ All generation requests will fail

### Main Q&A System
- ✅ Will start successfully
- ✅ Students can ask questions
- ✅ Questions get stored in database
- ⚠️ Instructors won't get AI suggestions
- ✅ Instructors can still manually answer

## Troubleshooting

### "All connection attempts failed"

```bash
# Check if OpenAI API is running
curl http://localhost:14345/v1/models

# If not, start your OpenAI API first
# Then restart the cache/AI services
```

### "error while attempting to bind on address"

```bash
# Port is already in use, kill the process
fuser -k 8901/tcp  # For AI service
fuser -k 8902/tcp  # For cache service

# Or use a different port
python main.py 8911  # AI on port 8911
python main.py 8912  # Cache on port 8912
```

### "Cannot connect to Milvus"

```bash
# Start Milvus if not running
cd cache_service
docker-compose up -d

# Check it's healthy
docker-compose ps
```

## Quick Health Check All Services

```bash
# Check OpenAI API
curl -s http://localhost:14345/v1/models && echo "✓ OpenAI API" || echo "✗ OpenAI API"

# Check Milvus
docker ps | grep chipt-milvus-standalone && echo "✓ Milvus" || echo "✗ Milvus"

# Check Cache Service
curl -s http://localhost:8902/health && echo "✓ Cache Service" || echo "✗ Cache Service"

# Check AI Service
curl -s http://localhost:8901/health && echo "✓ AI Service" || echo "✗ AI Service"

# Check Main Q&A
curl -s http://localhost:8000/ >/dev/null && echo "✓ Main Q&A" || echo "✗ Main Q&A"
```

## Testing Without Full Stack

You can test individual services:

### Test Cache Service (without OpenAI)
```bash
# Start Milvus only
cd cache_service
docker-compose up -d

# Start cache service (will warn about missing OpenAI)
python main.py

# Test health endpoint
curl http://localhost:8902/health
```

### Test AI Service (with OpenAI)
```bash
# Make sure OpenAI API is running
# Start AI service
cd ai_service
python main.py

# Test generation
curl -X POST http://localhost:8901/generate \
  -H "Content-Type: application/json" \
  -d '{"question": "What is 2+2?", "context": []}'
```

## Minimal Startup (Testing Only)

For quick testing without external dependencies:

```bash
# Just the main Q&A system
cd project
uvicorn main:app --reload --port 8000

# Students can ask questions
# They'll be stored in SQLite
# Instructors can answer manually
# No AI suggestions available
```
