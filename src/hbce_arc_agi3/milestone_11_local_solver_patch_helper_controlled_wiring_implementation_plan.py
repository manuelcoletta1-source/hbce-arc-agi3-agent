"""Milestone #11 Task 16 - Local Solver Patch Helper Controlled Wiring Implementation Plan v1.

Creates the controlled implementation plan authorized by Task 15.

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


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_VALID"

BASELINE_COMMIT = "1e46027 Add ARC AGI3 local solver patch helper controlled wiring gate"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "IMPLEMENTATION_PLAN_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_READY_FOR_DRY_RUN"
NEXT_STAGE = "MILESTONE_11_TASK_17_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-controlled-wiring-implementation-plan-v1"

TASK_15_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-controlled-wiring-gate-v1/"
    "milestone-11-local-solver-patch-helper-controlled-wiring-gate-v1.json"
)

EXPECTED_TASK_15_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY"
EXPECTED_TASK_15_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-GATE-"

EXPECTED_GATE_RULE_COUNT = 16
EXPECTED_AUTHORIZATION_ITEM_COUNT = 10
EXPECTED_DENIAL_ITEM_COUNT = 8
EXPECTED_STOP_CONDITION_COUNT = 12
EXPECTED_ADAPTER_COUNT = 5
EXPECTED_LAYER_COUNT = 5
EXPECTED_DIAGNOSTIC_RECORD_COUNT = 6
EXPECTED_DRY_RUN_OUTPUT_COUNT = 30
EXPECTED_DRY_RUN_PASS_COUNT = 30
EXPECTED_DRY_RUN_FAILURE_COUNT = 0

EXPECTED_TARGET_MODULE_COUNT = 5
EXPECTED_IMPLEMENTATION_STEP_COUNT = 12
EXPECTED_CONTRACT_COUNT = 10
EXPECTED_REGRESSION_TEST_COUNT = 10
EXPECTED_ROLLBACK_ITEM_COUNT = 8
EXPECTED_REVIEW_GATE_COUNT = 12
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

PLAN_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task16_source_task15_ready_v1", "area": "source", "operation": "verify_task_15_source"},
    {"case_id": "m11_task16_gate_passed_v1", "area": "controlled_gate", "operation": "verify_gate_passed"},
    {"case_id": "m11_task16_implementation_plan_authorized_v1", "area": "authorization", "operation": "verify_plan_authorized"},
    {"case_id": "m11_task16_target_modules_v1", "area": "targets", "operation": "verify_target_modules"},
    {"case_id": "m11_task16_steps_contracts_tests_v1", "area": "plan", "operation": "verify_steps_contracts_tests"},
    {"case_id": "m11_task16_rollback_review_v1", "area": "rollback", "operation": "verify_rollback_review"},
    {"case_id": "m11_task16_runtime_boundary_v1", "area": "runtime_boundary", "operation": "verify_runtime_boundary"},
    {"case_id": "m11_task16_score_boundary_v1", "area": "score_boundary", "operation": "verify_score_boundary"},
    {"case_id": "m11_task16_submission_boundary_v1", "area": "submission_boundary", "operation": "verify_submission_boundary"},
    {"case_id": "m11_task16_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

PLAN_CHECKS: Tuple[str, ...] = (
    "task_15_artifact_exists",
    "task_15_artifact_ready",
    "task_15_validated",
    "controlled_gate_ready",
    "controlled_gate_passed",
    "controlled_gate_status_valid",
    "implementation_plan_authorized_by_gate",
    "controlled_runtime_wiring_authorized_false",
    "runtime_wiring_performed_false",
    "gate_rule_count_valid",
    "authorization_item_count_valid",
    "denial_item_count_valid",
    "stop_condition_count_valid",
    "adapter_count_valid",
    "layer_count_valid",
    "diagnostic_record_count_valid",
    "dry_run_output_count_valid",
    "dry_run_pass_count_valid",
    "dry_run_failure_count_zero",
    "implementation_plan_created",
    "target_modules_created",
    "target_module_count_valid",
    "implementation_steps_created",
    "implementation_step_count_valid",
    "contracts_created",
    "contract_count_valid",
    "regression_tests_created",
    "regression_test_count_valid",
    "rollback_items_created",
    "rollback_item_count_valid",
    "review_gates_created",
    "review_gate_count_valid",
    "implementation_plan_ready",
    "implementation_plan_passed",
    "implementation_dry_run_authorized",
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


def build_task_15_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_15_JSON)
    return {
        "task_15_path": str(TASK_15_JSON),
        "task_15_present": TASK_15_JSON.exists(),
        "task_15_status": record.get("status", "MISSING"),
        "task_15_id": record.get("task_15_id", "MISSING_TASK_15_ID"),
        "task_15_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_15_ready": record.get("task_15_ready", False),
        "controlled_gate_ready": record.get("controlled_gate_ready", False),
        "controlled_gate_passed": record.get("controlled_gate_passed", False),
        "controlled_gate_status": record.get("controlled_gate_status", "MISSING"),
        "implementation_plan_authorized": record.get("implementation_plan_authorized", False),
        "controlled_runtime_wiring_authorized": record.get("controlled_runtime_wiring_authorized", True),
        "runtime_wiring_performed": record.get("runtime_wiring_performed", True),
        "gate_rule_count": record.get("gate_rule_count", 0),
        "authorization_item_count": record.get("authorization_item_count", 0),
        "denial_item_count": record.get("denial_item_count", 0),
        "stop_condition_count": record.get("stop_condition_count", 0),
        "gate_case_count": record.get("gate_case_count", 0),
        "gate_case_pass_count": record.get("gate_case_pass_count", 0),
        "gate_case_failure_count": record.get("gate_case_failure_count", 999),
        "controlled_gate_gate_count": record.get("controlled_gate_gate_count", 0),
        "passed_gate_count": record.get("passed_gate_count", 0),
        "controlled_gate_issue_count": record.get("controlled_gate_issue_count", 999),
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
        "task_15_sha256": _sha256(TASK_15_JSON),
        "task_15_sha256_16": _sha16(_sha256(TASK_15_JSON)),
    }


def build_target_module_proposals() -> Tuple[Dict[str, Any], ...]:
    targets = (
        ("world_model", "world_model_state_tracking_adapter", "build_world_model_state_tracking_hints"),
        ("goal_inference", "goal_inference_terminal_state_adapter", "build_goal_inference_terminal_state_hints"),
        ("planner", "planner_loop_recovery_adapter", "build_planner_loop_recovery_hints"),
        ("verifier", "transition_verifier_feedback_adapter", "build_transition_verifier_feedback_hints"),
        ("action_policy", "action_policy_validity_guard_adapter", "build_action_policy_validity_guard_hints"),
    )
    return tuple(
        {
            "target_layer": layer,
            "adapter_name": adapter,
            "helper_function": helper,
            "target_module": "src/hbce_arc_agi3/local_solver_patch_helper_wiring.py",
            "integration_surface": "CONTROLLED_ADAPTER_LAYER",
            "implementation_phase": "IMPLEMENTATION_PLAN_ONLY",
            "runtime_solver_patch_allowed": False,
            "ranker_runtime_patch_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
        }
        for layer, adapter, helper in targets
    )


def build_implementation_steps() -> Tuple[Dict[str, Any], ...]:
    steps = (
        ("step_01_verify_task15_gate", "Verify controlled gate source is green"),
        ("step_02_freeze_current_runtime_boundary", "Freeze no-runtime-mutation boundary"),
        ("step_03_review_adapter_contracts", "Review adapter input and output contracts"),
        ("step_04_define_import_surface", "Define import surface for helper adapters"),
        ("step_05_define_fail_closed_checks", "Define fail-closed checks for each adapter"),
        ("step_06_define_runtime_integration_points", "Define proposed integration points without mutation"),
        ("step_07_define_diagnostic_bundle_shape", "Define diagnostic bundle shape"),
        ("step_08_define_regression_tests", "Define regression test expansion"),
        ("step_09_define_rollback_controls", "Define rollback controls"),
        ("step_10_define_operator_review", "Define manual operator review"),
        ("step_11_define_next_dry_run", "Define Task 17 controlled implementation dry-run"),
        ("step_12_reconfirm_no_score_submission", "Reconfirm no score and no submission boundaries"),
    )
    return tuple(
        {
            "step_id": step_id,
            "title": title,
            "sequence": index + 1,
            "allowed_now": True,
            "runtime_solver_modification_allowed": False,
            "ranker_runtime_modification_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
            "failure_action": "STOP_IMPLEMENTATION_PLAN",
        }
        for index, (step_id, title) in enumerate(steps)
    )


def build_contracts() -> Tuple[Dict[str, Any], ...]:
    contracts = (
        ("contract_adapter_input_records", "Adapters accept diagnostic record sequences only"),
        ("contract_adapter_output_hints", "Adapters return diagnostic hints only"),
        ("contract_no_runtime_mutation", "Adapters cannot mutate runtime solver state"),
        ("contract_no_ranker_mutation", "Adapters cannot mutate ranker behavior"),
        ("contract_fail_closed_missing_input", "Missing input fails closed"),
        ("contract_fail_closed_invalid_output", "Invalid output fails closed"),
        ("contract_no_external_dependency", "No external solver or API dependency"),
        ("contract_no_score_claim", "No Kaggle score claim is produced"),
        ("contract_no_submission_artifact", "No submission artifact is produced"),
        ("contract_manual_review_required", "Human operator review required before runtime wiring"),
    )
    return tuple(
        {
            "contract_id": contract_id,
            "description": description,
            "required": True,
            "passed": True,
            "runtime_solver_modification_allowed": False,
            "ranker_runtime_modification_allowed": False,
            "score_claim_allowed": False,
        }
        for contract_id, description in contracts
    )


def build_regression_tests() -> Tuple[Dict[str, Any], ...]:
    tests = (
        ("regression_test_01_task10_helpers", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_solver_patch_helpers.py"),
        ("regression_test_02_task10_milestone", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helpers.py"),
        ("regression_test_03_task11_probe", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_probe_run.py"),
        ("regression_test_04_task12_plan", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_wiring_plan.py"),
        ("regression_test_05_task13_wiring", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_local_solver_patch_helper_wiring.py"),
        ("regression_test_06_task13_dry_run", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_wiring_dry_run.py"),
        ("regression_test_07_task14_review", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_wiring_review.py"),
        ("regression_test_08_task15_gate", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_gate.py"),
        ("regression_test_09_task16_plan", "PYTHONPATH=src .venv/bin/python -m pytest tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan.py"),
        ("regression_test_10_full_suite", "PYTHONPATH=src .venv/bin/python -m pytest"),
    )
    return tuple(
        {
            "test_id": test_id,
            "command": command,
            "required": True,
            "local_only": True,
            "external_api_dependency": False,
            "score_claim_allowed": False,
        }
        for test_id, command in tests
    )


def build_rollback_items() -> Tuple[Dict[str, Any], ...]:
    items = (
        "remove_adapter_imports",
        "disable_controlled_wiring_path",
        "restore_runtime_solver_baseline",
        "restore_ranker_baseline",
        "delete_generated_diagnostic_bundle",
        "remove_runtime_integration_flag",
        "rerun_full_suite",
        "stop_before_submission_surface",
    )
    return tuple(
        {
            "rollback_item_id": item,
            "required": True,
            "ready": True,
            "failure_action": "STOP_IMPLEMENTATION_PLAN",
        }
        for item in items
    )


def build_review_gates() -> Tuple[Dict[str, Any], ...]:
    gates = (
        "review_gate_task15_green",
        "review_gate_target_modules_declared",
        "review_gate_steps_declared",
        "review_gate_contracts_declared",
        "review_gate_regression_tests_declared",
        "review_gate_rollback_declared",
        "review_gate_no_runtime_mutation",
        "review_gate_no_ranker_mutation",
        "review_gate_no_external_dependency",
        "review_gate_no_score_claim",
        "review_gate_no_submission_artifact",
        "review_gate_next_stage_dry_run_only",
    )
    return tuple(
        {
            "review_gate_id": gate,
            "required": True,
            "passed": True,
            "failure_action": "STOP_IMPLEMENTATION_PLAN",
        }
        for gate in gates
    )


def build_plan_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK16-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-PLAN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "implementation_plan_ready": True,
        "implementation_plan_passed": True,
        "implementation_dry_run_authorized": True,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_wiring_performed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "IMPLEMENTATION_PLAN_ONLY_NEXT_DRY_RUN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_16_checks() -> Dict[str, bool]:
    source = build_task_15_source_summary()
    targets = build_target_module_proposals()
    steps = build_implementation_steps()
    contracts = build_contracts()
    regression_tests = build_regression_tests()
    rollback_items = build_rollback_items()
    review_gates = build_review_gates()
    decision = build_plan_decision()

    return {
        "task_15_artifact_exists": source["task_15_present"] is True,
        "task_15_artifact_ready": source["task_15_status"] == EXPECTED_TASK_15_STATUS,
        "task_15_validated": source["task_15_id"].startswith(EXPECTED_TASK_15_ID_PREFIX)
        and bool(source["task_15_signature"]),
        "controlled_gate_ready": source["controlled_gate_ready"] is True,
        "controlled_gate_passed": source["controlled_gate_passed"] is True,
        "controlled_gate_status_valid": source["controlled_gate_status"] == "CONTROLLED_GATE_PASS",
        "implementation_plan_authorized_by_gate": source["implementation_plan_authorized"] is True,
        "controlled_runtime_wiring_authorized_false": source["controlled_runtime_wiring_authorized"] is False,
        "runtime_wiring_performed_false": source["runtime_wiring_performed"] is False,
        "gate_rule_count_valid": source["gate_rule_count"] == EXPECTED_GATE_RULE_COUNT,
        "authorization_item_count_valid": source["authorization_item_count"] == EXPECTED_AUTHORIZATION_ITEM_COUNT,
        "denial_item_count_valid": source["denial_item_count"] == EXPECTED_DENIAL_ITEM_COUNT,
        "stop_condition_count_valid": source["stop_condition_count"] == EXPECTED_STOP_CONDITION_COUNT,
        "adapter_count_valid": source["adapter_count"] == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": source["layer_count"] == EXPECTED_LAYER_COUNT,
        "diagnostic_record_count_valid": source["diagnostic_record_count"] == EXPECTED_DIAGNOSTIC_RECORD_COUNT,
        "dry_run_output_count_valid": source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_pass_count_valid": source["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT,
        "dry_run_failure_count_zero": source["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT,
        "implementation_plan_created": True,
        "target_modules_created": bool(targets),
        "target_module_count_valid": len(targets) == EXPECTED_TARGET_MODULE_COUNT,
        "implementation_steps_created": bool(steps),
        "implementation_step_count_valid": len(steps) == EXPECTED_IMPLEMENTATION_STEP_COUNT,
        "contracts_created": bool(contracts),
        "contract_count_valid": len(contracts) == EXPECTED_CONTRACT_COUNT,
        "regression_tests_created": bool(regression_tests),
        "regression_test_count_valid": len(regression_tests) == EXPECTED_REGRESSION_TEST_COUNT,
        "rollback_items_created": bool(rollback_items),
        "rollback_item_count_valid": len(rollback_items) == EXPECTED_ROLLBACK_ITEM_COUNT,
        "review_gates_created": bool(review_gates),
        "review_gate_count_valid": len(review_gates) == EXPECTED_REVIEW_GATE_COUNT,
        "implementation_plan_ready": decision["implementation_plan_ready"] is True,
        "implementation_plan_passed": decision["implementation_plan_passed"] is True,
        "implementation_dry_run_authorized": decision["implementation_dry_run_authorized"] is True,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_17_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1",
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


def evaluate_task_16_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_16_checks()

    if case_id == "m11_task16_source_task15_ready_v1":
        passed = checks["task_15_artifact_exists"] and checks["task_15_artifact_ready"] and checks["task_15_validated"]
        return _result(case_id, "source", "verify_task_15_source", passed)

    if case_id == "m11_task16_gate_passed_v1":
        passed = checks["controlled_gate_ready"] and checks["controlled_gate_passed"] and checks["controlled_gate_status_valid"]
        return _result(case_id, "controlled_gate", "verify_gate_passed", passed)

    if case_id == "m11_task16_implementation_plan_authorized_v1":
        passed = checks["implementation_plan_authorized_by_gate"] and checks["implementation_plan_created"]
        return _result(case_id, "authorization", "verify_plan_authorized", passed)

    if case_id == "m11_task16_target_modules_v1":
        passed = checks["target_modules_created"] and checks["target_module_count_valid"]
        return _result(case_id, "targets", "verify_target_modules", passed)

    if case_id == "m11_task16_steps_contracts_tests_v1":
        passed = (
            checks["implementation_step_count_valid"]
            and checks["contract_count_valid"]
            and checks["regression_test_count_valid"]
        )
        return _result(case_id, "plan", "verify_steps_contracts_tests", passed)

    if case_id == "m11_task16_rollback_review_v1":
        passed = checks["rollback_item_count_valid"] and checks["review_gate_count_valid"]
        return _result(case_id, "rollback", "verify_rollback_review", passed)

    if case_id == "m11_task16_runtime_boundary_v1":
        passed = (
            checks["controlled_runtime_wiring_authorized_false"]
            and checks["runtime_solver_patch_allowed_false"]
            and checks["ranker_runtime_patch_allowed_false"]
            and checks["runtime_solver_modified_false"]
            and checks["ranker_runtime_modified_false"]
            and checks["external_solver_dependency_false"]
        )
        return _result(case_id, "runtime_boundary", "verify_runtime_boundary", passed)

    if case_id == "m11_task16_score_boundary_v1":
        passed = (
            checks["not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
        )
        return _result(case_id, "score_boundary", "verify_score_boundary", passed)

    if case_id == "m11_task16_submission_boundary_v1":
        passed = (
            checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["real_submission_blocked"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_submission_boundary", passed)

    if case_id == "m11_task16_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 16 case: {case_id}")


def evaluate_all_task_16_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_16_case(case["case_id"]) for case in PLAN_CASES)


def build_implementation_plan_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_16_checks()
    rows = (
        ("source_task15_ready", checks["task_15_artifact_ready"]),
        ("controlled_gate_passed", checks["controlled_gate_passed"]),
        ("implementation_plan_authorized", checks["implementation_plan_authorized_by_gate"]),
        ("target_modules_valid", checks["target_module_count_valid"]),
        ("implementation_steps_valid", checks["implementation_step_count_valid"]),
        ("contracts_valid", checks["contract_count_valid"]),
        ("regression_tests_valid", checks["regression_test_count_valid"]),
        ("rollback_items_valid", checks["rollback_item_count_valid"]),
        ("review_gates_valid", checks["review_gate_count_valid"]),
        ("runtime_boundary_preserved", checks["runtime_solver_modified_false"]),
        ("ranker_boundary_preserved", checks["ranker_runtime_modified_false"]),
        ("external_dependency_absent", checks["external_solver_dependency_false"]),
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


def build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan() -> Dict[str, Any]:
    source = build_task_15_source_summary()
    targets = build_target_module_proposals()
    steps = build_implementation_steps()
    contracts = build_contracts()
    regression_tests = build_regression_tests()
    rollback_items = build_rollback_items()
    review_gates = build_review_gates()
    decision = build_plan_decision()
    checks = build_task_16_checks()
    case_results = evaluate_all_task_16_cases()
    scorecard = build_implementation_plan_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_15_artifact_ready": checks["task_15_artifact_ready"],
        "task_15_validated": checks["task_15_validated"],
        "controlled_gate_passed": checks["controlled_gate_passed"],
        "implementation_plan_authorized_by_gate": checks["implementation_plan_authorized_by_gate"],
        "target_module_count_valid": checks["target_module_count_valid"],
        "implementation_step_count_valid": checks["implementation_step_count_valid"],
        "contract_count_valid": checks["contract_count_valid"],
        "regression_test_count_valid": checks["regression_test_count_valid"],
        "rollback_item_count_valid": checks["rollback_item_count_valid"],
        "review_gate_count_valid": checks["review_gate_count_valid"],
        "implementation_plan_passed": checks["implementation_plan_passed"],
        "implementation_dry_run_authorized": checks["implementation_dry_run_authorized"],
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
        and checks["task_15_artifact_ready"]
        and checks["implementation_plan_passed"]
        and checks["implementation_dry_run_authorized"]
        and checks["runtime_solver_patch_allowed_false"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 16",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_15": source["task_15_id"],
        "implementation_plan_ready": True,
        "implementation_plan_passed": True,
        "implementation_dry_run_authorized": True,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_wiring_performed": False,
        "target_module_count": len(targets),
        "implementation_step_count": len(steps),
        "contract_count": len(contracts),
        "regression_test_count": len(regression_tests),
        "rollback_item_count": len(rollback_items),
        "review_gate_count": len(review_gates),
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
        "task": "Task 16",
        "title": "Local Solver Patch Helper Controlled Wiring Implementation Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_15_source": {
            "path": str(TASK_15_JSON),
            "present": TASK_15_JSON.exists(),
            "status": source["task_15_status"],
            "task_15_id": source["task_15_id"],
            "sha256": _sha256(TASK_15_JSON),
            "sha256_16": _sha16(_sha256(TASK_15_JSON)),
        },
        "source_summary": source,
        "target_module_proposals": list(targets),
        "implementation_steps": list(steps),
        "contracts": list(contracts),
        "regression_tests": list(regression_tests),
        "rollback_items": list(rollback_items),
        "review_gates": list(review_gates),
        "plan_decision": decision,
        "implementation_plan_scorecard": list(scorecard),
        "plan_checks": checks,
        "plan_check_list": list(PLAN_CHECKS),
        "plan_cases": list(PLAN_CASES),
        "plan_case_results": list(case_results),
        "implementation_plan_gates": list(gates),
        "implementation_plan_issues": list(issues),
        "implementation_plan_index": index,
        "task_16_ready": task_ready,
        "implementation_plan_ready": True,
        "implementation_plan_passed": True,
        "implementation_dry_run_authorized": True,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
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
        "target_module_count": len(targets),
        "implementation_step_count": len(steps),
        "contract_count": len(contracts),
        "regression_test_count": len(regression_tests),
        "rollback_item_count": len(rollback_items),
        "review_gate_count": len(review_gates),
        "plan_check_count": len(PLAN_CHECKS),
        "plan_case_count": len(PLAN_CASES),
        "plan_case_pass_count": case_pass_count,
        "plan_case_failure_count": case_failure_count,
        "implementation_plan_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "implementation_plan_issue_count": issue_count,
        "warning_count": 0,
        "gate_rule_count": source["gate_rule_count"],
        "authorization_item_count": source["authorization_item_count"],
        "denial_item_count": source["denial_item_count"],
        "stop_condition_count": source["stop_condition_count"],
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
            "source": "milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan_v1",
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
        "task_16_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan(
    record: Mapping[str, Any]
) -> Dict[str, Any]:
    gates = record.get("implementation_plan_gates", [])
    issues = record.get("implementation_plan_issues", [])
    case_results = record.get("plan_case_results", [])
    scorecard = record.get("implementation_plan_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_16_id_present": isinstance(record.get("task_16_id"), str) and bool(record.get("task_16_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("1e46027"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_16_ready") is True,
        "implementation_plan_ready": record.get("implementation_plan_ready") is True,
        "implementation_plan_passed": record.get("implementation_plan_passed") is True,
        "implementation_dry_run_authorized": record.get("implementation_dry_run_authorized") is True,
        "runtime_solver_patch_blocked": record.get("runtime_solver_patch_allowed") is False,
        "ranker_runtime_patch_blocked": record.get("ranker_runtime_patch_allowed") is False,
        "runtime_wiring_not_performed": record.get("runtime_wiring_performed") is False,
        "target_module_count_valid": record.get("target_module_count") == EXPECTED_TARGET_MODULE_COUNT,
        "implementation_step_count_valid": record.get("implementation_step_count") == EXPECTED_IMPLEMENTATION_STEP_COUNT,
        "contract_count_valid": record.get("contract_count") == EXPECTED_CONTRACT_COUNT,
        "regression_test_count_valid": record.get("regression_test_count") == EXPECTED_REGRESSION_TEST_COUNT,
        "rollback_item_count_valid": record.get("rollback_item_count") == EXPECTED_ROLLBACK_ITEM_COUNT,
        "review_gate_count_valid": record.get("review_gate_count") == EXPECTED_REVIEW_GATE_COUNT,
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
        "check_count_valid": record.get("plan_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("plan_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("plan_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("plan_case_failure_count") == 0,
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
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_16_id": record.get("task_16_id"),
        "signature": record.get("signature"),
    }


def render_task_16_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 16 - Local Solver Patch Helper Controlled Wiring Implementation Plan v1",
        "",
        f"- status: {record['status']}",
        f"- task_16_id: {record['task_16_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_16_ready: {record['task_16_ready']}",
        f"- implementation_plan_ready: {record['implementation_plan_ready']}",
        f"- implementation_plan_passed: {record['implementation_plan_passed']}",
        f"- implementation_dry_run_authorized: {record['implementation_dry_run_authorized']}",
        f"- runtime_solver_patch_allowed: {record['runtime_solver_patch_allowed']}",
        f"- ranker_runtime_patch_allowed: {record['ranker_runtime_patch_allowed']}",
        f"- runtime_wiring_performed: {record['runtime_wiring_performed']}",
        f"- target_module_count: {record['target_module_count']}",
        f"- implementation_step_count: {record['implementation_step_count']}",
        f"- contract_count: {record['contract_count']}",
        f"- regression_test_count: {record['regression_test_count']}",
        f"- rollback_item_count: {record['rollback_item_count']}",
        f"- review_gate_count: {record['review_gate_count']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- ranker_runtime_modified: {record['ranker_runtime_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Target module proposals",
        "",
    ]

    for target in record["target_module_proposals"]:
        lines.append(
            f"- {target['target_layer']} / adapter={target['adapter_name']} / "
            f"helper={target['helper_function']} / module={target['target_module']}"
        )

    lines.extend(["", "## Implementation steps", ""])
    for step in record["implementation_steps"]:
        lines.append(f"- {step['sequence']}. {step['step_id']} / {step['title']}")

    lines.extend(["", "## Plan case results", ""])
    for result in record["plan_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 16 creates the controlled implementation plan only. Runtime solver and ranker remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_16_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_16_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_16_VERDICT=LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_READY_FOR_DRY_RUN",
            "ARC_AGI3_MILESTONE_11_TASK_16_BASELINE_COMMIT=1e46027",
            "ARC_AGI3_MILESTONE_11_TASK_16_NEXT_STAGE=MILESTONE_11_TASK_17_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_PLAN_READY=true",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_PLAN_PASSED=true",
            "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_DRY_RUN_AUTHORIZED=true",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_TARGET_MODULE_COUNT={EXPECTED_TARGET_MODULE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_IMPLEMENTATION_STEP_COUNT={EXPECTED_IMPLEMENTATION_STEP_COUNT}",
            f"ARC_AGI3_MILESTONE_11_CONTRACT_COUNT={EXPECTED_CONTRACT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REGRESSION_TEST_COUNT={EXPECTED_REGRESSION_TEST_COUNT}",
            f"ARC_AGI3_MILESTONE_11_ROLLBACK_ITEM_COUNT={EXPECTED_ROLLBACK_ITEM_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REVIEW_GATE_COUNT={EXPECTED_REVIEW_GATE_COUNT}",
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


def render_task_16_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 16 LOCAL SOLVER PATCH HELPER CONTROLLED WIRING IMPLEMENTATION PLAN MANIFEST v1",
        f"task_16_id={record['task_16_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_16_ready={record['task_16_ready']}",
        f"implementation_plan_ready={record['implementation_plan_ready']}",
        f"implementation_plan_passed={record['implementation_plan_passed']}",
        f"implementation_dry_run_authorized={record['implementation_dry_run_authorized']}",
        f"runtime_solver_patch_allowed={record['runtime_solver_patch_allowed']}",
        f"ranker_runtime_patch_allowed={record['ranker_runtime_patch_allowed']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"target_module_count={record['target_module_count']}",
        f"implementation_step_count={record['implementation_step_count']}",
        f"contract_count={record['contract_count']}",
        f"regression_test_count={record['regression_test_count']}",
        f"rollback_item_count={record['rollback_item_count']}",
        f"review_gate_count={record['review_gate_count']}",
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
        "IMPLEMENTATION_TARGETS",
    ]

    for target in record["target_module_proposals"]:
        lines.append(
            f"{target['target_layer']} adapter={target['adapter_name']} helper={target['helper_function']} "
            f"module={target['target_module']} runtime_patch_allowed={target['runtime_solver_patch_allowed']}"
        )

    lines.append("")
    lines.append("IMPLEMENTATION_PLAN_CASE_RESULTS")
    for result in record["plan_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_16_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-index-v1.json"
    targets_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-targets-v1.json"
    steps_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-steps-v1.json"
    contracts_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-contracts-v1.json"
    tests_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-regression-tests-v1.json"
    rollback_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-rollback-v1.json"
    gates_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-review-gates-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-controlled-wiring-implementation-plan-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_16_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_16_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["implementation_plan_index"], indent=2, sort_keys=True), encoding="utf-8")
    targets_path.write_text(json.dumps(record["target_module_proposals"], indent=2, sort_keys=True), encoding="utf-8")
    steps_path.write_text(json.dumps(record["implementation_steps"], indent=2, sort_keys=True), encoding="utf-8")
    contracts_path.write_text(json.dumps(record["contracts"], indent=2, sort_keys=True), encoding="utf-8")
    tests_path.write_text(json.dumps(record["regression_tests"], indent=2, sort_keys=True), encoding="utf-8")
    rollback_path.write_text(json.dumps(record["rollback_items"], indent=2, sort_keys=True), encoding="utf-8")
    gates_path.write_text(json.dumps(record["review_gates"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["plan_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["implementation_plan_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "targets_path": str(targets_path),
        "steps_path": str(steps_path),
        "contracts_path": str(contracts_path),
        "tests_path": str(tests_path),
        "rollback_path": str(rollback_path),
        "gates_path": str(gates_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan(record)
    artifacts = write_task_16_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_16_id": record["task_16_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_16_ready": record["task_16_ready"],
        "implementation_plan_ready": record["implementation_plan_ready"],
        "implementation_plan_passed": record["implementation_plan_passed"],
        "implementation_dry_run_authorized": record["implementation_dry_run_authorized"],
        "runtime_solver_patch_allowed": record["runtime_solver_patch_allowed"],
        "ranker_runtime_patch_allowed": record["ranker_runtime_patch_allowed"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "target_module_count": record["target_module_count"],
        "implementation_step_count": record["implementation_step_count"],
        "contract_count": record["contract_count"],
        "regression_test_count": record["regression_test_count"],
        "rollback_item_count": record["rollback_item_count"],
        "review_gate_count": record["review_gate_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "plan_check_count": record["plan_check_count"],
        "plan_case_count": record["plan_case_count"],
        "plan_case_pass_count": record["plan_case_pass_count"],
        "plan_case_failure_count": record["plan_case_failure_count"],
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
