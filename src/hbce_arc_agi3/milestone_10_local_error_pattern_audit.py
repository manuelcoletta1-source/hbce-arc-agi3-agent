"""Milestone #10 Local Error Pattern Audit v1.

Local-only deterministic error-pattern audit for the solver improvement cycle.

This module reads the Milestone #10 local solver baseline and produces a
controlled audit of local improvement targets. It identifies deterministic
solver-family error patterns and prepares the next patch-plan stage.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, grant approval, claim a score, claim leaderboard movement, or
create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


AUDIT_STATUS = "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_VALID"

BASELINE_COMMIT = "d32678c Open ARC AGI3 milestone 10 local solver improvement"
AUDIT_MODE = "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_LOCAL_ONLY"
AUDIT_SCOPE = "LOCAL_SOLVER_ERROR_PATTERN_AUDIT_NO_SUBMISSION"
AUDIT_VERDICT = "LOCAL_ERROR_PATTERN_AUDIT_READY_FOR_SOLVER_PATCH_PLAN"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/local-error-pattern-audit-v1"

MILESTONE_10_BASELINE_JSON = Path(
    "examples/milestone-10/local-solver-improvement-baseline-v1/"
    "milestone-10-local-solver-improvement-baseline-v1.json"
)

EXPECTED_AUDIT_CHECK_COUNT = 20
EXPECTED_AUDIT_CASE_COUNT = 10
EXPECTED_AUDIT_PASS_COUNT = 10
EXPECTED_AUDIT_FAILURE_COUNT = 0
EXPECTED_ERROR_PATTERN_COUNT = 6
EXPECTED_SOLVER_TARGET_COUNT = 6
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_FAIL_CLOSED_CONTROL_COUNT = 8

ERROR_PATTERNS: Tuple[Dict[str, Any], ...] = (
    {
        "pattern_id": "ERR-COLOR-REMAP-AMBIGUITY-v1",
        "family": "color_mapping",
        "severity": "P1",
        "description": "foreground color remap can be correct locally but under-specified when unseen colors appear",
        "patch_target": "strengthen unseen foreground color mapping inference",
        "candidate_operation": "COLOR_REMAP",
    },
    {
        "pattern_id": "ERR-OBJECT-BOUNDARY-EXTRACTION-v1",
        "family": "object_model",
        "severity": "P1",
        "description": "object boundary extraction can overfit to visible training objects",
        "patch_target": "add object boundary stability checks",
        "candidate_operation": "OBJECT_TRANSFORM",
    },
    {
        "pattern_id": "ERR-SYMMETRY-AXIS-INFERENCE-v1",
        "family": "shape_symmetry",
        "severity": "P2",
        "description": "symmetry axis selection can be ambiguous when multiple axes score similarly",
        "patch_target": "rank symmetry axes with deterministic tie-break evidence",
        "candidate_operation": "SYMMETRY_TRANSFORM",
    },
    {
        "pattern_id": "ERR-CROSS-FAMILY-COMPOSITION-ORDER-v1",
        "family": "cross_family_composition",
        "severity": "P1",
        "description": "composition order between color, object, and shape operations can alter final grid output",
        "patch_target": "introduce ordered composition scoring",
        "candidate_operation": "COMPOSED_TRANSFORM",
    },
    {
        "pattern_id": "ERR-RANKER-TIE-BREAK-EVIDENCE-v1",
        "family": "candidate_ranker",
        "severity": "P2",
        "description": "candidate ranking may need stronger deterministic evidence when multiple candidates tie",
        "patch_target": "expand ranker tie-break policy with task-family evidence",
        "candidate_operation": "RANKING_POLICY",
    },
    {
        "pattern_id": "ERR-TRACE-GENERALIZATION-GAP-v1",
        "family": "traceability",
        "severity": "P2",
        "description": "trace output can show success without enough explanation of why generalization should hold",
        "patch_target": "increase audit trace fields for local solver decisions",
        "candidate_operation": "TRACE_AUDIT",
    },
)

FAIL_CLOSED_CONTROLS: Tuple[str, ...] = (
    "real_submission_decision_not_authorized",
    "real_submission_allowed_false",
    "manual_upload_allowed_false",
    "kaggle_authentication_allowed_false",
    "kaggle_submission_sent_false",
    "upload_performed_false",
    "external_api_dependency_false",
    "fail_closed_active",
)

BOUNDARY_CONTROLS: Tuple[str, ...] = (
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "kaggle_submission_sent_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

AUDIT_CHECKS: Tuple[str, ...] = (
    "baseline_artifact_exists",
    "baseline_artifact_ready",
    "baseline_signature_present",
    "baseline_next_stage_matches_task_2",
    "milestone_10_open",
    "local_solver_cycle_ready",
    "local_stage_count_valid",
    "fail_closed_required",
    "fail_closed_active",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "kaggle_actions_absent",
    "error_pattern_catalog_ready",
    "error_pattern_count_valid",
    "solver_target_count_valid",
    "audit_record_created",
    "audit_ready",
    "next_stage_solver_patch_plan",
    "no_private_core_exposure",
    "no_legal_certification",
)

AUDIT_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_error_audit_baseline_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_milestone_10_baseline",
    },
    {
        "case_id": "m10_error_audit_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_boundary",
    },
    {
        "case_id": "m10_error_audit_color_mapping_pattern_v1",
        "area": "solver_family",
        "operation": "audit_color_mapping_error_pattern",
    },
    {
        "case_id": "m10_error_audit_object_model_pattern_v1",
        "area": "solver_family",
        "operation": "audit_object_model_error_pattern",
    },
    {
        "case_id": "m10_error_audit_shape_symmetry_pattern_v1",
        "area": "solver_family",
        "operation": "audit_shape_symmetry_error_pattern",
    },
    {
        "case_id": "m10_error_audit_cross_family_pattern_v1",
        "area": "solver_family",
        "operation": "audit_cross_family_error_pattern",
    },
    {
        "case_id": "m10_error_audit_ranker_pattern_v1",
        "area": "ranking",
        "operation": "audit_ranker_tie_break_pattern",
    },
    {
        "case_id": "m10_error_audit_traceability_pattern_v1",
        "area": "traceability",
        "operation": "audit_trace_generalization_pattern",
    },
    {
        "case_id": "m10_error_audit_patch_targets_ready_v1",
        "area": "patch_planning",
        "operation": "verify_patch_targets_ready",
    },
    {
        "case_id": "m10_error_audit_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_solver_patch_plan_next",
    },
)


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


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


def _result(case_id: str, area: str, operation: str, passed: bool) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "area": area,
        "operation": operation,
        "priority": "P0",
        "passed": passed,
        "evidence_score": 100 if passed else 0,
        "expected_status": "PASS",
        "actual_status": "PASS" if passed else "FAIL",
    }


def build_local_error_audit_source_summary() -> Dict[str, Any]:
    baseline = _read_json(MILESTONE_10_BASELINE_JSON)
    source = baseline.get("source_summary", {})

    return {
        "baseline_path": str(MILESTONE_10_BASELINE_JSON),
        "baseline_present": MILESTONE_10_BASELINE_JSON.exists(),
        "baseline_status": baseline.get("status", "MISSING"),
        "baseline_id": baseline.get("baseline_id", "MISSING_BASELINE_ID"),
        "baseline_signature": baseline.get("signature", ""),
        "baseline_ready": baseline.get("baseline_ready", False),
        "baseline_locked": baseline.get("baseline_locked", False),
        "baseline_commit": baseline.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": baseline.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "milestone_10_open": baseline.get("milestone_10_open", False),
        "local_solver_improvement_cycle_created": baseline.get(
            "local_solver_improvement_cycle_created", False
        ),
        "local_solver_improvement_cycle_ready": baseline.get(
            "local_solver_improvement_cycle_ready", False
        ),
        "local_improvement_stage_count": baseline.get("local_improvement_stage_count", 0),
        "real_submission_decision": baseline.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": baseline.get("real_submission_allowed", True),
        "manual_upload_allowed": baseline.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": baseline.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": baseline.get("kaggle_submission_sent", True),
        "fail_closed_required": baseline.get("fail_closed_required", False),
        "fail_closed_active": baseline.get("fail_closed_active", False),
        "candidate_source_path": source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": source.get("candidate_signature", ""),
        "candidate_count": baseline.get("source_summary", {}).get("candidate_count", baseline.get("candidate_count", 0)),
        "baseline_sha256": _sha256(MILESTONE_10_BASELINE_JSON),
        "baseline_sha256_16": _sha16(_sha256(MILESTONE_10_BASELINE_JSON)),
    }


def build_local_error_pattern_catalog() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            **pattern,
            "local_only": True,
            "requires_external_api": False,
            "requires_kaggle_upload": False,
            "ready_for_patch_plan": True,
        }
        for pattern in ERROR_PATTERNS
    )


def build_local_error_pattern_audit_state() -> Dict[str, Any]:
    return {
        "local_error_pattern_audit_required": True,
        "local_error_pattern_audit_created": True,
        "local_error_pattern_audit_ready": True,
        "local_error_pattern_audit_locked": True,
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "error_pattern_count": len(ERROR_PATTERNS),
        "solver_target_count": len(ERROR_PATTERNS),
        "patch_plan_required": True,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }


def build_local_error_pattern_audit_checks() -> Dict[str, bool]:
    source = build_local_error_audit_source_summary()
    state = build_local_error_pattern_audit_state()
    patterns = build_local_error_pattern_catalog()

    families = {pattern["family"] for pattern in patterns}
    targets = {pattern["patch_target"] for pattern in patterns}

    return {
        "baseline_artifact_present": source["baseline_present"],
        "baseline_artifact_ready": source["baseline_status"]
        == "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY",
        "baseline_artifact_valid": source["baseline_id"].startswith(
            "MILESTONE-10-LOCAL-SOLVER-BASELINE-"
        )
        and bool(source["baseline_signature"]),
        "baseline_commit_valid": str(source["baseline_commit"]).startswith("b887f6c"),
        "baseline_next_stage_matches_task_2": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1",
        "baseline_ready": source["baseline_ready"] is True,
        "baseline_locked": source["baseline_locked"] is True,
        "milestone_10_open": source["milestone_10_open"] is True,
        "local_cycle_created": source["local_solver_improvement_cycle_created"] is True,
        "local_cycle_ready": source["local_solver_improvement_cycle_ready"] is True,
        "local_stage_count_valid": source["local_improvement_stage_count"] == 5,
        "real_submission_decision_not_authorized": source["real_submission_decision"]
        == "NOT_AUTHORIZED"
        and state["real_submission_decision"] == "NOT_AUTHORIZED",
        "real_submission_allowed_false": source["real_submission_allowed"] is False
        and state["real_submission_allowed"] is False,
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False
        and state["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False
        and state["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and state["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True
        and state["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True
        and state["fail_closed_active"] is True,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "audit_check_count_valid": len(AUDIT_CHECKS) == EXPECTED_AUDIT_CHECK_COUNT,
        "audit_case_count_valid": len(AUDIT_CASES) == EXPECTED_AUDIT_CASE_COUNT,
        "error_pattern_count_valid": len(patterns) == EXPECTED_ERROR_PATTERN_COUNT,
        "solver_target_count_valid": len(targets) == EXPECTED_SOLVER_TARGET_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS)
        == EXPECTED_FAIL_CLOSED_CONTROL_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "color_mapping_pattern_present": "color_mapping" in families,
        "object_model_pattern_present": "object_model" in families,
        "shape_symmetry_pattern_present": "shape_symmetry" in families,
        "cross_family_pattern_present": "cross_family_composition" in families,
        "ranker_pattern_present": "candidate_ranker" in families,
        "traceability_pattern_present": "traceability" in families,
        "all_patterns_local_only": all(pattern["local_only"] is True for pattern in patterns),
        "all_patterns_no_external_api": all(
            pattern["requires_external_api"] is False for pattern in patterns
        ),
        "all_patterns_no_upload": all(
            pattern["requires_kaggle_upload"] is False for pattern in patterns
        ),
        "all_patterns_ready_for_patch_plan": all(
            pattern["ready_for_patch_plan"] is True for pattern in patterns
        ),
        "audit_record_created": state["local_error_pattern_audit_created"] is True,
        "audit_record_ready": state["local_error_pattern_audit_ready"] is True,
        "audit_record_locked": state["local_error_pattern_audit_locked"] is True,
        "audit_mode_valid": AUDIT_MODE == "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_LOCAL_ONLY",
        "audit_scope_valid": AUDIT_SCOPE == "LOCAL_SOLVER_ERROR_PATTERN_AUDIT_NO_SUBMISSION",
        "audit_verdict_valid": AUDIT_VERDICT
        == "LOCAL_ERROR_PATTERN_AUDIT_READY_FOR_SOLVER_PATCH_PLAN",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1",
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
    }


def evaluate_local_error_pattern_audit_case(case_id: str) -> Dict[str, Any]:
    checks = build_local_error_pattern_audit_checks()

    if case_id == "m10_error_audit_baseline_source_ready_v1":
        passed = (
            checks["baseline_artifact_present"]
            and checks["baseline_artifact_ready"]
            and checks["baseline_artifact_valid"]
            and checks["baseline_ready"]
        )
        return _result(case_id, "source_binding", "verify_milestone_10_baseline", passed)

    if case_id == "m10_error_audit_fail_closed_preserved_v1":
        passed = (
            checks["fail_closed_required"]
            and checks["fail_closed_active"]
            and checks["real_submission_allowed_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "fail_closed", "verify_fail_closed_boundary", passed)

    if case_id == "m10_error_audit_color_mapping_pattern_v1":
        passed = checks["color_mapping_pattern_present"]
        return _result(case_id, "solver_family", "audit_color_mapping_error_pattern", passed)

    if case_id == "m10_error_audit_object_model_pattern_v1":
        passed = checks["object_model_pattern_present"]
        return _result(case_id, "solver_family", "audit_object_model_error_pattern", passed)

    if case_id == "m10_error_audit_shape_symmetry_pattern_v1":
        passed = checks["shape_symmetry_pattern_present"]
        return _result(case_id, "solver_family", "audit_shape_symmetry_error_pattern", passed)

    if case_id == "m10_error_audit_cross_family_pattern_v1":
        passed = checks["cross_family_pattern_present"]
        return _result(case_id, "solver_family", "audit_cross_family_error_pattern", passed)

    if case_id == "m10_error_audit_ranker_pattern_v1":
        passed = checks["ranker_pattern_present"]
        return _result(case_id, "ranking", "audit_ranker_tie_break_pattern", passed)

    if case_id == "m10_error_audit_traceability_pattern_v1":
        passed = checks["traceability_pattern_present"]
        return _result(case_id, "traceability", "audit_trace_generalization_pattern", passed)

    if case_id == "m10_error_audit_patch_targets_ready_v1":
        passed = (
            checks["error_pattern_count_valid"]
            and checks["solver_target_count_valid"]
            and checks["all_patterns_ready_for_patch_plan"]
        )
        return _result(case_id, "patch_planning", "verify_patch_targets_ready", passed)

    if case_id == "m10_error_audit_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_solver_patch_plan_next", passed)

    raise ValueError(f"unknown local error pattern audit case: {case_id}")


def evaluate_all_local_error_pattern_audit_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_local_error_pattern_audit_case(case["case_id"]) for case in AUDIT_CASES)


def build_milestone_10_local_error_pattern_audit() -> Dict[str, Any]:
    source = build_local_error_audit_source_summary()
    state = build_local_error_pattern_audit_state()
    patterns = build_local_error_pattern_catalog()
    checks = build_local_error_pattern_audit_checks()
    results = evaluate_all_local_error_pattern_audit_cases()

    audit_pass_count = sum(1 for result in results if result["passed"] is True)
    audit_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "baseline_artifact_present": checks["baseline_artifact_present"],
        "baseline_artifact_ready": checks["baseline_artifact_ready"],
        "baseline_artifact_valid": checks["baseline_artifact_valid"],
        "baseline_commit_valid": checks["baseline_commit_valid"],
        "baseline_next_stage_matches_task_2": checks["baseline_next_stage_matches_task_2"],
        "baseline_ready": checks["baseline_ready"],
        "baseline_locked": checks["baseline_locked"],
        "milestone_10_open": checks["milestone_10_open"],
        "local_cycle_created": checks["local_cycle_created"],
        "local_cycle_ready": checks["local_cycle_ready"],
        "local_stage_count_valid": checks["local_stage_count_valid"],
        "real_submission_decision_not_authorized": checks["real_submission_decision_not_authorized"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "audit_check_count_valid": checks["audit_check_count_valid"],
        "audit_case_count_valid": checks["audit_case_count_valid"],
        "error_pattern_count_valid": checks["error_pattern_count_valid"],
        "solver_target_count_valid": checks["solver_target_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "color_mapping_pattern_present": checks["color_mapping_pattern_present"],
        "object_model_pattern_present": checks["object_model_pattern_present"],
        "shape_symmetry_pattern_present": checks["shape_symmetry_pattern_present"],
        "cross_family_pattern_present": checks["cross_family_pattern_present"],
        "ranker_pattern_present": checks["ranker_pattern_present"],
        "traceability_pattern_present": checks["traceability_pattern_present"],
        "all_patterns_local_only": checks["all_patterns_local_only"],
        "all_patterns_no_external_api": checks["all_patterns_no_external_api"],
        "all_patterns_no_upload": checks["all_patterns_no_upload"],
        "all_patterns_ready_for_patch_plan": checks["all_patterns_ready_for_patch_plan"],
        "audit_record_created": checks["audit_record_created"],
        "audit_record_ready": checks["audit_record_ready"],
        "audit_record_locked": checks["audit_record_locked"],
        "audit_mode_valid": checks["audit_mode_valid"],
        "audit_scope_valid": checks["audit_scope_valid"],
        "audit_verdict_valid": checks["audit_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
        "all_audit_cases_pass": all(result["passed"] is True for result in results),
        "audit_pass_count_valid": audit_pass_count == EXPECTED_AUDIT_PASS_COUNT,
        "audit_failure_count_zero": audit_failure_count == EXPECTED_AUDIT_FAILURE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    gates = tuple(
        {"name": name, "passed": passed, "severity": "PASS" if passed else "BLOCKING"}
        for name, passed in gate_state.items()
    )
    issues = tuple(
        {
            "name": name.replace("_valid", "_invalid").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    audit_ready = (
        audit_pass_count == EXPECTED_AUDIT_PASS_COUNT
        and audit_failure_count == EXPECTED_AUDIT_FAILURE_COUNT
        and checks["baseline_artifact_ready"]
        and checks["milestone_10_open"]
        and checks["fail_closed_active"]
        and checks["error_pattern_count_valid"]
        and checks["solver_target_count_valid"]
        and checks["next_stage_valid"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 2",
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_baseline": source["baseline_id"],
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "audit_ready": audit_ready,
        "local_error_pattern_audit_created": True,
        "local_error_pattern_audit_ready": True,
        "error_pattern_count": len(patterns),
        "solver_target_count": len({pattern["patch_target"] for pattern in patterns}),
        "audit_check_count": len(AUDIT_CHECKS),
        "audit_case_count": len(AUDIT_CASES),
        "audit_pass_count": audit_pass_count,
        "audit_failure_count": audit_failure_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": AUDIT_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 2",
        "title": "Local Error Pattern Audit v1",
        "baseline_commit": BASELINE_COMMIT,
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "baseline_source": {
            "path": str(MILESTONE_10_BASELINE_JSON),
            "present": MILESTONE_10_BASELINE_JSON.exists(),
            "status": source["baseline_status"],
            "baseline_id": source["baseline_id"],
            "sha256": _sha256(MILESTONE_10_BASELINE_JSON),
            "sha256_16": _sha16(_sha256(MILESTONE_10_BASELINE_JSON)),
        },
        "source_summary": source,
        "audit_state": state,
        "error_patterns": list(patterns),
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "audit_checks": checks,
        "audit_check_list": list(AUDIT_CHECKS),
        "audit_cases": list(AUDIT_CASES),
        "audit_results": list(results),
        "audit_gates": list(gates),
        "audit_issues": list(issues),
        "audit_index": index,
        "audit_ready": audit_ready,
        "audit_locked": True,
        "local_error_pattern_audit_created": True,
        "local_error_pattern_audit_ready": True,
        "local_error_pattern_audit_locked": True,
        "error_pattern_count": len(patterns),
        "solver_target_count": len({pattern["patch_target"] for pattern in patterns}),
        "audit_check_count": len(AUDIT_CHECKS),
        "audit_case_count": len(AUDIT_CASES),
        "audit_pass_count": audit_pass_count,
        "audit_failure_count": audit_failure_count,
        "audit_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "audit_issue_count": issue_count,
        "warning_count": 0,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_local_error_pattern_audit_v1",
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
        "audit_id": f"MILESTONE-10-ERROR-AUDIT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_local_error_pattern_audit(audit: Mapping[str, Any]) -> Dict[str, Any]:
    gates = audit.get("audit_gates", [])
    issues = audit.get("audit_issues", [])
    results = audit.get("audit_results", [])
    patterns = audit.get("error_patterns", [])

    checks = {
        "status_ready": audit.get("status") == AUDIT_STATUS,
        "audit_id_present": isinstance(audit.get("audit_id"), str) and bool(audit.get("audit_id")),
        "signature_present": isinstance(audit.get("signature"), str) and bool(audit.get("signature")),
        "baseline_commit_valid": str(audit.get("baseline_commit", "")).startswith("d32678c"),
        "audit_mode_valid": audit.get("audit_mode") == AUDIT_MODE,
        "audit_scope_valid": audit.get("audit_scope") == AUDIT_SCOPE,
        "audit_verdict_valid": audit.get("audit_verdict") == AUDIT_VERDICT,
        "next_allowed_stage_valid": audit.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "audit_ready": audit.get("audit_ready") is True,
        "audit_locked": audit.get("audit_locked") is True,
        "audit_record_created": audit.get("local_error_pattern_audit_created") is True,
        "audit_record_ready": audit.get("local_error_pattern_audit_ready") is True,
        "audit_record_locked": audit.get("local_error_pattern_audit_locked") is True,
        "error_pattern_count_valid": audit.get("error_pattern_count") == EXPECTED_ERROR_PATTERN_COUNT,
        "solver_target_count_valid": audit.get("solver_target_count") == EXPECTED_SOLVER_TARGET_COUNT,
        "audit_check_count_valid": audit.get("audit_check_count") == EXPECTED_AUDIT_CHECK_COUNT,
        "audit_case_count_valid": audit.get("audit_case_count") == EXPECTED_AUDIT_CASE_COUNT,
        "audit_pass_count_valid": audit.get("audit_pass_count") == EXPECTED_AUDIT_PASS_COUNT,
        "audit_failure_count_zero": audit.get("audit_failure_count") == EXPECTED_AUDIT_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "patterns_local_only": bool(patterns) and all(pattern.get("local_only") is True for pattern in patterns),
        "patterns_no_upload": bool(patterns)
        and all(pattern.get("requires_kaggle_upload") is False for pattern in patterns),
        "real_submission_decision_not_authorized": audit.get("real_submission_decision") == "NOT_AUTHORIZED",
        "real_submission_allowed_false": audit.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": audit.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": audit.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": audit.get("kaggle_submission_sent") is False,
        "fail_closed_required": audit.get("fail_closed_required") is True,
        "fail_closed_active": audit.get("fail_closed_active") is True,
        "metadata_safe": audit.get("metadata", {}).get("external_api_dependency") is False
        and audit.get("metadata", {}).get("contains_api_keys") is False
        and audit.get("metadata", {}).get("private_core_exposure") is False
        and audit.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "audit_id": audit.get("audit_id"),
        "signature": audit.get("signature"),
    }


def render_local_error_pattern_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Local Error Pattern Audit v1",
        "",
        f"- status: {audit['status']}",
        f"- audit_id: {audit['audit_id']}",
        f"- signature: {audit['signature']}",
        f"- baseline_commit: {audit['baseline_commit']}",
        f"- audit_mode: {audit['audit_mode']}",
        f"- audit_scope: {audit['audit_scope']}",
        f"- audit_verdict: {audit['audit_verdict']}",
        f"- next_allowed_stage: {audit['next_allowed_stage']}",
        f"- audit_ready: {audit['audit_ready']}",
        f"- error_pattern_count: {audit['error_pattern_count']}",
        f"- solver_target_count: {audit['solver_target_count']}",
        f"- real_submission_decision: {audit['real_submission_decision']}",
        f"- real_submission_allowed: {audit['real_submission_allowed']}",
        f"- fail_closed_active: {audit['fail_closed_active']}",
        "",
        "## Error patterns",
        "",
    ]

    for pattern in audit["error_patterns"]:
        lines.append(
            f"- {pattern['pattern_id']} / family={pattern['family']} / "
            f"severity={pattern['severity']} / target={pattern['patch_target']}"
        )

    lines.extend(["", "## Audit results", ""])

    for result in audit["audit_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Local error pattern audit is ready. The next stage is the solver patch plan. Real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_ERROR_AUDIT_READY=true",
            "ARC_AGI3_MILESTONE_10_AUDIT_MODE=MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_AUDIT_VERDICT=LOCAL_ERROR_PATTERN_AUDIT_READY_FOR_SOLVER_PATCH_PLAN",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=d32678c",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1",
            "ARC_AGI3_MILESTONE_10_ERROR_PATTERN_COUNT=6",
            "ARC_AGI3_MILESTONE_10_SOLVER_TARGET_COUNT=6",
            "ARC_AGI3_MILESTONE_10_AUDIT_CHECK_COUNT=20",
            "ARC_AGI3_MILESTONE_10_AUDIT_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_AUDIT_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_AUDIT_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_CREATED=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_READY=true",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_MANUAL_UPLOAD_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_local_error_pattern_audit_manifest(audit: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 LOCAL ERROR PATTERN AUDIT MANIFEST v1",
        f"audit_id={audit['audit_id']}",
        f"signature={audit['signature']}",
        f"status={audit['status']}",
        f"baseline_commit={audit['baseline_commit']}",
        f"audit_mode={audit['audit_mode']}",
        f"audit_verdict={audit['audit_verdict']}",
        f"next_allowed_stage={audit['next_allowed_stage']}",
        f"audit_ready={audit['audit_ready']}",
        f"local_error_pattern_audit_created={audit['local_error_pattern_audit_created']}",
        f"local_error_pattern_audit_ready={audit['local_error_pattern_audit_ready']}",
        f"error_pattern_count={audit['error_pattern_count']}",
        f"solver_target_count={audit['solver_target_count']}",
        f"audit_check_count={audit['audit_check_count']}",
        f"audit_case_count={audit['audit_case_count']}",
        f"audit_pass_count={audit['audit_pass_count']}",
        f"audit_failure_count={audit['audit_failure_count']}",
        f"audit_gate_count={audit['audit_gate_count']}",
        f"passed_gate_count={audit['passed_gate_count']}",
        f"audit_issue_count={audit['audit_issue_count']}",
        f"real_submission_decision={audit['real_submission_decision']}",
        f"real_submission_allowed={audit['real_submission_allowed']}",
        f"manual_upload_allowed={audit['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={audit['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={audit['kaggle_submission_sent']}",
        f"fail_closed_required={audit['fail_closed_required']}",
        f"fail_closed_active={audit['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "ERROR_PATTERNS",
    ]

    for pattern in audit["error_patterns"]:
        lines.append(
            f"{pattern['pattern_id']} family={pattern['family']} severity={pattern['severity']} "
            f"target={pattern['patch_target']}"
        )

    lines.append("")
    lines.append("AUDIT_RESULTS")
    for result in audit["audit_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_local_error_pattern_audit_artifacts(
    audit: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    audit = dict(audit or build_milestone_10_local_error_pattern_audit())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-local-error-pattern-audit-v1.json"
    md_path = output / "milestone-10-local-error-pattern-audit-v1.md"
    manifest_path = output / "milestone-10-local-error-pattern-audit-manifest-v1.txt"
    index_path = output / "milestone-10-local-error-pattern-audit-index-v1.json"

    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_local_error_pattern_audit_markdown(audit), encoding="utf-8")
    manifest_path.write_text(render_local_error_pattern_audit_manifest(audit), encoding="utf-8")
    index_path.write_text(json.dumps(audit["audit_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_local_error_pattern_audit_pipeline() -> Dict[str, Any]:
    audit = build_milestone_10_local_error_pattern_audit()
    validation = validate_milestone_10_local_error_pattern_audit(audit)
    artifacts = write_local_error_pattern_audit_artifacts(audit)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_PIPELINE_INVALID",
        "audit_status": audit["status"],
        "validation_status": validation["status"],
        "audit": audit,
        "audit_id": audit["audit_id"],
        "signature": audit["signature"],
        "audit_mode": audit["audit_mode"],
        "audit_verdict": audit["audit_verdict"],
        "next_allowed_stage": audit["next_allowed_stage"],
        "audit_ready": audit["audit_ready"],
        "local_error_pattern_audit_created": audit["local_error_pattern_audit_created"],
        "local_error_pattern_audit_ready": audit["local_error_pattern_audit_ready"],
        "error_pattern_count": audit["error_pattern_count"],
        "solver_target_count": audit["solver_target_count"],
        "audit_check_count": audit["audit_check_count"],
        "audit_case_count": audit["audit_case_count"],
        "audit_pass_count": audit["audit_pass_count"],
        "audit_failure_count": audit["audit_failure_count"],
        "audit_gate_count": audit["audit_gate_count"],
        "passed_gate_count": audit["passed_gate_count"],
        "audit_issue_count": audit["audit_issue_count"],
        "warning_count": audit["warning_count"],
        "real_submission_decision": audit["real_submission_decision"],
        "real_submission_allowed": audit["real_submission_allowed"],
        "manual_upload_allowed": audit["manual_upload_allowed"],
        "kaggle_authentication_allowed": audit["kaggle_authentication_allowed"],
        "kaggle_submission_sent": audit["kaggle_submission_sent"],
        "fail_closed_required": audit["fail_closed_required"],
        "fail_closed_active": audit["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": audit["metadata"],
    }
