"""
FILE: ai_router.py
PATH: yugnex/backend/services/ai_router.py
PURPOSE: Determines which AI model should handle a specific task.
WORKING:
    1. select_model: Implements the logic table from Blueprint Part 11.
    2. process_request: Orchestrates the call to ModelManager.
    3. Handles the 'fallback' logic (if Claude fails, try Gemini).
USAGE:
    router = AIRouter()
    response = await router.process_request("Create a DB schema", task_type="architecture")
"""

import logging
from typing import List, Optional
from langchain_core.messages import SystemMessage, HumanMessage, BaseMessage

from core.model_manager import ModelManager
from config.settings import settings

logger = logging.getLogger(__name__)

class AIRouter:
    def __init__(self):
        self.manager = ModelManager()

    def select_model(self, task_type: str, complexity: str = "medium", requires_speed: bool = False) -> tuple[str, Optional[str]]:
        """
        PURPOSE: Select the best model based on task requirements.
        RULES:
            - Complex/Architecture/Review -> Claude Opus 4.5 (smartest)
            - Simple/Quick/Bulk -> Gemini or Claude Haiku (fastest)
            - Medium complexity -> Claude Sonnet 4.5 (balanced)
        
        Returns:
            Tuple of (provider, specific_model_name)
            e.g., ("claude", "claude-sonnet-4-5") or ("gemini", None)
        """
        # Force specific tasks to Gemini (fastest for simple tasks)
        if task_type in ["quick_answer", "simple_code", "summarization"] and complexity == "low":
            return ("gemini", None)
        
        # Complex tasks -> Claude Opus 4.5 (smartest)
        if complexity == "high" or task_type in ["architecture", "code_review", "deep_analysis", "planning"]:
            specific_model = self.manager.select_claude_model(task_type, complexity, requires_speed)
            return ("claude", specific_model)
        
        # Fast tasks -> Claude Haiku 4.5 (fastest Claude)
        if requires_speed or (complexity == "low" and task_type not in ["architecture", "code_review"]):
            return ("claude", "claude-haiku-4-5")
        
        # Default: Claude Sonnet 4.5 (best balance)
        return ("claude", "claude-sonnet-4-5")

    async def process_request(
        self, 
        prompt: str, 
        system_instruction: str, 
        task_type: str = "general", 
        complexity: str = "medium",
        requires_speed: bool = False,
        model_override: Optional[str] = None
    ) -> str:
        """
        PURPOSE: Main entry point for Agents to get an AI response.
        WORKING:
            1. Selects model based on task requirements (or uses override).
            2. Constructs message list.
            3. Calls Manager with specific model.
            4. Implements fallback logic (Part 11: "Claude hits limit -> Switch to Gemini").
        """
        # 1. Determine Model
        if model_override:
            # Parse override: could be "claude", "gemini", or specific model like "claude-sonnet-4-5"
            if model_override.startswith("claude-"):
                target_provider = "claude"
                specific_model = model_override
            elif model_override == "claude":
                target_provider = "claude"
                specific_model = None  # Will use default
            else:
                target_provider = model_override
                specific_model = None
        else:
            target_provider, specific_model = self.select_model(task_type, complexity, requires_speed)
        
        # 2. Build Messages
        messages: List[BaseMessage] = [
            SystemMessage(content=system_instruction),
            HumanMessage(content=prompt)
        ]

        # 3. Attempt Execution with Fallback
        try:
            if settings.ENV == "development" and specific_model:
                logger.info(f"Using model: {specific_model} for task_type={task_type}, complexity={complexity}")
            
            return await self.manager.invoke_model(target_provider, messages, specific_claude_model=specific_model)
        except Exception as primary_error:
            logger.warning(f"Primary model {target_provider} ({specific_model}) failed: {primary_error}. Attempting fallback.")
            
            # Fallback Strategy: Try Gemini if Claude failed, or Claude Haiku if other Claude failed
            if target_provider == "claude":
                # Try Gemini as fallback
                try:
                    return await self.manager.invoke_model("gemini", messages)
                except Exception as secondary_error:
                    logger.error(f"Fallback to Gemini also failed: {secondary_error}")
                    raise secondary_error
            else:
                # Try Claude Haiku (fastest Claude) as fallback
                try:
                    return await self.manager.invoke_model("claude", messages, specific_claude_model="claude-haiku-4-5")
                except Exception as secondary_error:
                    logger.error(f"Fallback to Claude Haiku also failed: {secondary_error}")
                    raise secondary_error