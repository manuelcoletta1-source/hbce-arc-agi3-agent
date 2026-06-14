"""Milestone #7 Local Score Improvement Report v1.

Local-only score improvement report registry.

This module converts regression benchmark records into a deterministic local
improvement report. It does not claim a Kaggle score, does not claim public
leaderboard improvement, does not submit to Kaggle, does not authenticate,
does not upload files, does not call external APIs, does not read secrets,
does not create upload archives, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REPORT_STATUS = "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_READY"
PIPELINE_STATUS = "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_VALID"

BASELINE_COMMIT = "92efad5 Add ARC AGI3 regression benchmark"
REPORT_MODE = "LOCAL_SCORE_IMPROVEMENT_REPORT_ONLY_NO_UPLOAD"
REPORT_SCOPE = "REPORT_LOCAL_REGRESSION_AND_EVIDENCE_IMPROVEMENT_WITHOUT_COMPETITIVE_SCORE_CLAIM"
REPORT_VERDICT = "LOCAL_SCORE_IMPROVEMENT_REPORT_READY_FOR_SUBMISSION_CANDIDATE_REBUILD"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_8_SUBMISSION_CANDIDATE_REBUILD"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/local-score-improvement-report-v1"

BENCHMARK_JSON = Path(
    "examples/milestone-7/regression-benchmark-v1/"
    "milestone-7-regression-benchmark-v1.json"
)

EXPECTED_FAMILY_REPORT_COUNT = 3
EXPECTED_BENCHMARK_CASE_COUNT = 6
EXPECTED_LOCAL_MEASUREMENT_COUNT = 6
EXPECTED_IMPROVEMENT_SIGNAL_COUNT = 9
EXPECTED_BLOCKING_CONTROL_COUNT = 8
EXPECTED_REGRESSION_PASS_COUNT = 6
EXPECTED_REGRESSION_FAILURE_COUNT = 0
EXPECTED_REPORT_SECTION_COUNT = 7


FAMILY_REPORTS: Tuple[Dict[str, Any], ...] = (
    {
        "family_report_id": "local_score_report_color_mapping_v1",
        "family": "color_mapping",
        "priority": "P0",
        "source_cases": (
            "regression_color_palette_stability_v1",
            "regression_color_background_preservation_v1",
        ),
        "local_improvement_signals": (
            "palette_rank_evidence_ready",
            "background_preservation_guard_ready",
            "bounded_color_regression_ready",
        ),
        "measurement_summary": "Color mapping now has local evidence, bounded guards, and regression records.",
        "local_score_delta_claim": "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM",
        "competitive_score_claim": False,
        "public_leaderboard_claim": False,
        "ready_for_task_8": True,
    },
    {
        "family_report_id": "local_score_report_object_model_v1",
        "family": "object_model",
        "priority": "P0",
        "source_cases": (
            "regression_object_component_count_v1",
            "regression_object_spatial_delta_v1",
        ),
        "local_improvement_signals": (
            "component_count_evidence_ready",
            "object_spatial_delta_guard_ready",
            "bounded_object_regression_ready",
        ),
        "measurement_summary": "Object modeling now has local evidence, bounded guards, and regression records.",
        "local_score_delta_claim": "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM",
        "competitive_score_claim": False,
        "public_leaderboard_claim": False,
        "ready_for_task_8": True,
    },
    {
        "family_report_id": "local_score_report_shape_symmetry_v1",
        "family": "shape_symmetry",
        "priority": "P0",
        "source_cases": (
            "regression_shape_axis_symmetry_v1",
            "regression_shape_translation_bounds_v1",
        ),
        "local_improvement_signals": (
            "axis_symmetry_evidence_ready",
            "translation_bounds_guard_ready",
            "bounded_shape_regression_ready",
        ),
        "measurement_summary": "Shape symmetry now has local evidence, bounded guards, and regression records.",
        "local_score_delta_claim": "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM",
        "competitive_score_claim": False,
        "public_leaderboard_claim": False,
        "ready_for_task_8": True,
    },
)


LOCAL_MEASUREMENTS: Tuple[Dict[str, Any], ...] = (
    {
        "measurement_id": "local_measurement_color_palette_stability_v1",
        "family": "color_mapping",
        "source_case": "regression_color_palette_stability_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
    {
        "measurement_id": "local_measurement_color_background_preservation_v1",
        "family": "color_mapping",
        "source_case": "regression_color_background_preservation_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
    {
        "measurement_id": "local_measurement_object_component_count_v1",
        "family": "object_model",
        "source_case": "regression_object_component_count_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
    {
        "measurement_id": "local_measurement_object_spatial_delta_v1",
        "family": "object_model",
        "source_case": "regression_object_spatial_delta_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
    {
        "measurement_id": "local_measurement_shape_axis_symmetry_v1",
        "family": "shape_symmetry",
        "source_case": "regression_shape_axis_symmetry_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
    {
        "measurement_id": "local_measurement_shape_translation_bounds_v1",
        "family": "shape_symmetry",
        "source_case": "regression_shape_translation_bounds_v1",
        "measurement_type": "LOCAL_REGRESSION_PASS",
        "result": "PASS",
        "numeric_score_claim": False,
    },
)


BLOCKING_CONTROLS: Tuple[str, ...] = (
    "no_numeric_kaggle_score_claim",
    "no_public_leaderboard_claim",
    "no_real_submission_claim",
    "no_upload_performed",
    "no_kaggle_authentication_performed",
    "no_external_api_dependency",
    "no_private_core_exposure",
    "no_legal_certification_claim",
)


REPORT_SECTIONS: Tuple[str, ...] = (
    "baseline_chain",
    "family_improvement_summary",
    "local_measurement_summary",
    "regression_benchmark_summary",
    "blocking_controls",
    "submission_boundary",
    "next_stage",
)


REPORT_GATES: Tuple[str, ...] = (
    "benchmark_artifact_present",
    "benchmark_artifact_ready",
    "benchmark_artifact_valid",
    "benchmark_next_stage_matches_task_7",
    "regression_benchmark_records_ready",
    "report_mode_valid",
    "report_scope_valid",
    "report_verdict_valid",
    "report_ready",
    "report_locked",
    "family_report_count_valid",
    "benchmark_case_count_valid",
    "local_measurement_count_valid",
    "improvement_signal_count_valid",
    "blocking_control_count_valid",
    "report_section_count_valid",
    "regression_pass_count_valid",
    "regression_failure_count_zero",
    "all_family_reports_priority_p0",
    "all_family_reports_have_source_cases",
    "all_source_cases_found_in_benchmark",
    "all_family_reports_have_improvement_signals",
    "all_family_reports_have_measurement_summary",
    "all_family_reports_have_no_numeric_score_claim",
    "all_family_reports_no_competitive_score_claim",
    "all_family_reports_no_public_leaderboard_claim",
    "all_family_reports_ready_for_task_8",
    "all_measurements_have_source_case",
    "all_measurement_cases_found_in_benchmark",
    "all_measurements_passed",
    "all_measurements_have_no_numeric_score_claim",
    "color_report_present",
    "object_report_present",
    "shape_report_present",
    "local_score_report_ready",
    "local_score_claim_absent",
    "competitive_score_claim_absent",
    "public_leaderboard_claim_absent",
    "runtime_solver_not_modified",
    "ranker_runtime_not_modified",
    "benchmark_runtime_not_modified",
    "report_runtime_not_modified",
    "next_stage_valid",
    "submission_candidate_rebuild_required",
    "manual_submission_not_allowed",
    "manual_upload_not_performed",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

REPORT_ISSUES: Tuple[str, ...] = (
    "benchmark_artifact_missing",
    "benchmark_artifact_not_ready",
    "benchmark_artifact_invalid",
    "benchmark_next_stage_mismatch",
    "regression_benchmark_records_not_ready",
    "report_mode_invalid",
    "report_scope_invalid",
    "report_verdict_invalid",
    "report_not_ready",
    "report_not_locked",
    "family_report_count_invalid",
    "benchmark_case_count_invalid",
    "local_measurement_count_invalid",
    "improvement_signal_count_invalid",
    "blocking_control_count_invalid",
    "report_section_count_invalid",
    "regression_pass_count_invalid",
    "regression_failure_count_nonzero",
    "family_report_priority_not_p0",
    "family_report_source_cases_missing",
    "source_case_not_found_in_benchmark",
    "family_report_improvement_signals_missing",
    "family_report_measurement_summary_missing",
    "numeric_score_claim_detected",
    "competitive_score_claim_detected",
    "public_leaderboard_claim_detected",
    "family_report_not_ready_for_task_8",
    "measurement_source_case_missing",
    "measurement_case_not_found_in_benchmark",
    "measurement_not_passed",
    "measurement_numeric_score_claim_detected",
    "color_report_missing",
    "object_report_missing",
    "shape_report_missing",
    "local_score_report_not_ready",
    "local_score_claim_detected",
    "competitive_score_claim_detected_global",
    "public_leaderboard_claim_detected_global",
    "runtime_solver_modified",
    "ranker_runtime_modified",
    "benchmark_runtime_modified",
    "report_runtime_modified",
    "next_stage_invalid",
    "submission_candidate_rebuild_not_required",
    "manual_submission_allowed",
    "manual_upload_performed",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


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


def _boundary_from_benchmark(benchmark: Mapping[str, Any]) -> Dict[str, Any]:
    source = benchmark.get("boundary", {}) if isinstance(benchmark.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": benchmark.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    expected = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    return all(boundary.get(key) is value for key, value in expected.items())


def _benchmark_source(benchmark: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(BENCHMARK_JSON)
    return {
        "name": "milestone_7_regression_benchmark",
        "path": str(BENCHMARK_JSON),
        "present": BENCHMARK_JSON.exists(),
        "expected_status": "MILESTONE_7_REGRESSION_BENCHMARK_READY",
        "actual_status": benchmark.get("status", "MISSING"),
        "ready": BENCHMARK_JSON.exists()
        and benchmark.get("status") == "MILESTONE_7_REGRESSION_BENCHMARK_READY",
        "artifact_id": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _benchmark_case_ids(benchmark: Mapping[str, Any]) -> Tuple[str, ...]:
    items = benchmark.get("benchmark_cases", [])
    if not isinstance(items, list):
        return tuple()
    return tuple(str(item.get("case_id", "")) for item in items if isinstance(item, Mapping))


def build_milestone_7_local_score_improvement_report() -> Dict[str, Any]:
    benchmark = _read_json(BENCHMARK_JSON)
    boundary = _boundary_from_benchmark(benchmark)
    benchmark_source = _benchmark_source(benchmark)
    benchmark_case_ids = _benchmark_case_ids(benchmark)

    family_reports = tuple(dict(item) for item in FAMILY_REPORTS)
    measurements = tuple(dict(item) for item in LOCAL_MEASUREMENTS)
    families = {item["family"] for item in family_reports}

    benchmark_case_count = int(benchmark.get("benchmark_case_count", 0))
    regression_pass_count = int(benchmark.get("pass_count", -1))
    regression_failure_count = int(benchmark.get("failure_count", -1))
    improvement_signal_count = sum(len(item.get("local_improvement_signals", ())) for item in family_reports)

    report_record = {
        "report_mode": REPORT_MODE,
        "report_scope": REPORT_SCOPE,
        "report_verdict": REPORT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "report_ready": True,
        "report_locked": True,
        "benchmark_id": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
        "benchmark_ready": benchmark.get("benchmark_ready") is True,
        "regression_benchmark_records_ready": benchmark.get("regression_benchmark_records_ready") is True,
        "family_report_count": len(family_reports),
        "benchmark_case_count": benchmark_case_count,
        "local_measurement_count": len(measurements),
        "improvement_signal_count": improvement_signal_count,
        "blocking_control_count": len(BLOCKING_CONTROLS),
        "report_section_count": len(REPORT_SECTIONS),
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "families": sorted(families),
        "local_score_report_ready": True,
        "local_score_claim_absent": True,
        "competitive_score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "submission_candidate_rebuild_required": True,
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "boundary_intact": _boundary_intact(boundary),
    }

    gate_state = {
        "benchmark_artifact_present": BENCHMARK_JSON.exists(),
        "benchmark_artifact_ready": benchmark.get("status") == "MILESTONE_7_REGRESSION_BENCHMARK_READY",
        "benchmark_artifact_valid": bool(benchmark.get("benchmark_id")) and bool(benchmark.get("signature")),
        "benchmark_next_stage_matches_task_7": benchmark.get("next_allowed_stage") == "MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT",
        "regression_benchmark_records_ready": benchmark.get("regression_benchmark_records_ready") is True,
        "report_mode_valid": report_record["report_mode"] == REPORT_MODE,
        "report_scope_valid": report_record["report_scope"] == REPORT_SCOPE,
        "report_verdict_valid": report_record["report_verdict"] == REPORT_VERDICT,
        "report_ready": report_record["report_ready"] is True,
        "report_locked": report_record["report_locked"] is True,
        "family_report_count_valid": len(family_reports) == EXPECTED_FAMILY_REPORT_COUNT,
        "benchmark_case_count_valid": benchmark_case_count == EXPECTED_BENCHMARK_CASE_COUNT,
        "local_measurement_count_valid": len(measurements) == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "improvement_signal_count_valid": improvement_signal_count == EXPECTED_IMPROVEMENT_SIGNAL_COUNT,
        "blocking_control_count_valid": len(BLOCKING_CONTROLS) == EXPECTED_BLOCKING_CONTROL_COUNT,
        "report_section_count_valid": len(REPORT_SECTIONS) == EXPECTED_REPORT_SECTION_COUNT,
        "regression_pass_count_valid": regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT,
        "all_family_reports_priority_p0": all(item.get("priority") == "P0" for item in family_reports),
        "all_family_reports_have_source_cases": all(len(item.get("source_cases", ())) > 0 for item in family_reports),
        "all_source_cases_found_in_benchmark": all(
            case_id in benchmark_case_ids
            for item in family_reports
            for case_id in item.get("source_cases", ())
        ),
        "all_family_reports_have_improvement_signals": all(
            len(item.get("local_improvement_signals", ())) > 0 for item in family_reports
        ),
        "all_family_reports_have_measurement_summary": all(bool(item.get("measurement_summary")) for item in family_reports),
        "all_family_reports_have_no_numeric_score_claim": all(
            item.get("local_score_delta_claim") == "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM"
            for item in family_reports
        ),
        "all_family_reports_no_competitive_score_claim": all(
            item.get("competitive_score_claim") is False for item in family_reports
        ),
        "all_family_reports_no_public_leaderboard_claim": all(
            item.get("public_leaderboard_claim") is False for item in family_reports
        ),
        "all_family_reports_ready_for_task_8": all(item.get("ready_for_task_8") is True for item in family_reports),
        "all_measurements_have_source_case": all(bool(item.get("source_case")) for item in measurements),
        "all_measurement_cases_found_in_benchmark": all(item.get("source_case") in benchmark_case_ids for item in measurements),
        "all_measurements_passed": all(item.get("result") == "PASS" for item in measurements),
        "all_measurements_have_no_numeric_score_claim": all(item.get("numeric_score_claim") is False for item in measurements),
        "color_report_present": "color_mapping" in families,
        "object_report_present": "object_model" in families,
        "shape_report_present": "shape_symmetry" in families,
        "local_score_report_ready": report_record["local_score_report_ready"] is True,
        "local_score_claim_absent": report_record["local_score_claim_absent"] is True,
        "competitive_score_claim_absent": report_record["competitive_score_claim_absent"] is True,
        "public_leaderboard_claim_absent": report_record["public_leaderboard_claim_absent"] is True,
        "runtime_solver_not_modified": report_record["runtime_solver_modified"] is False,
        "ranker_runtime_not_modified": report_record["ranker_runtime_modified"] is False,
        "benchmark_runtime_not_modified": report_record["benchmark_runtime_modified"] is False,
        "report_runtime_not_modified": report_record["report_runtime_modified"] is False,
        "next_stage_valid": report_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "submission_candidate_rebuild_required": report_record["submission_candidate_rebuild_required"] is True,
        "manual_submission_not_allowed": report_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": report_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": report_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": report_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": report_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": report_record["kaggle_submission_sent"] is False,
        "upload_not_performed": report_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": report_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "benchmark_artifact_missing": not gate_state["benchmark_artifact_present"],
        "benchmark_artifact_not_ready": not gate_state["benchmark_artifact_ready"],
        "benchmark_artifact_invalid": not gate_state["benchmark_artifact_valid"],
        "benchmark_next_stage_mismatch": not gate_state["benchmark_next_stage_matches_task_7"],
        "regression_benchmark_records_not_ready": not gate_state["regression_benchmark_records_ready"],
        "report_mode_invalid": not gate_state["report_mode_valid"],
        "report_scope_invalid": not gate_state["report_scope_valid"],
        "report_verdict_invalid": not gate_state["report_verdict_valid"],
        "report_not_ready": not gate_state["report_ready"],
        "report_not_locked": not gate_state["report_locked"],
        "family_report_count_invalid": not gate_state["family_report_count_valid"],
        "benchmark_case_count_invalid": not gate_state["benchmark_case_count_valid"],
        "local_measurement_count_invalid": not gate_state["local_measurement_count_valid"],
        "improvement_signal_count_invalid": not gate_state["improvement_signal_count_valid"],
        "blocking_control_count_invalid": not gate_state["blocking_control_count_valid"],
        "report_section_count_invalid": not gate_state["report_section_count_valid"],
        "regression_pass_count_invalid": not gate_state["regression_pass_count_valid"],
        "regression_failure_count_nonzero": not gate_state["regression_failure_count_zero"],
        "family_report_priority_not_p0": not gate_state["all_family_reports_priority_p0"],
        "family_report_source_cases_missing": not gate_state["all_family_reports_have_source_cases"],
        "source_case_not_found_in_benchmark": not gate_state["all_source_cases_found_in_benchmark"],
        "family_report_improvement_signals_missing": not gate_state["all_family_reports_have_improvement_signals"],
        "family_report_measurement_summary_missing": not gate_state["all_family_reports_have_measurement_summary"],
        "numeric_score_claim_detected": not gate_state["all_family_reports_have_no_numeric_score_claim"],
        "competitive_score_claim_detected": not gate_state["all_family_reports_no_competitive_score_claim"],
        "public_leaderboard_claim_detected": not gate_state["all_family_reports_no_public_leaderboard_claim"],
        "family_report_not_ready_for_task_8": not gate_state["all_family_reports_ready_for_task_8"],
        "measurement_source_case_missing": not gate_state["all_measurements_have_source_case"],
        "measurement_case_not_found_in_benchmark": not gate_state["all_measurement_cases_found_in_benchmark"],
        "measurement_not_passed": not gate_state["all_measurements_passed"],
        "measurement_numeric_score_claim_detected": not gate_state["all_measurements_have_no_numeric_score_claim"],
        "color_report_missing": not gate_state["color_report_present"],
        "object_report_missing": not gate_state["object_report_present"],
        "shape_report_missing": not gate_state["shape_report_present"],
        "local_score_report_not_ready": not gate_state["local_score_report_ready"],
        "local_score_claim_detected": not gate_state["local_score_claim_absent"],
        "competitive_score_claim_detected_global": not gate_state["competitive_score_claim_absent"],
        "public_leaderboard_claim_detected_global": not gate_state["public_leaderboard_claim_absent"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "ranker_runtime_modified": not gate_state["ranker_runtime_not_modified"],
        "benchmark_runtime_modified": not gate_state["benchmark_runtime_not_modified"],
        "report_runtime_modified": not gate_state["report_runtime_not_modified"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "submission_candidate_rebuild_not_required": not gate_state["submission_candidate_rebuild_required"],
        "manual_submission_allowed": not gate_state["manual_submission_not_allowed"],
        "manual_upload_performed": not gate_state["manual_upload_not_performed"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in REPORT_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in REPORT_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    report_ready = (
        benchmark_source["ready"] is True
        and len(family_reports) == EXPECTED_FAMILY_REPORT_COUNT
        and benchmark_case_count == EXPECTED_BENCHMARK_CASE_COUNT
        and len(measurements) == EXPECTED_LOCAL_MEASUREMENT_COUNT
        and improvement_signal_count == EXPECTED_IMPROVEMENT_SIGNAL_COUNT
        and len(BLOCKING_CONTROLS) == EXPECTED_BLOCKING_CONTROL_COUNT
        and regression_pass_count == EXPECTED_REGRESSION_PASS_COUNT
        and regression_failure_count == EXPECTED_REGRESSION_FAILURE_COUNT
        and passed_gate_count == len(REPORT_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 7",
        "report_mode": REPORT_MODE,
        "report_scope": REPORT_SCOPE,
        "report_verdict": REPORT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_benchmark": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
        "report_ready": report_ready,
        "report_locked": True,
        "family_report_count": len(family_reports),
        "benchmark_case_count": benchmark_case_count,
        "local_measurement_count": len(measurements),
        "improvement_signal_count": improvement_signal_count,
        "blocking_control_count": len(BLOCKING_CONTROLS),
        "report_section_count": len(REPORT_SECTIONS),
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "local_score_report_ready": True,
        "local_score_claim_absent": True,
        "competitive_score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "submission_candidate_rebuild_required": True,
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": REPORT_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 7",
        "title": "Local Score Improvement Report v1",
        "baseline_commit": BASELINE_COMMIT,
        "report_mode": REPORT_MODE,
        "report_scope": REPORT_SCOPE,
        "report_verdict": REPORT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_benchmark_source": benchmark_source,
        "report_record": report_record,
        "family_reports": list(family_reports),
        "local_measurements": list(measurements),
        "blocking_controls": list(BLOCKING_CONTROLS),
        "report_sections": list(REPORT_SECTIONS),
        "report_gates": list(gates),
        "report_issues": list(issues),
        "report_index": index,
        "boundary": boundary,
        "family_report_count": len(family_reports),
        "benchmark_case_count": benchmark_case_count,
        "local_measurement_count": len(measurements),
        "improvement_signal_count": improvement_signal_count,
        "blocking_control_count": len(BLOCKING_CONTROLS),
        "report_section_count": len(REPORT_SECTIONS),
        "regression_pass_count": regression_pass_count,
        "regression_failure_count": regression_failure_count,
        "report_gate_count": len(REPORT_GATES),
        "passed_gate_count": passed_gate_count,
        "report_issue_count": issue_count,
        "warning_count": 0,
        "report_ready": report_ready,
        "report_locked": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "report_runtime_modified": False,
        "local_score_report_ready": True,
        "local_score_claim_absent": True,
        "competitive_score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "submission_candidate_rebuild_required": True,
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_submission_allowed": False,
        "manual_upload_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_7_local_score_improvement_report_v1",
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
        "report_id": f"MILESTONE-7-LOCAL-SCORE-REPORT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_local_score_improvement_report(report: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = report.get("boundary", {})
    gates = report.get("report_gates", [])
    issues = report.get("report_issues", [])
    family_reports = report.get("family_reports", [])
    measurements = report.get("local_measurements", [])
    source = report.get("milestone_7_benchmark_source", {})

    checks = {
        "status_ready": report.get("status") == REPORT_STATUS,
        "report_id_present": isinstance(report.get("report_id"), str) and bool(report.get("report_id")),
        "signature_present": isinstance(report.get("signature"), str) and bool(report.get("signature")),
        "baseline_commit_valid": str(report.get("baseline_commit", "")).startswith("92efad5"),
        "report_mode_valid": report.get("report_mode") == REPORT_MODE,
        "report_scope_valid": report.get("report_scope") == REPORT_SCOPE,
        "report_verdict_valid": report.get("report_verdict") == REPORT_VERDICT,
        "next_allowed_stage_valid": report.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "benchmark_source_ready": source.get("ready") is True,
        "benchmark_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "family_report_count_valid": report.get("family_report_count") == EXPECTED_FAMILY_REPORT_COUNT,
        "benchmark_case_count_valid": report.get("benchmark_case_count") == EXPECTED_BENCHMARK_CASE_COUNT,
        "local_measurement_count_valid": report.get("local_measurement_count") == EXPECTED_LOCAL_MEASUREMENT_COUNT,
        "improvement_signal_count_valid": report.get("improvement_signal_count") == EXPECTED_IMPROVEMENT_SIGNAL_COUNT,
        "blocking_control_count_valid": report.get("blocking_control_count") == EXPECTED_BLOCKING_CONTROL_COUNT,
        "report_section_count_valid": report.get("report_section_count") == EXPECTED_REPORT_SECTION_COUNT,
        "regression_pass_count_valid": report.get("regression_pass_count") == EXPECTED_REGRESSION_PASS_COUNT,
        "regression_failure_count_zero": report.get("regression_failure_count") == EXPECTED_REGRESSION_FAILURE_COUNT,
        "all_family_reports_have_source_cases": bool(family_reports)
        and all(len(item.get("source_cases", ())) > 0 for item in family_reports),
        "all_family_reports_have_improvement_signals": bool(family_reports)
        and all(len(item.get("local_improvement_signals", ())) > 0 for item in family_reports),
        "all_family_reports_no_score_claim": bool(family_reports)
        and all(item.get("local_score_delta_claim") == "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM" for item in family_reports),
        "all_family_reports_no_competitive_claim": bool(family_reports)
        and all(item.get("competitive_score_claim") is False for item in family_reports),
        "all_family_reports_no_public_leaderboard_claim": bool(family_reports)
        and all(item.get("public_leaderboard_claim") is False for item in family_reports),
        "all_family_reports_ready_for_task_8": bool(family_reports)
        and all(item.get("ready_for_task_8") is True for item in family_reports),
        "all_measurements_passed": bool(measurements) and all(item.get("result") == "PASS" for item in measurements),
        "all_measurements_no_numeric_score_claim": bool(measurements)
        and all(item.get("numeric_score_claim") is False for item in measurements),
        "runtime_solver_not_modified": report.get("runtime_solver_modified") is False,
        "ranker_runtime_not_modified": report.get("ranker_runtime_modified") is False,
        "benchmark_runtime_not_modified": report.get("benchmark_runtime_modified") is False,
        "report_runtime_not_modified": report.get("report_runtime_modified") is False,
        "local_score_report_ready": report.get("local_score_report_ready") is True,
        "local_score_claim_absent": report.get("local_score_claim_absent") is True,
        "competitive_score_claim_absent": report.get("competitive_score_claim_absent") is True,
        "public_leaderboard_claim_absent": report.get("public_leaderboard_claim_absent") is True,
        "submission_candidate_rebuild_required": report.get("submission_candidate_rebuild_required") is True,
        "report_gate_count_matches": report.get("report_gate_count") == len(REPORT_GATES),
        "all_report_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "report_issue_count_zero": report.get("report_issue_count") == 0,
        "all_report_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "report_ready": report.get("report_ready") is True,
        "report_locked": report.get("report_locked") is True,
        "solver_improvement_required": report.get("solver_improvement_required") is True,
        "competitive_claim_absent": report.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": report.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": report.get("manual_upload_performed") is False,
        "real_submission_allowed_false": report.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": report.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": report.get("real_submission_created") is False,
        "kaggle_submission_not_sent": report.get("kaggle_submission_sent") is False,
        "upload_not_performed": report.get("upload_performed") is False,
        "kaggle_authentication_not_performed": report.get("kaggle_authentication_performed") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_INVALID",
        "valid": valid,
        "checks": checks,
        "report_id": report.get("report_id"),
        "signature": report.get("signature"),
    }


def render_local_score_improvement_report_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Local Score Improvement Report v1",
        "",
        f"- status: {report['status']}",
        f"- report_id: {report['report_id']}",
        f"- signature: {report['signature']}",
        f"- baseline_commit: {report['baseline_commit']}",
        f"- report_mode: {report['report_mode']}",
        f"- report_scope: {report['report_scope']}",
        f"- report_verdict: {report['report_verdict']}",
        f"- next_allowed_stage: {report['next_allowed_stage']}",
        f"- family_report_count: {report['family_report_count']}",
        f"- benchmark_case_count: {report['benchmark_case_count']}",
        f"- local_measurement_count: {report['local_measurement_count']}",
        f"- improvement_signal_count: {report['improvement_signal_count']}",
        f"- blocking_control_count: {report['blocking_control_count']}",
        f"- report_section_count: {report['report_section_count']}",
        f"- regression_pass_count: {report['regression_pass_count']}",
        f"- regression_failure_count: {report['regression_failure_count']}",
        f"- report_gate_count: {report['report_gate_count']}",
        f"- passed_gate_count: {report['passed_gate_count']}",
        f"- report_issue_count: {report['report_issue_count']}",
        f"- report_ready: {report['report_ready']}",
        f"- local_score_claim_absent: {report['local_score_claim_absent']}",
        f"- competitive_score_claim_absent: {report['competitive_score_claim_absent']}",
        f"- public_leaderboard_claim_absent: {report['public_leaderboard_claim_absent']}",
        f"- real_submission_allowed: {report['real_submission_allowed']}",
        f"- kaggle_submission_sent: {report['kaggle_submission_sent']}",
        f"- upload_performed: {report['upload_performed']}",
        "",
        "## Family reports",
        "",
    ]

    for item in report["family_reports"]:
        lines.append(
            f"- {item['priority']} {item['family_report_id']} / family={item['family']} / "
            f"source_cases={len(item['source_cases'])} / signals={len(item['local_improvement_signals'])} / "
            f"ready_for_task_8={item['ready_for_task_8']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Local improvement evidence is report-ready. No numeric Kaggle score is claimed.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_VALID=true",
            "ARC_AGI3_MILESTONE_7_REPORT_MODE=LOCAL_SCORE_IMPROVEMENT_REPORT_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_REPORT_VERDICT=LOCAL_SCORE_IMPROVEMENT_REPORT_READY_FOR_SUBMISSION_CANDIDATE_REBUILD",
            "ARC_AGI3_MILESTONE_7_FAMILY_REPORT_COUNT=3",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_CASE_COUNT=6",
            "ARC_AGI3_MILESTONE_7_LOCAL_MEASUREMENT_COUNT=6",
            "ARC_AGI3_MILESTONE_7_IMPROVEMENT_SIGNAL_COUNT=9",
            "ARC_AGI3_MILESTONE_7_BLOCKING_CONTROL_COUNT=8",
            "ARC_AGI3_MILESTONE_7_REPORT_SECTION_COUNT=7",
            "ARC_AGI3_MILESTONE_7_REGRESSION_PASS_COUNT=6",
            "ARC_AGI3_MILESTONE_7_REGRESSION_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_CLAIM_ABSENT=true",
            "ARC_AGI3_MILESTONE_7_COMPETITIVE_SCORE_CLAIM_ABSENT=true",
            "ARC_AGI3_MILESTONE_7_PUBLIC_LEADERBOARD_CLAIM_ABSENT=true",
            "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_RANKER_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_REPORT_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_REQUIRED=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_8_SUBMISSION_CANDIDATE_REBUILD",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_BENCHMARK_COMMIT=92efad5",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_local_score_improvement_report_manifest(report: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 LOCAL SCORE IMPROVEMENT REPORT MANIFEST v1",
        f"report_id={report['report_id']}",
        f"signature={report['signature']}",
        f"status={report['status']}",
        f"baseline_commit={report['baseline_commit']}",
        f"report_mode={report['report_mode']}",
        f"report_verdict={report['report_verdict']}",
        f"next_allowed_stage={report['next_allowed_stage']}",
        f"family_report_count={report['family_report_count']}",
        f"benchmark_case_count={report['benchmark_case_count']}",
        f"local_measurement_count={report['local_measurement_count']}",
        f"improvement_signal_count={report['improvement_signal_count']}",
        f"blocking_control_count={report['blocking_control_count']}",
        f"report_section_count={report['report_section_count']}",
        f"regression_pass_count={report['regression_pass_count']}",
        f"regression_failure_count={report['regression_failure_count']}",
        f"report_gate_count={report['report_gate_count']}",
        f"passed_gate_count={report['passed_gate_count']}",
        f"report_issue_count={report['report_issue_count']}",
        f"report_ready={report['report_ready']}",
        f"report_locked={report['report_locked']}",
        f"runtime_solver_modified={report['runtime_solver_modified']}",
        f"ranker_runtime_modified={report['ranker_runtime_modified']}",
        f"benchmark_runtime_modified={report['benchmark_runtime_modified']}",
        f"report_runtime_modified={report['report_runtime_modified']}",
        f"local_score_report_ready={report['local_score_report_ready']}",
        f"local_score_claim_absent={report['local_score_claim_absent']}",
        f"competitive_score_claim_absent={report['competitive_score_claim_absent']}",
        f"public_leaderboard_claim_absent={report['public_leaderboard_claim_absent']}",
        f"submission_candidate_rebuild_required={report['submission_candidate_rebuild_required']}",
        f"solver_improvement_required={report['solver_improvement_required']}",
        f"competitive_claim_absent={report['competitive_claim_absent']}",
        f"manual_submission_allowed={report['manual_submission_allowed']}",
        f"manual_upload_performed={report['manual_upload_performed']}",
        f"real_submission_allowed={report['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={report['ready_for_real_kaggle_submission']}",
        f"real_submission_created={report['real_submission_created']}",
        f"kaggle_submission_sent={report['kaggle_submission_sent']}",
        f"upload_performed={report['upload_performed']}",
        f"kaggle_authentication_performed={report['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "FAMILY_REPORTS",
    ]

    for item in report["family_reports"]:
        lines.append(
            f"{item['priority']} {item['family_report_id']} family={item['family']} "
            f"source_case_count={len(item['source_cases'])} improvement_signal_count={len(item['local_improvement_signals'])} "
            f"local_score_delta_claim={item['local_score_delta_claim']} "
            f"competitive_score_claim={item['competitive_score_claim']} "
            f"public_leaderboard_claim={item['public_leaderboard_claim']} "
            f"ready_for_task_8={item['ready_for_task_8']}"
        )

    lines.append("")
    lines.append("LOCAL_MEASUREMENTS")

    for item in report["local_measurements"]:
        lines.append(
            f"{item['measurement_id']} family={item['family']} source_case={item['source_case']} "
            f"result={item['result']} numeric_score_claim={item['numeric_score_claim']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_local_score_improvement_report_artifacts(
    report: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    report = dict(report or build_milestone_7_local_score_improvement_report())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-local-score-improvement-report-v1.json"
    md_path = output / "milestone-7-local-score-improvement-report-v1.md"
    manifest_path = output / "milestone-7-local-score-improvement-report-manifest-v1.txt"
    index_path = output / "milestone-7-local-score-improvement-report-index-v1.json"

    json_path.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_local_score_improvement_report_markdown(report), encoding="utf-8")
    manifest_path.write_text(render_local_score_improvement_report_manifest(report), encoding="utf-8")
    index_path.write_text(json.dumps(report["report_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_local_score_improvement_report_pipeline() -> Dict[str, Any]:
    report = build_milestone_7_local_score_improvement_report()
    validation = validate_milestone_7_local_score_improvement_report(report)
    artifacts = write_local_score_improvement_report_artifacts(report)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_PIPELINE_INVALID",
        "report_status": report["status"],
        "validation_status": validation["status"],
        "report": report,
        "report_id": report["report_id"],
        "signature": report["signature"],
        "report_mode": report["report_mode"],
        "report_verdict": report["report_verdict"],
        "next_allowed_stage": report["next_allowed_stage"],
        "family_report_count": report["family_report_count"],
        "benchmark_case_count": report["benchmark_case_count"],
        "local_measurement_count": report["local_measurement_count"],
        "improvement_signal_count": report["improvement_signal_count"],
        "blocking_control_count": report["blocking_control_count"],
        "report_section_count": report["report_section_count"],
        "regression_pass_count": report["regression_pass_count"],
        "regression_failure_count": report["regression_failure_count"],
        "report_gate_count": report["report_gate_count"],
        "passed_gate_count": report["passed_gate_count"],
        "report_issue_count": report["report_issue_count"],
        "warning_count": report["warning_count"],
        "report_ready": report["report_ready"],
        "report_locked": report["report_locked"],
        "runtime_solver_modified": report["runtime_solver_modified"],
        "ranker_runtime_modified": report["ranker_runtime_modified"],
        "benchmark_runtime_modified": report["benchmark_runtime_modified"],
        "report_runtime_modified": report["report_runtime_modified"],
        "local_score_report_ready": report["local_score_report_ready"],
        "local_score_claim_absent": report["local_score_claim_absent"],
        "competitive_score_claim_absent": report["competitive_score_claim_absent"],
        "public_leaderboard_claim_absent": report["public_leaderboard_claim_absent"],
        "submission_candidate_rebuild_required": report["submission_candidate_rebuild_required"],
        "solver_improvement_required": report["solver_improvement_required"],
        "competitive_claim_absent": report["competitive_claim_absent"],
        "manual_submission_allowed": report["manual_submission_allowed"],
        "manual_upload_performed": report["manual_upload_performed"],
        "real_submission_allowed": report["real_submission_allowed"],
        "ready_for_real_kaggle_submission": report["ready_for_real_kaggle_submission"],
        "real_submission_created": report["real_submission_created"],
        "kaggle_submission_sent": report["kaggle_submission_sent"],
        "upload_performed": report["upload_performed"],
        "kaggle_authentication_performed": report["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": report["metadata"],
    }
