# backend/config/default.py
import os

class Settings:
    # API metadata
    PROJECT_NAME: str = "AURA AI Tutor"
    VERSION: str = "0.1.0"

    # Security
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Supabase
    SUPABASE_URL: str = os.getenv("VITE_SUPABASE_URL", "")
    SUPABASE_ANON_KEY: str = os.getenv("VITE_SUPABASE_ANON_KEY", "")

    # Twilio
    TWILIO_FROM: str = os.getenv("TWILIO_FROM", "")
    TWILIO_ACCOUNT_SID: str = os.getenv("TWILIO_ACCOUNT_SID", "")
    TWILIO_AUTH_TOKEN: str = os.getenv("TWILIO_AUTH_TOKEN", "")
    
    # AI Providers
    OPENAI_API_KEY: str = os.getenv("VITE_OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("VITE_GEMINI_API_KEY", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    # Default to SQLite for development if DATABASE_URL is not set
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./aura_users.db")

    # Redis for caching
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # This is a placeholder and should be overridden in production
    JWT_SECRET: str = "your-secret-key-change-in-production"
    SERVICE_USER_ID: str = os.getenv("SERVICE_USER_ID", "")

settings = Settings()
