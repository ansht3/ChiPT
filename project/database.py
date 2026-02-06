from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime
from typing import List
import enum
import logging
from config import DATABASE_URL

logger = logging.getLogger(__name__)


class UserRole(enum.Enum):
    student = "student"
    instructor = "instructor"


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
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.student)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    questions: Mapped[List["Question"]] = relationship("Question", back_populates="user")


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
                role=UserRole.student
            )
            instructor = User(
                email="instructor@purdue.edu",
                password_hash=hash_password("password"),
                role=UserRole.instructor
            )
            
            session.add(student)
            session.add(instructor)
            await session.commit()
            
            print("Sample users created:")
            print("  Student: student@purdue.edu / password")
            print("  Instructor: instructor@purdue.edu / password")


# For backward compatibility, keep Answer as alias to Message
Answer = Message
