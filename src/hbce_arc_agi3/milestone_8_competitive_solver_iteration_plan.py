"""Milestone #8 Competitive Solver Iteration Plan v2.

Local-only competitive solver iteration plan.

This module opens Milestone #8 after the Milestone #7 final competitive
readiness audit. It converts the previous audit verdict into a bounded solver
iteration plan. It does not submit to Kaggle, authenticate, upload files, call
external APIs, read secrets, create a real submission, claim a Kaggle score,
claim public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PLAN_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_READY"
PIPELINE_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_VALID"

BASELINE_COMMIT = "4c6e68d Add ARC AGI3 final competitive readiness audit"
PLAN_MODE = "COMPETITIVE_SOLVER_ITERATION_PLAN_ONLY_NO_UPLOAD"
PLAN_SCOPE = "OPEN_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_FROM_FINAL_AUDIT"
PLAN_VERDICT = "COMPETITIVE_SOLVER_ITERATION_PLAN_READY_FOR_SOLVER_KERNEL_V2"
NEXT_ALLOWED_STAGE = "MILESTONE_8_TASK_2_COMPETITIVE_SOLVER_KERNEL_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-8/competitive-solver-iteration-plan-v2"

FINAL_AUDIT_JSON = Path(
    "examples/milestone-7/final-competitive-readiness-audit-v1/"
    "milestone-7-final-competitive-readiness-audit-v1.json"
)

EXPECTED_AUDIT_GATE_COUNT = 57
EXPECTED_AUDIT_ISSUE_COUNT = 0
EXPECTED_BLOCKER_COUNT = 6
EXPECTED_READINESS_DIMENSION_COUNT = 7
EXPECTED_ITERATION_FAMILY_COUNT = 4
EXPECTED_SOLVER_ITERATION_COUNT = 8
EXPECTED_BENCHMARK_TARGET_COUNT = 8
EXPECTED_REGRESSION_GUARD_COUNT = 8
EXPECTED_CONTROL_COUNT = 10
EXPECTED_PLAN_SECTION_COUNT = 8
EXPECTED_TASK_QUEUE_COUNT = 5


ITERATION_FAMILIES: Tuple[Dict[str, Any], ...] = (
    {
        "family_id": "milestone_8_color_mapping_solver_v2",
        "priority": "P0",
        "source_family": "color_mapping",
        "objective": "Improve palette transfer, background preservation, and bounded recoloring decisions.",
        "risk": "False color remapping or background corruption.",
        "ready_for_kernel_v2": True,
    },
    {
        "family_id": "milestone_8_object_model_solver_v2",
        "priority": "P0",
        "source_family": "object_model",
        "objective": "Improve component counting, object delta tracking, and local spatial transformations.",
        "risk": "Object loss, object duplication, or unstable spatial movement.",
        "ready_for_kernel_v2": True,
    },
    {
        "family_id": "milestone_8_shape_symmetry_solver_v2",
        "priority": "P0",
        "source_family": "shape_symmetry",
        "objective": "Improve axis symmetry, reflection, translation bounds, and shape-preserving operations.",
        "risk": "Shape deformation or invalid symmetry generalization.",
        "ready_for_kernel_v2": True,
    },
    {
        "family_id": "milestone_8_cross_family_composition_solver_v2",
        "priority": "P0",
        "source_family": "cross_family_composition",
        "objective": "Combine color, object, and shape evidence without breaking deterministic ranking.",
        "risk": "Over-composition, noisy candidate explosion, or ranker instability.",
        "ready_for_kernel_v2": True,
    },
)


SOLVER_ITERATIONS: Tuple[Dict[str, Any], ...] = (
    {
        "iteration_id": "solver_v2_color_palette_transfer",
        "family": "color_mapping",
        "iteration_type": "COLOR_TRANSFER",
        "expected_effect": "Stronger palette mapping candidates.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_color_background_guard",
        "family": "color_mapping",
        "iteration_type": "BACKGROUND_PRESERVATION",
        "expected_effect": "Lower background corruption.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_object_component_delta",
        "family": "object_model",
        "iteration_type": "OBJECT_COMPONENT_DELTA",
        "expected_effect": "Better component-count transformations.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_object_spatial_transform",
        "family": "object_model",
        "iteration_type": "OBJECT_SPATIAL_TRANSFORM",
        "expected_effect": "Better object movement and displacement candidates.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_shape_axis_reflection",
        "family": "shape_symmetry",
        "iteration_type": "AXIS_REFLECTION",
        "expected_effect": "Better reflection and symmetry candidates.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_shape_translation_bounds",
        "family": "shape_symmetry",
        "iteration_type": "TRANSLATION_BOUNDS",
        "expected_effect": "Safer bounded geometric transforms.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_cross_family_candidate_merge",
        "family": "cross_family_composition",
        "iteration_type": "CANDIDATE_MERGE",
        "expected_effect": "Combine family candidates without candidate explosion.",
        "runtime_solver_target": True,
    },
    {
        "iteration_id": "solver_v2_cross_family_ranker_signal",
        "family": "cross_family_composition",
        "iteration_type": "RANKER_SIGNAL_COMPOSITION",
        "expected_effect": "Improve deterministic ranker scoring across families.",
        "runtime_solver_target": True,
    },
)


BENCHMARK_TARGETS: Tuple[str, ...] = (
    "benchmark_color_palette_transfer_v2",
    "benchmark_color_background_guard_v2",
    "benchmark_object_component_delta_v2",
    "benchmark_object_spatial_transform_v2",
    "benchmark_shape_axis_reflection_v2",
    "benchmark_shape_translation_bounds_v2",
    "benchmark_cross_family_candidate_merge_v2",
    "benchmark_cross_family_ranker_signal_v2",
)


REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_no_background_corruption_v2",
    "guard_no_object_loss_v2",
    "guard_no_object_duplication_v2",
    "guard_no_shape_deformation_v2",
    "guard_no_unbounded_translation_v2",
    "guard_no_candidate_explosion_v2",
    "guard_no_ranker_tie_instability_v2",
    "guard_no_real_submission_side_effect_v2",
)


CONTROL_FLAGS: Tuple[str, ...] = (
    "local_only",
    "dry_run_only",
    "deterministic",
    "public_safe",
    "no_kaggle_auth",
    "no_upload",
    "no_external_api",
    "no_private_core",
    "no_legal_certification",
    "no_score_claim",
)


PLAN_SECTIONS: Tuple[str, ...] = (
    "baseline_audit",
    "iteration_families",
    "solver_iteration_queue",
    "benchmark_targets",
    "regression_guards",
    "submission_boundary",
    "task_queue",
    "next_stage",
)


TASK_QUEUE: Tuple[Dict[str, Any], ...] = (
    {
        "task": "Milestone #8 Task 2",
        "name": "Competitive Solver Kernel v2",
        "purpose": "Implement local deterministic solver kernel improvements.",
        "commit_expected": True,
    },
    {
        "task": "Milestone #8 Task 3",
        "name": "Family Benchmark Cases v2",
        "purpose": "Create local benchmark fixtures for v2 solver families.",
        "commit_expected": True,
    },
    {
        "task": "Milestone #8 Task 4",
        "name": "Candidate Generator Runtime Upgrade v2",
        "purpose": "Wire v2 solver outputs into candidate generation.",
        "commit_expected": True,
    },
    {
        "task": "Milestone #8 Task 5",
        "name": "Ranker Runtime Upgrade v2",
        "purpose": "Improve ranking using v2 cross-family evidence.",
        "commit_expected": True,
    },
    {
        "task": "Milestone #8 Task 6",
        "name": "Milestone 8 Regression Benchmark v2",
        "purpose": "Measure v2 solver behavior without submission claims.",
        "commit_expected": True,
    },
)


PLAN_GATES: Tuple[str, ...] = (
    "audit_artifact_present",
    "audit_artifact_ready",
    "audit_artifact_valid",
    "audit_next_stage_matches_milestone_8",
    "audit_real_submission_blocked",
    "audit_solver_iteration_required",
    "plan_mode_valid",
    "plan_scope_valid",
    "plan_verdict_valid",
    "plan_ready",
    "plan_locked",
    "iteration_family_count_valid",
    "solver_iteration_count_valid",
    "benchmark_target_count_valid",
    "regression_guard_count_valid",
    "control_count_valid",
    "plan_section_count_valid",
    "task_queue_count_valid",
    "all_families_priority_p0",
    "all_families_ready_for_kernel_v2",
    "all_solver_iterations_runtime_targeted",
    "benchmark_targets_present",
    "regression_guards_present",
    "task_queue_commit_expected",
    "next_stage_valid",
    "local_only",
    "dry_run_only",
    "deterministic",
    "public_safe",
    "runtime_solver_iteration_required",
    "real_submission_not_created",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "score_claim_absent",
    "public_leaderboard_claim_absent",
)

PLAN_ISSUES: Tuple[str, ...] = (
    "audit_artifact_missing",
    "audit_artifact_not_ready",
    "audit_artifact_invalid",
    "audit_next_stage_mismatch",
    "audit_real_submission_not_blocked",
    "audit_solver_iteration_not_required",
    "plan_mode_invalid",
    "plan_scope_invalid",
    "plan_verdict_invalid",
    "plan_not_ready",
    "plan_not_locked",
    "iteration_family_count_invalid",
    "solver_iteration_count_invalid",
    "benchmark_target_count_invalid",
    "regression_guard_count_invalid",
    "control_count_invalid",
    "plan_section_count_invalid",
    "task_queue_count_invalid",
    "family_priority_not_p0",
    "family_not_ready_for_kernel_v2",
    "solver_iteration_not_runtime_targeted",
    "benchmark_targets_missing",
    "regression_guards_missing",
    "task_queue_commit_not_expected",
    "next_stage_invalid",
    "local_only_false",
    "dry_run_only_false",
    "deterministic_false",
    "public_safe_false",
    "runtime_solver_iteration_not_required",
    "real_submission_created",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "score_claim_detected",
    "public_leaderboard_claim_detected",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _sha256(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _sha16(value: str) -> str:
    return value[:16].upper() if value != "MISSING_HASH" else value


def _boundary_from_audit(audit: Mapping[str, Any]) -> Dict[str, Any]:
    source = audit.get("boundary", {}) if isinstance(audit.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": audit.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def build_milestone_8_competitive_solver_iteration_plan() -> Dict[str, Any]:
    audit = _read_json(FINAL_AUDIT_JSON)
    boundary = _boundary_from_audit(audit)

    plan_record = {
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "plan_ready": True,
        "plan_locked": True,
        "baseline_audit_id": audit.get("audit_id", "MISSING_AUDIT_ID"),
        "audit_ready": audit.get("audit_ready") is True,
        "audit_real_submission_readiness": audit.get("real_submission_readiness", "MISSING"),
        "audit_real_submission_decision": audit.get("real_submission_decision", "MISSING"),
        "audit_solver_iteration_required": audit.get("solver_iteration_required") is True,
        "iteration_family_count": len(ITERATION_FAMILIES),
        "solver_iteration_count": len(SOLVER_ITERATIONS),
        "benchmark_target_count": len(BENCHMARK_TARGETS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "control_count": len(CONTROL_FLAGS),
        "plan_section_count": len(PLAN_SECTIONS),
        "task_queue_count": len(TASK_QUEUE),
        "runtime_solver_iteration_required": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
    }

    gate_state = {
        "audit_artifact_present": FINAL_AUDIT_JSON.exists(),
        "audit_artifact_ready": audit.get("status") == "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_READY",
        "audit_artifact_valid": bool(audit.get("audit_id")) and bool(audit.get("signature")),
        "audit_next_stage_matches_milestone_8": audit.get("next_allowed_stage") == "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_V2",
        "audit_real_submission_blocked": audit.get("real_submission_readiness") == "BLOCKED",
        "audit_solver_iteration_required": audit.get("solver_iteration_required") is True,
        "plan_mode_valid": PLAN_MODE == "COMPETITIVE_SOLVER_ITERATION_PLAN_ONLY_NO_UPLOAD",
        "plan_scope_valid": PLAN_SCOPE == "OPEN_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_FROM_FINAL_AUDIT",
        "plan_verdict_valid": PLAN_VERDICT == "COMPETITIVE_SOLVER_ITERATION_PLAN_READY_FOR_SOLVER_KERNEL_V2",
        "plan_ready": plan_record["plan_ready"] is True,
        "plan_locked": plan_record["plan_locked"] is True,
        "iteration_family_count_valid": len(ITERATION_FAMILIES) == EXPECTED_ITERATION_FAMILY_COUNT,
        "solver_iteration_count_valid": len(SOLVER_ITERATIONS) == EXPECTED_SOLVER_ITERATION_COUNT,
        "benchmark_target_count_valid": len(BENCHMARK_TARGETS) == EXPECTED_BENCHMARK_TARGET_COUNT,
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "control_count_valid": len(CONTROL_FLAGS) == EXPECTED_CONTROL_COUNT,
        "plan_section_count_valid": len(PLAN_SECTIONS) == EXPECTED_PLAN_SECTION_COUNT,
        "task_queue_count_valid": len(TASK_QUEUE) == EXPECTED_TASK_QUEUE_COUNT,
        "all_families_priority_p0": all(item["priority"] == "P0" for item in ITERATION_FAMILIES),
        "all_families_ready_for_kernel_v2": all(item["ready_for_kernel_v2"] is True for item in ITERATION_FAMILIES),
        "all_solver_iterations_runtime_targeted": all(item["runtime_solver_target"] is True for item in SOLVER_ITERATIONS),
        "benchmark_targets_present": len(BENCHMARK_TARGETS) > 0,
        "regression_guards_present": len(REGRESSION_GUARDS) > 0,
        "task_queue_commit_expected": all(item["commit_expected"] is True for item in TASK_QUEUE),
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_8_TASK_2_COMPETITIVE_SOLVER_KERNEL_V2",
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "deterministic": boundary.get("deterministic") is True,
        "public_safe": boundary.get("public_safe") is True,
        "runtime_solver_iteration_required": plan_record["runtime_solver_iteration_required"] is True,
        "real_submission_not_created": plan_record["real_submission_created"] is False,
        "real_submission_allowed_false": plan_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": plan_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": plan_record["kaggle_submission_sent"] is False,
        "upload_not_performed": plan_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": plan_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
        "score_claim_absent": plan_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": plan_record["public_leaderboard_claim_absent"] is True,
    }

    issue_state = {
        "audit_artifact_missing": not gate_state["audit_artifact_present"],
        "audit_artifact_not_ready": not gate_state["audit_artifact_ready"],
        "audit_artifact_invalid": not gate_state["audit_artifact_valid"],
        "audit_next_stage_mismatch": not gate_state["audit_next_stage_matches_milestone_8"],
        "audit_real_submission_not_blocked": not gate_state["audit_real_submission_blocked"],
        "audit_solver_iteration_not_required": not gate_state["audit_solver_iteration_required"],
        "plan_mode_invalid": not gate_state["plan_mode_valid"],
        "plan_scope_invalid": not gate_state["plan_scope_valid"],
        "plan_verdict_invalid": not gate_state["plan_verdict_valid"],
        "plan_not_ready": not gate_state["plan_ready"],
        "plan_not_locked": not gate_state["plan_locked"],
        "iteration_family_count_invalid": not gate_state["iteration_family_count_valid"],
        "solver_iteration_count_invalid": not gate_state["solver_iteration_count_valid"],
        "benchmark_target_count_invalid": not gate_state["benchmark_target_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "control_count_invalid": not gate_state["control_count_valid"],
        "plan_section_count_invalid": not gate_state["plan_section_count_valid"],
        "task_queue_count_invalid": not gate_state["task_queue_count_valid"],
        "family_priority_not_p0": not gate_state["all_families_priority_p0"],
        "family_not_ready_for_kernel_v2": not gate_state["all_families_ready_for_kernel_v2"],
        "solver_iteration_not_runtime_targeted": not gate_state["all_solver_iterations_runtime_targeted"],
        "benchmark_targets_missing": not gate_state["benchmark_targets_present"],
        "regression_guards_missing": not gate_state["regression_guards_present"],
        "task_queue_commit_not_expected": not gate_state["task_queue_commit_expected"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "local_only_false": not gate_state["local_only"],
        "dry_run_only_false": not gate_state["dry_run_only"],
        "deterministic_false": not gate_state["deterministic"],
        "public_safe_false": not gate_state["public_safe"],
        "runtime_solver_iteration_not_required": not gate_state["runtime_solver_iteration_required"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
        "score_claim_detected": not gate_state["score_claim_absent"],
        "public_leaderboard_claim_detected": not gate_state["public_leaderboard_claim_absent"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in PLAN_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in PLAN_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    plan_ready = (
        audit.get("status") == "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_READY"
        and audit.get("real_submission_readiness") == "BLOCKED"
        and audit.get("solver_iteration_required") is True
        and len(ITERATION_FAMILIES) == EXPECTED_ITERATION_FAMILY_COUNT
        and len(SOLVER_ITERATIONS) == EXPECTED_SOLVER_ITERATION_COUNT
        and len(BENCHMARK_TARGETS) == EXPECTED_BENCHMARK_TARGET_COUNT
        and passed_gate_count == len(PLAN_GATES)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #8",
        "task": "Task 1",
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_audit": audit.get("audit_id", "MISSING_AUDIT_ID"),
        "plan_ready": plan_ready,
        "plan_locked": True,
        "iteration_family_count": len(ITERATION_FAMILIES),
        "solver_iteration_count": len(SOLVER_ITERATIONS),
        "benchmark_target_count": len(BENCHMARK_TARGETS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "control_count": len(CONTROL_FLAGS),
        "task_queue_count": len(TASK_QUEUE),
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_iteration_required": True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": PLAN_STATUS,
        "milestone": "Milestone #8",
        "task": "Task 1",
        "title": "Competitive Solver Iteration Plan v2",
        "baseline_commit": BASELINE_COMMIT,
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "final_audit_source": {
            "path": str(FINAL_AUDIT_JSON),
            "present": FINAL_AUDIT_JSON.exists(),
            "status": audit.get("status", "MISSING"),
            "audit_id": audit.get("audit_id", "MISSING_AUDIT_ID"),
            "sha256": _sha256(FINAL_AUDIT_JSON),
            "sha256_16": _sha16(_sha256(FINAL_AUDIT_JSON)),
        },
        "plan_record": plan_record,
        "iteration_families": list(ITERATION_FAMILIES),
        "solver_iterations": list(SOLVER_ITERATIONS),
        "benchmark_targets": list(BENCHMARK_TARGETS),
        "regression_guards": list(REGRESSION_GUARDS),
        "control_flags": list(CONTROL_FLAGS),
        "plan_sections": list(PLAN_SECTIONS),
        "task_queue": list(TASK_QUEUE),
        "plan_gates": list(gates),
        "plan_issues": list(issues),
        "plan_index": index,
        "boundary": boundary,
        "audit_gate_count": int(audit.get("audit_gate_count", 0)),
        "audit_issue_count": int(audit.get("audit_issue_count", -1)),
        "audit_real_submission_readiness": audit.get("real_submission_readiness", "MISSING"),
        "audit_real_submission_decision": audit.get("real_submission_decision", "MISSING"),
        "iteration_family_count": len(ITERATION_FAMILIES),
        "solver_iteration_count": len(SOLVER_ITERATIONS),
        "benchmark_target_count": len(BENCHMARK_TARGETS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "control_count": len(CONTROL_FLAGS),
        "plan_section_count": len(PLAN_SECTIONS),
        "task_queue_count": len(TASK_QUEUE),
        "plan_gate_count": len(PLAN_GATES),
        "passed_gate_count": passed_gate_count,
        "plan_issue_count": issue_count,
        "warning_count": 0,
        "plan_ready": plan_ready,
        "plan_locked": True,
        "runtime_solver_iteration_required": True,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_8_competitive_solver_iteration_plan_v2",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    signature = _stable_signature(base)
    return {
        **base,
        "plan_id": f"MILESTONE-8-COMPETITIVE-SOLVER-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_8_competitive_solver_iteration_plan(plan: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = plan.get("boundary", {})
    gates = plan.get("plan_gates", [])
    issues = plan.get("plan_issues", [])
    families = plan.get("iteration_families", [])
    iterations = plan.get("solver_iterations", [])

    checks = {
        "status_ready": plan.get("status") == PLAN_STATUS,
        "plan_id_present": isinstance(plan.get("plan_id"), str) and bool(plan.get("plan_id")),
        "signature_present": isinstance(plan.get("signature"), str) and bool(plan.get("signature")),
        "baseline_commit_valid": str(plan.get("baseline_commit", "")).startswith("4c6e68d"),
        "plan_mode_valid": plan.get("plan_mode") == PLAN_MODE,
        "plan_scope_valid": plan.get("plan_scope") == PLAN_SCOPE,
        "plan_verdict_valid": plan.get("plan_verdict") == PLAN_VERDICT,
        "next_allowed_stage_valid": plan.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "audit_gate_count_valid": plan.get("audit_gate_count") == EXPECTED_AUDIT_GATE_COUNT,
        "audit_issue_count_zero": plan.get("audit_issue_count") == EXPECTED_AUDIT_ISSUE_COUNT,
        "audit_real_submission_blocked": plan.get("audit_real_submission_readiness") == "BLOCKED",
        "audit_real_submission_not_ready": plan.get("audit_real_submission_decision") == "NOT_READY",
        "iteration_family_count_valid": plan.get("iteration_family_count") == EXPECTED_ITERATION_FAMILY_COUNT,
        "solver_iteration_count_valid": plan.get("solver_iteration_count") == EXPECTED_SOLVER_ITERATION_COUNT,
        "benchmark_target_count_valid": plan.get("benchmark_target_count") == EXPECTED_BENCHMARK_TARGET_COUNT,
        "regression_guard_count_valid": plan.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "control_count_valid": plan.get("control_count") == EXPECTED_CONTROL_COUNT,
        "plan_section_count_valid": plan.get("plan_section_count") == EXPECTED_PLAN_SECTION_COUNT,
        "task_queue_count_valid": plan.get("task_queue_count") == EXPECTED_TASK_QUEUE_COUNT,
        "families_priority_p0": bool(families) and all(item.get("priority") == "P0" for item in families),
        "families_ready_for_kernel_v2": bool(families) and all(item.get("ready_for_kernel_v2") is True for item in families),
        "iterations_runtime_targeted": bool(iterations) and all(item.get("runtime_solver_target") is True for item in iterations),
        "plan_gate_count_matches": plan.get("plan_gate_count") == len(PLAN_GATES),
        "all_plan_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "plan_issue_count_zero": plan.get("plan_issue_count") == 0,
        "all_plan_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "plan_ready": plan.get("plan_ready") is True,
        "plan_locked": plan.get("plan_locked") is True,
        "runtime_solver_iteration_required": plan.get("runtime_solver_iteration_required") is True,
        "real_submission_not_created": plan.get("real_submission_created") is False,
        "real_submission_allowed_false": plan.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": plan.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": plan.get("kaggle_submission_sent") is False,
        "upload_not_performed": plan.get("upload_performed") is False,
        "kaggle_authentication_not_performed": plan.get("kaggle_authentication_performed") is False,
        "score_claim_absent": plan.get("score_claim_absent") is True,
        "public_leaderboard_claim_absent": plan.get("public_leaderboard_claim_absent") is True,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_INVALID",
        "valid": valid,
        "checks": checks,
        "plan_id": plan.get("plan_id"),
        "signature": plan.get("signature"),
    }


def render_competitive_solver_iteration_plan_markdown(plan: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #8 - Competitive Solver Iteration Plan v2",
        "",
        f"- status: {plan['status']}",
        f"- plan_id: {plan['plan_id']}",
        f"- signature: {plan['signature']}",
        f"- baseline_commit: {plan['baseline_commit']}",
        f"- plan_mode: {plan['plan_mode']}",
        f"- plan_scope: {plan['plan_scope']}",
        f"- plan_verdict: {plan['plan_verdict']}",
        f"- next_allowed_stage: {plan['next_allowed_stage']}",
        f"- audit_real_submission_readiness: {plan['audit_real_submission_readiness']}",
        f"- audit_real_submission_decision: {plan['audit_real_submission_decision']}",
        f"- iteration_family_count: {plan['iteration_family_count']}",
        f"- solver_iteration_count: {plan['solver_iteration_count']}",
        f"- benchmark_target_count: {plan['benchmark_target_count']}",
        f"- regression_guard_count: {plan['regression_guard_count']}",
        f"- task_queue_count: {plan['task_queue_count']}",
        f"- plan_gate_count: {plan['plan_gate_count']}",
        f"- passed_gate_count: {plan['passed_gate_count']}",
        f"- plan_issue_count: {plan['plan_issue_count']}",
        f"- runtime_solver_iteration_required: {plan['runtime_solver_iteration_required']}",
        "",
        "## Iteration families",
        "",
    ]

    for item in plan["iteration_families"]:
        lines.append(
            f"- {item['priority']} {item['family_id']} / family={item['source_family']} / "
            f"ready_for_kernel_v2={item['ready_for_kernel_v2']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #8 is open. The next stage is Competitive Solver Kernel v2.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_V2_READY=true",
            "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_VALID=true",
            "ARC_AGI3_MILESTONE_8_PLAN_MODE=COMPETITIVE_SOLVER_ITERATION_PLAN_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_8_PLAN_VERDICT=COMPETITIVE_SOLVER_ITERATION_PLAN_READY_FOR_SOLVER_KERNEL_V2",
            "ARC_AGI3_MILESTONE_8_BASELINE_AUDIT_COMMIT=4c6e68d",
            "ARC_AGI3_MILESTONE_8_ITERATION_FAMILY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_SOLVER_ITERATION_COUNT=8",
            "ARC_AGI3_MILESTONE_8_BENCHMARK_TARGET_COUNT=8",
            "ARC_AGI3_MILESTONE_8_REGRESSION_GUARD_COUNT=8",
            "ARC_AGI3_MILESTONE_8_CONTROL_COUNT=10",
            "ARC_AGI3_MILESTONE_8_TASK_QUEUE_COUNT=5",
            "ARC_AGI3_MILESTONE_8_RUNTIME_SOLVER_ITERATION_REQUIRED=true",
            "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_2_COMPETITIVE_SOLVER_KERNEL_V2",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_competitive_solver_iteration_plan_manifest(plan: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 8 COMPETITIVE SOLVER ITERATION PLAN MANIFEST v2",
        f"plan_id={plan['plan_id']}",
        f"signature={plan['signature']}",
        f"status={plan['status']}",
        f"baseline_commit={plan['baseline_commit']}",
        f"plan_mode={plan['plan_mode']}",
        f"plan_verdict={plan['plan_verdict']}",
        f"next_allowed_stage={plan['next_allowed_stage']}",
        f"audit_real_submission_readiness={plan['audit_real_submission_readiness']}",
        f"audit_real_submission_decision={plan['audit_real_submission_decision']}",
        f"iteration_family_count={plan['iteration_family_count']}",
        f"solver_iteration_count={plan['solver_iteration_count']}",
        f"benchmark_target_count={plan['benchmark_target_count']}",
        f"regression_guard_count={plan['regression_guard_count']}",
        f"control_count={plan['control_count']}",
        f"plan_section_count={plan['plan_section_count']}",
        f"task_queue_count={plan['task_queue_count']}",
        f"plan_gate_count={plan['plan_gate_count']}",
        f"passed_gate_count={plan['passed_gate_count']}",
        f"plan_issue_count={plan['plan_issue_count']}",
        f"plan_ready={plan['plan_ready']}",
        f"plan_locked={plan['plan_locked']}",
        f"runtime_solver_iteration_required={plan['runtime_solver_iteration_required']}",
        f"real_submission_created={plan['real_submission_created']}",
        f"real_submission_allowed={plan['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={plan['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={plan['kaggle_submission_sent']}",
        f"upload_performed={plan['upload_performed']}",
        f"kaggle_authentication_performed={plan['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "ITERATION_FAMILIES",
    ]

    for item in plan["iteration_families"]:
        lines.append(
            f"{item['priority']} {item['family_id']} family={item['source_family']} "
            f"ready_for_kernel_v2={item['ready_for_kernel_v2']}"
        )

    lines.append("")
    lines.append("SOLVER_ITERATIONS")
    for item in plan["solver_iterations"]:
        lines.append(
            f"{item['iteration_id']} family={item['family']} type={item['iteration_type']} "
            f"runtime_solver_target={item['runtime_solver_target']}"
        )

    lines.append("")
    lines.append("TASK_QUEUE")
    for item in plan["task_queue"]:
        lines.append(f"{item['task']} name={item['name']} commit_expected={item['commit_expected']}")

    lines.append("")
    return "\n".join(lines)


def write_competitive_solver_iteration_plan_artifacts(
    plan: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    plan = dict(plan or build_milestone_8_competitive_solver_iteration_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-8-competitive-solver-iteration-plan-v2.json"
    md_path = output / "milestone-8-competitive-solver-iteration-plan-v2.md"
    manifest_path = output / "milestone-8-competitive-solver-iteration-plan-manifest-v2.txt"
    index_path = output / "milestone-8-competitive-solver-iteration-plan-index-v2.json"

    json_path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_competitive_solver_iteration_plan_markdown(plan), encoding="utf-8")
    manifest_path.write_text(render_competitive_solver_iteration_plan_manifest(plan), encoding="utf-8")
    index_path.write_text(json.dumps(plan["plan_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_8_competitive_solver_iteration_plan_pipeline() -> Dict[str, Any]:
    plan = build_milestone_8_competitive_solver_iteration_plan()
    validation = validate_milestone_8_competitive_solver_iteration_plan(plan)
    artifacts = write_competitive_solver_iteration_plan_artifacts(plan)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_PIPELINE_INVALID",
        "plan_status": plan["status"],
        "validation_status": validation["status"],
        "plan": plan,
        "plan_id": plan["plan_id"],
        "signature": plan["signature"],
        "plan_mode": plan["plan_mode"],
        "plan_verdict": plan["plan_verdict"],
        "next_allowed_stage": plan["next_allowed_stage"],
        "audit_real_submission_readiness": plan["audit_real_submission_readiness"],
        "audit_real_submission_decision": plan["audit_real_submission_decision"],
        "iteration_family_count": plan["iteration_family_count"],
        "solver_iteration_count": plan["solver_iteration_count"],
        "benchmark_target_count": plan["benchmark_target_count"],
        "regression_guard_count": plan["regression_guard_count"],
        "control_count": plan["control_count"],
        "plan_section_count": plan["plan_section_count"],
        "task_queue_count": plan["task_queue_count"],
        "plan_gate_count": plan["plan_gate_count"],
        "passed_gate_count": plan["passed_gate_count"],
        "plan_issue_count": plan["plan_issue_count"],
        "warning_count": plan["warning_count"],
        "plan_ready": plan["plan_ready"],
        "plan_locked": plan["plan_locked"],
        "runtime_solver_iteration_required": plan["runtime_solver_iteration_required"],
        "real_submission_created": plan["real_submission_created"],
        "real_submission_allowed": plan["real_submission_allowed"],
        "ready_for_real_kaggle_submission": plan["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": plan["kaggle_submission_sent"],
        "upload_performed": plan["upload_performed"],
        "kaggle_authentication_performed": plan["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": plan["metadata"],
    }
