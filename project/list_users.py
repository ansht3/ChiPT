import asyncio
import os
import sys

# Add current directory to path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from database import init_db, get_db, User
from sqlalchemy import select
from contextlib import asynccontextmanager

async def list_all_users():
    # Because get_db is a generator, we need to handle it properly
    # Actually, we can just create an AsyncSession manually
    from database import async_session_maker
    
    print(f"{'ID':<5} | {'Email':<30} | {'Global Role':<15} | {'Pending Instructor':<20}")
    print("-" * 80)
    
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        for u in users:
            role_str = u.global_role if isinstance(u.global_role, str) else u.global_role.value
            print(f"{u.id:<5} | {u.email:<30} | {role_str:<15} | {str(u.is_instructor_pending):<20}")

if __name__ == "__main__":
    asyncio.run(list_all_users())
