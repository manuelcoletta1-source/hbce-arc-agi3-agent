"""Local solver patch helper utilities."""

# === MILESTONE 11 LOCAL SOLVER PATCH HELPERS v1 START ===

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, Iterable, Mapping, Tuple


M11_SOLVER_PATCH_HELPERS_REVISION = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1"
M11_SOLVER_PATCH_HELPERS_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_READY"
M11_SOLVER_PATCH_HELPERS_SCOPE = "PATCH_HELPERS_ONLY_NO_RUNTIME_SOLVER_PATCH"
M11_SOLVER_PATCH_HELPERS_KAGGLE_SCORE_SEMANTICS = "NOT_A_KAGGLE_SCORE"


def _m11_stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _m11_records(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Mapping[str, Any], ...]:
    if records is None:
        return tuple()
    return tuple(item for item in records if isinstance(item, Mapping))


def _m11_hint_id(prefix: str, payload: Mapping[str, Any]) -> str:
    return f"{prefix}-{_m11_stable_signature(payload)[:12]}"


def _m11_boundary() -> Dict[str, Any]:
    return {
        "diagnostic_only": True,
        "kaggle_score_semantics": M11_SOLVER_PATCH_HELPERS_KAGGLE_SCORE_SEMANTICS,
        "score_claim_allowed": False,
        "submission_artifact_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "legal_certification": False,
    }


