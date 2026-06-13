"""World-model construction for the HBCE ARC-AGI-3 public baseline."""

from __future__ import annotations

from typing import Any, Dict


def build_world_model(observation: Dict[str, Any]) -> Dict[str, Any]:
    grid = observation.get("grid") or []
    objects = observation.get("objects") or []
    return {
        "status": "WORLD_MODEL_READY",
        "grid_height": len(grid),
        "grid_width": len(grid[0]) if grid and isinstance(grid[0], list) else 0,
        "object_count": len(objects),
        "goal_hint": observation.get("goal_hint"),
    }
