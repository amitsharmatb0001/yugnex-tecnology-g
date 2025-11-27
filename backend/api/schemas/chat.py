"""
Pydantic models for chat endpoints.
"""

from __future__ import annotations

from pydantic import BaseModel


class ChatMessage(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    reply: str
    mode: str

