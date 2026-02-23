#!/usr/bin/env python3
"""
Cache Service Debugging Script

Tests the cache service and helps diagnose issues.
"""
import httpx
import asyncio
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../project')))

from config import CACHE_SERVICE_URL

# CACHE_URL = "http://localhost:8902"

async def check_health():
    """Check if cache service is running."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CACHE_SERVICE_URL}/health")
            data = response.json()
            print("✓ Cache service is running")
            print(f"  Status: {data.get('status')}")
            print(f"  Milvus connected: {data.get('milvus_connected')}")
            return True
    except Exception as e:
        print(f"✗ Cannot connect to cache service: {e}")
        return False

async def check_stats():
    """Check cache statistics."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{CACHE_SERVICE_URL}/stats")
            data = response.json()
            
            if "error" in data:
                print(f"✗ Error getting stats: {data['error']}")
                return False
            
            total = data.get("total_qa_pairs", 0)
            print(f"\nCache Statistics:")
            print(f"  Total Q&A pairs: {total}")
            print(f"  Collection: {data.get('collection_name')}")
            print(f"  Similarity threshold: {data.get('similarity_threshold')}")
            
            if total == 0:
                print("\n⚠ WARNING: Collection is empty!")
                print("  Run the reseed command to add sample data.")
            
            return total > 0
    except Exception as e:
        print(f"✗ Error checking stats: {e}")
        return False

async def reseed():
    """Reseed the collection with sample data."""
    try:
        print("\nReseeding collection...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{CACHE_SERVICE_URL}/reseed")
            data = response.json()
            
            if response.status_code == 200:
                print(f"✓ {data.get('message')}")
                return True
            else:
                print(f"✗ Reseed failed: {data}")
                return False
    except Exception as e:
        print(f"✗ Error reseeding: {e}")
        return False

async def test_search(query: str):
    """Test searching the cache."""
    try:
        print(f"\nSearching for: '{query}'")
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{CACHE_SERVICE_URL}/search",
                json={"query": query}
            )
            data = response.json()
            
            if data.get("found"):
                print("✓ Cache HIT!")
                print(f"  Answer: {data.get('answer')[:100]}...")
            else:
                print("✗ Cache MISS")
                print("  No similar question found in cache")
            
            return data.get("found", False)
    except Exception as e:
        print(f"✗ Search error: {e}")
        return False

async def add_test_qa():
    """Add a test Q&A pair."""
    try:
        print("\nAdding test Q&A pair...")
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{CACHE_SERVICE_URL}/add",
                params={
                    "question": "What is the capital of France?",
                    "answer": "The capital of France is Paris."
                }
            )
            data = response.json()
            
            if response.status_code == 200:
                print(f"✓ {data.get('message')}")
                return True
            else:
                print(f"✗ Failed to add: {data}")
                return False
    except Exception as e:
        print(f"✗ Error adding Q&A: {e}")
        return False

async def main():
    print("=" * 60)
    print("Cache Service Debug Tool")
    print("=" * 60)
    
    # Check health
    if not await check_health():
        print("\nCache service is not running.")
        print("Start it with: cd cache_service && python main.py")
        return 1
    
    # Check stats
    has_data = await check_stats()
    
    # If no data, ask to reseed
    if not has_data:
        response = input("\nCollection is empty. Reseed with sample data? (y/n): ")
        if response.lower() == 'y':
            if await reseed():
                await check_stats()
    
    # Test searches
    print("\n" + "=" * 60)
    print("Testing Cache Searches")
    print("=" * 60)
    
    test_queries = [
        "What is machine learning?",
        "How does backpropagation work?",
        "What is overfitting?",
        "Tell me about neural networks",
    ]
    
    for query in test_queries:
        await test_search(query)
        await asyncio.sleep(1)  # Small delay between requests
    
    # Offer to add custom Q&A
    print("\n" + "=" * 60)
    response = input("\nWould you like to add a custom Q&A pair? (y/n): ")
    if response.lower() == 'y':
        question = input("Question: ")
        answer = input("Answer: ")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{CACHE_SERVICE_URL}/add",
                params={"question": question, "answer": answer}
            )
            print(f"\n{response.json()}")
        
        # Test searching for it
        await asyncio.sleep(2)
        await test_search(question)
    
    print("\n" + "=" * 60)
    print("Debug session complete")
    print("=" * 60)

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code or 0)
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        exit(1)
