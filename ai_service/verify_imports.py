import sys
print(f"Python executable: {sys.executable}")

try:
    import tiktoken
    print("✓ tiktoken available")
except ImportError as e:
    print(f"✗ tiktoken MISSING: {e}")

try:
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    print("✓ langchain.text_splitter available")
except ImportError as e:
    print(f"✗ langchain.text_splitter MISSING: {e}")
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        print("✓ langchain_text_splitters available (Alternative)")
    except ImportError as e2:
        print(f"✗ langchain_text_splitters MISSING: {e2}")

try:
    from langchain_community.document_loaders import UnstructuredMarkdownLoader
    print("✓ langchain_community available")
except ImportError as e:
    print(f"✗ langchain_community MISSING: {e}")

try:
    from pymilvus import MilvusClient
    print("✓ pymilvus available")
except ImportError as e:
    print(f"✗ pymilvus MISSING: {e}")

try:
    from openai import OpenAI
    print("✓ openai available")
except ImportError as e:
    print(f"✗ openai MISSING: {e}")

try:
    from chromadb.utils import embedding_functions
    print("✓ chromadb available")
except ImportError as e:
    print(f"✗ chromadb MISSING: {e}")

try:
    from chunking_evaluation.chunking import ClusterSemanticChunker
    print("✓ chunking_evaluation available")
except ImportError as e:
    print(f"✗ chunking_evaluation MISSING: {e}")
