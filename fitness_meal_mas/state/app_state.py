"""Shared application state used by all agents."""

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AppState:
    """Shared state container for the multi-agent system."""

    profile: Dict[str, Any] = field(default_factory=dict)
    nutrition: Dict[str, Any] = field(default_factory=dict)
    meal_plan: Dict[str, List[str]] = field(default_factory=dict)
    grocery_list: List[str] = field(default_factory=list)
    workout_plan: List[str] = field(default_factory=list)

