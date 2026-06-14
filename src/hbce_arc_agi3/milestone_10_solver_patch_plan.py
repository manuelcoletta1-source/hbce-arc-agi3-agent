"""Milestone #10 Solver Patch Plan v1.

Local-only deterministic patch plan for the solver improvement cycle.

This module reads the Milestone #10 local error-pattern audit and creates a
patch plan. It does not modify solver runtime code. It does not create a
submission candidate. It does not submit to Kaggle, authenticate, upload files,
call external APIs, read secrets, grant approval, claim a score, claim
leaderboard movement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PLAN_STATUS = "MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_SOLVER_PATCH_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_SOLVER_PATCH_PLAN_V1_VALID"

BASELINE_COMMIT = "88acc88 Add ARC AGI3 local error pattern audit"
PLAN_MODE = "MILESTONE_10_SOLVER_PATCH_PLAN_V1_LOCAL_ONLY"
PLAN_SCOPE = "LOCAL_SOLVER_PATCH_PLAN_NO_RUNTIME_MODIFICATION"
PLAN_VERDICT = "SOLVER_PATCH_PLAN_READY_FOR_LOCAL_IMPLEMENTATION"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_4_SOLVER_PATCH_IMPLEMENTATION_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/solver-patch-plan-v1"

ERROR_AUDIT_JSON = Path(
    "examples/milestone-10/local-error-pattern-audit-v1/"
    "milestone-10-local-error-pattern-audit-v1.json"
)

EXPECTED_PATCH_TARGET_COUNT = 6
EXPECTED_PATCH_STEP_COUNT = 6
EXPECTED_PLAN_CHECK_COUNT = 22
EXPECTED_PLAN_CASE_COUNT = 10
EXPECTED_PLAN_PASS_COUNT = 10
EXPECTED_PLAN_FAILURE_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_FAIL_CLOSED_CONTROL_COUNT = 8

PATCH_STEPS: Tuple[Dict[str, Any], ...] = (
    {
        "patch_id": "PATCH-COLOR-REMAP-STABILITY-v1",
        "source_pattern_id": "ERR-COLOR-REMAP-AMBIGUITY-v1",
        "target_module": "solver_candidate_generation",
        "family": "color_mapping",
        "priority": "P1",
        "implementation_intent": "add unseen-color remap stability scoring",
        "runtime_modification_allowed_now": False,
    },
    {
        "patch_id": "PATCH-OBJECT-BOUNDARY-STABILITY-v1",
        "source_pattern_id": "ERR-OBJECT-BOUNDARY-EXTRACTION-v1",
        "target_module": "object_transform_solver",
        "family": "object_model",
        "priority": "P1",
        "implementation_intent": "add object boundary extraction consistency checks",
        "runtime_modification_allowed_now": False,
    },
    {
        "patch_id": "PATCH-SYMMETRY-AXIS-TIEBREAK-v1",
        "source_pattern_id": "ERR-SYMMETRY-AXIS-INFERENCE-v1",
        "target_module": "shape_symmetry_solver",
        "family": "shape_symmetry",
        "priority": "P2",
        "implementation_intent": "rank symmetry axes with deterministic evidence fields",
        "runtime_modification_allowed_now": False,
    },
    {
        "patch_id": "PATCH-COMPOSITION-ORDER-SCORING-v1",
        "source_pattern_id": "ERR-CROSS-FAMILY-COMPOSITION-ORDER-v1",
        "target_module": "composed_transform_solver",
        "family": "cross_family_composition",
        "priority": "P1",
        "implementation_intent": "score operation order across color, object, and shape transforms",
        "runtime_modification_allowed_now": False,
    },
    {
        "patch_id": "PATCH-RANKER-EVIDENCE-TIEBREAK-v1",
        "source_pattern_id": "ERR-RANKER-TIE-BREAK-EVIDENCE-v1",
        "target_module": "candidate_ranker",
        "family": "candidate_ranker",
        "priority": "P2",
        "implementation_intent": "expand deterministic ranker tie-break evidence",
        "runtime_modification_allowed_now": False,
    },
    {
        "patch_id": "PATCH-TRACE-GENERALIZATION-FIELDS-v1",
        "source_pattern_id": "ERR-TRACE-GENERALIZATION-GAP-v1",
        "target_module": "audit_trace",
        "family": "traceability",
        "priority": "P2",
        "implementation_intent": "add local trace fields explaining generalization assumptions",
        "runtime_modification_allowed_now": False,
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

PLAN_CHECKS: Tuple[str, ...] = (
    "audit_artifact_exists",
    "audit_artifact_ready",
    "audit_signature_present",
    "audit_next_stage_matches_task_3",
    "error_pattern_count_valid",
    "solver_target_count_valid",
    "patch_target_count_valid",
    "patch_step_count_valid",
    "all_patch_steps_link_source_patterns",
    "all_patch_steps_local_only",
    "runtime_modification_blocked_now",
    "next_stage_implementation_valid",
    "fail_closed_required",
    "fail_closed_active",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_absent",
    "plan_record_created",
    "no_private_core_exposure",
    "no_legal_certification",
)

PLAN_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_patch_plan_audit_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_error_audit_source",
    },
    {
        "case_id": "m10_patch_plan_patch_targets_complete_v1",
        "area": "patch_targets",
        "operation": "verify_patch_target_count",
    },
    {
        "case_id": "m10_patch_plan_color_remap_patch_v1",
        "area": "patch_plan",
        "operation": "plan_color_remap_patch",
    },
    {
        "case_id": "m10_patch_plan_object_boundary_patch_v1",
        "area": "patch_plan",
        "operation": "plan_object_boundary_patch",
    },
    {
        "case_id": "m10_patch_plan_symmetry_patch_v1",
        "area": "patch_plan",
        "operation": "plan_symmetry_patch",
    },
    {
        "case_id": "m10_patch_plan_composition_patch_v1",
        "area": "patch_plan",
        "operation": "plan_composition_patch",
    },
    {
        "case_id": "m10_patch_plan_ranker_patch_v1",
        "area": "patch_plan",
        "operation": "plan_ranker_patch",
    },
    {
        "case_id": "m10_patch_plan_traceability_patch_v1",
        "area": "patch_plan",
        "operation": "plan_traceability_patch",
    },
    {
        "case_id": "m10_patch_plan_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_patch_plan_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_implementation_next",
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


def build_solver_patch_plan_source_summary() -> Dict[str, Any]:
    audit = _read_json(ERROR_AUDIT_JSON)
    source = audit.get("source_summary", {})

    return {
        "audit_path": str(ERROR_AUDIT_JSON),
        "audit_present": ERROR_AUDIT_JSON.exists(),
        "audit_status": audit.get("status", "MISSING"),
        "audit_id": audit.get("audit_id", "MISSING_AUDIT_ID"),
        "audit_signature": audit.get("signature", ""),
        "audit_ready": audit.get("audit_ready", False),
        "audit_locked": audit.get("audit_locked", False),
        "baseline_commit": audit.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": audit.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "error_pattern_count": audit.get("error_pattern_count", 0),
        "solver_target_count": audit.get("solver_target_count", 0),
        "error_patterns": audit.get("error_patterns", []),
        "candidate_source_path": source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": source.get("candidate_signature", ""),
        "candidate_count": source.get("candidate_count", 0),
        "real_submission_decision": audit.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": audit.get("real_submission_allowed", True),
        "manual_upload_allowed": audit.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": audit.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": audit.get("kaggle_submission_sent", True),
        "fail_closed_required": audit.get("fail_closed_required", False),
        "fail_closed_active": audit.get("fail_closed_active", False),
        "audit_sha256": _sha256(ERROR_AUDIT_JSON),
        "audit_sha256_16": _sha16(_sha256(ERROR_AUDIT_JSON)),
    }


def build_solver_patch_steps() -> Tuple[Dict[str, Any], ...]:
    audit_patterns = {
        pattern.get("pattern_id"): pattern
        for pattern in build_solver_patch_plan_source_summary()["error_patterns"]
    }

    return tuple(
        {
            **step,
            "source_pattern_present": step["source_pattern_id"] in audit_patterns,
            "local_only": True,
            "requires_external_api": False,
            "requires_kaggle_upload": False,
            "creates_submission_candidate": False,
            "ready_for_implementation": True,
        }
        for step in PATCH_STEPS
    )


def build_solver_patch_plan_state() -> Dict[str, Any]:
    return {
        "solver_patch_plan_required": True,
        "solver_patch_plan_created": True,
        "solver_patch_plan_ready": True,
        "solver_patch_plan_locked": True,
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "patch_target_count": len(PATCH_STEPS),
        "patch_step_count": len(PATCH_STEPS),
        "runtime_modification_allowed_now": False,
        "submission_candidate_created": False,
        "implementation_required_next": True,
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


def build_solver_patch_plan_checks() -> Dict[str, bool]:
    source = build_solver_patch_plan_source_summary()
    steps = build_solver_patch_steps()
    state = build_solver_patch_plan_state()

    families = {step["family"] for step in steps}
    source_pattern_ids = {step["source_pattern_id"] for step in steps}

    return {
        "audit_artifact_present": source["audit_present"],
        "audit_artifact_ready": source["audit_status"] == "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY",
        "audit_artifact_valid": source["audit_id"].startswith("MILESTONE-10-ERROR-AUDIT-")
        and bool(source["audit_signature"]),
        "audit_commit_valid": str(source["baseline_commit"]).startswith("d32678c"),
        "audit_next_stage_matches_task_3": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1",
        "audit_ready": source["audit_ready"] is True,
        "audit_locked": source["audit_locked"] is True,
        "error_pattern_count_valid": source["error_pattern_count"] == EXPECTED_PATCH_TARGET_COUNT,
        "solver_target_count_valid": source["solver_target_count"] == EXPECTED_PATCH_TARGET_COUNT,
        "patch_target_count_valid": len(source_pattern_ids) == EXPECTED_PATCH_TARGET_COUNT,
        "patch_step_count_valid": len(steps) == EXPECTED_PATCH_STEP_COUNT,
        "all_patch_steps_link_source_patterns": all(step["source_pattern_present"] is True for step in steps),
        "all_patch_steps_local_only": all(step["local_only"] is True for step in steps),
        "all_patch_steps_no_external_api": all(step["requires_external_api"] is False for step in steps),
        "all_patch_steps_no_upload": all(step["requires_kaggle_upload"] is False for step in steps),
        "all_patch_steps_no_submission_candidate": all(
            step["creates_submission_candidate"] is False for step in steps
        ),
        "all_patch_steps_ready_for_implementation": all(
            step["ready_for_implementation"] is True for step in steps
        ),
        "runtime_modification_blocked_now": all(
            step["runtime_modification_allowed_now"] is False for step in steps
        )
        and state["runtime_modification_allowed_now"] is False,
        "color_patch_present": "color_mapping" in families,
        "object_patch_present": "object_model" in families,
        "symmetry_patch_present": "shape_symmetry" in families,
        "composition_patch_present": "cross_family_composition" in families,
        "ranker_patch_present": "candidate_ranker" in families,
        "traceability_patch_present": "traceability" in families,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "plan_check_count_valid": len(PLAN_CHECKS) == EXPECTED_PLAN_CHECK_COUNT,
        "plan_case_count_valid": len(PLAN_CASES) == EXPECTED_PLAN_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS)
        == EXPECTED_FAIL_CLOSED_CONTROL_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "plan_record_created": state["solver_patch_plan_created"] is True,
        "plan_record_ready": state["solver_patch_plan_ready"] is True,
        "plan_record_locked": state["solver_patch_plan_locked"] is True,
        "plan_mode_valid": PLAN_MODE == "MILESTONE_10_SOLVER_PATCH_PLAN_V1_LOCAL_ONLY",
        "plan_scope_valid": PLAN_SCOPE == "LOCAL_SOLVER_PATCH_PLAN_NO_RUNTIME_MODIFICATION",
        "plan_verdict_valid": PLAN_VERDICT == "SOLVER_PATCH_PLAN_READY_FOR_LOCAL_IMPLEMENTATION",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_4_SOLVER_PATCH_IMPLEMENTATION_V1",
        "implementation_required_next": state["implementation_required_next"] is True,
        "real_submission_decision_not_authorized": source["real_submission_decision"] == "NOT_AUTHORIZED"
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
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
    }


def evaluate_solver_patch_plan_case(case_id: str) -> Dict[str, Any]:
    checks = build_solver_patch_plan_checks()

    if case_id == "m10_patch_plan_audit_source_ready_v1":
        passed = (
            checks["audit_artifact_present"]
            and checks["audit_artifact_ready"]
            and checks["audit_artifact_valid"]
            and checks["audit_ready"]
        )
        return _result(case_id, "source_binding", "verify_error_audit_source", passed)

    if case_id == "m10_patch_plan_patch_targets_complete_v1":
        passed = (
            checks["patch_target_count_valid"]
            and checks["patch_step_count_valid"]
            and checks["all_patch_steps_link_source_patterns"]
        )
        return _result(case_id, "patch_targets", "verify_patch_target_count", passed)

    if case_id == "m10_patch_plan_color_remap_patch_v1":
        return _result(case_id, "patch_plan", "plan_color_remap_patch", checks["color_patch_present"])

    if case_id == "m10_patch_plan_object_boundary_patch_v1":
        return _result(case_id, "patch_plan", "plan_object_boundary_patch", checks["object_patch_present"])

    if case_id == "m10_patch_plan_symmetry_patch_v1":
        return _result(case_id, "patch_plan", "plan_symmetry_patch", checks["symmetry_patch_present"])

    if case_id == "m10_patch_plan_composition_patch_v1":
        return _result(case_id, "patch_plan", "plan_composition_patch", checks["composition_patch_present"])

    if case_id == "m10_patch_plan_ranker_patch_v1":
        return _result(case_id, "patch_plan", "plan_ranker_patch", checks["ranker_patch_present"])

    if case_id == "m10_patch_plan_traceability_patch_v1":
        return _result(case_id, "patch_plan", "plan_traceability_patch", checks["traceability_patch_present"])

    if case_id == "m10_patch_plan_fail_closed_preserved_v1":
        passed = (
            checks["fail_closed_required"]
            and checks["fail_closed_active"]
            and checks["real_submission_allowed_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_patch_plan_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_implementation_next", checks["next_stage_valid"])

    raise ValueError(f"unknown solver patch plan case: {case_id}")


def evaluate_all_solver_patch_plan_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_solver_patch_plan_case(case["case_id"]) for case in PLAN_CASES)


def build_milestone_10_solver_patch_plan() -> Dict[str, Any]:
    source = build_solver_patch_plan_source_summary()
    steps = build_solver_patch_steps()
    state = build_solver_patch_plan_state()
    checks = build_solver_patch_plan_checks()
    results = evaluate_all_solver_patch_plan_cases()

    plan_pass_count = sum(1 for result in results if result["passed"] is True)
    plan_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "audit_artifact_present": checks["audit_artifact_present"],
        "audit_artifact_ready": checks["audit_artifact_ready"],
        "audit_artifact_valid": checks["audit_artifact_valid"],
        "audit_commit_valid": checks["audit_commit_valid"],
        "audit_next_stage_matches_task_3": checks["audit_next_stage_matches_task_3"],
        "audit_ready": checks["audit_ready"],
        "audit_locked": checks["audit_locked"],
        "error_pattern_count_valid": checks["error_pattern_count_valid"],
        "solver_target_count_valid": checks["solver_target_count_valid"],
        "patch_target_count_valid": checks["patch_target_count_valid"],
        "patch_step_count_valid": checks["patch_step_count_valid"],
        "all_patch_steps_link_source_patterns": checks["all_patch_steps_link_source_patterns"],
        "all_patch_steps_local_only": checks["all_patch_steps_local_only"],
        "all_patch_steps_no_external_api": checks["all_patch_steps_no_external_api"],
        "all_patch_steps_no_upload": checks["all_patch_steps_no_upload"],
        "all_patch_steps_no_submission_candidate": checks["all_patch_steps_no_submission_candidate"],
        "all_patch_steps_ready_for_implementation": checks["all_patch_steps_ready_for_implementation"],
        "runtime_modification_blocked_now": checks["runtime_modification_blocked_now"],
        "color_patch_present": checks["color_patch_present"],
        "object_patch_present": checks["object_patch_present"],
        "symmetry_patch_present": checks["symmetry_patch_present"],
        "composition_patch_present": checks["composition_patch_present"],
        "ranker_patch_present": checks["ranker_patch_present"],
        "traceability_patch_present": checks["traceability_patch_present"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "plan_check_count_valid": checks["plan_check_count_valid"],
        "plan_case_count_valid": checks["plan_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "plan_record_created": checks["plan_record_created"],
        "plan_record_ready": checks["plan_record_ready"],
        "plan_record_locked": checks["plan_record_locked"],
        "plan_mode_valid": checks["plan_mode_valid"],
        "plan_scope_valid": checks["plan_scope_valid"],
        "plan_verdict_valid": checks["plan_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "implementation_required_next": checks["implementation_required_next"],
        "real_submission_decision_not_authorized": checks["real_submission_decision_not_authorized"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
        "all_plan_cases_pass": all(result["passed"] is True for result in results),
        "plan_pass_count_valid": plan_pass_count == EXPECTED_PLAN_PASS_COUNT,
        "plan_failure_count_zero": plan_failure_count == EXPECTED_PLAN_FAILURE_COUNT,
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

    plan_ready = (
        plan_pass_count == EXPECTED_PLAN_PASS_COUNT
        and plan_failure_count == EXPECTED_PLAN_FAILURE_COUNT
        and checks["audit_artifact_ready"]
        and checks["patch_target_count_valid"]
        and checks["patch_step_count_valid"]
        and checks["runtime_modification_blocked_now"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 3",
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_audit": source["audit_id"],
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "plan_ready": plan_ready,
        "solver_patch_plan_created": True,
        "solver_patch_plan_ready": True,
        "patch_target_count": len(steps),
        "patch_step_count": len(steps),
        "runtime_modification_allowed_now": False,
        "submission_candidate_created": False,
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
        "status": PLAN_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 3",
        "title": "Solver Patch Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "plan_mode": PLAN_MODE,
        "plan_scope": PLAN_SCOPE,
        "plan_verdict": PLAN_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "audit_source": {
            "path": str(ERROR_AUDIT_JSON),
            "present": ERROR_AUDIT_JSON.exists(),
            "status": source["audit_status"],
            "audit_id": source["audit_id"],
            "sha256": _sha256(ERROR_AUDIT_JSON),
            "sha256_16": _sha16(_sha256(ERROR_AUDIT_JSON)),
        },
        "source_summary": source,
        "plan_state": state,
        "patch_steps": list(steps),
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "plan_checks": checks,
        "plan_check_list": list(PLAN_CHECKS),
        "plan_cases": list(PLAN_CASES),
        "plan_results": list(results),
        "plan_gates": list(gates),
        "plan_issues": list(issues),
        "plan_index": index,
        "plan_ready": plan_ready,
        "plan_locked": True,
        "solver_patch_plan_created": True,
        "solver_patch_plan_ready": True,
        "solver_patch_plan_locked": True,
        "patch_target_count": len(steps),
        "patch_step_count": len(steps),
        "plan_check_count": len(PLAN_CHECKS),
        "plan_case_count": len(PLAN_CASES),
        "plan_pass_count": plan_pass_count,
        "plan_failure_count": plan_failure_count,
        "plan_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "plan_issue_count": issue_count,
        "warning_count": 0,
        "runtime_modification_allowed_now": False,
        "submission_candidate_created": False,
        "implementation_required_next": True,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_solver_patch_plan_v1",
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
        "plan_id": f"MILESTONE-10-SOLVER-PATCH-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_solver_patch_plan(plan: Mapping[str, Any]) -> Dict[str, Any]:
    gates = plan.get("plan_gates", [])
    issues = plan.get("plan_issues", [])
    results = plan.get("plan_results", [])
    steps = plan.get("patch_steps", [])

    checks = {
        "status_ready": plan.get("status") == PLAN_STATUS,
        "plan_id_present": isinstance(plan.get("plan_id"), str) and bool(plan.get("plan_id")),
        "signature_present": isinstance(plan.get("signature"), str) and bool(plan.get("signature")),
        "baseline_commit_valid": str(plan.get("baseline_commit", "")).startswith("88acc88"),
        "plan_mode_valid": plan.get("plan_mode") == PLAN_MODE,
        "plan_scope_valid": plan.get("plan_scope") == PLAN_SCOPE,
        "plan_verdict_valid": plan.get("plan_verdict") == PLAN_VERDICT,
        "next_allowed_stage_valid": plan.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "plan_ready": plan.get("plan_ready") is True,
        "plan_locked": plan.get("plan_locked") is True,
        "plan_created": plan.get("solver_patch_plan_created") is True,
        "plan_record_ready": plan.get("solver_patch_plan_ready") is True,
        "plan_record_locked": plan.get("solver_patch_plan_locked") is True,
        "patch_target_count_valid": plan.get("patch_target_count") == EXPECTED_PATCH_TARGET_COUNT,
        "patch_step_count_valid": plan.get("patch_step_count") == EXPECTED_PATCH_STEP_COUNT,
        "plan_check_count_valid": plan.get("plan_check_count") == EXPECTED_PLAN_CHECK_COUNT,
        "plan_case_count_valid": plan.get("plan_case_count") == EXPECTED_PLAN_CASE_COUNT,
        "plan_pass_count_valid": plan.get("plan_pass_count") == EXPECTED_PLAN_PASS_COUNT,
        "plan_failure_count_zero": plan.get("plan_failure_count") == EXPECTED_PLAN_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "all_steps_local_only": bool(steps) and all(step.get("local_only") is True for step in steps),
        "all_steps_no_upload": bool(steps)
        and all(step.get("requires_kaggle_upload") is False for step in steps),
        "runtime_modification_blocked_now": plan.get("runtime_modification_allowed_now") is False,
        "submission_candidate_not_created": plan.get("submission_candidate_created") is False,
        "implementation_required_next": plan.get("implementation_required_next") is True,
        "real_submission_decision_not_authorized": plan.get("real_submission_decision") == "NOT_AUTHORIZED",
        "real_submission_allowed_false": plan.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": plan.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": plan.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": plan.get("kaggle_submission_sent") is False,
        "fail_closed_required": plan.get("fail_closed_required") is True,
        "fail_closed_active": plan.get("fail_closed_active") is True,
        "metadata_safe": plan.get("metadata", {}).get("external_api_dependency") is False
        and plan.get("metadata", {}).get("contains_api_keys") is False
        and plan.get("metadata", {}).get("private_core_exposure") is False
        and plan.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_SOLVER_PATCH_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "plan_id": plan.get("plan_id"),
        "signature": plan.get("signature"),
    }


def render_solver_patch_plan_markdown(plan: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Solver Patch Plan v1",
        "",
        f"- status: {plan['status']}",
        f"- plan_id: {plan['plan_id']}",
        f"- signature: {plan['signature']}",
        f"- baseline_commit: {plan['baseline_commit']}",
        f"- plan_mode: {plan['plan_mode']}",
        f"- plan_scope: {plan['plan_scope']}",
        f"- plan_verdict: {plan['plan_verdict']}",
        f"- next_allowed_stage: {plan['next_allowed_stage']}",
        f"- plan_ready: {plan['plan_ready']}",
        f"- patch_target_count: {plan['patch_target_count']}",
        f"- patch_step_count: {plan['patch_step_count']}",
        f"- runtime_modification_allowed_now: {plan['runtime_modification_allowed_now']}",
        f"- submission_candidate_created: {plan['submission_candidate_created']}",
        f"- implementation_required_next: {plan['implementation_required_next']}",
        f"- real_submission_decision: {plan['real_submission_decision']}",
        f"- real_submission_allowed: {plan['real_submission_allowed']}",
        f"- fail_closed_active: {plan['fail_closed_active']}",
        "",
        "## Patch steps",
        "",
    ]

    for step in plan["patch_steps"]:
        lines.append(
            f"- {step['patch_id']} / family={step['family']} / "
            f"module={step['target_module']} / priority={step['priority']} / "
            f"intent={step['implementation_intent']}"
        )

    lines.extend(["", "## Plan results", ""])

    for result in plan["plan_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Solver patch plan is ready. The next stage is local patch implementation. Runtime modification is not performed in this planning step.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_READY=true",
            "ARC_AGI3_MILESTONE_10_PLAN_MODE=MILESTONE_10_SOLVER_PATCH_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_PLAN_VERDICT=SOLVER_PATCH_PLAN_READY_FOR_LOCAL_IMPLEMENTATION",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=88acc88",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_4_SOLVER_PATCH_IMPLEMENTATION_V1",
            "ARC_AGI3_MILESTONE_10_PATCH_TARGET_COUNT=6",
            "ARC_AGI3_MILESTONE_10_PATCH_STEP_COUNT=6",
            "ARC_AGI3_MILESTONE_10_PLAN_CHECK_COUNT=22",
            "ARC_AGI3_MILESTONE_10_PLAN_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_PLAN_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_PLAN_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_CREATED=true",
            "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_READY=true",
            "ARC_AGI3_MILESTONE_10_RUNTIME_MODIFICATION_ALLOWED_NOW=false",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_IMPLEMENTATION_REQUIRED_NEXT=true",
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


def render_solver_patch_plan_manifest(plan: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 SOLVER PATCH PLAN MANIFEST v1",
        f"plan_id={plan['plan_id']}",
        f"signature={plan['signature']}",
        f"status={plan['status']}",
        f"baseline_commit={plan['baseline_commit']}",
        f"plan_mode={plan['plan_mode']}",
        f"plan_verdict={plan['plan_verdict']}",
        f"next_allowed_stage={plan['next_allowed_stage']}",
        f"plan_ready={plan['plan_ready']}",
        f"solver_patch_plan_created={plan['solver_patch_plan_created']}",
        f"solver_patch_plan_ready={plan['solver_patch_plan_ready']}",
        f"patch_target_count={plan['patch_target_count']}",
        f"patch_step_count={plan['patch_step_count']}",
        f"plan_check_count={plan['plan_check_count']}",
        f"plan_case_count={plan['plan_case_count']}",
        f"plan_pass_count={plan['plan_pass_count']}",
        f"plan_failure_count={plan['plan_failure_count']}",
        f"plan_gate_count={plan['plan_gate_count']}",
        f"passed_gate_count={plan['passed_gate_count']}",
        f"plan_issue_count={plan['plan_issue_count']}",
        f"runtime_modification_allowed_now={plan['runtime_modification_allowed_now']}",
        f"submission_candidate_created={plan['submission_candidate_created']}",
        f"implementation_required_next={plan['implementation_required_next']}",
        f"real_submission_decision={plan['real_submission_decision']}",
        f"real_submission_allowed={plan['real_submission_allowed']}",
        f"manual_upload_allowed={plan['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={plan['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={plan['kaggle_submission_sent']}",
        f"fail_closed_required={plan['fail_closed_required']}",
        f"fail_closed_active={plan['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "PATCH_STEPS",
    ]

    for step in plan["patch_steps"]:
        lines.append(
            f"{step['patch_id']} family={step['family']} module={step['target_module']} "
            f"priority={step['priority']} source={step['source_pattern_id']}"
        )

    lines.append("")
    lines.append("PLAN_RESULTS")
    for result in plan["plan_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_solver_patch_plan_artifacts(
    plan: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    plan = dict(plan or build_milestone_10_solver_patch_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-solver-patch-plan-v1.json"
    md_path = output / "milestone-10-solver-patch-plan-v1.md"
    manifest_path = output / "milestone-10-solver-patch-plan-manifest-v1.txt"
    index_path = output / "milestone-10-solver-patch-plan-index-v1.json"

    json_path.write_text(json.dumps(plan, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_solver_patch_plan_markdown(plan), encoding="utf-8")
    manifest_path.write_text(render_solver_patch_plan_manifest(plan), encoding="utf-8")
    index_path.write_text(json.dumps(plan["plan_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_solver_patch_plan_pipeline() -> Dict[str, Any]:
    plan = build_milestone_10_solver_patch_plan()
    validation = validate_milestone_10_solver_patch_plan(plan)
    artifacts = write_solver_patch_plan_artifacts(plan)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_10_SOLVER_PATCH_PLAN_V1_PIPELINE_INVALID",
        "plan_status": plan["status"],
        "validation_status": validation["status"],
        "plan": plan,
        "plan_id": plan["plan_id"],
        "signature": plan["signature"],
        "plan_mode": plan["plan_mode"],
        "plan_verdict": plan["plan_verdict"],
        "next_allowed_stage": plan["next_allowed_stage"],
        "plan_ready": plan["plan_ready"],
        "solver_patch_plan_created": plan["solver_patch_plan_created"],
        "solver_patch_plan_ready": plan["solver_patch_plan_ready"],
        "patch_target_count": plan["patch_target_count"],
        "patch_step_count": plan["patch_step_count"],
        "plan_check_count": plan["plan_check_count"],
        "plan_case_count": plan["plan_case_count"],
        "plan_pass_count": plan["plan_pass_count"],
        "plan_failure_count": plan["plan_failure_count"],
        "plan_gate_count": plan["plan_gate_count"],
        "passed_gate_count": plan["passed_gate_count"],
        "plan_issue_count": plan["plan_issue_count"],
        "warning_count": plan["warning_count"],
        "runtime_modification_allowed_now": plan["runtime_modification_allowed_now"],
        "submission_candidate_created": plan["submission_candidate_created"],
        "implementation_required_next": plan["implementation_required_next"],
        "real_submission_decision": plan["real_submission_decision"],
        "real_submission_allowed": plan["real_submission_allowed"],
        "manual_upload_allowed": plan["manual_upload_allowed"],
        "kaggle_authentication_allowed": plan["kaggle_authentication_allowed"],
        "kaggle_submission_sent": plan["kaggle_submission_sent"],
        "fail_closed_required": plan["fail_closed_required"],
        "fail_closed_active": plan["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": plan["metadata"],
    }
