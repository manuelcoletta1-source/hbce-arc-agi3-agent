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


# === HBCE ARC AGI3 VERIFICATION SCORING v1 START ===

from dataclasses import asdict as _hbce_score_asdict
from dataclasses import dataclass as _hbce_score_dataclass
from typing import Any as _HbceScoreAny
from typing import Dict as _HbceScoreDict
from typing import List as _HbceScoreList


@_hbce_score_dataclass(frozen=True)
class HbceVerificationResult:
    """Public-safe verification result for planner output."""

    status: str
    verified: bool
    reason: str
    checks: _HbceScoreDict[str, bool]
    selected_action: _HbceScoreDict[str, _HbceScoreAny]
    metadata: _HbceScoreDict[str, _HbceScoreAny]

    def to_dict(self) -> _HbceScoreDict[str, _HbceScoreAny]:
        return _hbce_score_asdict(self)


@_hbce_score_dataclass(frozen=True)
class HbceScoreResult:
    """Public-safe score result for verified planner output."""

    status: str
    score: float
    grade: str
    reason: str
    components: _HbceScoreDict[str, float]
    metadata: _HbceScoreDict[str, _HbceScoreAny]

    def to_dict(self) -> _HbceScoreDict[str, _HbceScoreAny]:
        return _hbce_score_asdict(self)


def _hbce_selected_action(plan: _HbceScoreDict[str, _HbceScoreAny]) -> _HbceScoreDict[str, _HbceScoreAny]:
    selected = plan.get("selected_action")
    return selected if isinstance(selected, dict) else {}


def _hbce_candidate_actions(plan: _HbceScoreDict[str, _HbceScoreAny]) -> _HbceScoreList[_HbceScoreDict[str, _HbceScoreAny]]:
    candidates = plan.get("candidate_actions")
    if not isinstance(candidates, list):
        return []

    return [candidate for candidate in candidates if isinstance(candidate, dict)]


def verify_plan_output(
    plan: _HbceScoreDict[str, _HbceScoreAny] | None = None,
    world_model: _HbceScoreDict[str, _HbceScoreAny] | None = None,
) -> HbceVerificationResult:
    """Verify deterministic planner output against a symbolic world model."""

    plan = plan or {}
    world_model = world_model or {}

    selected = _hbce_selected_action(plan)
    candidates = _hbce_candidate_actions(plan)
    candidate_ids = {str(candidate.get("action_id")) for candidate in candidates}

    selected_action_id = str(selected.get("action_id") or "")
    selected_action_type = str(selected.get("action_type") or "")

    dimensions = world_model.get("dimensions")
    has_dimensions = isinstance(dimensions, dict) and int(dimensions.get("cell_count") or 0) >= 0

    checks = {
        "plan_status_ready": plan.get("status") == "PLANNER_READY",
        "selected_action_present": bool(selected),
        "selected_action_has_id": bool(selected_action_id),
        "selected_action_has_type": bool(selected_action_type),
        "selected_action_in_candidates": bool(selected_action_id and selected_action_id in candidate_ids),
        "world_model_status_ready": world_model.get("status") == "WORLD_MODEL_READY",
        "world_model_dimensions_present": has_dimensions,
        "planner_public_safe": bool(plan.get("metadata", {}).get("public_safe")) if isinstance(plan.get("metadata"), dict) else False,
        "planner_deterministic": bool(plan.get("metadata", {}).get("deterministic")) if isinstance(plan.get("metadata"), dict) else False,
    }

    verified = all(checks.values())

    if verified:
        reason = "planner_output_verified_against_world_model"
        status = "VERIFICATION_READY"
    else:
        failed = [name for name, passed in checks.items() if not passed]
        reason = "verification_failed:" + ",".join(failed)
        status = "VERIFICATION_FAILED"

    return HbceVerificationResult(
        status=status,
        verified=verified,
        reason=reason,
        checks=checks,
        selected_action=selected,
        metadata={
            "source": "verification_scoring_v1",
            "candidate_count": len(candidates),
            "public_safe": True,
            "external_api_dependency": False,
        },
    )


def score_verified_plan(
    verification: HbceVerificationResult | _HbceScoreDict[str, _HbceScoreAny],
    plan: _HbceScoreDict[str, _HbceScoreAny] | None = None,
) -> HbceScoreResult:
    """Score a verified planner result using deterministic public-safe components."""

    plan = plan or {}

    verification_dict = (
        verification.to_dict()
        if isinstance(verification, HbceVerificationResult)
        else verification
    )

    verified = bool(verification_dict.get("verified"))
    selected = _hbce_selected_action(plan)

    try:
        confidence = float(selected.get("confidence") or 0.0)
    except (TypeError, ValueError):
        confidence = 0.0

    checks = verification_dict.get("checks")
    checks = checks if isinstance(checks, dict) else {}
    check_values = [bool(value) for value in checks.values()]
    verification_ratio = (
        sum(1 for value in check_values if value) / len(check_values)
        if check_values
        else 0.0
    )

    determinism_component = 1.0 if isinstance(plan.get("metadata"), dict) and plan["metadata"].get("deterministic") else 0.0
    public_safety_component = 1.0 if isinstance(plan.get("metadata"), dict) and plan["metadata"].get("public_safe") else 0.0

    if verified:
        raw_score = (0.45 * verification_ratio) + (0.35 * confidence) + (0.10 * determinism_component) + (0.10 * public_safety_component)
    else:
        raw_score = 0.25 * verification_ratio

    score = round(max(0.0, min(1.0, raw_score)), 6)

    if score >= 0.85:
        grade = "A"
    elif score >= 0.65:
        grade = "B"
    elif score >= 0.40:
        grade = "C"
    else:
        grade = "D"

    return HbceScoreResult(
        status="SCORING_READY",
        score=score,
        grade=grade,
        reason="verified_plan_scored" if verified else "unverified_plan_scored_with_penalty",
        components={
            "verification_ratio": round(verification_ratio, 6),
            "selected_action_confidence": round(confidence, 6),
            "determinism_component": determinism_component,
            "public_safety_component": public_safety_component,
        },
        metadata={
            "source": "verification_scoring_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    )


def verify_and_score_plan(
    plan: _HbceScoreDict[str, _HbceScoreAny] | None = None,
    world_model: _HbceScoreDict[str, _HbceScoreAny] | None = None,
) -> _HbceScoreDict[str, _HbceScoreAny]:
    """Compatibility wrapper returning verification and score dictionaries."""

    verification = verify_plan_output(plan, world_model)
    score = score_verified_plan(verification, plan or {})

    return {
        "status": "VERIFICATION_SCORING_READY",
        "verification": verification.to_dict(),
        "score": score.to_dict(),
        "metadata": {
            "source": "verification_scoring_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


# === HBCE ARC AGI3 VERIFICATION SCORING v1 END ===
