"""
Workflow helpers for chaining agents.
"""

from __future__ import annotations

from typing import Callable, Dict, List


def run_workflow(tasks: List[Callable[[Dict], Dict]], payload: Dict) -> Dict:
    """
    Executes a simple pipeline of callables, passing the payload along.
    """
    data = payload
    for step in tasks:
        data = step(data)
    return data

