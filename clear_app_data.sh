#!/bin/bash

echo "Clearing all app data and restarting services..."

# Stop all running services
pkill -f "uvicorn main:app" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true

# Clear the user database
rm -f /home/jd/AI_Tutor/backend/aura_users.db

# Clear localStorage and rebuild
echo "localStorage.clear();" > /tmp/clear_storage.js

echo "All app data cleared. Restarting backend..."

# Start backend
cd /home/jd/AI_Tutor/backend && uvicorn main:app --reload --port 9000 &

echo "Backend started. Ready for clean testing."