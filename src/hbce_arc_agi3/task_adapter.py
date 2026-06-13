"""Task adapter for HBCE ARC-AGI-3 public baseline.

The adapter normalizes raw task/game-like dictionaries into the internal
HBCE agent state format used by observer -> world_model -> planner.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass(frozen=True)
class NormalizedTask:
    status: str
    task_id: str
    grid: List[List[Any]]
    objects: List[Dict[str, Any]]
    goal_hint: str
    metadata: Dict[str, Any]

    def to_agent_state(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "grid": self.grid,
            "objects": self.objects,
            "goal_hint": self.goal_hint,
            "metadata": self.metadata,
        }

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _safe_grid(raw: Dict[str, Any]) -> List[List[Any]]:
    grid = raw.get("grid")
    if isinstance(grid, list):
        return grid

    input_grid = raw.get("input")
    if isinstance(input_grid, list):
        return input_grid

    state = raw.get("state")
    if isinstance(state, dict) and isinstance(state.get("grid"), list):
        return state["grid"]

    return []


def _safe_objects(raw: Dict[str, Any]) -> List[Dict[str, Any]]:
    objects = raw.get("objects")
    if isinstance(objects, list):
        return [obj for obj in objects if isinstance(obj, dict)]

    entities = raw.get("entities")
    if isinstance(entities, list):
        return [obj for obj in entities if isinstance(obj, dict)]

    return []


def normalize_task(raw: Dict[str, Any] | None = None, task_id: str | None = None) -> NormalizedTask:
    raw = raw or {}

    resolved_task_id = (
        task_id
        or str(raw.get("task_id") or raw.get("id") or raw.get("name") or "anonymous-task")
    )

    goal_hint = str(
        raw.get("goal_hint")
        or raw.get("goal")
        or raw.get("objective")
        or "explore"
    )

    metadata = {
        "raw_keys": sorted(str(key) for key in raw.keys()),
        "source": "task_adapter_v1",
        "has_grid": bool(_safe_grid(raw)),
        "object_count": len(_safe_objects(raw)),
    }

    return NormalizedTask(
        status="TASK_ADAPTER_READY",
        task_id=resolved_task_id,
        grid=_safe_grid(raw),
        objects=_safe_objects(raw),
        goal_hint=goal_hint,
        metadata=metadata,
    )
