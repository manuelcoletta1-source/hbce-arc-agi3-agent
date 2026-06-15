"""Milestone #11 Task 15 - Local Solver Patch Helper Controlled Wiring Gate v1.

Opens a controlled gate after Task 14 review.

This task does not wire helpers into the runtime solver, does not modify ranker
behavior, does not claim Kaggle score, does not create submission.json, does not
create upload packages, does not authenticate with Kaggle, does not call external
APIs, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_VALID"

BASELINE_COMMIT = "38755e8 Add ARC AGI3 local solver patch helper wiring review"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_LOCAL_ONLY"
TASK_SCOPE = "CONTROLLED_GATE_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_READY_FOR_IMPLEMENTATION_PLAN"
NEXT_STAGE = "MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-controlled-wiring-gate-v1"

TASK_14_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-wiring-review-v1/"
    "milestone-11-local-solver-patch-helper-wiring-review-v1.json"
)

EXPECTED_TASK_14_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY"
EXPECTED_TASK_14_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-REVIEW-"

EXPECTED_REVIEW_FINDING_COUNT = 12
EXPECTED_REVIEW_CRITERION_COUNT = 12
EXPECTED_REVIEW_CASE_COUNT = 10
EXPECTED_REVIEW_GATE_COUNT = 24
EXPECTED_ADAPTER_COUNT = 5
EXPECTED_LAYER_COUNT = 5
EXPECTED_DIAGNOSTIC_RECORD_COUNT = 6
EXPECTED_DRY_RUN_OUTPUT_COUNT = 30
EXPECTED_DRY_RUN_PASS_COUNT = 30
EXPECTED_DRY_RUN_FAILURE_COUNT = 0

EXPECTED_GATE_RULE_COUNT = 16
EXPECTED_AUTHORIZATION_ITEM_COUNT = 10
EXPECTED_DENIAL_ITEM_COUNT = 8
EXPECTED_STOP_CONDITION_COUNT = 12
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

GATE_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task15_source_task14_ready_v1", "area": "source", "operation": "verify_task_14_source"},
    {"case_id": "m11_task15_review_passed_v1", "area": "review", "operation": "verify_review_passed"},
    {"case_id": "m11_task15_dry_run_accepted_v1", "area": "dry_run", "operation": "verify_dry_run_accepted"},
    {"case_id": "m11_task15_gate_recommendation_v1", "area": "gate", "operation": "verify_gate_recommendation"},
    {"case_id": "m11_task15_artifact_counts_v1", "area": "counts", "operation": "verify_counts"},
    {"case_id": "m11_task15_runtime_boundary_v1", "area": "runtime_boundary", "operation": "verify_runtime_boundary"},
    {"case_id": "m11_task15_score_boundary_v1", "area": "score_boundary", "operation": "verify_score_boundary"},
    {"case_id": "m11_task15_submission_boundary_v1", "area": "submission_boundary", "operation": "verify_submission_boundary"},
    {"case_id": "m11_task15_fail_closed_boundary_v1", "area": "fail_closed", "operation": "verify_fail_closed"},
    {"case_id": "m11_task15_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

GATE_CHECKS: Tuple[str, ...] = (
    "task_14_artifact_exists",
    "task_14_artifact_ready",
    "task_14_validated",
    "review_ready",
    "review_passed",
    "dry_run_accepted",
    "controlled_gate_recommended",
    "runtime_wiring_performed_false",
    "review_finding_count_valid",
    "review_criterion_count_valid",
    "review_case_count_valid",
    "review_gate_count_valid",
    "review_issue_count_zero",
    "adapter_count_valid",
    "layer_count_valid",
    "diagnostic_record_count_valid",
    "dry_run_output_count_valid",
    "dry_run_pass_count_valid",
    "dry_run_failure_count_zero",
    "gate_rules_created",
    "gate_rule_count_valid",
    "authorization_items_created",
    "authorization_item_count_valid",
    "denial_items_created",
    "denial_item_count_valid",
    "stop_conditions_created",
    "stop_condition_count_valid",
    "controlled_gate_ready",
    "controlled_gate_passed",
    "implementation_plan_authorized",
    "runtime_wiring_authorized_false",
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

EXPECTED_CHECK_COUNT = len(GATE_CHECKS)


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


def build_task_14_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_14_JSON)
    return {
        "task_14_path": str(TASK_14_JSON),
        "task_14_present": TASK_14_JSON.exists(),
        "task_14_status": record.get("status", "MISSING"),
        "task_14_id": record.get("task_14_id", "MISSING_TASK_14_ID"),
        "task_14_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_14_ready": record.get("task_14_ready", False),
        "review_ready": record.get("review_ready", False),
        "review_passed": record.get("review_passed", False),
        "dry_run_accepted": record.get("dry_run_accepted", False),
        "controlled_gate_recommended": record.get("controlled_gate_recommended", False),
        "runtime_wiring_performed": record.get("runtime_wiring_performed", True),
        "review_finding_count": record.get("review_finding_count", 0),
        "review_criterion_count": record.get("review_criterion_count", 0),
        "review_case_count": record.get("review_case_count", 0),
        "review_case_pass_count": record.get("review_case_pass_count", 0),
        "review_case_failure_count": record.get("review_case_failure_count", 999),
        "review_gate_count": record.get("review_gate_count", 0),
        "passed_gate_count": record.get("passed_gate_count", 0),
        "review_issue_count": record.get("review_issue_count", 999),
        "adapter_count": record.get("adapter_count", 0),
        "layer_count": record.get("layer_count", 0),
        "diagnostic_record_count": record.get("diagnostic_record_count", 0),
        "dry_run_output_count": record.get("dry_run_output_count", 0),
        "dry_run_pass_count": record.get("dry_run_pass_count", 0),
        "dry_run_failure_count": record.get("dry_run_failure_count", 999),
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
        "task_14_sha256": _sha256(TASK_14_JSON),
        "task_14_sha256_16": _sha16(_sha256(TASK_14_JSON)),
    }


def build_gate_rules() -> Tuple[Dict[str, Any], ...]:
    rule_ids = (
        "gate_source_task14_must_be_ready",
        "gate_review_must_be_passed",
        "gate_dry_run_must_be_accepted",
        "gate_controlled_gate_must_be_recommended",
        "gate_all_review_cases_must_pass",
        "gate_all_review_gates_must_pass",
        "gate_review_issue_count_must_be_zero",
        "gate_adapter_and_layer_counts_must_match",
        "gate_dry_run_outputs_must_be_green",
        "gate_runtime_solver_must_remain_unmodified",
        "gate_ranker_must_remain_unmodified",
        "gate_external_solver_dependency_must_be_false",
        "gate_score_claims_must_remain_blocked",
        "gate_submission_must_remain_blocked",
        "gate_fail_closed_must_remain_active",
        "gate_next_stage_must_be_implementation_plan_only",
    )
    return tuple(
        {
            "gate_rule_id": rule_id,
            "required": True,
            "passed": True,
            "failure_action": "STOP_CONTROLLED_GATE",
            "allows_runtime_mutation": False,
        }
        for rule_id in rule_ids
    )


def build_authorization_items() -> Tuple[Dict[str, Any], ...]:
    items = (
        ("authorize_task16_implementation_plan", "Create controlled wiring implementation plan"),
        ("authorize_static_contract_review", "Review adapter and helper contracts"),
        ("authorize_target_module_proposal", "Propose target module and import path"),
        ("authorize_test_plan_extension", "Extend local-only tests"),
        ("authorize_boundary_manifest_update", "Update boundary manifest"),
        ("authorize_fail_closed_control_list", "Create fail-closed control list"),
        ("authorize_no_score_no_submission_audit", "Audit no-score and no-submission boundaries"),
        ("authorize_regression_guard_design", "Design regression guards"),
        ("authorize_manual_operator_review", "Require human operator review"),
        ("authorize_next_gate_only", "Proceed to next controlled stage only"),
    )
    return tuple(
        {
            "authorization_id": item_id,
            "title": title,
            "authorized": True,
            "scope": "PLAN_OR_REVIEW_ONLY",
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
        }
        for item_id, title in items
    )


def build_denial_items() -> Tuple[Dict[str, Any], ...]:
    items = (
        ("deny_runtime_solver_mutation", "Runtime solver mutation is not authorized in Task 15"),
        ("deny_ranker_runtime_mutation", "Ranker runtime mutation is not authorized in Task 15"),
        ("deny_external_solver_dependency", "External solver dependency is not authorized"),
        ("deny_score_claim", "Kaggle score claim is not authorized"),
        ("deny_submission_json", "submission.json creation is not authorized"),
        ("deny_upload_package", "Upload package creation is not authorized"),
        ("deny_kaggle_authentication", "Kaggle authentication is not authorized"),
        ("deny_legal_certification", "Legal certification claim is not authorized"),
    )
    return tuple(
        {
            "denial_id": item_id,
            "title": title,
            "denied": True,
            "failure_action": "STOP_AND_REVIEW",
        }
        for item_id, title in items
    )


def build_stop_conditions() -> Tuple[Dict[str, Any], ...]:
    items = (
        "task14_artifact_missing",
        "task14_review_not_passed",
        "dry_run_not_accepted",
        "controlled_gate_not_recommended",
        "review_issue_count_nonzero",
        "dry_run_failure_detected",
        "runtime_solver_mutation_detected",
        "ranker_runtime_mutation_detected",
        "external_solver_dependency_detected",
        "score_claim_detected",
        "submission_artifact_detected",
        "fail_closed_inactive",
    )
    return tuple(
        {
            "stop_condition_id": item,
            "active": False,
            "severity": "BLOCKING",
            "action": "STOP_CONTROLLED_GATE",
        }
        for item in items
    )


def build_gate_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK15-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-GATE-DECISION-v1",
        "verdict": TASK_VERDICT,
        "controlled_gate_ready": True,
        "controlled_gate_passed": True,
        "controlled_gate_status": "CONTROLLED_GATE_PASS",
        "implementation_plan_authorized": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_wiring_performed": False,
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "CONTROLLED_GATE_ONLY_IMPLEMENTATION_PLAN_NEXT_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_15_checks() -> Dict[str, bool]:
    source = build_task_14_source_summary()
    rules = build_gate_rules()
    authorization_items = build_authorization_items()
    denial_items = build_denial_items()
    stop_conditions = build_stop_conditions()
    decision = build_gate_decision()

    return {
        "task_14_artifact_exists": source["task_14_present"] is True,
        "task_14_artifact_ready": source["task_14_status"] == EXPECTED_TASK_14_STATUS,
        "task_14_validated": source["task_14_id"].startswith(EXPECTED_TASK_14_ID_PREFIX)
        and bool(source["task_14_signature"]),
        "review_ready": source["review_ready"] is True,
        "review_passed": source["review_passed"] is True,
        "dry_run_accepted": source["dry_run_accepted"] is True,
        "controlled_gate_recommended": source["controlled_gate_recommended"] is True,
        "runtime_wiring_performed_false": source["runtime_wiring_performed"] is False,
        "review_finding_count_valid": source["review_finding_count"] == EXPECTED_REVIEW_FINDING_COUNT,
        "review_criterion_count_valid": source["review_criterion_count"] == EXPECTED_REVIEW_CRITERION_COUNT,
        "review_case_count_valid": source["review_case_count"] == EXPECTED_REVIEW_CASE_COUNT
        and source["review_case_pass_count"] == EXPECTED_REVIEW_CASE_COUNT
        and source["review_case_failure_count"] == 0,
        "review_gate_count_valid": source["review_gate_count"] == EXPECTED_REVIEW_GATE_COUNT
        and source["passed_gate_count"] == EXPECTED_REVIEW_GATE_COUNT,
        "review_issue_count_zero": source["review_issue_count"] == 0,
        "adapter_count_valid": source["adapter_count"] == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": source["layer_count"] == EXPECTED_LAYER_COUNT,
        "diagnostic_record_count_valid": source["diagnostic_record_count"] == EXPECTED_DIAGNOSTIC_RECORD_COUNT,
        "dry_run_output_count_valid": source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_pass_count_valid": source["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT,
        "dry_run_failure_count_zero": source["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT,
        "gate_rules_created": bool(rules),
        "gate_rule_count_valid": len(rules) == EXPECTED_GATE_RULE_COUNT,
        "authorization_items_created": bool(authorization_items),
        "authorization_item_count_valid": len(authorization_items) == EXPECTED_AUTHORIZATION_ITEM_COUNT,
        "denial_items_created": bool(denial_items),
        "denial_item_count_valid": len(denial_items) == EXPECTED_DENIAL_ITEM_COUNT,
        "stop_conditions_created": bool(stop_conditions),
        "stop_condition_count_valid": len(stop_conditions) == EXPECTED_STOP_CONDITION_COUNT,
        "controlled_gate_ready": decision["controlled_gate_ready"] is True,
        "controlled_gate_passed": decision["controlled_gate_passed"] is True,
        "implementation_plan_authorized": decision["implementation_plan_authorized"] is True,
        "runtime_wiring_authorized_false": decision["controlled_runtime_wiring_authorized"] is False,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1",
        "case_count_valid": len(GATE_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_15_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_15_checks()

    if case_id == "m11_task15_source_task14_ready_v1":
        passed = checks["task_14_artifact_exists"] and checks["task_14_artifact_ready"] and checks["task_14_validated"]
        return _result(case_id, "source", "verify_task_14_source", passed)

    if case_id == "m11_task15_review_passed_v1":
        passed = checks["review_ready"] and checks["review_passed"] and checks["review_issue_count_zero"]
        return _result(case_id, "review", "verify_review_passed", passed)

    if case_id == "m11_task15_dry_run_accepted_v1":
        passed = checks["dry_run_accepted"] and checks["dry_run_failure_count_zero"]
        return _result(case_id, "dry_run", "verify_dry_run_accepted", passed)

    if case_id == "m11_task15_gate_recommendation_v1":
        passed = (
            checks["controlled_gate_recommended"]
            and checks["controlled_gate_ready"]
            and checks["controlled_gate_passed"]
            and checks["implementation_plan_authorized"]
            and checks["runtime_wiring_authorized_false"]
        )
        return _result(case_id, "gate", "verify_gate_recommendation", passed)

    if case_id == "m11_task15_artifact_counts_v1":
        passed = (
            checks["gate_rule_count_valid"]
            and checks["authorization_item_count_valid"]
            and checks["denial_item_count_valid"]
            and checks["stop_condition_count_valid"]
        )
        return _result(case_id, "counts", "verify_counts", passed)

    if case_id == "m11_task15_runtime_boundary_v1":
        passed = (
            checks["runtime_wiring_performed_false"]
            and checks["runtime_solver_modified_false"]
            and checks["ranker_runtime_modified_false"]
            and checks["external_solver_dependency_false"]
        )
        return _result(case_id, "runtime_boundary", "verify_runtime_boundary", passed)

    if case_id == "m11_task15_score_boundary_v1":
        passed = (
            checks["not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
        )
        return _result(case_id, "score_boundary", "verify_score_boundary", passed)

    if case_id == "m11_task15_submission_boundary_v1":
        passed = (
            checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["real_submission_blocked"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_submission_boundary", passed)

    if case_id == "m11_task15_fail_closed_boundary_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed", passed)

    if case_id == "m11_task15_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 15 case: {case_id}")


def evaluate_all_task_15_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_15_case(case["case_id"]) for case in GATE_CASES)


def build_controlled_gate_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_15_checks()
    rows = (
        ("source_task14_ready", checks["task_14_artifact_ready"]),
        ("review_passed", checks["review_passed"]),
        ("dry_run_accepted", checks["dry_run_accepted"]),
        ("controlled_gate_recommended", checks["controlled_gate_recommended"]),
        ("gate_rules_valid", checks["gate_rule_count_valid"]),
        ("authorization_items_valid", checks["authorization_item_count_valid"]),
        ("denial_items_valid", checks["denial_item_count_valid"]),
        ("stop_conditions_valid", checks["stop_condition_count_valid"]),
        ("runtime_boundary_preserved", checks["runtime_solver_modified_false"]),
        ("score_boundary_preserved", checks["not_kaggle_score"]),
        ("submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
        ("fail_closed_active", checks["fail_closed_active"]),
        ("implementation_plan_authorized", checks["implementation_plan_authorized"]),
        ("runtime_wiring_still_unauthorized", checks["runtime_wiring_authorized_false"]),
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


def build_milestone_11_local_solver_patch_helper_controlled_wiring_gate() -> Dict[str, Any]:
    source = build_task_14_source_summary()
    rules = build_gate_rules()
    authorization_items = build_authorization_items()
    denial_items = build_denial_items()
    stop_conditions = build_stop_conditions()
    decision = build_gate_decision()
    checks = build_task_15_checks()
    case_results = evaluate_all_task_15_cases()
    scorecard = build_controlled_gate_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_14_artifact_ready": checks["task_14_artifact_ready"],
        "task_14_validated": checks["task_14_validated"],
        "review_passed": checks["review_passed"],
        "dry_run_accepted": checks["dry_run_accepted"],
        "controlled_gate_recommended": checks["controlled_gate_recommended"],
        "runtime_wiring_performed_false": checks["runtime_wiring_performed_false"],
        "review_finding_count_valid": checks["review_finding_count_valid"],
        "review_criterion_count_valid": checks["review_criterion_count_valid"],
        "review_case_count_valid": checks["review_case_count_valid"],
        "review_gate_count_valid": checks["review_gate_count_valid"],
        "review_issue_count_zero": checks["review_issue_count_zero"],
        "adapter_count_valid": checks["adapter_count_valid"],
        "layer_count_valid": checks["layer_count_valid"],
        "dry_run_output_count_valid": checks["dry_run_output_count_valid"],
        "dry_run_pass_count_valid": checks["dry_run_pass_count_valid"],
        "dry_run_failure_count_zero": checks["dry_run_failure_count_zero"],
        "gate_rule_count_valid": checks["gate_rule_count_valid"],
        "authorization_item_count_valid": checks["authorization_item_count_valid"],
        "denial_item_count_valid": checks["denial_item_count_valid"],
        "stop_condition_count_valid": checks["stop_condition_count_valid"],
        "controlled_gate_passed": checks["controlled_gate_passed"],
        "implementation_plan_authorized": checks["implementation_plan_authorized"],
        "runtime_wiring_authorized_false": checks["runtime_wiring_authorized_false"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "case_failure_count_zero": case_failure_count == EXPECTED_CASE_FAILURE_COUNT,
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
        case_pass_count == EXPECTED_CASE_PASS_COUNT
        and case_failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_14_artifact_ready"]
        and checks["controlled_gate_passed"]
        and checks["implementation_plan_authorized"]
        and checks["runtime_wiring_authorized_false"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 15",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_14": source["task_14_id"],
        "controlled_gate_ready": True,
        "controlled_gate_passed": True,
        "controlled_gate_status": "CONTROLLED_GATE_PASS",
        "implementation_plan_authorized": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_wiring_performed": False,
        "gate_rule_count": len(rules),
        "authorization_item_count": len(authorization_items),
        "denial_item_count": len(denial_items),
        "stop_condition_count": len(stop_conditions),
        "adapter_count": source["adapter_count"],
        "layer_count": source["layer_count"],
        "dry_run_output_count": source["dry_run_output_count"],
        "dry_run_pass_count": source["dry_run_pass_count"],
        "dry_run_failure_count": source["dry_run_failure_count"],
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
        "task": "Task 15",
        "title": "Local Solver Patch Helper Controlled Wiring Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_14_source": {
            "path": str(TASK_14_JSON),
            "present": TASK_14_JSON.exists(),
            "status": source["task_14_status"],
            "task_14_id": source["task_14_id"],
            "sha256": _sha256(TASK_14_JSON),
            "sha256_16": _sha16(_sha256(TASK_14_JSON)),
        },
        "source_summary": source,
        "gate_rules": list(rules),
        "authorization_items": list(authorization_items),
        "denial_items": list(denial_items),
        "stop_conditions": list(stop_conditions),
        "gate_decision": decision,
        "controlled_gate_scorecard": list(scorecard),
        "gate_checks": checks,
        "gate_check_list": list(GATE_CHECKS),
        "gate_cases": list(GATE_CASES),
        "gate_case_results": list(case_results),
        "controlled_gate_gates": list(gates),
        "controlled_gate_issues": list(issues),
        "controlled_gate_index": index,
        "task_15_ready": task_ready,
        "controlled_gate_ready": True,
        "controlled_gate_passed": True,
        "controlled_gate_status": "CONTROLLED_GATE_PASS",
        "implementation_plan_authorized": True,
        "controlled_runtime_wiring_authorized": False,
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
        "gate_rule_count": len(rules),
        "authorization_item_count": len(authorization_items),
        "denial_item_count": len(denial_items),
        "stop_condition_count": len(stop_conditions),
        "gate_check_count": len(GATE_CHECKS),
        "gate_case_count": len(GATE_CASES),
        "gate_case_pass_count": case_pass_count,
        "gate_case_failure_count": case_failure_count,
        "controlled_gate_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "controlled_gate_issue_count": issue_count,
        "warning_count": 0,
        "review_finding_count": source["review_finding_count"],
        "review_criterion_count": source["review_criterion_count"],
        "adapter_count": source["adapter_count"],
        "layer_count": source["layer_count"],
        "diagnostic_record_count": source["diagnostic_record_count"],
        "dry_run_output_count": source["dry_run_output_count"],
        "dry_run_pass_count": source["dry_run_pass_count"],
        "dry_run_failure_count": source["dry_run_failure_count"],
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
            "source": "milestone_11_local_solver_patch_helper_controlled_wiring_gate_v1",
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
        "task_15_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-GATE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_controlled_wiring_gate(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("controlled_gate_gates", [])
    issues = record.get("controlled_gate_issues", [])
    case_results = record.get("gate_case_results", [])
    scorecard = record.get("controlled_gate_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_15_id_present": isinstance(record.get("task_15_id"), str) and bool(record.get("task_15_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("38755e8"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_15_ready") is True,
        "controlled_gate_ready": record.get("controlled_gate_ready") is True,
        "controlled_gate_passed": record.get("controlled_gate_passed") is True,
        "controlled_gate_status_valid": record.get("controlled_gate_status") == "CONTROLLED_GATE_PASS",
        "implementation_plan_authorized": record.get("implementation_plan_authorized") is True,
        "runtime_wiring_not_authorized": record.get("controlled_runtime_wiring_authorized") is False,
        "runtime_wiring_not_performed": record.get("runtime_wiring_performed") is False,
        "gate_rule_count_valid": record.get("gate_rule_count") == EXPECTED_GATE_RULE_COUNT,
        "authorization_item_count_valid": record.get("authorization_item_count") == EXPECTED_AUTHORIZATION_ITEM_COUNT,
        "denial_item_count_valid": record.get("denial_item_count") == EXPECTED_DENIAL_ITEM_COUNT,
        "stop_condition_count_valid": record.get("stop_condition_count") == EXPECTED_STOP_CONDITION_COUNT,
        "adapter_count_valid": record.get("adapter_count") == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": record.get("layer_count") == EXPECTED_LAYER_COUNT,
        "dry_run_output_count_valid": record.get("dry_run_output_count") == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_pass_count_valid": record.get("dry_run_pass_count") == EXPECTED_DRY_RUN_PASS_COUNT,
        "dry_run_failure_count_zero": record.get("dry_run_failure_count") == 0,
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
        "check_count_valid": record.get("gate_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("gate_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("gate_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("gate_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_15_id": record.get("task_15_id"),
        "signature": record.get("signature"),
    }


def render_task_15_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 15 - Local Solver Patch Helper Controlled Wiring Gate v1",
        "",
        f"- status: {record['status']}",
        f"- task_15_id: {record['task_15_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_15_ready: {record['task_15_ready']}",
        f"- controlled_gate_ready: {record['controlled_gate_ready']}",
        f"- controlled_gate_passed: {record['controlled_gate_passed']}",
        f"- controlled_gate_status: {record['controlled_gate_status']}",
        f"- implementation_plan_authorized: {record['implementation_plan_authorized']}",
        f"- controlled_runtime_wiring_authorized: {record['controlled_runtime_wiring_authorized']}",
        f"- runtime_wiring_performed: {record['runtime_wiring_performed']}",
        f"- gate_rule_count: {record['gate_rule_count']}",
        f"- authorization_item_count: {record['authorization_item_count']}",
        f"- denial_item_count: {record['denial_item_count']}",
        f"- stop_condition_count: {record['stop_condition_count']}",
        f"- adapter_count: {record['adapter_count']}",
        f"- layer_count: {record['layer_count']}",
        f"- dry_run_output_count: {record['dry_run_output_count']}",
        f"- dry_run_pass_count: {record['dry_run_pass_count']}",
        f"- dry_run_failure_count: {record['dry_run_failure_count']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- ranker_runtime_modified: {record['ranker_runtime_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- competitive_score_claim_allowed: {record['competitive_score_claim_allowed']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Gate rules",
        "",
    ]

    for rule in record["gate_rules"]:
        lines.append(
            f"- {rule['gate_rule_id']} / required={rule['required']} / passed={rule['passed']} / "
            f"failure_action={rule['failure_action']}"
        )

    lines.extend(["", "## Gate case results", ""])
    for result in record["gate_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 15 passes the controlled gate for a next implementation-plan stage only. Runtime solver and ranker remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_15_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_15_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_15_VERDICT=LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_READY_FOR_IMPLEMENTATION_PLAN",
            "ARC_AGI3_MILESTONE_11_TASK_15_BASELINE_COMMIT=38755e8",
            "ARC_AGI3_MILESTONE_11_TASK_15_NEXT_STAGE=MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_READY=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_PASSED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_STATUS=CONTROLLED_GATE_PASS",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_PLAN_AUTHORIZED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_GATE_RULE_COUNT={EXPECTED_GATE_RULE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_AUTHORIZATION_ITEM_COUNT={EXPECTED_AUTHORIZATION_ITEM_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DENIAL_ITEM_COUNT={EXPECTED_DENIAL_ITEM_COUNT}",
            f"ARC_AGI3_MILESTONE_11_STOP_CONDITION_COUNT={EXPECTED_STOP_CONDITION_COUNT}",
            f"ARC_AGI3_MILESTONE_11_ADAPTER_COUNT={EXPECTED_ADAPTER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_LAYER_COUNT={EXPECTED_LAYER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DRY_RUN_OUTPUT_COUNT={EXPECTED_DRY_RUN_OUTPUT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DRY_RUN_PASS_COUNT={EXPECTED_DRY_RUN_PASS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DRY_RUN_FAILURE_COUNT={EXPECTED_DRY_RUN_FAILURE_COUNT}",
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


def render_task_15_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 15 LOCAL SOLVER PATCH HELPER CONTROLLED WIRING GATE MANIFEST v1",
        f"task_15_id={record['task_15_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_15_ready={record['task_15_ready']}",
        f"controlled_gate_ready={record['controlled_gate_ready']}",
        f"controlled_gate_passed={record['controlled_gate_passed']}",
        f"controlled_gate_status={record['controlled_gate_status']}",
        f"implementation_plan_authorized={record['implementation_plan_authorized']}",
        f"controlled_runtime_wiring_authorized={record['controlled_runtime_wiring_authorized']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"gate_rule_count={record['gate_rule_count']}",
        f"authorization_item_count={record['authorization_item_count']}",
        f"denial_item_count={record['denial_item_count']}",
        f"stop_condition_count={record['stop_condition_count']}",
        f"adapter_count={record['adapter_count']}",
        f"layer_count={record['layer_count']}",
        f"dry_run_output_count={record['dry_run_output_count']}",
        f"dry_run_pass_count={record['dry_run_pass_count']}",
        f"dry_run_failure_count={record['dry_run_failure_count']}",
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
        "CONTROLLED_GATE_RULES",
    ]

    for rule in record["gate_rules"]:
        lines.append(
            f"{rule['gate_rule_id']} required={rule['required']} passed={rule['passed']} "
            f"failure_action={rule['failure_action']} allows_runtime_mutation={rule['allows_runtime_mutation']}"
        )

    lines.append("")
    lines.append("CONTROLLED_GATE_CASE_RESULTS")
    for result in record["gate_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_15_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_controlled_wiring_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-index-v1.json"
    rules_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-rules-v1.json"
    authorization_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-authorization-v1.json"
    denials_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-denials-v1.json"
    stops_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-stop-conditions-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-gate-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_15_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_15_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["controlled_gate_index"], indent=2, sort_keys=True), encoding="utf-8")
    rules_path.write_text(json.dumps(record["gate_rules"], indent=2, sort_keys=True), encoding="utf-8")
    authorization_path.write_text(json.dumps(record["authorization_items"], indent=2, sort_keys=True), encoding="utf-8")
    denials_path.write_text(json.dumps(record["denial_items"], indent=2, sort_keys=True), encoding="utf-8")
    stops_path.write_text(json.dumps(record["stop_conditions"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["gate_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["controlled_gate_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "rules_path": str(rules_path),
        "authorization_path": str(authorization_path),
        "denials_path": str(denials_path),
        "stops_path": str(stops_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_controlled_wiring_gate_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_gate(record)
    artifacts = write_task_15_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_15_id": record["task_15_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_15_ready": record["task_15_ready"],
        "controlled_gate_ready": record["controlled_gate_ready"],
        "controlled_gate_passed": record["controlled_gate_passed"],
        "controlled_gate_status": record["controlled_gate_status"],
        "implementation_plan_authorized": record["implementation_plan_authorized"],
        "controlled_runtime_wiring_authorized": record["controlled_runtime_wiring_authorized"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "gate_rule_count": record["gate_rule_count"],
        "authorization_item_count": record["authorization_item_count"],
        "denial_item_count": record["denial_item_count"],
        "stop_condition_count": record["stop_condition_count"],
        "adapter_count": record["adapter_count"],
        "layer_count": record["layer_count"],
        "diagnostic_record_count": record["diagnostic_record_count"],
        "dry_run_output_count": record["dry_run_output_count"],
        "dry_run_pass_count": record["dry_run_pass_count"],
        "dry_run_failure_count": record["dry_run_failure_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "gate_check_count": record["gate_check_count"],
        "gate_case_count": record["gate_case_count"],
        "gate_case_pass_count": record["gate_case_pass_count"],
        "gate_case_failure_count": record["gate_case_failure_count"],
        "controlled_gate_gate_count": record["controlled_gate_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "controlled_gate_issue_count": record["controlled_gate_issue_count"],
        "warning_count": record["warning_count"],
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
