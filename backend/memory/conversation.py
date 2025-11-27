"""
FILE: conversation.py
PATH: yugnex/backend/memory/conversation.py
PURPOSE: Manages chat history and context retrieval for active conversations.
WORKING:
    1. create_conversation: Starts a new chat thread.
    2. add_message: Saves a user or agent message to the DB.
    3. get_history: Retrieves recent messages formatted for the LLM (Context Window).
USAGE:
    chat_mgr = ConversationManager(db_session)
    await chat_mgr.add_message(conv_id=1, role="user", content="Hello")
    history = await chat_mgr.get_history(conv_id=1, limit=10)
"""

from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database.models import Conversation, Message

class ConversationManager:
    def __init__(self, db: AsyncSession):
        """
        PURPOSE: Initialize with database session.
        PARAMS: db (AsyncSession)
        """
        self.db = db

    async def create_conversation(self, user_id: int, project_id: Optional[int] = None, title: str = "New Chat") -> Conversation:
        """
        PURPOSE: Start a new conversation thread.
        PARAMS: user_id, project_id (optional), title.
        RETURNS: Conversation object.
        """
        new_chat = Conversation(
            user_id=user_id,
            project_id=project_id,
            title=title,
            mode="chat" # Default mode
        )
        self.db.add(new_chat)
        await self.db.commit()
        await self.db.refresh(new_chat)
        return new_chat

    async def add_message(
        self, 
        conversation_id: int, 
        role: str, 
        content: str, 
        agent_key: Optional[str] = None,
        model_used: Optional[str] = None
    ) -> Message:
        """
        PURPOSE: Save a message to the history.
        PARAMS: 
            role: 'user', 'assistant', or 'system'.
            agent_key: 'tilotma', 'advait', etc. (if applicable).
        """
        new_msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            agent_key=agent_key,
            model_used=model_used
        )
        self.db.add(new_msg)
        await self.db.commit()
        await self.db.refresh(new_msg)
        return new_msg

    async def get_history(self, conversation_id: int, limit: int = 20) -> List[Dict[str, str]]:
        """
        PURPOSE: Retrieve chat history formatted for AI consumption.
        RETURNS: List of dicts [{'role': 'user', 'content': '...'}, ...]
        NOTE: Returns oldest messages first (chronological order) for the LLM.
        """
        # 1. Fetch recent messages (descending first to get the latest N)
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        messages = result.scalars().all()
        
        # 2. Reverse to chronological order (Oldest -> Newest)
        messages.reverse()
        
        # 3. Format as clean dictionaries
        return [
            {"role": msg.role, "content": msg.content} 
            for msg in messages
        ]