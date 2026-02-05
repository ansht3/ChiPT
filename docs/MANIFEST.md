# ChiPT Q&A System - Package Manifest

## Configuration Summary

### Models & API
- **LLM**: gpt-oss:120b
- **Embeddings**: qwen3-embedding:8b-q8_0 (4096 dimensions)
- **API URL**: http://localhost:11434/v1
- **API Key**: nada

### Ports (Non-Standard)
- Main Q&A: 10000 (or 8909)
- AI Service: 8901
- Cache Service: 8902
- Milvus: 19531

### User Accounts (Auto-Seeded)
- Student: student@purdue.edu / 123456
- Instructor: instructor@purdue.edu / 123456

## Package Contents

### Root Directory
```
ChiPT/
├── README.md                      # Main documentation
├── verify_config.py               # Configuration verification tool
├── test_services.py               # Service health check tool
├── debug_cache.py                 # Cache debugging tool
├── start_services.sh              # Startup helper script
```

### Main Q&A Application
```
project/
├── main.py                        # FastAPI application
├── database.py                    # Database models & seeding
├── auth.py                        # JWT authentication
├── services.py                    # External API integration
├── schemas.py                     # Pydantic models
├── requirements.txt               # Python dependencies
├── README.md                      # Project-specific docs
├── verify.py                      # File structure verification
├── templates/
│   └── index.html                 # Main UI template
└── static/
    └── app.js                     # Frontend JavaScript
```

### AI Service
```
ai_service/
├── main.py                        # FastAPI service
├── requirements.txt               # Dependencies
└── README.md                      # Service documentation
```

### Cache Service
```
cache_service/
├── main.py                        # FastAPI service
├── docker-compose.yml             # Milvus setup
├── reset_collection.py            # Collection reset tool
├── requirements.txt               # Dependencies
└── README.md                      # Service documentation
```

## Verification Checklist

Before packaging, verify:

- [x] OPENAI_BASE_URL = http://localhost:11434/v1 (all services)
- [x] MODEL_NAME = gpt-oss:120b (ai_service)
- [x] EMBEDDING_MODEL = qwen3-embedding:8b-q8_0 (cache_service)
- [x] REWRITE_MODEL = gpt-oss:120b (cache_service)
- [x] EMBEDDING_DIM = 4096 (cache_service)
- [x] Student account: student@purdue / 123456
- [x] Instructor account: instructor@purdue / 123456
- [x] AI service port: 8901
- [x] Cache service port: 8902
- [x] Milvus port: 19531
- [x] No hardcoded if statements for test accounts

## Quick Verification

Run from root directory:
```bash
python verify_config.py
```

Should show all checks passing.

## Installation Order

1. Start Milvus (cache_service/docker-compose.yml)
2. Install dependencies in all three directories
3. Start cache_service (port 8902)
4. Start ai_service (port 8901)
5. Start project (port 10000)

## First Run

On first run, the system will automatically:
1. Create SQLite database (project/qa_system.db)
2. Seed with student@purdue and instructor@purdue accounts
3. Create Milvus collection with 4096 dimensions
4. Seed cache with 5 sample Q&A pairs

## Dependencies

### System Requirements
- Python 3.11+
- Docker & Docker Compose
- LLM API at localhost:11434 with:
  - gpt-oss:120b model
  - qwen3-embedding:8b-q8_0 model

### Python Packages
All listed in respective requirements.txt files:
- FastAPI
- Uvicorn
- SQLAlchemy (async)
- Pydantic
- PyMilvus
- httpx
- python-jose
- passlib/bcrypt
- etc.

## Notes

- Timeouts configured for large models (120B)
- Non-standard ports to avoid conflicts
- Database auto-seeds on first run
- No special handling for test accounts - they come from database
- All configuration in code (no environment variables required, but supported)
