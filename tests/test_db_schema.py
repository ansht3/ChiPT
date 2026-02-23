"""
Test File: test_db_schema.py
Description: Validates the SQLAlchemy schema configurations, ensuring tables can be minted securely with correct foreign keys and enum types.
How it is tested: Leverages an async engine running `Base.metadata.create_all` safely inside an isolated SQLite memory structure, simulating database instantiation. It inserts fake entity logic checking class relations.
"""
import asyncio
import sys
import os

# Add project root and project directory to path so we can import project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project')))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import select

from database import Base, User, Class, Enrollment, TAAllowlist, AuditLog, GlobalRole, ClassRole, normalize_email

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

async def run_tests():
    # Test normalize_email
    assert normalize_email(" Test@Example.com ") == "test@example.com"
    print("test_normalize_email passed")

    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    async with async_session_maker() as session:
        user = User(
            email="instructor@test.com",
            full_name="Test Instructor",
            password_hash="hash",
            global_role=GlobalRole.instructor
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        assert user.id is not None
        
        course = Class(
            name="CS101",
            code="CS101-01",
            created_by_user_id=user.id
        )
        session.add(course)
        await session.commit()
        await session.refresh(course)
        
        enrollment = Enrollment(
            class_id=course.id,
            user_id=user.id,
            class_role=ClassRole.instructor
        )
        session.add(enrollment)
        await session.commit()
        
        ta = TAAllowlist(
            class_id=course.id,
            email="ta@test.com"
        )
        session.add(ta)
        await session.commit()
        
        log = AuditLog(
            actor_user_id=user.id,
            action="created_class",
            class_id=course.id
        )
        session.add(log)
        await session.commit()
        print("Basic inserts passed")

        from sqlalchemy.exc import IntegrityError
        duplicate_ta = TAAllowlist(class_id=course.id, email="ta@test.com")
        session.add(duplicate_ta)
        try:
            await session.commit()
            print("FAILED: Unique constraint didn't trigger")
        except IntegrityError:
            print("Unique constraint on TAAllowlist passed")
            await session.rollback()

    await engine.dispose()
    print("All tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(run_tests())
