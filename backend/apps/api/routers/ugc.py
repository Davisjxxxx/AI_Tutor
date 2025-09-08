# apps/api/routers/ugc.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict
from core.ugc.engine import UGCEngine, UGCRequest, UGCResponse

router = APIRouter(prefix="/ugc", tags=["ugc"])

def get_ugc_engine():
    return UGCEngine()

@router.post("/generate", response_model=UGCResponse)
async def generate_ugc_content(
    request: UGCRequest,
    engine: UGCEngine = Depends(get_ugc_engine)
):
    """
    Generate AI avatar scripts and demos for teaching concepts
    """
    try:
        return engine.generate_content(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi_cache.decorator import cache

# ... (imports)

@router.get("/avatars", response_model=List[str])
@cache(expire=3600) # Cache for 1 hour
async def list_avatars(engine: UGCEngine = Depends(get_ugc_engine)):
    """
    List available avatar personas
    """
    return engine.list_avatars()

@router.post("/preview-cta", response_model=Dict)
async def preview_cta_variants(
    lesson_topic: str,
    cta_types: List[str],
    engine: UGCEngine = Depends(get_ugc_engine)
):
    """
    Preview CTA variants for a lesson topic
    """
    return engine.preview_cta(lesson_topic, cta_types)
