"""
FILE: leadership.py
PATH: yugnex/backend/agents/leadership.py
PURPOSE: Implements Advait (Tech Lead) with specific architecture logic.
USAGE:
    advait = Advait(db)
    plan = await advait.create_architecture_plan("Build a CRM")
"""

from sqlalchemy.ext.asyncio import AsyncSession
from agents.base import BaseAgent

class Advait(BaseAgent):
    """
    ROLE: Tech Lead
    FOCUS: Architecture, Tech Stack, Feasibility
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db, agent_key="advait")

    async def create_architecture_plan(self, requirement_summary: str, project_id: int) -> str:
        """
        PURPOSE: specific method to generate a structured tech plan.
        """
        # 1. Override task type to ensure Claude is used (Architecture = Complex)
        prompt = f"""
        REQ: {requirement_summary}
        
        TASK: Create a detailed technical architecture plan.
        OUTPUT FORMAT:
        1. Tech Stack (Backend, Frontend, DB)
        2. Database Schema (Tables & Relationships)
        3. API Endpoints (List critical routes)
        4. Folder Structure
        """
        
        response = await self.run(
            user_input=prompt,
            project_id=project_id,
            # Force complexity to high to trigger Claude via Router
            # (Note: BaseAgent passes this to Router)
        )
        
        return self._clean_output(response)

    def _clean_output(self, text: str) -> str:
        """
        PURPOSE: Remove unnecessary conversational fluff if needed.
        """
        if "Here is the architecture" in text:
            return text.split("Here is the architecture")[-1].strip()
        return text