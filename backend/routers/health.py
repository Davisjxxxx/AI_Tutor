# backend/routers/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter()

@router.get("/api/health/live", tags=["Health"])
async def live():
    """
    Simple liveness probe.
    """
    return {"status": "ok"}

@router.get("/api/health/ready", tags=["Health"])
async def ready(db: Session = Depends(get_db)):
    """
    Readiness probe that checks the database connection.
    """
    try:
        # A simple query to check if the database is responsive
        db.execute("SELECT 1")
        return {"status": "ok", "database": "ok"}
    except Exception as e:
        return {"status": "ok", "database": "error", "detail": str(e)}
