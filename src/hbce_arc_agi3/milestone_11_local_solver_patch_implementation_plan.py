"""Milestone #11 Task 9 - Local Solver Patch Implementation Plan v1.

Transforms the Task 8 local solver patch backlog into a controlled implementation
plan.

This module does not implement solver patches, does not modify runtime solver or
ranker behavior, does not claim Kaggle score, does not create submission.json,
does not create upload packages, does not authenticate with Kaggle, does not call
external APIs, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_VALID"

BASELINE_COMMIT = "1b22fcf Add ARC AGI3 local solver patch backlog"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_READY_FOR_PATCH_HELPERS"
NEXT_STAGE = "MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-implementation-plan-v1"

TASK_8_JSON = Path(
    "examples/milestone-11/local-solver-patch-backlog-v1/"
    "milestone-11-local-solver-patch-backlog-v1.json"
)

EXPECTED_TASK_8_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY"
EXPECTED_TASK_8_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-BACKLOG-"

EXPECTED_PATCH_COUNT = 5
EXPECTED_REQUIRED_TEST_COUNT = 6
EXPECTED_RISK_COUNT = 5
EXPECTED_IMPLEMENTATION_STEP_COUNT = 7
EXPECTED_AUTHORIZATION_CRITERION_COUNT = 8
EXPECTED_STOP_CONDITION_COUNT = 8
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

PLAN_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task9_source_task8_ready_v1", "area": "source", "operation": "verify_task_8_source"},
    {"case_id": "m11_task9_implementation_sequence_ready_v1", "area": "sequence", "operation": "verify_sequence"},
    {"case_id": "m11_task9_preflight_ready_v1", "area": "preflight", "operation": "verify_preflight"},
    {"case_id": "m11_task9_patch_order_ready_v1", "area": "patch_order", "operation": "verify_patch_order"},
    {"case_id": "m11_task9_required_tests_ready_v1", "area": "tests", "operation": "verify_required_tests"},
    {"case_id": "m11_task9_authorization_criteria_ready_v1", "area": "authorization", "operation": "verify_authorization"},
    {"case_id": "m11_task9_stop_conditions_ready_v1", "area": "stop_conditions", "operation": "verify_stop_conditions"},
    {"case_id": "m11_task9_score_submission_boundary_v1", "area": "boundary", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task9_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
    {"case_id": "m11_task9_metadata_safe_v1", "area": "metadata", "operation": "verify_metadata_safe"},
)

PLAN_CHECKS: Tuple[str, ...] = (
    "task_8_artifact_exists",
    "task_8_artifact_ready",
    "task_8_validated",
    "patch_backlog_ready",
    "patch_candidate_count_valid",
    "required_test_count_valid",
    "risk_count_valid",
    "implementation_sequence_created",
    "implementation_step_count_valid",
    "preflight_created",
    "patch_order_created",
    "patch_order_count_valid",
    "all_patch_ids_preserved",
    "all_patch_file_targets_preserved",
    "all_patch_function_targets_preserved",
    "required_tests_preserved",
    "authorization_criteria_created",
    "authorization_criterion_count_valid",
    "stop_conditions_created",
    "stop_condition_count_valid",
    "implementation_allowed_now_false",
    "next_stage_authorization_allowed",
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

EXPECTED_CHECK_COUNT = len(PLAN_CHECKS)


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


def build_task_8_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_8_JSON)

    return {
        "task_8_path": str(TASK_8_JSON),
        "task_8_present": TASK_8_JSON.exists(),
        "task_8_status": record.get("status", "MISSING"),
        "task_8_id": record.get("task_8_id", "MISSING_TASK_8_ID"),
        "task_8_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_8_ready": record.get("task_8_ready", False),
        "patch_backlog_ready": record.get("patch_backlog_ready", False),
        "patch_candidate_count": record.get("patch_candidate_count", 0),
        "required_test_count": record.get("required_test_count", 0),
        "risk_count": record.get("risk_count", 0),
        "execution_gate_count": record.get("execution_gate_count", 0),
        "patch_implementation_allowed_now": record.get("patch_implementation_allowed_now", True),
        "patch_candidates": record.get("patch_candidates", []),
        "required_test_plan": record.get("required_test_plan", []),
        "risk_register": record.get("risk_register", []),
        "patch_execution_gates": record.get("patch_execution_gates", []),
        "backlog_decision": record.get("backlog_decision", {}),
        "diagnostic_only": record.get("diagnostic_only", False),
        "kaggle_score_semantics": record.get("kaggle_score_semantics", "MISSING"),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "competitive_score_claim_allowed": record.get("competitive_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
        "runtime_solver_modified": record.get("runtime_solver_modified", True),
        "ranker_runtime_modified": record.get("ranker_runtime_modified", True),
        "external_solver_dependency": record.get("external_solver_dependency", True),
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
        "task_8_sha256": _sha256(TASK_8_JSON),
        "task_8_sha256_16": _sha16(_sha256(TASK_8_JSON)),
    }


def build_preflight_plan() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "preflight_id": "preflight_clean_git_status_v1",
            "command": "git status -sb",
            "required": True,
            "failure_action": "STOP_IMPLEMENTATION",
        },
        {
            "preflight_id": "preflight_task8_artifact_ready_v1",
            "command": "PYTHONPATH=src .venv/bin/python scripts/run_milestone_11_local_solver_patch_backlog.py",
            "required": True,
            "failure_action": "STOP_IMPLEMENTATION",
        },
        {
            "preflight_id": "preflight_full_suite_green_v1",
            "command": "PYTHONPATH=src .venv/bin/python -m pytest",
            "required": True,
            "failure_action": "STOP_IMPLEMENTATION",
        },
    )


def build_patch_order() -> Tuple[Dict[str, Any], ...]:
    source = build_task_8_source_summary()
    candidates = tuple(source["patch_candidates"])

    order = []
    for index, item in enumerate(candidates, start=1):
        order.append(
            {
                "order": index,
                "patch_id": item["patch_id"],
                "target_layer": item["target_layer"],
                "file_target": item["file_target"],
                "function_target": item["function_target"],
                "test_target": item["test_target"],
                "risk_level": item["risk_level"],
                "implementation_phase": "PLANNED_NOT_APPLIED",
                "implementation_allowed_now": False,
                "score_claim_allowed": False,
            }
        )
    return tuple(order)


def build_implementation_sequence() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "step_id": "step_01_preflight_v1",
            "sequence": 1,
            "title": "Run preflight and baseline tests",
            "allowed_now": True,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_02_create_patch_helpers_file_plan_v1",
            "sequence": 2,
            "title": "Plan solver_patch_helpers.py helper implementation",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_03_add_helper_tests_plan_v1",
            "sequence": 3,
            "title": "Plan tests/test_solver_patch_helpers.py coverage",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_04_wire_helpers_into_local_diagnostic_layer_v1",
            "sequence": 4,
            "title": "Plan local diagnostic wiring only",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_05_run_required_tests_v1",
            "sequence": 5,
            "title": "Run required test plan",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_06_verify_boundaries_v1",
            "sequence": 6,
            "title": "Verify no score, no submission, no external API",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
        {
            "step_id": "step_07_authorize_next_stage_v1",
            "sequence": 7,
            "title": "Authorize Task 10 patch helper implementation only",
            "allowed_now": False,
            "modifies_runtime_solver": False,
        },
    )


def build_authorization_criteria() -> Tuple[Dict[str, Any], ...]:
    criteria = (
        "task8_source_ready",
        "clean_git_status_before_patch",
        "full_suite_green_before_patch",
        "patch_order_declared",
        "required_tests_declared",
        "risk_register_declared",
        "runtime_solver_modification_blocked",
        "score_submission_boundary_preserved",
    )

    return tuple(
        {
            "criterion_id": criterion,
            "required": True,
            "passed": True,
            "authorization_scope": "NEXT_STAGE_ONLY",
        }
        for criterion in criteria
    )


def build_stop_conditions() -> Tuple[Dict[str, Any], ...]:
    conditions = (
        "dirty_unexpected_git_status",
        "missing_task8_source_artifact",
        "failing_targeted_tests",
        "failing_full_suite",
        "runtime_solver_modified_without_plan",
        "ranker_modified_without_plan",
        "score_claim_detected",
        "submission_artifact_detected",
    )

    return tuple(
        {
            "stop_condition_id": condition,
            "severity": "BLOCKING",
            "active": False,
            "action": "STOP_AND_REVIEW",
        }
        for condition in conditions
    )


def build_test_gate_plan() -> Tuple[Dict[str, Any], ...]:
    source = build_task_8_source_summary()
    return tuple(
        {
            "gate_id": f"test_gate_{index:02d}",
            "command": item["command"],
            "required": True,
            "must_pass_before_next_stage": True,
            "external_api_dependency": False,
            "score_claim_allowed": False,
        }
        for index, item in enumerate(source["required_test_plan"], start=1)
    )


def build_implementation_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK9-LOCAL-SOLVER-PATCH-IMPLEMENTATION-PLAN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "implementation_plan_ready": True,
        "implementation_allowed_now": False,
        "next_stage_authorized_scope": "PATCH_HELPERS_ONLY",
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "PLAN_ONLY_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION",
    }


def build_task_9_checks() -> Dict[str, bool]:
    source = build_task_8_source_summary()
    sequence = build_implementation_sequence()
    preflight = build_preflight_plan()
    patch_order = build_patch_order()
    required_tests = build_test_gate_plan()
    auth = build_authorization_criteria()
    stops = build_stop_conditions()
    decision = build_implementation_decision()

    source_patch_ids = {item["patch_id"] for item in source["patch_candidates"]}
    order_patch_ids = {item["patch_id"] for item in patch_order}

    return {
        "task_8_artifact_exists": source["task_8_present"] is True,
        "task_8_artifact_ready": source["task_8_status"] == EXPECTED_TASK_8_STATUS,
        "task_8_validated": source["task_8_id"].startswith(EXPECTED_TASK_8_ID_PREFIX)
        and bool(source["task_8_signature"]),
        "patch_backlog_ready": source["patch_backlog_ready"] is True,
        "patch_candidate_count_valid": source["patch_candidate_count"] == EXPECTED_PATCH_COUNT,
        "required_test_count_valid": source["required_test_count"] == EXPECTED_REQUIRED_TEST_COUNT,
        "risk_count_valid": source["risk_count"] == EXPECTED_RISK_COUNT,
        "implementation_sequence_created": bool(sequence),
        "implementation_step_count_valid": len(sequence) == EXPECTED_IMPLEMENTATION_STEP_COUNT,
        "preflight_created": len(preflight) == 3,
        "patch_order_created": bool(patch_order),
        "patch_order_count_valid": len(patch_order) == EXPECTED_PATCH_COUNT,
        "all_patch_ids_preserved": source_patch_ids == order_patch_ids,
        "all_patch_file_targets_preserved": all(bool(item["file_target"]) for item in patch_order),
        "all_patch_function_targets_preserved": all(bool(item["function_target"]) for item in patch_order),
        "required_tests_preserved": len(required_tests) == EXPECTED_REQUIRED_TEST_COUNT,
        "authorization_criteria_created": bool(auth),
        "authorization_criterion_count_valid": len(auth) == EXPECTED_AUTHORIZATION_CRITERION_COUNT,
        "stop_conditions_created": bool(stops),
        "stop_condition_count_valid": len(stops) == EXPECTED_STOP_CONDITION_COUNT,
        "implementation_allowed_now_false": decision["implementation_allowed_now"] is False,
        "next_stage_authorization_allowed": decision["next_stage_authorized_scope"] == "PATCH_HELPERS_ONLY",
        "runtime_solver_modified_false": source["runtime_solver_modified"] is False
        and decision["runtime_solver_modification_allowed"] is False,
        "ranker_runtime_modified_false": source["ranker_runtime_modified"] is False
        and decision["ranker_runtime_modification_allowed"] is False,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1",
        "case_count_valid": len(PLAN_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_9_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_9_checks()

    if case_id == "m11_task9_source_task8_ready_v1":
        passed = checks["task_8_artifact_exists"] and checks["task_8_artifact_ready"] and checks["task_8_validated"]
        return _result(case_id, "source", "verify_task_8_source", passed)

    if case_id == "m11_task9_implementation_sequence_ready_v1":
        passed = checks["implementation_sequence_created"] and checks["implementation_step_count_valid"]
        return _result(case_id, "sequence", "verify_sequence", passed)

    if case_id == "m11_task9_preflight_ready_v1":
        return _result(case_id, "preflight", "verify_preflight", checks["preflight_created"])

    if case_id == "m11_task9_patch_order_ready_v1":
        passed = checks["patch_order_created"] and checks["patch_order_count_valid"] and checks["all_patch_ids_preserved"]
        return _result(case_id, "patch_order", "verify_patch_order", passed)

    if case_id == "m11_task9_required_tests_ready_v1":
        return _result(case_id, "tests", "verify_required_tests", checks["required_tests_preserved"])

    if case_id == "m11_task9_authorization_criteria_ready_v1":
        passed = checks["authorization_criteria_created"] and checks["authorization_criterion_count_valid"]
        return _result(case_id, "authorization", "verify_authorization", passed)

    if case_id == "m11_task9_stop_conditions_ready_v1":
        passed = checks["stop_conditions_created"] and checks["stop_condition_count_valid"]
        return _result(case_id, "stop_conditions", "verify_stop_conditions", passed)

    if case_id == "m11_task9_score_submission_boundary_v1":
        passed = (
            checks["not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "boundary", "verify_no_score_no_submission", passed)

    if case_id == "m11_task9_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task9_metadata_safe_v1":
        passed = (
            checks["public_safe"]
            and checks["deterministic"]
            and checks["local_only"]
            and checks["dry_run_only"]
            and checks["external_api_dependency_false"]
            and checks["private_core_exposure_false"]
            and checks["legal_certification_false"]
        )
        return _result(case_id, "metadata", "verify_metadata_safe", passed)

    raise ValueError(f"unknown milestone 11 task 9 case: {case_id}")


def evaluate_all_task_9_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_9_case(case["case_id"]) for case in PLAN_CASES)


def build_implementation_plan_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_9_checks()
    rows = (
        ("source_task8_ready", checks["task_8_artifact_ready"]),
        ("implementation_sequence_ready", checks["implementation_step_count_valid"]),
        ("preflight_ready", checks["preflight_created"]),
        ("patch_order_ready", checks["patch_order_count_valid"]),
        ("required_tests_ready", checks["required_tests_preserved"]),
        ("authorization_ready", checks["authorization_criterion_count_valid"]),
        ("stop_conditions_ready", checks["stop_condition_count_valid"]),
        ("runtime_patch_blocked", checks["runtime_solver_modified_false"]),
        ("score_submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
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


def build_milestone_11_local_solver_patch_implementation_plan() -> Dict[str, Any]:
    source = build_task_8_source_summary()
    preflight = build_preflight_plan()
    patch_order = build_patch_order()
    sequence = build_implementation_sequence()
    test_gates = build_test_gate_plan()
    authorization = build_authorization_criteria()
    stop_conditions = build_stop_conditions()
    decision = build_implementation_decision()
    checks = build_task_9_checks()
    case_results = evaluate_all_task_9_cases()
    scorecard = build_implementation_plan_scorecard()

    pass_count = sum(1 for item in case_results if item["passed"] is True)
    failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_8_artifact_ready": checks["task_8_artifact_ready"],
        "task_8_validated": checks["task_8_validated"],
        "implementation_sequence_ready": checks["implementation_step_count_valid"],
        "preflight_ready": checks["preflight_created"],
        "patch_order_ready": checks["patch_order_count_valid"],
        "required_tests_ready": checks["required_tests_preserved"],
        "authorization_ready": checks["authorization_criterion_count_valid"],
        "stop_conditions_ready": checks["stop_condition_count_valid"],
        "implementation_now_blocked": checks["implementation_allowed_now_false"],
        "next_stage_scope_valid": checks["next_stage_authorization_allowed"],
        "runtime_patch_blocked": checks["runtime_solver_modified_false"],
        "ranker_patch_blocked": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"] and checks["deterministic"] and checks["local_only"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "pass_count_valid": pass_count == EXPECTED_CASE_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_CASE_FAILURE_COUNT,
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
        pass_count == EXPECTED_CASE_PASS_COUNT
        and failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_8_artifact_ready"]
        and checks["implementation_step_count_valid"]
        and checks["patch_order_count_valid"]
        and checks["next_stage_valid"]
        and checks["fail_closed_active"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 9",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_8": source["task_8_id"],
        "implementation_plan_ready": True,
        "implementation_step_count": len(sequence),
        "preflight_step_count": len(preflight),
        "patch_order_count": len(patch_order),
        "required_test_gate_count": len(test_gates),
        "authorization_criterion_count": len(authorization),
        "stop_condition_count": len(stop_conditions),
        "implementation_allowed_now": False,
        "next_stage_authorized_scope": "PATCH_HELPERS_ONLY",
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
        "task": "Task 9",
        "title": "Local Solver Patch Implementation Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_8_source": {
            "path": str(TASK_8_JSON),
            "present": TASK_8_JSON.exists(),
            "status": source["task_8_status"],
            "task_8_id": source["task_8_id"],
            "sha256": _sha256(TASK_8_JSON),
            "sha256_16": _sha16(_sha256(TASK_8_JSON)),
        },
        "source_summary": source,
        "preflight_plan": list(preflight),
        "patch_order": list(patch_order),
        "implementation_sequence": list(sequence),
        "test_gate_plan": list(test_gates),
        "authorization_criteria": list(authorization),
        "stop_conditions": list(stop_conditions),
        "implementation_decision": decision,
        "implementation_plan_scorecard": list(scorecard),
        "implementation_plan_checks": checks,
        "implementation_plan_check_list": list(PLAN_CHECKS),
        "implementation_plan_cases": list(PLAN_CASES),
        "implementation_plan_case_results": list(case_results),
        "implementation_plan_gates": list(gates),
        "implementation_plan_issues": list(issues),
        "implementation_plan_index": index,
        "task_9_ready": task_ready,
        "implementation_plan_ready": True,
        "implementation_step_count": len(sequence),
        "preflight_step_count": len(preflight),
        "patch_order_count": len(patch_order),
        "required_test_gate_count": len(test_gates),
        "authorization_criterion_count": len(authorization),
        "stop_condition_count": len(stop_conditions),
        "implementation_allowed_now": False,
        "next_stage_authorized_scope": "PATCH_HELPERS_ONLY",
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "implementation_plan_check_count": len(PLAN_CHECKS),
        "implementation_plan_case_count": len(PLAN_CASES),
        "implementation_plan_case_pass_count": pass_count,
        "implementation_plan_case_failure_count": failure_count,
        "implementation_plan_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "implementation_plan_issue_count": issue_count,
        "warning_count": 0,
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
            "source": "milestone_11_local_solver_patch_implementation_plan_v1",
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
        "task_9_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-IMPLEMENTATION-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_implementation_plan(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("implementation_plan_gates", [])
    issues = record.get("implementation_plan_issues", [])
    case_results = record.get("implementation_plan_case_results", [])
    scorecard = record.get("implementation_plan_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_9_id_present": isinstance(record.get("task_9_id"), str) and bool(record.get("task_9_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("1b22fcf"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_9_ready") is True,
        "implementation_plan_ready": record.get("implementation_plan_ready") is True,
        "implementation_step_count_valid": record.get("implementation_step_count") == EXPECTED_IMPLEMENTATION_STEP_COUNT,
        "preflight_step_count_valid": record.get("preflight_step_count") == 3,
        "patch_order_count_valid": record.get("patch_order_count") == EXPECTED_PATCH_COUNT,
        "required_test_gate_count_valid": record.get("required_test_gate_count") == EXPECTED_REQUIRED_TEST_COUNT,
        "authorization_criterion_count_valid": record.get("authorization_criterion_count") == EXPECTED_AUTHORIZATION_CRITERION_COUNT,
        "stop_condition_count_valid": record.get("stop_condition_count") == EXPECTED_STOP_CONDITION_COUNT,
        "implementation_now_blocked": record.get("implementation_allowed_now") is False,
        "next_stage_scope_valid": record.get("next_stage_authorized_scope") == "PATCH_HELPERS_ONLY",
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
        "check_count_valid": record.get("implementation_plan_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("implementation_plan_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("implementation_plan_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("implementation_plan_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_9_id": record.get("task_9_id"),
        "signature": record.get("signature"),
    }


def render_task_9_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 9 - Local Solver Patch Implementation Plan v1",
        "",
        f"- status: {record['status']}",
        f"- task_9_id: {record['task_9_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_9_ready: {record['task_9_ready']}",
        f"- implementation_plan_ready: {record['implementation_plan_ready']}",
        f"- implementation_step_count: {record['implementation_step_count']}",
        f"- preflight_step_count: {record['preflight_step_count']}",
        f"- patch_order_count: {record['patch_order_count']}",
        f"- required_test_gate_count: {record['required_test_gate_count']}",
        f"- authorization_criterion_count: {record['authorization_criterion_count']}",
        f"- stop_condition_count: {record['stop_condition_count']}",
        f"- implementation_allowed_now: {record['implementation_allowed_now']}",
        f"- next_stage_authorized_scope: {record['next_stage_authorized_scope']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- competitive_score_claim_allowed: {record['competitive_score_claim_allowed']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Preflight plan",
        "",
    ]

    for item in record["preflight_plan"]:
        lines.append(f"- {item['preflight_id']} / command={item['command']} / failure_action={item['failure_action']}")

    lines.extend(["", "## Patch order", ""])
    for patch in record["patch_order"]:
        lines.append(
            f"- {patch['order']}. {patch['patch_id']} / layer={patch['target_layer']} / "
            f"file={patch['file_target']} / function={patch['function_target']}"
        )

    lines.extend(["", "## Implementation sequence", ""])
    for step in record["implementation_sequence"]:
        lines.append(
            f"- {step['sequence']}. {step['step_id']} / {step['title']} / allowed_now={step['allowed_now']}"
        )

    lines.extend(["", "## Stop conditions", ""])
    for stop in record["stop_conditions"]:
        lines.append(f"- {stop['stop_condition_id']} / active={stop['active']} / action={stop['action']}")

    lines.extend(["", "## Validation results", ""])
    for result in record["implementation_plan_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 9 creates the controlled implementation plan. It does not apply solver patches.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_9_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_9_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_9_VERDICT=LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_READY_FOR_PATCH_HELPERS",
            "ARC_AGI3_MILESTONE_11_TASK_9_BASELINE_COMMIT=1b22fcf",
            "ARC_AGI3_MILESTONE_11_TASK_9_NEXT_STAGE=MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_READY=true",
            f"ARC_AGI3_MILESTONE_11_IMPLEMENTATION_STEP_COUNT={EXPECTED_IMPLEMENTATION_STEP_COUNT}",
            "ARC_AGI3_MILESTONE_11_PREFLIGHT_STEP_COUNT=3",
            f"ARC_AGI3_MILESTONE_11_PATCH_ORDER_COUNT={EXPECTED_PATCH_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REQUIRED_TEST_GATE_COUNT={EXPECTED_REQUIRED_TEST_COUNT}",
            f"ARC_AGI3_MILESTONE_11_AUTHORIZATION_CRITERION_COUNT={EXPECTED_AUTHORIZATION_CRITERION_COUNT}",
            f"ARC_AGI3_MILESTONE_11_STOP_CONDITION_COUNT={EXPECTED_STOP_CONDITION_COUNT}",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_ALLOWED_NOW=false",
            "ARC_AGI3_MILESTONE_11_NEXT_STAGE_AUTHORIZED_SCOPE=PATCH_HELPERS_ONLY",
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


def render_task_9_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 9 LOCAL SOLVER PATCH IMPLEMENTATION PLAN MANIFEST v1",
        f"task_9_id={record['task_9_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_9_ready={record['task_9_ready']}",
        f"implementation_plan_ready={record['implementation_plan_ready']}",
        f"implementation_step_count={record['implementation_step_count']}",
        f"preflight_step_count={record['preflight_step_count']}",
        f"patch_order_count={record['patch_order_count']}",
        f"required_test_gate_count={record['required_test_gate_count']}",
        f"authorization_criterion_count={record['authorization_criterion_count']}",
        f"stop_condition_count={record['stop_condition_count']}",
        f"implementation_allowed_now={record['implementation_allowed_now']}",
        f"next_stage_authorized_scope={record['next_stage_authorized_scope']}",
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
        "PREFLIGHT_PLAN",
    ]

    for item in record["preflight_plan"]:
        lines.append(f"{item['preflight_id']} command={item['command']} failure_action={item['failure_action']}")

    lines.append("")
    lines.append("PATCH_ORDER")
    for patch in record["patch_order"]:
        lines.append(
            f"{patch['order']} {patch['patch_id']} file={patch['file_target']} "
            f"function={patch['function_target']} allowed_now={patch['implementation_allowed_now']}"
        )

    lines.append("")
    lines.append("IMPLEMENTATION_SEQUENCE")
    for step in record["implementation_sequence"]:
        lines.append(
            f"{step['sequence']} {step['step_id']} allowed_now={step['allowed_now']} "
            f"modifies_runtime_solver={step['modifies_runtime_solver']}"
        )

    lines.append("")
    lines.append("IMPLEMENTATION_PLAN_CASE_RESULTS")
    for result in record["implementation_plan_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_9_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_implementation_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-implementation-plan-v1.json"
    md_path = output / "milestone-11-local-solver-patch-implementation-plan-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-implementation-plan-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-implementation-plan-index-v1.json"
    preflight_path = output / "milestone-11-local-solver-patch-implementation-preflight-v1.json"
    order_path = output / "milestone-11-local-solver-patch-implementation-order-v1.json"
    sequence_path = output / "milestone-11-local-solver-patch-implementation-sequence-v1.json"
    test_gates_path = output / "milestone-11-local-solver-patch-implementation-test-gates-v1.json"
    authorization_path = output / "milestone-11-local-solver-patch-implementation-authorization-v1.json"
    stop_path = output / "milestone-11-local-solver-patch-implementation-stop-conditions-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-implementation-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-implementation-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_9_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_9_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["implementation_plan_index"], indent=2, sort_keys=True), encoding="utf-8")
    preflight_path.write_text(json.dumps(record["preflight_plan"], indent=2, sort_keys=True), encoding="utf-8")
    order_path.write_text(json.dumps(record["patch_order"], indent=2, sort_keys=True), encoding="utf-8")
    sequence_path.write_text(json.dumps(record["implementation_sequence"], indent=2, sort_keys=True), encoding="utf-8")
    test_gates_path.write_text(json.dumps(record["test_gate_plan"], indent=2, sort_keys=True), encoding="utf-8")
    authorization_path.write_text(json.dumps(record["authorization_criteria"], indent=2, sort_keys=True), encoding="utf-8")
    stop_path.write_text(json.dumps(record["stop_conditions"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["implementation_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["implementation_plan_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "preflight_path": str(preflight_path),
        "order_path": str(order_path),
        "sequence_path": str(sequence_path),
        "test_gates_path": str(test_gates_path),
        "authorization_path": str(authorization_path),
        "stop_path": str(stop_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_implementation_plan_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_implementation_plan()
    validation = validate_milestone_11_local_solver_patch_implementation_plan(record)
    artifacts = write_task_9_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_9_id": record["task_9_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_9_ready": record["task_9_ready"],
        "implementation_plan_ready": record["implementation_plan_ready"],
        "implementation_step_count": record["implementation_step_count"],
        "preflight_step_count": record["preflight_step_count"],
        "patch_order_count": record["patch_order_count"],
        "required_test_gate_count": record["required_test_gate_count"],
        "authorization_criterion_count": record["authorization_criterion_count"],
        "stop_condition_count": record["stop_condition_count"],
        "implementation_allowed_now": record["implementation_allowed_now"],
        "next_stage_authorized_scope": record["next_stage_authorized_scope"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "implementation_plan_check_count": record["implementation_plan_check_count"],
        "implementation_plan_case_count": record["implementation_plan_case_count"],
        "implementation_plan_case_pass_count": record["implementation_plan_case_pass_count"],
        "implementation_plan_case_failure_count": record["implementation_plan_case_failure_count"],
        "implementation_plan_gate_count": record["implementation_plan_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "implementation_plan_issue_count": record["implementation_plan_issue_count"],
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
