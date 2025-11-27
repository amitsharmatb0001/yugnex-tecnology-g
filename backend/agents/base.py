"""
FILE: base.py
PATH: yugnex/backend/agents/base.py
PURPOSE: The abstract base class for all AI Agents in YugNex.
WORKING:
    1. Initializes with Memory and AI Router.
    2. Loads specific system prompts (e.g., 'tilotma.txt').
    3. Provides a standard 'run()' method that:
       a. Fetches context from memory.
       b. Constructs the full prompt.
       c. Calls the AI Router.
       d. Saves the result back to memory.
USAGE:
    class MyAgent(BaseAgent):
        def __init__(self, db):
            super().__init__(db, agent_key="my_agent")
"""

import os
import logging
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from services.ai_router import AIRouter
from memory.persistent import MemorySystem

logger = logging.getLogger(__name__)

class BaseAgent:
    def __init__(self, db: AsyncSession, agent_key: str):
        """
        PURPOSE: Initialize the agent with standard tools.
        PARAMS:
            db: Database session for memory access.
            agent_key: Unique ID (e.g., 'tilotma', 'advait') to load prompts.
        """
        self.agent_key = agent_key
        self.db = db
        self.memory = MemorySystem(db)
        self.router = AIRouter()
        
        # Load System Prompt
        self.system_prompt = self._load_prompt()

    def _load_prompt(self) -> str:
        """
        PURPOSE: Load the agent's specific instructions from config/prompts/.
        """
        try:
            # Construct path relative to this file or absolute project path
            # Assuming running from backend/ root
            path = f"config/prompts/{self.agent_key}.txt"
            
            if not os.path.exists(path):
                logger.warning(f"Prompt file not found for {self.agent_key}, using default.")
                return f"You are {self.agent_key}, a helpful AI assistant."
                
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading prompt for {self.agent_key}: {e}")
            return "You are an AI assistant."

    async def run(
        self, 
        user_input: str, 
        project_id: Optional[int] = None, 
        conversation_id: Optional[int] = None,
        context_files: Optional[str] = None
    ) -> str:
        """
        PURPOSE: The main execution loop for the agent.
        WORKING:
            1. Recall Memory (Context).
            2. Build Prompt (System + Context + User Input).
            3. Call AI (via Router).
            4. Remember Result.
        """
        # 1. Gather Context
        memory_context = ""
        if project_id:
            memory_context = await self.memory.recall_context(project_id)

        # 2. Construct Full System Instruction
        # We inject the memory context directly into the system prompt area
        full_system_instruction = f"""
{self.system_prompt}

=== CURRENT PROJECT CONTEXT ===
{memory_context}

=== PROVIDED FILES/CODE ===
{context_files if context_files else "None"}

=== BEHAVIOR RULES ===
1. NO HALLUCINATION: If unsure, ask.
2. HONESTY: If a task takes time, say so.
3. CONFIDENCE: State your confidence level if ambiguous.
"""

        # 3. Process with AI Router
        # Tilotma usually handles "general" tasks, others are specific
        response = await self.router.process_request(
            prompt=user_input,
            system_instruction=full_system_instruction,
            task_type="general", # Can be overridden by subclasses
            complexity="medium"
        )

        # 4. Save to Memory (Optional - usually handled by the conversation manager,
        # but the agent can save specific 'thoughts' or 'decisions' here if needed)
        
        return response