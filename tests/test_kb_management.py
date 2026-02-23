#!/usr/bin/env python3
"""
Test File: test_kb_management.py
Description: Tests the API interactions required for an instructor to manage their Knowledge Bases (KBs).
How it is tested: Imitates an authenticated instructor over HTTP requests to create a mock KB, upload a simulated `.txt` file parsing multipart data, retrieve KB source details, and completely delete the file, asserting HTTP status codes.
"""
import asyncio
import httpx
import os
import sys

# Configuration
BASE_URL = "http://localhost:8000"
INSTRUCTOR_EMAIL = "instructor@purdue.edu"
INSTRUCTOR_PASSWORD = "password"

async def login(client):
    """Login and return access token."""
    response = await client.post(f"{BASE_URL}/api/login", json={
        "email": INSTRUCTOR_EMAIL,
        "password": INSTRUCTOR_PASSWORD
    })
    
    if response.status_code != 200:
        print(f"Login failed: {response.text}")
        return None
        
    return response.json()["access_token"]

async def test_kb_flow():
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("1. Logging in as instructor...")
        token = await login(client)
        if not token:
            return False
            
        headers = {"Authorization": f"Bearer {token}"}
        
        # 2. Create KB
        kb_name = f"test_kb_{int(asyncio.get_event_loop().time())}"
        print(f"2. Creating Knowledge Base '{kb_name}'...")
        response = await client.post(
            f"{BASE_URL}/api/instructor/kbs",
            json={"name": kb_name},
            headers=headers
        )
        if response.status_code != 201:
            print(f"Failed to create KB: {response.status_code} - {response.text}")
            return False
        print("   KB created successfully.")
        
        # 3. List KBs
        print("3. Listing Knowledge Bases...")
        response = await client.get(f"{BASE_URL}/api/instructor/kbs", headers=headers)
        if response.status_code != 200:
             print(f"Failed to list KBs: {response.status_code}")
             return False
        kbs = response.json().get("kbs", [])
        if kb_name not in kbs:
             print(f"New KB '{kb_name}' not found in list: {kbs}")
             return False
        print(f"   KB '{kb_name}' found in list.")
        
        # 4. Upload File
        filename = "test_doc.txt"
        content = b"This is a test document for the knowledge base."
        print(f"4. Uploading file '{filename}' to KB...")
        
        # Create a dummy file object
        files = {'file': (filename, content, 'text/plain')}
        response = await client.post(
            f"{BASE_URL}/api/instructor/kbs/{kb_name}/files",
            files=files,
            headers=headers
        )
        if response.status_code != 200:
            print(f"Failed to upload file: {response.status_code} - {response.text}")
            return False
        print("   File uploaded successfully.")
        
        # 5. Get KB Details (verify file)
        print("5. Verifying file in KB...")
        response = await client.get(f"{BASE_URL}/api/instructor/kbs/{kb_name}", headers=headers)
        if response.status_code != 200:
             print(f"Failed to get KB details: {response.status_code}")
             return False
        data = response.json()
        # The API returns 'files' which is a list of source paths
        # We need to check if our filename is in any of the paths
        files_l = data.get("files", [])
        found = False
        for f in files_l:
            if filename in f:
                found = True
                break
        
        if not found:
             print(f"File '{filename}' not found in KB details: {files_l}")
             return False
        print("   File found in KB.")
        
        # 6. Delete File
        print("6. Deleting file from KB...")
        response = await client.delete(
            f"{BASE_URL}/api/instructor/kbs/{kb_name}/files/{filename}",
            headers=headers
        )
        if response.status_code != 200:
             print(f"Failed to delete file: {response.status_code} - {response.text}")
             return False
        print("   File deleted successfully.")
        
        # 7. Verify Deletion
        print("7. Verifying deletion...")
        response = await client.get(f"{BASE_URL}/api/instructor/kbs/{kb_name}", headers=headers)
        files_l = response.json().get("files", [])
        found = False
        for f in files_l:
            if filename in f:
                found = True
                break
        if found:
             print("File still exists in KB after deletion!")
             return False
        print("   File successfully removed.")
        
        print("\nAll tests passed!")
        return True

if __name__ == "__main__":
    try:
        if asyncio.run(test_kb_flow()):
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nTest interrupted")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)
