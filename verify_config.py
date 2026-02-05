#!/usr/bin/env python3
"""
ChiPT Q&A System - Configuration Verification Script
Verifies all configuration settings match requirements.
"""
import os
import re
import sys

# Expected configuration
EXPECTED_CONFIG = {
    "OPENAI_BASE_URL": "http://localhost:11434/v1",
    "EMBEDDING_MODEL": "qwen3-embedding:8b-q8_0",
    "CHAT_MODEL": "gpt-oss:120b",
    "EMBEDDING_DIM": "4096",
    "STUDENT_EMAIL": "student@purdue",
    "INSTRUCTOR_EMAIL": "instructor@purdue",
    "PASSWORD": "123456",
}

# Files to check
FILES_TO_CHECK = {
    "ai_service/main.py": {
        "OPENAI_BASE_URL": r'OPENAI_BASE_URL\s*=\s*"([^"]+)"',
        "MODEL_NAME": r'MODEL_NAME\s*=\s*"([^"]+)"',
    },
    "cache_service/main.py": {
        "OPENAI_BASE_URL": r'OPENAI_BASE_URL\s*=\s*"([^"]+)"',
        "EMBEDDING_MODEL": r'EMBEDDING_MODEL\s*=\s*"([^"]+)"',
        "REWRITE_MODEL": r'REWRITE_MODEL\s*=\s*"([^"]+)"',
        "EMBEDDING_DIM": r'EMBEDDING_DIM\s*=\s*(\d+)',
    },
    "project/database.py": {
        "INSTRUCTOR_EMAIL": r'instructor\s*=\s*User\(\s*email="([^"]+)"',
        "STUDENT_EMAIL": r'student\s*=\s*User\(\s*email="([^"]+)"',
        "PASSWORD": r'hash_password\("([^"]+)"\)',
    },
}

def check_file(filepath, checks):
    """Check a file for expected patterns."""
    if not os.path.exists(filepath):
        print(f"  ✗ File not found: {filepath}")
        return False
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    all_pass = True
    for name, pattern in checks.items():
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            value = match.group(1)
            
            # Check against expected value
            expected_key = name
            if expected_key in EXPECTED_CONFIG:
                expected = EXPECTED_CONFIG[expected_key]
                if value == expected:
                    print(f"  ✓ {name}: {value}")
                else:
                    print(f"  ✗ {name}: {value} (expected: {expected})")
                    all_pass = False
            else:
                print(f"  ✓ {name}: {value}")
        else:
            print(f"  ✗ {name}: Not found")
            all_pass = False
    
    return all_pass

def check_structure():
    """Verify directory structure."""
    print("\n" + "="*70)
    print("Directory Structure Check")
    print("="*70)
    
    required_dirs = [
        "project",
        "ai_service",
        "cache_service",
    ]
    
    required_files = [
        "project/main.py",
        "project/database.py",
        "project/auth.py",
        "project/services.py",
        "project/schemas.py",
        "project/requirements.txt",
        "project/templates/index.html",
        "project/static/app.js",
        "ai_service/main.py",
        "ai_service/requirements.txt",
        "cache_service/main.py",
        "cache_service/requirements.txt",
        "cache_service/docker-compose.yml",
        "README.md",
    ]
    
    all_pass = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"  ✓ Directory: {dir_name}/")
        else:
            print(f"  ✗ Missing directory: {dir_name}/")
            all_pass = False
    
    for filepath in required_files:
        if os.path.isfile(filepath):
            print(f"  ✓ File: {filepath}")
        else:
            print(f"  ✗ Missing file: {filepath}")
            all_pass = False
    
    return all_pass

def main():
    print("="*70)
    print("ChiPT Q&A System - Configuration Verification")
    print("="*70)
    print()
    print("Expected Configuration:")
    for key, value in EXPECTED_CONFIG.items():
        print(f"  {key}: {value}")
    
    # Check structure
    structure_ok = check_structure()
    
    # Check each file
    all_pass = True
    for filepath, checks in FILES_TO_CHECK.items():
        print(f"\n{'='*70}")
        print(f"Checking: {filepath}")
        print("="*70)
        result = check_file(filepath, checks)
        all_pass = all_pass and result
    
    # Final summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    
    if all_pass and structure_ok:
        print("✓ All checks PASSED")
        print("\nConfiguration is correct!")
        print("\nNext steps:")
        print("1. Start Milvus: cd cache_service && docker-compose up -d")
        print("2. Start cache service: cd cache_service && python main.py")
        print("3. Start AI service: cd ai_service && python main.py")
        print("4. Start main app: cd project && uvicorn main:app --reload --port 8000")
        return 0
    else:
        print("✗ Some checks FAILED")
        print("\nPlease review the errors above and fix the configuration.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted")
        sys.exit(1)
