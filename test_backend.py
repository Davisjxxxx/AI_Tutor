#!/usr/bin/env python3
"""
Backend Testing Script for Nova AI Tutor
Tests all the endpoints requested by the user
"""

import requests
import json
import sys
import subprocess
import time
import signal
import os
from typing import Dict, Any

class BackendTester:
    def __init__(self, base_url: str = "http://localhost:9000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_user_token = None
        
    def test_backend_running(self) -> bool:
        """Test if backend is running by checking the docs endpoint"""
        print("🔍 Testing if backend is running...")
        try:
            response = self.session.get(f"{self.base_url}/docs", timeout=5)
            if response.status_code == 200 and "swagger" in response.text.lower():
                print("✅ Backend is running and serving FastAPI docs")
                return True
            else:
                print(f"❌ Backend responded with status {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Backend not running: {e}")
            return False
    
    def start_backend(self) -> bool:
        """Start the backend server"""
        print("🚀 Starting backend server...")
        try:
            # Change to backend directory and start server
            backend_dir = "/home/jd/AI_Tutor/backend"
            os.chdir(backend_dir)
            
            # Start uvicorn in background
            proc = subprocess.Popen([
                "python3", "-m", "uvicorn", "main:app", 
                "--reload", "--port", "9000", "--host", "0.0.0.0"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Wait a bit for server to start
            print("⏳ Waiting for server to start...")
            time.sleep(5)
            
            # Check if it's running
            if self.test_backend_running():
                print("✅ Backend started successfully")
                return True
            else:
                print("❌ Backend failed to start")
                return False
                
        except Exception as e:
            print(f"❌ Error starting backend: {e}")
            return False
    
    def test_signup(self) -> Dict[str, Any]:
        """Test the signup endpoint"""
        print("\\n👤 Testing signup endpoint...")
        
        signup_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/signup",
                json=signup_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Signup successful")
                print(f"   User ID: {result['user']['id']}")
                print(f"   Email: {result['user']['email']}")
                print(f"   Token: {result['token'][:20]}...")
                
                # Store token for later tests
                self.test_user_token = result['token']
                
                return {
                    "status": "success",
                    "data": result,
                    "response_code": response.status_code
                }
            else:
                error_msg = response.json().get("detail", "Unknown error")
                print(f"❌ Signup failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "response_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ Signup request failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_login(self) -> Dict[str, Any]:
        """Test the login endpoint"""
        print("\\n🔐 Testing login endpoint...")
        
        login_data = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/auth/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Login successful")
                print(f"   User ID: {result['user']['id']}")
                print(f"   Email: {result['user']['email']}")
                print(f"   Token: {result['token'][:20]}...")
                
                # Update stored token
                self.test_user_token = result['token']
                
                return {
                    "status": "success",
                    "data": result,
                    "response_code": response.status_code
                }
            else:
                error_msg = response.json().get("detail", "Unknown error")
                print(f"❌ Login failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "response_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ Login request failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_chat(self) -> Dict[str, Any]:
        """Test the AI chat functionality"""
        print("\\n🤖 Testing AI chat endpoint...")
        
        chat_data = {
            "message": "Hello, I need help with JavaScript",
            "user_id": "test_user",
            "engine": "llama"
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Chat endpoint working")
                print(f"   Success: {result['success']}")
                print(f"   Response: {result['response'][:100]}...")
                
                return {
                    "status": "success",
                    "data": result,
                    "response_code": response.status_code
                }
            else:
                error_msg = response.json().get("detail", "Unknown error")
                print(f"❌ Chat failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "response_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ Chat request failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_agent_capabilities(self) -> Dict[str, Any]:
        """Test the agent capabilities endpoint"""
        print("\\n🎯 Testing agent capabilities endpoint...")
        
        try:
            response = self.session.get(f"{self.base_url}/api/agents/capabilities")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Agent capabilities endpoint working")
                print(f"   Success: {result['success']}")
                print(f"   Available agents: {len(result['agents'])}")
                
                for agent_name, agent_info in result['agents'].items():
                    print(f"   - {agent_name}: {len(agent_info['capabilities'])} capabilities")
                
                return {
                    "status": "success",
                    "data": result,
                    "response_code": response.status_code
                }
            else:
                error_msg = response.json().get("detail", "Unknown error")
                print(f"❌ Agent capabilities failed: {error_msg}")
                return {
                    "status": "error",
                    "error": error_msg,
                    "response_code": response.status_code
                }
                
        except Exception as e:
            print(f"❌ Agent capabilities request failed: {e}")
            return {"status": "error", "error": str(e)}
    
    def test_apk_file(self) -> Dict[str, Any]:
        """Test if APK file exists and check its size"""
        print("\\n📱 Testing APK file existence...")
        
        apk_path = "/home/jd/AI_Tutor/android/app/build/outputs/apk/debug/app-debug.apk"
        
        try:
            if os.path.exists(apk_path):
                file_size = os.path.getsize(apk_path)
                file_size_mb = file_size / (1024 * 1024)
                
                print(f"✅ APK file exists")
                print(f"   Path: {apk_path}")
                print(f"   Size: {file_size_mb:.2f} MB ({file_size:,} bytes)")
                
                return {
                    "status": "success",
                    "path": apk_path,
                    "size_bytes": file_size,
                    "size_mb": file_size_mb
                }
            else:
                print(f"❌ APK file not found at: {apk_path}")
                return {
                    "status": "error",
                    "error": "APK file not found",
                    "path": apk_path
                }
                
        except Exception as e:
            print(f"❌ Error checking APK file: {e}")
            return {"status": "error", "error": str(e)}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return summary"""
        print("🧪 Starting Nova AI Tutor Backend Tests")
        print("=" * 50)
        
        results = {}
        
        # Test 1: Check if backend is running
        if not self.test_backend_running():
            # Try to start backend
            if not self.start_backend():
                print("❌ Cannot proceed with tests - backend not running")
                return {"status": "failed", "error": "Backend not accessible"}
        
        # Test 2: Test signup
        results['signup'] = self.test_signup()
        
        # Test 3: Test login
        results['login'] = self.test_login()
        
        # Test 4: Test chat
        results['chat'] = self.test_chat()
        
        # Test 5: Test agent capabilities
        results['agent_capabilities'] = self.test_agent_capabilities()
        
        # Test 6: Test APK file
        results['apk_file'] = self.test_apk_file()
        
        # Summary
        print("\\n" + "=" * 50)
        print("📊 TEST SUMMARY")
        print("=" * 50)
        
        passed = 0
        failed = 0
        
        for test_name, result in results.items():
            status = "✅ PASSED" if result['status'] == 'success' else "❌ FAILED"
            print(f"{test_name:<20}: {status}")
            if result['status'] == 'success':
                passed += 1
            else:
                failed += 1
        
        print(f"\\nTotal: {passed} passed, {failed} failed")
        
        return {
            "status": "completed",
            "passed": passed,
            "failed": failed,
            "results": results
        }

def main():
    print("Nova AI Tutor Backend Testing Script")
    print("====================================\\n")
    
    tester = BackendTester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if results['failed'] == 0 else 1)

if __name__ == "__main__":
    main()