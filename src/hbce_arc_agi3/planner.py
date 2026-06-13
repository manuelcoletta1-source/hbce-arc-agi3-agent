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


# === HBCE ARC AGI3 PLANNER BASELINE v1 START ===

from dataclasses import asdict as _hbce_planner_asdict
from dataclasses import dataclass as _hbce_planner_dataclass
from typing import Any as _HbcePlannerAny
from typing import Dict as _HbcePlannerDict
from typing import List as _HbcePlannerList


@_hbce_planner_dataclass(frozen=True)
class HbceCandidateAction:
    """Deterministic public-safe candidate action."""

    action_id: str
    action_type: str
    confidence: float
    rationale: str
    payload: _HbcePlannerDict[str, _HbcePlannerAny]

    def to_dict(self) -> _HbcePlannerDict[str, _HbcePlannerAny]:
        return _hbce_planner_asdict(self)


@_hbce_planner_dataclass(frozen=True)
class HbcePlan:
    """Planner baseline output for ARC-AGI-3 public benchmark evidence."""

    status: str
    task_id: str
    goal: str
    candidate_actions: _HbcePlannerList[_HbceCandidateAction]
    selected_action: HbceCandidateAction
    planning_basis: _HbcePlannerDict[str, _HbcePlannerAny]
    metadata: _HbcePlannerDict[str, _HbcePlannerAny]

    def to_dict(self) -> _HbcePlannerDict[str, _HbcePlannerAny]:
        data = _hbce_planner_asdict(self)
        data["candidate_actions"] = [action.to_dict() for action in self.candidate_actions]
        data["selected_action"] = self.selected_action.to_dict()
        return data


def _hbce_world_dimensions(world_model: _HbcePlannerDict[str, _HbcePlannerAny]) -> _HbcePlannerDict[str, int]:
    dimensions = world_model.get("dimensions")
    if not isinstance(dimensions, dict):
        return {"width": 0, "height": 0, "cell_count": 0}

    return {
        "width": int(dimensions.get("width") or 0),
        "height": int(dimensions.get("height") or 0),
        "cell_count": int(dimensions.get("cell_count") or 0),
    }


def _hbce_symbol_inventory(world_model: _HbcePlannerDict[str, _HbcePlannerAny]) -> _HbcePlannerDict[str, int]:
    inventory = world_model.get("symbol_inventory")
    if not isinstance(inventory, dict):
        return {}

    safe_inventory: _HbcePlannerDict[str, int] = {}
    for key, value in inventory.items():
        try:
            safe_inventory[str(key)] = int(value)
        except (TypeError, ValueError):
            safe_inventory[str(key)] = 0

    return dict(sorted(safe_inventory.items()))


def plan_from_world_model(
    world_model: _HbcePlannerDict[str, _HbcePlannerAny] | None = None,
    *,
    goal: str = "solve",
) -> HbcePlan:
    """Create a deterministic baseline plan from the symbolic world model."""

    world_model = world_model or {}
    task_id = str(world_model.get("task_id") or "anonymous-task")
    dimensions = _hbce_world_dimensions(world_model)
    inventory = _hbce_symbol_inventory(world_model)
    density = float(world_model.get("density") or 0.0)
    uncertainty = world_model.get("uncertainty_markers")
    uncertainty_markers = uncertainty if isinstance(uncertainty, list) else []

    candidate_actions: _HbcePlannerList[HbceCandidateAction] = []

    if dimensions["cell_count"] == 0:
        candidate_actions.append(
            HbceCandidateAction(
                action_id="action-000-noop-empty-grid",
                action_type="noop",
                confidence=0.9,
                rationale="Grid dimensions are unknown or empty, so the safe baseline action is noop.",
                payload={"reason": "empty_or_unknown_grid"},
            )
        )
    else:
        candidate_actions.append(
            HbceCandidateAction(
                action_id="action-001-observe-symbols",
                action_type="analyze_symbol_inventory",
                confidence=0.55,
                rationale="Symbol inventory is available and should be used before transformation.",
                payload={"symbol_inventory": inventory},
            )
        )

        if density > 0:
            candidate_actions.append(
                HbceCandidateAction(
                    action_id="action-002-preserve-non-empty-structure",
                    action_type="preserve_non_empty_structure",
                    confidence=0.6,
                    rationale="Non-empty cells are present, so preserving observed structure is the safest baseline.",
                    payload={"density": density},
                )
            )

        if len(inventory) > 1:
            candidate_actions.append(
                HbceCandidateAction(
                    action_id="action-003-compare-symbol-relations",
                    action_type="compare_symbol_relations",
                    confidence=0.5,
                    rationale="Multiple symbols exist, so relation comparison is a valid candidate step.",
                    payload={"symbol_count": len(inventory)},
                )
            )

    if uncertainty_markers:
        candidate_actions.append(
            HbceCandidateAction(
                action_id="action-999-request-more-observation",
                action_type="request_more_observation",
                confidence=0.25,
                rationale="Uncertainty markers are present, so the planner flags incomplete observation.",
                payload={"uncertainty_markers": uncertainty_markers},
            )
        )

    if not candidate_actions:
        candidate_actions.append(
            HbceCandidateAction(
                action_id="action-000-noop-fallback",
                action_type="noop",
                confidence=0.1,
                rationale="Fallback candidate action for missing planning basis.",
                payload={"reason": "fallback"},
            )
        )

    selected_action = sorted(
        candidate_actions,
        key=lambda action: (-action.confidence, action.action_id),
    )[0]

    return HbcePlan(
        status="PLANNER_READY",
        task_id=task_id,
        goal=goal,
        candidate_actions=candidate_actions,
        selected_action=selected_action,
        planning_basis={
            "dimensions": dimensions,
            "symbol_inventory": inventory,
            "density": density,
            "uncertainty_markers": uncertainty_markers,
        },
        metadata={
            "source": "planner_baseline_v1",
            "candidate_count": len(candidate_actions),
            "selected_action_id": selected_action.action_id,
            "public_safe": True,
            "deterministic": True,
        },
    )


def build_plan(
    world_model: _HbcePlannerDict[str, _HbcePlannerAny] | None = None,
    *,
    goal: str = "solve",
) -> _HbcePlannerDict[str, _HbcePlannerAny]:
    """Compatibility wrapper returning a plain dictionary plan."""

    return plan_from_world_model(world_model, goal=goal).to_dict()


# === HBCE ARC AGI3 PLANNER BASELINE v1 END ===
