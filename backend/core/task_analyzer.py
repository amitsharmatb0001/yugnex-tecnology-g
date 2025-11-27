"""
Basic task analysis helpers.
"""

from __future__ import annotations

from typing import Dict


class TaskAnalyzer:
    """
    Extracts intent and important entities from user input.
    """

    def analyze_task(self, user_input: str) -> Dict[str, str]:
        summary = user_input.strip()
        priority = "high" if "urgent" in summary.lower() else "normal"
        return {"summary": summary, "priority": priority}

