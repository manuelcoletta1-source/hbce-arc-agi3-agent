"""Observation layer for ARC-AGI-3 style environments."""

from __future__ import annotations

from typing import Any, Dict


def observe(raw_state: Dict[str, Any] | None = None) -> Dict[str, Any]:
    state = raw_state or {}
    return {
        "status": "OBSERVATION_READY",
        "objects": state.get("objects", []),
        "grid": state.get("grid", []),
        "goal_hint": state.get("goal_hint"),
    }


# === HBCE ARC AGI3 OBSERVER UPGRADE v1 START ===


from collections import Counter as _HbceCounter
from dataclasses import asdict as _hbce_asdict
from dataclasses import dataclass as _hbce_dataclass
from typing import Any as _HbceAny
from typing import Dict as _HbceDict
from typing import List as _HbceList


@_hbce_dataclass(frozen=True)
class HbceGridObservation:
    """Public-safe structured observation for ARC-AGI-3 grid-like tasks."""

    status: str
    task_id: str
    width: int
    height: int
    cell_count: int
    symbols: _HbceDict[str, int]
    non_empty_cells: _HbceList[_HbceDict[str, _HbceAny]]
    objects: _HbceList[_HbceDict[str, _HbceAny]]
    uncertainty_markers: _HbceList[str]
    metadata: _HbceDict[str, _HbceAny]

    def to_dict(self) -> _HbceDict[str, _HbceAny]:
        return _hbce_asdict(self)


def _hbce_is_grid(grid: _HbceAny) -> bool:
    return isinstance(grid, list) and all(isinstance(row, list) for row in grid)


def _hbce_grid_dimensions(grid: _HbceAny) -> tuple[int, int]:
    if not _hbce_is_grid(grid) or not grid:
        return (0, 0)

    height = len(grid)
    width = max((len(row) for row in grid), default=0)
    return (width, height)


def _hbce_symbol_counts(grid: _HbceAny) -> _HbceDict[str, int]:
    if not _hbce_is_grid(grid):
        return {}

    counter: _HbceCounter[str] = _HbceCounter()
    for row in grid:
        for cell in row:
            counter[str(cell)] += 1

    return dict(sorted(counter.items()))


def _hbce_non_empty_cells(grid: _HbceAny) -> _HbceList[_HbceDict[str, _HbceAny]]:
    if not _hbce_is_grid(grid):
        return []

    cells: _HbceList[_HbceDict[str, _HbceAny]] = []
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value not in (0, None, "", "."):
                cells.append({"x": x, "y": y, "value": value})

    return cells


def observe_agent_state(agent_state: _HbceDict[str, _HbceAny] | None = None) -> HbceGridObservation:
    """Create a deterministic public-safe observation from normalized agent state."""

    agent_state = agent_state or {}
    grid = agent_state.get("grid", [])
    objects = agent_state.get("objects", [])
    task_id = str(agent_state.get("task_id") or "anonymous-task")

    width, height = _hbce_grid_dimensions(grid)
    uncertainty_markers: _HbceList[str] = []

    if not _hbce_is_grid(grid):
        uncertainty_markers.append("GRID_MISSING_OR_INVALID")
    if width == 0 or height == 0:
        uncertainty_markers.append("GRID_EMPTY")
    if not isinstance(objects, list):
        uncertainty_markers.append("OBJECTS_INVALID")

    safe_objects = [obj for obj in objects if isinstance(obj, dict)] if isinstance(objects, list) else []

    return HbceGridObservation(
        status="OBSERVER_READY",
        task_id=task_id,
        width=width,
        height=height,
        cell_count=width * height,
        symbols=_hbce_symbol_counts(grid),
        non_empty_cells=_hbce_non_empty_cells(grid),
        objects=safe_objects,
        uncertainty_markers=uncertainty_markers,
        metadata={
            "source": "observer_upgrade_v1",
            "has_grid": _hbce_is_grid(grid),
            "object_count": len(safe_objects),
            "public_safe": True,
        },
    )


def observe_task(agent_state: _HbceDict[str, _HbceAny] | None = None) -> _HbceDict[str, _HbceAny]:
    """Compatibility wrapper returning a plain dictionary observation."""

    return observe_agent_state(agent_state).to_dict()


# === HBCE ARC AGI3 OBSERVER UPGRADE v1 END ===
