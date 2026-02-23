
import httpx
import asyncio
import json

CACHE_API_URL = "http://localhost:8902/search"

async def test_cache_search():
    question = "What is a logistic regression?"
    print(f"Querying cache for: '{question}'")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                CACHE_API_URL,
                json={
                    "query": question,
                    "context": []  # Context not strictly needed for raw search trigger
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                print("\nResponse Status: 200 OK")
                print("Response Body:")
                print(json.dumps(data, indent=2))
                
                if not data.get("found"):
                    print("\n[RESULT] Cache MISS (Item not found or below threshold)")
                else:
                    print("\n[RESULT] Cache HIT")
            else:
                print(f"\nResponse Status: {response.status_code}")
                print(response.text)
                
    except httpx.ConnectError:
        print(f"\n[ERROR] Failed to connect to {CACHE_API_URL}. Is the cache service running?")
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(test_cache_search())
