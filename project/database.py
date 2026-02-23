from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime
from typing import List
import enum
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)


class GlobalRole(enum.Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"

class ClassRole(enum.Enum):
    student = "student"
    ta = "ta"
    instructor = "instructor"

def normalize_email(email: str) -> str:
    """Normalize email address by stripping whitespace and converting to lowercase."""
    if not email:
        return email
    return email.strip().lower()


class QuestionStatus(enum.Enum):
    pending = "pending"
    answered = "answered"


class MessageRole(enum.Enum):
    student = "student"
    instructor = "instructor"


# # Database URL - using SQLite for simplicity
# DATABASE_URL = "sqlite+aiosqlite:///./qa_system.db"

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    global_role: Mapped[GlobalRole] = mapped_column(SQLEnum(GlobalRole), default=GlobalRole.student)
    email_verified: Mapped[bool] = mapped_column(default=False)
    verify_token_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    verify_expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    token_version: Mapped[int] = mapped_column(default=1)
    is_instructor_pending: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="user")
    classes_created: Mapped[List["Class"]] = relationship("Class", back_populates="creator")
    enrollments: Mapped[List["Enrollment"]] = relationship("Enrollment", back_populates="user")


class Class(Base):
    __tablename__ = "classes"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    code: Mapped[str] = mapped_column(String(50), nullable=True)
    join_code_hash: Mapped[str] = mapped_column(String(255), nullable=True)
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    join_code_rotated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    creator: Mapped["User"] = relationship("User", back_populates="classes_created")
    enrollments: Mapped[List["Enrollment"]] = relationship("Enrollment", back_populates="class_")
    ta_allowlist: Mapped[List["TAAllowlist"]] = relationship("TAAllowlist", back_populates="class_")


class Enrollment(Base):
    __tablename__ = "enrollments"
    
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    class_role: Mapped[ClassRole] = mapped_column(SQLEnum(ClassRole), default=ClassRole.student)
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    class_: Mapped["Class"] = relationship("Class", back_populates="enrollments")
    user: Mapped["User"] = relationship("User", back_populates="enrollments")


from sqlalchemy import UniqueConstraint

class TAAllowlist(Base):
    __tablename__ = "ta_allowlist"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"))
    email: Mapped[str] = mapped_column(String(255))
    
    class_: Mapped["Class"] = relationship("Class", back_populates="ta_allowlist")
    
    __table_args__ = (
        UniqueConstraint('class_id', 'email', name='uq_ta_allowlist_class_email'),
    )


class AuditLog(Base):
    __tablename__ = "audit_log"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    actor_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    target_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=True)
    action: Mapped[str] = mapped_column(String(255))
    old_value: Mapped[str] = mapped_column(Text, nullable=True)
    new_value: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Question(Base):
    __tablename__ = "questions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(Text)
    status: Mapped[QuestionStatus] = mapped_column(SQLEnum(QuestionStatus), default=QuestionStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship("User", back_populates="questions")
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="question", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return (
            f"Question(id={self.id!r}, "
            f"status={self.status!r}, "
            f"messages={self.messages!r})"
        )

class Message(Base):
    __tablename__ = "messages"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"))
    content: Mapped[str] = mapped_column(Text)
    role: Mapped[MessageRole] = mapped_column(SQLEnum(MessageRole))
    source: Mapped[str] = mapped_column(String(50), nullable=True)  # 'manual', 'ai', 'cached'
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    question: Mapped["Question"] = relationship("Question", back_populates="messages")

    def __repr__(self) -> str:
        # Truncate content so it stays on one line
        short_content = (self.content[:30] + '..') if len(self.content) > 30 else self.content
        return f"<Message(id={self.id}, content='{short_content}')>"


async def get_db():
    """Dependency for getting async database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    """Close the database engine pool."""
    if engine:
        await engine.dispose()
        logger.warning("Database connection pool closed.")


async def seed_data():
    """Seed initial data if needed."""
    from auth import hash_password
    
    async with async_session_maker() as session:
        # Check if we already have users
        from sqlalchemy import select
        result = await session.execute(select(User))
        existing_users = result.scalars().all()
        
        if not existing_users:
            # Create sample users
            student = User(
                email="student@purdue.edu",
                password_hash=hash_password("password"),
                global_role=GlobalRole.student,
                email_verified=True
            )
            instructor = User(
                email="instructor@purdue.edu",
                password_hash=hash_password("password"),
                global_role=GlobalRole.instructor,
                email_verified=True
            )
            
            session.add(student)
            session.add(instructor)
            await session.commit()
            
            print("Sample users created:")
            print("  Student: student@purdue.edu / password")
            print("  Instructor: instructor@purdue.edu / password")


# For backward compatibility, keep Answer as alias to Message
Answer = Message
