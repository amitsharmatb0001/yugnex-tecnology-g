"""
FILE: user_preferences.py
PATH: yugnex/backend/memory/user_preferences.py
PURPOSE: Manages persistent user settings and preferences.
WORKING:
    1. get_preferences: Fetches the JSON blob from the user table.
    2. set_preference: Updates a specific key-value pair in the JSON blob.
    3. get_preference: Retrieves a single value (e.g., 'default_language').
USAGE:
    prefs_mgr = UserPreferencesManager(db_session)
    await prefs_mgr.set_preference(user_id=1, key="theme", value="dark")
"""

from typing import Any, Dict, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from database.models import User

class UserPreferencesManager:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self, user_id: int) -> Dict[str, Any]:
        """
        PURPOSE: Get the full preferences dictionary for a user.
        RETURNS: Dict (e.g., {'theme': 'dark', 'verbose_mode': True})
        """
        query = select(User.preferences).where(User.id == user_id)
        result = await self.db.execute(query)
        prefs = result.scalar_one_or_none()
        return prefs if prefs else {}

    async def get(self, user_id: int, key: str, default: Any = None) -> Any:
        """
        PURPOSE: Get a specific preference value.
        """
        prefs = await self.get_all(user_id)
        return prefs.get(key, default)

    async def set(self, user_id: int, key: str, value: Any) -> Dict[str, Any]:
        """
        PURPOSE: Update a single preference key.
        WORKING:
            1. Fetches current prefs.
            2. Updates the dictionary.
            3. Saves the entire dictionary back to DB.
            (PostgreSQL handles JSONB updates efficiently, but SQLAlchemy requires explicit set)
        """
        # 1. Get current
        current_prefs = await self.get_all(user_id)
        
        # 2. Update local dict
        updated_prefs = current_prefs.copy()
        updated_prefs[key] = value
        
        # 3. Update DB
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(preferences=updated_prefs)
            .execution_options(synchronize_session="fetch")
        )
        await self.db.execute(stmt)
        await self.db.commit()
        
        return updated_prefs