"""
FILE: chat.py
PATH: yugnex/backend/api/routes/chat.py
PURPOSE: Manage chat conversations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.connection import get_db
from database.models import User, Conversation
from api.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/conversations", tags=["Chat"])

class ConversationCreate(BaseModel):
    project_id: int = None
    title: str = "New Chat"

@router.post("/", response_model=dict)
async def start_conversation(
    conv_in: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_chat = Conversation(
        user_id=current_user.id,
        project_id=conv_in.project_id,
        title=conv_in.title
    )
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return {"id": new_chat.id, "title": new_chat.title}

@router.get("/", response_model=List[dict])
async def get_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Conversation).where(Conversation.user_id == current_user.id))
    chats = result.scalars().all()
    return [{"id": c.id, "title": c.title, "created_at": c.created_at} for c in chats]