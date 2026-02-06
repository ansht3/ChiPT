#!/usr/bin/env python3
"""
Verify that all required files are present for the Q&A system.
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists and print status."""
    exists = os.path.isfile(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {filepath:<30} {description}")
    return exists

def check_dir(dirpath, description):
    """Check if a directory exists and print status."""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {dirpath:<30} {description}")
    return exists

def main():
    print("=" * 60)
    print("Q&A System - File Structure Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Check main Python files
    print("Python Files:")
    all_good &= check_file("main.py", "FastAPI application")
    all_good &= check_file("database.py", "Database models")
    all_good &= check_file("auth.py", "Authentication")
    all_good &= check_file("schemas.py", "Pydantic schemas")
    all_good &= check_file("services.py", "Business logic")
    all_good &= check_file("requirements.txt", "Dependencies")
    print()
    
    # Check directories
    print("Directories:")
    all_good &= check_dir("templates", "Template directory")
    all_good &= check_dir("static", "Static files directory")
    print()
    
    # Check template files
    print("Template Files:")
    all_good &= check_file("templates/index.html", "Main HTML template")
    print()
    
    # Check static files
    print("Static Files:")
    all_good &= check_file("static/app.js", "Frontend JavaScript")
    print()
    
    print("=" * 60)
    if all_good:
        print("✓ All files present! You're ready to run the application.")
        print()
        print("Run with: uvicorn main:app --reload --port 8000")
        return 0
    else:
        print("✗ Some files are missing!")
        print()
        print("Missing files/directories need to be created.")
        print("Refer to the project structure in README.md")
        return 1

if __name__ == "__main__":
    sys.exit(main())
