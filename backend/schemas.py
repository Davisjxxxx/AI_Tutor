# backend/schemas.py
from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime.datetime
    learning_profile: Optional[str] = None
    subscription_status: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: str
    password: str

class AuthResponse(BaseModel):
    user: User
    token: str
    success: bool
    message: str

class ChatMessage(BaseModel):
    message: str
    user_id: str
    engine: str = "llama"

class ChatResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None
