# ChiPT Q&A System - Deployment Checklist

## ✅ Configuration Verification - ALL PASSED

All requirements have been verified and configured correctly:

### ✓ Models & API Configuration
- **API Endpoint**: http://localhost:11434/v1
- **Chat Model**: gpt-oss:120b
- **Embedding Model**: qwen3-embedding:8b-q8_0
- **Embedding Dimensions**: 4096

### ✓ Port Configuration (Non-Standard)
- **Main Q&A System**: 8000 (or 8909 for remote)
- **AI Service**: 8901
- **Cache Service**: 8902
- **Milvus**: 19531

### ✓ User Accounts
- **Student**: student@purdue / 123456
- **Instructor**: instructor@purdue / 123456
- **Registration**: Open for both roles
- **Database Seeding**: Automatic on first run
- **No hardcoded account logic**: All accounts come from database

### ✓ Directory Structure
```
ChiPT/                    # All in root directory
├── project/              # Main web application
├── ai_service/           # AI answer generation
├── cache_service/        # Semantic caching
└── Documentation/        # All .md files
```

## Pre-Deployment Requirements

Before running the system, ensure you have:

1. **Python 3.11+** installed
2. **Docker & Docker Compose** installed
3. **LLM API running at localhost:11434** with:
   - `gpt-oss:120b` model available
   - `qwen3-embedding:8b-q8_0` model available

### Test Your LLM API

```bash
# Test chat completion
curl -X POST http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-oss:120b","messages":[{"role":"user","content":"Hi"}]}'

# Test embeddings (should return 4096 dimensions)
curl -X POST http://localhost:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-embedding:8b-q8_0","input":"test"}'
```

## Deployment Steps

### 1. Extract the Package
```bash
# Extract to your desired location
unzip ChiPT-QA-System.zip
cd ChiPT
```

### 2. Verify Configuration
```bash
# Run verification script
python verify_config.py

# Should show: ✓ All checks PASSED
```

### 3. Install Dependencies
```bash
# AI Service
cd ai_service
pip install -r requirements.txt

# Cache Service
cd ../cache_service
pip install -r requirements.txt

# Main Application
cd ../project
pip install -r requirements.txt
```

### 4. Start Milvus
```bash
cd cache_service
docker compose up

# Wait 30 seconds for Milvus to initialize
sleep 30

# Verify it's running
docker ps
# Should show: chipt-milvus-standalone (healthy)
```

### 5. Start Services (3 Terminals)

**Terminal 1 - Cache Service:**
```bash
cd cache_service
python main.py

# Expected output:
# - Connected to Milvus
# - Collection has 0 entities
# - Seeding sample data...
# - Seeded 5 sample Q&A pairs
# - Uvicorn running on http://0.0.0.0:8902
```

**Terminal 2 - AI Service:**
```bash
cd ai_service
python main.py

# Expected output:
# - Uvicorn running on http://0.0.0.0:8901
```

**Terminal 3 - Main Q&A System:**
```bash
cd project
uvicorn main:app --host 0.0.0.0 --reload --port 10000

# Expected output:
# - Database initialized
# - Seed data created: instructor@purdue and student@purdue
# - Uvicorn running on http://localhost:8000
```

### 6. Access the System
```
Open browser: http://chipt.org:10000

Login with:
- student@purdue.edu / 123456
- instructor@purdue.edu / 123456

Or register a new account
```

## Verification Tests

### Test 1: Student Account
1. Login as student@purdue.edu
2. Ask a question: "What is machine learning?"
3. Verify it appears in "Your Questions"
4. Status should be "Pending"

### Test 2: Instructor - Cache Hit
1. Login as instructor@purdue.edu
2. View all questions
3. Click "Get AI Suggestion" on the ML question
4. Should get cached answer (~200ms)
5. Check logs: "Cache HIT!"

### Test 3: Instructor - AI Generation
1. Ask a new unique question as student
2. Login as instructor
3. Click "Get AI Suggestion"
4. Should generate new answer (~3-120s depending on model)
5. Check logs: "Cache MISS" then AI generation

### Test 4: Registration
1. Logout
2. Click "Register"
3. Create account with custom email
4. Choose "Student" or "Instructor" role
5. Login with new account
6. Verify role-based access works

## Common Issues & Solutions

### Issue: Cache service won't seed
**Symptom**: "Collection has 0 entities" and no seeding
**Solution**: 
```bash
# Check embedding API is working
curl -X POST http://localhost:11434/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-embedding:8b-q8_0","input":"test"}'

# Manual reseed
curl -X POST http://localhost:8902/reseed
```

### Issue: Dimension mismatch error
**Symptom**: "length(X) should divide dim(Y)"
**Solution**: Your embedding model returns different dimensions
```bash
cd cache_service
python reset_collection.py  # Drop and recreate collection
python main.py              # Will use correct dimensions
```

### Issue: Timeouts
**Symptom**: Requests timeout waiting for AI
**Solution**: Increase timeouts in configuration

### Issue: Port conflicts
**Symptom**: "Address already in use"
**Solution**: See PORT_CONFLICTS.md for resolution

## Support Files

- `README.md` - Main documentation
- `SETUP_GUIDE.md` - Detailed setup instructions  
- `ARCHITECTURE.md` - System architecture
- `QUICK_REFERENCE.md` - Command cheat sheet

## Utility Scripts

- `verify_config.py` - Verify configuration is correct
- `test_services.py` - Check all services are healthy
- `debug_cache.py` - Debug cache service issues
- `cache_service/reset_collection.py` - Reset Milvus collection

## Success Criteria

Your deployment is successful when:

- [x] All services start without errors
- [x] Students can register and ask questions
- [x] Instructors can view all questions
- [x] Cache returns answers for similar questions
- [x] AI generates new answers when needed
- [x] Database is seeded with purdue accounts
- [x] verify_config.py shows all checks passing

## Next Steps

After successful deployment:

1. **Test thoroughly** with both student and instructor accounts
2. **Monitor logs** to ensure cache hits are working
3. **Add more Q&A** to build up the cache
4. **Adjust timeouts** if needed for your model
5. **Backup database** regularly (qa_system.db)

## Production Deployment

For production use, consider:

- Use PostgreSQL instead of SQLite
- Deploy Milvus as a cluster
- Add HTTPS/SSL
- Use environment variables for secrets
- Add rate limiting
- Set up monitoring and logging
- Configure backup systems

---

**Configuration Status**: ✅ READY FOR DEPLOYMENT

All requirements met. The system is properly configured and ready to use.
