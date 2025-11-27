"""
FILE: __init__.py
PATH: yugnex/backend/memory/__init__.py
PURPOSE: Exports the Memory System facade and managers.
"""

from .project_memory import ProjectMemoryManager
from .conversation import ConversationManager
from .user_preferences import UserPreferencesManager
# FIX: Changed MemoryService to MemorySystem
from .persistent import MemorySystem

__all__ = [
    "ProjectMemoryManager", 
    "ConversationManager", 
    "UserPreferencesManager",
    "MemorySystem"
]