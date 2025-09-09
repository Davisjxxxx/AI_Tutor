"""main.py
FastAPI backend providing reminder CRUD, AI chat, and starting the background scheduler.
"""
import os
import sys
import uuid
import time
import datetime
import bcrypt
import jwt
import structlog
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from typing import List, Dict, Any, Optional
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from .core.config import settings
from .database import Base, engine
from . import models, schemas
from .database import get_db, Base, engine
from .agent_router import agent_router
from .aura_agent import get_aura_response, MEMORY
from .scheduler import start_scheduler
from .learning_profile import LearningProfile, LearningPathGenerator, ASSESSMENT_QUESTIONS
from .coach import router as coach_router
from .models_coach import Base as CoachBase
from .database import engine as coach_engine
from .auth import create_jwt_token, get_current_user, hash_password, verify_password

@app.post("/api/auth/google", response_model=schemas.AuthResponse)
async def google_auth(google_token: Dict[str, str], db: AsyncSession = Depends(get_db)):
    token = google_token.get("credential")
    if not token:
        raise HTTPException(status_code=400, detail="Missing Google credential")
    try:
        idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), settings.GOOGLE_CLIENT_ID)
        email = idinfo["email"]
        name = idinfo.get("name", "Google User")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Google token")
    user = await get_user_by_email(db, email=email)
    if not user:
        user = models.User(id=str(uuid.uuid4()), email=email, name=name, password_hash="google_auth")
        db.add(user)
        await db.commit()
        await db.refresh(user)
    token = create_jwt_token(user.id)
    return schemas.AuthResponse(user=user, token=token, success=True, message="Google authentication successful")

# --- AI Chat Endpoints ---
@app.post("/api/chat", response_model=schemas.ChatResponse)
async def chat_with_aura(message: schemas.ChatMessage):
    try:
        enhanced_prompt = agent_router.get_enhanced_prompt(message.message, user_context={"user_id": message.user_id})
        response = await get_aura_response(enhanced_prompt, user_id=message.user_id, engine=message.engine)
        return schemas.ChatResponse(response=response, success=True)
    except Exception as e:
        log.error("Chat endpoint error", error=e)
        return schemas.ChatResponse(response="", success=False, error=str(e))

# --- Startup Event ---
@app.on_event("startup")
async def startup_event():
    # Initialize caching
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    log.info("Cache initialized.")

    # Create coach DB tables
    CoachBase.metadata.create_all(bind=coach_engine)
    
    # Start original scheduler
    start_scheduler()

    # ---- APScheduler jobs for Coach ----
    sched = BackgroundScheduler(timezone=os.getenv("APP_TZ","America/Chicago"))
    service_user_id = settings.SERVICE_USER_ID
    if service_user_id:
        db = SessionLocal()
        service_user = get_user(db, service_user_id)
        if not service_user:
            db_user = models.User(id=service_user_id, email="service@aura.ai", name="Service Account", password_hash="service_account")
            db.add(db_user)
            db.commit()
        db.close()
        service_token = create_jwt_token(service_user_id)
        
        @sched.scheduled_job("cron", hour=8, minute=30)
        def _am_job():
            try:
                requests.post(f"{settings.BACKEND_BASE}/api/coach/am", json={"energy": 4}, headers={"Authorization": f"Bearer {service_token}"}, timeout=10)
            except Exception as e: 
                log.error("Error in AM job", error=e)
        
        sched.start() 
        log.info("APScheduler started for Coach jobs.")