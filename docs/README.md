# ChiPT Q&A System

Complete Q&A system with AI-powered answer suggestions, semantic caching, and role-based access control.

## System Configuration

### Models & API
- **LLM Model**: `gpt-oss:120b`
- **Embedding Model**: `qwen3-embedding:8b-q8_0`
- **Embedding Dimensions**: 4096
- **API Endpoint**: `http://localhost:11434/v1`
- **API Key**: `nada`

### Service Ports (Non-Standard to Avoid Conflicts)
- **Main Q&A System**: 8000 (or 8909 for remote access)
- **AI Service**: 8901
- **Cache Service**: 8902
- **Milvus (ChiPT)**: 19531 (standard: 19530)

### Default User Accounts
The database is automatically seeded with:
- **Student**: `student@purdue.edu` / `123456`
- **Instructor**: `instructor@purdue.edu` / `123456`

Users can also register new accounts as either student or instructor during registration.

## Project Structure

```
ChiPT/
├── project/              # Main Q&A web application
│   ├── main.py           # FastAPI application
│   ├── database.py       # SQLAlchemy models & seeding
│   ├── auth.py           # JWT authentication
│   ├── services.py       # External API integration
│   ├── schemas.py        # Pydantic models
│   ├── templates/        # HTML templates
│   ├── static/           # JavaScript & CSS
│   └── requirements.txt
│
├── ai_service/           # AI answer generation
│   ├── main.py           # FastAPI service
│   ├── requirements.txt
│   └── README.md
│
├── cache_service/        # Semantic search cache
│   ├── main.py           # FastAPI service
│   ├── docker-compose.yml # Milvus setup
│   ├── reset_collection.py # Collection reset tool
│   ├── requirements.txt
│   └── README.md
│
└── Documentation/
    ├── SETUP_GUIDE.md
    ├── ARCHITECTURE.md
    ├── PORT_CONFIGURATION.md
    ├── TIMEOUT_CONFIGURATION.md
    ├── QUICK_REFERENCE.md
    └── PORT_CONFLICTS.md
```

## Quick Start

### Prerequisites
1. Python 3.11+
2. Docker & Docker Compose (for Milvus)
3. LLM API running at `http://localhost:11434/v1` with models:
   - `gpt-oss:120b` (chat completions)
   - `qwen3-embedding:8b-q8_0` (embeddings)

### Installation

**Step 1: Start Milvus (Vector Database)**
```bash
cd cache_service
docker-compose up -d
```

**Step 2: Install Dependencies**
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

**Step 3: Start All Services**

Terminal 1 - Cache Service:
```bash
cd cache_service
python main.py
# Runs on http://localhost:8902
```

Terminal 2 - AI Service:
```bash
cd ai_service
python main.py
# Runs on http://localhost:8901
```

Terminal 3 - Main Q&A System:
```bash
cd project
uvicorn main:app --reload --port 8000
# Or for remote access:
# uvicorn main:app --host 0.0.0.0 --reload --port 8909
```

**Step 4: Access the System**

Open browser to: **http://localhost:8000**

Login with:
- Student: `student@purdue` / `123456`
- Instructor: `instructor@purdue` / `123456`

Or register a new account as student or instructor.

## How It Works

### Student Workflow
1. Login as student
2. Ask questions via the interface
3. View submitted questions and their answers
4. Questions appear as "pending" until answered

### Instructor Workflow
1. Login as instructor
2. View all pending questions from all students
3. Click "Get AI Suggestion" for any question:
   - **Cache Hit** (~200ms): Returns previously answered similar question
   - **Cache Miss**: Generates new AI answer (~3-120s depending on model)
4. Review/edit the suggested answer
5. Send answer to student
6. **Answer is automatically added to cache** for future reuse
7. Answer is marked with source (ai/cached/manual)

### System Flow
```
Question → Cache Check → [Hit: Cached Answer | Miss: AI Generation] → Instructor Review → Student
```

## Configuration

### Adjust Timeouts for Your Model

If using very large models (120B+), you may need to increase timeouts:

**AI Service** (`ai_service/main.py`):
```python
REQUEST_TIMEOUT = 300.0  # 5 minutes for 120B models
```

**Cache Service** (`cache_service/main.py`):
```python
REQUEST_TIMEOUT = 180.0  # 3 minutes
```

**Main System** (`project/services.py`):
```python
REQUEST_TIMEOUT = 360.0  # 6 minutes total
```

See `TIMEOUT_CONFIGURATION.md` for detailed guidance.

### Change Model Configuration

**AI Service** (`ai_service/main.py`):
```python
OPENAI_BASE_URL = "http://localhost:11434/v1"
MODEL_NAME = "gpt-oss:120b"
```

**Cache Service** (`cache_service/main.py`):
```python
EMBEDDING_MODEL = "qwen3-embedding:8b-q8_0"
REWRITE_MODEL = "gpt-oss:120b"
EMBEDDING_DIM = 4096  # Must match your embedding model's output
```

### Change Ports

Edit the port numbers in:
- `project/services.py`: CACHE_API_URL, AI_API_URL
- `ai_service/main.py`: Bottom of file
- `cache_service/main.py`: Bottom of file

## Troubleshooting

### Collection Dimension Mismatch

If you see: `the length(X) of float data should divide the dim(Y)`

Your embedding model returns different dimensions. Fix:
1. Update `EMBEDDING_DIM` in `cache_service/main.py`
2. Reset collection:
   ```bash
   cd cache_service
   python reset_collection.py
   ```

### Port Already in Use

```bash
# Find what's using the port
lsof -i :8901

# Kill the process
kill <PID>
```

Or use custom ports:
```bash
python main.py 8911  # Use port 8911 instead of 8901
```

### Timeouts

See `TIMEOUT_CONFIGURATION.md` for detailed timeout tuning.

## Features

- ✅ **Role-Based Access**: Students see only their questions, instructors see all
- ✅ **AI-Powered Suggestions**: Uses gpt-oss:120b for intelligent answers
- ✅ **Semantic Caching**: Finds similar questions using vector similarity
- ✅ **Direct Cache Insertion**: Fast Milvus insertion without HTTP overhead
- ✅ **Auto-Cache Population**: Answered questions automatically added to cache
- ✅ **Query Rewriting**: Generates alternative phrasings for better matching
- ✅ **Context-Aware**: AI considers student's previous Q&A history
- ✅ **Source Tracking**: Answers tagged as ai/cached/manual
- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **Auto-Seeding**: Database and cache pre-populated with examples
- ✅ **Non-Standard Ports**: Avoids conflicts with existing services
- ✅ **Unlimited Text Length**: Direct database insertion supports any answer length

## Documentation

- `SETUP_GUIDE.md` - Detailed setup instructions
- `ARCHITECTURE.md` - System architecture and data flow
- `PORT_CONFIGURATION.md` - Port configuration guide
- `TIMEOUT_CONFIGURATION.md` - Timeout tuning for different models
- `QUICK_REFERENCE.md` - Command cheat sheet
- `PORT_CONFLICTS.md` - Resolving port conflicts

## Security Notes

For production deployment:
1. Change `SECRET_KEY` in `project/auth.py`
2. Use environment variables for sensitive config
3. Enable HTTPS
4. Use PostgreSQL instead of SQLite
5. Add rate limiting
6. Deploy Milvus in cluster mode

## Support

For issues or questions:
1. Check the troubleshooting sections in the READMEs
2. Review the detailed documentation files
3. Check logs in each service terminal

## License

This project is provided as-is for educational purposes.
