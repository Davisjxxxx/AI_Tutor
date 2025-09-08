# backend/routers/ugc.py
import uuid
import sqlite3
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime

from ..main import get_current_user, DATABASE_PATH

router = APIRouter()

# Pydantic Models
class UGCContentIn(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=10000)

class UGCContentOut(UGCContentIn):
    id: str
    author_id: str
    status: str
    created_at: str

# Dependency to get the current user from the token
async def get_verified_user(user: dict = Depends(get_current_user)):
    if not user or "user" not in user:
        raise HTTPException(status_code=401, detail="Authentication failed")
    return user["user"]

@router.post("/api/ugc", response_model=UGCContentOut, tags=["UGC"])
async def create_ugc(content: UGCContentIn, current_user: dict = Depends(get_verified_user)):
    """Allows authenticated users to submit new content."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    content_id = str(uuid.uuid4())
    author_id = current_user.id
    
    try:
        cursor.execute("""
            INSERT INTO ugc_content (id, author_id, title, content, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (content_id, author_id, content.title, content.content, datetime.datetime.utcnow().isoformat()))
        conn.commit()
        
        return UGCContentOut(
            id=content_id,
            author_id=author_id,
            title=content.title,
            content=content.content,
            status='pending',
            created_at=datetime.datetime.utcnow().isoformat()
        )
    except sqlite3.IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Database error: {e}")
    finally:
        conn.close()

@router.get("/api/ugc", response_model=List[UGCContentOut], tags=["UGC"])
async def list_approved_ugc():
    """Returns a list of all approved user-generated content."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, author_id, title, content, status, created_at FROM ugc_content WHERE status = 'approved'")
    rows = cursor.fetchall()
    conn.close()
    
    return [
        UGCContentOut(
            id=row[0],
            author_id=row[1],
            title=row[2],
            content=row[3],
            status=row[4],
            created_at=row[5]
        ) for row in rows
    ]

@router.get("/api/ugc/{content_id}", response_model=UGCContentOut, tags=["UGC"])
async def get_ugc_item(content_id: str):
    """Retrieves a single piece of user-generated content by its ID."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, author_id, title, content, status, created_at FROM ugc_content WHERE id = ? AND status = 'approved'", (content_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Approved content not found")
        
    return UGCContentOut(
        id=row[0],
        author_id=row[1],
        title=row[2],
        content=row[3],
        status=row[4],
        created_at=row[5]
    )
