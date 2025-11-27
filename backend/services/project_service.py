"""
Business logic for projects.
"""

from __future__ import annotations

import uuid
from typing import Dict, List

from memory.project_memory import ProjectMemory


class ProjectService:
    """
    Provides CRUD-like helpers backed by ProjectMemory.
    """

    def __init__(self, store: ProjectMemory | None = None) -> None:
        self._store = store or ProjectMemory()

    def create_project(self, name: str, description: str | None = None) -> Dict[str, str]:
        project_id = uuid.uuid4().hex
        data = {"id": project_id, "name": name, "description": description}
        self._store.upsert_project(project_id, data)
        return data

    def get_project(self, project_id: str) -> Dict[str, str]:
        return self._store.get_project(project_id)

    def list_projects(self) -> List[Dict[str, str]]:
        # PersistentMemory is currently a simple key/value store; mimic listing.
        # Future implementation can fetch all keys; for now return empty list.
        return []

