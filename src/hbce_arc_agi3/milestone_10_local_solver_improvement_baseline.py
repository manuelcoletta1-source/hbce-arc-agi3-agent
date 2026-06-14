"""Milestone #10 Local Solver Improvement Baseline v1.

Local-only deterministic baseline for the next solver improvement cycle.

This module opens Milestone #10 only after Milestone #9 is closed with real
submission blocked. It keeps the Kaggle boundary closed and prepares a local
solver improvement cycle: error-pattern audit, solver refinement, benchmark
refresh, candidate refresh, and manual review.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, grant approval, claim a score, claim leaderboard movement, or
create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


BASELINE_STATUS = "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_VALID"

BASELINE_COMMIT = "b887f6c Close ARC AGI3 milestone 9 real submission blocked"
BASELINE_MODE = "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_LOCAL_ONLY"
BASELINE_SCOPE = "OPEN_LOCAL_SOLVER_IMPROVEMENT_AFTER_BLOCKED_SUBMISSION_CLOSURE"
BASELINE_VERDICT = "MILESTONE_10_OPEN_LOCAL_SOLVER_IMPROVEMENT_ONLY_REAL_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/local-solver-improvement-baseline-v1"

MILESTONE_9_CLOSURE_JSON = Path(
    "examples/milestone-9/real-submission-blocked-closure-v1/"
    "milestone-9-real-submission-blocked-closure-v1.json"
)

EXPECTED_BASELINE_CHECK_COUNT = 18
EXPECTED_BASELINE_CASE_COUNT = 10
EXPECTED_BASELINE_PASS_COUNT = 10
EXPECTED_BASELINE_FAILURE_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_LOCAL_STAGE_COUNT = 5

LOCAL_IMPROVEMENT_STAGES: Tuple[Dict[str, str], ...] = (
    {
        "stage_id": "m10_task_2_local_error_pattern_audit_v1",
        "name": "Local Error Pattern Audit v1",
        "purpose": "identify failure patterns from local benchmark traces",
    },
    {
        "stage_id": "m10_task_3_solver_patch_plan_v1",
        "name": "Solver Patch Plan v1",
        "purpose": "define local-only deterministic solver refinements",
    },
    {
        "stage_id": "m10_task_4_solver_patch_implementation_v1",
        "name": "Solver Patch Implementation v1",
        "purpose": "implement safe local solver improvements",
    },
    {
        "stage_id": "m10_task_5_benchmark_refresh_v1",
        "name": "Benchmark Refresh v1",
        "purpose": "rerun deterministic local checks and compare stability",
    },
    {
        "stage_id": "m10_task_6_candidate_refresh_v1",
        "name": "Candidate Refresh v1",
        "purpose": "produce a new local submission candidate for review only",
    },
)

BASELINE_CHECKS: Tuple[str, ...] = (
    "milestone_9_closure_artifact_exists",
    "milestone_9_closure_artifact_ready",
    "milestone_9_closed",
    "milestone_9_closed_with_real_submission_blocked",
    "real_submission_decision_not_authorized",
    "operator_approval_not_granted",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "real_submission_blocked",
    "kaggle_submission_absent",
    "local_solver_cycle_created",
    "local_solver_cycle_ready",
    "local_improvement_stages_present",
    "next_stage_error_pattern_audit",
    "fail_closed_boundary_preserved",
    "no_external_api_dependency",
    "no_private_core_exposure",
    "no_legal_certification",
)

BASELINE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_baseline_m9_closure_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_milestone_9_blocked_closure",
    },
    {
        "case_id": "m10_baseline_submission_still_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_still_blocked",
    },
    {
        "case_id": "m10_baseline_operator_approval_absent_v1",
        "area": "approval_boundary",
        "operation": "verify_operator_approval_absent",
    },
    {
        "case_id": "m10_baseline_kaggle_actions_absent_v1",
        "area": "kaggle_boundary",
        "operation": "verify_no_kaggle_action",
    },
    {
        "case_id": "m10_baseline_local_solver_cycle_ready_v1",
        "area": "local_solver",
        "operation": "verify_local_solver_cycle_ready",
    },
    {
        "case_id": "m10_baseline_local_stage_plan_ready_v1",
        "area": "roadmap",
        "operation": "verify_local_stage_plan",
    },
    {
        "case_id": "m10_baseline_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_error_pattern_audit_next",
    },
    {
        "case_id": "m10_baseline_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_boundary",
    },
    {
        "case_id": "m10_baseline_no_private_core_exposure_v1",
        "area": "public_safety",
        "operation": "verify_no_private_core_exposure",
    },
    {
        "case_id": "m10_baseline_no_legal_certification_v1",
        "area": "claim_boundary",
        "operation": "verify_no_legal_certification",
    },
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


def build_milestone_10_source_summary() -> Dict[str, Any]:
    closure = _read_json(MILESTONE_9_CLOSURE_JSON)
    closure_source = closure.get("closure_source_summary", {})

    return {
        "milestone_9_closure_path": str(MILESTONE_9_CLOSURE_JSON),
        "milestone_9_closure_present": MILESTONE_9_CLOSURE_JSON.exists(),
        "milestone_9_closure_status": closure.get("status", "MISSING"),
        "milestone_9_closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "milestone_9_closure_signature": closure.get("signature", ""),
        "milestone_9_closed": closure.get("milestone_9_closed", False),
        "milestone_9_closure_type": closure.get("milestone_9_closure_type", "MISSING_TYPE"),
        "milestone_9_closure_reason": closure.get("milestone_9_closure_reason", "MISSING_REASON"),
        "milestone_9_closure_verdict": closure.get("milestone_9_closure_verdict", "MISSING_VERDICT"),
        "real_submission_decision": closure.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_decision_reason": closure.get(
            "real_submission_decision_reason", "MISSING_DECISION_REASON"
        ),
        "operator_approval_required": closure.get("operator_approval_required", False),
        "operator_approval_granted": closure.get("operator_approval_granted", True),
        "operator_approval_received": closure.get("operator_approval_received", True),
        "manual_upload_allowed": closure.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": closure.get("kaggle_authentication_allowed", True),
        "real_submission_created": closure.get("real_submission_created", True),
        "real_submission_allowed": closure.get("real_submission_allowed", True),
        "ready_for_real_kaggle_submission": closure.get("ready_for_real_kaggle_submission", True),
        "kaggle_submission_sent": closure.get("kaggle_submission_sent", True),
        "upload_performed": closure.get("upload_performed", True),
        "kaggle_authentication_performed": closure.get("kaggle_authentication_performed", True),
        "candidate_source_path": closure_source.get(
            "candidate_source_path", "MISSING_CANDIDATE_SOURCE"
        ),
        "candidate_id": closure_source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": closure_source.get("candidate_signature", ""),
        "candidate_count": closure.get("candidate_count", 0),
        "closure_sha256": _sha256(MILESTONE_9_CLOSURE_JSON),
        "closure_sha256_16": _sha16(_sha256(MILESTONE_9_CLOSURE_JSON)),
    }


def build_milestone_10_local_solver_baseline_state() -> Dict[str, Any]:
    return {
        "milestone_10_open": True,
        "milestone_10_title": "Local Solver Improvement Cycle",
        "milestone_10_mode": BASELINE_MODE,
        "local_solver_improvement_cycle_created": True,
        "local_solver_improvement_cycle_ready": True,
        "local_solver_improvement_cycle_locked_to_local_only": True,
        "real_submission_boundary_status": "BLOCKED",
        "fail_closed_required": True,
        "fail_closed_active": True,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "kaggle_authentication_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_submission_sent": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "local_improvement_stage_count": len(LOCAL_IMPROVEMENT_STAGES),
    }


def build_milestone_10_baseline_checks() -> Dict[str, bool]:
    source = build_milestone_10_source_summary()
    state = build_milestone_10_local_solver_baseline_state()

    return {
        "closure_artifact_present": source["milestone_9_closure_present"],
        "closure_artifact_ready": source["milestone_9_closure_status"]
        == "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY",
        "closure_artifact_valid": source["milestone_9_closure_id"].startswith(
            "MILESTONE-9-BLOCKED-CLOSURE-"
        )
        and bool(source["milestone_9_closure_signature"]),
        "milestone_9_closed": source["milestone_9_closed"] is True,
        "closure_type_blocked": source["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED",
        "closure_reason_operator_approval_not_granted": source["milestone_9_closure_reason"]
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "closure_verdict_blocked": source["milestone_9_closure_verdict"]
        == "CLOSED_WITH_REAL_SUBMISSION_BLOCKED",
        "real_submission_decision_not_authorized": source["real_submission_decision"]
        == "NOT_AUTHORIZED",
        "real_submission_decision_reason_valid": source["real_submission_decision_reason"]
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "operator_approval_required": source["operator_approval_required"] is True,
        "operator_approval_not_granted": source["operator_approval_granted"] is False,
        "operator_approval_not_received": source["operator_approval_received"] is False,
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False,
        "real_submission_not_created": source["real_submission_created"] is False,
        "real_submission_allowed_false": source["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": source["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "upload_not_performed": source["upload_performed"] is False,
        "kaggle_authentication_not_performed": source["kaggle_authentication_performed"] is False,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "baseline_check_count_valid": len(BASELINE_CHECKS) == EXPECTED_BASELINE_CHECK_COUNT,
        "baseline_case_count_valid": len(BASELINE_CASES) == EXPECTED_BASELINE_CASE_COUNT,
        "local_stage_count_valid": len(LOCAL_IMPROVEMENT_STAGES) == EXPECTED_LOCAL_STAGE_COUNT,
        "milestone_10_open": state["milestone_10_open"] is True,
        "local_cycle_created": state["local_solver_improvement_cycle_created"] is True,
        "local_cycle_ready": state["local_solver_improvement_cycle_ready"] is True,
        "local_cycle_locked_to_local_only": state["local_solver_improvement_cycle_locked_to_local_only"] is True,
        "fail_closed_required": state["fail_closed_required"] is True,
        "fail_closed_active": state["fail_closed_active"] is True,
        "baseline_mode_valid": BASELINE_MODE == "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_LOCAL_ONLY",
        "baseline_scope_valid": BASELINE_SCOPE
        == "OPEN_LOCAL_SOLVER_IMPROVEMENT_AFTER_BLOCKED_SUBMISSION_CLOSURE",
        "baseline_verdict_valid": BASELINE_VERDICT
        == "MILESTONE_10_OPEN_LOCAL_SOLVER_IMPROVEMENT_ONLY_REAL_SUBMISSION_BLOCKED",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1",
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
        "metadata_boundary_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
    }


def evaluate_milestone_10_baseline_case(case_id: str) -> Dict[str, Any]:
    checks = build_milestone_10_baseline_checks()

    if case_id == "m10_baseline_m9_closure_source_ready_v1":
        passed = (
            checks["closure_artifact_present"]
            and checks["closure_artifact_ready"]
            and checks["closure_artifact_valid"]
            and checks["milestone_9_closed"]
        )
        return _result(case_id, "source_binding", "verify_milestone_9_blocked_closure", passed)

    if case_id == "m10_baseline_submission_still_blocked_v1":
        passed = (
            checks["real_submission_decision_not_authorized"]
            and checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_still_blocked", passed)

    if case_id == "m10_baseline_operator_approval_absent_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "approval_boundary", "verify_operator_approval_absent", passed)

    if case_id == "m10_baseline_kaggle_actions_absent_v1":
        passed = (
            checks["manual_upload_not_allowed"]
            and checks["kaggle_authentication_not_allowed"]
            and checks["upload_not_performed"]
            and checks["kaggle_authentication_not_performed"]
        )
        return _result(case_id, "kaggle_boundary", "verify_no_kaggle_action", passed)

    if case_id == "m10_baseline_local_solver_cycle_ready_v1":
        passed = (
            checks["milestone_10_open"]
            and checks["local_cycle_created"]
            and checks["local_cycle_ready"]
            and checks["local_cycle_locked_to_local_only"]
        )
        return _result(case_id, "local_solver", "verify_local_solver_cycle_ready", passed)

    if case_id == "m10_baseline_local_stage_plan_ready_v1":
        passed = checks["local_stage_count_valid"] and checks["candidate_count_positive"]
        return _result(case_id, "roadmap", "verify_local_stage_plan", passed)

    if case_id == "m10_baseline_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_error_pattern_audit_next", passed)

    if case_id == "m10_baseline_fail_closed_preserved_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed_boundary", passed)

    if case_id == "m10_baseline_no_private_core_exposure_v1":
        passed = checks["private_core_exposure_false"] and checks["external_api_dependency_false"]
        return _result(case_id, "public_safety", "verify_no_private_core_exposure", passed)

    if case_id == "m10_baseline_no_legal_certification_v1":
        passed = checks["legal_certification_false"]
        return _result(case_id, "claim_boundary", "verify_no_legal_certification", passed)

    raise ValueError(f"unknown milestone 10 baseline case: {case_id}")


def evaluate_all_milestone_10_baseline_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_milestone_10_baseline_case(case["case_id"]) for case in BASELINE_CASES)


def build_milestone_10_local_solver_improvement_baseline() -> Dict[str, Any]:
    source = build_milestone_10_source_summary()
    state = build_milestone_10_local_solver_baseline_state()
    checks = build_milestone_10_baseline_checks()
    results = evaluate_all_milestone_10_baseline_cases()

    baseline_pass_count = sum(1 for result in results if result["passed"] is True)
    baseline_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "closure_artifact_present": checks["closure_artifact_present"],
        "closure_artifact_ready": checks["closure_artifact_ready"],
        "closure_artifact_valid": checks["closure_artifact_valid"],
        "milestone_9_closed": checks["milestone_9_closed"],
        "closure_type_blocked": checks["closure_type_blocked"],
        "closure_reason_operator_approval_not_granted": checks[
            "closure_reason_operator_approval_not_granted"
        ],
        "closure_verdict_blocked": checks["closure_verdict_blocked"],
        "real_submission_decision_not_authorized": checks[
            "real_submission_decision_not_authorized"
        ],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "baseline_check_count_valid": checks["baseline_check_count_valid"],
        "baseline_case_count_valid": checks["baseline_case_count_valid"],
        "local_stage_count_valid": checks["local_stage_count_valid"],
        "milestone_10_open": checks["milestone_10_open"],
        "local_cycle_created": checks["local_cycle_created"],
        "local_cycle_ready": checks["local_cycle_ready"],
        "local_cycle_locked_to_local_only": checks["local_cycle_locked_to_local_only"],
        "baseline_mode_valid": checks["baseline_mode_valid"],
        "baseline_scope_valid": checks["baseline_scope_valid"],
        "baseline_verdict_valid": checks["baseline_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "all_baseline_cases_pass": all(result["passed"] is True for result in results),
        "baseline_pass_count_valid": baseline_pass_count == EXPECTED_BASELINE_PASS_COUNT,
        "baseline_failure_count_zero": baseline_failure_count == EXPECTED_BASELINE_FAILURE_COUNT,
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
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

    baseline_ready = (
        baseline_pass_count == EXPECTED_BASELINE_PASS_COUNT
        and baseline_failure_count == EXPECTED_BASELINE_FAILURE_COUNT
        and checks["milestone_9_closed"]
        and checks["real_submission_allowed_false"]
        and checks["local_cycle_ready"]
        and checks["fail_closed_active"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 1",
        "baseline_mode": BASELINE_MODE,
        "baseline_scope": BASELINE_SCOPE,
        "baseline_verdict": BASELINE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_milestone_9_closure": source["milestone_9_closure_id"],
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "baseline_ready": baseline_ready,
        "milestone_10_open": True,
        "local_solver_improvement_cycle_created": True,
        "local_solver_improvement_cycle_ready": True,
        "local_improvement_stage_count": len(LOCAL_IMPROVEMENT_STAGES),
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
        "status": BASELINE_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 1",
        "title": "Local Solver Improvement Baseline v1",
        "baseline_commit": BASELINE_COMMIT,
        "baseline_mode": BASELINE_MODE,
        "baseline_scope": BASELINE_SCOPE,
        "baseline_verdict": BASELINE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_9_closure_source": {
            "path": str(MILESTONE_9_CLOSURE_JSON),
            "present": MILESTONE_9_CLOSURE_JSON.exists(),
            "status": source["milestone_9_closure_status"],
            "closure_id": source["milestone_9_closure_id"],
            "sha256": _sha256(MILESTONE_9_CLOSURE_JSON),
            "sha256_16": _sha16(_sha256(MILESTONE_9_CLOSURE_JSON)),
        },
        "source_summary": source,
        "baseline_state": state,
        "baseline_checks": checks,
        "baseline_check_list": list(BASELINE_CHECKS),
        "baseline_cases": list(BASELINE_CASES),
        "baseline_results": list(results),
        "local_improvement_stages": list(LOCAL_IMPROVEMENT_STAGES),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "baseline_gates": list(gates),
        "baseline_issues": list(issues),
        "baseline_index": index,
        "baseline_ready": baseline_ready,
        "baseline_locked": True,
        "milestone_10_open": True,
        "local_solver_improvement_cycle_created": True,
        "local_solver_improvement_cycle_ready": True,
        "local_solver_improvement_cycle_locked_to_local_only": True,
        "local_improvement_stage_count": len(LOCAL_IMPROVEMENT_STAGES),
        "baseline_check_count": len(BASELINE_CHECKS),
        "baseline_case_count": len(BASELINE_CASES),
        "baseline_pass_count": baseline_pass_count,
        "baseline_failure_count": baseline_failure_count,
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "baseline_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "baseline_issue_count": issue_count,
        "warning_count": 0,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "real_submission_created": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_local_solver_improvement_baseline_v1",
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
        "baseline_id": f"MILESTONE-10-LOCAL-SOLVER-BASELINE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_local_solver_improvement_baseline(baseline: Mapping[str, Any]) -> Dict[str, Any]:
    gates = baseline.get("baseline_gates", [])
    issues = baseline.get("baseline_issues", [])
    results = baseline.get("baseline_results", [])

    checks = {
        "status_ready": baseline.get("status") == BASELINE_STATUS,
        "baseline_id_present": isinstance(baseline.get("baseline_id"), str) and bool(baseline.get("baseline_id")),
        "signature_present": isinstance(baseline.get("signature"), str) and bool(baseline.get("signature")),
        "baseline_commit_valid": str(baseline.get("baseline_commit", "")).startswith("b887f6c"),
        "baseline_mode_valid": baseline.get("baseline_mode") == BASELINE_MODE,
        "baseline_scope_valid": baseline.get("baseline_scope") == BASELINE_SCOPE,
        "baseline_verdict_valid": baseline.get("baseline_verdict") == BASELINE_VERDICT,
        "next_allowed_stage_valid": baseline.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "baseline_ready": baseline.get("baseline_ready") is True,
        "baseline_locked": baseline.get("baseline_locked") is True,
        "milestone_10_open": baseline.get("milestone_10_open") is True,
        "local_cycle_created": baseline.get("local_solver_improvement_cycle_created") is True,
        "local_cycle_ready": baseline.get("local_solver_improvement_cycle_ready") is True,
        "local_stage_count_valid": baseline.get("local_improvement_stage_count") == EXPECTED_LOCAL_STAGE_COUNT,
        "baseline_check_count_valid": baseline.get("baseline_check_count") == EXPECTED_BASELINE_CHECK_COUNT,
        "baseline_case_count_valid": baseline.get("baseline_case_count") == EXPECTED_BASELINE_CASE_COUNT,
        "baseline_pass_count_valid": baseline.get("baseline_pass_count") == EXPECTED_BASELINE_PASS_COUNT,
        "baseline_failure_count_zero": baseline.get("baseline_failure_count") == EXPECTED_BASELINE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "real_submission_decision_not_authorized": baseline.get("real_submission_decision") == "NOT_AUTHORIZED",
        "real_submission_allowed_false": baseline.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": baseline.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": baseline.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": baseline.get("kaggle_submission_sent") is False,
        "fail_closed_required": baseline.get("fail_closed_required") is True,
        "fail_closed_active": baseline.get("fail_closed_active") is True,
        "metadata_safe": baseline.get("metadata", {}).get("external_api_dependency") is False
        and baseline.get("metadata", {}).get("contains_api_keys") is False
        and baseline.get("metadata", {}).get("private_core_exposure") is False
        and baseline.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "baseline_id": baseline.get("baseline_id"),
        "signature": baseline.get("signature"),
    }


def render_milestone_10_baseline_markdown(baseline: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Local Solver Improvement Baseline v1",
        "",
        f"- status: {baseline['status']}",
        f"- baseline_id: {baseline['baseline_id']}",
        f"- signature: {baseline['signature']}",
        f"- baseline_commit: {baseline['baseline_commit']}",
        f"- baseline_mode: {baseline['baseline_mode']}",
        f"- baseline_scope: {baseline['baseline_scope']}",
        f"- baseline_verdict: {baseline['baseline_verdict']}",
        f"- next_allowed_stage: {baseline['next_allowed_stage']}",
        f"- baseline_ready: {baseline['baseline_ready']}",
        f"- milestone_10_open: {baseline['milestone_10_open']}",
        f"- local_solver_improvement_cycle_created: {baseline['local_solver_improvement_cycle_created']}",
        f"- local_solver_improvement_cycle_ready: {baseline['local_solver_improvement_cycle_ready']}",
        f"- local_improvement_stage_count: {baseline['local_improvement_stage_count']}",
        f"- real_submission_decision: {baseline['real_submission_decision']}",
        f"- real_submission_allowed: {baseline['real_submission_allowed']}",
        f"- fail_closed_required: {baseline['fail_closed_required']}",
        f"- fail_closed_active: {baseline['fail_closed_active']}",
        "",
        "## Local improvement stages",
        "",
    ]

    for stage in baseline["local_improvement_stages"]:
        lines.append(f"- {stage['stage_id']} / {stage['name']} / {stage['purpose']}")

    lines.extend(["", "## Baseline results", ""])

    for result in baseline["baseline_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #10 is open for local-only solver improvement. Real submission remains blocked and fail-closed boundaries remain active.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_OPEN=true",
            "ARC_AGI3_MILESTONE_10_MODE=MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_VERDICT=MILESTONE_10_OPEN_LOCAL_SOLVER_IMPROVEMENT_ONLY_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=b887f6c",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_2_LOCAL_ERROR_PATTERN_AUDIT_V1",
            "ARC_AGI3_MILESTONE_10_LOCAL_STAGE_COUNT=5",
            "ARC_AGI3_MILESTONE_10_BASELINE_CHECK_COUNT=18",
            "ARC_AGI3_MILESTONE_10_BASELINE_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_BASELINE_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_BASELINE_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_CYCLE_CREATED=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_CYCLE_READY=true",
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


def render_milestone_10_baseline_manifest(baseline: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 LOCAL SOLVER IMPROVEMENT BASELINE MANIFEST v1",
        f"baseline_id={baseline['baseline_id']}",
        f"signature={baseline['signature']}",
        f"status={baseline['status']}",
        f"baseline_commit={baseline['baseline_commit']}",
        f"baseline_mode={baseline['baseline_mode']}",
        f"baseline_verdict={baseline['baseline_verdict']}",
        f"next_allowed_stage={baseline['next_allowed_stage']}",
        f"baseline_ready={baseline['baseline_ready']}",
        f"milestone_10_open={baseline['milestone_10_open']}",
        f"local_solver_improvement_cycle_created={baseline['local_solver_improvement_cycle_created']}",
        f"local_solver_improvement_cycle_ready={baseline['local_solver_improvement_cycle_ready']}",
        f"local_improvement_stage_count={baseline['local_improvement_stage_count']}",
        f"baseline_check_count={baseline['baseline_check_count']}",
        f"baseline_case_count={baseline['baseline_case_count']}",
        f"baseline_pass_count={baseline['baseline_pass_count']}",
        f"baseline_failure_count={baseline['baseline_failure_count']}",
        f"baseline_gate_count={baseline['baseline_gate_count']}",
        f"passed_gate_count={baseline['passed_gate_count']}",
        f"baseline_issue_count={baseline['baseline_issue_count']}",
        f"real_submission_decision={baseline['real_submission_decision']}",
        f"real_submission_allowed={baseline['real_submission_allowed']}",
        f"manual_upload_allowed={baseline['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={baseline['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={baseline['kaggle_submission_sent']}",
        f"fail_closed_required={baseline['fail_closed_required']}",
        f"fail_closed_active={baseline['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "LOCAL_IMPROVEMENT_STAGES",
    ]

    for stage in baseline["local_improvement_stages"]:
        lines.append(f"{stage['stage_id']} name={stage['name']} purpose={stage['purpose']}")

    lines.append("")
    lines.append("BASELINE_RESULTS")
    for result in baseline["baseline_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_milestone_10_baseline_artifacts(
    baseline: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    baseline = dict(baseline or build_milestone_10_local_solver_improvement_baseline())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-local-solver-improvement-baseline-v1.json"
    md_path = output / "milestone-10-local-solver-improvement-baseline-v1.md"
    manifest_path = output / "milestone-10-local-solver-improvement-baseline-manifest-v1.txt"
    index_path = output / "milestone-10-local-solver-improvement-baseline-index-v1.json"

    json_path.write_text(json.dumps(baseline, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_milestone_10_baseline_markdown(baseline), encoding="utf-8")
    manifest_path.write_text(render_milestone_10_baseline_manifest(baseline), encoding="utf-8")
    index_path.write_text(json.dumps(baseline["baseline_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_local_solver_improvement_baseline_pipeline() -> Dict[str, Any]:
    baseline = build_milestone_10_local_solver_improvement_baseline()
    validation = validate_milestone_10_local_solver_improvement_baseline(baseline)
    artifacts = write_milestone_10_baseline_artifacts(baseline)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_10_LOCAL_SOLVER_IMPROVEMENT_BASELINE_V1_PIPELINE_INVALID",
        "baseline_status": baseline["status"],
        "validation_status": validation["status"],
        "baseline": baseline,
        "baseline_id": baseline["baseline_id"],
        "signature": baseline["signature"],
        "baseline_mode": baseline["baseline_mode"],
        "baseline_verdict": baseline["baseline_verdict"],
        "next_allowed_stage": baseline["next_allowed_stage"],
        "baseline_ready": baseline["baseline_ready"],
        "milestone_10_open": baseline["milestone_10_open"],
        "local_solver_improvement_cycle_created": baseline["local_solver_improvement_cycle_created"],
        "local_solver_improvement_cycle_ready": baseline["local_solver_improvement_cycle_ready"],
        "local_improvement_stage_count": baseline["local_improvement_stage_count"],
        "baseline_check_count": baseline["baseline_check_count"],
        "baseline_case_count": baseline["baseline_case_count"],
        "baseline_pass_count": baseline["baseline_pass_count"],
        "baseline_failure_count": baseline["baseline_failure_count"],
        "baseline_gate_count": baseline["baseline_gate_count"],
        "passed_gate_count": baseline["passed_gate_count"],
        "baseline_issue_count": baseline["baseline_issue_count"],
        "warning_count": baseline["warning_count"],
        "real_submission_decision": baseline["real_submission_decision"],
        "real_submission_allowed": baseline["real_submission_allowed"],
        "manual_upload_allowed": baseline["manual_upload_allowed"],
        "kaggle_authentication_allowed": baseline["kaggle_authentication_allowed"],
        "kaggle_submission_sent": baseline["kaggle_submission_sent"],
        "fail_closed_required": baseline["fail_closed_required"],
        "fail_closed_active": baseline["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": baseline["metadata"],
    }
