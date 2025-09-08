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
from . import models, schemas
from .database import get_db
from .agent_router import agent_router
from .aura_agent import get_aura_response, MEMORY
from .scheduler import start_scheduler
from .learning_profile import LearningProfile, LearningPathGenerator, ASSESSMENT_QUESTIONS
from .coach import router as coach_router
from .models_coach import Base as CoachBase
from .database import engine as coach_engine

# Structured Logging Configuration
structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)
log = structlog.get_logger()

# Create DB tables on startup
Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
@app.middleware("http")
async def root_middleware(request: Request, call_next):
    structlog.contextvars.clear_contextvars()
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)
    start_time = time.monotonic()
    log.info("request_started", method=request.method, path=request.url.path, client=request.client.host)
    
    response = await call_next(request)
    
    process_time = (time.monotonic() - start_time) * 1000
    log.info(
        "request_finished",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time_ms=round(process_time, 2),
    )
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; connect-src 'self';"
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-production-domain.com"], # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from .routers import ugc as ugc_storage_router
from .apps.api.routers import ugc as ugc_generation_router
from .routers import health
app.include_router(coach_router)
app.include_router(ugc_storage_router.router)
app.include_router(ugc_generation_router.router)
app.include_router(health.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Dependency


# --- Authentication Helper Functions ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_jwt_token(user_id: str) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
async def get_user(db: AsyncSession, user_id: str):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()

async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(
        id=str(uuid.uuid4()), 
        email=user.email, 
        name=user.name, 
        password_hash=hashed_password
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Authentication Endpoints ---
@app.post("/api/auth/signup", response_model=schemas.AuthResponse)
@limiter.limit("10/minute")
async def signup(request: Request, user_data: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = await create_user(db=db, user=user_data)
    token = create_jwt_token(created_user.id)
    return schemas.AuthResponse(user=created_user, token=token, success=True, message="Account created successfully")

@app.post("/api/auth/login", response_model=schemas.AuthResponse)
@limiter.limit("5/minute")
async def login(request: Request, login_data: schemas.UserLogin, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, email=login_data.email)
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_jwt_token(user.id)
    return schemas.AuthResponse(user=user, token=token, success=True, message="Login successful")

@app.get("/api/auth/me", response_model=schemas.User)
async def get_current_user(db: AsyncSession = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    token = authorization.credentials
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await get_user(db, user_id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

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