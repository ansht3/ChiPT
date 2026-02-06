# Quick Reference Guide

## Starting Services

### 1. Start Milvus
```bash
cd cache_service
docker-compose up -d
```

### 2. Start Cache Service
```bash
cd cache_service
python main.py
# Runs on http://localhost:8902
```

### 3. Start AI Service
```bash
cd ai_service
python main.py
# Runs on http://localhost:8901
```

### 4. Start Main Q&A System
```bash
cd project
uvicorn main:app --reload --port 8000
# Or for remote access:
uvicorn main:app --host 0.0.0.0 --reload --port 8909
```

## Stopping Services

```bash
# Stop services: Ctrl+C in each terminal

# Stop Milvus:
cd cache_service
docker-compose down
```

## Test Accounts

- **Student**: student@purdue / 123456
- **Instructor**: instructor@purdue / 123456

Or register new accounts as needed.

## Health Checks

```bash
# Main Q&A
curl http://localhost:8000/api/me

# AI Service
curl http://localhost:8901/health

# Cache Service
curl http://localhost:8902/health
curl http://localhost:8902/stats
```

## Common API Calls

### Ask a Question (Student)
```bash
curl -X POST http://localhost:8000/api/questions \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "What is machine learning?"}'
```

### Search Cache
```bash
curl -X POST http://localhost:8902/search \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

### Generate AI Answer
```bash
curl -X POST http://localhost:8901/generate \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is a neural network?",
    "context": []
  }'
```

### Add to Cache
```bash
curl -X POST "http://localhost:8902/add?question=What%20is%20ReLU?&answer=ReLU%20is%20an%20activation%20function"
```

## Troubleshooting

### Timeout Errors

If you see timeout warnings in logs:
```bash
WARNING:services:Timeout while checking cached answer
WARNING:services:Timeout while generating AI answer
ERROR:__main__:OpenAI API request timed out
```

**Quick fix for large models (30B+):**
```python
# project/services.py
REQUEST_TIMEOUT = 300.0  # Increase from 180.0

# ai_service/main.py  
REQUEST_TIMEOUT = 240.0  # Increase from 120.0

# cache_service/main.py
REQUEST_TIMEOUT = 180.0  # Increase from 120.0
```

See `TIMEOUT_CONFIGURATION.md` for detailed guide.

### Milvus Issues
```bash
cd cache_service
docker-compose down
docker-compose up -d
docker-compose logs -f chipt-milvus-standalone
```

### Reset Database
```bash
cd project
rm qa_system.db
# Restart main service - will recreate DB with seed data
```

### Clear Milvus Data
```bash
cd cache_service
docker-compose down
rm -rf volumes/
docker-compose up -d
# Restart cache service - will recreate collection with seed data
```

## File Locations

- **Main DB**: `project/qa_system.db`
- **Milvus Data**: `cache_service/volumes/milvus/`
- **Logs**: Terminal outputs (no log files by default)

## Service Dependencies

```
Main Q&A System
  └─ Cache Service
      └─ Milvus (Docker)
      └─ OpenAI API (localhost:14345)
  └─ AI Service
      └─ OpenAI API (localhost:14345)
```

## Performance Tips

1. **Improve Cache Hit Rate**:
   - Add more Q&A pairs to cache
   - Lower similarity threshold in cache_service/main.py

2. **Faster Responses**:
   - Cache service ~200ms
   - AI service ~2-5s
   - Use cache for common questions

3. **Monitor Usage**:
   ```bash
   curl http://localhost:8902/stats
   ```

## Configuration Files

| File | Purpose |
|------|---------|
| `project/auth.py` | JWT secret, token expiry |
| `project/services.py` | API URLs, **timeouts** |
| `ai_service/main.py` | OpenAI URL, model, **timeout** |
| `cache_service/main.py` | Milvus config, similarity threshold, **timeout** |
| `cache_service/docker-compose.yml` | Milvus settings |

**Important:** If using large models (30B+), increase timeouts. See `TIMEOUT_CONFIGURATION.md`.

## Ports

| Service | Port | Protocol |
|---------|------|----------|
| Main Q&A | 8000/8909 | HTTP |
| AI Service | 8901 | HTTP |
| Cache Service | 8902 | HTTP |
| Milvus (ChiPT) | 19531 | gRPC |
| Milvus Health | 9092 | HTTP |
| MinIO API | 9002 | HTTP |
| MinIO Console | 9003 | HTTP |
| Etcd | 2379 | HTTP |

**Note:** ChiPT Milvus uses port 19531 to avoid conflicts with existing Milvus on port 19530.

## Quick Test

```bash
# Run automated tests
python test_services.py
```

## Development Workflow

1. Make changes to service
2. Service auto-reloads (if using --reload)
3. Test via web UI or curl
4. Check logs in terminal
5. Commit changes

## Production Checklist

- [ ] Change SECRET_KEY in project/auth.py
- [ ] Change OPENAI_API_KEY in services
- [ ] Use PostgreSQL instead of SQLite
- [ ] Add HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Set up monitoring
- [ ] Configure backups
- [ ] Use environment variables
- [ ] Deploy Milvus cluster
- [ ] Add authentication to AI/Cache services
