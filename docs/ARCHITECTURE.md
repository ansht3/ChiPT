# System Architecture Diagram

## Complete Flow Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                              FRONTEND (Browser)                          │
│                         http://localhost:8000                            │
│                                                                          │
│  ┌─────────────────────┐              ┌──────────────────────┐          │
│  │   Student View      │              │  Instructor View     │          │
│  │  - Ask Questions    │              │  - View All Qs       │          │
│  │  - View Own Q&As    │              │  - Get AI Suggestion │          │
│  └─────────────────────┘              │  - Answer Questions  │          │
│                                       └──────────────────────┘          │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
                            JWT Authentication
                                    │
                                    ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                       MAIN Q&A BACKEND (FastAPI)                         │
│                         Port: 8000/8909                                  │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
│  │  Auth    │  │ Database │  │ Services │  │  Routes  │                │
│  │ (JWT)    │  │(SQLite)  │  │ (Logic)  │  │  (API)   │                │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘                │
│                                                                          │
│  Database Tables:                                                        │
│  - Users (id, email, password_hash, role)                               │
│  - Questions (id, user_id, content, status)                             │
│  - Answers (id, question_id, content, source)                           │
└──────────────────────────────────────────────────────────────────────────┘
                                    │
              ┌─────────────────────┴─────────────────────┐
              │                                           │
              ▼                                           ▼
┌──────────────────────────────┐         ┌──────────────────────────────┐
│   CACHE SERVICE (FastAPI)    │         │   AI SERVICE (FastAPI)       │
│      Port: 8902               │         │      Port: 8901              │
│                               │         │                              │
│  Endpoints:                   │         │  Endpoint:                   │
│  - POST /search               │         │  - POST /generate            │
│  - POST /add                  │         │                              │
│  - GET /health                │         │  Input:                      │
│  - GET /stats                 │         │  {                           │
│                               │         │    "question": "...",        │
│  Flow:                        │         │    "context": [Q&A pairs]   │
│  1. Query Rewriting (GLM-4.5) │         │  }                           │
│  2. Generate Embeddings       │         │                              │
│  3. Vector Search (Milvus)    │         │  Output:                     │
│  4. Similarity Match (≥0.85)  │         │  {                           │
│  5. Return Cached Answer      │         │    "answer": "..."           │
│                               │         │  }                           │
└──────────────────────────────┘         └──────────────────────────────┘
              │                                           │
              │                                           │
              ▼                                           ▼
┌──────────────────────────────┐         ┌──────────────────────────────┐
│   MILVUS (Vector DB)          │         │   OpenAI API                 │
│      Port: 19531              │         │   Port: 14345                │
│   (alternate port)            │         │                              │
│                               │         │  Endpoints:                  │
│  Components:                  │         │  - /v1/chat/completions      │
│  - Milvus Standalone          │         │  - /v1/embeddings            │
│  - Etcd (metadata)            │         │                              │
│  - MinIO (object storage)     │         │  Models:                     │
│                               │         │  - unsloth/GLM-4.5-Air       │
│  Collection: qa_cache         │         │  - text-embedding-ada-002    │
│  - question (VARCHAR)         │         │                              │
│  - answer (VARCHAR)           │         │  API Key: nada               │
│  - embedding (FLOAT_VECTOR)   │         │                              │
│  - Dimension: 1536            │         │                              │
│  - Index: IVF_FLAT            │         │                              │
└──────────────────────────────┘         └──────────────────────────────┘
              │
              └────────────────────────────────┐
                                               │
                              Uses embeddings from OpenAI API
```

## Request Flow Examples

### 1. Student Asks Question

```
Student Browser
    │
    │ POST /api/questions {"content": "What is ML?"}
    ▼
Main Q&A System
    │
    │ INSERT INTO questions (user_id, content, status='pending')
    ▼
SQLite Database
    │
    │ Return question_id
    ▼
Student sees "Pending" question
```

### 2. Instructor Gets AI Suggestion (Cache Hit)

```
Instructor Browser
    │
    │ GET /api/instructor/suggest/123
    ▼
Main Q&A System (services.py)
    │
    │ POST /search {"query": "What is ML?"}
    ▼
Cache Service
    │
    ├─ Rewrite query (GLM-4.5-Air)
    │  "What is ML?" → ["What is ML?", "Explain machine learning", ...]
    │
    ├─ Generate embeddings for each variation
    │  ▼
    │  OpenAI API → [0.123, -0.456, ..., 0.789] (1536 dims)
    │
    ├─ Search Milvus for similar vectors
    │  ▼
    │  Milvus → [{"question": "What is machine learning?", 
    │            "answer": "...", "score": 0.92}]
    │
    └─ Check score ≥ 0.85 → YES!
       │
       │ {"found": true, "answer": "Machine learning is..."}
       ▼
Main Q&A System
    │
    │ {"suggested_answer": "...", "source": "cached"}
    ▼
