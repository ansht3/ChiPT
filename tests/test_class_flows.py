"""
Test File: test_class_flows.py
Description: This script tests the end-to-end integration flows for Class Creation, Joining via codes, and Roster Roles.
How it is tested: It uses an in-memory SQLite database (`sqlite+aiosqlite:///:memory:`) and overrides the FastAPI `get_db` dependency to interact with the application securely and in isolation from the actual production database.
"""
import asyncio
import os
import sys
from httpx import AsyncClient
from datetime import datetime, timedelta

# Add project root and project directory to path so we can import project files
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project')))

from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from database import Base, User, GlobalRole, normalize_email, ClassRole, TAAllowlist
from config import DATABASE_URL
from auth import hash_password, verify_password
from main import app
import database

# Use a physical SQLite file to avoid StaticPool single-connection concurrency clashes
DB_FILE = "test_class_flows.db"
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{DB_FILE}"

async def test_class_flows():
    # Remove file if it exists prior to test
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)

    # 1. Create the DB and tables
    engine = create_async_engine(
        TEST_DATABASE_URL, 
        echo=False
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)

    # 2. Override the get_db dependency in the FastAPI app and patch the module
    database.SessionLocal = SessionLocal

    async def override_get_db():
        async with SessionLocal() as session:
            yield session
            
    app.dependency_overrides[database.get_db] = override_get_db
    database.get_db = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        instructor_email = "prof@purdue.edu"
        student1_email = "student1@purdue.edu"
        student2_email = "ta@purdue.edu" # Will be TA
        password = "password123"
        
        # --- PREPARATION: Register and verify users ---
        print("\n--- PREP: Creating & Verifying Users ---")
        for email in [instructor_email, student1_email, student2_email]:
            await client.post("/api/register", json={"email": email, "password": password, "intent": "instructor" if email == instructor_email else None})
            
            async with SessionLocal() as db:
                from sqlalchemy import select
                result = await db.execute(select(User).where(User.email == email))
                user = result.scalar_one()
                user.email_verified = True
                user.verify_token_hash = None
                
                if email == instructor_email:
                    user.global_role = GlobalRole.instructor
                    user.is_instructor_pending = False
                await db.commit()
                
        # Login and get tokens
        tokens = {}
        for email in [instructor_email, student1_email, student2_email]:
            res = await client.post("/api/login", json={"email": email, "password": password})
            tokens[email] = res.json()["access_token"]
            
        print("Users registered, verified, and logged in.")
        
        # --- 1. Class Creation ---
        print("\n--- 1. Testing Class Creation ---")
        headers_inst = {"Authorization": f"Bearer {tokens[instructor_email]}"}
        create_res = await client.post("/api/classes", json={"name": "CS101"}, headers=headers_inst)
        if create_res.status_code != 201:
            print(f"FAILED TO CREATE CLASS: {create_res.status_code} - {create_res.text}")
        assert create_res.status_code == 201
        class_data = create_res.json()
        class_id = class_data["id"]
        join_code_1 = class_data["code"]
        assert class_data["name"] == "CS101"
        assert join_code_1 is not None
        print(f"Class created with ID {class_id} and code {join_code_1}")

        # Add TA to allowlist directly in DB now that Class exists
        async with SessionLocal() as db:
            ta = TAAllowlist(class_id=class_id, email=student2_email)
            db.add(ta)
            await db.commit()

        # --- 2. Rotate Code ---
        print("\n--- 2. Testing Code Rotation ---")
        rotate_res = await client.post(f"/api/classes/{class_id}/rotate-code", headers=headers_inst)
        assert rotate_res.status_code == 200
        join_code_2 = rotate_res.json()["join_code"]
        assert join_code_2 != join_code_1
        print(f"Code rotated successfully to {join_code_2}")

        # --- 3. Join Class as Student ---
        print("\n--- 3. Testing Join Class (Student) ---")
        headers_s1 = {"Authorization": f"Bearer {tokens[student1_email]}"}
        join_res_bad = await client.post("/api/classes/join", json={"code": join_code_1}, headers=headers_s1)
        assert join_res_bad.status_code == 400 # Old code should fail

        join_res_s1 = await client.post("/api/classes/join", json={"code": join_code_2}, headers=headers_s1)
        assert join_res_s1.status_code == 200
        assert join_res_s1.json()["role"] == "student"
        print("Student 1 joined successfully.")

        # --- 4. Join Class as TA (Allowlist) ---
        print("\n--- 4. Testing Join Class (TA Auto-promote) ---")
        headers_s2 = {"Authorization": f"Bearer {tokens[student2_email]}"}
        join_res_s2 = await client.post("/api/classes/join", json={"code": join_code_2}, headers=headers_s2)
        assert join_res_s2.status_code == 200
        assert join_res_s2.json()["role"] == "ta"
        print("Student 2 joined and was auto-promoted to TA.")

        # --- 5. Roster Check ---
        print("\n--- 5. Testing Roster Fetch ---")
        roster_res = await client.get(f"/api/classes/{class_id}/roster", headers=headers_inst)
        assert roster_res.status_code == 200
        roster = roster_res.json()["roster"]
        assert len(roster) == 3 # Inst, S1, S2
        print(f"Roster contains {len(roster)} users.")

        # --- 6. Set Role ---
        print("\n--- 6. Testing Role Update ---")
        # Find Student 1 ID from roster
        s1_id = next(r["user_id"] for r in roster if r["email"] == student1_email)
        update_res = await client.post(f"/api/classes/{class_id}/set-role", json={"user_id": s1_id, "class_role": "ta"}, headers=headers_inst)
        assert update_res.status_code == 200
        
        # Verify
        roster_res2 = await client.get(f"/api/classes/{class_id}/roster", headers=headers_inst)
        s1_role = next(r["class_role"] for r in roster_res2.json()["roster"] if r["email"] == student1_email)
        assert s1_role == "ta"
        print("Student 1 manually promoted to TA.")

        # --- 7. Email Update & Token Invalidation ---
        print("\n--- 7. Testing Email Update & Verification Wipe ---")
        update_email_res = await client.post("/api/account/update-email", json={"new_email": "newprof@purdue.edu", "password": password}, headers=headers_inst)
        assert update_email_res.status_code == 200
        
        # Old token should now fail
        roster_res3 = await client.get(f"/api/classes/{class_id}/roster", headers=headers_inst)
        assert roster_res3.status_code == 401
        print("Email updated and previous token successfully invalidated.")

    # Cleanup constraints
    app.dependency_overrides.clear()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
    
    # Delete test db file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    print("\nAll class/roster tests completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_class_flows())
