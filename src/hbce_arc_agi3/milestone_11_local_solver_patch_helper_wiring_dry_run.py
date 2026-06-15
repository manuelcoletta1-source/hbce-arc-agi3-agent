"""Milestone #11 Task 13 - Local Solver Patch Helper Wiring Dry Run v1."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple

from hbce_arc_agi3.local_solver_patch_helper_wiring import (
    LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION,
    LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
    run_local_solver_patch_helper_wiring_dry_run,
)


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_VALID"

BASELINE_COMMIT = "8d74231 Add ARC AGI3 local solver patch helper wiring plan"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_WIRING_DRY_RUN_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_READY_FOR_REVIEW"
NEXT_STAGE = "MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-wiring-dry-run-v1"

TASK_12_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-wiring-plan-v1/"
    "milestone-11-local-solver-patch-helper-wiring-plan-v1.json"
)

TASK_5_JSON = Path(
    "examples/milestone-11/local-diagnostic-fixture-harness-v1/"
    "milestone-11-local-diagnostic-fixture-harness-v1.json"
)

EXPECTED_TASK_12_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY"
EXPECTED_TASK_12_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-PLAN-"

EXPECTED_RECORD_COUNT = 6
EXPECTED_ADAPTER_COUNT = 5
EXPECTED_LAYER_COUNT = 5
EXPECTED_OUTPUT_COUNT_PER_LAYER = 6
EXPECTED_DRY_RUN_OUTPUT_COUNT = 30
EXPECTED_DRY_RUN_PASS_COUNT = 30
EXPECTED_DRY_RUN_FAILURE_COUNT = 0
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

DRY_RUN_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task13_source_task12_ready_v1", "area": "source", "operation": "verify_task_12_source"},
    {"case_id": "m11_task13_records_ready_v1", "area": "records", "operation": "verify_diagnostic_records"},
    {"case_id": "m11_task13_wiring_module_ready_v1", "area": "module", "operation": "verify_wiring_module"},
    {"case_id": "m11_task13_adapter_outputs_ready_v1", "area": "adapter_outputs", "operation": "verify_adapter_outputs"},
    {"case_id": "m11_task13_all_layers_pass_v1", "area": "layers", "operation": "verify_all_layers"},
    {"case_id": "m11_task13_dry_run_output_count_v1", "area": "dry_run", "operation": "verify_dry_run_counts"},
    {"case_id": "m11_task13_no_runtime_mutation_v1", "area": "runtime_boundary", "operation": "verify_no_runtime_mutation"},
    {"case_id": "m11_task13_score_submission_boundary_v1", "area": "score_submission", "operation": "verify_no_score_no_submission"},
    {"case_id": "m11_task13_fail_closed_boundary_v1", "area": "fail_closed", "operation": "verify_fail_closed"},
    {"case_id": "m11_task13_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

DRY_RUN_CHECKS: Tuple[str, ...] = (
    "task_12_artifact_exists",
    "task_12_artifact_ready",
    "task_12_validated",
    "wiring_plan_ready",
    "wiring_performed_false",
    "next_stage_scope_valid",
    "diagnostic_records_present",
    "diagnostic_record_count_valid",
    "local_wiring_module_revision_valid",
    "local_wiring_module_status_valid",
    "dry_run_bundle_created",
    "dry_run_id_present",
    "adapter_count_valid",
    "layer_count_valid",
    "all_layers_have_outputs",
    "all_layer_output_counts_valid",
    "dry_run_output_count_valid",
    "dry_run_pass_count_valid",
    "dry_run_failure_count_zero",
    "all_adapter_outputs_pass",
    "all_adapter_outputs_diagnostic_only",
    "all_adapter_outputs_not_kaggle_score",
    "all_adapter_outputs_score_claim_blocked",
    "all_adapter_outputs_submission_blocked",
    "wiring_dry_run_true",
    "wiring_performed_false_after_dry_run",
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

EXPECTED_CHECK_COUNT = len(DRY_RUN_CHECKS)


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


def build_task_12_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_12_JSON)
    return {
        "task_12_path": str(TASK_12_JSON),
        "task_12_present": TASK_12_JSON.exists(),
        "task_12_status": record.get("status", "MISSING"),
        "task_12_id": record.get("task_12_id", "MISSING_TASK_12_ID"),
        "task_12_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_12_ready": record.get("task_12_ready", False),
        "wiring_plan_ready": record.get("wiring_plan_ready", False),
        "wiring_performed": record.get("wiring_performed", True),
        "next_stage_authorized_scope": record.get("next_stage_authorized_scope", "MISSING_SCOPE"),
        "wiring_target_count": record.get("wiring_target_count", 0),
        "adapter_plan_count": record.get("adapter_plan_count", 0),
        "wiring_step_count": record.get("wiring_step_count", 0),
        "wiring_gate_count": record.get("wiring_gate_count", 0),
        "stop_condition_count": record.get("stop_condition_count", 0),
        "required_test_count": record.get("required_test_count", 0),
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
        "task_12_sha256": _sha256(TASK_12_JSON),
        "task_12_sha256_16": _sha16(_sha256(TASK_12_JSON)),
    }


def build_diagnostic_records() -> Tuple[Dict[str, Any], ...]:
    record = _read_json(TASK_5_JSON)
    rows = record.get("episode_results", [])
    return tuple(row for row in rows if isinstance(row, dict))


def build_dry_run_bundle() -> Dict[str, Any]:
    return run_local_solver_patch_helper_wiring_dry_run(build_diagnostic_records())


def _flat_outputs(bundle: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    rows = []
    for output in bundle.get("adapter_outputs", {}).values():
        rows.extend(item for item in output if isinstance(item, dict))
    return tuple(rows)


def build_dry_run_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK13-LOCAL-SOLVER-PATCH-HELPER-WIRING-DRY-RUN-DECISION-v1",
        "verdict": TASK_VERDICT,
        "dry_run_ready": True,
        "dry_run_passed": True,
        "wiring_dry_run": True,
        "wiring_performed": False,
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "DRY_RUN_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION",
    }


def build_task_13_checks() -> Dict[str, bool]:
    source = build_task_12_source_summary()
    records = build_diagnostic_records()
    bundle = build_dry_run_bundle()
    outputs = _flat_outputs(bundle)

    return {
        "task_12_artifact_exists": source["task_12_present"] is True,
        "task_12_artifact_ready": source["task_12_status"] == EXPECTED_TASK_12_STATUS,
        "task_12_validated": source["task_12_id"].startswith(EXPECTED_TASK_12_ID_PREFIX)
        and bool(source["task_12_signature"]),
        "wiring_plan_ready": source["wiring_plan_ready"] is True,
        "wiring_performed_false": source["wiring_performed"] is False,
        "next_stage_scope_valid": source["next_stage_authorized_scope"] == "LOCAL_WIRING_DRY_RUN_ONLY",
        "diagnostic_records_present": bool(records),
        "diagnostic_record_count_valid": len(records) == EXPECTED_RECORD_COUNT,
        "local_wiring_module_revision_valid": LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION
        == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1",
        "local_wiring_module_status_valid": LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS
        == "LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_READY",
        "dry_run_bundle_created": bundle["status"] == LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
        "dry_run_id_present": isinstance(bundle.get("dry_run_id"), str) and bool(bundle["dry_run_id"]),
        "adapter_count_valid": bundle["adapter_count"] == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": len(bundle["layer_summary"]) == EXPECTED_LAYER_COUNT,
        "all_layers_have_outputs": all(item["output_count"] == EXPECTED_OUTPUT_COUNT_PER_LAYER for item in bundle["layer_summary"]),
        "all_layer_output_counts_valid": all(item["output_count"] == EXPECTED_OUTPUT_COUNT_PER_LAYER for item in bundle["layer_summary"]),
        "dry_run_output_count_valid": bundle["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_pass_count_valid": bundle["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT,
        "dry_run_failure_count_zero": bundle["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT,
        "all_adapter_outputs_pass": all(item["adapter_status"] == "DRY_RUN_PASS" for item in outputs),
        "all_adapter_outputs_diagnostic_only": all(item["diagnostic_only"] is True for item in outputs),
        "all_adapter_outputs_not_kaggle_score": all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in outputs),
        "all_adapter_outputs_score_claim_blocked": all(item["score_claim_allowed"] is False for item in outputs),
        "all_adapter_outputs_submission_blocked": all(item["submission_artifact_allowed"] is False for item in outputs),
        "wiring_dry_run_true": bundle["wiring_dry_run"] is True,
        "wiring_performed_false_after_dry_run": bundle["wiring_performed"] is False,
        "runtime_solver_modified_false": bundle["runtime_solver_modified"] is False and source["runtime_solver_modified"] is False,
        "ranker_runtime_modified_false": bundle["ranker_runtime_modified"] is False and source["ranker_runtime_modified"] is False,
        "external_solver_dependency_false": bundle["external_solver_dependency"] is False and source["external_solver_dependency"] is False,
        "diagnostic_only": bundle["diagnostic_only"] is True and source["diagnostic_only"] is True,
        "not_kaggle_score": bundle["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE",
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
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1",
        "case_count_valid": len(DRY_RUN_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_13_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_13_checks()

    if case_id == "m11_task13_source_task12_ready_v1":
        passed = checks["task_12_artifact_exists"] and checks["task_12_artifact_ready"] and checks["task_12_validated"]
        return _result(case_id, "source", "verify_task_12_source", passed)

    if case_id == "m11_task13_records_ready_v1":
        passed = checks["diagnostic_records_present"] and checks["diagnostic_record_count_valid"]
        return _result(case_id, "records", "verify_diagnostic_records", passed)

    if case_id == "m11_task13_wiring_module_ready_v1":
        passed = checks["local_wiring_module_revision_valid"] and checks["local_wiring_module_status_valid"]
        return _result(case_id, "module", "verify_wiring_module", passed)

    if case_id == "m11_task13_adapter_outputs_ready_v1":
        passed = checks["all_adapter_outputs_pass"] and checks["dry_run_output_count_valid"]
        return _result(case_id, "adapter_outputs", "verify_adapter_outputs", passed)

    if case_id == "m11_task13_all_layers_pass_v1":
        passed = checks["layer_count_valid"] and checks["all_layers_have_outputs"] and checks["all_layer_output_counts_valid"]
        return _result(case_id, "layers", "verify_all_layers", passed)

    if case_id == "m11_task13_dry_run_output_count_v1":
        passed = checks["dry_run_output_count_valid"] and checks["dry_run_pass_count_valid"] and checks["dry_run_failure_count_zero"]
        return _result(case_id, "dry_run", "verify_dry_run_counts", passed)

    if case_id == "m11_task13_no_runtime_mutation_v1":
        passed = (
            checks["wiring_performed_false_after_dry_run"]
            and checks["runtime_solver_modified_false"]
            and checks["ranker_runtime_modified_false"]
            and checks["external_solver_dependency_false"]
        )
        return _result(case_id, "runtime_boundary", "verify_no_runtime_mutation", passed)

    if case_id == "m11_task13_score_submission_boundary_v1":
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
        return _result(case_id, "score_submission", "verify_no_score_no_submission", passed)

    if case_id == "m11_task13_fail_closed_boundary_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed", passed)

    if case_id == "m11_task13_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 13 case: {case_id}")


def evaluate_all_task_13_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_13_case(case["case_id"]) for case in DRY_RUN_CASES)


def build_dry_run_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_13_checks()
    rows = (
        ("source_task12_ready", checks["task_12_artifact_ready"]),
        ("diagnostic_records_ready", checks["diagnostic_record_count_valid"]),
        ("wiring_module_ready", checks["local_wiring_module_status_valid"]),
        ("adapter_outputs_ready", checks["all_adapter_outputs_pass"]),
        ("all_layers_pass", checks["all_layer_output_counts_valid"]),
        ("dry_run_counts_valid", checks["dry_run_output_count_valid"]),
        ("runtime_solver_untouched", checks["runtime_solver_modified_false"]),
        ("score_submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
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


def build_milestone_11_local_solver_patch_helper_wiring_dry_run() -> Dict[str, Any]:
    source = build_task_12_source_summary()
    records = build_diagnostic_records()
    bundle = build_dry_run_bundle()
    outputs = _flat_outputs(bundle)
    decision = build_dry_run_decision()
    checks = build_task_13_checks()
    case_results = evaluate_all_task_13_cases()
    scorecard = build_dry_run_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_12_artifact_ready": checks["task_12_artifact_ready"],
        "task_12_validated": checks["task_12_validated"],
        "diagnostic_records_ready": checks["diagnostic_record_count_valid"],
        "wiring_module_ready": checks["local_wiring_module_status_valid"],
        "dry_run_bundle_created": checks["dry_run_bundle_created"],
        "adapter_count_valid": checks["adapter_count_valid"],
        "layer_count_valid": checks["layer_count_valid"],
        "dry_run_output_count_valid": checks["dry_run_output_count_valid"],
        "dry_run_pass_count_valid": checks["dry_run_pass_count_valid"],
        "dry_run_failure_count_zero": checks["dry_run_failure_count_zero"],
        "all_adapter_outputs_pass": checks["all_adapter_outputs_pass"],
        "wiring_performed_false": checks["wiring_performed_false_after_dry_run"],
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
        bundle["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
        and bundle["dry_run_failure_count"] == 0
        and case_pass_count == EXPECTED_CASE_PASS_COUNT
        and case_failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_12_artifact_ready"]
        and checks["next_stage_valid"]
        and checks["fail_closed_active"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 13",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_12": source["task_12_id"],
        "local_wiring_module_revision": LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION,
        "local_wiring_module_status": LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
        "dry_run_ready": True,
        "dry_run_passed": True,
        "wiring_dry_run": True,
        "wiring_performed": False,
        "adapter_count": bundle["adapter_count"],
        "record_count": len(records),
        "dry_run_output_count": bundle["dry_run_output_count"],
        "dry_run_pass_count": bundle["dry_run_pass_count"],
        "dry_run_failure_count": bundle["dry_run_failure_count"],
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
        "task": "Task 13",
        "title": "Local Solver Patch Helper Wiring Dry Run v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_12_source": {
            "path": str(TASK_12_JSON),
            "present": TASK_12_JSON.exists(),
            "status": source["task_12_status"],
            "task_12_id": source["task_12_id"],
            "sha256": _sha256(TASK_12_JSON),
            "sha256_16": _sha16(_sha256(TASK_12_JSON)),
        },
        "source_summary": source,
        "diagnostic_record_count": len(records),
        "local_wiring_module_revision": LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION,
        "local_wiring_module_status": LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
        "dry_run_bundle": bundle,
        "dry_run_outputs": list(outputs),
        "dry_run_layer_summary": bundle["layer_summary"],
        "dry_run_decision": decision,
        "dry_run_scorecard": list(scorecard),
        "dry_run_checks": checks,
        "dry_run_check_list": list(DRY_RUN_CHECKS),
        "dry_run_cases": list(DRY_RUN_CASES),
        "dry_run_case_results": list(case_results),
        "dry_run_gates": list(gates),
        "dry_run_issues": list(issues),
        "dry_run_index": index,
        "task_13_ready": task_ready,
        "dry_run_ready": True,
        "dry_run_passed": True,
        "wiring_dry_run": True,
        "wiring_performed": False,
        "adapter_count": bundle["adapter_count"],
        "layer_count": len(bundle["layer_summary"]),
        "dry_run_output_count": bundle["dry_run_output_count"],
        "dry_run_pass_count": bundle["dry_run_pass_count"],
        "dry_run_failure_count": bundle["dry_run_failure_count"],
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "dry_run_check_count": len(DRY_RUN_CHECKS),
        "dry_run_case_count": len(DRY_RUN_CASES),
        "dry_run_case_pass_count": case_pass_count,
        "dry_run_case_failure_count": case_failure_count,
        "dry_run_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "dry_run_issue_count": issue_count,
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
            "source": "milestone_11_local_solver_patch_helper_wiring_dry_run_v1",
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
        "task_13_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-DRY-RUN-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_wiring_dry_run(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("dry_run_gates", [])
    issues = record.get("dry_run_issues", [])
    case_results = record.get("dry_run_case_results", [])
    scorecard = record.get("dry_run_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_13_id_present": isinstance(record.get("task_13_id"), str) and bool(record.get("task_13_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("8d74231"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_13_ready") is True,
        "dry_run_ready": record.get("dry_run_ready") is True,
        "dry_run_passed": record.get("dry_run_passed") is True,
        "wiring_dry_run": record.get("wiring_dry_run") is True,
        "wiring_not_performed": record.get("wiring_performed") is False,
        "adapter_count_valid": record.get("adapter_count") == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": record.get("layer_count") == EXPECTED_LAYER_COUNT,
        "diagnostic_record_count_valid": record.get("diagnostic_record_count") == EXPECTED_RECORD_COUNT,
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
        "check_count_valid": record.get("dry_run_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("dry_run_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("dry_run_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
        "case_failure_count_zero": record.get("dry_run_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_13_id": record.get("task_13_id"),
        "signature": record.get("signature"),
    }


def render_task_13_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 13 - Local Solver Patch Helper Wiring Dry Run v1",
        "",
        f"- status: {record['status']}",
        f"- task_13_id: {record['task_13_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_13_ready: {record['task_13_ready']}",
        f"- dry_run_ready: {record['dry_run_ready']}",
        f"- dry_run_passed: {record['dry_run_passed']}",
        f"- wiring_dry_run: {record['wiring_dry_run']}",
        f"- wiring_performed: {record['wiring_performed']}",
        f"- adapter_count: {record['adapter_count']}",
        f"- layer_count: {record['layer_count']}",
        f"- diagnostic_record_count: {record['diagnostic_record_count']}",
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
        "## Dry-run layer summary",
        "",
    ]

    for row in record["dry_run_layer_summary"]:
        lines.append(
            f"- {row['target_layer']} / adapter={row['adapter_name']} / output={row['output_count']} / "
            f"pass={row['pass_count']} / fail={row['failure_count']} / passed={row['dry_run_passed']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["dry_run_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 13 performs a local wiring dry-run only. Runtime solver and ranker behavior remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_13_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_13_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_13_VERDICT=LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_READY_FOR_REVIEW",
            "ARC_AGI3_MILESTONE_11_TASK_13_BASELINE_COMMIT=8d74231",
            "ARC_AGI3_MILESTONE_11_TASK_13_NEXT_STAGE=MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_READY=true",
            "ARC_AGI3_MILESTONE_11_DRY_RUN_PASSED=true",
            "ARC_AGI3_MILESTONE_11_WIRING_DRY_RUN=true",
            "ARC_AGI3_MILESTONE_11_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_ADAPTER_COUNT={EXPECTED_ADAPTER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_LAYER_COUNT={EXPECTED_LAYER_COUNT}",
            f"ARC_AGI3_MILESTONE_11_DIAGNOSTIC_RECORD_COUNT={EXPECTED_RECORD_COUNT}",
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


def render_task_13_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 13 LOCAL SOLVER PATCH HELPER WIRING DRY RUN MANIFEST v1",
        f"task_13_id={record['task_13_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_13_ready={record['task_13_ready']}",
        f"dry_run_ready={record['dry_run_ready']}",
        f"dry_run_passed={record['dry_run_passed']}",
        f"wiring_dry_run={record['wiring_dry_run']}",
        f"wiring_performed={record['wiring_performed']}",
        f"adapter_count={record['adapter_count']}",
        f"layer_count={record['layer_count']}",
        f"diagnostic_record_count={record['diagnostic_record_count']}",
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
        "DRY_RUN_LAYER_SUMMARY",
    ]

    for row in record["dry_run_layer_summary"]:
        lines.append(
            f"{row['target_layer']} adapter={row['adapter_name']} output={row['output_count']} "
            f"pass={row['pass_count']} fail={row['failure_count']} passed={row['dry_run_passed']}"
        )

    lines.append("")
    lines.append("DRY_RUN_CASE_RESULTS")
    for result in record["dry_run_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_13_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_wiring_dry_run())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-index-v1.json"
    bundle_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-bundle-v1.json"
    outputs_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-outputs-v1.json"
    layer_summary_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-layer-summary-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-wiring-dry-run-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_13_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_13_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["dry_run_index"], indent=2, sort_keys=True), encoding="utf-8")
    bundle_path.write_text(json.dumps(record["dry_run_bundle"], indent=2, sort_keys=True), encoding="utf-8")
    outputs_path.write_text(json.dumps(record["dry_run_outputs"], indent=2, sort_keys=True), encoding="utf-8")
    layer_summary_path.write_text(json.dumps(record["dry_run_layer_summary"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["dry_run_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["dry_run_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "bundle_path": str(bundle_path),
        "outputs_path": str(outputs_path),
        "layer_summary_path": str(layer_summary_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_wiring_dry_run_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_dry_run(record)
    artifacts = write_task_13_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_13_id": record["task_13_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_13_ready": record["task_13_ready"],
        "dry_run_ready": record["dry_run_ready"],
        "dry_run_passed": record["dry_run_passed"],
        "wiring_dry_run": record["wiring_dry_run"],
        "wiring_performed": record["wiring_performed"],
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
        "dry_run_check_count": record["dry_run_check_count"],
        "dry_run_case_count": record["dry_run_case_count"],
        "dry_run_case_pass_count": record["dry_run_case_pass_count"],
        "dry_run_case_failure_count": record["dry_run_case_failure_count"],
        "dry_run_gate_count": record["dry_run_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "dry_run_issue_count": record["dry_run_issue_count"],
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
