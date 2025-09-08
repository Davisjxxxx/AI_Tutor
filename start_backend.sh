#!/bin/bash

echo "Starting Nova AI Tutor backend..."

# Check for existing uvicorn processes
echo "1. Checking for existing uvicorn processes:"
ps aux | grep uvicorn | grep -v grep

# Kill any existing uvicorn processes
echo "2. Killing any existing uvicorn processes:"
pkill -f uvicorn
sleep 2

# Navigate to backend directory and start server
echo "3. Starting uvicorn server on port 9000:"
cd /home/jd/AI_Tutor/backend
uvicorn main:app --reload --port 9000 &
UVICORN_PID=$!

echo "4. Uvicorn started with PID: $UVICORN_PID"

# Wait a moment for server to start
sleep 5

# Test if backend is responding
echo "5. Testing backend docs endpoint:"
curl -s http://localhost:9000/docs | head -5

echo "6. Testing signup API endpoint:"
curl -X POST http://localhost:9000/api/auth/signup \
     -H "Content-Type: application/json" \
     -d '{"name": "Test User", "email": "test@example.com", "password": "password123"}'

echo ""
echo "7. Checking if uvicorn process is running:"
ps aux | grep uvicorn | grep -v grep

echo ""
echo "Backend startup complete!"