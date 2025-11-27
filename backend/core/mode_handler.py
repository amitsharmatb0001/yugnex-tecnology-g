"""
Utility helpers to detect the current interaction mode.
"""

from __future__ import annotations

from typing import Literal


def detect_mode(user_input: str) -> Literal["chat", "agent"]:
    """
    Simple heuristic that distinguishes conversational input from task requests.
    """
    normalized = user_input.strip().lower()
    if any(keyword in normalized for keyword in ("build", "fix", "implement", "task:")):
        return "agent"
    return "chat"

