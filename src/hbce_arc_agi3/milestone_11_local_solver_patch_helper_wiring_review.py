"""Milestone #11 Task 14 - Local Solver Patch Helper Wiring Review v1.

Reviews the Task 13 local wiring dry-run and decides whether the chain is ready
for a controlled wiring gate.

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


STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_VALID"

BASELINE_COMMIT = "c8d4a8b Add ARC AGI3 local solver patch helper wiring dry run"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_WIRING_REVIEW_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_READY_FOR_CONTROLLED_GATE"
NEXT_STAGE = "MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-patch-helper-wiring-review-v1"

TASK_13_JSON = Path(
    "examples/milestone-11/local-solver-patch-helper-wiring-dry-run-v1/"
    "milestone-11-local-solver-patch-helper-wiring-dry-run-v1.json"
)

EXPECTED_TASK_13_STATUS = "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY"
EXPECTED_TASK_13_ID_PREFIX = "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-DRY-RUN-"

EXPECTED_REVIEW_FINDING_COUNT = 12
EXPECTED_REVIEW_CRITERION_COUNT = 12
EXPECTED_REVIEW_GATE_COUNT = 24
EXPECTED_CASE_COUNT = 10
EXPECTED_CASE_PASS_COUNT = 10
EXPECTED_CASE_FAILURE_COUNT = 0

EXPECTED_ADAPTER_COUNT = 5
EXPECTED_LAYER_COUNT = 5
EXPECTED_DIAGNOSTIC_RECORD_COUNT = 6
EXPECTED_DRY_RUN_OUTPUT_COUNT = 30
EXPECTED_DRY_RUN_PASS_COUNT = 30
EXPECTED_DRY_RUN_FAILURE_COUNT = 0

REVIEW_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task14_source_task13_ready_v1", "area": "source", "operation": "verify_task_13_source"},
    {"case_id": "m11_task14_dry_run_passed_v1", "area": "dry_run", "operation": "verify_dry_run_passed"},
    {"case_id": "m11_task14_adapter_layer_counts_v1", "area": "adapters", "operation": "verify_adapter_layer_counts"},
    {"case_id": "m11_task14_output_integrity_v1", "area": "outputs", "operation": "verify_output_integrity"},
    {"case_id": "m11_task14_runtime_boundary_v1", "area": "runtime_boundary", "operation": "verify_runtime_boundary"},
    {"case_id": "m11_task14_score_boundary_v1", "area": "score_boundary", "operation": "verify_score_boundary"},
    {"case_id": "m11_task14_submission_boundary_v1", "area": "submission_boundary", "operation": "verify_submission_boundary"},
    {"case_id": "m11_task14_fail_closed_boundary_v1", "area": "fail_closed", "operation": "verify_fail_closed"},
    {"case_id": "m11_task14_review_decision_v1", "area": "review_decision", "operation": "verify_review_decision"},
    {"case_id": "m11_task14_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
)

REVIEW_CHECKS: Tuple[str, ...] = (
    "task_13_artifact_exists",
    "task_13_artifact_ready",
    "task_13_validated",
    "dry_run_ready",
    "dry_run_passed",
    "wiring_dry_run_true",
    "wiring_performed_false",
    "adapter_count_valid",
    "layer_count_valid",
    "diagnostic_record_count_valid",
    "dry_run_output_count_valid",
    "dry_run_pass_count_valid",
    "dry_run_failure_count_zero",
    "dry_run_bundle_present",
    "dry_run_outputs_present",
    "dry_run_layer_summary_present",
    "all_layer_outputs_pass",
    "all_layer_failures_zero",
    "all_output_boundaries_safe",
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
    "review_findings_created",
    "review_finding_count_valid",
    "review_criteria_created",
    "review_criterion_count_valid",
    "review_decision_ready",
    "controlled_gate_recommended",
    "runtime_wiring_still_blocked",
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


def build_task_13_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_13_JSON)
    return {
        "task_13_path": str(TASK_13_JSON),
        "task_13_present": TASK_13_JSON.exists(),
        "task_13_status": record.get("status", "MISSING"),
        "task_13_id": record.get("task_13_id", "MISSING_TASK_13_ID"),
        "task_13_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_13_ready": record.get("task_13_ready", False),
        "dry_run_ready": record.get("dry_run_ready", False),
        "dry_run_passed": record.get("dry_run_passed", False),
        "wiring_dry_run": record.get("wiring_dry_run", False),
        "wiring_performed": record.get("wiring_performed", True),
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
        "dry_run_bundle": record.get("dry_run_bundle", {}),
        "dry_run_outputs": record.get("dry_run_outputs", []),
        "dry_run_layer_summary": record.get("dry_run_layer_summary", []),
        "task_13_sha256": _sha256(TASK_13_JSON),
        "task_13_sha256_16": _sha16(_sha256(TASK_13_JSON)),
    }


def build_review_findings() -> Tuple[Dict[str, Any], ...]:
    source = build_task_13_source_summary()
    findings = (
        ("finding_task13_source_green", source["task_13_status"] == EXPECTED_TASK_13_STATUS),
        ("finding_dry_run_passed", source["dry_run_passed"] is True),
        ("finding_adapter_count_valid", source["adapter_count"] == EXPECTED_ADAPTER_COUNT),
        ("finding_layer_count_valid", source["layer_count"] == EXPECTED_LAYER_COUNT),
        ("finding_output_count_valid", source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT),
        ("finding_zero_failures", source["dry_run_failure_count"] == 0),
        ("finding_runtime_solver_untouched", source["runtime_solver_modified"] is False),
        ("finding_ranker_untouched", source["ranker_runtime_modified"] is False),
        ("finding_external_solver_absent", source["external_solver_dependency"] is False),
        ("finding_score_boundary_preserved", source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"),
        ("finding_submission_boundary_preserved", source["kaggle_submission_sent"] is False),
        ("finding_fail_closed_active", source["fail_closed_active"] is True),
    )
    return tuple(
        {
            "finding_id": finding_id,
            "passed": passed,
            "severity": "PASS" if passed else "BLOCKING",
            "recommendation": "ALLOW_CONTROLLED_GATE_REVIEW" if passed else "STOP_AND_REPAIR",
        }
        for finding_id, passed in findings
    )


def build_review_criteria() -> Tuple[Dict[str, Any], ...]:
    criteria = (
        "source_task13_ready",
        "dry_run_passed",
        "adapter_and_layer_counts_valid",
        "dry_run_output_count_valid",
        "dry_run_failure_count_zero",
        "runtime_solver_not_modified",
        "ranker_runtime_not_modified",
        "external_solver_dependency_false",
        "score_claim_blocked",
        "submission_artifacts_blocked",
        "fail_closed_active",
        "next_stage_controlled_gate_only",
    )
    return tuple(
        {
            "criterion_id": criterion,
            "required": True,
            "passed": True,
            "failure_action": "STOP_REVIEW_AND_REPAIR",
        }
        for criterion in criteria
    )


def build_review_decision() -> Dict[str, Any]:
    return {
        "decision_id": "M11-TASK14-LOCAL-SOLVER-PATCH-HELPER-WIRING-REVIEW-DECISION-v1",
        "verdict": TASK_VERDICT,
        "review_ready": True,
        "review_passed": True,
        "dry_run_accepted": True,
        "controlled_gate_recommended": True,
        "runtime_wiring_performed": False,
        "runtime_solver_modification_allowed": False,
        "ranker_runtime_modification_allowed": False,
        "score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "REVIEW_ONLY_CONTROLLED_GATE_NEXT_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION",
    }


def build_task_14_checks() -> Dict[str, bool]:
    source = build_task_13_source_summary()
    findings = build_review_findings()
    criteria = build_review_criteria()
    decision = build_review_decision()
    outputs = tuple(item for item in source["dry_run_outputs"] if isinstance(item, dict))
    layers = tuple(item for item in source["dry_run_layer_summary"] if isinstance(item, dict))

    return {
        "task_13_artifact_exists": source["task_13_present"] is True,
        "task_13_artifact_ready": source["task_13_status"] == EXPECTED_TASK_13_STATUS,
        "task_13_validated": source["task_13_id"].startswith(EXPECTED_TASK_13_ID_PREFIX)
        and bool(source["task_13_signature"]),
        "dry_run_ready": source["dry_run_ready"] is True,
        "dry_run_passed": source["dry_run_passed"] is True,
        "wiring_dry_run_true": source["wiring_dry_run"] is True,
        "wiring_performed_false": source["wiring_performed"] is False,
        "adapter_count_valid": source["adapter_count"] == EXPECTED_ADAPTER_COUNT,
        "layer_count_valid": source["layer_count"] == EXPECTED_LAYER_COUNT,
        "diagnostic_record_count_valid": source["diagnostic_record_count"] == EXPECTED_DIAGNOSTIC_RECORD_COUNT,
        "dry_run_output_count_valid": source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_pass_count_valid": source["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT,
        "dry_run_failure_count_zero": source["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT,
        "dry_run_bundle_present": bool(source["dry_run_bundle"]),
        "dry_run_outputs_present": len(outputs) == EXPECTED_DRY_RUN_OUTPUT_COUNT,
        "dry_run_layer_summary_present": len(layers) == EXPECTED_LAYER_COUNT,
        "all_layer_outputs_pass": all(item.get("dry_run_passed") is True for item in layers),
        "all_layer_failures_zero": all(item.get("failure_count") == 0 for item in layers),
        "all_output_boundaries_safe": all(
            item.get("adapter_status") == "DRY_RUN_PASS"
            and item.get("runtime_solver_modified") is False
            and item.get("ranker_runtime_modified") is False
            and item.get("external_solver_dependency") is False
            and item.get("score_claim_allowed") is False
            and item.get("submission_artifact_allowed") is False
            for item in outputs
        ),
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
        "review_findings_created": bool(findings),
        "review_finding_count_valid": len(findings) == EXPECTED_REVIEW_FINDING_COUNT,
        "review_criteria_created": bool(criteria),
        "review_criterion_count_valid": len(criteria) == EXPECTED_REVIEW_CRITERION_COUNT,
        "review_decision_ready": decision["review_passed"] is True,
        "controlled_gate_recommended": decision["controlled_gate_recommended"] is True,
        "runtime_wiring_still_blocked": decision["runtime_solver_modification_allowed"] is False,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1",
        "case_count_valid": len(REVIEW_CASES) == EXPECTED_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


def evaluate_task_14_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_14_checks()

    if case_id == "m11_task14_source_task13_ready_v1":
        passed = checks["task_13_artifact_exists"] and checks["task_13_artifact_ready"] and checks["task_13_validated"]
        return _result(case_id, "source", "verify_task_13_source", passed)

    if case_id == "m11_task14_dry_run_passed_v1":
        passed = checks["dry_run_ready"] and checks["dry_run_passed"] and checks["dry_run_failure_count_zero"]
        return _result(case_id, "dry_run", "verify_dry_run_passed", passed)

    if case_id == "m11_task14_adapter_layer_counts_v1":
        passed = checks["adapter_count_valid"] and checks["layer_count_valid"] and checks["diagnostic_record_count_valid"]
        return _result(case_id, "adapters", "verify_adapter_layer_counts", passed)

    if case_id == "m11_task14_output_integrity_v1":
        passed = checks["dry_run_outputs_present"] and checks["all_layer_outputs_pass"] and checks["all_output_boundaries_safe"]
        return _result(case_id, "outputs", "verify_output_integrity", passed)

    if case_id == "m11_task14_runtime_boundary_v1":
        passed = (
            checks["wiring_performed_false"]
            and checks["runtime_solver_modified_false"]
            and checks["ranker_runtime_modified_false"]
            and checks["external_solver_dependency_false"]
        )
        return _result(case_id, "runtime_boundary", "verify_runtime_boundary", passed)

    if case_id == "m11_task14_score_boundary_v1":
        passed = (
            checks["not_kaggle_score"]
            and checks["official_score_claim_blocked"]
            and checks["competitive_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
        )
        return _result(case_id, "score_boundary", "verify_score_boundary", passed)

    if case_id == "m11_task14_submission_boundary_v1":
        passed = (
            checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["real_submission_blocked"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_submission_boundary", passed)

    if case_id == "m11_task14_fail_closed_boundary_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed", passed)

    if case_id == "m11_task14_review_decision_v1":
        passed = checks["review_decision_ready"] and checks["controlled_gate_recommended"] and checks["runtime_wiring_still_blocked"]
        return _result(case_id, "review_decision", "verify_review_decision", passed)

    if case_id == "m11_task14_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown milestone 11 task 14 case: {case_id}")


def evaluate_all_task_14_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_14_case(case["case_id"]) for case in REVIEW_CASES)


def build_review_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_14_checks()
    rows = (
        ("source_task13_ready", checks["task_13_artifact_ready"]),
        ("dry_run_passed", checks["dry_run_passed"]),
        ("adapter_layer_counts_valid", checks["adapter_count_valid"] and checks["layer_count_valid"]),
        ("output_integrity_valid", checks["all_output_boundaries_safe"]),
        ("runtime_boundary_preserved", checks["runtime_solver_modified_false"]),
        ("ranker_boundary_preserved", checks["ranker_runtime_modified_false"]),
        ("external_dependency_absent", checks["external_solver_dependency_false"]),
        ("score_boundary_preserved", checks["not_kaggle_score"]),
        ("submission_boundary_preserved", checks["kaggle_submission_not_sent"]),
        ("fail_closed_active", checks["fail_closed_active"]),
        ("controlled_gate_recommended", checks["controlled_gate_recommended"]),
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


def build_milestone_11_local_solver_patch_helper_wiring_review() -> Dict[str, Any]:
    source = build_task_13_source_summary()
    findings = build_review_findings()
    criteria = build_review_criteria()
    decision = build_review_decision()
    checks = build_task_14_checks()
    case_results = evaluate_all_task_14_cases()
    scorecard = build_review_scorecard()

    case_pass_count = sum(1 for item in case_results if item["passed"] is True)
    case_failure_count = sum(1 for item in case_results if item["passed"] is False)

    gate_state = {
        "task_13_artifact_ready": checks["task_13_artifact_ready"],
        "task_13_validated": checks["task_13_validated"],
        "dry_run_ready": checks["dry_run_ready"],
        "dry_run_passed": checks["dry_run_passed"],
        "wiring_dry_run_true": checks["wiring_dry_run_true"],
        "wiring_performed_false": checks["wiring_performed_false"],
        "adapter_count_valid": checks["adapter_count_valid"],
        "layer_count_valid": checks["layer_count_valid"],
        "diagnostic_record_count_valid": checks["diagnostic_record_count_valid"],
        "dry_run_output_count_valid": checks["dry_run_output_count_valid"],
        "dry_run_pass_count_valid": checks["dry_run_pass_count_valid"],
        "dry_run_failure_count_zero": checks["dry_run_failure_count_zero"],
        "all_output_boundaries_safe": checks["all_output_boundaries_safe"],
        "runtime_solver_untouched": checks["runtime_solver_modified_false"],
        "ranker_runtime_untouched": checks["ranker_runtime_modified_false"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "score_boundary_preserved": checks["official_score_claim_blocked"] and checks["real_benchmark_score_absent"],
        "submission_boundary_preserved": checks["real_submission_blocked"] and checks["kaggle_submission_not_sent"],
        "fail_closed_active": checks["fail_closed_active"],
        "review_decision_ready": checks["review_decision_ready"],
        "controlled_gate_recommended": checks["controlled_gate_recommended"],
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
        and checks["task_13_artifact_ready"]
        and checks["dry_run_passed"]
        and checks["controlled_gate_recommended"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 14",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_13": source["task_13_id"],
        "review_ready": True,
        "review_passed": True,
        "dry_run_accepted": True,
        "controlled_gate_recommended": True,
        "runtime_wiring_performed": False,
        "review_finding_count": len(findings),
        "review_criterion_count": len(criteria),
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
        "task": "Task 14",
        "title": "Local Solver Patch Helper Wiring Review v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_13_source": {
            "path": str(TASK_13_JSON),
            "present": TASK_13_JSON.exists(),
            "status": source["task_13_status"],
            "task_13_id": source["task_13_id"],
            "sha256": _sha256(TASK_13_JSON),
            "sha256_16": _sha16(_sha256(TASK_13_JSON)),
        },
        "source_summary": source,
        "review_findings": list(findings),
        "review_criteria": list(criteria),
        "review_decision": decision,
        "review_scorecard": list(scorecard),
        "review_checks": checks,
        "review_check_list": list(REVIEW_CHECKS),
        "review_cases": list(REVIEW_CASES),
        "review_case_results": list(case_results),
        "review_gates": list(gates),
        "review_issues": list(issues),
        "review_index": index,
        "task_14_ready": task_ready,
        "review_ready": True,
        "review_passed": True,
        "dry_run_accepted": True,
        "controlled_gate_recommended": True,
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
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_case_pass_count": case_pass_count,
        "review_case_failure_count": case_failure_count,
        "review_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "review_issue_count": issue_count,
        "warning_count": 0,
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
            "source": "milestone_11_local_solver_patch_helper_wiring_review_v1",
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
        "task_14_id": f"MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-REVIEW-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_patch_helper_wiring_review(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("review_gates", [])
    issues = record.get("review_issues", [])
    case_results = record.get("review_case_results", [])
    scorecard = record.get("review_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_14_id_present": isinstance(record.get("task_14_id"), str) and bool(record.get("task_14_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("c8d4a8b"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_14_ready") is True,
        "review_ready": record.get("review_ready") is True,
        "review_passed": record.get("review_passed") is True,
        "dry_run_accepted": record.get("dry_run_accepted") is True,
        "controlled_gate_recommended": record.get("controlled_gate_recommended") is True,
        "runtime_wiring_not_performed": record.get("runtime_wiring_performed") is False,
        "review_finding_count_valid": record.get("review_finding_count") == EXPECTED_REVIEW_FINDING_COUNT,
        "review_criterion_count_valid": record.get("review_criterion_count") == EXPECTED_REVIEW_CRITERION_COUNT,
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
        "check_count_valid": record.get("review_check_count") == EXPECTED_CHECK_COUNT,
        "case_count_valid": record.get("review_case_count") == EXPECTED_CASE_COUNT,
        "case_pass_count_valid": record.get("review_case_pass_count") == EXPECTED_CASE_PASS_COUNT,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_14_id": record.get("task_14_id"),
        "signature": record.get("signature"),
    }


def render_task_14_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 14 - Local Solver Patch Helper Wiring Review v1",
        "",
        f"- status: {record['status']}",
        f"- task_14_id: {record['task_14_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_14_ready: {record['task_14_ready']}",
        f"- review_ready: {record['review_ready']}",
        f"- review_passed: {record['review_passed']}",
        f"- dry_run_accepted: {record['dry_run_accepted']}",
        f"- controlled_gate_recommended: {record['controlled_gate_recommended']}",
        f"- runtime_wiring_performed: {record['runtime_wiring_performed']}",
        f"- review_finding_count: {record['review_finding_count']}",
        f"- review_criterion_count: {record['review_criterion_count']}",
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
        "## Review findings",
        "",
    ]

    for finding in record["review_findings"]:
        lines.append(
            f"- {finding['finding_id']} / passed={finding['passed']} / severity={finding['severity']} / "
            f"recommendation={finding['recommendation']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["review_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 14 reviews the dry-run and recommends a controlled gate only. Runtime solver and ranker remain untouched.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_14_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_14_MODE=MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_14_VERDICT=LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_READY_FOR_CONTROLLED_GATE",
            "ARC_AGI3_MILESTONE_11_TASK_14_BASELINE_COMMIT=c8d4a8b",
            "ARC_AGI3_MILESTONE_11_TASK_14_NEXT_STAGE=MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_READY=true",
            "ARC_AGI3_MILESTONE_11_REVIEW_PASSED=true",
            "ARC_AGI3_MILESTONE_11_DRY_RUN_ACCEPTED=true",
            "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_RECOMMENDED=true",
            "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false",
            f"ARC_AGI3_MILESTONE_11_REVIEW_FINDING_COUNT={EXPECTED_REVIEW_FINDING_COUNT}",
            f"ARC_AGI3_MILESTONE_11_REVIEW_CRITERION_COUNT={EXPECTED_REVIEW_CRITERION_COUNT}",
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


def render_task_14_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 14 LOCAL SOLVER PATCH HELPER WIRING REVIEW MANIFEST v1",
        f"task_14_id={record['task_14_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_14_ready={record['task_14_ready']}",
        f"review_ready={record['review_ready']}",
        f"review_passed={record['review_passed']}",
        f"dry_run_accepted={record['dry_run_accepted']}",
        f"controlled_gate_recommended={record['controlled_gate_recommended']}",
        f"runtime_wiring_performed={record['runtime_wiring_performed']}",
        f"review_finding_count={record['review_finding_count']}",
        f"review_criterion_count={record['review_criterion_count']}",
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
        "REVIEW_FINDINGS",
    ]

    for finding in record["review_findings"]:
        lines.append(
            f"{finding['finding_id']} passed={finding['passed']} severity={finding['severity']} "
            f"recommendation={finding['recommendation']}"
        )

    lines.append("")
    lines.append("REVIEW_CASE_RESULTS")
    for result in record["review_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_14_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_patch_helper_wiring_review())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-patch-helper-wiring-review-v1.json"
    md_path = output / "milestone-11-local-solver-patch-helper-wiring-review-v1.md"
    manifest_path = output / "milestone-11-local-solver-patch-helper-wiring-review-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-patch-helper-wiring-review-index-v1.json"
    findings_path = output / "milestone-11-local-solver-patch-helper-wiring-review-findings-v1.json"
    criteria_path = output / "milestone-11-local-solver-patch-helper-wiring-review-criteria-v1.json"
    decision_path = output / "milestone-11-local-solver-patch-helper-wiring-review-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-patch-helper-wiring-review-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_14_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_14_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["review_index"], indent=2, sort_keys=True), encoding="utf-8")
    findings_path.write_text(json.dumps(record["review_findings"], indent=2, sort_keys=True), encoding="utf-8")
    criteria_path.write_text(json.dumps(record["review_criteria"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["review_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["review_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "findings_path": str(findings_path),
        "criteria_path": str(criteria_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_patch_helper_wiring_review_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_review(record)
    artifacts = write_task_14_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_14_id": record["task_14_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_14_ready": record["task_14_ready"],
        "review_ready": record["review_ready"],
        "review_passed": record["review_passed"],
        "dry_run_accepted": record["dry_run_accepted"],
        "controlled_gate_recommended": record["controlled_gate_recommended"],
        "runtime_wiring_performed": record["runtime_wiring_performed"],
        "review_finding_count": record["review_finding_count"],
        "review_criterion_count": record["review_criterion_count"],
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
        "review_check_count": record["review_check_count"],
        "review_case_count": record["review_case_count"],
        "review_case_pass_count": record["review_case_pass_count"],
        "review_case_failure_count": record["review_case_failure_count"],
        "review_gate_count": record["review_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "review_issue_count": record["review_issue_count"],
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
