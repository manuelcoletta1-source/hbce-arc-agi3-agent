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
