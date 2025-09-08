# backend/core/config.py
import os
from dotenv import load_dotenv

# Load .env file before importing settings
load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

if APP_ENV == "production":
    from ..config.production import settings
else:
    # Default to development settings
    from ..config.default import settings

__all__ = ["settings"]
