"""
FILE: analysts.py
PATH: yugnex/backend/agents/analysts.py
PURPOSE: Implements Saanvi (Analyst) with requirements gathering logic.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from agents.base import BaseAgent

class Saanvi(BaseAgent):
    """
    ROLE: Product Analyst
    FOCUS: Requirements, User Stories, Edge Cases
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db, agent_key="saanvi")

    async def analyze_request(self, user_input: str, project_id: int) -> str:
        """
        PURPOSE: First pass to see if requirements are clear.
        """
        prompt = f"""
        USER SAYS: "{user_input}"
        
        TASK: Analyze this request.
        1. Is it clear? (Yes/No)
        2. If No, list 3 specific questions to ask the user.
        3. If Yes, generate a summary of the scope.
        """
        
        return await self.run(user_input=prompt, project_id=project_id)

    async def generate_user_stories(self, confirmed_scope: str, project_id: int) -> str:
        """
        PURPOSE: Convert scope into formal tickets/stories.
        """
        prompt = f"""
        SCOPE: {confirmed_scope}
        
        TASK: Create a list of User Stories for the developers.
        FORMAT:
        - [Feature Name]: As a <role>, I want <action> so that <benefit>.
        - Acceptance Criteria: ...
        """
        
        return await self.run(user_input=prompt, project_id=project_id)