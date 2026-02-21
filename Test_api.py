import argparse
import numpy as np
import requests
from openai import OpenAI
import sys
import time

# Client Configuration
CLIENT = OpenAI(
    base_url="http://localhost:8002/v1",
    api_key="aiforge-DZzMR1N2hChWEWTXeVTWr61ms_Em_hcUbznl3l3GaSM"
)

# Ollama Configuration for validation
OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL = "nomic-embed-text:latest"

# Test Configuration
# Using the same test prompt as before, separated into System and User for Chat API
SYSTEM_PROMPT = "You are a Minecraft expert."
MODEL_NAME = "llama3.3:70b-instruct-q8_0" #"gpt-oss:120b"

USER_PROMPTS = [
    "Briefly explain how to craft a crafting table. Limit your answer to one sentence.",
    "What is the purpose of a crafting table?",
    "How do I make a wooden sword?",
    "What are the different types of wood in Minecraft?",
    "How do I make a furnace?",
    "What is the difference between a furnace and a blast furnace?",
    "How do I make a crafting table?",
    "What is the purpose of a crafting table?",
    "How do I make a wooden sword?",
    "What are the different types of wood in Minecraft?",
    "How do I make a furnace?",
    "What is the difference between a furnace and a blast furnace?",
]

def cosine_similarity(v1, v2):
    """Calculates cosine similarity between two vectors."""
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    return dot_product / (norm_v1 * norm_v2)

def test_generation(prompts):
    """Tests the generation API."""
    print("\n" + "="*50)
    print(f"Testing GENERATION connection to Proxy...")
    print(f"Target URL: {CLIENT.base_url}")
    print(f"Model: {MODEL_NAME}")
    print("="*50 + "\n")

    for prompt in prompts:
        print(f"\nUser Prompt: {prompt}")
        try:
            start_time = time.time()

            response = CLIENT.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=32768
            )

            duration = time.time() - start_time

            print(f"Success! (Took {duration:.2f}s)")
            print(f"Model Used: {response.model}")
            print(f"Response: {response.choices[0].message.content}")

        except Exception as e:
            print(f"Failed: {e}")

def get_ollama_embedding(text):
    """Gets embedding directly from Ollama for validation."""
    try:
        response = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": EMBEDDING_MODEL,
                "prompt": text
            }
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except Exception as e:
        print(f"Error fetching Ollama embedding: {e}")
        return None

def test_embedding(prompts):
    """Tests the embedding API and compares with direct Ollama call."""
    print("\n" + "="*50)
    print(f"Testing EMBEDDING connection to Proxy...")
    print(f"Target URL: {CLIENT.base_url}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Comparison URL: {OLLAMA_EMBED_URL}")
    print("="*50 + "\n")

    for prompt in prompts:
        print(f"Prompt: {prompt[:50]}...")
        
        # 1. Get Embedding from Proxy (OpenAI Client)
        try:
            start_time = time.time()
            proxy_response = CLIENT.embeddings.create(
                model=EMBEDDING_MODEL,
                input=prompt
            )
            proxy_embedding = proxy_response.data[0].embedding
            proxy_duration = time.time() - start_time
            print(f"  Proxy API Success (Took {proxy_duration:.2f}s)")
        except Exception as e:
            print(f"  Proxy API Failed: {e}")
            continue

        # 2. Get Embedding from Ollama (Direct)
        ollama_embedding = get_ollama_embedding(prompt)
        if ollama_embedding:
            print(f"  Ollama Direct Success")
            
            # 3. Compare
            similarity = cosine_similarity(proxy_embedding, ollama_embedding)
            print(f"  Cosine Similarity: {similarity:.4f}")
            
            if similarity > 0.99:
                print("  [PASS] Embeddings match.")
            else:
                print("  [FAIL] Embeddings significantly different.")
        else:
             print("  [SKIP] Comparison skipped due to Ollama failure.")
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Minecraft RAG API (Generation & Embeddings)")
    parser.add_argument("-g", "--generate", action="store_true", help="Test LLM Generation")
    parser.add_argument("-e", "--embed", action="store_true", help="Test LLM Embeddings")
    
    args = parser.parse_args()

    if not (args.generate or args.embed):
        print("Please specify -g (generate) and/or -e (embed) to run tests.")
        parser.print_help()
        sys.exit(1)

    if args.generate:
        test_generation(USER_PROMPTS)
    
    if args.embed:
        test_embedding(USER_PROMPTS)  