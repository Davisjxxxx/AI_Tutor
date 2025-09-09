# backend/core/config.py
import os
from dotenv import load_dotenv

# Load .env file from the backend directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

APP_ENV = os.getenv("APP_ENV", "development")

if APP_ENV == "production":
    from ..config.production import settings
else:
    # Default to development settings
    from ..config.default import settings

__all__ = ["settings"]
