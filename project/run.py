#!/usr/bin/env python3
"""
Fix marshmallow version and run cache service
"""
import subprocess
import sys

def fix_marshmallow():
    """Upgrade marshmallow to fix version compatibility."""
    print("Checking marshmallow version...")
    
    try:
        import marshmallow
        version = getattr(marshmallow, '__version__', None)
        print(f"Current marshmallow version: {version}")
        
        # Check if __version_info__ exists
        if not hasattr(marshmallow, '__version_info__'):
            print("✗ marshmallow is missing __version_info__ attribute")
            print("Upgrading marshmallow...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                "--upgrade", "marshmallow>=3.20.0"
            ])
            print("✓ marshmallow upgraded")
            print("\nPlease run this script again to start the service.")
            return False
        else:
            print("✓ marshmallow version is compatible")
            return True
            
    except ImportError:
        print("✗ marshmallow not installed")
        print("Installing marshmallow...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "marshmallow>=3.20.0"
        ])
        print("✓ marshmallow installed")
        print("\nPlease run this script again to start the service.")
        return False

if __name__ == "__main__":
    if fix_marshmallow():
        print("\nStarting cache service...")
        print("-" * 60)
        # Import and run main
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8902, reload=True)
    else:
        sys.exit(1)
