#!/usr/bin/env python3
"""
Approve an instructor request.
This script sets a user's role to 'instructor', clears their pending status,
and bumps their token version to invalidate existing sessions.
"""
import argparse
import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import select

from database import User, GlobalRole, AuditLog, normalize_email
from config import DATABASE_URL

async def approve_instructor(email: str):
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
            
        if user.global_role == GlobalRole.instructor:
            print(f"User {normalized_email} is already an instructor.")
            await engine.dispose()
            sys.exit(0)
            
        if not user.is_instructor_pending:
            print(f"Warning: User {normalized_email} did not request instructor status.")
        
        user.global_role = GlobalRole.instructor
        user.is_instructor_pending = False
        user.token_version += 1
        
        # Add an audit log for the approval action
        # Note: We don't have a systemic "admin" user ID yet unless we hardcode 1, 
        # so we will use the user's own ID as the actor for this CLI script for now.
        audit_log = AuditLog(
            actor_user_id=user.id,
            target_user_id=user.id,
            action="instructor_approval",
            old_value="student",
            new_value="instructor"
        )
        db.add(audit_log)
        
        await db.commit()
        
        print(f"Success: User {normalized_email} has been approved as an instructor.")
        print("Their previous sessions have been invalidated and they will need to log in again.")
        
    await engine.dispose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Approve a pending instructor request.")
    parser.add_argument("--email", required=True, help="The email address of the user to approve.")
    
    args = parser.parse_args()
    
    asyncio.run(approve_instructor(args.email))
