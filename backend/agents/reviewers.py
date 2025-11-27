"""
FILE: reviewers.py
PATH: yugnex/backend/agents/reviewers.py
PURPOSE: Implements Navya (Reviewer) with QA logic.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from agents.base import BaseAgent

class Navya(BaseAgent):
    """
    ROLE: Code Reviewer
    FOCUS: QA, Security, Best Practices
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db, agent_key="navya")

    async def review_code(self, code_snippet: str, context: str, project_id: int) -> str:
        """
        PURPOSE: Review a specific piece of code.
        """
        prompt = f"""
        CONTEXT: {context}
        CODE TO REVIEW:
        {code_snippet}
        
        TASK: Review this code for:
        1. Bugs
        2. Security Vulnerabilities
        3. Readability
        
        FINAL VERDICT: Start your response with either [APPROVE] or [REQUEST CHANGES].
        """
        
        return await self.run(user_input=prompt, project_id=project_id)

    def parse_verdict(self, review_text: str) -> str:
        """
        PURPOSE: programmatic check of the review result.
        """
        upper_text = review_text.upper()
        if "[APPROVE]" in upper_text:
            return "approved"
        elif "[REQUEST CHANGES]" in upper_text or "REQUEST CHANGES" in upper_text:
            return "rejected"
        else:
            return "ambiguous"