#!/usr/bin/env python3
"""
Test script to verify all Q&A system services are working
"""
import httpx
import asyncio
import sys
from typing import Tuple
from config import MAIN_QA_URL, AI_SERVICE_URL, CACHE_SERVICE_URL

# # Service endpoints
# MAIN_QA_URL = "http://localhost:8000"
# AI_SERVICE_URL = "http://localhost:8901"
# CACHE_SERVICE_URL = "http://localhost:8902"

TIMEOUT = 10.0


async def test_main_qa() -> Tuple[bool, str]:
    """Test main Q&A system"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{MAIN_QA_URL}/")
            if response.status_code == 200:
                return True, "Main Q&A system is running"
            return False, f"Main Q&A returned status {response.status_code}"
    except httpx.ConnectError:
        return False, "Cannot connect to main Q&A system"
    except Exception as e:
        return False, f"Error: {str(e)}"


async def test_ai_service() -> Tuple[bool, str]:
    """Test AI service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Test health endpoint
            response = await client.get(f"{AI_SERVICE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    return True, "AI service is healthy"
                return False, f"AI service status: {data.get('status')}"
            return False, f"AI service returned status {response.status_code}"
    except httpx.ConnectError:
        return False, "Cannot connect to AI service"
    except Exception as e:
        return False, f"Error: {str(e)}"


async def test_cache_service() -> Tuple[bool, str]:
    """Test cache service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            # Test health endpoint
            response = await client.get(f"{CACHE_SERVICE_URL}/health")
            if response.status_code == 200:
                data = response.json()
                status = data.get("status")
                milvus = data.get("milvus_connected", False)
                
                if status == "healthy" and milvus:
                    return True, "Cache service is healthy (Milvus connected)"
                elif status == "healthy":
                    return False, "Cache service running but Milvus not connected"
                return False, f"Cache service status: {status}"
            return False, f"Cache service returned status {response.status_code}"
    except httpx.ConnectError:
        return False, "Cannot connect to cache service"
    except Exception as e:
        return False, f"Error: {str(e)}"


async def test_cache_stats() -> Tuple[bool, str]:
    """Test cache service statistics"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f"{CACHE_SERVICE_URL}/stats")
            if response.status_code == 200:
                data = response.json()
                total = data.get("total_qa_pairs", 0)
                return True, f"Cache has {total} Q&A pairs"
            return False, "Cannot get cache stats"
    except Exception as e:
        return False, f"Error: {str(e)}"


async def test_cache_search() -> Tuple[bool, str]:
    """Test cache service search functionality"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Search for a question from sample data
            response = await client.post(
                f"{CACHE_SERVICE_URL}/search",
                json={"query": "What is machine learning?"}
            )
            if response.status_code == 200:
                data = response.json()
                if data.get("found"):
                    return True, "Cache search working (found sample answer)"
                return True, "Cache search working (no match found, which is ok)"
            return False, f"Cache search returned status {response.status_code}"
    except httpx.TimeoutException:
        return False, "Cache search timed out (may need OpenAI API)"
    except Exception as e:
        return False, f"Error: {str(e)}"


async def test_ai_generate() -> Tuple[bool, str]:
    """Test AI service generation"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{AI_SERVICE_URL}/generate",
                json={
                    "question": "What is 2+2?",
                    "context": []
                }
            )
            if response.status_code == 200:
                data = response.json()
                if "answer" in data and data["answer"]:
                    return True, "AI generation working"
                return False, "AI returned empty answer"
            return False, f"AI service returned status {response.status_code}"
    except httpx.TimeoutException:
        return False, "AI generation timed out (check OpenAI API)"
    except Exception as e:
        return False, f"Error: {str(e)}"


def print_result(service: str, success: bool, message: str):
    """Print test result with formatting"""
    status = "✓" if success else "✗"
    color = "\033[92m" if success else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{status}{reset} {service:<25} {message}")


async def main():
    """Run all tests"""
    print("=" * 70)
    print("Q&A System - Service Health Check")
    print("=" * 70)
    print()
    
    all_passed = True
    
    # Core services
    print("Core Services:")
    success, message = await test_main_qa()
    print_result("Main Q&A System", success, message)
    all_passed &= success
    
    success, message = await test_ai_service()
    print_result("AI Service", success, message)
    all_passed &= success
    
    success, message = await test_cache_service()
    print_result("Cache Service", success, message)
    all_passed &= success
    
    print()
    
    # Additional tests
    print("Functionality Tests:")
    
    success, message = await test_cache_stats()
    print_result("Cache Stats", success, message)
    
    success, message = await test_cache_search()
    print_result("Cache Search", success, message)
    
    success, message = await test_ai_generate()
    print_result("AI Generation", success, message)
    
    print()
    print("=" * 70)
    
    if all_passed:
        print("✓ All core services are running!")
        print()
        print("Next steps:")
        print("  1. Open http://localhost:8000")
        print("  2. Login with student@test.com / password123")
        print("  3. Ask a question")
        print("  4. Login as instructor@test.com / password123")
        print("  5. Get AI suggestion and answer the question")
        return 0
    else:
        print("✗ Some services are not running properly")
        print()
        print("Troubleshooting:")
        print("  - Check if all services are started")
        print("  - Verify Milvus is running: docker-compose ps")
        print("  - Check logs in each service terminal")
        return 1


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(1)
