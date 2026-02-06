#!/usr/bin/env python3
"""
Quick Fix for "collection not found" Error

This script checks which Milvus instance you're connected to and
helps recover from collection not found errors.
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from pymilvus import connections, utility, Collection
import requests

def check_milvus_instances():
    """Check both Milvus instances."""
    instances = {
        "ChiPT Milvus (19531)": ("localhost", "19531"),
        "Standard Milvus (19530)": ("localhost", "19530"),
    }
    
    print("Checking Milvus instances...")
    print("=" * 60)
    
    for name, (host, port) in instances.items():
        try:
            connections.connect(alias=f"check_{port}", host=host, port=port)
            collections = utility.list_collections()
            print(f"\n✓ {name} - RUNNING")
            print(f"  Collections: {collections}")
            
            if "qa_cache" in collections:
                coll = Collection("qa_cache")
                print(f"  qa_cache entities: {coll.num_entities}")
            
            connections.disconnect(f"check_{port}")
        except Exception as e:
            print(f"\n✗ {name} - NOT AVAILABLE")
            print(f"  Error: {str(e)[:100]}")

def check_cache_service_config():
    """Check cache service configuration."""
    print("\n" + "=" * 60)
    print("Cache Service Configuration")
    print("=" * 60)
    
    try:
        with open('main.py', 'r') as f:
            content = f.read()
            
            # Find MILVUS_PORT
            import re
            port_match = re.search(r'MILVUS_PORT\s*=\s*"(\d+)"', content)
            if port_match:
                port = port_match.group(1)
                print(f"Configured Milvus Port: {port}")
                
                if port == "19531":
                    print("✓ Correct - should use ChiPT Milvus on port 19531")
                elif port == "19530":
                    print("✗ ERROR - pointing to standard Milvus (19530)")
                    print("  Should be 19531 for ChiPT Milvus")
                    return False
            else:
                print("✗ Could not find MILVUS_PORT in main.py")
                return False
    except Exception as e:
        print(f"✗ Error reading config: {e}")
        return False
    
    return True

def fix_collection():
    """Try to fix the collection issue."""
    print("\n" + "=" * 60)
    print("Attempting to Fix Collection")
    print("=" * 60)
    
    try:
        # Connect to ChiPT Milvus
        connections.connect(alias="default", host="localhost", port="19531")
        print("✓ Connected to ChiPT Milvus (19531)")
        
        # Check if collection exists
        if utility.has_collection("qa_cache"):
            print("✓ Collection 'qa_cache' exists")
            coll = Collection("qa_cache")
            coll.load()
            print(f"✓ Collection loaded with {coll.num_entities} entities")
            print("\nCollection is OK. The cache service should work now.")
            print("If you're still having issues, restart the cache service:")
            print("  python main.py")
        else:
            print("✗ Collection 'qa_cache' not found")
            print("\nTo fix: Restart the cache service and it will recreate the collection:")
            print("  1. Stop cache service (Ctrl+C)")
            print("  2. python main.py")
            print("\nThe service will automatically create and seed the collection.")
        
        connections.disconnect("default")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        print("\nSuggested fixes:")
        print("1. Make sure ChiPT Milvus is running:")
        print("   cd cache_service && docker-compose ps")
        print("2. If not running, start it:")
        print("   cd cache_service && docker-compose up -d")
        print("3. Wait 30 seconds, then restart cache service:")
        print("   python main.py")

def main():
    print("=" * 60)
    print("ChiPT Cache Service - Collection Not Found Fix")
    print("=" * 60)
    
    # Check Milvus instances
    check_milvus_instances()
    
    # Check configuration
    config_ok = check_cache_service_config()
    
    if not config_ok:
        print("\n" + "!" * 60)
        print("CONFIGURATION ERROR DETECTED")
        print("!" * 60)
        print("\nYour cache service is pointing to the wrong Milvus instance.")
        print("Please fix the configuration in main.py:")
        print('  MILVUS_PORT = "19531"  # Should be 19531, not 19530')
        return 1
    
    # Try to fix
    fix_collection()
    
    print("\n" + "=" * 60)
    print("Diagnostic Complete")
    print("=" * 60)

if __name__ == "__main__":
    try:
        exit(main())
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)

