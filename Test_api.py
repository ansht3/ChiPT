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

print("Models available:")
for model in CLIENT.models.list():
    print(model.id)

# Ollama Configuration for validation
OLLAMA_EMBED_URL = "http://localhost:11434/api/embed"
EMBEDDING_MODEL = "qwen3-embedding:8b-q8_0"

# Test Configuration
# Using the same test prompt as before, separated into System and User for Chat API
SYSTEM_PROMPT = "You are a Minecraft expert."
MODEL_NAME = "gpt-oss:120b" #"llama3.3:70b-instruct-q8_0" #"gpt-oss:120b"

USER_PROMPTS = [
    "Briefly explain how to craft a crafting table.",
    "What is the purpose of a crafting table?",
    "How do I make a wooden sword?",
    "What are the different types of wood in Minecraft?",
    "How do I make a furnace?",
    "What is the difference between a furnace and a blast furnace?",
    "What are some ways of efficiently storing items in Minecraft?",
    "How do I make a redstone torch?",
    "How can I beat the ender dragon?",
]

SIMILAR_USER_PROMPTS = [
    "How do I make a crafting table?",
    "What do I do with a crafting table?",
    "How is a wooden sword made?",
    "What are the various wood blocks in Minecraft?",
    "Can I make a furnace using cobblestone?",
    "What is the difference between a blast furnace and a regular furnace?",
    "I have too many items and blocks, how can I store them efficiently?",
    "What can a redstone torch be used for?",
    "How do I complete Minecraft?",
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

def get_ollama_embeddings(input_list):
    """Gets embedding directly from Ollama for validation."""
    try:
        response = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": EMBEDDING_MODEL,
                "input": input_list
            }
        )
        response.raise_for_status()
        return response.json()["embeddings"]
    except Exception as e:
        print(f"Error fetching Ollama embedding: {e}")
        return None

def test_embedding(prompts, similar_prompts):
    """Tests the embedding API and compares with direct Ollama call."""
    print("\n" + "="*50)
    print(f"Testing EMBEDDING connection to Proxy...")
    print(f"Target URL: {CLIENT.base_url}")
    print(f"Model: {EMBEDDING_MODEL}")
    print(f"Comparison URL: {OLLAMA_EMBED_URL}")
    print("="*50 + "\n")

    for p1, p2 in zip(prompts, similar_prompts):
        print(f"Prompt 1: {p1[:50]}...")
        print(f"Prompt 2: {p2[:50]}...")
        
        # 1. Get Embedding from Proxy (OpenAI Client)
        try:
            start_time = time.time()
            proxy_response = CLIENT.embeddings.create(
                model=EMBEDDING_MODEL,
                input=[p1, p2]
            )
            proxy_embedding1 = proxy_response.data[0].embedding
            proxy_embedding2 = proxy_response.data[1].embedding
            proxy_duration = time.time() - start_time
            print(f"  Proxy API Success (Took {proxy_duration:.2f}s)")
        except Exception as e:
            print(f"  Proxy API Failed: {e}")
            continue

        # 2. Get Embedding from Ollama (Direct)
        start_time = time.time()
        ollama_embeddings = get_ollama_embeddings([p1, p2])
        if ollama_embeddings is None:
            continue
        ollama_embedding1 = ollama_embeddings[0]
        ollama_embedding2 = ollama_embeddings[1]
        ollama_duration = time.time() - start_time
        if ollama_embedding1 and ollama_embedding2:
            print(f"  Ollama Direct Success (Took {ollama_duration:.2f}s)")
            
            # 3. Compare
            inter_model_similarity1 = cosine_similarity(proxy_embedding1, ollama_embedding1)
            inter_model_similarity2 = cosine_similarity(proxy_embedding2, ollama_embedding2)
            intra_proxy_model_similarity = cosine_similarity(proxy_embedding1, proxy_embedding2)
            intra_ollama_model_similarity = cosine_similarity(ollama_embedding1, ollama_embedding2)
            print(f"  Inter-Model Cosine Similarity prompt 1: {inter_model_similarity1:.4f}")
            print(f"  Inter-Model Cosine Similarity prompt 2: {inter_model_similarity2:.4f}")
            print(f"  Intra-Proxy-Model Cosine Similarity   : {intra_proxy_model_similarity:.4f}")
            print(f"  Intra-Ollama-Model Cosine Similarity  : {intra_ollama_model_similarity:.4f}")
            
            if inter_model_similarity1 > 0.99 and inter_model_similarity2 > 0.99:
                print("  [PASS] Embeddings match.")
            else:
                print("  [FAIL] Embeddings significantly different.")
        else:
             print("  [SKIP] Comparison skipped due to Ollama failure.")
        print("-" * 30)

def test_proxy_embedding(prompts, similar_prompts):
    """Tests the proxy embedding API and calculates intra-model similarity."""
    print("\n" + "="*50)
    print(f"Testing PROXY EMBEDDING ONLY...")
    print(f"Target URL: {CLIENT.base_url}")
    print(f"Model: {EMBEDDING_MODEL}")
    print("="*50 + "\n")

    for p1, p2 in zip(prompts, similar_prompts):
        print(f"Prompt 1: {p1[:50]}...")
        print(f"Prompt 2: {p2[:50]}...")
        
        try:
            start_time = time.time()
            proxy_response = CLIENT.embeddings.create(
                model=EMBEDDING_MODEL,
                input=[p1, p2]
            )
            proxy_embedding1 = proxy_response.data[0].embedding
            proxy_embedding2 = proxy_response.data[1].embedding
            proxy_duration = time.time() - start_time
            print(f"  Proxy API Success (Took {proxy_duration:.2f}s)")
            
            sim = cosine_similarity(proxy_embedding1, proxy_embedding2)
            print(f"  Intra-Proxy-Model Cosine Similarity: {sim:.4f}")
        except Exception as e:
            print(f"  Proxy API Failed: {e}")
        print("-" * 30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Minecraft RAG API (Generation & Embeddings)")
    parser.add_argument("-g", "--generate", action="store_true", help="Test LLM Generation")
    parser.add_argument("-e", "--embed", action="store_true", help="Test LLM Embeddings (Compare w/ Ollama)")
    parser.add_argument("-p", "--embed-proxy", action="store_true", help="Test Proxy Embeddings only (Intra-model similarity)")
    
    args = parser.parse_args()

    if not (args.generate or args.embed or args.embed_proxy):
        print("Please specify -g (generate), -e (embed), and/or -p (embed-proxy) to run tests.")
        parser.print_help()
        sys.exit(1)

    if args.generate:
        test_generation(USER_PROMPTS)
    
    if args.embed:
        test_embedding(USER_PROMPTS, SIMILAR_USER_PROMPTS)  
        
    if args.embed_proxy:
        test_proxy_embedding(USER_PROMPTS, SIMILAR_USER_PROMPTS)











