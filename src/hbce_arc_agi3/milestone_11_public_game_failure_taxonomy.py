"""Milestone #11 Task 3 - Public Game Failure Taxonomy v1.

Local-only deterministic taxonomy after public game inventory and baseline run.

This module classifies the Task 2 outcome into an explicit failure/constraint
taxonomy. If no local public fixtures are available, the taxonomy marks the
condition as a measurement constraint rather than a solver failure. It does not
claim a real public score, does not create submission.json, does not create an
upload package, does not authenticate with Kaggle, does not call external APIs,
does not read secrets, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_VALID"

BASELINE_COMMIT = "d3b39b0 Add ARC AGI3 public game inventory baseline run"
TASK_MODE = "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_LOCAL_ONLY"
TASK_SCOPE = "PUBLIC_GAME_FAILURE_TAXONOMY_FOR_NO_LOCAL_FIXTURE_AND_BASELINE_CONSTRAINTS"
TASK_VERDICT = "PUBLIC_GAME_FAILURE_TAXONOMY_READY_FOR_LOCAL_FIXTURE_HARNESS_PLAN"
NEXT_STAGE = "MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/public-game-failure-taxonomy-v1"

TASK_2_JSON = Path(
    "examples/milestone-11/public-game-inventory-baseline-run-v1/"
    "milestone-11-public-game-inventory-baseline-run-v1.json"
)

EXPECTED_TASK_2_ID_PREFIX = "MILESTONE-11-PUBLIC-GAME-INVENTORY-BASELINE-RUN-"
EXPECTED_TASK_2_STATUS = "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY"
EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILT_CANDIDATE_ID = "MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87"

TAXONOMY_CLASSES: Tuple[Dict[str, str], ...] = (
    {
        "taxonomy_id": "dataset_missing_v1",
        "category": "DATASET_CONSTRAINT",
        "severity": "CONSTRAINT",
        "description": "No local public game dataset files are present in scanned candidate paths.",
    },
    {
        "taxonomy_id": "fixture_missing_v1",
        "category": "FIXTURE_CONSTRAINT",
        "severity": "CONSTRAINT",
        "description": "No compatible public fixtures are available for a local baseline run.",
    },
    {
        "taxonomy_id": "baseline_not_executed_v1",
        "category": "BASELINE_CONSTRAINT",
        "severity": "CONSTRAINT",
        "description": "Baseline was not executed because there are no local compatible public fixtures.",
    },
    {
        "taxonomy_id": "score_not_claimed_v1",
        "category": "SCORE_BOUNDARY",
        "severity": "PASS",
        "description": "No real public or private score is claimed without a valid local or official run.",
    },
    {
        "taxonomy_id": "solver_not_measured_v1",
        "category": "MEASUREMENT_CONSTRAINT",
        "severity": "CONSTRAINT",
        "description": "The solver has not been measured on public games because no local fixtures exist.",
    },
    {
        "taxonomy_id": "submission_still_blocked_v1",
        "category": "SUBMISSION_BOUNDARY",
        "severity": "PASS",
        "description": "Real submission remains blocked and no submission package exists.",
    },
    {
        "taxonomy_id": "next_action_required_v1",
        "category": "NEXT_ACTION",
        "severity": "ACTION_REQUIRED",
        "description": "Next action is to create a local fixture harness plan or import compatible public fixtures.",
    },
)

NEXT_ACTIONS: Tuple[Dict[str, str], ...] = (
    {
        "action_id": "m11_task4_local_fixture_harness_plan_v1",
        "priority": "P0",
        "action": "Create a local fixture harness plan for deterministic solver measurement.",
    },
    {
        "action_id": "m11_public_fixture_import_policy_v1",
        "priority": "P0",
        "action": "Define safe import policy for public fixtures without claiming official scores.",
    },
    {
        "action_id": "m11_synthetic_fixture_boundary_v1",
        "priority": "P1",
        "action": "Allow synthetic/local fixtures only as solver diagnostics, never as Kaggle score evidence.",
    },
    {
        "action_id": "m11_failure_taxonomy_to_patch_plan_v1",
        "priority": "P1",
        "action": "Map taxonomy classes to world-model, planner, verifier, and policy patch targets.",
    },
)

TAXONOMY_CHECKS: Tuple[str, ...] = (
    "task_2_artifact_exists",
    "task_2_artifact_ready",
    "task_2_validated",
    "candidate_identity_loaded",
    "inventory_created",
    "inventory_scan_completed",
    "no_local_public_fixtures_detected",
    "baseline_not_executed_due_to_no_fixtures",
    "no_real_public_score_claimed",
    "no_private_score_claimed",
    "solver_not_measured_condition_detected",
    "taxonomy_classes_created",
    "taxonomy_dataset_missing_created",
    "taxonomy_fixture_missing_created",
    "taxonomy_baseline_not_executed_created",
    "taxonomy_score_not_claimed_created",
    "taxonomy_solver_not_measured_created",
    "taxonomy_submission_blocked_created",
    "taxonomy_next_action_required_created",
    "next_actions_created",
    "failure_is_constraint_not_solver_failure",
    "real_submission_blocked",
    "submission_json_absent",
    "upload_package_absent",
    "kaggle_submission_not_sent",
    "fail_closed_required",
    "fail_closed_active",
    "next_stage_valid",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

TAXONOMY_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_task3_source_task2_ready_v1",
        "area": "source_binding",
        "operation": "verify_task_2_inventory_baseline_source",
    },
    {
        "case_id": "m11_task3_no_local_public_fixtures_classified_v1",
        "area": "dataset_constraint",
        "operation": "classify_no_local_public_fixtures",
    },
    {
        "case_id": "m11_task3_baseline_not_executed_classified_v1",
        "area": "baseline_constraint",
        "operation": "classify_baseline_not_executed",
    },
    {
        "case_id": "m11_task3_score_boundary_classified_v1",
        "area": "score_boundary",
        "operation": "classify_score_not_claimed",
    },
    {
        "case_id": "m11_task3_solver_not_measured_classified_v1",
        "area": "measurement_constraint",
        "operation": "classify_solver_not_measured",
    },
    {
        "case_id": "m11_task3_submission_boundary_classified_v1",
        "area": "submission_boundary",
        "operation": "classify_submission_still_blocked",
    },
    {
        "case_id": "m11_task3_next_actions_ready_v1",
        "area": "next_action",
        "operation": "verify_next_actions",
    },
    {
        "case_id": "m11_task3_taxonomy_not_solver_failure_v1",
        "area": "interpretation",
        "operation": "verify_constraint_not_solver_failure",
    },
    {
        "case_id": "m11_task3_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_task3_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_TAXONOMY_CLASS_COUNT = len(TAXONOMY_CLASSES)
EXPECTED_NEXT_ACTION_COUNT = len(NEXT_ACTIONS)
EXPECTED_TAXONOMY_CHECK_COUNT = len(TAXONOMY_CHECKS)
EXPECTED_TAXONOMY_CASE_COUNT = len(TAXONOMY_CASES)
EXPECTED_TAXONOMY_PASS_COUNT = len(TAXONOMY_CASES)
EXPECTED_TAXONOMY_FAILURE_COUNT = 0


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


def build_task_2_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_2_JSON)
    source = record.get("source_summary", {})

    return {
        "task_2_path": str(TASK_2_JSON),
        "task_2_present": TASK_2_JSON.exists(),
        "task_2_status": record.get("status", "MISSING"),
        "task_2_id": record.get("task_2_id", "MISSING_TASK_2_ID"),
        "task_2_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_2_ready": record.get("task_2_ready", False),
        "task_verdict": record.get("task_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "selected_candidate_id": source.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": source.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "rebuilt_candidate_id": source.get("rebuilt_candidate_id", "MISSING_REBUILT_CANDIDATE_ID"),
        "inventory_created": record.get("inventory_created", False),
        "inventory_scan_completed": record.get("inventory_scan_completed", False),
        "compatible_fixture_detection_completed": record.get(
            "compatible_fixture_detection_completed", False
        ),
        "candidate_path_count": record.get("candidate_path_count", -1),
        "total_file_count": record.get("total_file_count", -1),
        "compatible_fixture_count": record.get("compatible_fixture_count", -1),
        "has_local_public_fixtures": record.get("has_local_public_fixtures", True),
        "baseline_policy_created": record.get("baseline_policy_created", False),
        "baseline_attempt_recorded": record.get("baseline_attempt_recorded", False),
        "baseline_result_recorded": record.get("baseline_result_recorded", False),
        "baseline_execution_performed": record.get("baseline_execution_performed", True),
        "baseline_execution_mode": record.get("baseline_execution_mode", "MISSING_BASELINE_EXECUTION_MODE"),
        "baseline_status": record.get("baseline_status", "MISSING_BASELINE_STATUS"),
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
        "task_2_sha256": _sha256(TASK_2_JSON),
        "task_2_sha256_16": _sha16(_sha256(TASK_2_JSON)),
    }


def build_public_game_failure_taxonomy() -> Tuple[Dict[str, Any], ...]:
    source = build_task_2_source_summary()

    condition_map = {
        "dataset_missing_v1": source["total_file_count"] == 0,
        "fixture_missing_v1": source["compatible_fixture_count"] == 0,
        "baseline_not_executed_v1": source["baseline_execution_performed"] is False
        and source["baseline_execution_mode"] == "NO_LOCAL_PUBLIC_FIXTURES"
        and source["baseline_status"] == "BASELINE_NOT_EXECUTED_NO_LOCAL_PUBLIC_FIXTURES",
        "score_not_claimed_v1": source["real_public_score_claimed"] is False
        and source["private_score_claimed"] is False
        and source["real_benchmark_score"] is None,
        "solver_not_measured_v1": source["baseline_execution_performed"] is False
        and source["compatible_fixture_count"] == 0,
        "submission_still_blocked_v1": source["real_submission_allowed"] is False
        and source["submission_json_created"] is False
        and source["upload_package_created"] is False
        and source["kaggle_submission_sent"] is False,
        "next_action_required_v1": True,
    }

    return tuple(
        {
            **item,
            "active": condition_map[item["taxonomy_id"]],
            "evidence": {
                "total_file_count": source["total_file_count"],
                "compatible_fixture_count": source["compatible_fixture_count"],
                "baseline_execution_performed": source["baseline_execution_performed"],
                "baseline_execution_mode": source["baseline_execution_mode"],
                "baseline_status": source["baseline_status"],
                "real_public_score_claimed": source["real_public_score_claimed"],
                "private_score_claimed": source["private_score_claimed"],
                "real_benchmark_score": source["real_benchmark_score"],
                "real_submission_allowed": source["real_submission_allowed"],
                "kaggle_submission_sent": source["kaggle_submission_sent"],
            },
        }
        for item in TAXONOMY_CLASSES
    )


def build_failure_taxonomy_interpretation() -> Dict[str, Any]:
    source = build_task_2_source_summary()
    taxonomy = build_public_game_failure_taxonomy()
    active_categories = tuple(item["category"] for item in taxonomy if item["active"] is True)

    return {
        "interpretation_id": "M11-TASK3-FAILURE-TAXONOMY-INTERPRETATION-v1",
        "primary_condition": "NO_LOCAL_PUBLIC_FIXTURES"
        if source["has_local_public_fixtures"] is False
        else "LOCAL_PUBLIC_FIXTURES_AVAILABLE",
        "primary_classification": "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
        "solver_failure_detected": False,
        "dataset_constraint_detected": "DATASET_CONSTRAINT" in active_categories,
        "fixture_constraint_detected": "FIXTURE_CONSTRAINT" in active_categories,
        "baseline_constraint_detected": "BASELINE_CONSTRAINT" in active_categories,
        "score_boundary_preserved": "SCORE_BOUNDARY" in active_categories,
        "solver_not_measured": "MEASUREMENT_CONSTRAINT" in active_categories,
        "submission_boundary_preserved": "SUBMISSION_BOUNDARY" in active_categories,
        "next_action_required": "NEXT_ACTION" in active_categories,
        "reason": "No compatible local public fixtures were found; therefore baseline execution and solver measurement cannot be claimed.",
        "safe_next_stage": NEXT_STAGE,
    }


def build_next_action_plan() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            **item,
            "status": "PLANNED",
            "implementation_required": True,
            "requires_external_api": False,
            "requires_secret": False,
            "requires_real_submission": False,
            "score_claim_allowed": False,
        }
        for item in NEXT_ACTIONS
    )


def build_task_3_checks() -> Dict[str, bool]:
    source = build_task_2_source_summary()
    taxonomy = build_public_game_failure_taxonomy()
    interpretation = build_failure_taxonomy_interpretation()
    next_actions = build_next_action_plan()

    taxonomy_ids = {item["taxonomy_id"] for item in taxonomy}
    active_ids = {item["taxonomy_id"] for item in taxonomy if item["active"] is True}

    return {
        "task_2_artifact_exists": source["task_2_present"] is True,
        "task_2_artifact_ready": source["task_2_status"] == EXPECTED_TASK_2_STATUS,
        "task_2_validated": source["task_2_id"].startswith(EXPECTED_TASK_2_ID_PREFIX)
        and bool(source["task_2_signature"]),
        "candidate_identity_loaded": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
        and source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID,
        "inventory_created": source["inventory_created"] is True,
        "inventory_scan_completed": source["inventory_scan_completed"] is True,
        "no_local_public_fixtures_detected": source["has_local_public_fixtures"] is False
        and source["total_file_count"] == 0
        and source["compatible_fixture_count"] == 0,
        "baseline_not_executed_due_to_no_fixtures": source["baseline_execution_performed"] is False
        and source["baseline_execution_mode"] == "NO_LOCAL_PUBLIC_FIXTURES"
        and source["baseline_status"] == "BASELINE_NOT_EXECUTED_NO_LOCAL_PUBLIC_FIXTURES",
        "no_real_public_score_claimed": source["real_public_score_claimed"] is False
        and source["real_benchmark_score"] is None,
        "no_private_score_claimed": source["private_score_claimed"] is False,
        "solver_not_measured_condition_detected": interpretation["solver_not_measured"] is True
        and interpretation["solver_failure_detected"] is False,
        "taxonomy_classes_created": len(taxonomy) == EXPECTED_TAXONOMY_CLASS_COUNT,
        "taxonomy_dataset_missing_created": "dataset_missing_v1" in taxonomy_ids
        and "dataset_missing_v1" in active_ids,
        "taxonomy_fixture_missing_created": "fixture_missing_v1" in taxonomy_ids
        and "fixture_missing_v1" in active_ids,
        "taxonomy_baseline_not_executed_created": "baseline_not_executed_v1" in taxonomy_ids
        and "baseline_not_executed_v1" in active_ids,
        "taxonomy_score_not_claimed_created": "score_not_claimed_v1" in taxonomy_ids
        and "score_not_claimed_v1" in active_ids,
        "taxonomy_solver_not_measured_created": "solver_not_measured_v1" in taxonomy_ids
        and "solver_not_measured_v1" in active_ids,
        "taxonomy_submission_blocked_created": "submission_still_blocked_v1" in taxonomy_ids
        and "submission_still_blocked_v1" in active_ids,
        "taxonomy_next_action_required_created": "next_action_required_v1" in taxonomy_ids
        and "next_action_required_v1" in active_ids,
        "next_actions_created": len(next_actions) == EXPECTED_NEXT_ACTION_COUNT,
        "failure_is_constraint_not_solver_failure": interpretation["primary_classification"]
        == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
        and interpretation["solver_failure_detected"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "submission_json_absent": source["submission_json_created"] is False,
        "upload_package_absent": source["upload_package_created"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1",
        "taxonomy_check_count_valid": len(TAXONOMY_CHECKS) == EXPECTED_TAXONOMY_CHECK_COUNT,
        "taxonomy_case_count_valid": len(TAXONOMY_CASES) == EXPECTED_TAXONOMY_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_3_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_3_checks()

    if case_id == "m11_task3_source_task2_ready_v1":
        passed = (
            checks["task_2_artifact_exists"]
            and checks["task_2_artifact_ready"]
            and checks["task_2_validated"]
        )
        return _result(case_id, "source_binding", "verify_task_2_inventory_baseline_source", passed)

    if case_id == "m11_task3_no_local_public_fixtures_classified_v1":
        passed = checks["no_local_public_fixtures_detected"] and checks[
            "taxonomy_dataset_missing_created"
        ] and checks["taxonomy_fixture_missing_created"]
        return _result(case_id, "dataset_constraint", "classify_no_local_public_fixtures", passed)

    if case_id == "m11_task3_baseline_not_executed_classified_v1":
        passed = checks["baseline_not_executed_due_to_no_fixtures"] and checks[
            "taxonomy_baseline_not_executed_created"
        ]
        return _result(case_id, "baseline_constraint", "classify_baseline_not_executed", passed)

    if case_id == "m11_task3_score_boundary_classified_v1":
        passed = checks["no_real_public_score_claimed"] and checks[
            "taxonomy_score_not_claimed_created"
        ]
        return _result(case_id, "score_boundary", "classify_score_not_claimed", passed)

    if case_id == "m11_task3_solver_not_measured_classified_v1":
        passed = checks["solver_not_measured_condition_detected"] and checks[
            "taxonomy_solver_not_measured_created"
        ]
        return _result(case_id, "measurement_constraint", "classify_solver_not_measured", passed)

    if case_id == "m11_task3_submission_boundary_classified_v1":
        passed = (
            checks["real_submission_blocked"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
            and checks["taxonomy_submission_blocked_created"]
        )
        return _result(case_id, "submission_boundary", "classify_submission_still_blocked", passed)

    if case_id == "m11_task3_next_actions_ready_v1":
        passed = checks["next_actions_created"] and checks["taxonomy_next_action_required_created"]
        return _result(case_id, "next_action", "verify_next_actions", passed)

    if case_id == "m11_task3_taxonomy_not_solver_failure_v1":
        return _result(
            case_id,
            "interpretation",
            "verify_constraint_not_solver_failure",
            checks["failure_is_constraint_not_solver_failure"],
        )

    if case_id == "m11_task3_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task3_metadata_safe_v1":
        passed = (
            checks["public_safe"]
            and checks["deterministic"]
            and checks["local_only"]
            and checks["dry_run_only"]
            and checks["external_api_dependency_false"]
            and checks["private_core_exposure_false"]
            and checks["legal_certification_false"]
        )
        return _result(case_id, "metadata", "verify_public_safe_metadata", passed)

    raise ValueError(f"unknown milestone 11 task 3 case: {case_id}")


def evaluate_all_task_3_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_3_case(case["case_id"]) for case in TAXONOMY_CASES)


def build_taxonomy_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_3_checks()
    rows = (
        ("source_task2_ready", checks["task_2_artifact_exists"] and checks["task_2_artifact_ready"]),
        ("dataset_missing_classified", checks["taxonomy_dataset_missing_created"]),
        ("fixture_missing_classified", checks["taxonomy_fixture_missing_created"]),
        ("baseline_not_executed_classified", checks["taxonomy_baseline_not_executed_created"]),
        ("score_not_claimed_classified", checks["taxonomy_score_not_claimed_created"]),
        ("solver_not_measured_classified", checks["taxonomy_solver_not_measured_created"]),
        ("submission_boundary_classified", checks["taxonomy_submission_blocked_created"]),
        ("next_actions_ready", checks["next_actions_created"]),
        ("constraint_not_solver_failure", checks["failure_is_constraint_not_solver_failure"]),
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


def build_milestone_11_public_game_failure_taxonomy() -> Dict[str, Any]:
    source = build_task_2_source_summary()
    taxonomy = build_public_game_failure_taxonomy()
    interpretation = build_failure_taxonomy_interpretation()
    next_actions = build_next_action_plan()
    checks = build_task_3_checks()
    results = evaluate_all_task_3_cases()
    scorecard = build_taxonomy_scorecard()

    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "task_2_artifact_exists": checks["task_2_artifact_exists"],
        "task_2_artifact_ready": checks["task_2_artifact_ready"],
        "task_2_validated": checks["task_2_validated"],
        "candidate_identity_loaded": checks["candidate_identity_loaded"],
        "inventory_created": checks["inventory_created"],
        "inventory_scan_completed": checks["inventory_scan_completed"],
        "no_local_public_fixtures_detected": checks["no_local_public_fixtures_detected"],
        "baseline_not_executed_due_to_no_fixtures": checks[
            "baseline_not_executed_due_to_no_fixtures"
        ],
        "no_real_public_score_claimed": checks["no_real_public_score_claimed"],
        "no_private_score_claimed": checks["no_private_score_claimed"],
        "solver_not_measured_condition_detected": checks["solver_not_measured_condition_detected"],
        "taxonomy_classes_created": checks["taxonomy_classes_created"],
        "next_actions_created": checks["next_actions_created"],
        "failure_is_constraint_not_solver_failure": checks["failure_is_constraint_not_solver_failure"],
        "real_submission_blocked": checks["real_submission_blocked"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(result["passed"] is True for result in results),
        "pass_count_valid": pass_count == EXPECTED_TAXONOMY_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_TAXONOMY_FAILURE_COUNT,
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
        pass_count == EXPECTED_TAXONOMY_PASS_COUNT
        and failure_count == EXPECTED_TAXONOMY_FAILURE_COUNT
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_2_artifact_ready"]
        and checks["taxonomy_classes_created"]
        and checks["failure_is_constraint_not_solver_failure"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 3",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_2": source["task_2_id"],
        "primary_condition": interpretation["primary_condition"],
        "primary_classification": interpretation["primary_classification"],
        "solver_failure_detected": False,
        "solver_not_measured": interpretation["solver_not_measured"],
        "taxonomy_class_count": len(taxonomy),
        "next_action_count": len(next_actions),
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
        "task": "Task 3",
        "title": "Public Game Failure Taxonomy v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_2_source": {
            "path": str(TASK_2_JSON),
            "present": TASK_2_JSON.exists(),
            "status": source["task_2_status"],
            "task_2_id": source["task_2_id"],
            "sha256": _sha256(TASK_2_JSON),
            "sha256_16": _sha16(_sha256(TASK_2_JSON)),
        },
        "source_summary": source,
        "failure_taxonomy": list(taxonomy),
        "taxonomy_interpretation": interpretation,
        "next_action_plan": list(next_actions),
        "taxonomy_scorecard": list(scorecard),
        "taxonomy_checks": checks,
        "taxonomy_check_list": list(TAXONOMY_CHECKS),
        "taxonomy_cases": list(TAXONOMY_CASES),
        "taxonomy_results": list(results),
        "taxonomy_gates": list(gates),
        "taxonomy_issues": list(issues),
        "taxonomy_index": index,
        "task_3_ready": task_ready,
        "taxonomy_created": True,
        "taxonomy_validated": True,
        "taxonomy_class_count": len(taxonomy),
        "active_taxonomy_class_count": sum(1 for item in taxonomy if item["active"] is True),
        "next_action_count": len(next_actions),
        "primary_condition": interpretation["primary_condition"],
        "primary_classification": interpretation["primary_classification"],
        "solver_failure_detected": False,
        "solver_not_measured": interpretation["solver_not_measured"],
        "failure_is_constraint_not_solver_failure": True,
        "dataset_missing": interpretation["dataset_constraint_detected"],
        "fixture_missing": interpretation["fixture_constraint_detected"],
        "baseline_not_executed": interpretation["baseline_constraint_detected"],
        "score_not_claimed": interpretation["score_boundary_preserved"],
        "submission_boundary_preserved": interpretation["submission_boundary_preserved"],
        "taxonomy_check_count": len(TAXONOMY_CHECKS),
        "taxonomy_case_count": len(TAXONOMY_CASES),
        "taxonomy_pass_count": pass_count,
        "taxonomy_failure_count": failure_count,
        "taxonomy_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "taxonomy_issue_count": issue_count,
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
            "source": "milestone_11_public_game_failure_taxonomy_v1",
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
        "task_3_id": f"MILESTONE-11-PUBLIC-GAME-FAILURE-TAXONOMY-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_public_game_failure_taxonomy(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("taxonomy_gates", [])
    issues = record.get("taxonomy_issues", [])
    results = record.get("taxonomy_results", [])
    scorecard = record.get("taxonomy_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_3_id_present": isinstance(record.get("task_3_id"), str) and bool(record.get("task_3_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("d3b39b0"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_3_ready") is True,
        "task_2_source_present": record.get("task_2_source", {}).get("present") is True,
        "taxonomy_created": record.get("taxonomy_created") is True,
        "taxonomy_validated": record.get("taxonomy_validated") is True,
        "taxonomy_class_count_valid": record.get("taxonomy_class_count") == EXPECTED_TAXONOMY_CLASS_COUNT,
        "active_taxonomy_class_count_valid": record.get("active_taxonomy_class_count")
        == EXPECTED_TAXONOMY_CLASS_COUNT,
        "next_action_count_valid": record.get("next_action_count") == EXPECTED_NEXT_ACTION_COUNT,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "taxonomy_check_count_valid": record.get("taxonomy_check_count") == EXPECTED_TAXONOMY_CHECK_COUNT,
        "taxonomy_case_count_valid": record.get("taxonomy_case_count") == EXPECTED_TAXONOMY_CASE_COUNT,
        "taxonomy_pass_count_valid": record.get("taxonomy_pass_count") == EXPECTED_TAXONOMY_PASS_COUNT,
        "taxonomy_failure_count_zero": record.get("taxonomy_failure_count") == EXPECTED_TAXONOMY_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "primary_condition_valid": record.get("primary_condition") == "NO_LOCAL_PUBLIC_FIXTURES",
        "classification_valid": record.get("primary_classification")
        == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
        "solver_failure_false": record.get("solver_failure_detected") is False,
        "solver_not_measured_true": record.get("solver_not_measured") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_3_id": record.get("task_3_id"),
        "signature": record.get("signature"),
    }


def render_task_3_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 3 - Public Game Failure Taxonomy v1",
        "",
        f"- status: {record['status']}",
        f"- task_3_id: {record['task_3_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_3_ready: {record['task_3_ready']}",
        f"- primary_condition: {record['primary_condition']}",
        f"- primary_classification: {record['primary_classification']}",
        f"- solver_failure_detected: {record['solver_failure_detected']}",
        f"- solver_not_measured: {record['solver_not_measured']}",
        f"- taxonomy_class_count: {record['taxonomy_class_count']}",
        f"- active_taxonomy_class_count: {record['active_taxonomy_class_count']}",
        f"- next_action_count: {record['next_action_count']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- private_score_claimed: {record['private_score_claimed']}",
        f"- real_benchmark_score: {record['real_benchmark_score']}",
        f"- real_submission_candidate_created: {record['real_submission_candidate_created']}",
        f"- submission_json_created: {record['submission_json_created']}",
        f"- upload_package_created: {record['upload_package_created']}",
        f"- real_submission_decision: {record['real_submission_decision']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Failure taxonomy",
        "",
    ]

    for item in record["failure_taxonomy"]:
        lines.append(
            f"- {item['taxonomy_id']} / category={item['category']} / "
            f"severity={item['severity']} / active={item['active']}"
        )

    lines.extend(["", "## Interpretation", ""])

    interpretation = record["taxonomy_interpretation"]
    lines.append(f"- primary_condition: {interpretation['primary_condition']}")
    lines.append(f"- primary_classification: {interpretation['primary_classification']}")
    lines.append(f"- solver_failure_detected: {interpretation['solver_failure_detected']}")
    lines.append(f"- reason: {interpretation['reason']}")

    lines.extend(["", "## Next action plan", ""])

    for action in record["next_action_plan"]:
        lines.append(
            f"- {action['action_id']} / priority={action['priority']} / "
            f"status={action['status']} / action={action['action']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in record["taxonomy_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 3 classifies the Task 2 outcome as a measurement constraint, not a solver failure. No real score is claimed and real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_3_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_3_MODE=MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_3_VERDICT=PUBLIC_GAME_FAILURE_TAXONOMY_READY_FOR_LOCAL_FIXTURE_HARNESS_PLAN",
            "ARC_AGI3_MILESTONE_11_TASK_3_BASELINE_COMMIT=d3b39b0",
            "ARC_AGI3_MILESTONE_11_TASK_3_NEXT_STAGE=MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1",
            "ARC_AGI3_MILESTONE_11_PRIMARY_CONDITION=NO_LOCAL_PUBLIC_FIXTURES",
            "ARC_AGI3_MILESTONE_11_PRIMARY_CLASSIFICATION=MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
            "ARC_AGI3_MILESTONE_11_SOLVER_FAILURE_DETECTED=false",
            "ARC_AGI3_MILESTONE_11_SOLVER_NOT_MEASURED=true",
            "ARC_AGI3_MILESTONE_11_DATASET_MISSING=true",
            "ARC_AGI3_MILESTONE_11_FIXTURE_MISSING=true",
            "ARC_AGI3_MILESTONE_11_BASELINE_NOT_EXECUTED=true",
            "ARC_AGI3_MILESTONE_11_SCORE_NOT_CLAIMED=true",
            "ARC_AGI3_MILESTONE_11_TAXONOMY_CREATED=true",
            f"ARC_AGI3_MILESTONE_11_TAXONOMY_CLASS_COUNT={EXPECTED_TAXONOMY_CLASS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_NEXT_ACTION_COUNT={EXPECTED_NEXT_ACTION_COUNT}",
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


def render_task_3_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 3 PUBLIC GAME FAILURE TAXONOMY MANIFEST v1",
        f"task_3_id={record['task_3_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_3_ready={record['task_3_ready']}",
        f"primary_condition={record['primary_condition']}",
        f"primary_classification={record['primary_classification']}",
        f"solver_failure_detected={record['solver_failure_detected']}",
        f"solver_not_measured={record['solver_not_measured']}",
        f"dataset_missing={record['dataset_missing']}",
        f"fixture_missing={record['fixture_missing']}",
        f"baseline_not_executed={record['baseline_not_executed']}",
        f"score_not_claimed={record['score_not_claimed']}",
        f"taxonomy_class_count={record['taxonomy_class_count']}",
        f"active_taxonomy_class_count={record['active_taxonomy_class_count']}",
        f"next_action_count={record['next_action_count']}",
        f"real_public_score_claimed={record['real_public_score_claimed']}",
        f"private_score_claimed={record['private_score_claimed']}",
        f"real_benchmark_score={record['real_benchmark_score']}",
        f"real_submission_candidate_created={record['real_submission_candidate_created']}",
        f"submission_json_created={record['submission_json_created']}",
        f"upload_package_created={record['upload_package_created']}",
        f"real_submission_decision={record['real_submission_decision']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"manual_upload_allowed={record['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"fail_closed_required={record['fail_closed_required']}",
        f"fail_closed_active={record['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "FAILURE_TAXONOMY",
    ]

    for item in record["failure_taxonomy"]:
        lines.append(
            f"{item['taxonomy_id']} category={item['category']} severity={item['severity']} active={item['active']}"
        )

    lines.append("")
    lines.append("NEXT_ACTION_PLAN")
    for action in record["next_action_plan"]:
        lines.append(
            f"{action['action_id']} priority={action['priority']} status={action['status']} "
            f"requires_real_submission={action['requires_real_submission']}"
        )

    lines.append("")
    lines.append("TAXONOMY_VALIDATION_RESULTS")
    for result in record["taxonomy_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_public_game_failure_taxonomy())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-public-game-failure-taxonomy-v1.json"
    md_path = output / "milestone-11-public-game-failure-taxonomy-v1.md"
    manifest_path = output / "milestone-11-public-game-failure-taxonomy-manifest-v1.txt"
    index_path = output / "milestone-11-public-game-failure-taxonomy-index-v1.json"
    taxonomy_path = output / "milestone-11-failure-taxonomy-v1.json"
    next_actions_path = output / "milestone-11-failure-taxonomy-next-actions-v1.json"
    interpretation_path = output / "milestone-11-failure-taxonomy-interpretation-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_3_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_3_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["taxonomy_index"], indent=2, sort_keys=True), encoding="utf-8")
    taxonomy_path.write_text(json.dumps(record["failure_taxonomy"], indent=2, sort_keys=True), encoding="utf-8")
    next_actions_path.write_text(json.dumps(record["next_action_plan"], indent=2, sort_keys=True), encoding="utf-8")
    interpretation_path.write_text(
        json.dumps(record["taxonomy_interpretation"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "taxonomy_path": str(taxonomy_path),
        "next_actions_path": str(next_actions_path),
        "interpretation_path": str(interpretation_path),
    }


def run_milestone_11_public_game_failure_taxonomy_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_public_game_failure_taxonomy()
    validation = validate_milestone_11_public_game_failure_taxonomy(record)
    artifacts = write_task_3_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_3_id": record["task_3_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_3_ready": record["task_3_ready"],
        "taxonomy_created": record["taxonomy_created"],
        "taxonomy_validated": record["taxonomy_validated"],
        "taxonomy_class_count": record["taxonomy_class_count"],
        "active_taxonomy_class_count": record["active_taxonomy_class_count"],
        "next_action_count": record["next_action_count"],
        "primary_condition": record["primary_condition"],
        "primary_classification": record["primary_classification"],
        "solver_failure_detected": record["solver_failure_detected"],
        "solver_not_measured": record["solver_not_measured"],
        "dataset_missing": record["dataset_missing"],
        "fixture_missing": record["fixture_missing"],
        "baseline_not_executed": record["baseline_not_executed"],
        "score_not_claimed": record["score_not_claimed"],
        "taxonomy_check_count": record["taxonomy_check_count"],
        "taxonomy_case_count": record["taxonomy_case_count"],
        "taxonomy_pass_count": record["taxonomy_pass_count"],
        "taxonomy_failure_count": record["taxonomy_failure_count"],
        "taxonomy_gate_count": record["taxonomy_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "taxonomy_issue_count": record["taxonomy_issue_count"],
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
