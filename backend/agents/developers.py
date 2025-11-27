"""
FILE: developers.py
PATH: yugnex/backend/agents/developers.py
PURPOSE: Implements Shubham (Developer) with code extraction logic.
"""

import re
from typing import Dict, List
from sqlalchemy.ext.asyncio import AsyncSession
from agents.base import BaseAgent

class Shubham(BaseAgent):
    """
    ROLE: Senior Developer
    FOCUS: Implementation, Code Generation
    """
    def __init__(self, db: AsyncSession):
        super().__init__(db, agent_key="shubham")

    async def generate_feature(self, spec: str, project_id: int) -> str:
        """
        PURPOSE: Write code based on a spec.
        """
        prompt = f"""
        SPECIFICATION: {spec}
        
        TASK: Write the code for this feature.
        RULES:
        1. Include file paths in comments (e.g., # FILE: app.py)
        2. Write full implementations, no placeholders.
        """
        
        response = await self.run(user_input=prompt, project_id=project_id)
        return response

    def extract_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        PURPOSE: Helper to parse the AI response and separate code from chat.
        RETURNS: List of dicts {'language': 'python', 'code': '...'}
        """
        # Regex to find ```python ... ``` blocks
        pattern = r"```(\w+)\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        
        extracted = []
        for lang, code in matches:
            extracted.append({
                "language": lang,
                "code": code.strip()
            })
            
        return extracted