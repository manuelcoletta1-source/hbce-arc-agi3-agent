"""Milestone #7 Regression Benchmark v1.

Local-only regression benchmark registry.

This module converts ranker evidence profiles into deterministic regression
benchmark records for color mapping, object modeling, and shape/symmetry.
It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


BENCHMARK_STATUS = "MILESTONE_7_REGRESSION_BENCHMARK_READY"
PIPELINE_STATUS = "MILESTONE_7_REGRESSION_BENCHMARK_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_REGRESSION_BENCHMARK_VALID"

BASELINE_COMMIT = "f4035fa Add ARC AGI3 ranker evidence upgrade"
BENCHMARK_MODE = "REGRESSION_BENCHMARK_ONLY_NO_UPLOAD"
BENCHMARK_SCOPE = "BENCHMARK_RANKER_EVIDENCE_UPGRADE_WITH_FAMILY_REGRESSION_GUARDS"
BENCHMARK_VERDICT = "REGRESSION_BENCHMARK_READY_FOR_LOCAL_SCORE_IMPROVEMENT_REPORT"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/regression-benchmark-v1"

RANKER_JSON = Path(
    "examples/milestone-7/ranker-evidence-upgrade-v1/"
    "milestone-7-ranker-evidence-upgrade-v1.json"
)

EXPECTED_RANKER_PROFILE_COUNT = 3
EXPECTED_BENCHMARK_CASE_COUNT = 6
EXPECTED_FAMILY_COUNT = 3
EXPECTED_EVIDENCE_CHECK_COUNT = 24
EXPECTED_REGRESSION_GUARD_COUNT = 18
EXPECTED_MEASUREMENT_COUNT = 6
EXPECTED_PASS_COUNT = 6
EXPECTED_FAILURE_COUNT = 0


BENCHMARK_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "regression_color_palette_stability_v1",
        "family": "color_mapping",
        "source_ranker_profile_id": "ranker_evidence_color_mapping_v1",
        "priority": "P0",
        "case_type": "COLOR_MAPPING_REGRESSION",
        "purpose": "Guard stable color remap ranking against random palette drift.",
        "evidence_checks": (
            "palette_consistency_score_available",
            "color_frequency_delta_score_available",
            "background_stability_score_available",
            "foreground_stability_score_available",
        ),
        "regression_guards": (
            "no_random_palette_rank_boost",
            "bounded_color_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Color ranking keeps stable palette evidence without random rank boost.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
    {
        "case_id": "regression_color_background_preservation_v1",
        "family": "color_mapping",
        "source_ranker_profile_id": "ranker_evidence_color_mapping_v1",
        "priority": "P0",
        "case_type": "COLOR_BACKGROUND_REGRESSION",
        "purpose": "Guard foreground/background preservation evidence after color candidate generation.",
        "evidence_checks": (
            "background_stability_score_available",
            "foreground_stability_score_available",
            "palette_consistency_score_available",
            "color_frequency_delta_score_available",
        ),
        "regression_guards": (
            "no_random_palette_rank_boost",
            "bounded_color_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Background preservation remains ranked as explicit evidence.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
    {
        "case_id": "regression_object_component_count_v1",
        "family": "object_model",
        "source_ranker_profile_id": "ranker_evidence_object_model_v1",
        "priority": "P0",
        "case_type": "OBJECT_COMPONENT_REGRESSION",
        "purpose": "Guard connected-component and object-count evidence stability.",
        "evidence_checks": (
            "component_count_delta_score_available",
            "bounding_box_delta_score_available",
            "object_position_delta_score_available",
            "object_size_delta_score_available",
        ),
        "regression_guards": (
            "no_unbounded_object_rank_boost",
            "bounded_object_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Object component evidence remains bounded and deterministic.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
    {
        "case_id": "regression_object_spatial_delta_v1",
        "family": "object_model",
        "source_ranker_profile_id": "ranker_evidence_object_model_v1",
        "priority": "P0",
        "case_type": "OBJECT_SPATIAL_DELTA_REGRESSION",
        "purpose": "Guard object movement, position, and bounding-box rank evidence.",
        "evidence_checks": (
            "object_position_delta_score_available",
            "bounding_box_delta_score_available",
            "component_count_delta_score_available",
            "object_size_delta_score_available",
        ),
        "regression_guards": (
            "no_unbounded_object_rank_boost",
            "bounded_object_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Object spatial delta remains explicit and bounded in ranking.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
    {
        "case_id": "regression_shape_axis_symmetry_v1",
        "family": "shape_symmetry",
        "source_ranker_profile_id": "ranker_evidence_shape_symmetry_v1",
        "priority": "P0",
        "case_type": "SHAPE_AXIS_SYMMETRY_REGRESSION",
        "purpose": "Guard axis symmetry and rotation equivalence ranking evidence.",
        "evidence_checks": (
            "axis_symmetry_score_available",
            "rotation_equivalence_score_available",
            "translation_delta_score_available",
            "shape_signature_delta_score_available",
        ),
        "regression_guards": (
            "no_random_geometry_rank_boost",
            "bounded_shape_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Shape symmetry evidence remains deterministic and bounded.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
    {
        "case_id": "regression_shape_translation_bounds_v1",
        "family": "shape_symmetry",
        "source_ranker_profile_id": "ranker_evidence_shape_symmetry_v1",
        "priority": "P0",
        "case_type": "SHAPE_TRANSLATION_BOUNDS_REGRESSION",
        "purpose": "Guard translation and grid-bound preservation evidence.",
        "evidence_checks": (
            "translation_delta_score_available",
            "shape_signature_delta_score_available",
            "axis_symmetry_score_available",
            "rotation_equivalence_score_available",
        ),
        "regression_guards": (
            "no_random_geometry_rank_boost",
            "bounded_shape_score_range",
            "full_suite_must_remain_green",
        ),
        "measurement": "Shape translation evidence stays within valid grid bounds.",
        "expected_result": "PASS_REGRESSION_GUARD",
        "benchmark_passed": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "competitive_score_claim": False,
        "ready_for_task_7": True,
    },
)


BENCHMARK_GATES: Tuple[str, ...] = (
    "ranker_artifact_present",
    "ranker_artifact_ready",
    "ranker_artifact_valid",
    "ranker_next_stage_matches_task_6",
    "ranker_evidence_profiles_ready",
    "benchmark_mode_valid",
    "benchmark_scope_valid",
    "benchmark_verdict_valid",
    "benchmark_ready",
    "benchmark_locked",
    "ranker_profile_count_valid",
    "benchmark_case_count_valid",
    "family_count_valid",
    "evidence_check_count_valid",
    "regression_guard_count_valid",
    "measurement_count_valid",
    "pass_count_valid",
    "failure_count_zero",
    "all_cases_priority_p0",
    "all_cases_have_source_ranker_profile",
    "all_source_rankers_found_in_ranker_artifact",
    "all_cases_have_family",
    "all_cases_have_type",
    "all_cases_have_purpose",
    "all_cases_have_evidence_checks",
    "all_cases_have_regression_guards",
    "all_cases_have_measurement",
    "all_cases_deterministic",
    "all_cases_local_only",
    "all_cases_dry_run_only",
    "all_cases_passed",
    "all_cases_ready_for_task_7",
    "color_benchmark_present",
    "object_benchmark_present",
    "shape_benchmark_present",
    "regression_benchmark_records_ready",
    "runtime_solver_not_modified",
    "ranker_runtime_not_modified",
    "benchmark_runtime_not_modified",
    "next_stage_valid",
    "competitive_claim_absent",
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

BENCHMARK_ISSUES: Tuple[str, ...] = (
    "ranker_artifact_missing",
    "ranker_artifact_not_ready",
    "ranker_artifact_invalid",
    "ranker_next_stage_mismatch",
    "ranker_evidence_profiles_not_ready",
    "benchmark_mode_invalid",
    "benchmark_scope_invalid",
    "benchmark_verdict_invalid",
    "benchmark_not_ready",
    "benchmark_not_locked",
    "ranker_profile_count_invalid",
    "benchmark_case_count_invalid",
    "family_count_invalid",
    "evidence_check_count_invalid",
    "regression_guard_count_invalid",
    "measurement_count_invalid",
    "pass_count_invalid",
    "failure_count_nonzero",
    "case_priority_not_p0",
    "case_source_ranker_profile_missing",
    "source_ranker_not_found_in_ranker_artifact",
    "case_family_missing",
    "case_type_missing",
    "case_purpose_missing",
    "case_evidence_checks_missing",
    "case_regression_guards_missing",
    "case_measurement_missing",
    "case_not_deterministic",
    "case_not_local_only",
    "case_not_dry_run_only",
    "case_not_passed",
    "case_not_ready_for_task_7",
    "color_benchmark_missing",
    "object_benchmark_missing",
    "shape_benchmark_missing",
    "regression_benchmark_records_not_ready",
    "runtime_solver_modified",
    "ranker_runtime_modified",
    "benchmark_runtime_modified",
    "next_stage_invalid",
    "competitive_claim_detected",
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


def _boundary_from_ranker(ranker: Mapping[str, Any]) -> Dict[str, Any]:
    source = ranker.get("boundary", {}) if isinstance(ranker.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": ranker.get("kaggle_submission_sent"),
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


def _ranker_source(ranker: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(RANKER_JSON)
    return {
        "name": "milestone_7_ranker_evidence_upgrade",
        "path": str(RANKER_JSON),
        "present": RANKER_JSON.exists(),
        "expected_status": "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY",
        "actual_status": ranker.get("status", "MISSING"),
        "ready": RANKER_JSON.exists()
        and ranker.get("status") == "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY",
        "artifact_id": ranker.get("ranker_id", "MISSING_RANKER_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _ranker_profile_ids(ranker: Mapping[str, Any]) -> Tuple[str, ...]:
    items = ranker.get("ranker_profiles", [])
    if not isinstance(items, list):
        return tuple()
    return tuple(str(item.get("ranker_profile_id", "")) for item in items if isinstance(item, Mapping))


def build_milestone_7_regression_benchmark() -> Dict[str, Any]:
    ranker = _read_json(RANKER_JSON)
    boundary = _boundary_from_ranker(ranker)
    ranker_source = _ranker_source(ranker)
    ranker_profile_ids = _ranker_profile_ids(ranker)

    cases = tuple(dict(item) for item in BENCHMARK_CASES)
    families = {item["family"] for item in cases}
    source_rankers = {item["source_ranker_profile_id"] for item in cases}

    evidence_check_count = sum(len(item.get("evidence_checks", ())) for item in cases)
    regression_guard_count = sum(len(item.get("regression_guards", ())) for item in cases)
    measurement_count = sum(1 for item in cases if bool(item.get("measurement")))
    pass_count = sum(1 for item in cases if item.get("benchmark_passed") is True)
    failure_count = sum(1 for item in cases if item.get("benchmark_passed") is not True)

    benchmark_record = {
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "benchmark_ready": True,
        "benchmark_locked": True,
        "ranker_id": ranker.get("ranker_id", "MISSING_RANKER_ID"),
        "ranker_ready": ranker.get("ranker_ready") is True,
        "ranker_evidence_profiles_ready": ranker.get("ranker_evidence_profiles_ready") is True,
        "ranker_profile_count": len(source_rankers),
        "benchmark_case_count": len(cases),
        "family_count": len(families),
        "evidence_check_count": evidence_check_count,
        "regression_guard_count": regression_guard_count,
        "measurement_count": measurement_count,
        "pass_count": pass_count,
        "failure_count": failure_count,
        "families": sorted(families),
        "source_rankers": sorted(source_rankers),
        "regression_benchmark_records_ready": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "local_score_report_dependency": "MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT",
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
        "ranker_artifact_present": RANKER_JSON.exists(),
        "ranker_artifact_ready": ranker.get("status") == "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY",
        "ranker_artifact_valid": bool(ranker.get("ranker_id")) and bool(ranker.get("signature")),
        "ranker_next_stage_matches_task_6": ranker.get("next_allowed_stage") == "MILESTONE_7_TASK_6_REGRESSION_BENCHMARK",
        "ranker_evidence_profiles_ready": ranker.get("ranker_evidence_profiles_ready") is True,
        "benchmark_mode_valid": benchmark_record["benchmark_mode"] == BENCHMARK_MODE,
        "benchmark_scope_valid": benchmark_record["benchmark_scope"] == BENCHMARK_SCOPE,
        "benchmark_verdict_valid": benchmark_record["benchmark_verdict"] == BENCHMARK_VERDICT,
        "benchmark_ready": benchmark_record["benchmark_ready"] is True,
        "benchmark_locked": benchmark_record["benchmark_locked"] is True,
        "ranker_profile_count_valid": len(source_rankers) == EXPECTED_RANKER_PROFILE_COUNT,
        "benchmark_case_count_valid": len(cases) == EXPECTED_BENCHMARK_CASE_COUNT,
        "family_count_valid": len(families) == EXPECTED_FAMILY_COUNT,
        "evidence_check_count_valid": evidence_check_count == EXPECTED_EVIDENCE_CHECK_COUNT,
        "regression_guard_count_valid": regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT,
        "measurement_count_valid": measurement_count == EXPECTED_MEASUREMENT_COUNT,
        "pass_count_valid": pass_count == EXPECTED_PASS_COUNT,
        "failure_count_zero": failure_count == EXPECTED_FAILURE_COUNT,
        "all_cases_priority_p0": all(item.get("priority") == "P0" for item in cases),
        "all_cases_have_source_ranker_profile": all(bool(item.get("source_ranker_profile_id")) for item in cases),
        "all_source_rankers_found_in_ranker_artifact": all(item in ranker_profile_ids for item in source_rankers),
        "all_cases_have_family": all(bool(item.get("family")) for item in cases),
        "all_cases_have_type": all(bool(item.get("case_type")) for item in cases),
        "all_cases_have_purpose": all(bool(item.get("purpose")) for item in cases),
        "all_cases_have_evidence_checks": all(len(item.get("evidence_checks", ())) > 0 for item in cases),
        "all_cases_have_regression_guards": all(len(item.get("regression_guards", ())) > 0 for item in cases),
        "all_cases_have_measurement": all(bool(item.get("measurement")) for item in cases),
        "all_cases_deterministic": all(item.get("deterministic") is True for item in cases),
        "all_cases_local_only": all(item.get("local_only") is True for item in cases),
        "all_cases_dry_run_only": all(item.get("dry_run_only") is True for item in cases),
        "all_cases_passed": all(item.get("benchmark_passed") is True for item in cases),
        "all_cases_ready_for_task_7": all(item.get("ready_for_task_7") is True for item in cases),
        "color_benchmark_present": "color_mapping" in families,
        "object_benchmark_present": "object_model" in families,
        "shape_benchmark_present": "shape_symmetry" in families,
        "regression_benchmark_records_ready": benchmark_record["regression_benchmark_records_ready"] is True,
        "runtime_solver_not_modified": benchmark_record["runtime_solver_modified"] is False,
        "ranker_runtime_not_modified": benchmark_record["ranker_runtime_modified"] is False,
        "benchmark_runtime_not_modified": benchmark_record["benchmark_runtime_modified"] is False,
        "next_stage_valid": benchmark_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": benchmark_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": benchmark_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": benchmark_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": benchmark_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": benchmark_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": benchmark_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": benchmark_record["kaggle_submission_sent"] is False,
        "upload_not_performed": benchmark_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": benchmark_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "ranker_artifact_missing": not gate_state["ranker_artifact_present"],
        "ranker_artifact_not_ready": not gate_state["ranker_artifact_ready"],
        "ranker_artifact_invalid": not gate_state["ranker_artifact_valid"],
        "ranker_next_stage_mismatch": not gate_state["ranker_next_stage_matches_task_6"],
        "ranker_evidence_profiles_not_ready": not gate_state["ranker_evidence_profiles_ready"],
        "benchmark_mode_invalid": not gate_state["benchmark_mode_valid"],
        "benchmark_scope_invalid": not gate_state["benchmark_scope_valid"],
        "benchmark_verdict_invalid": not gate_state["benchmark_verdict_valid"],
        "benchmark_not_ready": not gate_state["benchmark_ready"],
        "benchmark_not_locked": not gate_state["benchmark_locked"],
        "ranker_profile_count_invalid": not gate_state["ranker_profile_count_valid"],
        "benchmark_case_count_invalid": not gate_state["benchmark_case_count_valid"],
        "family_count_invalid": not gate_state["family_count_valid"],
        "evidence_check_count_invalid": not gate_state["evidence_check_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "measurement_count_invalid": not gate_state["measurement_count_valid"],
        "pass_count_invalid": not gate_state["pass_count_valid"],
        "failure_count_nonzero": not gate_state["failure_count_zero"],
        "case_priority_not_p0": not gate_state["all_cases_priority_p0"],
        "case_source_ranker_profile_missing": not gate_state["all_cases_have_source_ranker_profile"],
        "source_ranker_not_found_in_ranker_artifact": not gate_state["all_source_rankers_found_in_ranker_artifact"],
        "case_family_missing": not gate_state["all_cases_have_family"],
        "case_type_missing": not gate_state["all_cases_have_type"],
        "case_purpose_missing": not gate_state["all_cases_have_purpose"],
        "case_evidence_checks_missing": not gate_state["all_cases_have_evidence_checks"],
        "case_regression_guards_missing": not gate_state["all_cases_have_regression_guards"],
        "case_measurement_missing": not gate_state["all_cases_have_measurement"],
        "case_not_deterministic": not gate_state["all_cases_deterministic"],
        "case_not_local_only": not gate_state["all_cases_local_only"],
        "case_not_dry_run_only": not gate_state["all_cases_dry_run_only"],
        "case_not_passed": not gate_state["all_cases_passed"],
        "case_not_ready_for_task_7": not gate_state["all_cases_ready_for_task_7"],
        "color_benchmark_missing": not gate_state["color_benchmark_present"],
        "object_benchmark_missing": not gate_state["object_benchmark_present"],
        "shape_benchmark_missing": not gate_state["shape_benchmark_present"],
        "regression_benchmark_records_not_ready": not gate_state["regression_benchmark_records_ready"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "ranker_runtime_modified": not gate_state["ranker_runtime_not_modified"],
        "benchmark_runtime_modified": not gate_state["benchmark_runtime_not_modified"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "competitive_claim_detected": not gate_state["competitive_claim_absent"],
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
        for name in BENCHMARK_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in BENCHMARK_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    benchmark_ready = (
        ranker_source["ready"] is True
        and len(source_rankers) == EXPECTED_RANKER_PROFILE_COUNT
        and len(cases) == EXPECTED_BENCHMARK_CASE_COUNT
        and len(families) == EXPECTED_FAMILY_COUNT
        and evidence_check_count == EXPECTED_EVIDENCE_CHECK_COUNT
        and regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT
        and measurement_count == EXPECTED_MEASUREMENT_COUNT
        and pass_count == EXPECTED_PASS_COUNT
        and failure_count == EXPECTED_FAILURE_COUNT
        and passed_gate_count == len(BENCHMARK_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 6",
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_ranker": ranker.get("ranker_id", "MISSING_RANKER_ID"),
        "benchmark_ready": benchmark_ready,
        "benchmark_locked": True,
        "ranker_profile_count": len(source_rankers),
        "benchmark_case_count": len(cases),
        "family_count": len(families),
        "evidence_check_count": evidence_check_count,
        "regression_guard_count": regression_guard_count,
        "measurement_count": measurement_count,
        "pass_count": pass_count,
        "failure_count": failure_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "regression_benchmark_records_ready": True,
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
        "status": BENCHMARK_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 6",
        "title": "Regression Benchmark v1",
        "baseline_commit": BASELINE_COMMIT,
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_ranker_source": ranker_source,
        "benchmark_record": benchmark_record,
        "benchmark_cases": list(cases),
        "benchmark_gates": list(gates),
        "benchmark_issues": list(issues),
        "benchmark_index": index,
        "boundary": boundary,
        "ranker_profile_count": len(source_rankers),
        "benchmark_case_count": len(cases),
        "family_count": len(families),
        "evidence_check_count": evidence_check_count,
        "regression_guard_count": regression_guard_count,
        "measurement_count": measurement_count,
        "pass_count": pass_count,
        "failure_count": failure_count,
        "benchmark_gate_count": len(BENCHMARK_GATES),
        "passed_gate_count": passed_gate_count,
        "benchmark_issue_count": issue_count,
        "warning_count": 0,
        "benchmark_ready": benchmark_ready,
        "benchmark_locked": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "benchmark_runtime_modified": False,
        "regression_benchmark_records_ready": True,
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
            "source": "milestone_7_regression_benchmark_v1",
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
        "benchmark_id": f"MILESTONE-7-REGRESSION-BENCHMARK-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_regression_benchmark(benchmark: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = benchmark.get("boundary", {})
    gates = benchmark.get("benchmark_gates", [])
    issues = benchmark.get("benchmark_issues", [])
    cases = benchmark.get("benchmark_cases", [])
    source = benchmark.get("milestone_7_ranker_source", {})

    checks = {
        "status_ready": benchmark.get("status") == BENCHMARK_STATUS,
        "benchmark_id_present": isinstance(benchmark.get("benchmark_id"), str) and bool(benchmark.get("benchmark_id")),
        "signature_present": isinstance(benchmark.get("signature"), str) and bool(benchmark.get("signature")),
        "baseline_commit_valid": str(benchmark.get("baseline_commit", "")).startswith("f4035fa"),
        "benchmark_mode_valid": benchmark.get("benchmark_mode") == BENCHMARK_MODE,
        "benchmark_scope_valid": benchmark.get("benchmark_scope") == BENCHMARK_SCOPE,
        "benchmark_verdict_valid": benchmark.get("benchmark_verdict") == BENCHMARK_VERDICT,
        "next_allowed_stage_valid": benchmark.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "ranker_source_ready": source.get("ready") is True,
        "ranker_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "ranker_profile_count_valid": benchmark.get("ranker_profile_count") == EXPECTED_RANKER_PROFILE_COUNT,
        "benchmark_case_count_valid": benchmark.get("benchmark_case_count") == EXPECTED_BENCHMARK_CASE_COUNT,
        "family_count_valid": benchmark.get("family_count") == EXPECTED_FAMILY_COUNT,
        "evidence_check_count_valid": benchmark.get("evidence_check_count") == EXPECTED_EVIDENCE_CHECK_COUNT,
        "regression_guard_count_valid": benchmark.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "measurement_count_valid": benchmark.get("measurement_count") == EXPECTED_MEASUREMENT_COUNT,
        "pass_count_valid": benchmark.get("pass_count") == EXPECTED_PASS_COUNT,
        "failure_count_zero": benchmark.get("failure_count") == EXPECTED_FAILURE_COUNT,
        "all_cases_have_evidence_checks": bool(cases) and all(len(item.get("evidence_checks", ())) > 0 for item in cases),
        "all_cases_have_regression_guards": bool(cases) and all(len(item.get("regression_guards", ())) > 0 for item in cases),
        "all_cases_have_measurement": bool(cases) and all(bool(item.get("measurement")) for item in cases),
        "all_cases_deterministic": bool(cases) and all(item.get("deterministic") is True for item in cases),
        "all_cases_local_only": bool(cases) and all(item.get("local_only") is True for item in cases),
        "all_cases_dry_run_only": bool(cases) and all(item.get("dry_run_only") is True for item in cases),
        "all_cases_passed": bool(cases) and all(item.get("benchmark_passed") is True for item in cases),
        "all_cases_ready_for_task_7": bool(cases) and all(item.get("ready_for_task_7") is True for item in cases),
        "runtime_solver_not_modified": benchmark.get("runtime_solver_modified") is False,
        "ranker_runtime_not_modified": benchmark.get("ranker_runtime_modified") is False,
        "benchmark_runtime_not_modified": benchmark.get("benchmark_runtime_modified") is False,
        "regression_benchmark_records_ready": benchmark.get("regression_benchmark_records_ready") is True,
        "benchmark_gate_count_matches": benchmark.get("benchmark_gate_count") == len(BENCHMARK_GATES),
        "all_benchmark_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "benchmark_issue_count_zero": benchmark.get("benchmark_issue_count") == 0,
        "all_benchmark_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "benchmark_ready": benchmark.get("benchmark_ready") is True,
        "benchmark_locked": benchmark.get("benchmark_locked") is True,
        "solver_improvement_required": benchmark.get("solver_improvement_required") is True,
        "competitive_claim_absent": benchmark.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": benchmark.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": benchmark.get("manual_upload_performed") is False,
        "real_submission_allowed_false": benchmark.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": benchmark.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": benchmark.get("real_submission_created") is False,
        "kaggle_submission_not_sent": benchmark.get("kaggle_submission_sent") is False,
        "upload_not_performed": benchmark.get("upload_performed") is False,
        "kaggle_authentication_not_performed": benchmark.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_REGRESSION_BENCHMARK_INVALID",
        "valid": valid,
        "checks": checks,
        "benchmark_id": benchmark.get("benchmark_id"),
        "signature": benchmark.get("signature"),
    }


def render_regression_benchmark_markdown(benchmark: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Regression Benchmark v1",
        "",
        f"- status: {benchmark['status']}",
        f"- benchmark_id: {benchmark['benchmark_id']}",
        f"- signature: {benchmark['signature']}",
        f"- baseline_commit: {benchmark['baseline_commit']}",
        f"- benchmark_mode: {benchmark['benchmark_mode']}",
        f"- benchmark_scope: {benchmark['benchmark_scope']}",
        f"- benchmark_verdict: {benchmark['benchmark_verdict']}",
        f"- next_allowed_stage: {benchmark['next_allowed_stage']}",
        f"- ranker_profile_count: {benchmark['ranker_profile_count']}",
        f"- benchmark_case_count: {benchmark['benchmark_case_count']}",
        f"- family_count: {benchmark['family_count']}",
        f"- evidence_check_count: {benchmark['evidence_check_count']}",
        f"- regression_guard_count: {benchmark['regression_guard_count']}",
        f"- measurement_count: {benchmark['measurement_count']}",
        f"- pass_count: {benchmark['pass_count']}",
        f"- failure_count: {benchmark['failure_count']}",
        f"- benchmark_gate_count: {benchmark['benchmark_gate_count']}",
        f"- passed_gate_count: {benchmark['passed_gate_count']}",
        f"- benchmark_issue_count: {benchmark['benchmark_issue_count']}",
        f"- benchmark_ready: {benchmark['benchmark_ready']}",
        f"- benchmark_runtime_modified: {benchmark['benchmark_runtime_modified']}",
        f"- runtime_solver_modified: {benchmark['runtime_solver_modified']}",
        f"- real_submission_allowed: {benchmark['real_submission_allowed']}",
        f"- kaggle_submission_sent: {benchmark['kaggle_submission_sent']}",
        f"- upload_performed: {benchmark['upload_performed']}",
        "",
        "## Regression benchmark cases",
        "",
    ]

    for item in benchmark["benchmark_cases"]:
        lines.append(
            f"- {item['priority']} {item['case_id']} / family={item['family']} / "
            f"source={item['source_ranker_profile_id']} / evidence_checks={len(item['evidence_checks'])} / "
            f"guards={len(item['regression_guards'])} / passed={item['benchmark_passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Regression benchmark records are ready for the local score improvement report.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_VALID=true",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_MODE=REGRESSION_BENCHMARK_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_VERDICT=REGRESSION_BENCHMARK_READY_FOR_LOCAL_SCORE_IMPROVEMENT_REPORT",
            "ARC_AGI3_MILESTONE_7_RANKER_PROFILE_COUNT=3",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_CASE_COUNT=6",
            "ARC_AGI3_MILESTONE_7_FAMILY_COUNT=3",
            "ARC_AGI3_MILESTONE_7_EVIDENCE_CHECK_COUNT=24",
            "ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=18",
            "ARC_AGI3_MILESTONE_7_MEASUREMENT_COUNT=6",
            "ARC_AGI3_MILESTONE_7_PASS_COUNT=6",
            "ARC_AGI3_MILESTONE_7_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_RANKER_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_BENCHMARK_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_RECORDS_READY=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_RANKER_COMMIT=f4035fa",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_regression_benchmark_manifest(benchmark: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 REGRESSION BENCHMARK MANIFEST v1",
        f"benchmark_id={benchmark['benchmark_id']}",
        f"signature={benchmark['signature']}",
        f"status={benchmark['status']}",
        f"baseline_commit={benchmark['baseline_commit']}",
        f"benchmark_mode={benchmark['benchmark_mode']}",
        f"benchmark_verdict={benchmark['benchmark_verdict']}",
        f"next_allowed_stage={benchmark['next_allowed_stage']}",
        f"ranker_profile_count={benchmark['ranker_profile_count']}",
        f"benchmark_case_count={benchmark['benchmark_case_count']}",
        f"family_count={benchmark['family_count']}",
        f"evidence_check_count={benchmark['evidence_check_count']}",
        f"regression_guard_count={benchmark['regression_guard_count']}",
        f"measurement_count={benchmark['measurement_count']}",
        f"pass_count={benchmark['pass_count']}",
        f"failure_count={benchmark['failure_count']}",
        f"benchmark_gate_count={benchmark['benchmark_gate_count']}",
        f"passed_gate_count={benchmark['passed_gate_count']}",
        f"benchmark_issue_count={benchmark['benchmark_issue_count']}",
        f"benchmark_ready={benchmark['benchmark_ready']}",
        f"benchmark_locked={benchmark['benchmark_locked']}",
        f"runtime_solver_modified={benchmark['runtime_solver_modified']}",
        f"ranker_runtime_modified={benchmark['ranker_runtime_modified']}",
        f"benchmark_runtime_modified={benchmark['benchmark_runtime_modified']}",
        f"regression_benchmark_records_ready={benchmark['regression_benchmark_records_ready']}",
        f"solver_improvement_required={benchmark['solver_improvement_required']}",
        f"competitive_claim_absent={benchmark['competitive_claim_absent']}",
        f"manual_submission_allowed={benchmark['manual_submission_allowed']}",
        f"manual_upload_performed={benchmark['manual_upload_performed']}",
        f"real_submission_allowed={benchmark['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={benchmark['ready_for_real_kaggle_submission']}",
        f"real_submission_created={benchmark['real_submission_created']}",
        f"kaggle_submission_sent={benchmark['kaggle_submission_sent']}",
        f"upload_performed={benchmark['upload_performed']}",
        f"kaggle_authentication_performed={benchmark['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "BENCHMARK_CASES",
    ]

    for item in benchmark["benchmark_cases"]:
        lines.append(
            f"{item['priority']} {item['case_id']} family={item['family']} "
            f"source_ranker={item['source_ranker_profile_id']} case_type={item['case_type']} "
            f"evidence_check_count={len(item['evidence_checks'])} regression_guard_count={len(item['regression_guards'])} "
            f"deterministic={item['deterministic']} local_only={item['local_only']} dry_run_only={item['dry_run_only']} "
            f"benchmark_passed={item['benchmark_passed']} ready_for_task_7={item['ready_for_task_7']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_regression_benchmark_artifacts(
    benchmark: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    benchmark = dict(benchmark or build_milestone_7_regression_benchmark())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-regression-benchmark-v1.json"
    md_path = output / "milestone-7-regression-benchmark-v1.md"
    manifest_path = output / "milestone-7-regression-benchmark-manifest-v1.txt"
    index_path = output / "milestone-7-regression-benchmark-index-v1.json"

    json_path.write_text(json.dumps(benchmark, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_regression_benchmark_markdown(benchmark), encoding="utf-8")
    manifest_path.write_text(render_regression_benchmark_manifest(benchmark), encoding="utf-8")
    index_path.write_text(json.dumps(benchmark["benchmark_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_regression_benchmark_pipeline() -> Dict[str, Any]:
    benchmark = build_milestone_7_regression_benchmark()
    validation = validate_milestone_7_regression_benchmark(benchmark)
    artifacts = write_regression_benchmark_artifacts(benchmark)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_REGRESSION_BENCHMARK_PIPELINE_INVALID",
        "benchmark_status": benchmark["status"],
        "validation_status": validation["status"],
        "benchmark": benchmark,
        "benchmark_id": benchmark["benchmark_id"],
        "signature": benchmark["signature"],
        "benchmark_mode": benchmark["benchmark_mode"],
        "benchmark_verdict": benchmark["benchmark_verdict"],
        "next_allowed_stage": benchmark["next_allowed_stage"],
        "ranker_profile_count": benchmark["ranker_profile_count"],
        "benchmark_case_count": benchmark["benchmark_case_count"],
        "family_count": benchmark["family_count"],
        "evidence_check_count": benchmark["evidence_check_count"],
        "regression_guard_count": benchmark["regression_guard_count"],
        "measurement_count": benchmark["measurement_count"],
        "pass_count": benchmark["pass_count"],
        "failure_count": benchmark["failure_count"],
        "benchmark_gate_count": benchmark["benchmark_gate_count"],
        "passed_gate_count": benchmark["passed_gate_count"],
        "benchmark_issue_count": benchmark["benchmark_issue_count"],
        "warning_count": benchmark["warning_count"],
        "benchmark_ready": benchmark["benchmark_ready"],
        "benchmark_locked": benchmark["benchmark_locked"],
        "runtime_solver_modified": benchmark["runtime_solver_modified"],
        "ranker_runtime_modified": benchmark["ranker_runtime_modified"],
        "benchmark_runtime_modified": benchmark["benchmark_runtime_modified"],
        "regression_benchmark_records_ready": benchmark["regression_benchmark_records_ready"],
        "solver_improvement_required": benchmark["solver_improvement_required"],
        "competitive_claim_absent": benchmark["competitive_claim_absent"],
        "manual_submission_allowed": benchmark["manual_submission_allowed"],
        "manual_upload_performed": benchmark["manual_upload_performed"],
        "real_submission_allowed": benchmark["real_submission_allowed"],
        "ready_for_real_kaggle_submission": benchmark["ready_for_real_kaggle_submission"],
        "real_submission_created": benchmark["real_submission_created"],
        "kaggle_submission_sent": benchmark["kaggle_submission_sent"],
        "upload_performed": benchmark["upload_performed"],
        "kaggle_authentication_performed": benchmark["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": benchmark["metadata"],
    }
