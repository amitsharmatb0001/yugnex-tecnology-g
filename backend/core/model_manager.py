"""
FILE: model_manager.py
PATH: yugnex/backend/core/model_manager.py
PURPOSE: Manages direct connections to AI providers (Claude & Gemini).
WORKING:
    1. Initializes LangChain clients for ChatAnthropic and ChatGoogleGenerativeAI.
    2. Provides a unified 'invoke_model' method to send messages to either provider.
    3. Handles basic error catching (though specific retry logic is often handled by LangChain).
USAGE:
    manager = ModelManager()
    response = await manager.invoke_model("claude", [HumanMessage(content="Hello")])
"""

import logging
from typing import List, Optional

from importlib import import_module
from typing import Any

from langchain_core.messages import BaseMessage
from langchain_anthropic import ChatAnthropic
from config.settings import settings

ChatGoogleGenerativeAI: Any | None
try:  # pragma: no cover - optional dependency at runtime
    ChatGoogleGenerativeAI = import_module("langchain_google_genai").ChatGoogleGenerativeAI
    _HAS_GOOGLE_GENAI = True
except ModuleNotFoundError:  # pragma: no cover
    ChatGoogleGenerativeAI = None
    _HAS_GOOGLE_GENAI = False

# Configure logging
logger = logging.getLogger(__name__)

# Model name mapping: friendly names -> actual API model identifiers
# Based on official Claude API documentation: https://platform.claude.com/docs/en/about-claude/models/overview
def get_model_name_map() -> dict:
    """Get model name mapping, with support for .env override."""
    default_map = {
        # =====================================================================
        # Claude 4.5 Models (Latest - November 2025)
        # =====================================================================
        # Claude Sonnet 4.5 - Smartest model for complex agents and coding
        "claude-sonnet-4.5": "claude-sonnet-4-5",  # Friendly name with dot -> official alias
        "claude-sonnet-4-5": "claude-sonnet-4-5",  # Official API alias
        "claude-sonnet-4-5-20250929": "claude-sonnet-4-5-20250929",  # Full API ID
        
        # Claude Haiku 4.5 - Fastest model with near-frontier intelligence
        "claude-haiku-4.5": "claude-haiku-4-5",  # Friendly name with dot -> official alias
        "claude-haiku-4-5": "claude-haiku-4-5",  # Official API alias
        "claude-haiku-4-5-20251001": "claude-haiku-4-5-20251001",  # Full API ID
        
        # Claude Opus 4.5 - Premium model combining maximum intelligence with practical performance
        "claude-opus-4.5": "claude-opus-4-5",  # Friendly name with dot -> official alias
        "claude-opus-4-5": "claude-opus-4-5",  # Official API alias
        "claude-opus-4-5-20251101": "claude-opus-4-5-20251101",  # Full API ID
        
        # Claude Opus 4.1 - Exceptional model for specialized reasoning tasks
        "claude-opus-4.1": "claude-opus-4-1",  # Friendly name with dot -> official alias
        "claude-opus-4-1": "claude-opus-4-1",  # Official API alias
        "claude-opus-4-1-20250805": "claude-opus-4-1-20250805",  # Full API ID
        
        # =====================================================================
        # Claude 3.5 Models (Previous Generation)
        # =====================================================================
        "claude-3-5-sonnet-20241022": "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet": "claude-3-5-sonnet-20241022",
        "claude-3-5-sonnet-latest": "claude-sonnet-4-5",  # Map to latest 4.5
        
        "claude-3-5-haiku-20241022": "claude-3-5-haiku-20241022",
        "claude-3-5-haiku": "claude-3-5-haiku-20241022",
        "claude-3-5-haiku-latest": "claude-haiku-4-5",  # Map to latest 4.5
        
        # =====================================================================
        # Claude 3.0 Models (Legacy)
        # =====================================================================
        "claude-3-opus-20240229": "claude-3-opus-20240229",
        "claude-3-opus": "claude-3-opus-20240229",
        
        "claude-3-sonnet-20240229": "claude-3-sonnet-20240229",
        "claude-3-sonnet": "claude-3-sonnet-20240229",
        
        "claude-3-haiku-20240307": "claude-3-haiku-20240307",
        "claude-3-haiku": "claude-3-haiku-20240307",
        
        # =====================================================================
        # Convenience Aliases
        # =====================================================================
        "claude-latest": "claude-sonnet-4-5",  # Default to Sonnet 4.5 (smartest for complex agents)
        "claude-fastest": "claude-haiku-4-5",  # Fastest model
        "claude-smartest": "claude-opus-4-5",  # Smartest model (premium)
        "claude-default": "claude-sonnet-4-5",  # Default model
        
        # =====================================================================
        # Gemini Models
        # =====================================================================
        "gemini-2.5-pro": "gemini-2.5-pro",
        "gemini-1.5-pro": "gemini-1.5-pro",
        "gemini-1.5-flash": "gemini-1.5-flash",
    }
    
    # Check if user provided custom mapping in settings
    if hasattr(settings, 'ANTHROPIC_MODEL_MAP') and settings.ANTHROPIC_MODEL_MAP:
        import json
        try:
            custom_map = json.loads(settings.ANTHROPIC_MODEL_MAP) if isinstance(settings.ANTHROPIC_MODEL_MAP, str) else settings.ANTHROPIC_MODEL_MAP
            default_map.update(custom_map)
        except:
            pass
    
    return default_map

