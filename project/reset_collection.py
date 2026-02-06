#!/usr/bin/env python3
"""
Drop and recreate the Milvus collection with correct dimensions.
Run this when you change EMBEDDING_DIM.
"""
from pymilvus import connections, utility, Collection
from config import QA_DOCS_MILVUS_PORT, QA_DOCS_COLLECTION_NAME, MILVUS_HOST

# # Configuration - must match main.py
# MILVUS_HOST = "localhost"
# MILVUS_PORT = "19531"
# COLLECTION_NAME = "qa_cache"

def reset_collection():
    """Drop the existing collection so it can be recreated."""
    try:
        # Connect to Milvus
        connections.connect(
            alias="default",
            host=MILVUS_HOST,
            port=QA_DOCS_MILVUS_PORT
        )
        print(f"✓ Connected to Milvus at {MILVUS_HOST}:{QA_DOCS_MILVUS_PORT}")
        
        # Check if collection exists
        if utility.has_collection(QA_DOCS_COLLECTION_NAME):
            print(f"Found collection '{QA_DOCS_COLLECTION_NAME}'")
            
            # Get entity count before dropping
            collection = Collection(QA_DOCS_COLLECTION_NAME)
            count = collection.num_entities
            print(f"  Current entities: {count}")
            
            # Drop the collection
            utility.drop_collection(QA_DOCS_COLLECTION_NAME)
            print(f"✓ Dropped collection '{QA_DOCS_COLLECTION_NAME}'")
        else:
            print(f"Collection '{QA_DOCS_COLLECTION_NAME}' does not exist")
        
        # Disconnect
        connections.disconnect("default")
        
        print("\n" + "=" * 60)
        print("Collection reset complete!")
        print("Now restart the cache service:")
        print("  python main.py")
        print("\nIt will automatically create a new collection with")
        print("the correct dimensions and seed sample data.")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Milvus Collection Reset Tool")
    print("=" * 60)
    print()
    
    response = input(f"Drop collection '{QA_DOCS_COLLECTION_NAME}'? (y/n): ")
    if response.lower() == 'y':
        reset_collection()
    else:
        print("Cancelled")
