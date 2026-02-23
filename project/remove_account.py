#!/usr/bin/env python3
"""
Remove a user account by email.
This script completely deletes a user from the database.
"""
import argparse
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select, delete

from project.database import User, normalize_email
from config import DATABASE_URL

async def remove_user(email: str):
    engine = create_async_engine(DATABASE_URL, echo=False)
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    normalized_email = normalize_email(email)
    
    async with SessionLocal() as db:
        result = await db.execute(select(User).where(User.email == normalized_email))
        user = result.scalar_one_or_none()
        
        if not user:
            print(f"Error: User with email {normalized_email} not found.")
            await engine.dispose()
            sys.exit(1)
            
        await db.execute(delete(User).where(User.email == normalized_email))
        await db.commit()
        
        print(f"Success: User {normalized_email} has been completely removed.")
        
    await engine.dispose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove a user account.")
    parser.add_argument("--email", required=True, help="The email address of the user to remove.")
    
    args = parser.parse_args()
    
    asyncio.run(remove_user(args.email))
