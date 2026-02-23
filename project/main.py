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
from datetime import datetime, timedelta

# Add parent directory to sys.path to allow importing config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import (
    get_db, init_db, close_db, seed_data, User, Question, Message, 
    MessageRole, normalize_email, Class, Enrollment, AuditLog, ClassRole, TAAllowlist
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_instructor, require_verified_user,
    require_class_instructor, SECRET_KEY, ALGORITHM
)
from schemas import (
    RegisterRequest, RegisterResponse, LoginRequest, LoginResponse,
    UserResponse, QuestionCreate, QuestionCreateResponse,
    QuestionResponse, MessageResponse, InstructorQuestionResponse,
    SuggestAnswerResponse, MessageCreate, MessageCreateResponse,
    KBCreateRequest, KBFileDeleteRequest, VerifyEmailRequest,
    ClassCreateRequest, ClassResponse, RotateCodeResponse, JoinClassRequest,
    RosterResponse, RosterUserResponse, SetRoleRequest, UpdateEmailRequest
)
from email_utils import generate_verification_token, send_verification_email
import secrets
import string
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

app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
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
    normalized_email = normalize_email(request.email)
    
    result = await db.execute(
        select(User).where(User.email == normalized_email)
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    token = generate_verification_token()
    
    new_user = User(
        email=normalized_email,
        password_hash=hash_password(request.password),
        global_role="student",
        verify_token_hash=hash_password(token),  # Re-use our password hasher for the token!
        verify_expires_at=datetime.utcnow() + timedelta(minutes=15),
        is_instructor_pending=(request.intent == "instructor")
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    await send_verification_email(new_user.email, token)
    
    return RegisterResponse(user_id=new_user.id)


@app.post("/api/verify-email")
async def verify_email(
    request: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db)
):
    """Verify a user's email address."""
    normalized_email = normalize_email(request.email)
    
    result = await db.execute(
        select(User).where(User.email == normalized_email)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    if user.email_verified:
        return {"message": "Email already verified"}
        
    if not user.verify_token_hash or not verify_password(request.token, user.verify_token_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token"
        )
        
    if datetime.utcnow() > user.verify_expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verification token expired"
        )
        
    # Success, mark as verified and clean up
    user.email_verified = True
    user.verify_token_hash = None
    user.verify_expires_at = None
    user.token_version += 1 # Invalidate any existing sessions just in case
    
    await db.commit()
    return {"message": "Email verified successfully"}


@app.post("/api/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    """Login and get access token."""
    normalized_email = normalize_email(request.email)
    
    result = await db.execute(
        select(User).where(User.email == normalized_email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
        
    if not user.email_verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email verification required. Please check your email inbox."
        )
    
    role_str = user.global_role if isinstance(user.global_role, str) else user.global_role.value
    access_token = create_access_token(user.id, role_str, token_version=user.token_version)
    
    return LoginResponse(access_token=access_token, role=role_str)


# ==========================================
# Class Management
# ==========================================

def generate_join_code(length: int = 8) -> str:
    """Generate a random alphanumeric join code."""
    alphabet = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

@app.post("/api/classes", response_model=ClassResponse, status_code=status.HTTP_201_CREATED)
async def create_class(
    request: ClassCreateRequest,
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db)
):
    """Create a new class (instructors only)."""
    # 1. Generate code and create Class
    join_code = generate_join_code()
    
    new_class = Class(
        name=request.name,
        code=request.name[:50], # Optional custom code vs name mapping if needed
        join_code_hash=hash_password(join_code),
        created_by_user_id=current_user.id
    )
    db.add(new_class)
    await db.flush() # flush to get the new_class.id
    
    # 2. Auto-enroll creator as instructor
    enrollment = Enrollment(
        class_id=new_class.id,
        user_id=current_user.id,
        class_role=ClassRole.instructor
    )
    db.add(enrollment)
    
    # 3. Audit log
    audit = AuditLog(
        actor_user_id=current_user.id,
        class_id=new_class.id,
        action="create_class"
    )
    db.add(audit)
    
    await db.commit()
    await db.refresh(new_class)
    
    # Return the raw join code ONLY upon creation
    return ClassResponse(
        id=new_class.id,
        name=new_class.name,
        code=join_code,
        created_at=new_class.created_at
    )

@app.post("/api/classes/{class_id}/rotate-code", response_model=RotateCodeResponse)
async def rotate_class_code(
    class_id: int,
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db)
):
    """Rotate the join code for a class (global instructors who created it)."""
    result = await db.execute(select(Class).where(Class.id == class_id))
    class_obj = result.scalar_one_or_none()
    
    if not class_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
        
    if class_obj.created_by_user_id != current_user.id:
        # Check if they are an instructor in the class via enrollment
        enroll_res = await db.execute(
            select(Enrollment).where(
                Enrollment.class_id == class_id, Enrollment.user_id == current_user.id
            )
        )
        enroll = enroll_res.scalar_one_or_none()
        if not enroll or enroll.class_role != ClassRole.instructor:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not an instructor for this class")

    new_code = generate_join_code()
    class_obj.join_code_hash = hash_password(new_code)
    class_obj.join_code_rotated_at = datetime.utcnow()
    
    audit = AuditLog(
        actor_user_id=current_user.id,
        class_id=class_obj.id,
        action="rotate_join_code"
    )
    db.add(audit)
    
    await db.commit()
    return RotateCodeResponse(join_code=new_code)

@app.post("/api/classes/join")
async def join_class(
    request: JoinClassRequest,
    current_user: User = Depends(require_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """Join a class using a code."""
    # To check the code securely (since we hashed it but didn't know which class id),
    # we either fetch ALL classes and check hashing (slow), OR we assume our generated 
    # codes are strong/cryptographic and we could just store it in plaintext in another field.
    # Since we used bcrypt, we fetch all classes. Wait, we should optimize if there are many.
    # For now, fetch all classes and check matches:
    
    result = await db.execute(select(Class))
    classes = result.scalars().all()
    
    matched_class = None
    for c in classes:
        if c.join_code_hash and verify_password(request.code, c.join_code_hash):
            matched_class = c
            break
            
    if not matched_class:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid join code")
        
    async with db.begin_nested():
        # Check if already enrolled
        enroll_res = await db.execute(
            select(Enrollment).where(
                Enrollment.class_id == matched_class.id,
                Enrollment.user_id == current_user.id
            )
        )
        if enroll_res.scalar_one_or_none():
            return {"message": "Already enrolled", "class_id": matched_class.id}
            
        # Check TA Allowlist
        role = ClassRole.student
        ta_res = await db.execute(
            select(TAAllowlist).where(
                TAAllowlist.class_id == matched_class.id,
                TAAllowlist.email == normalize_email(current_user.email)
            )
        )
        if ta_res.scalar_one_or_none():
            role = ClassRole.ta
            
        enrollment = Enrollment(
            class_id=matched_class.id,
            user_id=current_user.id,
            class_role=role
        )
        db.add(enrollment)
        
        audit = AuditLog(
            actor_user_id=current_user.id,
            class_id=matched_class.id,
            action=f"joined_class_as_{role.name if not isinstance(role, str) else role}"
        )
        db.add(audit)
        
    await db.commit()
    return {"message": "Successfully joined class", "class_id": matched_class.id, "role": role}


@app.get("/api/classes/{class_id}/roster", response_model=RosterResponse)
async def get_class_roster(
    class_id: int,
    current_user: User = Depends(require_verified_user), # Workaround for path param dependency
    db: AsyncSession = Depends(get_db)
):
    """Get the roster of a class (instructors only)."""
    # Workaround for dynamic path parameter dependency
    # We do the check manually here because Depends() resolves before the function body
    enroll_res = await db.execute(
        select(Enrollment).where(
            Enrollment.class_id == class_id, Enrollment.user_id == current_user.id
        )
    )
    enroll = enroll_res.scalar_one_or_none()
    user_g_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
    
    if user_g_role != "admin" and (not enroll or (isinstance(enroll.class_role, str) and enroll.class_role != "instructor") and (not isinstance(enroll.class_role, str) and enroll.class_role.value != "instructor")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must be an instructor of this class.")

    # Fetch users in the class
    result = await db.execute(
        select(User, Enrollment)
        .join(Enrollment, User.id == Enrollment.user_id)
        .where(Enrollment.class_id == class_id)
    )
    
    roster_list = []
    for user, enrollment in result.all():
        roster_list.append(
            RosterUserResponse(
                user_id=user.id,
                email=user.email,
                full_name=user.full_name,
                class_role=enrollment.class_role if isinstance(enrollment.class_role, str) else enrollment.class_role.value,
                joined_at=enrollment.joined_at
            )
        )
        
    return RosterResponse(class_id=class_id, roster=roster_list)

@app.post("/api/classes/{class_id}/set-role")
async def set_class_role(
    class_id: int,
    request: SetRoleRequest,
    current_user: User = Depends(require_verified_user), # Again, manual check below
    db: AsyncSession = Depends(get_db)
):
    """Set a user's role in a class (instructors only)."""
    # Dependency check workaround
    enroll_res = await db.execute(
        select(Enrollment).where(
            Enrollment.class_id == class_id, Enrollment.user_id == current_user.id
        )
    )
    enroll = enroll_res.scalar_one_or_none()
    user_g_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
    
    if user_g_role != "admin" and (not enroll or (isinstance(enroll.class_role, str) and enroll.class_role != "instructor") and (not isinstance(enroll.class_role, str) and enroll.class_role.value != "instructor")):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Must be an instructor of this class.")
        
    # Find the target user's enrollment
    target_res = await db.execute(
        select(Enrollment).where(
            Enrollment.class_id == class_id, Enrollment.user_id == request.user_id
        )
    )
    target_enrollment = target_res.scalar_one_or_none()
    
    if not target_enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not enrolled in this class.")
        
    old_role = target_enrollment.class_role if isinstance(target_enrollment.class_role, str) else target_enrollment.class_role.value
    target_enrollment.class_role = request.class_role
    
    audit = AuditLog(
        actor_user_id=current_user.id,
        target_user_id=request.user_id,
        class_id=class_id,
        action="set_class_role",
        old_value=old_role,
        new_value=request.class_role
    )
    db.add(audit)
    
    await db.commit()
    return {"message": "Role updated successfully"}


# ==========================================
# Account Management
# ==========================================

@app.post("/api/account/update-email")
async def update_email(
    request: UpdateEmailRequest,
    current_user: User = Depends(require_verified_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user email and force re-verification."""
    # Validate password
    if not verify_password(request.password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
        
    normalized_new_email = normalize_email(request.new_email)
    
    # Enforce @purdue.edu (could make this configurable later, hardcoding for now per plan)
    if not normalized_new_email.endswith("@purdue.edu"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email must end with @purdue.edu")
        
    # Ensure it's not already taken
    result = await db.execute(select(User).where(User.email == normalized_new_email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
        
    old_email = current_user.email
        
    # Re-fetch user in the current session to ensure changes are tracked
    result_user = await db.execute(select(User).where(User.id == current_user.id))
    db_user = result_user.scalar_one()

    # Apply changes
    db_user.email = normalized_new_email
    db_user.email_verified = False
    
    token = generate_verification_token()
    db_user.verify_token_hash = hash_password(token)
    db_user.verify_expires_at = datetime.utcnow() + timedelta(minutes=15)
    db_user.token_version += 1 # Invalidate current session
    
    # Audit log
    audit = AuditLog(
        actor_user_id=db_user.id,
        target_user_id=db_user.id,
        action="update_email",
        old_value=old_email,
        new_value=normalized_new_email
    )
    db.add(audit)
    
    await db.commit()
    
    await send_verification_email(normalized_new_email, token)
    
    return {"message": "Email updated successfully. Please verify your new email address to log in."}


@app.get("/api/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information."""
    role_str = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
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
    user_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
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
    
    user_role = current_user.global_role if isinstance(current_user.global_role, str) else current_user.global_role.value
    
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


# --- Document Proxy Endpoints ---
# These forward requests to the AI Service which holds the actual files

from fastapi.responses import StreamingResponse
from config import AI_SERVICE_URL
import httpx

@app.get("/kbs/{name}/docs/{file_uuid}")
async def proxy_get_kb_document(name: str, file_uuid: str):
    """Proxy for raw document retrieval."""
    target_url = f"{AI_SERVICE_URL}/kbs/{name}/docs/{file_uuid}"
    try:
        client = httpx.AsyncClient()
        req = client.build_request("GET", target_url)
        r = await client.send(req, stream=True)
        return StreamingResponse(
            r.aiter_raw(),
            status_code=r.status_code,
            headers=r.headers,
            background=None
        )
    except Exception as e:
        logger.error(f"Proxy error for document: {e}")
        raise HTTPException(status_code=500, detail="Document service unavailable")

@app.get("/kbs/{name}/docs/{file_uuid}/view")
async def proxy_view_kb_document(name: str, file_uuid: str):
    """Proxy for document viewer."""
    target_url = f"{AI_SERVICE_URL}/kbs/{name}/docs/{file_uuid}/view"
    try:
        client = httpx.AsyncClient()
        req = client.build_request("GET", target_url)
        r = await client.send(req, stream=True)
        return StreamingResponse(
            r.aiter_raw(),
            status_code=r.status_code,
            headers=r.headers,
            background=None
        )
    except Exception as e:
        logger.error(f"Proxy error for view: {e}")
        raise HTTPException(status_code=500, detail="Document service unavailable")

@app.get("/kbs/{name}/docs/{file_uuid}/download")
async def proxy_download_kb_document(name: str, file_uuid: str):
    """Proxy for document download."""
    target_url = f"{AI_SERVICE_URL}/kbs/{name}/docs/{file_uuid}/download"
    try:
        client = httpx.AsyncClient()
        req = client.build_request("GET", target_url)
        r = await client.send(req, stream=True)
        return StreamingResponse(
            r.aiter_raw(),
            status_code=r.status_code,
            headers=r.headers,
            background=None
        )
    except Exception as e:
        logger.error(f"Proxy error for download: {e}")
        raise HTTPException(status_code=500, detail="Document service unavailable")

@app.get("/kbs/{name}/docs/{file_uuid}/inline")
async def proxy_inline_kb_document(name: str, file_uuid: str):
    """Proxy for inline document viewing."""
    target_url = f"{AI_SERVICE_URL}/kbs/{name}/docs/{file_uuid}/inline"
    try:
        client = httpx.AsyncClient()
        req = client.build_request("GET", target_url)
        r = await client.send(req, stream=True)
        return StreamingResponse(
            r.aiter_raw(),
            status_code=r.status_code,
            headers=r.headers,
            background=None
        )
    except Exception as e:
        logger.error(f"Proxy error for inline view: {e}")
        raise HTTPException(status_code=500, detail="Document service unavailable")

