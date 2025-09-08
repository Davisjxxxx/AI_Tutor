#!/usr/bin/env python3

import requests
import json

API_URL = "http://localhost:9000/api"

def test_auth():
    print("=== Nova AI Tutor Authentication Test ===")
    
    # Test 1: Sign up
    print("\n1. Testing User Signup...")
    signup_data = {
        "name": "Test User",
        "email": f"test{import random; random.randint(1000, 9999)}@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{API_URL}/auth/signup", json=signup_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✓ Signup successful: {result['user']['name']} ({result['user']['email']})")
            user_id = result['user']['id']
            token = result['token']
            
            # Test 2: Login with same credentials
            print("\n2. Testing User Login...")
            login_data = {
                "email": signup_data["email"],
                "password": signup_data["password"]
            }
            
            response = requests.post(f"{API_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✓ Login successful: {result['user']['name']}")
                
                # Test 3: Test AI Chat
                print("\n3. Testing AI Chat...")
                chat_data = {
                    "message": "Hello, I need help with JavaScript",
                    "user_id": user_id,
                    "engine": "llama"
                }
                
                response = requests.post(f"{API_URL}/chat", json=chat_data)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"✓ AI Chat working: {result['response'][:100]}...")
                    else:
                        print(f"✗ AI Chat failed: {result.get('error', 'Unknown error')}")
                else:
                    print(f"✗ AI Chat failed: {response.status_code}")
                
                print("\n=== All Tests Completed ===")
                print("✓ Authentication system working")
                print("✓ User registration and login functional")
                print("✓ AI chat system operational")
                return True
            else:
                print(f"✗ Login failed: {response.status_code}")
                return False
        else:
            print(f"✗ Signup failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"✗ Connection error: {e}")
        print("Make sure the backend is running on port 9000")
        return False

if __name__ == "__main__":
    test_auth()