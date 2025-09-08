#!/bin/bash

echo "=== APK File Details ==="
ls -lh /home/jd/AI_Tutor/android/app/build/outputs/apk/debug/app-debug.apk
echo ""

echo "=== File Type ==="
file /home/jd/AI_Tutor/android/app/build/outputs/apk/debug/app-debug.apk
echo ""

echo "=== Starting Backend Server ==="
cd /home/jd/AI_Tutor/backend
nohup uvicorn main:app --reload --port 9000 > backend.log 2>&1 &
echo "Backend server started with PID: $!"
echo ""

echo "=== Waiting for server to start ==="
sleep 5
echo ""

echo "=== Testing Backend Health ==="
curl -s http://localhost:9000/docs | head -1
echo ""

echo "=== Testing Authentication ==="
curl -X POST http://localhost:9000/api/auth/signup -H "Content-Type: application/json" -d '{"name": "Mobile Test", "email": "mobile@test.com", "password": "password123"}'
echo ""

echo "=== Checking for ADB ==="
which adb
echo ""

echo "=== ADB Devices ==="
adb devices 2>/dev/null || echo "ADB not available"
echo ""

echo "=== Process Status ==="
ps aux | grep uvicorn | grep -v grep