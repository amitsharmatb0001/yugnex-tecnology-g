"""
FILE: user.py
PATH: yugnex/backend/api/schemas/user.py
PURPOSE: Defines Pydantic models for User data validation.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

# Properties to return to client (NEVER return password)
class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        from_attributes = True

# Login Request
class UserLogin(BaseModel):
    username: str
    password: str

# Token Response
class Token(BaseModel):
    access_token: str
    token_type: str

# Token Payload (Used in Middleware)
class TokenData(BaseModel):
    username: Optional[str] = None