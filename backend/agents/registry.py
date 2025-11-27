"""
FILE: registry.py
PATH: yugnex/backend/agents/registry.py
PURPOSE: Central factory to load agents dynamically.
WORKING:
    1. Maps string keys ('advait') to Classes (Advait).
    2. Provides a 'get_agent' factory method.
USAGE:
    agent = AgentRegistry.get_agent("advait", db_session)
"""

from typing import Dict, Type
from sqlalchemy.ext.asyncio import AsyncSession

# Import all agents
from core.tilotma import Tilotma
from agents.leadership import Advait
from agents.analysts import Saanvi
from agents.developers import Shubham
from agents.reviewers import Navya
from agents.base import BaseAgent

class AgentRegistry:
    # Map keys to classes
    AGENTS: Dict[str, Type[BaseAgent]] = {
        "tilotma": Tilotma,
        "advait": Advait,
        "saanvi": Saanvi,
        "shubham": Shubham,
        "navya": Navya
    }

    @staticmethod
    def get_agent(agent_key: str, db: AsyncSession) -> BaseAgent:
        """
        PURPOSE: Factory method to instantiate an agent by name.
        PARAMS: agent_key (str), db (AsyncSession)
        RETURNS: Instance of the requested Agent.
        RAISES: ValueError if agent_key is unknown.
        """
        agent_cls = AgentRegistry.AGENTS.get(agent_key.lower())
        
        if not agent_cls:
            valid_keys = list(AgentRegistry.AGENTS.keys())
            raise ValueError(f"Unknown agent: '{agent_key}'. Valid agents: {valid_keys}")
            
        return agent_cls(db)