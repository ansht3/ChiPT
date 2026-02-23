"""
Test File: test_startup.py
Description: Tests the underlying database startup functions (init_db and seed_data) over the active database configuration.
How it is tested: Simply imports and successfully executes the application startup lifespan operations gracefully to verify tables synchronize.
"""
import asyncio
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from project.database import init_db, seed_data

async def run():
    print("Initializing database...")
    await init_db()
    
    print("Seeding database (if not already seeded)...")
    await seed_data()
    print("Done!")

if __name__ == "__main__":
    asyncio.run(run())
