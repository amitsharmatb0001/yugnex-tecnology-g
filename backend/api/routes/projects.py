"""
FILE: projects.py
PATH: yugnex/backend/api/routes/projects.py
PURPOSE: Manage project creation and retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from database.connection import get_db
from database.models import User, Project
from api.middleware.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter(prefix="/projects", tags=["Projects"])

# Schema for creating a project
class ProjectCreate(BaseModel):
    name: str
    description: str = None
    tech_stack: str = None

@router.post("/", response_model=dict)
async def create_project(
    project_in: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_project = Project(
        user_id=current_user.id,
        name=project_in.name,
        description=project_in.description,
        tech_stack=project_in.tech_stack
    )
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return {"id": new_project.id, "name": new_project.name, "status": "created"}

@router.get("/", response_model=List[dict])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Project).where(Project.user_id == current_user.id))
    projects = result.scalars().all()
    return [{"id": p.id, "name": p.name, "description": p.description} for p in projects]