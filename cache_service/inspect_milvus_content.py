
import sys
import os
from pymilvus import connections, Collection, utility

# Add parent directory to path to import config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import MILVUS_HOST, QA_DOCS_MILVUS_PORT, QA_DOCS_COLLECTION_NAME, LOCAL_MILVUS, MILVUS_RAG_DOCS_DB_PATH
from pymilvus import MilvusClient, connections, Collection, utility

def inspect_cache():
    try:
        if LOCAL_MILVUS:
            print(f"Connecting to Milvus Lite at {MILVUS_RAG_DOCS_DB_PATH}...")
            client = MilvusClient(MILVUS_RAG_DOCS_DB_PATH)
            
            if QA_DOCS_COLLECTION_NAME not in client.list_collections():
                print(f"Collection '{QA_DOCS_COLLECTION_NAME}' does not exist.")
                return

            print(f"Collection '{QA_DOCS_COLLECTION_NAME}' exists.")
            
            # Get count
            res = client.query(
                collection_name=QA_DOCS_COLLECTION_NAME,
                filter="id >= 0",
                output_fields=["count(*)"]
            )
            # MilvusClient query behavior for count might vary, let's just get all items if small
            
            results = client.query(
                collection_name=QA_DOCS_COLLECTION_NAME,
                filter="id >= 0",
                output_fields=["question", "answer"],
                limit=100
            )
            
            num_entities = len(results)
            print(f"Collection has {num_entities} entities (showing max 100).")
            
            if num_entities > 0:
                print("\nListing cached questions:")
                for i, res in enumerate(results):
                    q = res.get("question")
                    a = res.get("answer")
                    print(f"{i+1}. Q: {q}")
                    print(f"   A: {a[:50]}..." if a else "   A: [None]")
                    print("-" * 40)
            else:
                print("Cache is empty.")
                
        else:
            print(f"Connecting to Milvus at {MILVUS_HOST}:{QA_DOCS_MILVUS_PORT}...")
            connections.connect(
                alias="inspect",
                host=MILVUS_HOST,
                port=QA_DOCS_MILVUS_PORT
            )
            
            if not utility.has_collection(QA_DOCS_COLLECTION_NAME, using="inspect"):
                print(f"Collection '{QA_DOCS_COLLECTION_NAME}' does not exist.")
                return

            collection = Collection(QA_DOCS_COLLECTION_NAME, using="inspect")
            collection.load()
            
            num_entities = collection.num_entities
            print(f"Collection '{QA_DOCS_COLLECTION_NAME}' has {num_entities} entities.")
            
            if num_entities > 0:
                print("\nListing all cached questions:")
                results = collection.query(
                    expr="id >= 0",
                    output_fields=["question", "answer"],
                    limit=100
                )
                
                for i, res in enumerate(results):
                    q = res.get("question")
                    a = res.get("answer")
                    print(f"{i+1}. Q: {q}")
                    print(f"   A: {a[:50]}...")
                    print("-" * 40)
            else:
                print("Cache is empty.")

    except Exception as e:
        print(f"Error inspecting cache: {e}")

if __name__ == "__main__":
    inspect_cache()
