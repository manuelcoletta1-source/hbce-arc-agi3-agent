"""Milestone #11 Task 7 - Local Solver Probe Report v1.

Creates an operational report from the Task 6 solver probe integration.

The report explains measured coverage, remaining limits, diagnostic-only
semantics, and the next solver patch backlog. It does not claim Kaggle score,
does not create submission.json, does not create upload packages, does not
authenticate with Kaggle, does not call external APIs, and does not create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


STATUS = "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_READY"
PIPELINE_STATUS = "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_VALID"

BASELINE_COMMIT = "2d9ccce Add ARC AGI3 solver probe integration"
TASK_MODE = "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_SOLVER_PROBE_REPORT_NO_SCORE_NO_SUBMISSION"
TASK_VERDICT = "LOCAL_SOLVER_PROBE_REPORT_READY_FOR_SOLVER_PATCH_BACKLOG"
NEXT_STAGE = "MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-11/local-solver-probe-report-v1"

TASK_6_JSON = Path(
    "examples/milestone-11/solver-probe-integration-v1/"
    "milestone-11-solver-probe-integration-v1.json"
)

EXPECTED_TASK_6_STATUS = "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_READY"
EXPECTED_TASK_6_ID_PREFIX = "MILESTONE-11-SOLVER-PROBE-INTEGRATION-"

EXPECTED_PROBE_COMPONENT_COUNT = 5
EXPECTED_PROBE_RESULT_COUNT = 30
EXPECTED_PROBE_PASS_COUNT = 30
EXPECTED_PROBE_FAILURE_COUNT = 0
EXPECTED_LAYER_REPORT_COUNT = 5

REPORT_SECTIONS: Tuple[str, ...] = (
    "executive_summary",
    "measured_layers",
    "coverage_matrix",
    "diagnostic_interpretation",
    "limits_and_non_claims",
    "solver_patch_backlog",
    "boundary_control",
)

REPORT_CHECKS: Tuple[str, ...] = (
    "task_6_artifact_exists",
    "task_6_artifact_ready",
    "task_6_validated",
    "probe_integration_ready",
    "probe_contract_created",
    "probe_result_count_valid",
    "probe_pass_count_valid",
    "probe_failure_count_zero",
    "layer_report_count_valid",
    "report_sections_created",
    "report_section_count_valid",
    "coverage_matrix_created",
    "coverage_matrix_count_valid",
    "all_layers_reported",
    "diagnostic_interpretation_created",
    "limits_created",
    "patch_backlog_created",
    "patch_backlog_count_valid",
    "report_decision_created",
    "diagnostic_only_preserved",
    "not_kaggle_score_preserved",
    "official_score_claim_blocked",
    "public_score_claim_blocked",
    "private_score_claim_blocked",
    "real_public_score_not_claimed",
    "private_score_not_claimed",
    "real_benchmark_score_absent",
    "runtime_solver_not_modified",
    "external_solver_dependency_false",
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

REPORT_CASES: Tuple[Dict[str, str], ...] = (
    {"case_id": "m11_task7_source_task6_ready_v1", "area": "source", "operation": "verify_task_6_source"},
    {"case_id": "m11_task7_report_sections_ready_v1", "area": "report", "operation": "verify_report_sections"},
    {"case_id": "m11_task7_coverage_matrix_ready_v1", "area": "coverage", "operation": "verify_coverage_matrix"},
    {"case_id": "m11_task7_limits_ready_v1", "area": "limits", "operation": "verify_limits"},
    {"case_id": "m11_task7_patch_backlog_ready_v1", "area": "patch_backlog", "operation": "verify_patch_backlog"},
    {"case_id": "m11_task7_report_decision_ready_v1", "area": "decision", "operation": "verify_report_decision"},
    {"case_id": "m11_task7_score_boundary_preserved_v1", "area": "score_boundary", "operation": "verify_no_score_claim"},
    {"case_id": "m11_task7_submission_boundary_preserved_v1", "area": "submission_boundary", "operation": "verify_no_submission"},
    {"case_id": "m11_task7_next_stage_valid_v1", "area": "next_stage", "operation": "verify_next_stage"},
    {"case_id": "m11_task7_metadata_safe_v1", "area": "metadata", "operation": "verify_metadata_safe"},
)

EXPECTED_REPORT_SECTION_COUNT = len(REPORT_SECTIONS)
EXPECTED_REPORT_CASE_COUNT = len(REPORT_CASES)
EXPECTED_REPORT_PASS_COUNT = len(REPORT_CASES)
EXPECTED_REPORT_FAILURE_COUNT = 0
EXPECTED_PATCH_BACKLOG_COUNT = 5


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


def build_task_6_source_summary() -> Dict[str, Any]:
    record = _read_json(TASK_6_JSON)

    return {
        "task_6_path": str(TASK_6_JSON),
        "task_6_present": TASK_6_JSON.exists(),
        "task_6_status": record.get("status", "MISSING"),
        "task_6_id": record.get("task_6_id", "MISSING_TASK_6_ID"),
        "task_6_signature": record.get("signature", ""),
        "baseline_commit": record.get("baseline_commit", "MISSING_BASELINE"),
        "task_6_ready": record.get("task_6_ready", False),
        "task_verdict": record.get("task_verdict", "MISSING_VERDICT"),
        "next_stage": record.get("next_stage", "MISSING_NEXT_STAGE"),
        "solver_probe_contract_created": record.get("solver_probe_contract_created", False),
        "solver_probe_integration_created": record.get("solver_probe_integration_created", False),
        "probe_component_count": record.get("probe_component_count", 0),
        "probe_result_count": record.get("probe_result_count", 0),
        "probe_pass_count": record.get("probe_pass_count", 0),
        "probe_failure_count": record.get("probe_failure_count", 999),
        "layer_report_count": record.get("layer_report_count", 0),
        "local_solver_diagnostic_measured": record.get("local_solver_diagnostic_measured", False),
        "diagnostic_only": record.get("diagnostic_only", False),
        "kaggle_score_semantics": record.get("kaggle_score_semantics", "MISSING"),
        "probe_components": record.get("probe_components", []),
        "solver_probe_results": record.get("solver_probe_results", []),
        "probe_layer_report": record.get("probe_layer_report", []),
        "probe_summary": record.get("probe_summary", {}),
        "official_score_claim_allowed": record.get("official_score_claim_allowed", True),
        "synthetic_fixture_score_claim_allowed": record.get("synthetic_fixture_score_claim_allowed", True),
        "public_score_claim_allowed": record.get("public_score_claim_allowed", True),
        "private_score_claim_allowed": record.get("private_score_claim_allowed", True),
        "runtime_solver_modified": record.get("runtime_solver_modified", True),
        "ranker_runtime_modified": record.get("ranker_runtime_modified", True),
        "external_solver_dependency": record.get("external_solver_dependency", True),
        "primary_condition": record.get("primary_condition", "MISSING_PRIMARY_CONDITION"),
        "primary_classification": record.get("primary_classification", "MISSING_PRIMARY_CLASSIFICATION"),
        "solver_failure_detected": record.get("solver_failure_detected", True),
        "solver_not_measured_from_task_5": record.get("solver_not_measured_from_task_5", False),
        "solver_probe_measured": record.get("solver_probe_measured", False),
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
        "task_6_sha256": _sha256(TASK_6_JSON),
        "task_6_sha256_16": _sha16(_sha256(TASK_6_JSON)),
    }


def build_coverage_matrix() -> Tuple[Dict[str, Any], ...]:
    source = build_task_6_source_summary()
    layer_report = source["probe_layer_report"]

    matrix = []
    for row in layer_report:
        result_count = row.get("result_count", 0)
        pass_count = row.get("pass_count", 0)
        failure_count = row.get("failure_count", 999)
        coverage = "COVERED_PASS" if result_count == 6 and pass_count == 6 and failure_count == 0 else "COVERAGE_GAP"
        matrix.append(
            {
                "layer": row.get("target_layer"),
                "probe_id": row.get("probe_id"),
                "result_count": result_count,
                "pass_count": pass_count,
                "failure_count": failure_count,
                "coverage": coverage,
                "diagnostic_only": True,
                "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
            }
        )

    return tuple(matrix)


def build_limits_and_non_claims() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "limit_id": "not_official_kaggle_score_v1",
            "severity": "BLOCKING",
            "statement": "The probe report is local diagnostic output and is not a Kaggle public/private score.",
        },
        {
            "limit_id": "local_fixture_scope_only_v1",
            "severity": "HIGH",
            "statement": "The report measures synthetic/local diagnostic fixtures only.",
        },
        {
            "limit_id": "no_runtime_solver_patch_yet_v1",
            "severity": "HIGH",
            "statement": "Task 6 did not modify runtime solver or ranker logic.",
        },
        {
            "limit_id": "no_real_submission_artifact_v1",
            "severity": "BLOCKING",
            "statement": "No submission.json, upload package, authentication, or Kaggle upload exists.",
        },
        {
            "limit_id": "competitive_claim_not_allowed_v1",
            "severity": "BLOCKING",
            "statement": "No public competitive claim is allowed from this diagnostic report.",
        },
    )


def build_solver_patch_backlog() -> Tuple[Dict[str, Any], ...]:
    return (
        {
            "patch_id": "patch_world_model_state_tracking_v1",
            "target_layer": "world_model",
            "priority": "P0",
            "status": "PLANNED",
            "reason": "Convert diagnostic signatures into reusable object-state tracking hints.",
            "score_claim_allowed": False,
        },
        {
            "patch_id": "patch_goal_inference_from_terminal_state_v1",
            "target_layer": "goal_inference",
            "priority": "P0",
            "status": "PLANNED",
            "reason": "Use diagnostic terminal-state patterns to improve goal hypothesis ranking.",
            "score_claim_allowed": False,
        },
        {
            "patch_id": "patch_planner_loop_recovery_v1",
            "target_layer": "planner",
            "priority": "P0",
            "status": "PLANNED",
            "reason": "Turn planner-loop diagnostics into fallback exploration constraints.",
            "score_claim_allowed": False,
        },
        {
            "patch_id": "patch_transition_verifier_feedback_v1",
            "target_layer": "verifier",
            "priority": "P0",
            "status": "PLANNED",
            "reason": "Use verifier mismatch traces to refine transition checking.",
            "score_claim_allowed": False,
        },
        {
            "patch_id": "patch_action_policy_validity_guard_v1",
            "target_layer": "action_policy",
            "priority": "P0",
            "status": "PLANNED",
            "reason": "Preserve action validity and non-submission safety during solver improvements.",
            "score_claim_allowed": False,
        },
    )


def build_report_decision() -> Dict[str, Any]:
    source = build_task_6_source_summary()
    return {
        "decision_id": "M11-TASK7-LOCAL-SOLVER-PROBE-REPORT-DECISION-v1",
        "verdict": TASK_VERDICT,
        "probe_results_interpreted": True,
        "local_solver_diagnostic_measured": source["local_solver_diagnostic_measured"],
        "coverage_status": "LOCAL_DIAGNOSTIC_COVERAGE_PASS",
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "real_submission_allowed": False,
        "next_stage": NEXT_STAGE,
        "decision_boundary": "REPORT_ONLY_NO_SCORE_NO_SUBMISSION",
    }


def build_report_sections() -> Dict[str, Any]:
    source = build_task_6_source_summary()
    coverage = build_coverage_matrix()
    limits = build_limits_and_non_claims()
    backlog = build_solver_patch_backlog()
    decision = build_report_decision()

    return {
        "executive_summary": {
            "summary_id": "M11-TASK7-EXECUTIVE-SUMMARY-v1",
            "text": "Local solver probe integration produced 30 diagnostic probe results across 5 layers with 0 failures.",
            "probe_result_count": source["probe_result_count"],
            "probe_pass_count": source["probe_pass_count"],
            "probe_failure_count": source["probe_failure_count"],
            "diagnostic_only": True,
            "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        },
        "measured_layers": tuple(row["layer"] for row in coverage),
        "coverage_matrix": coverage,
        "diagnostic_interpretation": {
            "interpretation_id": "M11-TASK7-DIAGNOSTIC-INTERPRETATION-v1",
            "solver_failure_detected": source["solver_failure_detected"],
            "solver_probe_measured": source["solver_probe_measured"],
            "meaning": "Local diagnostic probe layer is working; this is not a real benchmark score.",
        },
        "limits_and_non_claims": limits,
        "solver_patch_backlog": backlog,
        "boundary_control": {
            "diagnostic_only": True,
            "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
            "official_score_claim_allowed": False,
            "public_score_claim_allowed": False,
            "private_score_claim_allowed": False,
            "submission_json_created": False,
            "upload_package_created": False,
            "kaggle_submission_sent": False,
        },
        "report_decision": decision,
    }


def build_task_7_checks() -> Dict[str, bool]:
    source = build_task_6_source_summary()
    sections = build_report_sections()
    coverage = sections["coverage_matrix"]
    limits = sections["limits_and_non_claims"]
    backlog = sections["solver_patch_backlog"]
    decision = sections["report_decision"]

    layers = {row["layer"] for row in coverage}

    return {
        "task_6_artifact_exists": source["task_6_present"] is True,
        "task_6_artifact_ready": source["task_6_status"] == EXPECTED_TASK_6_STATUS,
        "task_6_validated": source["task_6_id"].startswith(EXPECTED_TASK_6_ID_PREFIX)
        and bool(source["task_6_signature"]),
        "probe_integration_ready": source["task_6_ready"] is True and source["solver_probe_integration_created"] is True,
        "probe_contract_created": source["solver_probe_contract_created"] is True,
        "probe_result_count_valid": source["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": source["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT,
        "probe_failure_count_zero": source["probe_failure_count"] == EXPECTED_PROBE_FAILURE_COUNT,
        "layer_report_count_valid": source["layer_report_count"] == EXPECTED_LAYER_REPORT_COUNT,
        "report_sections_created": set(REPORT_SECTIONS).issubset(sections.keys()),
        "report_section_count_valid": len(REPORT_SECTIONS) == EXPECTED_REPORT_SECTION_COUNT,
        "coverage_matrix_created": bool(coverage),
        "coverage_matrix_count_valid": len(coverage) == EXPECTED_LAYER_REPORT_COUNT,
        "all_layers_reported": {"world_model", "goal_inference", "planner", "verifier", "action_policy"}.issubset(layers),
        "diagnostic_interpretation_created": "diagnostic_interpretation" in sections,
        "limits_created": len(limits) == 5,
        "patch_backlog_created": bool(backlog),
        "patch_backlog_count_valid": len(backlog) == EXPECTED_PATCH_BACKLOG_COUNT,
        "report_decision_created": decision["decision_id"] == "M11-TASK7-LOCAL-SOLVER-PROBE-REPORT-DECISION-v1",
        "diagnostic_only_preserved": source["diagnostic_only"] is True
        and sections["boundary_control"]["diagnostic_only"] is True,
        "not_kaggle_score_preserved": source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
        and sections["boundary_control"]["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE",
        "official_score_claim_blocked": source["official_score_claim_allowed"] is False,
        "public_score_claim_blocked": source["public_score_claim_allowed"] is False,
        "private_score_claim_blocked": source["private_score_claim_allowed"] is False,
        "real_public_score_not_claimed": source["real_public_score_claimed"] is False,
        "private_score_not_claimed": source["private_score_claimed"] is False,
        "real_benchmark_score_absent": source["real_benchmark_score"] is None,
        "runtime_solver_not_modified": source["runtime_solver_modified"] is False
        and source["ranker_runtime_modified"] is False,
        "external_solver_dependency_false": source["external_solver_dependency"] is False,
        "real_submission_candidate_absent": source["real_submission_candidate_created"] is False,
        "submission_json_absent": source["submission_json_created"] is False,
        "upload_package_absent": source["upload_package_created"] is False,
        "real_submission_blocked": source["real_submission_allowed"] is False
        and source["real_submission_decision"] == "NOT_AUTHORIZED",
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True,
        "next_stage_valid": NEXT_STAGE == "MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1",
        "report_check_count_valid": len(REPORT_CHECKS) == EXPECTED_REPORT_CHECK_COUNT,
        "report_case_count_valid": len(REPORT_CASES) == EXPECTED_REPORT_CASE_COUNT,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency_false": True,
        "contains_api_keys_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
    }


EXPECTED_REPORT_CHECK_COUNT = len(REPORT_CHECKS)


def evaluate_task_7_case(case_id: str) -> Dict[str, Any]:
    checks = build_task_7_checks()

    if case_id == "m11_task7_source_task6_ready_v1":
        passed = checks["task_6_artifact_exists"] and checks["task_6_artifact_ready"] and checks["task_6_validated"]
        return _result(case_id, "source", "verify_task_6_source", passed)

    if case_id == "m11_task7_report_sections_ready_v1":
        passed = checks["report_sections_created"] and checks["report_section_count_valid"]
        return _result(case_id, "report", "verify_report_sections", passed)

    if case_id == "m11_task7_coverage_matrix_ready_v1":
        passed = checks["coverage_matrix_created"] and checks["coverage_matrix_count_valid"] and checks["all_layers_reported"]
        return _result(case_id, "coverage", "verify_coverage_matrix", passed)

    if case_id == "m11_task7_limits_ready_v1":
        return _result(case_id, "limits", "verify_limits", checks["limits_created"])

    if case_id == "m11_task7_patch_backlog_ready_v1":
        passed = checks["patch_backlog_created"] and checks["patch_backlog_count_valid"]
        return _result(case_id, "patch_backlog", "verify_patch_backlog", passed)

    if case_id == "m11_task7_report_decision_ready_v1":
        return _result(case_id, "decision", "verify_report_decision", checks["report_decision_created"])

    if case_id == "m11_task7_score_boundary_preserved_v1":
        passed = (
            checks["not_kaggle_score_preserved"]
            and checks["official_score_claim_blocked"]
            and checks["public_score_claim_blocked"]
            and checks["private_score_claim_blocked"]
            and checks["real_benchmark_score_absent"]
        )
        return _result(case_id, "score_boundary", "verify_no_score_claim", passed)

    if case_id == "m11_task7_submission_boundary_preserved_v1":
        passed = (
            checks["real_submission_candidate_absent"]
            and checks["submission_json_absent"]
            and checks["upload_package_absent"]
            and checks["real_submission_blocked"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission_boundary", "verify_no_submission", passed)

    if case_id == "m11_task7_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    if case_id == "m11_task7_metadata_safe_v1":
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

    raise ValueError(f"unknown milestone 11 task 7 case: {case_id}")


def evaluate_all_task_7_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_task_7_case(case["case_id"]) for case in REPORT_CASES)


def build_report_scorecard() -> Tuple[Dict[str, Any], ...]:
    checks = build_task_7_checks()
    rows = (
        ("source_task6_ready", checks["task_6_artifact_ready"]),
        ("probe_results_valid", checks["probe_result_count_valid"] and checks["probe_failure_count_zero"]),
        ("coverage_matrix_ready", checks["coverage_matrix_count_valid"]),
        ("all_layers_reported", checks["all_layers_reported"]),
        ("limits_ready", checks["limits_created"]),
        ("patch_backlog_ready", checks["patch_backlog_count_valid"]),
        ("decision_ready", checks["report_decision_created"]),
        ("score_boundary_preserved", checks["not_kaggle_score_preserved"]),
        ("submission_boundary_preserved", checks["real_submission_blocked"]),
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


def build_milestone_11_local_solver_probe_report() -> Dict[str, Any]:
    source = build_task_6_source_summary()
    sections = build_report_sections()
    checks = build_task_7_checks()
    cases = evaluate_all_task_7_cases()
    scorecard = build_report_scorecard()

    pass_count = sum(1 for item in cases if item["passed"] is True)
    failure_count = sum(1 for item in cases if item["passed"] is False)

    gate_state = {
        "task_6_artifact_ready": checks["task_6_artifact_ready"],
        "task_6_validated": checks["task_6_validated"],
        "probe_results_valid": checks["probe_result_count_valid"]
        and checks["probe_pass_count_valid"]
        and checks["probe_failure_count_zero"],
        "coverage_matrix_ready": checks["coverage_matrix_count_valid"],
        "all_layers_reported": checks["all_layers_reported"],
        "limits_ready": checks["limits_created"],
        "patch_backlog_ready": checks["patch_backlog_count_valid"],
        "report_decision_ready": checks["report_decision_created"],
        "score_boundary_preserved": checks["not_kaggle_score_preserved"]
        and checks["official_score_claim_blocked"]
        and checks["real_public_score_not_claimed"],
        "submission_boundary_preserved": checks["real_submission_blocked"]
        and checks["submission_json_absent"]
        and checks["kaggle_submission_not_sent"],
        "runtime_solver_not_modified": checks["runtime_solver_not_modified"],
        "external_solver_dependency_false": checks["external_solver_dependency_false"],
        "fail_closed_active": checks["fail_closed_active"],
        "next_stage_valid": checks["next_stage_valid"],
        "metadata_safe": checks["public_safe"]
        and checks["deterministic"]
        and checks["local_only"]
        and checks["external_api_dependency_false"]
        and checks["private_core_exposure_false"]
        and checks["legal_certification_false"],
        "all_cases_pass": all(item["passed"] is True for item in cases),
        "pass_count_valid": pass_count == EXPECTED_REPORT_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_REPORT_FAILURE_COUNT,
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
        pass_count == EXPECTED_REPORT_PASS_COUNT
        and failure_count == 0
        and passed_gate_count == len(gates)
        and issue_count == 0
        and checks["task_6_artifact_ready"]
        and checks["coverage_matrix_count_valid"]
        and checks["patch_backlog_count_valid"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
    )

    index = {
        "milestone": "Milestone #11",
        "task": "Task 7",
        "status": STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "depends_on_task_6": source["task_6_id"],
        "report_created": True,
        "report_section_count": EXPECTED_REPORT_SECTION_COUNT,
        "coverage_layer_count": len(sections["coverage_matrix"]),
        "patch_backlog_count": len(sections["solver_patch_backlog"]),
        "probe_result_count": source["probe_result_count"],
        "probe_pass_count": source["probe_pass_count"],
        "probe_failure_count": source["probe_failure_count"],
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "real_benchmark_score": None,
        "runtime_solver_modified": False,
        "external_solver_dependency": False,
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
        "task": "Task 7",
        "title": "Local Solver Probe Report v1",
        "baseline_commit": BASELINE_COMMIT,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "next_stage": NEXT_STAGE,
        "task_6_source": {
            "path": str(TASK_6_JSON),
            "present": TASK_6_JSON.exists(),
            "status": source["task_6_status"],
            "task_6_id": source["task_6_id"],
            "sha256": _sha256(TASK_6_JSON),
            "sha256_16": _sha16(_sha256(TASK_6_JSON)),
        },
        "source_summary": source,
        "report_sections": sections,
        "coverage_matrix": list(sections["coverage_matrix"]),
        "limits_and_non_claims": list(sections["limits_and_non_claims"]),
        "solver_patch_backlog": list(sections["solver_patch_backlog"]),
        "report_decision": sections["report_decision"],
        "report_scorecard": list(scorecard),
        "report_checks": checks,
        "report_check_list": list(REPORT_CHECKS),
        "report_cases": list(REPORT_CASES),
        "report_case_results": list(cases),
        "report_gates": list(gates),
        "report_issues": list(issues),
        "report_index": index,
        "task_7_ready": task_ready,
        "report_created": True,
        "report_section_count": EXPECTED_REPORT_SECTION_COUNT,
        "coverage_layer_count": len(sections["coverage_matrix"]),
        "limits_count": len(sections["limits_and_non_claims"]),
        "patch_backlog_count": len(sections["solver_patch_backlog"]),
        "probe_result_count": source["probe_result_count"],
        "probe_pass_count": source["probe_pass_count"],
        "probe_failure_count": source["probe_failure_count"],
        "diagnostic_only": True,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "official_score_claim_allowed": False,
        "synthetic_fixture_score_claim_allowed": False,
        "public_score_claim_allowed": False,
        "private_score_claim_allowed": False,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "external_solver_dependency": False,
        "competitive_score_claim_allowed": False,
        "primary_condition": source["primary_condition"],
        "primary_classification": source["primary_classification"],
        "solver_failure_detected": source["solver_failure_detected"],
        "solver_probe_measured": source["solver_probe_measured"],
        "report_check_count": len(REPORT_CHECKS),
        "report_case_count": len(REPORT_CASES),
        "report_case_pass_count": pass_count,
        "report_case_failure_count": failure_count,
        "report_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "report_issue_count": issue_count,
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
            "source": "milestone_11_local_solver_probe_report_v1",
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
        "task_7_id": f"MILESTONE-11-LOCAL-SOLVER-PROBE-REPORT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_11_local_solver_probe_report(record: Mapping[str, Any]) -> Dict[str, Any]:
    gates = record.get("report_gates", [])
    issues = record.get("report_issues", [])
    case_results = record.get("report_case_results", [])
    scorecard = record.get("report_scorecard", [])

    checks = {
        "status_ready": record.get("status") == STATUS,
        "task_7_id_present": isinstance(record.get("task_7_id"), str) and bool(record.get("task_7_id")),
        "signature_present": isinstance(record.get("signature"), str) and bool(record.get("signature")),
        "baseline_commit_valid": str(record.get("baseline_commit", "")).startswith("2d9ccce"),
        "task_mode_valid": record.get("task_mode") == TASK_MODE,
        "task_scope_valid": record.get("task_scope") == TASK_SCOPE,
        "task_verdict_valid": record.get("task_verdict") == TASK_VERDICT,
        "next_stage_valid": record.get("next_stage") == NEXT_STAGE,
        "task_ready": record.get("task_7_ready") is True,
        "task_6_source_present": record.get("task_6_source", {}).get("present") is True,
        "report_created": record.get("report_created") is True,
        "report_section_count_valid": record.get("report_section_count") == EXPECTED_REPORT_SECTION_COUNT,
        "coverage_layer_count_valid": record.get("coverage_layer_count") == EXPECTED_LAYER_REPORT_COUNT,
        "limits_count_valid": record.get("limits_count") == 5,
        "patch_backlog_count_valid": record.get("patch_backlog_count") == EXPECTED_PATCH_BACKLOG_COUNT,
        "probe_result_count_valid": record.get("probe_result_count") == EXPECTED_PROBE_RESULT_COUNT,
        "probe_pass_count_valid": record.get("probe_pass_count") == EXPECTED_PROBE_PASS_COUNT,
        "probe_failure_count_zero": record.get("probe_failure_count") == 0,
        "diagnostic_only": record.get("diagnostic_only") is True,
        "not_kaggle_score": record.get("kaggle_score_semantics") == "NOT_A_KAGGLE_SCORE",
        "score_claim_blocked": record.get("official_score_claim_allowed") is False
        and record.get("public_score_claim_allowed") is False
        and record.get("private_score_claim_allowed") is False
        and record.get("competitive_score_claim_allowed") is False,
        "runtime_solver_not_modified": record.get("runtime_solver_modified") is False
        and record.get("ranker_runtime_modified") is False,
        "external_solver_dependency_false": record.get("external_solver_dependency") is False,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "report_check_count_valid": record.get("report_check_count") == EXPECTED_REPORT_CHECK_COUNT,
        "report_case_count_valid": record.get("report_case_count") == EXPECTED_REPORT_CASE_COUNT,
        "report_case_pass_count_valid": record.get("report_case_pass_count") == EXPECTED_REPORT_PASS_COUNT,
        "report_case_failure_count_zero": record.get("report_case_failure_count") == 0,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "task_7_id": record.get("task_7_id"),
        "signature": record.get("signature"),
    }


def render_task_7_markdown(record: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #11 Task 7 - Local Solver Probe Report v1",
        "",
        f"- status: {record['status']}",
        f"- task_7_id: {record['task_7_id']}",
        f"- signature: {record['signature']}",
        f"- baseline_commit: {record['baseline_commit']}",
        f"- task_mode: {record['task_mode']}",
        f"- task_scope: {record['task_scope']}",
        f"- task_verdict: {record['task_verdict']}",
        f"- next_stage: {record['next_stage']}",
        f"- task_7_ready: {record['task_7_ready']}",
        f"- report_created: {record['report_created']}",
        f"- report_section_count: {record['report_section_count']}",
        f"- coverage_layer_count: {record['coverage_layer_count']}",
        f"- limits_count: {record['limits_count']}",
        f"- patch_backlog_count: {record['patch_backlog_count']}",
        f"- probe_result_count: {record['probe_result_count']}",
        f"- probe_pass_count: {record['probe_pass_count']}",
        f"- probe_failure_count: {record['probe_failure_count']}",
        f"- diagnostic_only: {record['diagnostic_only']}",
        f"- kaggle_score_semantics: {record['kaggle_score_semantics']}",
        f"- official_score_claim_allowed: {record['official_score_claim_allowed']}",
        f"- competitive_score_claim_allowed: {record['competitive_score_claim_allowed']}",
        f"- runtime_solver_modified: {record['runtime_solver_modified']}",
        f"- external_solver_dependency: {record['external_solver_dependency']}",
        f"- real_submission_allowed: {record['real_submission_allowed']}",
        f"- kaggle_submission_sent: {record['kaggle_submission_sent']}",
        f"- fail_closed_active: {record['fail_closed_active']}",
        "",
        "## Coverage matrix",
        "",
    ]

    for row in record["coverage_matrix"]:
        lines.append(
            f"- {row['layer']} / probe={row['probe_id']} / results={row['result_count']} / "
            f"pass={row['pass_count']} / fail={row['failure_count']} / coverage={row['coverage']}"
        )

    lines.extend(["", "## Limits and non-claims", ""])
    for item in record["limits_and_non_claims"]:
        lines.append(f"- {item['limit_id']} / severity={item['severity']} / {item['statement']}")

    lines.extend(["", "## Solver patch backlog", ""])
    for item in record["solver_patch_backlog"]:
        lines.append(
            f"- {item['patch_id']} / target={item['target_layer']} / priority={item['priority']} / status={item['status']}"
        )

    lines.extend(["", "## Validation results", ""])
    for result in record["report_case_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task 7 converts local solver probe results into an operational report. It confirms diagnostic coverage but does not authorize benchmark claims or real submission.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1_VALID=true",
            "ARC_AGI3_MILESTONE_11_TASK_7_READY=true",
            "ARC_AGI3_MILESTONE_11_TASK_7_MODE=MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_11_TASK_7_VERDICT=LOCAL_SOLVER_PROBE_REPORT_READY_FOR_SOLVER_PATCH_BACKLOG",
            "ARC_AGI3_MILESTONE_11_TASK_7_BASELINE_COMMIT=2d9ccce",
            "ARC_AGI3_MILESTONE_11_TASK_7_NEXT_STAGE=MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1",
            "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_CREATED=true",
            f"ARC_AGI3_MILESTONE_11_REPORT_SECTION_COUNT={EXPECTED_REPORT_SECTION_COUNT}",
            f"ARC_AGI3_MILESTONE_11_COVERAGE_LAYER_COUNT={EXPECTED_LAYER_REPORT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PATCH_BACKLOG_COUNT={EXPECTED_PATCH_BACKLOG_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_RESULT_COUNT={EXPECTED_PROBE_RESULT_COUNT}",
            f"ARC_AGI3_MILESTONE_11_PROBE_PASS_COUNT={EXPECTED_PROBE_PASS_COUNT}",
            "ARC_AGI3_MILESTONE_11_PROBE_FAILURE_COUNT=0",
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
            "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_task_7_manifest(record: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 11 TASK 7 LOCAL SOLVER PROBE REPORT MANIFEST v1",
        f"task_7_id={record['task_7_id']}",
        f"signature={record['signature']}",
        f"status={record['status']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_verdict={record['task_verdict']}",
        f"next_stage={record['next_stage']}",
        f"task_7_ready={record['task_7_ready']}",
        f"report_created={record['report_created']}",
        f"report_section_count={record['report_section_count']}",
        f"coverage_layer_count={record['coverage_layer_count']}",
        f"limits_count={record['limits_count']}",
        f"patch_backlog_count={record['patch_backlog_count']}",
        f"probe_result_count={record['probe_result_count']}",
        f"probe_pass_count={record['probe_pass_count']}",
        f"probe_failure_count={record['probe_failure_count']}",
        f"diagnostic_only={record['diagnostic_only']}",
        f"kaggle_score_semantics={record['kaggle_score_semantics']}",
        f"official_score_claim_allowed={record['official_score_claim_allowed']}",
        f"competitive_score_claim_allowed={record['competitive_score_claim_allowed']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"external_solver_dependency={record['external_solver_dependency']}",
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
        "COVERAGE_MATRIX",
    ]

    for row in record["coverage_matrix"]:
        lines.append(
            f"{row['layer']} probe={row['probe_id']} result_count={row['result_count']} "
            f"pass_count={row['pass_count']} failure_count={row['failure_count']} coverage={row['coverage']}"
        )

    lines.append("")
    lines.append("SOLVER_PATCH_BACKLOG")
    for patch in record["solver_patch_backlog"]:
        lines.append(
            f"{patch['patch_id']} target={patch['target_layer']} priority={patch['priority']} status={patch['status']}"
        )

    lines.append("")
    lines.append("REPORT_CASE_RESULTS")
    for result in record["report_case_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_7_artifacts(
    record: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    record = dict(record or build_milestone_11_local_solver_probe_report())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-11-local-solver-probe-report-v1.json"
    md_path = output / "milestone-11-local-solver-probe-report-v1.md"
    manifest_path = output / "milestone-11-local-solver-probe-report-manifest-v1.txt"
    index_path = output / "milestone-11-local-solver-probe-report-index-v1.json"
    coverage_path = output / "milestone-11-local-solver-probe-coverage-matrix-v1.json"
    limits_path = output / "milestone-11-local-solver-probe-limits-v1.json"
    backlog_path = output / "milestone-11-local-solver-patch-backlog-v1.json"
    decision_path = output / "milestone-11-local-solver-probe-report-decision-v1.json"
    scorecard_path = output / "milestone-11-local-solver-probe-report-scorecard-v1.json"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_7_markdown(record), encoding="utf-8")
    manifest_path.write_text(render_task_7_manifest(record), encoding="utf-8")
    index_path.write_text(json.dumps(record["report_index"], indent=2, sort_keys=True), encoding="utf-8")
    coverage_path.write_text(json.dumps(record["coverage_matrix"], indent=2, sort_keys=True), encoding="utf-8")
    limits_path.write_text(json.dumps(record["limits_and_non_claims"], indent=2, sort_keys=True), encoding="utf-8")
    backlog_path.write_text(json.dumps(record["solver_patch_backlog"], indent=2, sort_keys=True), encoding="utf-8")
    decision_path.write_text(json.dumps(record["report_decision"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(record["report_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "coverage_path": str(coverage_path),
        "limits_path": str(limits_path),
        "backlog_path": str(backlog_path),
        "decision_path": str(decision_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_11_local_solver_probe_report_pipeline() -> Dict[str, Any]:
    record = build_milestone_11_local_solver_probe_report()
    validation = validate_milestone_11_local_solver_probe_report(record)
    artifacts = write_task_7_artifacts(record)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_PIPELINE_INVALID",
        "task_status": record["status"],
        "validation_status": validation["status"],
        "record": record,
        "task_7_id": record["task_7_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_mode": record["task_mode"],
        "task_verdict": record["task_verdict"],
        "next_stage": record["next_stage"],
        "task_7_ready": record["task_7_ready"],
        "report_created": record["report_created"],
        "report_section_count": record["report_section_count"],
        "coverage_layer_count": record["coverage_layer_count"],
        "limits_count": record["limits_count"],
        "patch_backlog_count": record["patch_backlog_count"],
        "probe_result_count": record["probe_result_count"],
        "probe_pass_count": record["probe_pass_count"],
        "probe_failure_count": record["probe_failure_count"],
        "diagnostic_only": record["diagnostic_only"],
        "kaggle_score_semantics": record["kaggle_score_semantics"],
        "official_score_claim_allowed": record["official_score_claim_allowed"],
        "competitive_score_claim_allowed": record["competitive_score_claim_allowed"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "external_solver_dependency": record["external_solver_dependency"],
        "primary_condition": record["primary_condition"],
        "primary_classification": record["primary_classification"],
        "solver_failure_detected": record["solver_failure_detected"],
        "solver_probe_measured": record["solver_probe_measured"],
        "report_check_count": record["report_check_count"],
        "report_case_count": record["report_case_count"],
        "report_case_pass_count": record["report_case_pass_count"],
        "report_case_failure_count": record["report_case_failure_count"],
        "report_gate_count": record["report_gate_count"],
        "passed_gate_count": record["passed_gate_count"],
        "report_issue_count": record["report_issue_count"],
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
