"""
Project API models.
"""

from __future__ import annotations

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: str | None = None


class ProjectRead(ProjectCreate):
    id: str

