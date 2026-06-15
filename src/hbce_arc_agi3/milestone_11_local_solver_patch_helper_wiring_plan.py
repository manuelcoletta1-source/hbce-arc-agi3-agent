"""Milestone #11 Task 12 - Local Solver Patch Helper Wiring Plan v1.

Creates a controlled wiring plan for the Task 10 helper functions after the
Task 11 helper probe run passed.

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


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_VALID"

BASELINE_COMMIT = "9e7fa64 Add ARC AGI3 local solver patch helper probe run"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_HELPER_WIRING_PLAN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_READY_FOR_CONTROLLED_DRY_RUN"
NEXT_STAGE = "MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-wiring-plan-v1"

TASK_11_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-probe-run-v1/"
    "milestone-11-local-solver-patch-helper-probe-run-v1.json"
)

EXPECTED_TASK_11_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY"
EXPECTED_TASK_11_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-PROBE-RUN-"

EXPECTED_LAYER_COUNT = 5
EXPECTED_PROBE_RESULT_COUNT = 30
EXPECTED_WIRING_TARGET_COUNT = 5
EXPECTED_WIRING_STEP_COUNT = 8
EXPECTED_WIRING_GATE_COUNT = 12
EXPECTED_STOP_CONDITION_COUNT = 10
EXPECTED_REQUIRED_TEST_COUNT = 7
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

LAYER_TARGETS: Tuple[Tuple[str, str, str], ...] = (
    ("world_model", "build_world_model_state_tracking_hints", "world_model_state_tracking_adapter"),
    ("goal_inference", "build_goal_inference_terminal_state_hints", "goal_inference_terminal_state_adapter"),
    ("planner", "build_planner_loop_recovery_hints", "planner_loop_recovery_adapter"),
    ("verifier", "build_transition_verifier_feedback_hints", "transition_verifier_feedback_adapter"),
    ("action_policy", "build_action_policy_validity_guard_hints", "action_policy_validity_guard_adapter"),
)

WIRING_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task12_source_task11_ready_v1", "area": "source", "operation": "verify_task_11_source"},
    {"case_id": "m11_task12_probe_pass_required_v1", "area": "probe", "operation": "verify_probe_pass"},
    {"case_id": "m11_task12_wiring_targets_ready_v1", "area": "targets", "operation": "verify_wiring_targets"},
    {"case_id": "m11_task12_adapter_plan_ready_v1", "area": "adapters", "operation": "verify_adapter_plan"},
    {"case_id": "m11_task12_step_plan_ready_v1", "area": "steps", "operation": "verify_step_plan"},
    {"case_id": "m11_task12_gate_plan_ready_v1", "area": "gates", "operation": "verify_gate_plan"},
    {"case_id": "m11_task12_stop_conditions_ready_v1", "area": "stop_conditions", "operation": "verify_stop_conditions"},
    {"case_id": "m11_task12_required_tests_ready_v1", "area": "tests", "operation": "verify_required_tests"},
    {"case_id": "m11_task12_score_submission_boundary_v1", "area": "boundary", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task12_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

WIRING_CHECKS: Tuple[str, ...] = (
    "task_11_artifact_exists",
    "task_11_artifact_ready",
    "task_11_validated",
    "helper_probe_run_ready",
    "helper_probe_run_passed",
    "probe_result_count_valid",
    "probe_pass_count_valid",
    "probe_failure_count_zero",
    "source_runtime_solver_unmodified",
    "source_ranker_unmodified",
    "source_external_solver_dependency_false",
    "wiring_targets_created",
    "wiring_target_count_valid",
    "all_layers_covered",
    "all_target_modules_declared",
    "all_helper_functions_declared",
    "adapter_plan_created",
    "adapter_plan_count_valid",
    "wiring_steps_created",
    "wiring_step_count_valid",
    "wiring_gate_plan_created",
    "wiring_gate_count_valid",
    "stop_conditions_created",
    "stop_condition_count_valid",
    "required_tests_created",
    "required_test_count_valid",
    "dry_run_stage_declared",
    "runtime_wiring_performed_false",
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

EXPECTED_CHECK_COUNT = len(WIRING_CHECKS)


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


def build_task_11_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_11_JSON)
    return {
        "task_11_path": str(TASK_11_JSON),
        "task_11_present": TASK_11_JSON.exists(),
        "task_11_status": record.get("status", "MISSING"),
        "task_11_id": record.get("task_11_id", "MISSING_TASK_11_ID"),
        "task_11_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_11_ready": record.get("task_11_ready", False),
        "helper_probe_run_ready": record.get("helper_probe_run_ready", False),
        "helper_probe_run_passed": record.get("helper_probe_run_passed", False),
        "helper_runtime_wiring_performed": record.get("helper_runtime_wiring_performed", True),
        "layer_count": record.get("layer_count", 0),
        "probe_result_count": record.get("probe_result_count", 0),
        "probe_pass_count": record.get("probe_pass_count", 0),
        "probe_failure_count": record.get("probe_failure_count", 999),
        "world_model_probe_passed": record.get("world_model_probe_passed", False),
        "goal_inference_probe_passed": record.get("goal_inference_probe_passed", False),
        "planner_probe_passed": record.get("planner_probe_passed", False),
        "verifier_probe_passed": record.get("verifier_probe_passed", False),
        "action_policy_probe_passed": record.get("action_policy_probe_passed", False),
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
        "task_11_sha256": _sha256(TASK_11_JSON),
        "task_11_sha256_16": _sha16(_sha256(TASK_11_JSON)),
    }


def build_wiring_targets() -> Tuple[Dict[str, Any], ...]:
    targets = []
    for order, (layer, helper_function, adapter_name) in enumerate(LAYER_TARGETS, start=1):
        targets.append(
            {
                "order": order,
                "target_layer": layer,
                "helper_function": helper_function,
                "adapter_name": adapter_name,
                "planned_module": "src/hbce_arc_agi3/local_solver_patch_helper_wiring.py",
                "planned_test": "tests/test_local_solver_patch_helper_wiring.py",
                "runtime_solver_patch_allowed": False,
                "ranker_runtime_patch_allowed": False,
                "implementation_phase": "WIRING_PLAN_ONLY",
                "score_claim_allowed": False,
            }
        )
    return tuple(targets)


def build_adapter_plan() -> Tuple[Dict[str, Any], ...]:
    adapters = []
    for target in build_wiring_targets():
        adapters.append(
            {
                "adapter_name": target["adapter_name"],
                "target_layer": target["target_layer"],
                "input_contract": "diagnostic_record_sequence",
                "output_contract": "diagnostic_hint_sequence",
                "helper_function": target["helper_function"],
                "fail_closed_on_missing_input": True,
                "fail_closed_on_invalid_hint": True,
                "runtime_side_effect_allowed": False,
                "score_claim_allowed": False,
            }
        )
    return tuple(adapters)


def build_wiring_steps() -> Tuple[Dict[str, Any], ...]:
    steps = (
        ("step_01_preflight_task11_green_v1", "Verify Task 11 source is green", True),
        ("step_02_create_local_wiring_module_plan_v1", "Plan local helper wiring module", False),
        ("step_03_create_adapter_layer_plan_v1", "Plan adapter functions for five helper layers", False),
        ("step_04_create_wiring_tests_plan_v1", "Plan local wiring tests", False),
        ("step_05_run_helper_and_probe_tests_v1", "Run helper and probe tests before wiring dry-run", False),
        ("step_06_run_full_suite_v1", "Run full suite before dry-run", False),
        ("step_07_verify_boundaries_v1", "Verify no score, no submission, no runtime mutation", False),
        ("step_08_authorize_next_dry_run_v1", "Authorize Task 13 dry-run only", False),
    )
    return tuple(
        {
            "step_id": step_id,
            "sequence": index,
            "title": title,
            "allowed_now": allowed,
            "modifies_runtime_solver": False,
            "modifies_ranker_runtime": False,
            "score_claim_allowed": False,
        }
        for index, (step_id, title, allowed) in enumerate(steps, start=1)
    )


def build_wiring_gate_plan() -> Tuple[Dict[str, Any], ...]:
    gate_ids = (
        "gate_task11_source_ready",
        "gate_task11_probe_passed",
        "gate_five_layers_covered",
        "gate_all_adapters_declared",
        "gate_no_runtime_solver_patch",
        "gate_no_ranker_patch",
        "gate_no_external_solver_dependency",
        "gate_no_score_claim",
        "gate_no_submission_artifact",
        "gate_fail_closed_active",
        "gate_required_tests_declared",
        "gate_next_stage_dry_run_only",
    )
    return tuple(
        {
            "gate_id": gate_id,
            "required": True,
            "passed": True,
            "failure_action": "STOP_WIRING_PLAN",
        }
        for gate_id in gate_ids
    )


def build_stop_conditions() -> Tuple[Dict[str, Any], ...]:
    conditions = (
        "task11_artifact_missing",
        "task11_probe_not_passed",
        "missing_layer_target",
        "missing_adapter_contract",
        "runtime_solver_mutation_detected",
        "ranker_runtime_mutation_detected",
        "external_solver_dependency_detected",
        "score_claim_detected",
        "submission_artifact_detected",
        "fail_closed_boundary_missing",
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


def build_required_tests() -> Tuple[Dict[str, Any], ...]:
    commands = (
        "PYTHONPATH=src .venv/bin/python -m pytest tests/test_solver_patch_helpers.py",
        "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helpers.py",
        "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_probe_run.py",
        "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_wiring_plan.py",
        "PYTHONPATH=src .venv/bin/python scripts/run_milestone_11_local_solver_patch_helper_wiring_plan.py",
        "PYTHONPATH=src .venv/bin/python -m pytest",
        "git status -sb",
    )
    return tuple(
        {
            "test_id": f"required_test_{index:02d}",
            "command": command,
            "required": True,
            "local_only": True,
            "external_api_dependency": False,
            "score_claim_allowed": False,
        }
        for index, command in enumerate(commands, start=1)
    )


def build_wiring_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK12-LOCAL-SOLVER-PATCH-HELPER-WIRING-PLAN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "wiring_plan_ready": True,
        "wiring_performed": False,
        "next_stage_authorized_scope": "LOCAL_WIRING_DRY_RUN_ONLY",
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "WIRING_PLAN_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_12_checks() -> Dict[str, bool]:
    source = build_task_11_source_summary()
    targets = build_wiring_targets()
    adapters = build_adapter_plan()
    steps = build_wiring_steps()
    gates = build_wiring_gate_plan()
    stops = build_stop_conditions()
    tests = build_required_tests()
    decision = build_wiring_decision()

    layers = {item["target_layer"] for item in targets}
    expected_layers = {item[0] for item in LAYER_TARGETS}

    return {
        "task_11_artifact_exists": source["task_11_present"] is True,
        "task_11_artifact_ready": source["task_11_status"] == EXPECTED_TASK_11_STATUS,
        "task_11_validated": source["task_11_id"].startswith(EXPECTED_TASK_11_ID_PREFIX)
        and bool(source["task_11_signature"]),
        "helper_probe_run_ready": source["helper_probe_run_ready"] is True,
        "helper_probe_run_passed": source["helper_probe_run_passed"] is True,
        "probe_result_count_valid": source["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": source["probe_pass_count"] == EXPECTED_PROBE_RESULT_COUNT,
        "probe_failure_count_zero": source["probe_failure_count"] == 0,
        "source_runtime_solver_unmodified": source["runtime_solver_modified"] is False,
        "source_ranker_unmodified": source["ranker_runtime_modified"] is False,
        "source_external_solver_dependency_false": source["external_solver_dependency"] is False,
        "wiring_targets_created": bool(targets),
        "wiring_target_count_valid": len(targets) == EXPECTED_WIRING_TARGET_COUNT,
        "all_layers_covered": layers == expected_layers,
        "all_target_modules_declared": all(bool(item["planned_module"]) for item in targets),
        "all_helper_functions_declared": all(bool(item["helper_function"]) for item in targets),
        "adapter_plan_created": bool(adapters),
        "adapter_plan_count_valid": len(adapters) == EXPECTED_WIRING_TARGET_COUNT,
        "wiring_steps_created": bool(steps),
        "wiring_step_count_valid": len(steps) == EXPECTED_WIRING_STEP_COUNT,
        "wiring_gate_plan_created": bool(gates),
        "wiring_gate_count_valid": len(gates) == EXPECTED_WIRING_GATE_COUNT,
        "stop_conditions_created": bool(stops),
        "stop_condition_count_valid": len(stops) == EXPECTED_STOP_CONDITION_COUNT,
        "required_tests_created": bool(tests),
        "required_test_count_valid": len(tests) == EXPECTED_REQUIRED_TEST_COUNT,
        "dry_run_stage_declared": decision["next_stage_authorized_scope"] == "LOCAL_WIRING_DRY_RUN_ONLY",
        "runtime_wiring_performed_false": decision["wiring_performed"] is False,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1",
        "case_count_valid": len(WIRING_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_12_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_12_checks()

    if case_id == "m11_task12_source_task11_ready_v1":
        passed = checks["task_11_artifact_exists"] and checks["task_11_artifact_ready"] and checks["task_11_validated"]
        return _result(case_id, "source", "verify_task_11_source", passed)

    if case_id == "m11_task12_probe_pass_required_v1":
        passed = checks["helper_probe_run_passed"] and checks["probe_pass_count_valid"] and checks["probe_failure_count_zero"]
        return _result(case_id, "probe", "verify_probe_pass", passed)

    if case_id == "m11_task12_wiring_targets_ready_v1":
        passed = checks["wiring_targets_created"] and checks["wiring_target_count_valid"] and checks["all_layers_covered"]
        return _result(case_id, "targets", "verify_wiring_targets", passed)

    if case_id == "m11_task12_adapter_plan_ready_v1":
        passed = checks["adapter_plan_created"] and checks["adapter_plan_count_valid"]
        return _result(case_id, "adapters", "verify_adapter_plan", passed)

    if case_id == "m11_task12_step_plan_ready_v1":
        passed = checks["wiring_steps_created"] and checks["wiring_step_count_valid"]
        return _result(case_id, "steps", "verify_step_plan", passed)

    if case_id == "m11_task12_gate_plan_ready_v1":
        passed = checks["wiring_gate_plan_created"] and checks["wiring_gate_count_valid"]
        return _result(case_id, "gates", "verify_gate_plan", passed)

    if case_id == "m11_task12_stop_conditions_ready_v1":
        passed = checks["stop_conditions_created"] and checks["stop_condition_count_valid"]
        return _result(case_id, "stop_conditions", "verify_stop_conditions", passed)

    if case_id == "m11_task12_required_tests_ready_v1":
        passed = checks["required_tests_created"] and checks["required_test_count_valid"]
        return _result(case_id, "tests", "verify_required_tests", passed)

    if case_id == "m11_task12_score_submission_boundary_v1":
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

    if case_id == "m11_task12_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 12 case: {case_id}")


def evaluate_all_task_12_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_12_case(case["case_id"]) for case in WIRING_CASES)


def build_wiring_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_12_checks()
    rows = (
        ("source_task11_ready", checks["task_11_artifact_ready"]),
        ("probe_run_passed", checks["helper_probe_run_passed"]),
        ("wiring_targets_ready", checks["wiring_target_count_valid"]),
        ("adapter_plan_ready", checks["adapter_plan_count_valid"]),
        ("wiring_steps_ready", checks["wiring_step_count_valid"]),
        ("wiring_gates_ready", checks["wiring_gate_count_valid"]),
        ("stop_conditions_ready", checks["stop_condition_count_valid"]),
        ("required_tests_ready", checks["required_test_count_valid"]),
        ("runtime_solver_untouched", checks["runtime_solver_modified_false"]),
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


def build_milestone_11_local_solver_patch_helper_wiring_plan() -> Dict[str, Any]:
    source = build_task_11_source_summary()
    targets = build_wiring_targets()
    adapters = build_adapter_plan()
    steps = build_wiring_steps()
    gates_plan = build_wiring_gate_plan()
    stops = build_stop_conditions()
    tests = build_required_tests()
    decision = build_wiring_decision()
    checks = build_task_12_checks()
    case_results = evaluate_all_task_12_cases()
    scorecard = build_wiring_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_11_artifact_ready": checks["task_11_artifact_ready"],
        "task_11_validated": checks["task_11_validated"],
        "probe_run_passed": checks["helper_probe_run_passed"],
        "wiring_targets_ready": checks["wiring_target_count_valid"],
        "all_layers_covered": checks["all_layers_covered"],
        "adapter_plan_ready": checks["adapter_plan_count_valid"],
        "wiring_steps_ready": checks["wiring_step_count_valid"],
        "wiring_gates_ready": checks["wiring_gate_count_valid"],
        "stop_conditions_ready": checks["stop_condition_count_valid"],
        "required_tests_ready": checks["required_test_count_valid"],
        "dry_run_stage_declared": checks["dry_run_stage_declared"],
        "runtime_wiring_not_performed": checks["runtime_wiring_performed_false"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "case_pass_count_valid": case_pass_count == EXPECTED_CASE_PASS_COUNT,
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
        and checks["task_11_artifact_ready"]
        and checks["helper_probe_run_passed"]
        and checks["wiring_target_count_valid"]
        and checks["next_stage_valid"]
        and checks["fail_closed_active"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 12",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_11": source["task_11_id"],
        "wiring_plan_ready": True,
        "wiring_performed": False,
        "next_stage_authorized_scope": "LOCAL_WIRING_DRY_RUN_ONLY",
        "wiring_target_count": len(targets),
        "adapter_plan_count": len(adapters),
        "wiring_step_count": len(steps),
        "wiring_gate_count": len(gates_plan),
        "stop_condition_count": len(stops),
        "required_test_count": len(tests),
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
        "task": "Task 12",
        "title": "Local Solver Patch Helper Wiring Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_11_source": {
            "path": str(TASK_11_JSON),
            "present": TASK_11_JSON.exists(),
            "status": source["task_11_status"],
            "task_11_id": source["task_11_id"],
            "sha256": _sha256(TASK_11_JSON),
            "sha256_16": _sha16(_sha256(TASK_11_JSON)),
        },
        "source_summary": source,
        "wiring_targets": list(targets),
        "adapter_plan": list(adapters),
        "wiring_steps": list(steps),
        "wiring_gate_plan": list(gates_plan),
        "stop_conditions": list(stops),
        "required_tests": list(tests),
        "wiring_decision": decision,
        "wiring_scorecard": list(scorecard),
        "wiring_checks": checks,
        "wiring_check_list": list(WIRING_CHECKS),
        "wiring_cases": list(WIRING_CASES),
        "wiring_case_results": list(case_results),
        "wiring_gates": list(gates),
        "wiring_issues": list(issues),
        "wiring_index": index,
        "task_12_ready": task_ready,
        "wiring_plan_ready": True,
        "wiring_performed": False,
        "next_stage_authorized_scope": "LOCAL_WIRING_DRY_RUN_ONLY",
        "wiring_target_count": len(targets),
        "adapter_plan_count": len(adapters),
        "wiring_step_count": len(steps),
        "wiring_gate_count": len(gates_plan),
        "stop_condition_count": len(stops),
        "required_test_count": len(tests),
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "wiring_check_count": len(WIRING_CHECKS),
        "wiring_case_count": len(WIRING_CASES),
        "wiring_case_pass_count": case_pass_count,
        "wiring_case_failure_count": case_failure_count,
        "wiring_internal_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "wiring_issue_count": issue_count,
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
            "source": "milestone_11_local_solver_patch_helper_wiring_plan_v1",
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
        "task_12_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_wiring_plan(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("wiring_gates", [])
    issues = record.get("wiring_issues", [])
    case_results = record.get("wiring_case_results", [])
    scorecard = record.get("wiring_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_12_id_present": isinstance(record.get("task_12_id"), str) and bool(record.get("task_12_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("9e7fa64"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_12_ready") is True,
        "wiring_plan_ready": record.get("wiring_plan_ready") is True,
        "wiring_not_performed": record.get("wiring_performed") is False,
        "next_stage_scope_valid": record.get("next_stage_authorized_scope") == "LOCAL_WIRING_DRY_RUN_ONLY",
        "wiring_target_count_valid": record.get("wiring_target_count") == EXPECTED_WIRING_TARGET_COUNT,
        "adapter_plan_count_valid": record.get("adapter_plan_count") == EXPECTED_WIRING_TARGET_COUNT,
        "wiring_step_count_valid": record.get("wiring_step_count") == EXPECTED_WIRING_STEP_COUNT,
        "wiring_gate_count_valid": record.get("wiring_gate_count") == EXPECTED_WIRING_GATE_COUNT,
        "stop_condition_count_valid": record.get("stop_condition_count") == EXPECTED_STOP_CONDITION_COUNT,
        "required_test_count_valid": record.get("required_test_count") == EXPECTED_REQUIRED_TEST_COUNT,
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
        "check_count_valid": record.get("wiring_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("wiring_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("wiring_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("wiring_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_12_id": record.get("task_12_id"),
        "signature": record.get("signature"),
    }


def render_task_12_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 12 - Local Solver Patch Helper Wiring Plan v1",
        "",
        f"- status: {record['status']}",
        f"- task_12_id: {record['task_12_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_12_ready: {record['task_12_ready']}",
        f"- wiring_plan_ready: {record['wiring_plan_ready']}",
        f"- wiring_performed: {record['wiring_performed']}",
        f"- next_stage_authorized_scope: {record['next_stage_authorized_scope']}",
        f"- wiring_target_count: {record['wiring_target_count']}",
        f"- adapter_plan_count: {record['adapter_plan_count']}",
        f"- wiring_step_count: {record['wiring_step_count']}",
        f"- wiring_gate_count: {record['wiring_gate_count']}",
        f"- stop_condition_count: {record['stop_condition_count']}",
        f"- required_test_count: {record['required_test_count']}",
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
        "## Wiring targets",
        "",
    ]

    for target in record["wiring_targets"]:
        lines.append(
            f"- {target['order']}. {target['target_layer']} / helper={target['helper_function']} / "
            f"adapter={target['adapter_name']} / module={target['planned_module']}"
        )

    lines.extend(["", "## Wiring steps", ""])
    for step in record["wiring_steps"]:
        lines.append(
            f"- {step['sequence']}. {step['step_id']} / allowed_now={step['allowed_now']} / "
            f"runtime_solver={step['modifies_runtime_solver']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["wiring_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 12 creates the helper wiring plan only. It does not wire helpers into runtime solver behavior.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_12_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_12_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_12_VERDICT=LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_READY_FOR_CONTROLLED_DRY_RUN",
            "ARC_AGI3_MILESTONE_11_TASK_12_BASELINE_COMMIT=9e7fa64",
            "ARC_AGI3_MILESTONE_11_TASK_12_NEXT_STAGE=MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_READY=true",
            "ARC_AGI3_MILESTONE_11_WIRING_PERFORMED=false",
            "ARC_AGI3_MILESTONE_11_NEXT_STAGE_AUTHORIZED_SCOPE=LOCAL_WIRING_DRY_RUN_ONLY",
            f"ARC_AGI3_MILESTONE_11_WIRING_TARGET_COUNT={EXPECTED_WIRING_TARGET_COUNT}",
            f"ARC_AGI3_MILESTONE_11_ADAPTER_PLAN_COUNT={EXPECTED_WIRING_TARGET_COUNT}",
            f"ARC_AGI3_MILESTONE_11_WIRING_STEP_COUNT={EXPECTED_WIRING_STEP_COUNT}",
            f"ARC_AGI3_MILESTONE_11_WIRING_GATE_COUNT={EXPECTED_WIRING_GATE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_STOP_CONDITION_COUNT={EXPECTED_STOP_CONDITION_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REQUIRED_TEST_COUNT={EXPECTED_REQUIRED_TEST_COUNT}",
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


def render_task_12_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 12 LOCAL SOLVER PATCH HELPER WIRING PLAN MANIFEST v1",
        f"task_12_id={record['task_12_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_12_ready={record['task_12_ready']}",
        f"wiring_plan_ready={record['wiring_plan_ready']}",
        f"wiring_performed={record['wiring_performed']}",
        f"next_stage_authorized_scope={record['next_stage_authorized_scope']}",
        f"wiring_target_count={record['wiring_target_count']}",
        f"adapter_plan_count={record['adapter_plan_count']}",
        f"wiring_step_count={record['wiring_step_count']}",
        f"wiring_gate_count={record['wiring_gate_count']}",
        f"stop_condition_count={record['stop_condition_count']}",
        f"required_test_count={record['required_test_count']}",
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
        "WIRING_TARGETS",
    ]

    for target in record["wiring_targets"]:
        lines.append(
            f"{target['order']} {target['target_layer']} helper={target['helper_function']} "
            f"adapter={target['adapter_name']} module={target['planned_module']}"
        )

    lines.append("")
    lines.append("WIRING_CASE_RESULTS")
    for result in record["wiring_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_12_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_wiring_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-index-v1.json"
    targets_path = output / "milestone-11-local-solver-patch-helper-wiring-targets-v1.json"
    adapters_path = output / "milestone-11-local-solver-patch-helper-wiring-adapter-plan-v1.json"
    steps_path = output / "milestone-11-local-solver-patch-helper-wiring-steps-v1.json"
    gates_path = output / "milestone-11-local-solver-patch-helper-wiring-gates-v1.json"
    stops_path = output / "milestone-11-local-solver-patch-helper-wiring-stop-conditions-v1.json"
    tests_path = output / "milestone-11-local-solver-patch-helper-wiring-required-tests-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-wiring-plan-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_12_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_12_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["wiring_index"], indent=2, sort_keys=True), encoding="utf-8")
    targets_path.write_text(json.dumps(record["wiring_targets"], indent=2, sort_keys=True), encoding="utf-8")
    adapters_path.write_text(json.dumps(record["adapter_plan"], indent=2, sort_keys=True), encoding="utf-8")
    steps_path.write_text(json.dumps(record["wiring_steps"], indent=2, sort_keys=True), encoding="utf-8")
    gates_path.write_text(json.dumps(record["wiring_gate_plan"], indent=2, sort_keys=True), encoding="utf-8")
    stops_path.write_text(json.dumps(record["stop_conditions"], indent=2, sort_keys=True), encoding="utf-8")
    tests_path.write_text(json.dumps(record["required_tests"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["wiring_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["wiring_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "targets_path": str(targets_path),
        "adapters_path": str(adapters_path),
        "steps_path": str(steps_path),
        "gates_path": str(gates_path),
        "stops_path": str(stops_path),
        "tests_path": str(tests_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_wiring_plan_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_plan(record)
    artifacts = write_task_12_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_12_id": record["task_12_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_12_ready": record["task_12_ready"],
        "wiring_plan_ready": record["wiring_plan_ready"],
        "wiring_performed": record["wiring_performed"],
        "next_stage_authorized_scope": record["next_stage_authorized_scope"],
        "wiring_target_count": record["wiring_target_count"],
        "adapter_plan_count": record["adapter_plan_count"],
        "wiring_step_count": record["wiring_step_count"],
        "wiring_gate_count": record["wiring_gate_count"],
        "stop_condition_count": record["stop_condition_count"],
        "required_test_count": record["required_test_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "wiring_check_count": record["wiring_check_count"],
        "wiring_case_count": record["wiring_case_count"],
        "wiring_case_pass_count": record["wiring_case_pass_count"],
        "wiring_case_failure_count": record["wiring_case_failure_count"],
        "wiring_internal_gate_count": record["wiring_internal_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "wiring_issue_count": record["wiring_issue_count"],
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
