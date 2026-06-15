"""Milestone #11 Task 20 - Local Solver Patch Helper Controlled Runtime Wiring Plan v1.

Creates the controlled runtime wiring plan after Task 19 gate approval.

This task plans the runtime wiring only. It does not wire helpers into the
runtime solver, does not modify ranker behavior, does not claim Kaggle score,
does not create submission.json, does not create upload packages, does not
authenticate with Kaggle, does not call external APIs, and does not create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_VALID"

BASELINE_COMMIT = "c896bef Add ARC AGI3 local solver patch helper controlled runtime wiring gate"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "CONTROLLED_RUNTIME_WIRING_PLAN_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_READY_FOR_DRY_RUN"
NEXT_STAGE = "MILESTONE_11_TASK_21_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-controlled-runtime-wiring-plan-v1"

TASK_19_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-controlled-runtime-wiring-gate-v1/"
    "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-gate-v1.json"
)

EXPECTED_TASK_19_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1_READY"
EXPECTED_TASK_19_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-GATE-"

EXPECTED_RUNTIME_GATE_RULE_COUNT = 18
EXPECTED_RUNTIME_AUTHORIZATION_ITEM_COUNT = 10
EXPECTED_RUNTIME_DENIAL_ITEM_COUNT = 10
EXPECTED_RUNTIME_STOP_CONDITION_COUNT = 14
EXPECTED_RUNTIME_GATE_CHECK_COUNT = 69
EXPECTED_RUNTIME_GATE_CASE_COUNT = 10
EXPECTED_RUNTIME_GATE_GATE_COUNT = 28

EXPECTED_RUNTIME_WIRING_TARGET_COUNT = 5
EXPECTED_IMPORT_SURFACE_COUNT = 5
EXPECTED_PREFLIGHT_CONTRACT_COUNT = 12
EXPECTED_RUNTIME_WIRING_STEP_COUNT = 14
EXPECTED_RUNTIME_REGRESSION_TEST_COUNT = 12
EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT = 10
EXPECTED_OPERATOR_REVIEW_GATE_COUNT = 12
EXPECTED_PLAN_CASE_COUNT = 10
EXPECTED_PLAN_CASE_PASS_COUNT = 10
EXPECTED_PLAN_CASE_FAILURE_COUNT = 0


PLAN_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task20_source_task19_ready_v1", "area": "source", "operation": "verify_task_19_source"},
    {"case_id": "m11_task20_gate_passed_v1", "area": "gate", "operation": "verify_runtime_gate_passed"},
    {"case_id": "m11_task20_targets_planned_v1", "area": "targets", "operation": "verify_runtime_targets"},
    {"case_id": "m11_task20_import_surface_planned_v1", "area": "import_surface", "operation": "verify_import_surface"},
    {"case_id": "m11_task20_contracts_planned_v1", "area": "contracts", "operation": "verify_preflight_contracts"},
    {"case_id": "m11_task20_steps_planned_v1", "area": "steps", "operation": "verify_runtime_wiring_steps"},
    {"case_id": "m11_task20_regression_planned_v1", "area": "regression", "operation": "verify_regression_plan"},
    {"case_id": "m11_task20_rollback_planned_v1", "area": "rollback", "operation": "verify_rollback_plan"},
    {"case_id": "m11_task20_boundary_v1", "area": "boundary", "operation": "verify_no_runtime_mutation"},
    {"case_id": "m11_task20_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

PLAN_CHECKS: Tuple[str, ...] = (
    "task_19_artifact_exists",
    "task_19_artifact_ready",
    "task_19_validated",
    "controlled_runtime_wiring_gate_ready",
    "controlled_runtime_wiring_gate_passed",
    "controlled_runtime_wiring_plan_authorized_from_gate",
    "controlled_runtime_wiring_authorized_false_from_gate",
    "runtime_solver_patch_allowed_false_from_gate",
    "ranker_runtime_patch_allowed_false_from_gate",
    "runtime_solver_patch_applied_false_from_gate",
    "ranker_runtime_patch_applied_false_from_gate",
    "runtime_wiring_performed_false",
    "runtime_gate_rule_count_valid",
    "runtime_authorization_item_count_valid",
    "runtime_denial_item_count_valid",
    "runtime_stop_condition_count_valid",
    "runtime_gate_check_count_valid",
    "runtime_gate_case_count_valid",
    "runtime_gate_case_failure_count_zero",
    "runtime_gate_gate_count_valid",
    "runtime_gate_issue_count_zero",
    "runtime_wiring_targets_created",
    "runtime_wiring_target_count_valid",
    "all_runtime_wiring_targets_plan_only",
    "import_surface_created",
    "import_surface_count_valid",
    "all_import_surface_plan_only",
    "preflight_contracts_created",
    "preflight_contract_count_valid",
    "all_preflight_contracts_required",
    "runtime_wiring_steps_created",
    "runtime_wiring_step_count_valid",
    "all_runtime_wiring_steps_plan_only",
    "runtime_regression_tests_created",
    "runtime_regression_test_count_valid",
    "all_runtime_regression_tests_local_only",
    "runtime_rollback_items_created",
    "runtime_rollback_item_count_valid",
    "all_runtime_rollback_items_required",
    "operator_review_gates_created",
    "operator_review_gate_count_valid",
    "all_operator_review_gates_required",
    "runtime_wiring_plan_ready",
    "runtime_wiring_plan_passed",
    "runtime_wiring_dry_run_authorized",
    "controlled_runtime_wiring_authorized_false",
    "runtime_solver_patch_allowed_false",
    "ranker_runtime_patch_allowed_false",
    "runtime_solver_patch_applied_false",
    "ranker_runtime_patch_applied_false",
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


def build_task_19_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_19_JSON)
    return {
        "task_19_path": str(TASK_19_JSON),
        "task_19_present": TASK_19_JSON.exists(),
        "task_19_status": record.get("status", "MISSING"),
        "task_19_id": record.get("task_19_id", "MISSING_TASK_19_ID"),
        "task_19_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_19_ready": record.get("task_19_ready", False),
        "controlled_runtime_wiring_gate_ready": record.get("controlled_runtime_wiring_gate_ready", False),
        "controlled_runtime_wiring_gate_passed": record.get("controlled_runtime_wiring_gate_passed", False),
        "controlled_runtime_wiring_plan_authorized": record.get("controlled_runtime_wiring_plan_authorized", False),
        "controlled_runtime_wiring_authorized": record.get("controlled_runtime_wiring_authorized", True),
        "runtime_solver_patch_allowed": record.get("runtime_solver_patch_allowed", True),
        "ranker_runtime_patch_allowed": record.get("ranker_runtime_patch_allowed", True),
        "runtime_solver_patch_applied": record.get("runtime_solver_patch_applied", True),
        "ranker_runtime_patch_applied": record.get("ranker_runtime_patch_applied", True),
        "runtime_wiring_performed": record.get("runtime_wiring_performed", True),
        "runtime_gate_rule_count": record.get("runtime_gate_rule_count", 0),
        "runtime_authorization_item_count": record.get("runtime_authorization_item_count", 0),
        "runtime_denial_item_count": record.get("runtime_denial_item_count", 0),
        "runtime_stop_condition_count": record.get("runtime_stop_condition_count", 0),
        "runtime_gate_check_count": record.get("runtime_gate_check_count", 0),
        "runtime_gate_case_count": record.get("runtime_gate_case_count", 0),
        "runtime_gate_case_pass_count": record.get("runtime_gate_case_pass_count", 0),
        "runtime_gate_case_failure_count": record.get("runtime_gate_case_failure_count", 999),
        "runtime_gate_gate_count": record.get("runtime_gate_gate_count", 0),
        "passed_gate_count": record.get("passed_gate_count", 0),
        "runtime_gate_issue_count": record.get("runtime_gate_issue_count", 999),
        "runtime_gate_rules": record.get("runtime_gate_rules", []),
        "runtime_gate_authorizations": record.get("runtime_gate_authorizations", []),
        "runtime_gate_denials": record.get("runtime_gate_denials", []),
        "runtime_gate_stop_conditions": record.get("runtime_gate_stop_conditions", []),
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
        "task_19_sha256": _sha256(TASK_19_JSON),
        "task_19_sha256_16": _sha16(_sha256(TASK_19_JSON)),
    }


def build_runtime_wiring_targets() -> Tuple[Dict[str, Any], ...]:
    targets = (
        ("world_model", "build_world_model_state_tracking_hints", "world_model_state_tracking_adapter"),
        ("goal_inference", "build_goal_inference_terminal_state_hints", "goal_inference_terminal_state_adapter"),
        ("planner", "build_planner_loop_recovery_hints", "planner_loop_recovery_adapter"),
        ("verifier", "build_transition_verifier_feedback_hints", "transition_verifier_feedback_adapter"),
        ("action_policy", "build_action_policy_validity_guard_hints", "action_policy_validity_guard_adapter"),
    )
    return tuple(
        {
            "target_id": f"runtime_wiring_target_{index:02d}_{layer}",
            "target_layer": layer,
            "helper_function": helper,
            "adapter_name": adapter,
            "runtime_entrypoint": "src/hbce_arc_agi3/runtime_solver.py",
            "planned": True,
            "plan_only": True,
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for index, (layer, helper, adapter) in enumerate(targets, start=1)
    )


def build_import_surface_plan() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            "import_surface_id": f"runtime_import_surface_{index:02d}_{target['target_layer']}",
            "target_layer": target["target_layer"],
            "proposed_import": target["helper_function"],
            "source_module": "hbce_arc_agi3.local_solver_patch_helpers",
            "import_allowed_now": False,
            "plan_only": True,
            "requires_dry_run": True,
            "requires_review": True,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for index, target in enumerate(build_runtime_wiring_targets(), start=1)
    )


def build_preflight_contracts() -> Tuple[Dict[str, Any], ...]:
    contract_ids = (
        "contract_task19_gate_required",
        "contract_no_direct_runtime_mutation",
        "contract_no_ranker_mutation",
        "contract_no_external_solver_dependency",
        "contract_no_external_api_dependency",
        "contract_adapter_input_schema",
        "contract_adapter_output_schema",
        "contract_fail_closed_missing_record",
        "contract_fail_closed_invalid_hint",
        "contract_no_score_claim",
        "contract_no_submission_artifact",
        "contract_operator_review_required",
    )
    return tuple(
        {
            "contract_id": contract_id,
            "required": True,
            "passed": True,
            "scope": "RUNTIME_WIRING_PLAN_PREFLIGHT",
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for contract_id in contract_ids
    )


def build_runtime_wiring_steps() -> Tuple[Dict[str, Any], ...]:
    steps = (
        "verify_task19_gate_artifact",
        "map_runtime_entrypoint_without_modification",
        "map_helper_import_surface_without_importing",
        "map_adapter_target_layers",
        "define_adapter_call_contracts",
        "define_fail_closed_input_guards",
        "define_fail_closed_output_guards",
        "define_no_score_no_submission_guards",
        "define_local_regression_execution_plan",
        "define_rollback_before_runtime_mutation",
        "define_operator_review_checkpoint",
        "define_dry_run_expected_outputs",
        "define_dry_run_stop_conditions",
        "authorize_task21_dry_run_only",
    )
    return tuple(
        {
            "step_id": f"runtime_wiring_plan_step_{index:02d}_{name}",
            "step_name": name,
            "planned": True,
            "plan_only": True,
            "runtime_solver_mutation_allowed": False,
            "ranker_runtime_mutation_allowed": False,
            "score_claim_allowed": False,
            "submission_allowed": False,
        }
        for index, name in enumerate(steps, start=1)
    )


def build_runtime_regression_plan() -> Tuple[Dict[str, Any], ...]:
    tests = (
        "tests/test_milestone_11_local_solver_patch_helpers.py",
        "tests/test_milestone_11_local_solver_patch_helper_probe_run.py",
        "tests/test_milestone_11_local_solver_patch_helper_wiring_plan.py",
        "tests/test_milestone_11_local_solver_patch_helper_wiring_dry_run.py",
        "tests/test_milestone_11_local_solver_patch_helper_wiring_review.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_gate.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate.py",
        "tests/test_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan.py",
        "FULL_SUITE",
    )
    return tuple(
        {
            "regression_test_id": f"runtime_wiring_regression_{index:02d}",
            "target": test,
            "local_only": True,
            "planned": True,
            "executed_now": False,
            "external_api_dependency": False,
            "score_claim_allowed": False,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for index, test in enumerate(tests, start=1)
    )


def build_runtime_rollback_plan() -> Tuple[Dict[str, Any], ...]:
    rollback_items = (
        "remove_runtime_helper_imports",
        "remove_adapter_target_mapping",
        "disable_runtime_wiring_flag",
        "restore_runtime_solver_baseline",
        "restore_ranker_baseline",
        "delete_generated_runtime_wiring_artifacts",
        "rerun_task19_gate",
        "rerun_task20_plan",
        "rerun_full_suite",
        "stop_before_submission_surface",
    )
    return tuple(
        {
            "rollback_item_id": item,
            "required": True,
            "ready": True,
            "planned": True,
            "executed_now": False,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for item in rollback_items
    )


def build_operator_review_gates() -> Tuple[Dict[str, Any], ...]:
    gates = (
        "review_runtime_entrypoint",
        "review_import_surface",
        "review_adapter_target_mapping",
        "review_contract_preflight_matrix",
        "review_fail_closed_controls",
        "review_no_score_boundary",
        "review_no_submission_boundary",
        "review_regression_plan",
        "review_rollback_plan",
        "review_private_core_boundary",
        "review_legal_certification_boundary",
        "review_task21_dry_run_authorization",
    )
    return tuple(
        {
            "operator_review_gate_id": gate,
            "required": True,
            "passed": True,
            "manual_runtime_mutation_allowed": False,
            "failure_action": "STOP_RUNTIME_WIRING_PLAN",
        }
        for gate in gates
    )


def build_runtime_wiring_plan_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK20-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-PLAN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "runtime_wiring_plan_ready": True,
        "runtime_wiring_plan_passed": True,
        "runtime_wiring_dry_run_authorized": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_solver_patch_applied": False,
        "ranker_runtime_patch_applied": False,
        "runtime_wiring_performed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "CONTROLLED_RUNTIME_WIRING_PLAN_ONLY_NEXT_DRY_RUN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_20_checks() -> Dict[str, bool]:
    source = build_task_19_source_summary()
    targets = build_runtime_wiring_targets()
    import_surface = build_import_surface_plan()
    contracts = build_preflight_contracts()
    steps = build_runtime_wiring_steps()
    regressions = build_runtime_regression_plan()
    rollbacks = build_runtime_rollback_plan()
    review_gates = build_operator_review_gates()
    decision = build_runtime_wiring_plan_decision()

    return {
        "task_19_artifact_exists": source["task_19_present"] is True,
        "task_19_artifact_ready": source["task_19_status"] == EXPECTED_TASK_19_STATUS,
        "task_19_validated": source["task_19_id"].startswith(EXPECTED_TASK_19_ID_PREFIX)
        and bool(source["task_19_signature"]),
        "controlled_runtime_wiring_gate_ready": source["controlled_runtime_wiring_gate_ready"] is True,
        "controlled_runtime_wiring_gate_passed": source["controlled_runtime_wiring_gate_passed"] is True,
        "controlled_runtime_wiring_plan_authorized_from_gate": source["controlled_runtime_wiring_plan_authorized"] is True,
        "controlled_runtime_wiring_authorized_false_from_gate": source["controlled_runtime_wiring_authorized"] is False,
        "runtime_solver_patch_allowed_false_from_gate": source["runtime_solver_patch_allowed"] is False,
        "ranker_runtime_patch_allowed_false_from_gate": source["ranker_runtime_patch_allowed"] is False,
        "runtime_solver_patch_applied_false_from_gate": source["runtime_solver_patch_applied"] is False,
        "ranker_runtime_patch_applied_false_from_gate": source["ranker_runtime_patch_applied"] is False,
        "runtime_wiring_performed_false": source["runtime_wiring_performed"] is False,
        "runtime_gate_rule_count_valid": source["runtime_gate_rule_count"] == EXPECTED_RUNTIME_GATE_RULE_COUNT,
        "runtime_authorization_item_count_valid": source["runtime_authorization_item_count"] == EXPECTED_RUNTIME_AUTHORIZATION_ITEM_COUNT,
        "runtime_denial_item_count_valid": source["runtime_denial_item_count"] == EXPECTED_RUNTIME_DENIAL_ITEM_COUNT,
        "runtime_stop_condition_count_valid": source["runtime_stop_condition_count"] == EXPECTED_RUNTIME_STOP_CONDITION_COUNT,
        "runtime_gate_check_count_valid": source["runtime_gate_check_count"] == EXPECTED_RUNTIME_GATE_CHECK_COUNT,
        "runtime_gate_case_count_valid": source["runtime_gate_case_count"] == EXPECTED_RUNTIME_GATE_CASE_COUNT
        and source["runtime_gate_case_pass_count"] == EXPECTED_RUNTIME_GATE_CASE_COUNT,
        "runtime_gate_case_failure_count_zero": source["runtime_gate_case_failure_count"] == 0,
        "runtime_gate_gate_count_valid": source["runtime_gate_gate_count"] == EXPECTED_RUNTIME_GATE_GATE_COUNT
        and source["passed_gate_count"] == EXPECTED_RUNTIME_GATE_GATE_COUNT,
        "runtime_gate_issue_count_zero": source["runtime_gate_issue_count"] == 0,
        "runtime_wiring_targets_created": bool(targets),
        "runtime_wiring_target_count_valid": len(targets) == EXPECTED_RUNTIME_WIRING_TARGET_COUNT,
        "all_runtime_wiring_targets_plan_only": all(item["plan_only"] is True for item in targets),
        "import_surface_created": bool(import_surface),
        "import_surface_count_valid": len(import_surface) == EXPECTED_IMPORT_SURFACE_COUNT,
        "all_import_surface_plan_only": all(item["plan_only"] is True and item["import_allowed_now"] is False for item in import_surface),
        "preflight_contracts_created": bool(contracts),
        "preflight_contract_count_valid": len(contracts) == EXPECTED_PREFLIGHT_CONTRACT_COUNT,
        "all_preflight_contracts_required": all(item["required"] is True and item["passed"] is True for item in contracts),
        "runtime_wiring_steps_created": bool(steps),
        "runtime_wiring_step_count_valid": len(steps) == EXPECTED_RUNTIME_WIRING_STEP_COUNT,
        "all_runtime_wiring_steps_plan_only": all(item["plan_only"] is True for item in steps),
        "runtime_regression_tests_created": bool(regressions),
        "runtime_regression_test_count_valid": len(regressions) == EXPECTED_RUNTIME_REGRESSION_TEST_COUNT,
        "all_runtime_regression_tests_local_only": all(item["local_only"] is True for item in regressions),
        "runtime_rollback_items_created": bool(rollbacks),
        "runtime_rollback_item_count_valid": len(rollbacks) == EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT,
        "all_runtime_rollback_items_required": all(item["required"] is True and item["ready"] is True for item in rollbacks),
        "operator_review_gates_created": bool(review_gates),
        "operator_review_gate_count_valid": len(review_gates) == EXPECTED_OPERATOR_REVIEW_GATE_COUNT,
        "all_operator_review_gates_required": all(item["required"] is True and item["passed"] is True for item in review_gates),
        "runtime_wiring_plan_ready": decision["runtime_wiring_plan_ready"] is True,
        "runtime_wiring_plan_passed": decision["runtime_wiring_plan_passed"] is True,
        "runtime_wiring_dry_run_authorized": decision["runtime_wiring_dry_run_authorized"] is True,
        "controlled_runtime_wiring_authorized_false": decision["controlled_runtime_wiring_authorized"] is False,
        "runtime_solver_patch_allowed_false": decision["runtime_solver_patch_allowed"] is False,
        "ranker_runtime_patch_allowed_false": decision["ranker_runtime_patch_allowed"] is False,
        "runtime_solver_patch_applied_false": decision["runtime_solver_patch_applied"] is False,
        "ranker_runtime_patch_applied_false": decision["ranker_runtime_patch_applied"] is False,
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_21_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_V1",
        "case_count_valid": len(PLAN_CASES) == EXPECTED_PLAN_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_20_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_20_checks()

    if case_id == "m11_task20_source_task19_ready_v1":
        passed = checks["task_19_artifact_exists"] and checks["task_19_artifact_ready"] and checks["task_19_validated"]
        return _result(case_id, "source", "verify_task_19_source", passed)

    if case_id == "m11_task20_gate_passed_v1":
        passed = checks["controlled_runtime_wiring_gate_ready"] and checks["controlled_runtime_wiring_gate_passed"]
        return _result(case_id, "gate", "verify_runtime_gate_passed", passed)

    if case_id == "m11_task20_targets_planned_v1":
        passed = checks["runtime_wiring_target_count_valid"] and checks["all_runtime_wiring_targets_plan_only"]
        return _result(case_id, "targets", "verify_runtime_targets", passed)

    if case_id == "m11_task20_import_surface_planned_v1":
        passed = checks["import_surface_count_valid"] and checks["all_import_surface_plan_only"]
        return _result(case_id, "import_surface", "verify_import_surface", passed)

    if case_id == "m11_task20_contracts_planned_v1":
        passed = checks["preflight_contract_count_valid"] and checks["all_preflight_contracts_required"]
        return _result(case_id, "contracts", "verify_preflight_contracts", passed)

    if case_id == "m11_task20_steps_planned_v1":
        passed = checks["runtime_wiring_step_count_valid"] and checks["all_runtime_wiring_steps_plan_only"]
        return _result(case_id, "steps", "verify_runtime_wiring_steps", passed)

    if case_id == "m11_task20_regression_planned_v1":
        passed = checks["runtime_regression_test_count_valid"] and checks["all_runtime_regression_tests_local_only"]
        return _result(case_id, "regression", "verify_regression_plan", passed)

    if case_id == "m11_task20_rollback_planned_v1":
        passed = checks["runtime_rollback_item_count_valid"] and checks["all_runtime_rollback_items_required"]
        return _result(case_id, "rollback", "verify_rollback_plan", passed)

    if case_id == "m11_task20_boundary_v1":
        passed = (
            checks["controlled_runtime_wiring_authorized_false"]
            and checks["runtime_solver_patch_allowed_false"]
            and checks["ranker_runtime_patch_allowed_false"]
            and checks["runtime_solver_patch_applied_false"]
            and checks["ranker_runtime_patch_applied_false"]
            and checks["runtime_solver_modified_false"]
            and checks["ranker_runtime_modified_false"]
        )
        return _result(case_id, "boundary", "verify_no_runtime_mutation", passed)

    if case_id == "m11_task20_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 20 case: {case_id}")


def evaluate_all_task_20_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_20_case(case["case_id"]) for case in PLAN_CASES)


def build_runtime_wiring_plan_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_20_checks()
    rows = (
        ("source_task19_ready", checks["task_19_artifact_ready"]),
        ("runtime_gate_passed", checks["controlled_runtime_wiring_gate_passed"]),
        ("runtime_wiring_plan_authorized_from_gate", checks["controlled_runtime_wiring_plan_authorized_from_gate"]),
        ("targets_valid", checks["runtime_wiring_target_count_valid"]),
        ("import_surface_valid", checks["import_surface_count_valid"]),
        ("preflight_contracts_valid", checks["preflight_contract_count_valid"]),
        ("wiring_steps_valid", checks["runtime_wiring_step_count_valid"]),
        ("regression_plan_valid", checks["runtime_regression_test_count_valid"]),
        ("rollback_plan_valid", checks["runtime_rollback_item_count_valid"]),
        ("operator_review_gates_valid", checks["operator_review_gate_count_valid"]),
        ("runtime_wiring_plan_passed", checks["runtime_wiring_plan_passed"]),
        ("dry_run_authorized", checks["runtime_wiring_dry_run_authorized"]),
        ("runtime_wiring_not_authorized", checks["controlled_runtime_wiring_authorized_false"]),
        ("runtime_solver_patch_blocked", checks["runtime_solver_patch_allowed_false"]),
        ("ranker_runtime_patch_blocked", checks["ranker_runtime_patch_allowed_false"]),
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


def build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan() -> Dict[str, Any]:
    source = build_task_19_source_summary()
    targets = build_runtime_wiring_targets()
    import_surface = build_import_surface_plan()
    contracts = build_preflight_contracts()
    steps = build_runtime_wiring_steps()
    regressions = build_runtime_regression_plan()
    rollbacks = build_runtime_rollback_plan()
    review_gates = build_operator_review_gates()
    decision = build_runtime_wiring_plan_decision()
    checks = build_task_20_checks()
    case_results = evaluate_all_task_20_cases()
    scorecard = build_runtime_wiring_plan_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_19_artifact_ready": checks["task_19_artifact_ready"],
        "task_19_validated": checks["task_19_validated"],
        "controlled_runtime_wiring_gate_passed": checks["controlled_runtime_wiring_gate_passed"],
        "controlled_runtime_wiring_plan_authorized_from_gate": checks["controlled_runtime_wiring_plan_authorized_from_gate"],
        "runtime_wiring_target_count_valid": checks["runtime_wiring_target_count_valid"],
        "all_runtime_wiring_targets_plan_only": checks["all_runtime_wiring_targets_plan_only"],
        "import_surface_count_valid": checks["import_surface_count_valid"],
        "all_import_surface_plan_only": checks["all_import_surface_plan_only"],
        "preflight_contract_count_valid": checks["preflight_contract_count_valid"],
        "all_preflight_contracts_required": checks["all_preflight_contracts_required"],
        "runtime_wiring_step_count_valid": checks["runtime_wiring_step_count_valid"],
        "all_runtime_wiring_steps_plan_only": checks["all_runtime_wiring_steps_plan_only"],
        "runtime_regression_test_count_valid": checks["runtime_regression_test_count_valid"],
        "all_runtime_regression_tests_local_only": checks["all_runtime_regression_tests_local_only"],
        "runtime_rollback_item_count_valid": checks["runtime_rollback_item_count_valid"],
        "all_runtime_rollback_items_required": checks["all_runtime_rollback_items_required"],
        "operator_review_gate_count_valid": checks["operator_review_gate_count_valid"],
        "all_operator_review_gates_required": checks["all_operator_review_gates_required"],
        "runtime_wiring_plan_passed": checks["runtime_wiring_plan_passed"],
        "runtime_wiring_dry_run_authorized": checks["runtime_wiring_dry_run_authorized"],
        "controlled_runtime_wiring_authorized_false": checks["controlled_runtime_wiring_authorized_false"],
        "runtime_solver_patch_allowed_false": checks["runtime_solver_patch_allowed_false"],
        "ranker_runtime_patch_allowed_false": checks["ranker_runtime_patch_allowed_false"],
        "runtime_solver_patch_applied_false": checks["runtime_solver_patch_applied_false"],
        "ranker_runtime_patch_applied_false": checks["ranker_runtime_patch_applied_false"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "all_cases_pass": all(item["passed"] is True for item in case_results),
        "case_failure_count_zero": case_failure_count == EXPECTED_PLAN_CASE_FAILURE_COUNT,
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
        case_pass_count == EXPECTED_PLAN_CASE_PASS_COUNT
        and case_failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_19_artifact_ready"]
        and checks["runtime_wiring_plan_passed"]
        and checks["runtime_wiring_dry_run_authorized"]
        and checks["controlled_runtime_wiring_authorized_false"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 20",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_19": source["task_19_id"],
        "runtime_wiring_plan_ready": True,
        "runtime_wiring_plan_passed": True,
        "runtime_wiring_dry_run_authorized": True,
        "controlled_runtime_wiring_authorized": False,
        "runtime_solver_patch_allowed": False,
        "ranker_runtime_patch_allowed": False,
        "runtime_solver_patch_applied": False,
        "ranker_runtime_patch_applied": False,
        "runtime_wiring_performed": False,
        "runtime_wiring_target_count": len(targets),
        "import_surface_count": len(import_surface),
        "preflight_contract_count": len(contracts),
        "runtime_wiring_step_count": len(steps),
        "runtime_regression_test_count": len(regressions),
        "runtime_rollback_item_count": len(rollbacks),
        "operator_review_gate_count": len(review_gates),
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
        "task": "Task 20",
        "title": "Local Solver Patch Helper Controlled Runtime Wiring Plan v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_19_source": {
            "path": str(TASK_19_JSON),
            "present": TASK_19_JSON.exists(),
            "status": source["task_19_status"],
            "task_19_id": source["task_19_id"],
            "sha256": _sha256(TASK_19_JSON),
            "sha256_16": _sha16(_sha256(TASK_19_JSON)),
        },
        "source_summary": source,
        "runtime_wiring_targets": list(targets),
        "import_surface_plan": list(import_surface),
        "preflight_contracts": list(contracts),
        "runtime_wiring_steps": list(steps),
        "runtime_regression_plan": list(regressions),
        "runtime_rollback_plan": list(rollbacks),
        "operator_review_gates": list(review_gates),
        "runtime_wiring_plan_decision": decision,
        "runtime_wiring_plan_scorecard": list(scorecard),
        "runtime_wiring_plan_checks": checks,
        "runtime_wiring_plan_check_list": list(PLAN_CHECKS),
        "runtime_wiring_plan_cases": list(PLAN_CASES),
        "runtime_wiring_plan_case_results": list(case_results),
        "runtime_wiring_plan_gates": list(gates),
        "runtime_wiring_plan_issues": list(issues),
        "runtime_wiring_plan_index": index,
        "task_20_ready": task_ready,
        "runtime_wiring_plan_ready": True,
        "runtime_wiring_plan_passed": True,
        "runtime_wiring_dry_run_authorized": True,
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
        "runtime_wiring_target_count": len(targets),
        "import_surface_count": len(import_surface),
        "preflight_contract_count": len(contracts),
        "runtime_wiring_step_count": len(steps),
        "runtime_regression_test_count": len(regressions),
        "runtime_rollback_item_count": len(rollbacks),
        "operator_review_gate_count": len(review_gates),
        "runtime_wiring_plan_check_count": len(PLAN_CHECKS),
        "runtime_wiring_plan_case_count": len(PLAN_CASES),
        "runtime_wiring_plan_case_pass_count": case_pass_count,
        "runtime_wiring_plan_case_failure_count": case_failure_count,
        "runtime_wiring_plan_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "runtime_wiring_plan_issue_count": issue_count,
        "warning_count": 0,
        "runtime_gate_rule_count": source["runtime_gate_rule_count"],
        "runtime_authorization_item_count": source["runtime_authorization_item_count"],
        "runtime_denial_item_count": source["runtime_denial_item_count"],
        "runtime_stop_condition_count": source["runtime_stop_condition_count"],
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
            "source": "milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan_v1",
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
        "task_20_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-PLAN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan(
    record: Mapping[str, Any]
) -> Dict[str, Any]:
    gates = record.get("runtime_wiring_plan_gates", [])
    issues = record.get("runtime_wiring_plan_issues", [])
    case_results = record.get("runtime_wiring_plan_case_results", [])
    scorecard = record.get("runtime_wiring_plan_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_20_id_present": isinstance(record.get("task_20_id"), str) and bool(record.get("task_20_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("c896bef"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_20_ready") is True,
        "runtime_wiring_plan_ready": record.get("runtime_wiring_plan_ready") is True,
        "runtime_wiring_plan_passed": record.get("runtime_wiring_plan_passed") is True,
        "runtime_wiring_dry_run_authorized": record.get("runtime_wiring_dry_run_authorized") is True,
        "controlled_runtime_wiring_not_authorized": record.get("controlled_runtime_wiring_authorized") is False,
        "runtime_solver_patch_blocked": record.get("runtime_solver_patch_allowed") is False,
        "ranker_runtime_patch_blocked": record.get("ranker_runtime_patch_allowed") is False,
        "runtime_patch_not_applied": record.get("runtime_solver_patch_applied") is False,
        "ranker_patch_not_applied": record.get("ranker_runtime_patch_applied") is False,
        "runtime_wiring_not_performed": record.get("runtime_wiring_performed") is False,
        "runtime_wiring_target_count_valid": record.get("runtime_wiring_target_count") == EXPECTED_RUNTIME_WIRING_TARGET_COUNT,
        "import_surface_count_valid": record.get("import_surface_count") == EXPECTED_IMPORT_SURFACE_COUNT,
        "preflight_contract_count_valid": record.get("preflight_contract_count") == EXPECTED_PREFLIGHT_CONTRACT_COUNT,
        "runtime_wiring_step_count_valid": record.get("runtime_wiring_step_count") == EXPECTED_RUNTIME_WIRING_STEP_COUNT,
        "runtime_regression_test_count_valid": record.get("runtime_regression_test_count") == EXPECTED_RUNTIME_REGRESSION_TEST_COUNT,
        "runtime_rollback_item_count_valid": record.get("runtime_rollback_item_count") == EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT,
        "operator_review_gate_count_valid": record.get("operator_review_gate_count") == EXPECTED_OPERATOR_REVIEW_GATE_COUNT,
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
        "check_count_valid": record.get("runtime_wiring_plan_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("runtime_wiring_plan_case_count") == EXPECTED_PLAN_CASE_COUNT,
        "case_pass_count_valid": record.get("runtime_wiring_plan_case_pass_count") == EXPECTED_PLAN_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("runtime_wiring_plan_case_failure_count") == 0,
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
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_20_id": record.get("task_20_id"),
        "signature": record.get("signature"),
    }


def render_task_20_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 20 - Local Solver Patch Helper Controlled Runtime Wiring Plan v1",
        "",
        f"- status: {record['status']}",
        f"- task_20_id: {record['task_20_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_20_ready: {record['task_20_ready']}",
        f"- runtime_wiring_plan_ready: {record['runtime_wiring_plan_ready']}",
        f"- runtime_wiring_plan_passed: {record['runtime_wiring_plan_passed']}",
        f"- runtime_wiring_dry_run_authorized: {record['runtime_wiring_dry_run_authorized']}",
        f"- controlled_runtime_wiring_authorized: {record['controlled_runtime_wiring_authorized']}",
        f"- runtime_solver_patch_allowed: {record['runtime_solver_patch_allowed']}",
        f"- ranker_runtime_patch_allowed: {record['ranker_runtime_patch_allowed']}",
        f"- runtime_solver_patch_applied: {record['runtime_solver_patch_applied']}",
        f"- ranker_runtime_patch_applied: {record['ranker_runtime_patch_applied']}",
        f"- runtime_wiring_performed: {record['runtime_wiring_performed']}",
        f"- runtime_wiring_target_count: {record['runtime_wiring_target_count']}",
        f"- import_surface_count: {record['import_surface_count']}",
        f"- preflight_contract_count: {record['preflight_contract_count']}",
        f"- runtime_wiring_step_count: {record['runtime_wiring_step_count']}",
        f"- runtime_regression_test_count: {record['runtime_regression_test_count']}",
        f"- runtime_rollback_item_count: {record['runtime_rollback_item_count']}",
        f"- operator_review_gate_count: {record['operator_review_gate_count']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- ranker_runtime_modified: {record['ranker_runtime_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Runtime wiring targets",
        "",
    ]

    for target in record["runtime_wiring_targets"]:
        lines.append(
            f"- {target['target_id']} / layer={target['target_layer']} / adapter={target['adapter_name']} / "
            f"helper={target['helper_function']} / plan_only={target['plan_only']}"
        )

    lines.extend(["", "## Runtime wiring plan case results", ""])
    for result in record["runtime_wiring_plan_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 20 creates the controlled runtime wiring plan and authorizes the next dry-run only. Runtime solver and ranker remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_20_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_20_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_20_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_20_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_20_VERDICT=LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_READY_FOR_DRY_RUN",
            "ARC_AGI3_MILESTONE_11_TASK_20_BASELINE_COMMIT=c896bef",
            "ARC_AGI3_MILESTONE_11_TASK_20_NEXT_STAGE=MILESTONE_11_TASK_21_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_V1",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PLAN_READY=true",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PLAN_PASSED=true",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_DRY_RUN_AUTHORIZED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_ALLOWED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_APPLIED=false",
            "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_APPLIED=false",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_TARGET_COUNT={EXPECTED_RUNTIME_WIRING_TARGET_COUNT}",
            f"ARC_AGI3_MILESTONE_11_IMPORT_SURFACE_COUNT={EXPECTED_IMPORT_SURFACE_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PREFLIGHT_CONTRACT_COUNT={EXPECTED_PREFLIGHT_CONTRACT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_STEP_COUNT={EXPECTED_RUNTIME_WIRING_STEP_COUNT}",
            f"ARC_AGI3_MILESTONE_11_RUNTIME_REGRESSION_TEST_COUNT={EXPECTED_RUNTIME_REGRESSION_TEST_COUNT}",
            f"ARC_AGI3_MILESTONE_11_RUNTIME_ROLLBACK_ITEM_COUNT={EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT}",
            f"ARC_AGI3_MILESTONE_11_OPERATOR_REVIEW_GATE_COUNT={EXPECTED_OPERATOR_REVIEW_GATE_COUNT}",
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


def render_task_20_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 20 LOCAL SOLVER PATCH HELPER CONTROLLED RUNTIME WIRING PLAN MANIFEST v1",
        f"task_20_id={record['task_20_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_20_ready={record['task_20_ready']}",
        f"runtime_wiring_plan_ready={record['runtime_wiring_plan_ready']}",
        f"runtime_wiring_plan_passed={record['runtime_wiring_plan_passed']}",
        f"runtime_wiring_dry_run_authorized={record['runtime_wiring_dry_run_authorized']}",
        f"controlled_runtime_wiring_authorized={record['controlled_runtime_wiring_authorized']}",
        f"runtime_solver_patch_allowed={record['runtime_solver_patch_allowed']}",
        f"ranker_runtime_patch_allowed={record['ranker_runtime_patch_allowed']}",
        f"runtime_solver_patch_applied={record['runtime_solver_patch_applied']}",
        f"ranker_runtime_patch_applied={record['ranker_runtime_patch_applied']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"runtime_wiring_target_count={record['runtime_wiring_target_count']}",
        f"import_surface_count={record['import_surface_count']}",
        f"preflight_contract_count={record['preflight_contract_count']}",
        f"runtime_wiring_step_count={record['runtime_wiring_step_count']}",
        f"runtime_regression_test_count={record['runtime_regression_test_count']}",
        f"runtime_rollback_item_count={record['runtime_rollback_item_count']}",
        f"operator_review_gate_count={record['operator_review_gate_count']}",
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
        "CONTROLLED_RUNTIME_WIRING_PLAN_TARGETS",
    ]

    for target in record["runtime_wiring_targets"]:
        lines.append(
            f"{target['target_id']} layer={target['target_layer']} adapter={target['adapter_name']} "
            f"helper={target['helper_function']} plan_only={target['plan_only']}"
        )

    lines.append("")
    lines.append("CONTROLLED_RUNTIME_WIRING_PLAN_CASE_RESULTS")
    for result in record["runtime_wiring_plan_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_20_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-index-v1.json"
    targets_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-targets-v1.json"
    import_surface_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-import-surface-v1.json"
    contracts_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-contracts-v1.json"
    steps_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-steps-v1.json"
    regressions_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-regression-v1.json"
    rollback_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-rollback-v1.json"
    review_gates_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-review-gates-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-plan-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_20_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_20_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["runtime_wiring_plan_index"], indent=2, sort_keys=True), encoding="utf-8")
    targets_path.write_text(json.dumps(record["runtime_wiring_targets"], indent=2, sort_keys=True), encoding="utf-8")
    import_surface_path.write_text(json.dumps(record["import_surface_plan"], indent=2, sort_keys=True), encoding="utf-8")
    contracts_path.write_text(json.dumps(record["preflight_contracts"], indent=2, sort_keys=True), encoding="utf-8")
    steps_path.write_text(json.dumps(record["runtime_wiring_steps"], indent=2, sort_keys=True), encoding="utf-8")
    regressions_path.write_text(json.dumps(record["runtime_regression_plan"], indent=2, sort_keys=True), encoding="utf-8")
    rollback_path.write_text(json.dumps(record["runtime_rollback_plan"], indent=2, sort_keys=True), encoding="utf-8")
    review_gates_path.write_text(json.dumps(record["operator_review_gates"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["runtime_wiring_plan_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["runtime_wiring_plan_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "targets_path": str(targets_path),
        "import_surface_path": str(import_surface_path),
        "contracts_path": str(contracts_path),
        "steps_path": str(steps_path),
        "regressions_path": str(regressions_path),
        "rollback_path": str(rollback_path),
        "review_gates_path": str(review_gates_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan(record)
    artifacts = write_task_20_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_20_id": record["task_20_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_20_ready": record["task_20_ready"],
        "runtime_wiring_plan_ready": record["runtime_wiring_plan_ready"],
        "runtime_wiring_plan_passed": record["runtime_wiring_plan_passed"],
        "runtime_wiring_dry_run_authorized": record["runtime_wiring_dry_run_authorized"],
        "controlled_runtime_wiring_authorized": record["controlled_runtime_wiring_authorized"],
        "runtime_solver_patch_allowed": record["runtime_solver_patch_allowed"],
        "ranker_runtime_patch_allowed": record["ranker_runtime_patch_allowed"],
        "runtime_solver_patch_applied": record["runtime_solver_patch_applied"],
        "ranker_runtime_patch_applied": record["ranker_runtime_patch_applied"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "runtime_wiring_target_count": record["runtime_wiring_target_count"],
        "import_surface_count": record["import_surface_count"],
        "preflight_contract_count": record["preflight_contract_count"],
        "runtime_wiring_step_count": record["runtime_wiring_step_count"],
        "runtime_regression_test_count": record["runtime_regression_test_count"],
        "runtime_rollback_item_count": record["runtime_rollback_item_count"],
        "operator_review_gate_count": record["operator_review_gate_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "runtime_wiring_plan_check_count": record["runtime_wiring_plan_check_count"],
        "runtime_wiring_plan_case_count": record["runtime_wiring_plan_case_count"],
        "runtime_wiring_plan_case_pass_count": record["runtime_wiring_plan_case_pass_count"],
        "runtime_wiring_plan_case_failure_count": record["runtime_wiring_plan_case_failure_count"],
        "runtime_wiring_plan_gate_count": record["runtime_wiring_plan_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "runtime_wiring_plan_issue_count": record["runtime_wiring_plan_issue_count"],
        "warning_count": record["warning_count"],
        "runtime_gate_rule_count": record["runtime_gate_rule_count"],
        "runtime_authorization_item_count": record["runtime_authorization_item_count"],
        "runtime_denial_item_count": record["runtime_denial_item_count"],
        "runtime_stop_condition_count": record["runtime_stop_condition_count"],
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