def get_actual_model_name(model_name: str) -> str:
    """
    Convert friendly model name to actual API model identifier.
    
    Args:
        model_name: Friendly model name (e.g., "claude-sonnet-4.5")
        
    Returns:
        Actual API model identifier (e.g., "claude-3-5-sonnet-20241022")
    """
    model_map = get_model_name_map()
    return model_map.get(model_name, model_name)  # Return as-is if not in map

class ModelManager:
    def __init__(self):
        """
        PURPOSE: Initialize AI clients with API keys from settings.
        NOTE: No default model - models are selected dynamically based on task requirements.
        """
        # Store API key for dynamic model creation
        if settings.ANTHROPIC_API_KEY:
            # Validate key format
            api_key = settings.ANTHROPIC_API_KEY.strip()
            if not api_key.startswith("sk-ant-"):
                logger.warning(f"Anthropic API key doesn't start with 'sk-ant-'. Key starts with: {api_key[:10]}...")
            
            # Log key length for debugging (first 15 chars only for security)
            if settings.ENV == "development":
                logger.info(f"Anthropic key length: {len(api_key)} chars, starts with: {api_key[:15]}...")
            
            # Set as environment variable (LangChain prefers this)
            import os
            os.environ["ANTHROPIC_API_KEY"] = api_key
            self.anthropic_api_key = api_key
        else:
            self.anthropic_api_key = None
            if settings.ENV == "development":
                logger.warning("ANTHROPIC_API_KEY not found in environment variables")
        
        # Cache for created Claude clients (lazy initialization)
        self._claude_clients: dict[str, ChatAnthropic] = {}
        
        # List of working Claude models (from test results)
        self.available_claude_models = [
            "claude-sonnet-4-5",  # Official alias - Smartest for complex agents
            "claude-sonnet-4-5-20250929",  # Full API ID
            "claude-haiku-4-5",  # Official alias - Fastest model
            "claude-haiku-4-5-20251001",  # Full API ID
            "claude-opus-4-5",  # Official alias - Premium maximum intelligence
            "claude-opus-4-5-20251101",  # Full API ID
            "claude-opus-4-1",  # Official alias - Specialized reasoning
            "claude-opus-4-1-20250805",  # Full API ID
            "claude-3-5-haiku-20241022",  # Legacy
            "claude-3-haiku-20240307",  # Legacy
        ]

        # Initialize Gemini (Google)
        # Use GOOGLE_AI_STUDIO_KEY if available, otherwise fall back to GOOGLE_API_KEY
        google_key = settings.GOOGLE_AI_STUDIO_KEY or settings.GOOGLE_API_KEY
        
        if google_key and not _HAS_GOOGLE_GENAI:
            raise ImportError(
                "langchain-google-genai is required when Google API key is set. "
                "Install it via `pip install langchain-google-genai`."
            )

        self.gemini = (
            ChatGoogleGenerativeAI(
                model="gemini-2.5-pro",
                temperature=0,
                max_output_tokens=4096,
                google_api_key=google_key,
                convert_system_message_to_human=True,  # Gemini sometimes prefers system instructions differently
            )
            if google_key and _HAS_GOOGLE_GENAI
            else None
        )
        
        # Debug logging (only in development)
        if settings.ENV == "development":
            logger.info(f"Claude API Key configured: {bool(settings.ANTHROPIC_API_KEY)}")
            logger.info(f"Google API Key configured: {bool(google_key)}")
            if settings.ANTHROPIC_API_KEY:
                # Show first 10 chars for verification (security: don't log full key)
                logger.info(f"Anthropic key starts with: {settings.ANTHROPIC_API_KEY[:10]}...")
            if google_key:
                logger.info(f"Google key starts with: {google_key[:10]}...")

    def get_claude_client(self, model_name: str) -> ChatAnthropic:
        """
        Get or create a Claude client for the specified model.
        Uses lazy initialization and caching for efficiency.
        
        Args:
            model_name: Claude model name (e.g., "claude-sonnet-4-5")
            
        Returns:
            ChatAnthropic client instance
        """
        if not self.anthropic_api_key:
            raise ValueError("Anthropic API Key not configured.")
        
        # Map friendly name to actual API model identifier
        actual_model_name = get_actual_model_name(model_name)
        
        # Check cache first
        if actual_model_name in self._claude_clients:
            return self._claude_clients[actual_model_name]
        
        # Create new client
        client = ChatAnthropic(
            model=actual_model_name,
            temperature=0,
            max_tokens=4096,
            api_key=self.anthropic_api_key
        )
        
        # Cache it
        self._claude_clients[actual_model_name] = client
        
        if settings.ENV == "development":
            logger.info(f"Created Claude client for model: {actual_model_name}")
        
        return client
    
    def select_claude_model(self, task_type: str, complexity: str = "medium", requires_speed: bool = False) -> str:
        """
        Select the best Claude model based on task requirements.
        
        Args:
            task_type: Type of task (architecture, code_review, simple_code, etc.)
            complexity: Task complexity (low, medium, high)
            requires_speed: Whether speed is more important than quality
            
        Returns:
            Model name to use (e.g., "claude-sonnet-4-5")
        """
        # Fast tasks -> Haiku (fastest)
        if requires_speed or task_type in ["quick_answer", "simple_code", "summarization"]:
            return "claude-haiku-4-5"
        
        # Complex tasks -> Opus (smartest)
        if complexity == "high" or task_type in ["architecture", "deep_analysis", "planning", "code_review"]:
            return "claude-opus-4-5"
        
        # Specialized reasoning -> Opus 4.1
        if task_type in ["specialized_reasoning", "complex_problem_solving"]:
            return "claude-opus-4-1"
        
        # Default: Sonnet 4.5 (best balance of speed and intelligence)
        return "claude-sonnet-4-5"
    
    async def invoke_model(self, model_name: str, messages: List[BaseMessage], specific_claude_model: Optional[str] = None) -> str:
        """
        PURPOSE: Send a standardized message list to the requested model.
        PARAMS:
            model_name (str): 'claude' or 'gemini', or specific model name.
            messages (List[BaseMessage]): LangChain message objects (System, Human, AI).
            specific_claude_model (str, optional): Specific Claude model to use (e.g., "claude-sonnet-4-5").
        RETURNS: str (The content of the AI response).
        """
        try:
            # Handle specific Claude model names
            if model_name.startswith("claude-") or (model_name == "claude" and specific_claude_model):
                if not self.anthropic_api_key:
                    raise ValueError("Anthropic API Key not configured.")
                
                # Use specific model if provided, otherwise use default selection
                claude_model = specific_claude_model if specific_claude_model else "claude-sonnet-4-5"
                client = self.get_claude_client(claude_model)
                response = await client.ainvoke(messages)
                return response.content

            elif model_name == "gemini":
                if not self.gemini:
                    google_key = settings.GOOGLE_AI_STUDIO_KEY or settings.GOOGLE_API_KEY
                    if not google_key:
                        raise ValueError("Google API Key not configured. Set GOOGLE_AI_STUDIO_KEY or GOOGLE_API_KEY in .env")
                    else:
                        raise ValueError(f"Google API Key is set but Gemini client not initialized. Check langchain-google-genai installation.")
                response = await self.gemini.ainvoke(messages)
                return response.content
            
            else:
                raise ValueError(f"Unknown model name: {model_name}. Use 'claude', 'gemini', or a specific Claude model name.")

        except Exception as e:
            logger.error(f"Error invoking {model_name}: {str(e)}")
            # In a production v2, we would trigger auto-fallback here
            raise e