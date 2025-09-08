#!/usr/bin/env python3
"""
Test script to start and test Nova AI Tutor backend
Run this script manually: python3 test_backend_startup.py
"""

import subprocess
import time
import requests
import json
import os
import signal
import sys

def run_command(cmd, description):
    """Run a shell command and return the result"""
    print(f"\n{description}")
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        print(f"Return code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
        return result
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return None
    except Exception as e:
        print(f"Error running command: {e}")
        return None

def test_backend():
    print("=== Nova AI Tutor Backend Startup Test ===")
    
    # 1. Check for existing uvicorn processes
    run_command("ps aux | grep uvicorn", "1. Checking for existing uvicorn processes")
    
    # 2. Kill any existing uvicorn processes
    run_command("pkill -f uvicorn", "2. Killing any existing uvicorn processes")
    time.sleep(2)
    
    # 3. Start uvicorn server
    print("\n3. Starting uvicorn server...")
    backend_dir = "/home/jd/AI_Tutor/backend"
    os.chdir(backend_dir)
    
    # Start uvicorn in background
    uvicorn_process = subprocess.Popen([
        "uvicorn", "main:app", "--reload", "--port", "9000"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    print(f"Started uvicorn with PID: {uvicorn_process.pid}")
    
    # Wait for server to start
    print("Waiting 5 seconds for server to start...")
    time.sleep(5)
    
    # 4. Test if backend is responding
    print("\n4. Testing backend endpoints...")
    
    try:
        # Test docs endpoint
        print("Testing /docs endpoint...")
        response = requests.get("http://localhost:9000/docs", timeout=5)
        print(f"Docs endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Docs endpoint is working!")
            print(f"First 200 chars: {response.text[:200]}...")
        else:
            print(f"✗ Docs endpoint failed with status {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to connect to docs endpoint: {e}")
    
    try:
        # Test signup API endpoint
        print("\nTesting /api/auth/signup endpoint...")
        signup_data = {
            "name": "Test User",
            "email": "test@example.com", 
            "password": "password123"
        }
        
        response = requests.post(
            "http://localhost:9000/api/auth/signup",
            headers={"Content-Type": "application/json"},
            json=signup_data,
            timeout=5
        )
        
        print(f"Signup endpoint status: {response.status_code}")
        if response.status_code in [200, 201]:
            print("✓ Signup endpoint is working!")
            print(f"Response: {response.json()}")
        elif response.status_code == 400:
            print("⚠ Signup endpoint working but user might already exist")
            print(f"Response: {response.json()}")
        else:
            print(f"✗ Signup endpoint failed with status {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed to connect to signup endpoint: {e}")
    
    # 5. Check if process is still running
    print("\n5. Checking if uvicorn process is still running...")
    run_command("ps aux | grep uvicorn", "Current uvicorn processes")
    
    # Keep server running or kill it
    print(f"\nUvicorn server is running with PID: {uvicorn_process.pid}")
    print("Server will continue running in background.")
    print("To stop it later, run: kill", uvicorn_process.pid)
    print("Or use: pkill -f uvicorn")
    
    return uvicorn_process.pid

if __name__ == "__main__":
    try:
        pid = test_backend()
        print(f"\n=== Backend test completed. Server PID: {pid} ===")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nTest failed with error: {e}")