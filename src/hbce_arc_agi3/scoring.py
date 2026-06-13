"""Scoring utilities for baseline ARC-AGI-3 agent traces."""

from __future__ import annotations

from typing import Any, Dict


def score_plan(plan: Dict[str, Any]) -> Dict[str, Any]:
    actions = plan.get("actions") or []
    score = min(1.0, 0.25 + 0.25 * len(actions))
    return {
        "status": "SCORE_READY",
        "score": score,
        "action_count": len(actions),
        "verified": bool(actions),
    }
