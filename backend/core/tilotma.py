"""
FILE: tilotma.py
PATH: yugnex/backend/core/tilotma.py
PURPOSE: Implementation of the Chief AI Officer (Tilotma).
WORKING:
    1. Inherits from BaseAgent.
    2. Overrides 'run' if specific orchestration logic is needed.
    3. Acts as the gateway to the rest of the team (delegation logic will go here in v2).
USAGE:
    tilotma = Tilotma(db_session)
    response = await tilotma.run("Build me a website")
"""

import logging
from sqlalchemy.ext.asyncio import AsyncSession
from agents.base import BaseAgent

logger = logging.getLogger(__name__)

class Tilotma(BaseAgent):
    def __init__(self, db: AsyncSession):
        """
        PURPOSE: Initialize Tilotma with her specific key.
        """
        super().__init__(db, agent_key="tilotma")

    async def run(
        self, 
        user_input: str, 
        project_id: int = None, 
        conversation_id: int = None,
        context_files: str = None
    ) -> str:
        """
        PURPOSE: Process user input as the Chief AI Officer.
        NOTE: In v1, Tilotma handles the conversation directly. 
              In v2, this method will parse intent and call 'advait.run()' etc.
        """
        logger.info(f"Tilotma processing: {user_input[:50]}...")
        
        # In the future, we can add 'intent detection' logic here.
        # Example:
        # if "review this code" in user_input:
        #     return await self.delegate_to_navya(user_input, ...)

        # For v1 Phase 2, she processes it using her System Prompt + Router
        response = await super().run(
            user_input=user_input,
            project_id=project_id,
            conversation_id=conversation_id,
            context_files=context_files
        )
        
        return response