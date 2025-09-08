#!/usr/bin/env python3

import requests
import json
import os

def test_endpoints():
    """Test all the endpoints requested by the user"""
    
    print("Nova AI Tutor Backend Testing")
    print("=" * 40)
    
    base_url = "http://localhost:9000"
    
    # Test 1: Check if backend is running
    print("\\n1. Testing if backend is running...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=5)
        if response.status_code == 200:
            print("✓ Backend is running - FastAPI docs accessible")
            print(f"  Status: {response.status_code}")
            print(f"  Content includes Swagger UI: {'swagger' in response.text.lower()}")
        else:
            print(f"✗ Backend responded with status {response.status_code}")
            return
    except Exception as e:
        print(f"✗ Backend not running: {e}")
        print("  Please start the backend with: cd /home/jd/AI_Tutor/backend && uvicorn main:app --reload --port 9000")
        return
    
    # Test 2: Test signup endpoint
    print("\\n2. Testing authentication signup endpoint...")
    signup_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/signup", json=signup_data)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✓ Signup successful")
            print(f"  User ID: {result['user']['id']}")
            print(f"  Token: {result['token'][:20]}...")
            token = result['token']
        else:
            print(f"✗ Signup failed: {response.text}")
            token = None
    except Exception as e:
        print(f"✗ Signup error: {e}")
        token = None
    
    # Test 3: Test login endpoint
    print("\\n3. Testing authentication login endpoint...")
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/auth/login", json=login_data)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✓ Login successful")
            print(f"  User ID: {result['user']['id']}")
            print(f"  Token: {result['token'][:20]}...")
        else:
            print(f"✗ Login failed: {response.text}")
    except Exception as e:
        print(f"✗ Login error: {e}")
    
    # Test 4: Test AI chat functionality
    print("\\n4. Testing AI chat functionality...")
    chat_data = {
        "message": "Hello, I need help with JavaScript",
        "user_id": "test_user",
        "engine": "llama"
    }
    
    try:
        response = requests.post(f"{base_url}/api/chat", json=chat_data)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✓ Chat endpoint working")
            print(f"  Success: {result.get('success', False)}")
            if result.get('response'):
                print(f"  Response: {result['response'][:100]}...")
            if result.get('error'):
                print(f"  Error: {result['error']}")
        else:
            print(f"✗ Chat failed: {response.text}")
    except Exception as e:
        print(f"✗ Chat error: {e}")
    
    # Test 5: Test agent capabilities
    print("\\n5. Testing agent capabilities...")
    try:
        response = requests.get(f"{base_url}/api/agents/capabilities")
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✓ Agent capabilities endpoint working")
            print(f"  Success: {result.get('success', False)}")
            if result.get('agents'):
                print(f"  Available agents: {len(result['agents'])}")
                for agent_name in result['agents'].keys():
                    print(f"    - {agent_name}")
        else:
            print(f"✗ Agent capabilities failed: {response.text}")
    except Exception as e:
        print(f"✗ Agent capabilities error: {e}")
    
    # Test 6: Check APK file
    print("\\n6. Checking APK file...")
    apk_path = "/home/jd/AI_Tutor/android/app/build/outputs/apk/debug/app-debug.apk"
    
    if os.path.exists(apk_path):
        file_size = os.path.getsize(apk_path)
        file_size_mb = file_size / (1024 * 1024)
        print("✓ APK file exists")
        print(f"  Path: {apk_path}")
        print(f"  Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")
        
        # Check metadata
        metadata_path = os.path.join(os.path.dirname(apk_path), "output-metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
                print(f"  Application ID: {metadata.get('applicationId', 'unknown')}")
                print(f"  Version: {metadata.get('elements', [{}])[0].get('versionName', 'unknown')}")
    else:
        print(f"✗ APK file not found at: {apk_path}")
    
    print("\\n" + "=" * 40)
    print("Testing completed!")

if __name__ == "__main__":
    test_endpoints()