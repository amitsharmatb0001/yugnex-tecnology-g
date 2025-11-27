"""
FILE: agents.py
PATH: yugnex/backend/api/routes/agents.py
PURPOSE: List available agents and their status.
"""

from fastapi import APIRouter
from agents.registry import AgentRegistry

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/")
async def list_agents():
    """Return list of active agents"""
    return [
        {"key": "tilotma", "role": "Chief AI Officer"},
        {"key": "advait", "role": "Tech Lead"},
        {"key": "saanvi", "role": "Product Analyst"},
        {"key": "shubham", "role": "Senior Developer"},
        {"key": "navya", "role": "Code Reviewer"},
    ]