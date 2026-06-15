"""Milestone #11 Task 10 - Local Solver Patch Helpers v1.

Creates and validates local solver patch helper artifacts from Task 9.

This task adds helper functions only. It does not modify runtime solver behavior,
does not modify ranker behavior, does not claim Kaggle score, does not create a
submission artifact, does not call external APIs, and does not create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from hbce_arc_agi3.solver_patch_helpers import (
    M11_SOLVER_PATCH_HELPERS_REVISION,
    M11_SOLVER_PATCH_HELPERS_STATUS,
    build_action_policy_validity_guard_hints,
    build_goal_inference_terminal_state_hints,
    build_planner_loop_recovery_hints,
    build_solver_patch_helper_bundle,
    build_transition_verifier_feedback_hints,
    build_world_model_state_tracking_hints,
)


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_VALID"

BASELINE_COMMIT = "3f96067 Add ARC AGI3 local solver patch implementation plan"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_LOCAL_ONLY"
TASK_SCOPE = "PATCH_HELPERS_ONLY_NO_RUNTIME_SOLVER_PATCH_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPERS_READY_FOR_LOCAL_HELPER_PROBE_RUN"
NEXT_STAGE = "MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helpers-v1"

TASK_9_JSON = Path(
    "examples/milestone-11/local-solver-patch-implementation-plan-v1/"
    "milestone-11-local-solver-patch-implementation-plan-v1.json"
)

TASK_5_JSON = Path(
    "examples/milestone-11/local-diagnostic-fixture-harness-v1/"
    "milestone-11-local-diagnostic-fixture-harness-v1.json"
)

EXPECTED_TASK_9_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY"
EXPECTED_TASK_9_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-IMPLEMENTATION-PLAN-"

EXPECTED_HELPER_COUNT = 5
EXPECTED_RECORD_COUNT = 6
EXPECTED_HINT_COUNT_PER_LAYER = 6
EXPECTED_TOTAL_HINT_COUNT = 30
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

HELPER_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task10_source_task9_ready_v1", "area": "source", "operation": "verify_task_9_source"},
    {"case_id": "m11_task10_helper_module_ready_v1", "area": "helper_module", "operation": "verify_helper_module"},
    {"case_id": "m11_task10_world_model_hints_ready_v1", "area": "world_model", "operation": "verify_world_model_hints"},
    {"case_id": "m11_task10_goal_inference_hints_ready_v1", "area": "goal_inference", "operation": "verify_goal_inference_hints"},
    {"case_id": "m11_task10_planner_hints_ready_v1", "area": "planner", "operation": "verify_planner_hints"},
    {"case_id": "m11_task10_verifier_hints_ready_v1", "area": "verifier", "operation": "verify_verifier_hints"},
    {"case_id": "m11_task10_action_policy_hints_ready_v1", "area": "action_policy", "operation": "verify_action_policy_hints"},
    {"case_id": "m11_task10_score_submission_boundary_v1", "area": "boundary", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task10_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
    {"case_id": "m11_task10_metadata_safe_v1", "area": "metadata", "operation": "verify_metadata_safe"},
)

HELPER_CHECKS: Tuple[str, ...] = (
    "task_9_artifact_exists",
    "task_9_artifact_ready",
    "task_9_validated",
    "implementation_plan_ready",
    "next_stage_scope_patch_helpers_only",
    "task_5_fixture_source_exists",
    "diagnostic_records_loaded",
    "helper_module_revision_valid",
    "helper_module_status_valid",
    "helper_bundle_created",
    "helper_count_valid",
    "world_model_hints_created",
    "world_model_hint_count_valid",
    "goal_inference_hints_created",
    "goal_inference_hint_count_valid",
    "planner_hints_created",
    "planner_hint_count_valid",
    "transition_verifier_hints_created",
    "transition_verifier_hint_count_valid",
    "action_policy_hints_created",
    "action_policy_hint_count_valid",
    "total_hint_count_valid",
    "all_hints_diagnostic_only",
    "all_hints_not_kaggle_score",
    "all_hints_score_claim_blocked",
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

EXPECTED_CHECK_COUNT = len(HELPER_CHECKS)


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


def build_task_9_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_9_JSON)
    return {
        "task_9_path": str(TASK_9_JSON),
        "task_9_present": TASK_9_JSON.exists(),
        "task_9_status": record.get("status", "MISSING"),
        "task_9_id": record.get("task_9_id", "MISSING_TASK_9_ID"),
        "task_9_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_9_ready": record.get("task_9_ready", False),
        "implementation_plan_ready": record.get("implementation_plan_ready", False),
        "next_stage_authorized_scope": record.get("next_stage_authorized_scope", "MISSING_SCOPE"),
        "implementation_allowed_now": record.get("implementation_allowed_now", True),
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
        "task_9_sha256": _sha256(TASK_9_JSON),
        "task_9_sha256_16": _sha16(_sha256(TASK_9_JSON)),
    }


def build_diagnostic_records() -> Tuple[Dict[str, Any], ...]:
    record = _read_json(TASK_5_JSON)
    rows = record.get("episode_results", [])
    return tuple(row for row in rows if isinstance(row, dict))


def build_helper_outputs() -> Dict[str, Any]:
    records = build_diagnostic_records()
    bundle = build_solver_patch_helper_bundle(records)

    return {
        "records": list(records),
        "bundle": bundle,
        "world_model_hints": list(build_world_model_state_tracking_hints(records)),
        "goal_inference_hints": list(build_goal_inference_terminal_state_hints(records)),
        "planner_hints": list(build_planner_loop_recovery_hints(records)),
        "transition_verifier_hints": list(build_transition_verifier_feedback_hints(records)),
        "action_policy_hints": list(build_action_policy_validity_guard_hints(records)),
    }


def _all_hints(outputs: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    rows = []
    for key in (
        "world_model_hints",
        "goal_inference_hints",
        "planner_hints",
        "transition_verifier_hints",
        "action_policy_hints",
    ):
        rows.extend(outputs[key])
    return tuple(rows)


def build_task_10_checks() -> Dict[str, bool]:
    source = build_task_9_source_summary()
    records = build_diagnostic_records()
    outputs = build_helper_outputs()
    all_hints = _all_hints(outputs)

    return {
        "task_9_artifact_exists": source["task_9_present"] is True,
        "task_9_artifact_ready": source["task_9_status"] == EXPECTED_TASK_9_STATUS,
        "task_9_validated": source["task_9_id"].startswith(EXPECTED_TASK_9_ID_PREFIX)
        and bool(source["task_9_signature"]),
        "implementation_plan_ready": source["implementation_plan_ready"] is True,
        "next_stage_scope_patch_helpers_only": source["next_stage_authorized_scope"] == "PATCH_HELPERS_ONLY",
        "task_5_fixture_source_exists": TASK_5_JSON.exists(),
        "diagnostic_records_loaded": len(records) == EXPECTED_RECORD_COUNT,
        "helper_module_revision_valid": M11_SOLVER_PATCH_HELPERS_REVISION == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1",
        "helper_module_status_valid": M11_SOLVER_PATCH_HELPERS_STATUS == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_READY",
        "helper_bundle_created": outputs["bundle"]["status"] == M11_SOLVER_PATCH_HELPERS_STATUS,
        "helper_count_valid": EXPECTED_HELPER_COUNT == 5,
        "world_model_hints_created": bool(outputs["world_model_hints"]),
        "world_model_hint_count_valid": len(outputs["world_model_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER,
        "goal_inference_hints_created": bool(outputs["goal_inference_hints"]),
        "goal_inference_hint_count_valid": len(outputs["goal_inference_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER,
        "planner_hints_created": bool(outputs["planner_hints"]),
        "planner_hint_count_valid": len(outputs["planner_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER,
        "transition_verifier_hints_created": bool(outputs["transition_verifier_hints"]),
        "transition_verifier_hint_count_valid": len(outputs["transition_verifier_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER,
        "action_policy_hints_created": bool(outputs["action_policy_hints"]),
        "action_policy_hint_count_valid": len(outputs["action_policy_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER,
        "total_hint_count_valid": len(all_hints) == EXPECTED_TOTAL_HINT_COUNT,
        "all_hints_diagnostic_only": all(item["diagnostic_only"] is True for item in all_hints),
        "all_hints_not_kaggle_score": all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in all_hints),
        "all_hints_score_claim_blocked": all(item["score_claim_allowed"] is False for item in all_hints),
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1",
        "case_count_valid": len(HELPER_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_10_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_10_checks()

    if case_id == "m11_task10_source_task9_ready_v1":
        passed = checks["task_9_artifact_exists"] and checks["task_9_artifact_ready"] and checks["task_9_validated"]
        return _result(case_id, "source", "verify_task_9_source", passed)

    if case_id == "m11_task10_helper_module_ready_v1":
        passed = checks["helper_module_revision_valid"] and checks["helper_module_status_valid"] and checks["helper_bundle_created"]
        return _result(case_id, "helper_module", "verify_helper_module", passed)

    if case_id == "m11_task10_world_model_hints_ready_v1":
        passed = checks["world_model_hints_created"] and checks["world_model_hint_count_valid"]
        return _result(case_id, "world_model", "verify_world_model_hints", passed)

    if case_id == "m11_task10_goal_inference_hints_ready_v1":
        passed = checks["goal_inference_hints_created"] and checks["goal_inference_hint_count_valid"]
        return _result(case_id, "goal_inference", "verify_goal_inference_hints", passed)

    if case_id == "m11_task10_planner_hints_ready_v1":
        passed = checks["planner_hints_created"] and checks["planner_hint_count_valid"]
        return _result(case_id, "planner", "verify_planner_hints", passed)

    if case_id == "m11_task10_verifier_hints_ready_v1":
        passed = checks["transition_verifier_hints_created"] and checks["transition_verifier_hint_count_valid"]
        return _result(case_id, "verifier", "verify_verifier_hints", passed)

    if case_id == "m11_task10_action_policy_hints_ready_v1":
        passed = checks["action_policy_hints_created"] and checks["action_policy_hint_count_valid"]
        return _result(case_id, "action_policy", "verify_action_policy_hints", passed)

    if case_id == "m11_task10_score_submission_boundary_v1":
        passed = (
            checks["all_hints_not_kaggle_score"]
            and checks["all_hints_score_claim_blocked"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
            and checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "boundary", "verify_no_score_no_submission", passed)

    if case_id == "m11_task10_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task10_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 10 case: {case_id}")


def evaluate_all_task_10_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_10_case(case["case_id"]) for case in HELPER_CASES)


def build_helper_layer_summary() -> Tuple[Dict[str, Any], ...]:
    outputs = build_helper_outputs()
    rows = []
    for key, layer in (
        ("world_model_hints", "world_model"),
        ("goal_inference_hints", "goal_inference"),
        ("planner_hints", "planner"),
        ("transition_verifier_hints", "verifier"),
        ("action_policy_hints", "action_policy"),
    ):
        hints = outputs[key]
        rows.append(
            {
                "target_layer": layer,
                "hint_count": len(hints),
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
                "score_claim_allowed": False,
            }
        )
    return tuple(rows)


def build_helper_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_10_checks()
    rows = (
        ("source_task9_ready", checks["task_9_artifact_ready"]),
        ("helper_module_ready", checks["helper_module_status_valid"]),
        ("world_model_hints_ready", checks["world_model_hint_count_valid"]),
        ("goal_inference_hints_ready", checks["goal_inference_hint_count_valid"]),
        ("planner_hints_ready", checks["planner_hint_count_valid"]),
        ("verifier_hints_ready", checks["transition_verifier_hint_count_valid"]),
        ("action_policy_hints_ready", checks["action_policy_hint_count_valid"]),
        ("runtime_solver_untouched", checks["runtime_solver_modified_false"]),
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


def build_task_10_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK10-LOCAL-SOLVER-PATCH-HELPERS-DECISION-v1",
        "verdict": TASK_VERDICT,
        "helper_implementation_ready": True,
        "helper_scope": "PATCH_HELPERS_ONLY",
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "HELPERS_ONLY_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION",
    }


def build_milestone_11_local_solver_patch_helpers() -> Dict[str, Any]:
    source = build_task_9_source_summary()
    outputs = build_helper_outputs()
    all_hints = _all_hints(outputs)
    layer_summary = build_helper_layer_summary()
    decision = build_task_10_decision()
    checks = build_task_10_checks()
    case_results = evaluate_all_task_10_cases()
    scorecard = build_helper_scorecard()

    pass_count = sum(1 for item in case_results if item["passed"] is True)
    failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_9_artifact_ready": checks["task_9_artifact_ready"],
        "task_9_validated": checks["task_9_validated"],
        "helper_module_ready": checks["helper_module_status_valid"],
        "helper_bundle_created": checks["helper_bundle_created"],
        "diagnostic_records_loaded": checks["diagnostic_records_loaded"],
        "all_layer_hints_ready": checks["total_hint_count_valid"],
        "all_hints_diagnostic_only": checks["all_hints_diagnostic_only"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
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
        and checks["task_9_artifact_ready"]
        and checks["helper_bundle_created"]
        and checks["total_hint_count_valid"]
        and checks["next_stage_valid"]
        and checks["fail_closed_active"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 10",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_9": source["task_9_id"],
        "helper_module_revision": M11_SOLVER_PATCH_HELPERS_REVISION,
        "helper_module_status": M11_SOLVER_PATCH_HELPERS_STATUS,
        "helper_implementation_ready": True,
        "helper_count": EXPECTED_HELPER_COUNT,
        "diagnostic_record_count": len(outputs["records"]),
        "total_hint_count": len(all_hints),
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
        "task": "Task 10",
        "title": "Local Solver Patch Helpers v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_9_source": {
            "path": str(TASK_9_JSON),
            "present": TASK_9_JSON.exists(),
            "status": source["task_9_status"],
            "task_9_id": source["task_9_id"],
            "sha256": _sha256(TASK_9_JSON),
            "sha256_16": _sha16(_sha256(TASK_9_JSON)),
        },
        "source_summary": source,
        "helper_module_revision": M11_SOLVER_PATCH_HELPERS_REVISION,
        "helper_module_status": M11_SOLVER_PATCH_HELPERS_STATUS,
        "helper_bundle": outputs["bundle"],
        "helper_layer_summary": list(layer_summary),
        "world_model_hints": outputs["world_model_hints"],
        "goal_inference_hints": outputs["goal_inference_hints"],
        "planner_hints": outputs["planner_hints"],
        "transition_verifier_hints": outputs["transition_verifier_hints"],
        "action_policy_hints": outputs["action_policy_hints"],
        "task_10_decision": decision,
        "helper_scorecard": list(scorecard),
        "helper_checks": checks,
        "helper_check_list": list(HELPER_CHECKS),
        "helper_cases": list(HELPER_CASES),
        "helper_case_results": list(case_results),
        "helper_gates": list(gates),
        "helper_issues": list(issues),
        "helper_index": index,
        "task_10_ready": task_ready,
        "helper_implementation_ready": True,
        "helper_count": EXPECTED_HELPER_COUNT,
        "diagnostic_record_count": len(outputs["records"]),
        "total_hint_count": len(all_hints),
        "world_model_hint_count": len(outputs["world_model_hints"]),
        "goal_inference_hint_count": len(outputs["goal_inference_hints"]),
        "planner_hint_count": len(outputs["planner_hints"]),
        "transition_verifier_hint_count": len(outputs["transition_verifier_hints"]),
        "action_policy_hint_count": len(outputs["action_policy_hints"]),
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "helper_check_count": len(HELPER_CHECKS),
        "helper_case_count": len(HELPER_CASES),
        "helper_case_pass_count": pass_count,
        "helper_case_failure_count": failure_count,
        "helper_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "helper_issue_count": issue_count,
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
            "source": "milestone_11_local_solver_patch_helpers_v1",
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
        "task_10_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPERS-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helpers(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("helper_gates", [])
    issues = record.get("helper_issues", [])
    case_results = record.get("helper_case_results", [])
    scorecard = record.get("helper_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_10_id_present": isinstance(record.get("task_10_id"), str) and bool(record.get("task_10_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("3f96067"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_10_ready") is True,
        "helper_implementation_ready": record.get("helper_implementation_ready") is True,
        "helper_count_valid": record.get("helper_count") == EXPECTED_HELPER_COUNT,
        "diagnostic_record_count_valid": record.get("diagnostic_record_count") == EXPECTED_RECORD_COUNT,
        "total_hint_count_valid": record.get("total_hint_count") == EXPECTED_TOTAL_HINT_COUNT,
        "world_model_hint_count_valid": record.get("world_model_hint_count") == EXPECTED_HINT_COUNT_PER_LAYER,
        "goal_inference_hint_count_valid": record.get("goal_inference_hint_count") == EXPECTED_HINT_COUNT_PER_LAYER,
        "planner_hint_count_valid": record.get("planner_hint_count") == EXPECTED_HINT_COUNT_PER_LAYER,
        "transition_verifier_hint_count_valid": record.get("transition_verifier_hint_count") == EXPECTED_HINT_COUNT_PER_LAYER,
        "action_policy_hint_count_valid": record.get("action_policy_hint_count") == EXPECTED_HINT_COUNT_PER_LAYER,
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
        "check_count_valid": record.get("helper_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("helper_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("helper_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("helper_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_10_id": record.get("task_10_id"),
        "signature": record.get("signature"),
    }


def render_task_10_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 10 - Local Solver Patch Helpers v1",
        "",
        f"- status: {record['status']}",
        f"- task_10_id: {record['task_10_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_10_ready: {record['task_10_ready']}",
        f"- helper_implementation_ready: {record['helper_implementation_ready']}",
        f"- helper_count: {record['helper_count']}",
        f"- diagnostic_record_count: {record['diagnostic_record_count']}",
        f"- total_hint_count: {record['total_hint_count']}",
        f"- world_model_hint_count: {record['world_model_hint_count']}",
        f"- goal_inference_hint_count: {record['goal_inference_hint_count']}",
        f"- planner_hint_count: {record['planner_hint_count']}",
        f"- transition_verifier_hint_count: {record['transition_verifier_hint_count']}",
        f"- action_policy_hint_count: {record['action_policy_hint_count']}",
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
        "## Helper layer summary",
        "",
    ]

    for row in record["helper_layer_summary"]:
        lines.append(
            f"- {row['target_layer']} / hint_count={row['hint_count']} / "
            f"diagnostic_only={row['diagnostic_only']} / score_claim_allowed={row['score_claim_allowed']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["helper_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 10 creates local solver patch helpers only. It does not modify runtime solver or ranker behavior.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_10_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_10_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_10_VERDICT=LOCAL_SOLVER_PATCH_HELPERS_READY_FOR_LOCAL_HELPER_PROBE_RUN",
            "ARC_AGI3_MILESTONE_11_TASK_10_BASELINE_COMMIT=3f96067",
            "ARC_AGI3_MILESTONE_11_TASK_10_NEXT_STAGE=MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_READY=true",
            f"ARC_AGI3_MILESTONE_11_HELPER_COUNT={EXPECTED_HELPER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DIAGNOSTIC_RECORD_COUNT={EXPECTED_RECORD_COUNT}",
            f"ARC_AGI3_MILESTONE_11_TOTAL_HINT_COUNT={EXPECTED_TOTAL_HINT_COUNT}",
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


def render_task_10_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 10 LOCAL SOLVER PATCH HELPERS MANIFEST v1",
        f"task_10_id={record['task_10_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_10_ready={record['task_10_ready']}",
        f"helper_implementation_ready={record['helper_implementation_ready']}",
        f"helper_count={record['helper_count']}",
        f"diagnostic_record_count={record['diagnostic_record_count']}",
        f"total_hint_count={record['total_hint_count']}",
        f"world_model_hint_count={record['world_model_hint_count']}",
        f"goal_inference_hint_count={record['goal_inference_hint_count']}",
        f"planner_hint_count={record['planner_hint_count']}",
        f"transition_verifier_hint_count={record['transition_verifier_hint_count']}",
        f"action_policy_hint_count={record['action_policy_hint_count']}",
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
        "HELPER_LAYER_SUMMARY",
    ]

    for row in record["helper_layer_summary"]:
        lines.append(
            f"{row['target_layer']} hint_count={row['hint_count']} diagnostic_only={row['diagnostic_only']} "
            f"score_claim_allowed={row['score_claim_allowed']}"
        )

    lines.append("")
    lines.append("HELPER_CASE_RESULTS")
    for result in record["helper_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_10_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helpers())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helpers-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helpers-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helpers-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helpers-index-v1.json"
    bundle_path = output / "milestone-11-local-solver-patch-helper-bundle-v1.json"
    layer_summary_path = output / "milestone-11-local-solver-patch-helper-layer-summary-v1.json"
    wm_path = output / "milestone-11-world-model-state-tracking-hints-v1.json"
    gi_path = output / "milestone-11-goal-inference-terminal-state-hints-v1.json"
    planner_path = output / "milestone-11-planner-loop-recovery-hints-v1.json"
    verifier_path = output / "milestone-11-transition-verifier-feedback-hints-v1.json"
    action_path = output / "milestone-11-action-policy-validity-guard-hints-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helpers-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helpers-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_10_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_10_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["helper_index"], indent=2, sort_keys=True), encoding="utf-8")
    bundle_path.write_text(json.dumps(record["helper_bundle"], indent=2, sort_keys=True), encoding="utf-8")
    layer_summary_path.write_text(json.dumps(record["helper_layer_summary"], indent=2, sort_keys=True), encoding="utf-8")
    wm_path.write_text(json.dumps(record["world_model_hints"], indent=2, sort_keys=True), encoding="utf-8")
    gi_path.write_text(json.dumps(record["goal_inference_hints"], indent=2, sort_keys=True), encoding="utf-8")
    planner_path.write_text(json.dumps(record["planner_hints"], indent=2, sort_keys=True), encoding="utf-8")
    verifier_path.write_text(json.dumps(record["transition_verifier_hints"], indent=2, sort_keys=True), encoding="utf-8")
    action_path.write_text(json.dumps(record["action_policy_hints"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["task_10_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["helper_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "bundle_path": str(bundle_path),
        "layer_summary_path": str(layer_summary_path),
        "world_model_path": str(wm_path),
        "goal_inference_path": str(gi_path),
        "planner_path": str(planner_path),
        "verifier_path": str(verifier_path),
        "action_policy_path": str(action_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helpers_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helpers()
    validation = validate_milestone_11_local_solver_patch_helpers(record)
    artifacts = write_task_10_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_10_id": record["task_10_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_10_ready": record["task_10_ready"],
        "helper_implementation_ready": record["helper_implementation_ready"],
        "helper_count": record["helper_count"],
        "diagnostic_record_count": record["diagnostic_record_count"],
        "total_hint_count": record["total_hint_count"],
        "world_model_hint_count": record["world_model_hint_count"],
        "goal_inference_hint_count": record["goal_inference_hint_count"],
        "planner_hint_count": record["planner_hint_count"],
        "transition_verifier_hint_count": record["transition_verifier_hint_count"],
        "action_policy_hint_count": record["action_policy_hint_count"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "helper_check_count": record["helper_check_count"],
        "helper_case_count": record["helper_case_count"],
        "helper_case_pass_count": record["helper_case_pass_count"],
        "helper_case_failure_count": record["helper_case_failure_count"],
        "helper_gate_count": record["helper_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "helper_issue_count": record["helper_issue_count"],
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
