from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# User Schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    intent: Optional[str] = None  # E.g., 'instructor'


class RegisterResponse(BaseModel):
    user_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    role: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: str

class VerifyEmailRequest(BaseModel):
    email: EmailStr
    token: str

class UpdateEmailRequest(BaseModel):
    new_email: EmailStr
    password: str

# Class Schemas
class ClassCreateRequest(BaseModel):
    name: str

class ClassResponse(BaseModel):
    id: int
    name: str
    code: Optional[str] = None
    created_at: datetime
    
class RotateCodeResponse(BaseModel):
    join_code: str

class JoinClassRequest(BaseModel):
    code: str

class RosterUserResponse(BaseModel):
    user_id: int
    email: str
    full_name: Optional[str] = None
    class_role: str
    joined_at: datetime

class RosterResponse(BaseModel):
    class_id: int
    roster: List[RosterUserResponse]

class SetRoleRequest(BaseModel):
    user_id: int
    class_role: str


# Question Schemas
class QuestionCreate(BaseModel):
    content: str


class QuestionCreateResponse(BaseModel):
    question_id: int


# Message Schemas
class MessageResponse(BaseModel):
    id: int
    content: str
    role: str  # 'student' or 'instructor'
    source: Optional[str] = None
    created_at: datetime


class MessageCreate(BaseModel):
    content: str
    source: Optional[str] = "manual"


class MessageCreateResponse(BaseModel):
    message_id: int

class KBCreateRequest(BaseModel):
    name: str

class KBFileDeleteRequest(BaseModel):
    filename: str


# Question with Messages
class QuestionResponse(BaseModel):
    id: int
    content: str
    status: str
    created_at: datetime
    messages: List[MessageResponse] = []


class InstructorQuestionResponse(BaseModel):
    id: int
    user_email: str
    content: str
    status: str
    created_at: datetime
    messages: List[MessageResponse] = []


# AI Suggestion
class SuggestAnswerResponse(BaseModel):
    suggested_answer: str
    source: str


# Legacy schemas for backward compatibility
class AnswerResponse(MessageResponse):
    pass


class AnswerCreate(MessageCreate):
    pass


class AnswerCreateResponse(MessageCreateResponse):
    pass
