from fastapi import FastAPI, Depends, HTTPException, status, Request, WebSocket, WebSocketDisconnect, UploadFile, File
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from contextlib import asynccontextmanager
from typing import List, Optional
import logging
import jwt
import traceback
import sys
import os

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import get_db, init_db, close_db, seed_data, User, Question, Message, MessageRole
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_instructor, SECRET_KEY, ALGORITHM
)
from schemas import (
    RegisterRequest, RegisterResponse, LoginRequest, LoginResponse,
    UserResponse, QuestionCreate, QuestionCreateResponse,
    QuestionResponse, MessageResponse, InstructorQuestionResponse,
    SuggestAnswerResponse, MessageCreate, MessageCreateResponse,
    KBCreateRequest, KBFileDeleteRequest
)
from services import (
    get_suggested_answer,
    get_knowledge_bases,
    create_knowledge_base,
    get_kb_details,
    upload_file_to_kb,
    delete_file_from_kb
)
from websocket_manager import manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_data()
    
    yield # The APP is running here

    # --- Shutdown ---
    logger.warning("Shutting down: Closing database connections...")
    await close_db()

app = FastAPI(title="ChiPT Q&A System", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = None
):
    """WebSocket endpoint for real-time updates."""
    if not token:
        await websocket.close(code=1008)
        return
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
        
        if not user_id:
            await websocket.close(code=1008)
            return
        
        await manager.connect(websocket, user_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                if data == "ping":
                    await websocket.send_text("pong")
        
        except WebSocketDisconnect:
            manager.disconnect(websocket)
    
    except jwt.ExpiredSignatureError:
        await websocket.close(code=1008)
    except jwt.InvalidTokenError:
        await websocket.close(code=1008)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)


@app.post("/api/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    new_user = User(
        email=request.email,
        password_hash=hash_password(request.password),
        role="student"
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return RegisterResponse(user_id=new_user.id)


@app.post("/api/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token."""
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    role_str = user.role if isinstance(user.role, str) else user.role.value
    access_token = create_access_token(user.id, role_str)
    
    return LoginResponse(access_token=access_token, role=role_str)


@app.get("/api/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    role_str = current_user.role if isinstance(current_user.role, str) else current_user.role.value
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        role=role_str
    )


@app.post("/api/questions", response_model=QuestionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    request: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new question (students only)."""
    user_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
    if user_role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can ask questions"
        )
    
    new_question = Question(
        user_id=current_user.id,
        content=request.content,
        status="pending"
    )
    
    db.add(new_question)
    await db.commit()
    await db.refresh(new_question)
    
    # Prepare question data for broadcast
    question_data = {
        "id": new_question.id,
        "user_email": current_user.email,
        "content": new_question.content,
        "status": "pending",
        "created_at": new_question.created_at.isoformat(),
        "messages": []
    }
    
    # Broadcast to instructors
    await manager.broadcast_new_question(question_data, db)
    print("Broadcasted new question to instructors")  
    # Also send to the student who created it
    await manager.send_to_user(current_user.id, {
        "type": "new_question",
        "data": question_data
    })
    print("Sent new question to student")
    # try:
    #     print(1/0)
    # except Exception as e:
    #     traceback.print_exc()  # Prints full stack trace
    
    return QuestionCreateResponse(question_id=new_question.id)


@app.get("/api/questions", response_model=List[QuestionResponse])
async def get_my_questions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all questions for the current user."""
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.messages))
        .where(Question.user_id == current_user.id)
        .order_by(Question.created_at.desc())
    )
    questions = result.scalars().all()
    
    response = []
    for question in questions:
        messages_data = []
        for msg in question.messages:
            msg_role = msg.role if isinstance(msg.role, str) else msg.role.value
            messages_data.append(MessageResponse(
                id=msg.id,
                content=msg.content,
                role=msg_role,
                source=msg.source,
                created_at=msg.created_at
            ))
        
        question_status = question.status if isinstance(question.status, str) else question.status.value
        response.append(QuestionResponse(
            id=question.id,
            content=question.content,
            status=question_status,
            created_at=question.created_at,
            messages=messages_data
        ))
    
    return response


@app.get("/api/instructor/questions", response_model=List[InstructorQuestionResponse])
async def get_all_questions(
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db)
):
    """Get all questions (instructors only)."""
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.messages), selectinload(Question.user))
        .order_by(Question.created_at.desc())
    )
    questions = result.scalars().all()
    
    response = []
    for question in questions:
        messages_data = []
        for msg in question.messages:
            msg_role = msg.role if isinstance(msg.role, str) else msg.role.value
            messages_data.append(MessageResponse(
                id=msg.id,
                content=msg.content,
                role=msg_role,
                source=msg.source,
                created_at=msg.created_at
            ))
        
        question_status = question.status if isinstance(question.status, str) else question.status.value
        response.append(InstructorQuestionResponse(
            id=question.id,
            user_email=question.user.email,
            content=question.content,
            status=question_status,
            created_at=question.created_at,
            messages=messages_data
        ))
    
    return response