Instructor sees suggestion (instant, ~200ms)
```

### 3. Instructor Gets AI Suggestion (Cache Miss)

```
Instructor Browser
    │
    │ GET /api/instructor/suggest/123
    ▼
Main Q&A System (services.py)
    │
    │ POST /search {"query": "Explain gradient descent"}
    ▼
Cache Service
    │
    ├─ Search process (as above)
    │
    └─ Best score: 0.72 → BELOW threshold (0.85)
       │
       │ {"found": false, "answer": null}
       ▼
Main Q&A System
    │
    ├─ Get student's last 5 Q&A pairs from DB
    │
    │ POST /generate {
    │   "question": "Explain gradient descent",
    │   "context": [
    │     {"q": "What is backprop?", "a": "..."},
    │     {"q": "What is a loss function?", "a": "..."}
    │   ]
    │ }
    ▼
AI Service
    │
    ├─ Build prompt with context
    │  "You are a helpful TA. Previous Q&As: ... Question: ..."
    │
    │ POST /v1/chat/completions
    ▼
OpenAI API
    │
    │ {"choices": [{"message": {"content": "Gradient descent is..."}}]}
    ▼
AI Service
    │
    │ {"answer": "Gradient descent is..."}
    ▼
Main Q&A System
    │
    │ {"suggested_answer": "...", "source": "ai"}
    ▼
Instructor sees AI-generated suggestion (~3-5 seconds)
```

### 4. Instructor Sends Answer

```
Instructor edits/approves suggestion
    │
    │ POST /api/instructor/answer/123
    │ {"content": "Final answer...", "source": "ai"}
    ▼
Main Q&A System
    │
    ├─ INSERT INTO answers (question_id, content, source)
    ├─ UPDATE questions SET status='answered'
    │
    ├─ Add to cache (direct Milvus insertion)
    │  │
    │  ├─ Get embedding from LLM API
    │  │  POST http://localhost:11434/v1/embeddings
    │  │  {"model": "qwen3-embedding:8b-q8_0", "input": "question text"}
    │  │  → [0.123, -0.456, ..., 0.789] (4096 dims)
    │  │
    │  ├─ Normalize embedding vector
    │  │
    │  └─ Direct INSERT into Milvus
    │     connection: localhost:19531
    │     collection: qa_cache
    │     data: [question, answer, embedding]
    │     → Fast, no HTTP overhead, unlimited text length
    │
    ▼
SQLite Database
    │
    ▼
Student sees answer in their dashboard
```

**Note:** Answered questions are added directly to Milvus (not via HTTP), which is faster and supports unlimited text length. The embedding generation still uses the LLM API, but the Milvus insertion is direct.

## Data Models

### Main System Database (SQLite)

```
┌────────────────────────────────────┐
│            users                   │
├────────────────────────────────────┤
│ id (PK)                            │
│ email (UNIQUE)                     │
│ password_hash                      │
│ role (student/instructor)          │
│ created_at                         │
└────────────────────────────────────┘
                │
                │ 1:N
                ▼
┌────────────────────────────────────┐
│          questions                 │
├────────────────────────────────────┤
│ id (PK)                            │
│ user_id (FK → users.id)            │
│ content                            │
│ status (pending/answered)          │
│ created_at                         │
└────────────────────────────────────┘
                │
                │ 1:1
                ▼
┌────────────────────────────────────┐
│           answers                  │
├────────────────────────────────────┤
│ id (PK)                            │
│ question_id (FK → questions.id)    │
│ content                            │
│ source (ai/cached/manual)          │
│ created_at                         │
└────────────────────────────────────┘
```

### Cache Service Database (Milvus)

```
┌────────────────────────────────────────────┐
│         qa_cache collection                │
├────────────────────────────────────────────┤
│ id (auto_id)                               │
│ question (VARCHAR, max 10000)              │
│ answer (VARCHAR, max 50000)                │
│ embedding (FLOAT_VECTOR, dim=1536)         │
│                                            │
│ Index: IVF_FLAT on embedding               │
│ Metric: IP (Inner Product / Cosine Sim)   │
└────────────────────────────────────────────┘
```

## Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Frontend | HTML + Vanilla JS + Tailwind CSS | User interface |
| Main Backend | FastAPI + SQLAlchemy (async) | Core Q&A system |
| Database | SQLite (async via aiosqlite) | User/Q&A storage |
| Auth | JWT (python-jose) + bcrypt | Authentication |
| AI Service | FastAPI + httpx | Answer generation |
| Cache Service | FastAPI + pymilvus 2.6.1 | Semantic search |
| Vector DB | Milvus 2.6.1 | Vector similarity |
| LLM Provider | OpenAI API (custom endpoint) | AI & embeddings |
| Embeddings | text-embedding-ada-002 (1536d) | Semantic vectors |
| LLM | unsloth/GLM-4.5-Air | Answer generation & query rewriting |
