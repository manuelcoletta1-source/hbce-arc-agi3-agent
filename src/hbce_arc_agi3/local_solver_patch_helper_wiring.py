"""Local solver patch helper wiring adapters.

This module is dry-run only. It adapts diagnostic records to the helper
functions created in Milestone #11 Task 10 without mutating runtime solver
or ranker behavior.
"""

from __future__ import annotations

import hashlib
import json
from typing import Any, Callable, Dict, Iterable, Mapping, Tuple

from hbce_arc_agi3.solver_patch_helpers import (
    build_action_policy_validity_guard_hints,
    build_goal_inference_terminal_state_hints,
    build_planner_loop_recovery_hints,
    build_transition_verifier_feedback_hints,
    build_world_model_state_tracking_hints,
)


LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1"
LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS = "LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_READY"
LOCAL_SOLVER_PATCH_HELPER_WIRING_SCOPE = "DRY_RUN_ONLY_NO_RUNTIME_SOLVER_MUTATION"
LOCAL_SOLVER_PATCH_HELPER_WIRING_SCORE_SEMANTICS = "NOT_A_KAGGLE_SCORE"


AdapterFunction = Callable[[Iterable[Mapping[str, Any]] | None], Tuple[Dict[str, Any], ...]]


def _records(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Mapping[str, Any], ...]:
    if records is None:
        return tuple()
    return tuple(record for record in records if isinstance(record, Mapping))


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _decorate_hint(adapter_name: str, target_layer: str, hint: Mapping[str, Any]) -> Dict[str, Any]:
    payload = dict(hint)
    payload.update(
        {
            "adapter_name": adapter_name,
            "adapter_target_layer": target_layer,
            "wiring_dry_run": True,
            "adapter_status": "DRY_RUN_PASS",
            "diagnostic_only": True,
            "kaggle_score_semantics": LOCAL_SOLVER_PATCH_HELPER_WIRING_SCORE_SEMANTICS,
            "score_claim_allowed": False,
            "submission_artifact_allowed": False,
            "runtime_solver_modified": False,
            "ranker_runtime_modified": False,
            "external_solver_dependency": False,
            "legal_certification": False,
        }
    )
    payload["adapter_signature"] = _stable_signature(payload)
    return payload


def world_model_state_tracking_adapter(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    return tuple(
        _decorate_hint("world_model_state_tracking_adapter", "world_model", hint)
        for hint in build_world_model_state_tracking_hints(_records(records))
    )


def goal_inference_terminal_state_adapter(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    return tuple(
        _decorate_hint("goal_inference_terminal_state_adapter", "goal_inference", hint)
        for hint in build_goal_inference_terminal_state_hints(_records(records))
    )


def planner_loop_recovery_adapter(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    return tuple(
        _decorate_hint("planner_loop_recovery_adapter", "planner", hint)
        for hint in build_planner_loop_recovery_hints(_records(records))
    )


def transition_verifier_feedback_adapter(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    return tuple(
        _decorate_hint("transition_verifier_feedback_adapter", "verifier", hint)
        for hint in build_transition_verifier_feedback_hints(_records(records))
    )


def action_policy_validity_guard_adapter(records: Iterable[Mapping[str, Any]] | None) -> Tuple[Dict[str, Any], ...]:
    return tuple(
        _decorate_hint("action_policy_validity_guard_adapter", "action_policy", hint)
        for hint in build_action_policy_validity_guard_hints(_records(records))
    )


ADAPTERS: Tuple[Tuple[str, str, AdapterFunction], ...] = (
    ("world_model", "world_model_state_tracking_adapter", world_model_state_tracking_adapter),
    ("goal_inference", "goal_inference_terminal_state_adapter", goal_inference_terminal_state_adapter),
    ("planner", "planner_loop_recovery_adapter", planner_loop_recovery_adapter),
    ("verifier", "transition_verifier_feedback_adapter", transition_verifier_feedback_adapter),
    ("action_policy", "action_policy_validity_guard_adapter", action_policy_validity_guard_adapter),
)


def run_local_solver_patch_helper_wiring_dry_run(
    records: Iterable[Mapping[str, Any]] | None,
) -> Dict[str, Any]:
    rows = _records(records)
    adapter_outputs: Dict[str, Tuple[Dict[str, Any], ...]] = {}
    layer_summary = []

    for target_layer, adapter_name, adapter_fn in ADAPTERS:
        output = adapter_fn(rows)
        adapter_outputs[target_layer] = output
        failure_count = sum(1 for item in output if item.get("adapter_status") != "DRY_RUN_PASS")
        layer_summary.append(
            {
                "target_layer": target_layer,
                "adapter_name": adapter_name,
                "output_count": len(output),
                "pass_count": len(output) - failure_count,
                "failure_count": failure_count,
                "dry_run_passed": bool(output) and failure_count == 0,
                "runtime_solver_modified": False,
                "ranker_runtime_modified": False,
                "external_solver_dependency": False,
                "diagnostic_only": True,
                "kaggle_score_semantics": LOCAL_SOLVER_PATCH_HELPER_WIRING_SCORE_SEMANTICS,
                "score_claim_allowed": False,
            }
        )

    flat_outputs = tuple(item for output in adapter_outputs.values() for item in output)

    bundle = {
        "revision": LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION,
        "status": LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
        "scope": LOCAL_SOLVER_PATCH_HELPER_WIRING_SCOPE,
        "record_count": len(rows),
        "adapter_count": len(ADAPTERS),
        "adapter_outputs": {key: list(value) for key, value in adapter_outputs.items()},
        "layer_summary": layer_summary,
        "dry_run_output_count": len(flat_outputs),
        "dry_run_pass_count": sum(1 for item in flat_outputs if item.get("adapter_status") == "DRY_RUN_PASS"),
        "dry_run_failure_count": sum(1 for item in flat_outputs if item.get("adapter_status") != "DRY_RUN_PASS"),
        "wiring_dry_run": True,
        "wiring_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": LOCAL_SOLVER_PATCH_HELPER_WIRING_SCORE_SEMANTICS,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "legal_certification": False,
    }
    bundle["dry_run_id"] = f"M11-LOCAL-WIRING-DRY-RUN-{_stable_signature(bundle)[:12]}"
    return bundle