def build_world_model_state_tracking_hints(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    """Build local diagnostic world-model state tracking hints.

    This helper does not patch the runtime solver. It converts diagnostic records
    into conservative state-transition hints.
    """

    hints = []
    for record in _m11_records(records):
        payload = {
            "fixture_id": record.get("fixture_id", "UNKNOWN_FIXTURE"),
            "episode_id": record.get("episode_id", "UNKNOWN_EPISODE"),
            "initial_signature": record.get("initial_signature") or record.get("initial_state_signature"),
            "final_signature": record.get("final_signature") or record.get("final_state_signature"),
            "goal_signature": record.get("goal_signature"),
        }
        hint = {
            "hint_id": _m11_hint_id("WM-HINT", payload),
            "target_layer": "world_model",
            "hint_type": "state_tracking",
            "state_transition_observed": bool(payload["initial_signature"] and payload["final_signature"]),
            "confidence": 1.0 if payload["initial_signature"] and payload["final_signature"] else 0.0,
            **payload,
            **_m11_boundary(),
        }
        hints.append(hint)
    return tuple(hints)


def build_goal_inference_terminal_state_hints(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    """Build local diagnostic goal inference hints from terminal states."""

    hints = []
    for record in _m11_records(records):
        payload = {
            "fixture_id": record.get("fixture_id", "UNKNOWN_FIXTURE"),
            "episode_id": record.get("episode_id", "UNKNOWN_EPISODE"),
            "goal_reached": bool(record.get("goal_reached", False)),
            "goal_signature": record.get("goal_signature"),
            "final_signature": record.get("final_signature") or record.get("final_state_signature"),
        }
        hint = {
            "hint_id": _m11_hint_id("GI-HINT", payload),
            "target_layer": "goal_inference",
            "hint_type": "terminal_state_goal_inference",
            "goal_signal_present": bool(payload["goal_reached"] or payload["goal_signature"]),
            "confidence": 1.0 if payload["goal_reached"] else 0.5 if payload["goal_signature"] else 0.0,
            **payload,
            **_m11_boundary(),
        }
        hints.append(hint)
    return tuple(hints)


def build_planner_loop_recovery_hints(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    """Build local diagnostic planner loop recovery hints."""

    hints = []
    for record in _m11_records(records):
        trace = record.get("trace", [])
        actions = tuple(step.get("action", "UNKNOWN") for step in trace if isinstance(step, Mapping))
        repeated_action_count = max((actions.count(action) for action in set(actions)), default=0)
        loop_risk = repeated_action_count >= 3 and bool(actions)

        payload = {
            "fixture_id": record.get("fixture_id", "UNKNOWN_FIXTURE"),
            "episode_id": record.get("episode_id", "UNKNOWN_EPISODE"),
            "step_count": int(record.get("step_count", len(actions)) or 0),
            "action_sequence": list(actions),
            "loop_risk_detected": loop_risk,
        }
        hint = {
            "hint_id": _m11_hint_id("PLANNER-HINT", payload),
            "target_layer": "planner",
            "hint_type": "loop_recovery",
            "fallback_required": loop_risk,
            "confidence": 1.0 if loop_risk else 0.75 if actions else 0.0,
            **payload,
            **_m11_boundary(),
        }
        hints.append(hint)
    return tuple(hints)


def build_transition_verifier_feedback_hints(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    """Build local diagnostic transition verifier feedback hints."""

    hints = []
    for record in _m11_records(records):
        trace = record.get("trace", [])
        verifier_values = tuple(
            step.get("verifier_match")
            for step in trace
            if isinstance(step, Mapping) and "verifier_match" in step
        )
        mismatch_count = sum(1 for item in verifier_values if item is False)
        match_count = sum(1 for item in verifier_values if item is True)

        payload = {
            "fixture_id": record.get("fixture_id", "UNKNOWN_FIXTURE"),
            "episode_id": record.get("episode_id", "UNKNOWN_EPISODE"),
            "verifier_match_count": match_count,
            "verifier_mismatch_count": mismatch_count,
            "transition_check_count": len(verifier_values),
        }
        hint = {
            "hint_id": _m11_hint_id("VERIFIER-HINT", payload),
            "target_layer": "verifier",
            "hint_type": "transition_feedback",
            "verifier_feedback_required": mismatch_count > 0,
            "confidence": 1.0 if verifier_values else 0.0,
            **payload,
            **_m11_boundary(),
        }
        hints.append(hint)
    return tuple(hints)


def build_action_policy_validity_guard_hints(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    """Build local diagnostic action-policy validity guard hints."""

    allowed_actions = {"UP", "DOWN", "LEFT", "RIGHT", "STAY", "VERIFY"}
    hints = []
    for record in _m11_records(records):
        trace = record.get("trace", [])
        actions = tuple(step.get("action", "UNKNOWN") for step in trace if isinstance(step, Mapping))
        invalid_actions = tuple(action for action in actions if action not in allowed_actions)

        payload = {
            "fixture_id": record.get("fixture_id", "UNKNOWN_FIXTURE"),
            "episode_id": record.get("episode_id", "UNKNOWN_EPISODE"),
            "action_sequence": list(actions),
            "invalid_actions": list(invalid_actions),
            "allowed_actions": sorted(allowed_actions),
        }
        hint = {
            "hint_id": _m11_hint_id("ACTION-HINT", payload),
            "target_layer": "action_policy",
            "hint_type": "action_validity_guard",
            "action_policy_valid": len(invalid_actions) == 0,
            "confidence": 1.0 if actions and not invalid_actions else 0.0,
            **payload,
            **_m11_boundary(),
        }
        hints.append(hint)
    return tuple(hints)


def build_solver_patch_helper_bundle(records: Iterable[Mapping[str, Any]] | None) -> Dict[str, Any]:
    """Build all Milestone 11 local patch helper hints.

    The bundle is deterministic and diagnostic-only. It is not a Kaggle score and
    does not modify solver or ranker runtime behavior.
    """

    rows = _m11_records(records)
    bundle = {
        "revision": M11_SOLVER_PATCH_HELPERS_REVISION,
        "status": M11_SOLVER_PATCH_HELPERS_STATUS,
        "scope": M11_SOLVER_PATCH_HELPERS_SCOPE,
        "record_count": len(rows),
        "world_model_hints": list(build_world_model_state_tracking_hints(rows)),
        "goal_inference_hints": list(build_goal_inference_terminal_state_hints(rows)),
        "planner_hints": list(build_planner_loop_recovery_hints(rows)),
        "transition_verifier_hints": list(build_transition_verifier_feedback_hints(rows)),
        "action_policy_hints": list(build_action_policy_validity_guard_hints(rows)),
        "diagnostic_only": True,
        "kaggle_score_semantics": M11_SOLVER_PATCH_HELPERS_KAGGLE_SCORE_SEMANTICS,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "legal_certification": False,
    }
    bundle["bundle_id"] = f"M11-SOLVER-PATCH-HELPER-BUNDLE-{_m11_stable_signature(bundle)[:12]}"
    return bundle


# === MILESTONE 11 LOCAL SOLVER PATCH HELPERS v1 END ===
