"""Planner Strategy Expansion v1 for HBCE ARC-AGI-3 public baseline.

This module selects deterministic hypothesis-driven planner strategies from
Rule Hypothesis v1 outputs.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.object_model import build_object_model
from hbce_arc_agi3.rule_hypothesis import (
    RuleHypothesisSet,
    generate_rule_hypotheses,
    validate_rule_hypothesis_set,
)


@dataclass(frozen=True)
class PlannerStrategy:
    status: str
    strategy_id: str
    task_id: str
    selected_rule_type: str
    selected_hypothesis_id: str
    selected_action: str
    confidence: float
    rationale: str
    evidence: Dict[str, Any]
    parameters: Dict[str, Any]
    ranked_hypotheses: List[Dict[str, Any]]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


RULE_TYPE_ACTION_MAP = {
    "preserve_structure": "preserve_non_background_structure",
    "object_count_invariant": "preserve_object_count",
    "dominant_value_focus": "transform_or_preserve_dominant_value",
    "horizontal_symmetry_candidate": "evaluate_horizontal_mirror",
    "vertical_symmetry_candidate": "evaluate_vertical_mirror",
    "largest_object_anchor": "anchor_largest_object_copy_move_expand",
}


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_hypothesis_set(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, RuleHypothesisSet):
        return payload.to_dict()

    if isinstance(payload, dict):
        if payload.get("status") == "RULE_HYPOTHESIS_READY":
            return payload

        if "hypotheses" in payload:
            raise ValueError("Planner strategy requires a valid RULE_HYPOTHESIS_READY payload")

    try:
        return generate_rule_hypotheses(payload).to_dict()
    except ValueError as exc:
        raise ValueError("Planner strategy requires a valid RULE_HYPOTHESIS_READY payload") from exc


def _rank_hypotheses(hypotheses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return sorted(
        hypotheses,
        key=lambda item: (
            -float(item.get("confidence", 0.0)),
            str(item.get("rule_type", "")),
            str(item.get("hypothesis_id", "")),
        ),
    )


def _action_for_rule_type(rule_type: str) -> str:
    return RULE_TYPE_ACTION_MAP.get(rule_type, "evaluate_candidate_rule")


def select_planner_strategy(payload: Any) -> PlannerStrategy:
    """Select a deterministic planner strategy from hypotheses or source payload."""

    hypothesis_set = _coerce_hypothesis_set(payload)
    validation = validate_rule_hypothesis_set(hypothesis_set)

    if validation.get("status") != "RULE_HYPOTHESIS_VALID":
        raise ValueError("Planner strategy requires a valid RULE_HYPOTHESIS_READY payload")

    hypotheses = hypothesis_set.get("hypotheses", [])
    if not isinstance(hypotheses, list) or not hypotheses:
        raise ValueError("Planner strategy requires at least one hypothesis")

    ranked = _rank_hypotheses(hypotheses)
    selected = ranked[0]

    rule_type = str(selected.get("rule_type"))
    selected_action = _action_for_rule_type(rule_type)
    task_id = str(hypothesis_set.get("task_id") or "anonymous-task")
    confidence = round(float(selected.get("confidence", 0.0)), 6)

    strategy_basis = {
        "task_id": task_id,
        "selected_hypothesis_id": selected.get("hypothesis_id"),
        "selected_rule_type": rule_type,
        "selected_action": selected_action,
        "confidence": confidence,
        "object_model_signature": hypothesis_set.get("object_model_signature"),
    }
    signature = _stable_signature(strategy_basis)

    return PlannerStrategy(
        status="PLANNER_STRATEGY_READY",
        strategy_id=f"PS-{signature[:12]}",
        task_id=task_id,
        selected_rule_type=rule_type,
        selected_hypothesis_id=str(selected.get("hypothesis_id")),
        selected_action=selected_action,
        confidence=confidence,
        rationale=str(selected.get("description") or "Selected highest-confidence deterministic rule hypothesis."),
        evidence=selected.get("evidence") if isinstance(selected.get("evidence"), dict) else {},
        parameters=selected.get("parameters") if isinstance(selected.get("parameters"), dict) else {},
        ranked_hypotheses=[
            {
                "rank": index + 1,
                "hypothesis_id": str(item.get("hypothesis_id")),
                "rule_type": str(item.get("rule_type")),
                "confidence": round(float(item.get("confidence", 0.0)), 6),
                "selected": index == 0,
            }
            for index, item in enumerate(ranked)
        ],
        metadata={
            "source": "planner_strategy_expansion_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "uses_rule_hypothesis": True,
            "uses_object_model": True,
            "strategy_signature": signature,
        },
    )


def validate_planner_strategy(strategy: PlannerStrategy | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Planner Strategy Expansion v1 public contract."""

    data = strategy.to_dict() if isinstance(strategy, PlannerStrategy) else dict(strategy)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "PLANNER_STRATEGY_READY",
        "strategy_id_present": bool(data.get("strategy_id")),
        "task_id_present": bool(data.get("task_id")),
        "selected_rule_type_present": bool(data.get("selected_rule_type")),
        "selected_hypothesis_id_present": bool(data.get("selected_hypothesis_id")),
        "selected_action_present": bool(data.get("selected_action")),
        "confidence_number": isinstance(data.get("confidence"), float),
        "ranked_hypotheses_list": isinstance(data.get("ranked_hypotheses"), list),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "uses_rule_hypothesis_true": metadata.get("uses_rule_hypothesis") is True,
        "uses_object_model_true": metadata.get("uses_object_model") is True,
    }

    valid = all(checks.values())

    return {
        "status": "PLANNER_STRATEGY_VALID" if valid else "PLANNER_STRATEGY_INVALID",
        "valid": valid,
        "checks": checks,
        "strategy_id": data.get("strategy_id"),
        "selected_action": data.get("selected_action"),
        "selected_rule_type": data.get("selected_rule_type"),
        "metadata": {
            "source": "planner_strategy_expansion_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def build_strategy_from_grid_payload(payload: Any) -> Dict[str, Any]:
    """Build object model, rule hypotheses, and selected planner strategy."""

    object_model = build_object_model(payload)
    hypotheses = generate_rule_hypotheses(object_model)
    strategy = select_planner_strategy(hypotheses)
    validation = validate_planner_strategy(strategy)

    return {
        "status": "PLANNER_STRATEGY_PIPELINE_READY",
        "object_model": object_model.to_dict(),
        "rule_hypotheses": hypotheses.to_dict(),
        "planner_strategy": strategy.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "planner_strategy_expansion_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
        },
    }
