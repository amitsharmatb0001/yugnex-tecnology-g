"""
FILE: project_memory.py
PATH: yugnex/backend/memory/project_memory.py
PURPOSE: Manages long-term storage of project context (requirements, decisions, etc.).
WORKING:
    1. add_entry: Saves a new memory snippet to the database.
    2. get_recent: Retrieves the most recent memories for context injection.
    3. get_by_type: Filters memories by category (e.g., 'requirement' vs 'decision').
USAGE:
    manager = ProjectMemoryManager(db_session)
    await manager.add_entry(project_id=1, kind="requirement", content="Use FastAPI")
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from database.models import ProjectMemory

class ProjectMemoryManager:
    def __init__(self, db: AsyncSession):
        """
        PURPOSE: Initialize with an active database session.
        PARAMS: db (AsyncSession)
        """
        self.db = db

    async def add_entry(
        self, 
        project_id: int, 
        memory_type: str, 
        content: str, 
        importance: int = 5
    ) -> ProjectMemory:
        """
        PURPOSE: Save a new piece of context to the project's memory.
        PARAMS: 
            project_id (int): ID of the project.
            memory_type (str): Category ('requirement', 'decision', 'code', 'note').
            content (str): The actual information to remember.
            importance (int): 1-10 scale of how critical this memory is.
        RETURNS: The created ProjectMemory object.
        """
        new_memory = ProjectMemory(
            project_id=project_id,
            memory_type=memory_type,
            content=content,
            importance=importance
        )
        
        self.db.add(new_memory)
        await self.db.commit()
        await self.db.refresh(new_memory)
        return new_memory

    async def get_recent(self, project_id: int, limit: int = 10) -> List[ProjectMemory]:
        """
        PURPOSE: Retrieve the most recent context items.
        PARAMS: project_id (int), limit (int)
        RETURNS: List of ProjectMemory objects ordered by creation date (newest first).
        """
        query = (
            select(ProjectMemory)
            .where(ProjectMemory.project_id == project_id)
            .order_by(desc(ProjectMemory.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_important(self, project_id: int, min_importance: int = 7, limit: int = 10) -> List[ProjectMemory]:
        """
        PURPOSE: Retrieve high-importance context (e.g., core architectural decisions).
        PARAMS: project_id (int), min_importance (int)
        RETURNS: List of critical ProjectMemory objects.
        """
        query = (
            select(ProjectMemory)
            .where(
                ProjectMemory.project_id == project_id,
                ProjectMemory.importance >= min_importance
            )
            .order_by(desc(ProjectMemory.importance))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_type(self, project_id: int, memory_type: str) -> List[ProjectMemory]:
        """
        PURPOSE: Retrieve all context of a specific type (e.g., all 'requirements').
        PARAMS: project_id (int), memory_type (str)
        RETURNS: List of ProjectMemory objects.
        """
        query = (
            select(ProjectMemory)
            .where(
                ProjectMemory.project_id == project_id,
                ProjectMemory.memory_type == memory_type
            )
            .order_by(desc(ProjectMemory.created_at))
        )
        result = await self.db.execute(query)
        return result.scalars().all()