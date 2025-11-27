"""
FILE: persistent.py
PATH: yugnex/backend/memory/persistent.py
PURPOSE: The high-level facade for the Memory System.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from memory.project_memory import ProjectMemoryManager
from memory.conversation import ConversationManager

class MemorySystem:
    def __init__(self, db: AsyncSession):
        """
        PURPOSE: Initialize the Memory System with necessary sub-managers.
        PARAMS: db (AsyncSession)
        """
        self.db = db
        self.project_memory = ProjectMemoryManager(db)
        self.conversation_memory = ConversationManager(db)

    async def remember(self, project_id: int, content: str, kind: str = "note", importance: int = 5):
        """
        PURPOSE: Universal method for an agent to save information.
        """
        return await self.project_memory.add_entry(
            project_id=project_id,
            memory_type=kind,
            content=content,
            importance=importance
        )

    async def recall_context(self, project_id: int) -> str:
        """
        PURPOSE: Build a text block of context to feed into an AI Agent's prompt.
        """
        # 1. Get Critical Context (High Importance)
        critical_items = await self.project_memory.get_important(project_id, min_importance=8, limit=5)
        
        # 2. Get Recent Context (Short-term memory)
        recent_items = await self.project_memory.get_recent(project_id, limit=5)
        
        # 3. Format Output
        context_lines = ["--- PROJECT CONTEXT ---"]
        
        if critical_items:
            context_lines.append("\n[CRITICAL DECISIONS]")
            for item in critical_items:
                context_lines.append(f"- [{item.memory_type.upper()}] {item.content}")
                
        if recent_items:
            context_lines.append("\n[RECENT UPDATES]")
            for item in recent_items:
                # Avoid duplicates if an item is both critical and recent
                if item not in critical_items:
                    context_lines.append(f"- [{item.memory_type.upper()}] {item.content}")
        
        context_lines.append("-----------------------")
        
        return "\n".join(context_lines)