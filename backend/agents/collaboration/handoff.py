"""
FILE: handoff.py
PATH: yugnex/backend/agents/collaboration/handoff.py
PURPOSE: Manages the transfer of tasks between agents.
WORKING:
    1. Creates a log entry in 'agent_logs' recording the transfer.
    2. Instantiates the target agent.
    3. Passes the context (history) to the new agent.
USAGE:
    next_agent_response = await HandoffManager.transfer(
        db, from_agent="tilotma", to_agent="advait", 
        task="Design the DB schema", context="..."
    )
"""

import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

# Import registry to load target agents dynamically
# Note: Local import inside method to avoid circular dependency if registry imports this
# from agents.registry import AgentRegistry (done inside method)

from database.models import AgentLog

logger = logging.getLogger(__name__)

class HandoffManager:
    @staticmethod
    async def transfer(
        db: AsyncSession,
        conversation_id: int,
        from_agent_key: str,
        to_agent_key: str,
        task_summary: str,
        context: str
    ) -> str:
        """
        PURPOSE: Execute a handoff from one agent to another.
        """
        from agents.registry import AgentRegistry  # Lazy import
        
        logger.info(f"HANDOFF: {from_agent_key} -> {to_agent_key} | Task: {task_summary[:50]}...")

        # 1. Log the Handoff in DB
        log_entry = AgentLog(
            conversation_id=conversation_id,
            agent_key=from_agent_key,
            action="handoff",
            output_summary=f"Transferred to {to_agent_key}: {task_summary}",
            input_summary=context[:200] # Log snippet of context
        )
        db.add(log_entry)
        await db.commit()

        # 2. Instantiate Target Agent
        target_agent = AgentRegistry.get_agent(to_agent_key, db)

        # 3. Construct Handoff Prompt
        # We wrap the task in a specific format so the target agent knows it's a handoff
        handoff_prompt = f"""
[INCOMING HANDOFF FROM {from_agent_key.upper()}]
TASK: {task_summary}

CONTEXT:
{context}

Please execute this task based on your role.
"""

        # 4. Run Target Agent
        response = await target_agent.run(
            user_input=handoff_prompt,
            conversation_id=conversation_id
        )

        return response