@app.get("/api/instructor/suggest/{question_id}", response_model=SuggestAnswerResponse)
async def suggest_answer(
    question_id: int,
    kb_name: str = None,
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db)
):
    """Get suggested answer for a question (instructors only)."""
    result = await db.execute(
        select(Question).where(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    try:
        suggestion = await get_suggested_answer(db, question_id, kb_name=kb_name)
        return SuggestAnswerResponse(
            suggested_answer=suggestion["suggested_answer"],
            source=suggestion["source"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting suggestion: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate suggestion"
        )


@app.post("/api/questions/{question_id}/messages", response_model=MessageCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    question_id: int,
    request: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Add a message to a question thread (students and instructors)."""
    result = await db.execute(
        select(Question)
        .options(selectinload(Question.user))
        .where(Question.id == question_id)
    )
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    
    user_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
    
    if user_role == "student" and question.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only reply to your own questions"
        )
    
    new_message = Message(
        question_id=question_id,
        content=request.content,
        role=MessageRole.instructor if user_role == "instructor" else MessageRole.student,
        source=request.source
    )
    
    if user_role == "instructor":
        question.status = "answered"
    
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    
    message_data = {
        "id": new_message.id,
        "content": new_message.content,
        "role": user_role,
        "source": new_message.source,
        "created_at": new_message.created_at.isoformat()
    }
    
    broadcast_data = {
        "type": "new_message",
        "data": {
            "question_id": question_id,
            "message": message_data
        }
    }
    
    await manager.send_to_user(question.user_id, broadcast_data)
    await manager.broadcast_to_all_instructors(broadcast_data, db)
    
    if user_role == "instructor":
        from services import add_to_cache
        try:
            await add_to_cache(question.content, request.content)
            logger.info(f"Added Q&A to cache: question_id={question_id}")
        except Exception as e:
            logger.error(f"Failed to add to cache: {str(e)}")
    
    return MessageCreateResponse(message_id=new_message.id)


# --- Knowledge Base Management Endpoints (Instructors Only) ---

class InstructorConfig(BaseModel):
    active_kb: Optional[str] = None

# Config persistence helper
CONFIG_FILE = "project_config.json"

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

import json
import os

@app.get("/api/instructor/config", response_model=InstructorConfig)
async def get_instructor_config(current_user: User = Depends(require_instructor)):
    """Get instructor configuration (e.g. active KB)."""
    data = load_config()
    return InstructorConfig(active_kb=data.get("active_kb"))

@app.post("/api/instructor/config")
async def update_instructor_config(config: InstructorConfig, current_user: User = Depends(require_instructor)):
    """Update instructor configuration."""
    data = load_config()
    if config.active_kb is not None:
        data["active_kb"] = config.active_kb
    save_config(data)
    return {"message": "Configuration updated", "config": config}


@app.get("/api/instructor/kbs")
async def list_knowledge_bases_endpoint(
    current_user: User = Depends(require_instructor)
):
    """List available knowledge bases."""
    kbs = await get_knowledge_bases()
    return {"kbs": kbs}

@app.post("/api/instructor/kbs", status_code=status.HTTP_201_CREATED)
async def create_kb_endpoint(
    request: KBCreateRequest,
    current_user: User = Depends(require_instructor)
):
    """Create a new knowledge base."""
    success = await create_knowledge_base(request.name)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create Knowledge Base")
    return {"message": "Created successfully"}

@app.get("/api/instructor/kbs/{name}")
async def get_kb_details_endpoint(
    name: str,
    current_user: User = Depends(require_instructor)
):
    """Get KB details."""
    details = await get_kb_details(name)
    return details

@app.post("/api/instructor/kbs/{name}/files")
async def upload_file_to_kb_endpoint(
    name: str,
    file: UploadFile = File(...),
    current_user: User = Depends(require_instructor)
):
    """Upload file to KB."""
    content = await file.read()
    success = await upload_file_to_kb(name, file.filename, content)
    if not success:
         raise HTTPException(status_code=500, detail="Failed to upload file")
    return {"message": "Uploaded successfully"}

@app.delete("/api/instructor/kbs/{name}/files/{filename}")
async def delete_file_from_kb_endpoint(
    name: str,
    filename: str,
    current_user: User = Depends(require_instructor)
):
    """Delete file from KB."""
    success = await delete_file_from_kb(name, filename)
    if not success:
         raise HTTPException(status_code=500, detail="Failed to delete file")
    return {"message": "Deleted successfully"}

