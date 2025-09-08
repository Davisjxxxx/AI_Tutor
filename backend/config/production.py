# backend/config/production.py
import os
from .default import Settings

class ProductionSettings(Settings):
    # In production, secrets MUST be loaded from the environment.
    # The application will fail to start if these are not set.
    JWT_SECRET: str = os.environ["JWT_SECRET"]
    DATABASE_URL: str = os.environ["DATABASE_URL"]
    REDIS_URL: str = os.environ["REDIS_URL"]
    
    # All API keys must also be set in the production environment
    VITE_SUPABASE_URL: str = os.environ["VITE_SUPABASE_URL"]
    VITE_SUPABASE_ANON_KEY: str = os.environ["VITE_SUPABASE_ANON_KEY"]
    TWILIO_FROM: str = os.environ["TWILIO_FROM"]
    TWILIO_ACCOUNT_SID: str = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN: str = os.environ["TWILIO_AUTH_TOKEN"]
    VITE_OPENAI_API_KEY: str = os.environ["VITE_OPENAI_API_KEY"]

settings = ProductionSettings()
