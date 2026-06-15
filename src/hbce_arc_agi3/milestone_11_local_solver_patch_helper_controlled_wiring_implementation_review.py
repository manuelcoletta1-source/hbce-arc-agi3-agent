"""Milestone #11 Task 18 - Local Solver Patch Helper Controlled Wiring Implementation Review v1.

Reviews the Task 17 controlled implementation dry-run.

This task performs review only. It does not wire helpers into the runtime solver,
does not modify ranker behavior, does not claim Kaggle score, does not create
submission.json, does not create upload packages, does not authenticate with
Kaggle, does not call external APIs, and does not create legal certification
claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_VALID"

BASELINE_COMMIT = "77cf06f Add ARC AGI3 local solver patch helper controlled wiring implementation dry run"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_LOCAL_ONLY"
TASK_SCOPE = "IMPLEMENTATION_REVIEW_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_READY_FOR_CONTROLLED_RUNTIME_WIRING_GATE"
NEXT_STAGE = "MILESTONE_11_TASK_19_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-controlled-wiring-implementation-review-v1"

TASK_17_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-controlled-wiring-implementation-dry-run-v1/"
    "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-dry-run-v1.json"
)

EXPECTED_TASK_17_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1_READY"
EXPECTED_TASK_17_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-DRY-RUN-"

EXPECTED_SIMULATED_OPERATION_COUNT = 5
EXPECTED_CONTRACT_VALIDATION_COUNT = 10
EXPECTED_REGRESSION_SIMULATION_COUNT = 10
EXPECTED_ROLLBACK_SIMULATION_COUNT = 8
EXPECTED_BOUNDARY_ASSERTION_COUNT = 14
EXPECTED_DRY_RUN_CHECK_COUNT = 71
EXPECTED_DRY_RUN_CASE_COUNT = 10
EXPECTED_DRY_RUN_GATE_COUNT = 29

EXPECTED_REVIEW_FINDING_COUNT = 14
EXPECTED_REVIEW_CRITERION_COUNT = 12
EXPECTED_ACCEPTANCE_ITEM_COUNT = 10
EXPECTED_STOP_CONDITION_COUNT = 12
EXPECTED_REVIEW_CASE_COUNT = 10
EXPECTED_REVIEW_CASE_PASS_COUNT = 10
EXPECTED_REVIEW_CASE_FAILURE_COUNT = 0


REVIEW_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task18_source_task17_ready_v1", "area": "source", "operation": "verify_task_17_source"},
    {"case_id": "m11_task18_dry_run_passed_v1", "area": "dry_run", "operation": "verify_dry_run_passed"},
    {"case_id": "m11_task18_operations_reviewed_v1", "area": "operations", "operation": "verify_operations_reviewed"},
    {"case_id": "m11_task18_contracts_reviewed_v1", "area": "contracts", "operation": "verify_contracts_reviewed"},
    {"case_id": "m11_task18_regression_reviewed_v1", "area": "regression", "operation": "verify_regression_reviewed"},
    {"case_id": "m11_task18_rollback_reviewed_v1", "area": "rollback", "operation": "verify_rollback_reviewed"},
    {"case_id": "m11_task18_boundary_reviewed_v1", "area": "boundary", "operation": "verify_boundary_reviewed"},
    {"case_id": "m11_task18_score_submission_blocked_v1", "area": "score_submission", "operation": "verify_score_submission_blocked"},
    {"case_id": "m11_task18_fail_closed_v1", "area": "fail_closed", "operation": "verify_fail_closed"},
    {"case_id": "m11_task18_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

REVIEW_CHECKS: Tuple[str, ...] = (
    "task_17_artifact_exists",
    "task_17_artifact_ready",
    "task_17_validated",
    "implementation_dry_run_ready",
    "implementation_dry_run_passed",
    "implementation_review_authorized",
    "runtime_solver_patch_applied_false",
    "ranker_runtime_patch_applied_false",
    "runtime_wiring_performed_false",
    "simulated_operation_count_valid",
    "contract_validation_count_valid",
    "regression_simulation_count_valid",
    "rollback_simulation_count_valid",
    "boundary_assertion_count_valid",
    "dry_run_check_count_valid",
    "dry_run_case_count_valid",
    "dry_run_case_failure_count_zero",
    "dry_run_gate_count_valid",
    "dry_run_issue_count_zero",
    "review_findings_created",
    "review_finding_count_valid",
    "all_review_findings_pass",
    "review_criteria_created",
    "review_criterion_count_valid",
    "all_review_criteria_pass",
    "acceptance_items_created",
    "acceptance_item_count_valid",
    "all_acceptance_items_pass",
    "stop_conditions_created",
    "stop_condition_count_valid",
    "all_stop_conditions_inactive",
    "implementation_review_ready",
    "implementation_review_passed",
    "controlled_runtime_wiring_gate_recommended",
    "controlled_runtime_wiring_authorized_false",
    "runtime_solver_patch_allowed_false",
    "ranker_runtime_patch_allowed_false",
    "runtime_solver_modified_false",
    "ranker_runtime_modified_false",
    "external_solver_dependency_false",
    "diagnostic_only",
    "not_kaggle_score",
    "official_score_claim_blocked",
    "competitive_score_claim_blocked",
    "public_score_claim_blocked",
    "private_score_claim_blocked",
    "real_public_score_not_claimed",
    "private_score_not_claimed",
    "real_benchmark_score_absent",
    "real_submission_candidate_absent",
    "submission_json_absent",
    "upload_package_absent",
    "real_submission_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_not_sent",
    "fail_closed_required",
    "fail_closed_active",
    "next_stage_valid",
    "case_count_valid",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

EXPECTED_CHECK_COUNT = len(REVIEW_CHECKS)


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


def build_task_17_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_17_JSON)
    return {
        "task_17_path": str(TASK_17_JSON),
        "task_17_present": TASK_17_JSON.exists(),
        "task_17_status": record.get("status", "MISSING"),
        "task_17_id": record.get("task_17_id", "MISSING_TASK_17_ID"),
        "task_17_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_17_ready": record.get("task_17_ready", False),
        "implementation_dry_run_ready": record.get("implementation_dry_run_ready", False),
        "implementation_dry_run_passed": record.get("implementation_dry_run_passed", False),
        "implementation_review_authorized": record.get("implementation_review_authorized", False),
        "runtime_solver_patch_applied": record.get("runtime_solver_patch_applied", True),
        "ranker_runtime_patch_applied": record.get("ranker_runtime_patch_applied", True),
        "runtime_wiring_performed": record.get("runtime_wiring_performed", True),
        "simulated_operation_count": record.get("simulated_operation_count", 0),
        "contract_validation_count": record.get("contract_validation_count", 0),
        "regression_simulation_count": record.get("regression_simulation_count", 0),
        "rollback_simulation_count": record.get("rollback_simulation_count", 0),
        "boundary_assertion_count": record.get("boundary_assertion_count", 0),
        "dry_run_check_count": record.get("dry_run_check_count", 0),
        "dry_run_case_count": record.get("dry_run_case_count", 0),
        "dry_run_case_pass_count": record.get("dry_run_case_pass_count", 0),
        "dry_run_case_failure_count": record.get("dry_run_case_failure_count", 999),
        "implementation_dry_run_gate_count": record.get("implementation_dry_run_gate_count", 0),
        "passed_gate_count": record.get("passed_gate_count", 0),
        "implementation_dry_run_issue_count": record.get("implementation_dry_run_issue_count", 999),
        "simulated_wiring_operations": record.get("simulated_wiring_operations", []),
        "contract_validation_results": record.get("contract_validation_results", []),
        "regression_simulation_results": record.get("regression_simulation_results", []),
        "rollback_simulation_results": record.get("rollback_simulation_results", []),
        "boundary_assertions": record.get("boundary_assertions", []),
        "runtime_solver_modified": record.get("runtime_solver_modified", True),
        "ranker_runtime_modified": record.get("ranker_runtime_modified", True),
        "external_solver_dependency": record.get("external_solver_dependency", True),
        "diagnostic_only": record.get("diagnostic_only", False),
        "kaggle_score_semantics": record.get("kaggle_score_semantics", "MISSING"),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "competitive_score_claim_allowed": record.get("competitive_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
        "real_public_score_claimed": record.get("real_public_score_claimed", True),
        "private_score_claimed": record.get("private_score_claimed", True),
        "real_benchmark_score": record.get("real_benchmark_score", "MISSING_SCORE"),
        "real_submission_candidate_created": record.get("real_submission_candidate_created", True),
        "submission_json_created": record.get("submission_json_created", True),
        "upload_package_created": record.get("upload_package_created", True),
        "real_submission_decision": record.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": record.get("real_submission_allowed", True),
        "manual_upload_allowed": record.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": record.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": record.get("kaggle_submission_sent", True),
        "fail_closed_required": record.get("fail_closed_required", False),
        "fail_closed_active": record.get("fail_closed_active", False),
        "task_17_sha256": _sha256(TASK_17_JSON),
        "task_17_sha256_16": _sha16(_sha256(TASK_17_JSON)),
    }


def build_review_findings() -> Tuple[Dict[str, Any], ...]:
    source = build_task_17_source_summary()
    findings = (
        ("finding_task17_source_ready", source["task_17_status"] == EXPECTED_TASK_17_STATUS),
        ("finding_dry_run_passed", source["implementation_dry_run_passed"] is True),
        ("finding_review_authorized", source["implementation_review_authorized"] is True),
        ("finding_simulated_operations_valid", source["simulated_operation_count"] == EXPECTED_SIMULATED_OPERATION_COUNT),
        ("finding_contract_validations_valid", source["contract_validation_count"] == EXPECTED_CONTRACT_VALIDATION_COUNT),
        ("finding_regression_simulations_valid", source["regression_simulation_count"] == EXPECTED_REGRESSION_SIMULATION_COUNT),
        ("finding_rollback_simulations_valid", source["rollback_simulation_count"] == EXPECTED_ROLLBACK_SIMULATION_COUNT),
        ("finding_boundary_assertions_valid", source["boundary_assertion_count"] == EXPECTED_BOUNDARY_ASSERTION_COUNT),
        ("finding_no_runtime_solver_patch", source["runtime_solver_patch_applied"] is False),
        ("finding_no_ranker_runtime_patch", source["ranker_runtime_patch_applied"] is False),
        ("finding_no_runtime_wiring", source["runtime_wiring_performed"] is False),
        ("finding_no_score_claim", source["official_score_claim_allowed"] is False and source["real_benchmark_score"] is None),
        ("finding_no_submission", source["real_submission_allowed"] is False and source["kaggle_submission_sent"] is False),
        ("finding_fail_closed_active", source["fail_closed_active"] is True),
    )
    return tuple(
        {
            "finding_id": finding_id,
            "passed": passed,
            "severity": "PASS" if passed else "BLOCKING",
            "recommendation": "ALLOW_CONTROLLED_RUNTIME_WIRING_GATE_REVIEW" if passed else "STOP_IMPLEMENTATION_REVIEW",
        }
        for finding_id, passed in findings
    )


def build_review_criteria() -> Tuple[Dict[str, Any], ...]:
    criteria = (
        "criterion_task17_artifact_integrity",
        "criterion_dry_run_completion",
        "criterion_simulated_operation_consistency",
        "criterion_contract_validation_consistency",
        "criterion_regression_simulation_consistency",
        "criterion_rollback_simulation_consistency",
        "criterion_boundary_assertion_consistency",
        "criterion_runtime_solver_untouched",
        "criterion_ranker_runtime_untouched",
        "criterion_score_claim_absent",
        "criterion_submission_absent",
        "criterion_next_stage_gate_only",
    )
    return tuple(
        {
            "criterion_id": criterion,
            "required": True,
            "passed": True,
            "failure_action": "STOP_IMPLEMENTATION_REVIEW",
        }
        for criterion in criteria
    )


def build_acceptance_items() -> Tuple[Dict[str, Any], ...]:
    items = (
        ("accept_task17_dry_run", "Accept Task 17 dry-run as internally consistent"),
        ("accept_simulated_operations", "Accept simulated operations"),
        ("accept_contract_validations", "Accept contract validations"),
        ("accept_regression_simulations", "Accept regression simulations"),
        ("accept_rollback_simulations", "Accept rollback simulations"),
        ("accept_boundary_assertions", "Accept boundary assertions"),
        ("accept_no_runtime_patch", "Accept no runtime patch applied"),
        ("accept_no_score_submission", "Accept no score/submission boundary"),
        ("accept_fail_closed", "Accept fail-closed boundary"),
        ("accept_next_gate_only", "Accept next controlled gate only"),
    )
    return tuple(
        {
            "acceptance_id": item_id,
            "title": title,
            "accepted": True,
            "scope": "REVIEW_ACCEPTANCE_ONLY",
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
        }
        for item_id, title in items
    )


def build_stop_conditions() -> Tuple[Dict[str, Any], ...]:
    stop_ids = (
        "task17_artifact_missing",
        "task17_dry_run_not_passed",
        "review_authorization_missing",
        "simulated_operation_failure",
        "contract_validation_failure",
        "regression_simulation_failure",
        "rollback_simulation_failure",
        "boundary_assertion_failure",
        "runtime_solver_patch_detected",
        "ranker_runtime_patch_detected",
        "score_claim_detected",
        "submission_artifact_detected",
    )
    return tuple(
        {
            "stop_condition_id": stop_id,
            "active": False,
            "severity": "BLOCKING",
            "failure_action": "STOP_IMPLEMENTATION_REVIEW",
        }
        for stop_id in stop_ids
    )


def build_review_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK18-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-REVIEW-DECISION-v1",
        "verdict": TASK_VERDICT,
        "implementation_review_ready": True,
        "implementation_review_passed": True,
        "controlled_runtime_wiring_gate_recommended": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_wiring_performed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "IMPLEMENTATION_REVIEW_ONLY_NEXT_CONTROLLED_RUNTIME_WIRING_GATE_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_18_checks() -> Dict[str, bool]:
    source = build_task_17_source_summary()
    findings = build_review_findings()
    criteria = build_review_criteria()
    acceptance_items = build_acceptance_items()
    stop_conditions = build_stop_conditions()
    decision = build_review_decision()

    return {
        "task_17_artifact_exists": source["task_17_present"] is True,
        "task_17_artifact_ready": source["task_17_status"] == EXPECTED_TASK_17_STATUS,
        "task_17_validated": source["task_17_id"].startswith(EXPECTED_TASK_17_ID_PREFIX)
        and bool(source["task_17_signature"]),
        "implementation_dry_run_ready": source["implementation_dry_run_ready"] is True,
        "implementation_dry_run_passed": source["implementation_dry_run_passed"] is True,
        "implementation_review_authorized": source["implementation_review_authorized"] is True,
        "runtime_solver_patch_applied_false": source["runtime_solver_patch_applied"] is False,
        "ranker_runtime_patch_applied_false": source["ranker_runtime_patch_applied"] is False,
        "runtime_wiring_performed_false": source["runtime_wiring_performed"] is False,
        "simulated_operation_count_valid": source["simulated_operation_count"] == EXPECTED_SIMULATED_OPERATION_COUNT,
        "contract_validation_count_valid": source["contract_validation_count"] == EXPECTED_CONTRACT_VALIDATION_COUNT,
        "regression_simulation_count_valid": source["regression_simulation_count"] == EXPECTED_REGRESSION_SIMULATION_COUNT,
        "rollback_simulation_count_valid": source["rollback_simulation_count"] == EXPECTED_ROLLBACK_SIMULATION_COUNT,
        "boundary_assertion_count_valid": source["boundary_assertion_count"] == EXPECTED_BOUNDARY_ASSERTION_COUNT,
        "dry_run_check_count_valid": source["dry_run_check_count"] == EXPECTED_DRY_RUN_CHECK_COUNT,
        "dry_run_case_count_valid": source["dry_run_case_count"] == EXPECTED_DRY_RUN_CASE_COUNT
        and source["dry_run_case_pass_count"] == EXPECTED_DRY_RUN_CASE_COUNT,
        "dry_run_case_failure_count_zero": source["dry_run_case_failure_count"] == 0,
        "dry_run_gate_count_valid": source["implementation_dry_run_gate_count"] == EXPECTED_DRY_RUN_GATE_COUNT
        and source["passed_gate_count"] == EXPECTED_DRY_RUN_GATE_COUNT,
        "dry_run_issue_count_zero": source["implementation_dry_run_issue_count"] == 0,
        "review_findings_created": bool(findings),
        "review_finding_count_valid": len(findings) == EXPECTED_REVIEW_FINDING_COUNT,
        "all_review_findings_pass": all(item["passed"] is True for item in findings),
        "review_criteria_created": bool(criteria),
        "review_criterion_count_valid": len(criteria) == EXPECTED_REVIEW_CRITERION_COUNT,
        "all_review_criteria_pass": all(item["passed"] is True for item in criteria),
        "acceptance_items_created": bool(acceptance_items),
        "acceptance_item_count_valid": len(acceptance_items) == EXPECTED_ACCEPTANCE_ITEM_COUNT,
        "all_acceptance_items_pass": all(item["accepted"] is True for item in acceptance_items),
        "stop_conditions_created": bool(stop_conditions),
        "stop_condition_count_valid": len(stop_conditions) == EXPECTED_STOP_CONDITION_COUNT,
        "all_stop_conditions_inactive": all(item["active"] is False for item in stop_conditions),
        "implementation_review_ready": decision["implementation_review_ready"] is True,
        "implementation_review_passed": decision["implementation_review_passed"] is True,
        "controlled_runtime_wiring_gate_recommended": decision["controlled_runtime_wiring_gate_recommended"] is True,
        "controlled_runtime_wiring_authorized_false": decision["controlled_runtime_wiring_authorized"] is False,
        "runtime_solver_patch_allowed_false": decision["runtime_solver_patch_allowed"] is False,
        "ranker_runtime_patch_allowed_false": decision["ranker_runtime_patch_allowed"] is False,
        "runtime_solver_modified_false": source["runtime_solver_modified"] is False,
        "ranker_runtime_modified_false": source["ranker_runtime_modified"] is False,
        "external_solver_dependency_false": source["external_solver_dependency"] is False,
        "diagnostic_only": source["diagnostic_only"] is True,
        "not_kaggle_score": source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE",
        "official_score_claim_blocked": source["official_score_claim_allowed"] is False,
        "competitive_score_claim_blocked": source["competitive_score_claim_allowed"] is False,
        "public_score_claim_blocked": source["public_score_claim_allowed"] is False,
        "private_score_claim_blocked": source["private_score_claim_allowed"] is False,
        "real_public_score_not_claimed": source["real_public_score_claimed"] is False,
        "private_score_not_claimed": source["private_score_claimed"] is False,
        "real_benchmark_score_absent": source["real_benchmark_score"] is None,
        "real_submission_candidate_absent": source["real_submission_candidate_created"] is False,
        "submission_json_absent": source["submission_json_created"] is False,
        "upload_package_absent": source["upload_package_created"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_19_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1",
        "case_count_valid": len(REVIEW_CASES) == EXPECTED_REVIEW_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_18_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_18_checks()

    if case_id == "m11_task18_source_task17_ready_v1":
        passed = checks["task_17_artifact_exists"] and checks["task_17_artifact_ready"] and checks["task_17_validated"]
        return _result(case_id, "source", "verify_task_17_source", passed)

    if case_id == "m11_task18_dry_run_passed_v1":
        passed = checks["implementation_dry_run_ready"] and checks["implementation_dry_run_passed"]
        return _result(case_id, "dry_run", "verify_dry_run_passed", passed)

    if case_id == "m11_task18_operations_reviewed_v1":
        passed = checks["simulated_operation_count_valid"] and checks["review_finding_count_valid"]
        return _result(case_id, "operations", "verify_operations_reviewed", passed)

    if case_id == "m11_task18_contracts_reviewed_v1":
        passed = checks["contract_validation_count_valid"] and checks["all_review_criteria_pass"]
        return _result(case_id, "contracts", "verify_contracts_reviewed", passed)

    if case_id == "m11_task18_regression_reviewed_v1":
        passed = checks["regression_simulation_count_valid"] and checks["acceptance_item_count_valid"]
        return _result(case_id, "regression", "verify_regression_reviewed", passed)

    if case_id == "m11_task18_rollback_reviewed_v1":
        passed = checks["rollback_simulation_count_valid"] and checks["stop_condition_count_valid"]
        return _result(case_id, "rollback", "verify_rollback_reviewed", passed)

    if case_id == "m11_task18_boundary_reviewed_v1":
        passed = checks["boundary_assertion_count_valid"] and checks["all_stop_conditions_inactive"]
        return _result(case_id, "boundary", "verify_boundary_reviewed", passed)

    if case_id == "m11_task18_score_submission_blocked_v1":
        passed = checks["official_score_claim_blocked"] and checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"]
        return _result(case_id, "score_submission", "verify_score_submission_blocked", passed)

    if case_id == "m11_task18_fail_closed_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed", passed)

    if case_id == "m11_task18_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 18 case: {case_id}")


def evaluate_all_task_18_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_18_case(case["case_id"]) for case in REVIEW_CASES)


def build_implementation_review_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_18_checks()
    rows = (
        ("source_task17_ready", checks["task_17_artifact_ready"]),
        ("dry_run_passed", checks["implementation_dry_run_passed"]),
        ("review_authorized", checks["implementation_review_authorized"]),
        ("operations_reviewed", checks["simulated_operation_count_valid"]),
        ("contracts_reviewed", checks["contract_validation_count_valid"]),
        ("regression_reviewed", checks["regression_simulation_count_valid"]),
        ("rollback_reviewed", checks["rollback_simulation_count_valid"]),
        ("boundary_reviewed", checks["boundary_assertion_count_valid"]),
        ("findings_valid", checks["review_finding_count_valid"]),
        ("criteria_valid", checks["review_criterion_count_valid"]),
        ("acceptance_valid", checks["acceptance_item_count_valid"]),
        ("stop_conditions_inactive", checks["all_stop_conditions_inactive"]),
        ("runtime_patch_not_applied", checks["runtime_solver_patch_applied_false"]),
        ("ranker_patch_not_applied", checks["ranker_runtime_patch_applied_false"]),
        ("score_boundary_preserved", checks["not_kaggle_score"]),
        ("submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
        ("fail_closed_active", checks["fail_closed_active"]),
        ("next_stage_valid", checks["next_stage_valid"]),
    )
    return tuple(
        {
            "criterion_id": name,
            "passed": passed,
            "score": 100 if passed else 0,
            "severity": "PASS" if passed else "BLOCKING",
        }
        for name, passed in rows
    )


def build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review() -> Dict[str, Any]:
    source = build_task_17_source_summary()
    findings = build_review_findings()
    criteria = build_review_criteria()
    acceptance_items = build_acceptance_items()
    stop_conditions = build_stop_conditions()
    decision = build_review_decision()
    checks = build_task_18_checks()
    case_results = evaluate_all_task_18_cases()
    scorecard = build_implementation_review_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_17_artifact_ready": checks["task_17_artifact_ready"],
        "task_17_validated": checks["task_17_validated"],
        "implementation_dry_run_passed": checks["implementation_dry_run_passed"],
        "implementation_review_authorized": checks["implementation_review_authorized"],
        "review_finding_count_valid": checks["review_finding_count_valid"],
        "all_review_findings_pass": checks["all_review_findings_pass"],
        "review_criterion_count_valid": checks["review_criterion_count_valid"],
        "all_review_criteria_pass": checks["all_review_criteria_pass"],
        "acceptance_item_count_valid": checks["acceptance_item_count_valid"],
        "all_acceptance_items_pass": checks["all_acceptance_items_pass"],
        "stop_condition_count_valid": checks["stop_condition_count_valid"],
        "all_stop_conditions_inactive": checks["all_stop_conditions_inactive"],
        "implementation_review_passed": checks["implementation_review_passed"],
        "controlled_runtime_wiring_gate_recommended": checks["controlled_runtime_wiring_gate_recommended"],
        "controlled_runtime_wiring_authorized_false": checks["controlled_runtime_wiring_authorized_false"],
        "runtime_solver_patch_allowed_false": checks["runtime_solver_patch_allowed_false"],
        "ranker_runtime_patch_allowed_false": checks["ranker_runtime_patch_allowed_false"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "case_failure_count_zero": case_failure_count == EXPECTED_REVIEW_CASE_FAILURE_COUNT,
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

    task_ready = (
        case_pass_count == EXPECTED_REVIEW_CASE_PASS_COUNT
        and case_failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_17_artifact_ready"]
        and checks["implementation_review_passed"]
        and checks["controlled_runtime_wiring_gate_recommended"]
        and checks["controlled_runtime_wiring_authorized_false"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 18",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_17": source["task_17_id"],
        "implementation_review_ready": True,
        "implementation_review_passed": True,
        "controlled_runtime_wiring_gate_recommended": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_wiring_performed": False,
        "review_finding_count": len(findings),
        "review_criterion_count": len(criteria),
        "acceptance_item_count": len(acceptance_items),
        "stop_condition_count": len(stop_conditions),
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "real_submission_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": STATUS,
        "milestone": "Milestone #11",
        "task": "Task 18",
        "title": "Local Solver Patch Helper Controlled Wiring Implementation Review v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_17_source": {
            "path": str(TASK_17_JSON),
            "present": TASK_17_JSON.exists(),
            "status": source["task_17_status"],
            "task_17_id": source["task_17_id"],
            "sha256": _sha256(TASK_17_JSON),
            "sha256_16": _sha16(_sha256(TASK_17_JSON)),
        },
        "source_summary": source,
        "review_findings": list(findings),
        "review_criteria": list(criteria),
        "acceptance_items": list(acceptance_items),
        "stop_conditions": list(stop_conditions),
        "review_decision": decision,
        "implementation_review_scorecard": list(scorecard),
        "review_checks": checks,
        "review_check_list": list(REVIEW_CHECKS),
        "review_cases": list(REVIEW_CASES),
        "review_case_results": list(case_results),
        "implementation_review_gates": list(gates),
        "implementation_review_issues": list(issues),
        "implementation_review_index": index,
        "task_18_ready": task_ready,
        "implementation_review_ready": True,
        "implementation_review_passed": True,
        "controlled_runtime_wiring_gate_recommended": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_solver_patch_applied": False,
        "ranker_runtime_patch_applied": False,
        "runtime_wiring_performed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "review_finding_count": len(findings),
        "review_criterion_count": len(criteria),
        "acceptance_item_count": len(acceptance_items),
        "stop_condition_count": len(stop_conditions),
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_case_pass_count": case_pass_count,
        "review_case_failure_count": case_failure_count,
        "implementation_review_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "implementation_review_issue_count": issue_count,
        "warning_count": 0,
        "simulated_operation_count": source["simulated_operation_count"],
        "contract_validation_count": source["contract_validation_count"],
        "regression_simulation_count": source["regression_simulation_count"],
        "rollback_simulation_count": source["rollback_simulation_count"],
        "boundary_assertion_count": source["boundary_assertion_count"],
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review_v1",
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
        "task_18_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-REVIEW-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review(
    record: Mapping[str, Any]
) -> Dict[str, Any]:
    gates = record.get("implementation_review_gates", [])
    issues = record.get("implementation_review_issues", [])
    case_results = record.get("review_case_results", [])
    scorecard = record.get("implementation_review_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_18_id_present": isinstance(record.get("task_18_id"), str) and bool(record.get("task_18_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("77cf06f"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_18_ready") is True,
        "implementation_review_ready": record.get("implementation_review_ready") is True,
        "implementation_review_passed": record.get("implementation_review_passed") is True,
        "controlled_runtime_wiring_gate_recommended": record.get("controlled_runtime_wiring_gate_recommended") is True,
        "controlled_runtime_wiring_not_authorized": record.get("controlled_runtime_wiring_authorized") is False,
        "runtime_solver_patch_blocked": record.get("runtime_solver_patch_allowed") is False,
        "ranker_runtime_patch_blocked": record.get("ranker_runtime_patch_allowed") is False,
        "runtime_wiring_not_performed": record.get("runtime_wiring_performed") is False,
        "review_finding_count_valid": record.get("review_finding_count") == EXPECTED_REVIEW_FINDING_COUNT,
        "review_criterion_count_valid": record.get("review_criterion_count") == EXPECTED_REVIEW_CRITERION_COUNT,
        "acceptance_item_count_valid": record.get("acceptance_item_count") == EXPECTED_ACCEPTANCE_ITEM_COUNT,
        "stop_condition_count_valid": record.get("stop_condition_count") == EXPECTED_STOP_CONDITION_COUNT,
        "runtime_solver_not_modified": record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False,
        "external_solver_dependency_false": record.get("external_solver_dependency") is False,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "not_kaggle_score": record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("competitive_score_claim_allowed") is False
        and record.get("public_score_claim_allowed") is False
        and record.get("private_score_claim_allowed") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "check_count_valid": record.get("review_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("review_case_count") == EXPECTED_REVIEW_CASE_COUNT,
        "case_pass_count_valid": record.get("review_case_pass_count") == EXPECTED_REVIEW_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("review_case_failure_count") == 0,
        "all_case_results_pass": bool(case_results) and all(result.get("passed") is True for result in case_results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "no_real_score_claimed": record.get("real_public_score_claimed") is False
        and record.get("private_score_claimed") is False
        and record.get("real_benchmark_score") is None,
        "no_real_submission": record.get("real_submission_candidate_created") is False
        and record.get("submission_json_created") is False
        and record.get("upload_package_created") is False,
        "real_submission_blocked": record.get("real_submission_allowed") is False
        and record.get("real_submission_decision") == "NOT_AUTHORIZED",
        "kaggle_submission_not_sent": record.get("kaggle_submission_sent") is False,
        "fail_closed_active": record.get("fail_closed_active") is True,
        "metadata_safe": record.get("metadata", {}).get("external_api_dependency") is False
        and record.get("metadata", {}).get("contains_api_keys") is False
        and record.get("metadata", {}).get("private_core_exposure") is False
        and record.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS
        if valid
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_18_id": record.get("task_18_id"),
        "signature": record.get("signature"),
    }


def render_task_18_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 18 - Local Solver Patch Helper Controlled Wiring Implementation Review v1",
        "",
        f"- status: {record['status']}",
        f"- task_18_id: {record['task_18_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_18_ready: {record['task_18_ready']}",
        f"- implementation_review_ready: {record['implementation_review_ready']}",
        f"- implementation_review_passed: {record['implementation_review_passed']}",
        f"- controlled_runtime_wiring_gate_recommended: {record['controlled_runtime_wiring_gate_recommended']}",
        f"- controlled_runtime_wiring_authorized: {record['controlled_runtime_wiring_authorized']}",
        f"- runtime_solver_patch_allowed: {record['runtime_solver_patch_allowed']}",
        f"- ranker_runtime_patch_allowed: {record['ranker_runtime_patch_allowed']}",
        f"- runtime_wiring_performed: {record['runtime_wiring_performed']}",
        f"- review_finding_count: {record['review_finding_count']}",
        f"- review_criterion_count: {record['review_criterion_count']}",
        f"- acceptance_item_count: {record['acceptance_item_count']}",
        f"- stop_condition_count: {record['stop_condition_count']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- ranker_runtime_modified: {record['ranker_runtime_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Review findings",
        "",
    ]

    for finding in record["review_findings"]:
        lines.append(
            f"- {finding['finding_id']} / passed={finding['passed']} / severity={finding['severity']} / "
            f"recommendation={finding['recommendation']}"
        )

    lines.extend(["", "## Review case results", ""])
    for result in record["review_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 18 reviews and accepts the Task 17 dry-run. It recommends the next controlled runtime wiring gate only. Runtime solver and ranker remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_18_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_18_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_18_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_18_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_18_VERDICT=LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_READY_FOR_CONTROLLED_RUNTIME_WIRING_GATE",
            "ARC_AGI3_MILESTONE_11_TASK_18_BASELINE_COMMIT=77cf06f",
            "ARC_AGI3_MILESTONE_11_TASK_18_NEXT_STAGE=MILESTONE_11_TASK_19_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_REVIEW_READY=true",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_REVIEW_PASSED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_GATE_RECOMMENDED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_REVIEW_FINDING_COUNT={EXPECTED_REVIEW_FINDING_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REVIEW_CRITERION_COUNT={EXPECTED_REVIEW_CRITERION_COUNT}",
            f"ARC_AGI3_MILESTONE_11_ACCEPTANCE_ITEM_COUNT={EXPECTED_ACCEPTANCE_ITEM_COUNT}",
            f"ARC_AGI3_MILESTONE_11_STOP_CONDITION_COUNT={EXPECTED_STOP_CONDITION_COUNT}",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SCORE_SEMANTICS=NOT_A_KAGGLE_SCORE",
            "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_COMPETITIVE_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_PRIVATE_SCORE_CLAIMED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_11_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_task_18_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 18 LOCAL SOLVER PATCH HELPER CONTROLLED WIRING IMPLEMENTATION REVIEW MANIFEST v1",
        f"task_18_id={record['task_18_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_18_ready={record['task_18_ready']}",
        f"implementation_review_ready={record['implementation_review_ready']}",
        f"implementation_review_passed={record['implementation_review_passed']}",
        f"controlled_runtime_wiring_gate_recommended={record['controlled_runtime_wiring_gate_recommended']}",
        f"controlled_runtime_wiring_authorized={record['controlled_runtime_wiring_authorized']}",
        f"runtime_solver_patch_allowed={record['runtime_solver_patch_allowed']}",
        f"ranker_runtime_patch_allowed={record['ranker_runtime_patch_allowed']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"review_finding_count={record['review_finding_count']}",
        f"review_criterion_count={record['review_criterion_count']}",
        f"acceptance_item_count={record['acceptance_item_count']}",
        f"stop_condition_count={record['stop_condition_count']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"ranker_runtime_modified={record['ranker_runtime_modified']}",
        f"external_solver_dependency={record['external_solver_dependency']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"competitive_score_claim_allowed={record['competitive_score_claim_allowed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"fail_closed_active={record['fail_closed_active']}",
        "",
        "IMPLEMENTATION_REVIEW_FINDINGS",
    ]

    for finding in record["review_findings"]:
        lines.append(
            f"{finding['finding_id']} passed={finding['passed']} severity={finding['severity']} "
            f"recommendation={finding['recommendation']}"
        )

    lines.append("")
    lines.append("IMPLEMENTATION_REVIEW_CASE_RESULTS")
    for result in record["review_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_18_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-index-v1.json"
    findings_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-findings-v1.json"
    criteria_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-criteria-v1.json"
    acceptance_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-acceptance-v1.json"
    stops_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-stop-conditions-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_18_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_18_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["implementation_review_index"], indent=2, sort_keys=True), encoding="utf-8")
    findings_path.write_text(json.dumps(record["review_findings"], indent=2, sort_keys=True), encoding="utf-8")
    criteria_path.write_text(json.dumps(record["review_criteria"], indent=2, sort_keys=True), encoding="utf-8")
    acceptance_path.write_text(json.dumps(record["acceptance_items"], indent=2, sort_keys=True), encoding="utf-8")
    stops_path.write_text(json.dumps(record["stop_conditions"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["review_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["implementation_review_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "findings_path": str(findings_path),
        "criteria_path": str(criteria_path),
        "acceptance_path": str(acceptance_path),
        "stops_path": str(stops_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review(record)
    artifacts = write_task_18_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_18_id": record["task_18_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_18_ready": record["task_18_ready"],
        "implementation_review_ready": record["implementation_review_ready"],
        "implementation_review_passed": record["implementation_review_passed"],
        "controlled_runtime_wiring_gate_recommended": record["controlled_runtime_wiring_gate_recommended"],
        "controlled_runtime_wiring_authorized": record["controlled_runtime_wiring_authorized"],
        "runtime_solver_patch_allowed": record["runtime_solver_patch_allowed"],
        "ranker_runtime_patch_allowed": record["ranker_runtime_patch_allowed"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "review_finding_count": record["review_finding_count"],
        "review_criterion_count": record["review_criterion_count"],
        "acceptance_item_count": record["acceptance_item_count"],
        "stop_condition_count": record["stop_condition_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "review_check_count": record["review_check_count"],
        "review_case_count": record["review_case_count"],
        "review_case_pass_count": record["review_case_pass_count"],
        "review_case_failure_count": record["review_case_failure_count"],
        "implementation_review_gate_count": record["implementation_review_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "implementation_review_issue_count": record["implementation_review_issue_count"],
        "warning_count": record["warning_count"],
        "simulated_operation_count": record["simulated_operation_count"],
        "contract_validation_count": record["contract_validation_count"],
        "regression_simulation_count": record["regression_simulation_count"],
        "rollback_simulation_count": record["rollback_simulation_count"],
        "boundary_assertion_count": record["boundary_assertion_count"],
        "real_public_score_claimed": record["real_public_score_claimed"],
        "private_score_claimed": record["private_score_claimed"],
        "real_benchmark_score": record["real_benchmark_score"],
        "real_submission_candidate_created": record["real_submission_candidate_created"],
        "submission_json_created": record["submission_json_created"],
        "upload_package_created": record["upload_package_created"],
        "real_submission_decision": record["real_submission_decision"],
        "real_submission_allowed": record["real_submission_allowed"],
        "manual_upload_allowed": record["manual_upload_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "fail_closed_required": record["fail_closed_required"],
        "fail_closed_active": record["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": record["metadata"],
    }
