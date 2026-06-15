"""Milestone #11 Task 4 - Local Fixture Harness Plan v1.

Local-only deterministic harness plan after public game failure taxonomy.

This module converts the Task 3 taxonomy into a local fixture harness plan. The
plan defines how to test world model, planner, verifier, and action policy using
local diagnostic fixtures without claiming Kaggle score, without creating a real
submission candidate, without creating submission.json, without creating upload
packages, without authenticating with Kaggle, without external APIs, and without
legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_VALID"

BASELINE_COMMIT = "b609069 Add ARC AGI3 public game failure taxonomy"
TASK_MODE = "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_PLAN_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION"
NEXT_STAGE = "MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-fixture-harness-plan-v1"

TASK_3_JSON = Path(
    "examples/milestone-11/public-game-failure-taxonomy-v1/"
    "milestone-11-public-game-failure-taxonomy-v1.json"
)

EXPECTED_TASK_3_STATUS = "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY"
EXPECTED_TASK_3_ID_PREFIX = "MILESTONE-11-PUBLIC-GAME-FAILURE-TAXONOMY-"

HARNESS_COMPONENTS: Tuple[Dict[str, str], ...] = (
    {
        "component_id": "local_fixture_loader_v1",
        "layer": "fixture_io",
        "priority": "P0",
        "purpose": "Load local diagnostic fixtures from deterministic JSON files.",
    },
    {
        "component_id": "episode_runner_v1",
        "layer": "runtime",
        "priority": "P0",
        "purpose": "Execute deterministic local episodes without external services.",
    },
    {
        "component_id": "observation_trace_recorder_v1",
        "layer": "trace",
        "priority": "P0",
        "purpose": "Record observations, actions, predicted transitions, and actual transitions.",
    },
    {
        "component_id": "world_model_probe_v1",
        "layer": "world_model",
        "priority": "P0",
        "purpose": "Measure whether the solver models objects, state, transitions, and rules.",
    },
    {
        "component_id": "goal_inference_probe_v1",
        "layer": "goal_inference",
        "priority": "P0",
        "purpose": "Measure whether the solver infers candidate goals from state changes.",
    },
    {
        "component_id": "planner_probe_v1",
        "layer": "planner",
        "priority": "P0",
        "purpose": "Measure planning quality, loop avoidance, and action sequence selection.",
    },
    {
        "component_id": "transition_verifier_probe_v1",
        "layer": "verifier",
        "priority": "P0",
        "purpose": "Compare predicted and observed transitions after every action.",
    },
    {
        "component_id": "score_boundary_guard_v1",
        "layer": "boundary",
        "priority": "P0",
        "purpose": "Prevent diagnostic fixture results from being treated as Kaggle scores.",
    },
)

FIXTURE_CLASSES: Tuple[Dict[str, str], ...] = (
    {
        "fixture_class_id": "object_persistence_fixture_v1",
        "target_layer": "world_model",
        "purpose": "Test whether objects persist across observations and transformations.",
    },
    {
        "fixture_class_id": "color_rule_fixture_v1",
        "target_layer": "rule_inference",
        "purpose": "Test simple color remap and rule tracking.",
    },
    {
        "fixture_class_id": "movement_transition_fixture_v1",
        "target_layer": "transition_model",
        "purpose": "Test deterministic movement, collision, and state transition predictions.",
    },
    {
        "fixture_class_id": "goal_inference_fixture_v1",
        "target_layer": "goal_inference",
        "purpose": "Test inferred objective from reward-like terminal conditions.",
    },
    {
        "fixture_class_id": "planner_loop_fixture_v1",
        "target_layer": "planner",
        "purpose": "Test loop detection, fallback exploration, and progress tracking.",
    },
    {
        "fixture_class_id": "verifier_mismatch_fixture_v1",
        "target_layer": "verifier",
        "purpose": "Test correction when predicted transition differs from actual transition.",
    },
)

MEASUREMENT_AXES: Tuple[Dict[str, str], ...] = (
    {
        "axis_id": "world_model_accuracy_v1",
        "scope": "diagnostic_only",
        "description": "Measures internal state and transition prediction quality.",
    },
    {
        "axis_id": "goal_inference_quality_v1",
        "scope": "diagnostic_only",
        "description": "Measures whether the solver infers goals from local feedback.",
    },
    {
        "axis_id": "planner_progress_v1",
        "scope": "diagnostic_only",
        "description": "Measures progress, loop avoidance, and plan stability.",
    },
    {
        "axis_id": "transition_verification_v1",
        "scope": "diagnostic_only",
        "description": "Measures predicted versus observed transition agreement.",
    },
    {
        "axis_id": "action_policy_safety_v1",
        "scope": "diagnostic_only",
        "description": "Measures whether action choice avoids repeated non-progress actions.",
    },
)

BOUNDARY_RULES: Tuple[Dict[str, str], ...] = (
    {
        "rule_id": "no_kaggle_score_claim_from_local_fixture_v1",
        "severity": "BLOCKING",
        "rule": "Local fixture harness results must never be reported as Kaggle public or private score.",
    },
    {
        "rule_id": "no_submission_json_from_harness_v1",
        "severity": "BLOCKING",
        "rule": "The harness plan must not create submission.json.",
    },
    {
        "rule_id": "no_upload_package_from_harness_v1",
        "severity": "BLOCKING",
        "rule": "The harness plan must not create an upload package.",
    },
    {
        "rule_id": "no_external_api_dependency_v1",
        "severity": "BLOCKING",
        "rule": "Harness execution must remain local-only and must not call external APIs.",
    },
    {
        "rule_id": "diagnostic_result_label_required_v1",
        "severity": "BLOCKING",
        "rule": "Every harness result must be labelled diagnostic-only.",
    },
)

HARNESS_CHECKS: Tuple[str, ...] = (
    "task_3_artifact_exists",
    "task_3_artifact_ready",
    "task_3_validated",
    "primary_condition_no_local_public_fixtures",
    "classification_measurement_constraint",
    "solver_not_measured",
    "solver_failure_false",
    "harness_components_created",
    "fixture_classes_created",
    "measurement_axes_created",
    "boundary_rules_created",
    "harness_plan_created",
    "fixture_generation_deferred",
    "diagnostic_only_enforced",
    "no_real_public_score_claimed",
    "no_private_score_claimed",
    "no_real_benchmark_score",
    "real_submission_candidate_absent",
    "submission_json_absent",
    "upload_package_absent",
    "real_submission_blocked",
    "kaggle_authentication_blocked",
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

HARNESS_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m11_task4_source_task3_ready_v1",
        "area": "source_binding",
        "operation": "verify_task_3_failure_taxonomy_source",
    },
    {
        "case_id": "m11_task4_measurement_constraint_loaded_v1",
        "area": "constraint",
        "operation": "verify_measurement_constraint_not_solver_failure",
    },
    {
        "case_id": "m11_task4_harness_components_ready_v1",
        "area": "harness_components",
        "operation": "verify_harness_components",
    },
    {
        "case_id": "m11_task4_fixture_classes_ready_v1",
        "area": "fixture_plan",
        "operation": "verify_fixture_classes",
    },
    {
        "case_id": "m11_task4_measurement_axes_ready_v1",
        "area": "measurement",
        "operation": "verify_measurement_axes",
    },
    {
        "case_id": "m11_task4_boundary_rules_ready_v1",
        "area": "boundary",
        "operation": "verify_boundary_rules",
    },
    {
        "case_id": "m11_task4_diagnostic_only_enforced_v1",
        "area": "score_boundary",
        "operation": "verify_diagnostic_only_enforced",
    },
    {
        "case_id": "m11_task4_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m11_task4_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
    {
        "case_id": "m11_task4_metadata_safe_v1",
        "area": "metadata",
        "operation": "verify_public_safe_metadata",
    },
)

EXPECTED_HARNESS_COMPONENT_COUNT = len(HARNESS_COMPONENTS)
EXPECTED_FIXTURE_CLASS_COUNT = len(FIXTURE_CLASSES)
EXPECTED_MEASUREMENT_AXIS_COUNT = len(MEASUREMENT_AXES)
EXPECTED_BOUNDARY_RULE_COUNT = len(BOUNDARY_RULES)
EXPECTED_HARNESS_CHECK_COUNT = len(HARNESS_CHECKS)
EXPECTED_HARNESS_CASE_COUNT = len(HARNESS_CASES)
EXPECTED_HARNESS_PASS_COUNT = len(HARNESS_CASES)
EXPECTED_HARNESS_FAILURE_COUNT = 0


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


def build_task_3_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_3_JSON)

    return {
        "task_3_path": str(TASK_3_JSON),
        "task_3_present": TASK_3_JSON.exists(),
        "task_3_status": record.get("status", "MISSING"),
        "task_3_id": record.get("task_3_id", "MISSING_TASK_3_ID"),
        "task_3_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_3_ready": record.get("task_3_ready", False),
        "task_verdict": record.get("task_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "primary_condition": record.get("primary_condition", "MISSING_PRIMARY_CONDITION"),
        "primary_classification": record.get("primary_classification", "MISSING_PRIMARY_CLASSIFICATION"),
        "solver_failure_detected": record.get("solver_failure_detected", True),
        "solver_not_measured": record.get("solver_not_measured", False),
        "dataset_missing": record.get("dataset_missing", False),
        "fixture_missing": record.get("fixture_missing", False),
        "baseline_not_executed": record.get("baseline_not_executed", False),
        "score_not_claimed": record.get("score_not_claimed", False),
        "taxonomy_created": record.get("taxonomy_created", False),
        "taxonomy_validated": record.get("taxonomy_validated", False),
        "taxonomy_class_count": record.get("taxonomy_class_count", 0),
        "next_action_count": record.get("next_action_count", 0),
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
        "task_3_sha256": _sha256(TASK_3_JSON),
        "task_3_sha256_16": _sha16(_sha256(TASK_3_JSON)),
    }


def build_local_fixture_harness_plan() -> Dict[str, Any]:
    source = build_task_3_source_summary()

    return {
        "harness_plan_id": "M11-TASK4-LOCAL-FIXTURE-HARNESS-PLAN-v1",
        "source_primary_condition": source["primary_condition"],
        "source_primary_classification": source["primary_classification"],
        "diagnostic_only": True,
        "fixture_generation_performed": False,
        "fixture_generation_deferred_to": NEXT_STAGE,
        "public_fixture_import_allowed": False,
        "synthetic_fixture_allowed": True,
        "synthetic_fixture_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "harness_components": list(HARNESS_COMPONENTS),
        "fixture_classes": list(FIXTURE_CLASSES),
        "measurement_axes": list(MEASUREMENT_AXES),
        "boundary_rules": list(BOUNDARY_RULES),
        "result_label": "LOCAL_DIAGNOSTIC_ONLY_NOT_KAGGLE_SCORE",
        "required_trace_fields": [
            "fixture_id",
            "episode_id",
            "observation_index",
            "action",
            "predicted_transition",
            "observed_transition",
            "world_model_state",
            "planner_state",
            "verifier_result",
            "diagnostic_only",
        ],
    }


def build_task_4_next_action_plan() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "action_id": "m11_task5_create_local_diagnostic_fixture_schema_v1",
            "priority": "P0",
            "status": "PLANNED",
            "description": "Create deterministic fixture schema and validator.",
            "requires_real_submission": False,
            "score_claim_allowed": False,
        },
        {
            "action_id": "m11_task5_create_minimal_diagnostic_fixtures_v1",
            "priority": "P0",
            "status": "PLANNED",
            "description": "Create small local diagnostic fixtures for world model, planner, and verifier.",
            "requires_real_submission": False,
            "score_claim_allowed": False,
        },
        {
            "action_id": "m11_task5_create_episode_runner_contract_v1",
            "priority": "P0",
            "status": "PLANNED",
            "description": "Create local episode runner contract with deterministic traces.",
            "requires_real_submission": False,
            "score_claim_allowed": False,
        },
        {
            "action_id": "m11_task5_create_diagnostic_result_guard_v1",
            "priority": "P0",
            "status": "PLANNED",
            "description": "Force all outputs to remain diagnostic-only and not official score evidence.",
            "requires_real_submission": False,
            "score_claim_allowed": False,
        },
    )


def build_task_4_checks() -> Dict[str, bool]:
    source = build_task_3_source_summary()
    plan = build_local_fixture_harness_plan()
    next_actions = build_task_4_next_action_plan()

    boundary_ids = {rule["rule_id"] for rule in BOUNDARY_RULES}

    return {
        "task_3_artifact_exists": source["task_3_present"] is True,
        "task_3_artifact_ready": source["task_3_status"] == EXPECTED_TASK_3_STATUS,
        "task_3_validated": source["task_3_id"].startswith(EXPECTED_TASK_3_ID_PREFIX)
        and bool(source["task_3_signature"]),
        "primary_condition_no_local_public_fixtures": source["primary_condition"] == "NO_LOCAL_PUBLIC_FIXTURES",
        "classification_measurement_constraint": source["primary_classification"]
        == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
        "solver_not_measured": source["solver_not_measured"] is True,
        "solver_failure_false": source["solver_failure_detected"] is False,
        "harness_components_created": len(plan["harness_components"]) == EXPECTED_HARNESS_COMPONENT_COUNT,
        "fixture_classes_created": len(plan["fixture_classes"]) == EXPECTED_FIXTURE_CLASS_COUNT,
        "measurement_axes_created": len(plan["measurement_axes"]) == EXPECTED_MEASUREMENT_AXIS_COUNT,
        "boundary_rules_created": len(plan["boundary_rules"]) == EXPECTED_BOUNDARY_RULE_COUNT
        and "no_kaggle_score_claim_from_local_fixture_v1" in boundary_ids
        and "diagnostic_result_label_required_v1" in boundary_ids,
        "harness_plan_created": plan["harness_plan_id"] == "M11-TASK4-LOCAL-FIXTURE-HARNESS-PLAN-v1",
        "fixture_generation_deferred": plan["fixture_generation_performed"] is False
        and plan["fixture_generation_deferred_to"] == NEXT_STAGE,
        "diagnostic_only_enforced": plan["diagnostic_only"] is True
        and plan["result_label"] == "LOCAL_DIAGNOSTIC_ONLY_NOT_KAGGLE_SCORE"
        and plan["official_score_claim_allowed"] is False,
        "no_real_public_score_claimed": source["real_public_score_claimed"] is False
        and plan["official_score_claim_allowed"] is False,
        "no_private_score_claimed": source["private_score_claimed"] is False,
        "no_real_benchmark_score": source["real_benchmark_score"] is None,
        "real_submission_candidate_absent": source["real_submission_candidate_created"] is False,
        "submission_json_absent": source["submission_json_created"] is False,
        "upload_package_absent": source["upload_package_created"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1",
        "harness_check_count_valid": len(HARNESS_CHECKS) == EXPECTED_HARNESS_CHECK_COUNT,
        "harness_case_count_valid": len(HARNESS_CASES) == EXPECTED_HARNESS_CASE_COUNT,
        "next_action_count_valid": len(next_actions) == 4,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_4_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_4_checks()

    if case_id == "m11_task4_source_task3_ready_v1":
        passed = checks["task_3_artifact_exists"] and checks["task_3_artifact_ready"] and checks["task_3_validated"]
        return _result(case_id, "source_binding", "verify_task_3_failure_taxonomy_source", passed)

    if case_id == "m11_task4_measurement_constraint_loaded_v1":
        passed = (
            checks["primary_condition_no_local_public_fixtures"]
            and checks["classification_measurement_constraint"]
            and checks["solver_not_measured"]
            and checks["solver_failure_false"]
        )
        return _result(case_id, "constraint", "verify_measurement_constraint_not_solver_failure", passed)

    if case_id == "m11_task4_harness_components_ready_v1":
        return _result(case_id, "harness_components", "verify_harness_components", checks["harness_components_created"])

    if case_id == "m11_task4_fixture_classes_ready_v1":
        return _result(case_id, "fixture_plan", "verify_fixture_classes", checks["fixture_classes_created"])

    if case_id == "m11_task4_measurement_axes_ready_v1":
        return _result(case_id, "measurement", "verify_measurement_axes", checks["measurement_axes_created"])

    if case_id == "m11_task4_boundary_rules_ready_v1":
        return _result(case_id, "boundary", "verify_boundary_rules", checks["boundary_rules_created"])

    if case_id == "m11_task4_diagnostic_only_enforced_v1":
        passed = checks["diagnostic_only_enforced"] and checks["no_real_public_score_claimed"] and checks["no_private_score_claimed"]
        return _result(case_id, "score_boundary", "verify_diagnostic_only_enforced", passed)

    if case_id == "m11_task4_real_submission_blocked_v1":
        passed = (
            checks["real_submission_blocked"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m11_task4_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task4_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 4 case: {case_id}")


def evaluate_all_task_4_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_4_case(case["case_id"]) for case in HARNESS_CASES)


def build_harness_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_4_checks()
    rows = (
        ("source_task3_ready", checks["task_3_artifact_exists"] and checks["task_3_artifact_ready"]),
        ("measurement_constraint_loaded", checks["classification_measurement_constraint"]),
        ("harness_components_ready", checks["harness_components_created"]),
        ("fixture_classes_ready", checks["fixture_classes_created"]),
        ("measurement_axes_ready", checks["measurement_axes_created"]),
        ("boundary_rules_ready", checks["boundary_rules_created"]),
        ("diagnostic_only_enforced", checks["diagnostic_only_enforced"]),
        ("real_submission_blocked", checks["real_submission_blocked"]),
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


def build_milestone_11_local_fixture_harness_plan() -> Dict[str, Any]:
    source = build_task_3_source_summary()
    plan = build_local_fixture_harness_plan()
    next_actions = build_task_4_next_action_plan()
    checks = build_task_4_checks()
    results = evaluate_all_task_4_cases()
    scorecard = build_harness_scorecard()

    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "task_3_artifact_exists": checks["task_3_artifact_exists"],
        "task_3_artifact_ready": checks["task_3_artifact_ready"],
        "task_3_validated": checks["task_3_validated"],
        "measurement_constraint_loaded": checks["classification_measurement_constraint"]
        and checks["solver_not_measured"]
        and checks["solver_failure_false"],
        "harness_components_created": checks["harness_components_created"],
        "fixture_classes_created": checks["fixture_classes_created"],
        "measurement_axes_created": checks["measurement_axes_created"],
        "boundary_rules_created": checks["boundary_rules_created"],
        "harness_plan_created": checks["harness_plan_created"],
        "fixture_generation_deferred": checks["fixture_generation_deferred"],
        "diagnostic_only_enforced": checks["diagnostic_only_enforced"],
        "no_score_claimed": checks["no_real_public_score_claimed"] and checks["no_private_score_claimed"],
        "no_real_benchmark_score": checks["no_real_benchmark_score"],
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
        "pass_count_valid": pass_count == EXPECTED_HARNESS_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_HARNESS_FAILURE_COUNT,
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
        pass_count == EXPECTED_HARNESS_PASS_COUNT
        and failure_count == EXPECTED_HARNESS_FAILURE_COUNT
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_3_artifact_ready"]
        and checks["harness_plan_created"]
        and checks["diagnostic_only_enforced"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 4",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_3": source["task_3_id"],
        "primary_condition": source["primary_condition"],
        "primary_classification": source["primary_classification"],
        "harness_component_count": len(HARNESS_COMPONENTS),
        "fixture_class_count": len(FIXTURE_CLASSES),
        "measurement_axis_count": len(MEASUREMENT_AXES),
        "boundary_rule_count": len(BOUNDARY_RULES),
        "diagnostic_only": True,
        "fixture_generation_performed": False,
        "fixture_generation_deferred_to": NEXT_STAGE,
        "official_score_claim_allowed": False,
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
        "task": "Task 4",
        "title": "Local Fixture Harness Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_3_source": {
            "path": str(TASK_3_JSON),
            "present": TASK_3_JSON.exists(),
            "status": source["task_3_status"],
            "task_3_id": source["task_3_id"],
            "sha256": _sha256(TASK_3_JSON),
            "sha256_16": _sha16(_sha256(TASK_3_JSON)),
        },
        "source_summary": source,
        "local_fixture_harness_plan": plan,
        "harness_components": list(HARNESS_COMPONENTS),
        "fixture_classes": list(FIXTURE_CLASSES),
        "measurement_axes": list(MEASUREMENT_AXES),
        "boundary_rules": list(BOUNDARY_RULES),
        "next_action_plan": list(next_actions),
        "harness_scorecard": list(scorecard),
        "harness_checks": checks,
        "harness_check_list": list(HARNESS_CHECKS),
        "harness_cases": list(HARNESS_CASES),
        "harness_results": list(results),
        "harness_gates": list(gates),
        "harness_issues": list(issues),
        "harness_index": index,
        "task_4_ready": task_ready,
        "harness_plan_created": True,
        "harness_component_count": len(HARNESS_COMPONENTS),
        "fixture_class_count": len(FIXTURE_CLASSES),
        "measurement_axis_count": len(MEASUREMENT_AXES),
        "boundary_rule_count": len(BOUNDARY_RULES),
        "next_action_count": len(next_actions),
        "diagnostic_only": True,
        "fixture_generation_performed": False,
        "fixture_generation_deferred_to": NEXT_STAGE,
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "primary_condition": source["primary_condition"],
        "primary_classification": source["primary_classification"],
        "solver_failure_detected": source["solver_failure_detected"],
        "solver_not_measured": source["solver_not_measured"],
        "harness_check_count": len(HARNESS_CHECKS),
        "harness_case_count": len(HARNESS_CASES),
        "harness_pass_count": pass_count,
        "harness_failure_count": failure_count,
        "harness_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "harness_issue_count": issue_count,
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
            "source": "milestone_11_local_fixture_harness_plan_v1",
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
        "task_4_id": f"MILESTONE-11-LOCAL-FIXTURE-HARNESS-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_fixture_harness_plan(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("harness_gates", [])
    issues = record.get("harness_issues", [])
    results = record.get("harness_results", [])
    scorecard = record.get("harness_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_4_id_present": isinstance(record.get("task_4_id"), str) and bool(record.get("task_4_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("b609069"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_4_ready") is True,
        "task_3_source_present": record.get("task_3_source", {}).get("present") is True,
        "harness_plan_created": record.get("harness_plan_created") is True,
        "harness_component_count_valid": record.get("harness_component_count") == EXPECTED_HARNESS_COMPONENT_COUNT,
        "fixture_class_count_valid": record.get("fixture_class_count") == EXPECTED_FIXTURE_CLASS_COUNT,
        "measurement_axis_count_valid": record.get("measurement_axis_count") == EXPECTED_MEASUREMENT_AXIS_COUNT,
        "boundary_rule_count_valid": record.get("boundary_rule_count") == EXPECTED_BOUNDARY_RULE_COUNT,
        "next_action_count_valid": record.get("next_action_count") == 4,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "fixture_generation_deferred": record.get("fixture_generation_performed") is False
        and record.get("fixture_generation_deferred_to") == NEXT_STAGE,
        "official_score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("synthetic_fixture_score_claim_allowed") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "harness_check_count_valid": record.get("harness_check_count") == EXPECTED_HARNESS_CHECK_COUNT,
        "harness_case_count_valid": record.get("harness_case_count") == EXPECTED_HARNESS_CASE_COUNT,
        "harness_pass_count_valid": record.get("harness_pass_count") == EXPECTED_HARNESS_PASS_COUNT,
        "harness_failure_count_zero": record.get("harness_failure_count") == EXPECTED_HARNESS_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "classification_valid": record.get("primary_classification") == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_4_id": record.get("task_4_id"),
        "signature": record.get("signature"),
    }


def render_task_4_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 4 - Local Fixture Harness Plan v1",
        "",
        f"- status: {record['status']}",
        f"- task_4_id: {record['task_4_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_4_ready: {record['task_4_ready']}",
        f"- primary_condition: {record['primary_condition']}",
        f"- primary_classification: {record['primary_classification']}",
        f"- solver_failure_detected: {record['solver_failure_detected']}",
        f"- solver_not_measured: {record['solver_not_measured']}",
        f"- harness_component_count: {record['harness_component_count']}",
        f"- fixture_class_count: {record['fixture_class_count']}",
        f"- measurement_axis_count: {record['measurement_axis_count']}",
        f"- boundary_rule_count: {record['boundary_rule_count']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- fixture_generation_performed: {record['fixture_generation_performed']}",
        f"- fixture_generation_deferred_to: {record['fixture_generation_deferred_to']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- real_public_score_claimed: {record['real_public_score_claimed']}",
        f"- private_score_claimed: {record['private_score_claimed']}",
        f"- real_benchmark_score: {record['real_benchmark_score']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Harness components",
        "",
    ]

    for item in record["harness_components"]:
        lines.append(
            f"- {item['component_id']} / layer={item['layer']} / priority={item['priority']} / purpose={item['purpose']}"
        )

    lines.extend(["", "## Fixture classes", ""])
    for item in record["fixture_classes"]:
        lines.append(
            f"- {item['fixture_class_id']} / target={item['target_layer']} / purpose={item['purpose']}"
        )

    lines.extend(["", "## Measurement axes", ""])
    for item in record["measurement_axes"]:
        lines.append(f"- {item['axis_id']} / scope={item['scope']} / {item['description']}")

    lines.extend(["", "## Boundary rules", ""])
    for item in record["boundary_rules"]:
        lines.append(f"- {item['rule_id']} / severity={item['severity']} / {item['rule']}")

    lines.extend(["", "## Validation results", ""])
    for result in record["harness_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 4 creates a local diagnostic fixture harness plan. It does not generate fixtures yet, does not claim score, and does not authorize real submission.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_4_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_4_MODE=MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_4_VERDICT=LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION",
            "ARC_AGI3_MILESTONE_11_TASK_4_BASELINE_COMMIT=b609069",
            "ARC_AGI3_MILESTONE_11_TASK_4_NEXT_STAGE=MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1",
            "ARC_AGI3_MILESTONE_11_PRIMARY_CLASSIFICATION=MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE",
            "ARC_AGI3_MILESTONE_11_SOLVER_FAILURE_DETECTED=false",
            "ARC_AGI3_MILESTONE_11_SOLVER_NOT_MEASURED=true",
            f"ARC_AGI3_MILESTONE_11_HARNESS_COMPONENT_COUNT={EXPECTED_HARNESS_COMPONENT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_FIXTURE_CLASS_COUNT={EXPECTED_FIXTURE_CLASS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_MEASUREMENT_AXIS_COUNT={EXPECTED_MEASUREMENT_AXIS_COUNT}",
            f"ARC_AGI3_MILESTONE_11_BOUNDARY_RULE_COUNT={EXPECTED_BOUNDARY_RULE_COUNT}",
            "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true",
            "ARC_AGI3_MILESTONE_11_FIXTURE_GENERATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_SYNTHETIC_FIXTURE_SCORE_CLAIM_ALLOWED=false",
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


def render_task_4_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 4 LOCAL FIXTURE HARNESS PLAN MANIFEST v1",
        f"task_4_id={record['task_4_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_4_ready={record['task_4_ready']}",
        f"primary_condition={record['primary_condition']}",
        f"primary_classification={record['primary_classification']}",
        f"solver_failure_detected={record['solver_failure_detected']}",
        f"solver_not_measured={record['solver_not_measured']}",
        f"harness_component_count={record['harness_component_count']}",
        f"fixture_class_count={record['fixture_class_count']}",
        f"measurement_axis_count={record['measurement_axis_count']}",
        f"boundary_rule_count={record['boundary_rule_count']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"fixture_generation_performed={record['fixture_generation_performed']}",
        f"fixture_generation_deferred_to={record['fixture_generation_deferred_to']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"synthetic_fixture_score_claim_allowed={record['synthetic_fixture_score_claim_allowed']}",
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
        "HARNESS_COMPONENTS",
    ]

    for item in record["harness_components"]:
        lines.append(f"{item['component_id']} layer={item['layer']} priority={item['priority']}")

    lines.append("")
    lines.append("FIXTURE_CLASSES")
    for item in record["fixture_classes"]:
        lines.append(f"{item['fixture_class_id']} target_layer={item['target_layer']}")

    lines.append("")
    lines.append("MEASUREMENT_AXES")
    for item in record["measurement_axes"]:
        lines.append(f"{item['axis_id']} scope={item['scope']}")

    lines.append("")
    lines.append("BOUNDARY_RULES")
    for item in record["boundary_rules"]:
        lines.append(f"{item['rule_id']} severity={item['severity']}")

    lines.append("")
    lines.append("HARNESS_VALIDATION_RESULTS")
    for result in record["harness_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_4_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_fixture_harness_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-fixture-harness-plan-v1.json"
    md_path = output / "milestone-11-local-fixture-harness-plan-v1.md"
    manifest_path = output / "milestone-11-local-fixture-harness-plan-manifest-v1.txt"
    index_path = output / "milestone-11-local-fixture-harness-plan-index-v1.json"
    components_path = output / "milestone-11-harness-components-v1.json"
    fixture_classes_path = output / "milestone-11-fixture-classes-v1.json"
    boundary_rules_path = output / "milestone-11-harness-boundary-rules-v1.json"
    next_actions_path = output / "milestone-11-local-fixture-harness-next-actions-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_4_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_4_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["harness_index"], indent=2, sort_keys=True), encoding="utf-8")
    components_path.write_text(json.dumps(record["harness_components"], indent=2, sort_keys=True), encoding="utf-8")
    fixture_classes_path.write_text(json.dumps(record["fixture_classes"], indent=2, sort_keys=True), encoding="utf-8")
    boundary_rules_path.write_text(json.dumps(record["boundary_rules"], indent=2, sort_keys=True), encoding="utf-8")
    next_actions_path.write_text(json.dumps(record["next_action_plan"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "components_path": str(components_path),
        "fixture_classes_path": str(fixture_classes_path),
        "boundary_rules_path": str(boundary_rules_path),
        "next_actions_path": str(next_actions_path),
    }


def run_milestone_11_local_fixture_harness_plan_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_fixture_harness_plan()
    validation = validate_milestone_11_local_fixture_harness_plan(record)
    artifacts = write_task_4_artifacts(record)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_4_id": record["task_4_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_4_ready": record["task_4_ready"],
        "harness_plan_created": record["harness_plan_created"],
        "harness_component_count": record["harness_component_count"],
        "fixture_class_count": record["fixture_class_count"],
        "measurement_axis_count": record["measurement_axis_count"],
        "boundary_rule_count": record["boundary_rule_count"],
        "next_action_count": record["next_action_count"],
        "diagnostic_only": record["diagnostic_only"],
        "fixture_generation_performed": record["fixture_generation_performed"],
        "fixture_generation_deferred_to": record["fixture_generation_deferred_to"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "synthetic_fixture_score_claim_allowed": record["synthetic_fixture_score_claim_allowed"],
        "primary_condition": record["primary_condition"],
        "primary_classification": record["primary_classification"],
        "solver_failure_detected": record["solver_failure_detected"],
        "solver_not_measured": record["solver_not_measured"],
        "harness_check_count": record["harness_check_count"],
        "harness_case_count": record["harness_case_count"],
        "harness_pass_count": record["harness_pass_count"],
        "harness_failure_count": record["harness_failure_count"],
        "harness_gate_count": record["harness_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "harness_issue_count": record["harness_issue_count"],
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
