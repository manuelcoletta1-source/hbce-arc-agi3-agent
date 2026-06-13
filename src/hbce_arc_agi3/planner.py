"""Planning layer for public ARC-AGI-3 smoke baseline."""

from __future__ import annotations

from typing import Any, Dict, List


def plan_action(world_model: Dict[str, Any]) -> Dict[str, Any]:
    goal_hint = world_model.get("goal_hint") or "explore"
    actions: List[str] = []

    if world_model.get("object_count", 0) > 0:
        actions.append("inspect_objects")
    if world_model.get("grid_height", 0) > 0:
        actions.append("inspect_grid")
    actions.append("propose_next_action")

    return {
        "status": "PLAN_READY",
        "goal": goal_hint,
        "actions": actions,
    }
