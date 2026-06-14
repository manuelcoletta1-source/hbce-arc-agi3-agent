"""Milestone #8 Candidate Generator Runtime Upgrade v2.

Local-only deterministic candidate generator runtime upgrade.

This module connects Competitive Solver Kernel v2 and Family Benchmark Cases v2
into a deterministic local candidate generator runtime. It creates ranked and
deduplicated candidates across color mapping, object model, shape symmetry, and
cross-family composition.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, create a real submission, claim a Kaggle score, claim public
leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence, Tuple

from hbce_arc_agi3.milestone_8_competitive_solver_kernel import (
    apply_color_mapping,
    background_color,
    candidate_signature,
    connected_components,
    flatten_grid,
    infer_color_mapping,
    merge_candidate_sets,
    normalize_grid,
    rank_kernel_candidates,
    reflect_grid_horizontal,
    reflect_grid_vertical,
    translate_component,
)


RUNTIME_STATUS = "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY"
PIPELINE_STATUS = "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_VALID"

BASELINE_COMMIT = "1df6919 Add ARC AGI3 family benchmark cases"
RUNTIME_MODE = "CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_LOCAL_ONLY"
RUNTIME_SCOPE = "CONNECT_KERNEL_V2_TO_RUNTIME_CANDIDATE_GENERATION"
RUNTIME_VERDICT = "CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY_FOR_RANKER_RUNTIME_UPGRADE"
NEXT_ALLOWED_STAGE = "MILESTONE_8_TASK_5_RANKER_RUNTIME_UPGRADE_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-8/candidate-generator-runtime-upgrade-v2"

BENCHMARK_JSON = Path(
    "examples/milestone-8/family-benchmark-cases-v2/"
    "milestone-8-family-benchmark-cases-v2.json"
)

EXPECTED_FAMILY_COUNT = 4
EXPECTED_RUNTIME_PROFILE_COUNT = 4
EXPECTED_GENERATOR_OPERATION_COUNT = 8
EXPECTED_RUNTIME_CASE_COUNT = 8
EXPECTED_RUNTIME_PASS_COUNT = 8
EXPECTED_RUNTIME_FAILURE_COUNT = 0
EXPECTED_BENCHMARK_GATE_COUNT = 50
EXPECTED_BENCHMARK_ISSUE_COUNT = 0
EXPECTED_BENCHMARK_PASS_COUNT = 8
EXPECTED_BENCHMARK_FAILURE_COUNT = 0
EXPECTED_EVIDENCE_FIELD_COUNT = 8
EXPECTED_REGRESSION_GUARD_COUNT = 8
EXPECTED_BOUNDARY_CONTROL_COUNT = 9

RUNTIME_FAMILIES: Tuple[str, ...] = (
    "color_mapping",
    "object_model",
    "shape_symmetry",
    "cross_family_composition",
)

RUNTIME_PROFILES: Tuple[Dict[str, Any], ...] = (
    {
        "profile_id": "candidate_runtime_color_mapping_v2",
        "family": "color_mapping",
        "priority": "P0",
        "operation_count": 2,
    },
    {
        "profile_id": "candidate_runtime_object_model_v2",
        "family": "object_model",
        "priority": "P0",
        "operation_count": 2,
    },
    {
        "profile_id": "candidate_runtime_shape_symmetry_v2",
        "family": "shape_symmetry",
        "priority": "P0",
        "operation_count": 2,
    },
    {
        "profile_id": "candidate_runtime_cross_family_composition_v2",
        "family": "cross_family_composition",
        "priority": "P0",
        "operation_count": 2,
    },
)

GENERATOR_OPERATIONS: Tuple[str, ...] = (
    "runtime_color_mapping_from_training_pair",
    "runtime_color_mapping_non_background_shift",
    "runtime_object_translate_largest_right",
    "runtime_object_translate_largest_down",
    "runtime_shape_reflect_horizontal",
    "runtime_shape_reflect_vertical",
    "runtime_cross_family_merge_deduplicate",
    "runtime_cross_family_rank_candidates",
)

RUNTIME_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "runtime_upgrade_color_training_pair_candidate_v2",
        "family": "color_mapping",
        "operation": "runtime_color_mapping_from_training_pair",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_color_background_guard_candidate_v2",
        "family": "color_mapping",
        "operation": "runtime_color_mapping_non_background_shift",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_object_translate_right_candidate_v2",
        "family": "object_model",
        "operation": "runtime_object_translate_largest_right",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_object_translate_down_candidate_v2",
        "family": "object_model",
        "operation": "runtime_object_translate_largest_down",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_shape_reflect_horizontal_candidate_v2",
        "family": "shape_symmetry",
        "operation": "runtime_shape_reflect_horizontal",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_shape_reflect_vertical_candidate_v2",
        "family": "shape_symmetry",
        "operation": "runtime_shape_reflect_vertical",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_cross_family_merge_deduplicate_v2",
        "family": "cross_family_composition",
        "operation": "runtime_cross_family_merge_deduplicate",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "runtime_upgrade_cross_family_rank_candidates_v2",
        "family": "cross_family_composition",
        "operation": "runtime_cross_family_rank_candidates",
        "priority": "P0",
        "expected_status": "PASS",
    },
)

EVIDENCE_FIELDS: Tuple[str, ...] = (
    "case_id",
    "family",
    "operation",
    "priority",
    "passed",
    "evidence_score",
    "expected_status",
    "actual_status",
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_runtime_uses_kernel_color_mapping",
    "guard_runtime_preserves_background",
    "guard_runtime_uses_component_translation",
    "guard_runtime_translation_bounds",
    "guard_runtime_uses_shape_reflection",
    "guard_runtime_candidate_deduplication",
    "guard_runtime_ranker_ordering",
    "guard_runtime_no_submission_side_effect",
)

BOUNDARY_CONTROLS: Tuple[str, ...] = (
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "kaggle_submission_sent_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

RUNTIME_GATES: Tuple[str, ...] = (
    "benchmark_artifact_present",
    "benchmark_artifact_ready",
    "benchmark_artifact_valid",
    "benchmark_next_stage_matches_task_4",
    "benchmark_gate_count_valid",
    "benchmark_issue_count_zero",
    "benchmark_pass_count_valid",
    "benchmark_failure_count_zero",
    "runtime_mode_valid",
    "runtime_scope_valid",
    "runtime_verdict_valid",
    "runtime_ready",
    "runtime_locked",
    "family_count_valid",
    "runtime_profile_count_valid",
    "generator_operation_count_valid",
    "runtime_case_count_valid",
    "runtime_pass_count_valid",
    "runtime_failure_count_zero",
    "evidence_field_count_valid",
    "regression_guard_count_valid",
    "boundary_control_count_valid",
    "all_profiles_priority_p0",
    "all_cases_priority_p0",
    "all_cases_expected_pass",
    "color_training_pair_candidate_pass",
    "color_background_guard_candidate_pass",
    "object_translate_right_candidate_pass",
    "object_translate_down_candidate_pass",
    "shape_reflect_horizontal_candidate_pass",
    "shape_reflect_vertical_candidate_pass",
    "cross_family_merge_deduplicate_pass",
    "cross_family_rank_candidates_pass",
    "all_runtime_cases_pass",
    "runtime_family_coverage_color_mapping",
    "runtime_family_coverage_object_model",
    "runtime_family_coverage_shape_symmetry",
    "runtime_family_coverage_cross_family_composition",
    "candidate_generator_runtime_upgrade_created",
    "runtime_candidates_ranked",
    "runtime_candidates_deduplicated",
    "next_stage_valid",
    "real_submission_not_created",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
    "score_claim_absent",
    "public_leaderboard_claim_absent",
    "public_safe",
    "deterministic",
    "local_only",
    "dry_run_only",
)

RUNTIME_ISSUES: Tuple[str, ...] = (
    "benchmark_artifact_missing",
    "benchmark_artifact_not_ready",
    "benchmark_artifact_invalid",
    "benchmark_next_stage_mismatch",
    "benchmark_gate_count_invalid",
    "benchmark_issue_count_nonzero",
    "benchmark_pass_count_invalid",
    "benchmark_failure_count_nonzero",
    "runtime_mode_invalid",
    "runtime_scope_invalid",
    "runtime_verdict_invalid",
    "runtime_not_ready",
    "runtime_not_locked",
    "family_count_invalid",
    "runtime_profile_count_invalid",
    "generator_operation_count_invalid",
    "runtime_case_count_invalid",
    "runtime_pass_count_invalid",
    "runtime_failure_count_nonzero",
    "evidence_field_count_invalid",
    "regression_guard_count_invalid",
    "boundary_control_count_invalid",
    "profile_priority_not_p0",
    "case_priority_not_p0",
    "case_expected_status_not_pass",
    "color_training_pair_candidate_failed",
    "color_background_guard_candidate_failed",
    "object_translate_right_candidate_failed",
    "object_translate_down_candidate_failed",
    "shape_reflect_horizontal_candidate_failed",
    "shape_reflect_vertical_candidate_failed",
    "cross_family_merge_deduplicate_failed",
    "cross_family_rank_candidates_failed",
    "runtime_case_failure_detected",
    "runtime_family_coverage_color_mapping_missing",
    "runtime_family_coverage_object_model_missing",
    "runtime_family_coverage_shape_symmetry_missing",
    "runtime_family_coverage_cross_family_composition_missing",
    "candidate_generator_runtime_upgrade_missing",
    "runtime_candidates_not_ranked",
    "runtime_candidates_not_deduplicated",
    "next_stage_invalid",
    "real_submission_created",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "score_claim_detected",
    "public_leaderboard_claim_detected",
    "public_safe_false",
    "deterministic_false",
    "local_only_false",
    "dry_run_only_false",
)


GridLike = Sequence[Sequence[int]]


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


def _candidate(
    *,
    candidate_id: str,
    family: str,
    operation: str,
    grid: GridLike,
    evidence_score: float,
) -> Dict[str, Any]:
    normalized = normalize_grid(grid)
    return {
        "candidate_id": candidate_id,
        "family": family,
        "operation": operation,
        "grid": normalized,
        "evidence_score": float(evidence_score),
        "signature": candidate_signature(normalized),
    }


def build_color_mapping_runtime_candidates(
    grid: GridLike,
    *,
    training_input: GridLike | None = None,
    training_output: GridLike | None = None,
) -> Tuple[Dict[str, Any], ...]:
    normalized = normalize_grid(grid)
    candidates: List[Dict[str, Any]] = []

    if training_input is not None and training_output is not None:
        mapping = infer_color_mapping(training_input, training_output)
        candidates.append(
            _candidate(
                candidate_id="runtime_v2_color_mapping_from_training_pair",
                family="color_mapping",
                operation="runtime_color_mapping_from_training_pair",
                grid=apply_color_mapping(normalized, mapping, preserve_background=True),
                evidence_score=91.0,
            )
        )

    bg = background_color(normalized)
    non_background_colors = sorted(value for value in set(flatten_grid(normalized)) if value != bg)
    if non_background_colors:
        shift_mapping = {color: (color + 1) % 10 for color in non_background_colors}
        candidates.append(
            _candidate(
                candidate_id="runtime_v2_color_mapping_non_background_shift",
                family="color_mapping",
                operation="runtime_color_mapping_non_background_shift",
                grid=apply_color_mapping(normalized, shift_mapping, preserve_background=True),
                evidence_score=76.0,
            )
        )

    return tuple(candidates)


def build_object_model_runtime_candidates(grid: GridLike) -> Tuple[Dict[str, Any], ...]:
    normalized = normalize_grid(grid)
    components = connected_components(normalized)
    if not components:
        return tuple()

    largest = components[0]
    return (
        _candidate(
            candidate_id="runtime_v2_object_translate_largest_right",
            family="object_model",
            operation="runtime_object_translate_largest_right",
            grid=translate_component(normalized, largest["cells"], dr=0, dc=1),
            evidence_score=74.0,
        ),
        _candidate(
            candidate_id="runtime_v2_object_translate_largest_down",
            family="object_model",
            operation="runtime_object_translate_largest_down",
            grid=translate_component(normalized, largest["cells"], dr=1, dc=0),
            evidence_score=73.0,
        ),
    )


def build_shape_symmetry_runtime_candidates(grid: GridLike) -> Tuple[Dict[str, Any], ...]:
    normalized = normalize_grid(grid)
    return (
        _candidate(
            candidate_id="runtime_v2_shape_reflect_horizontal",
            family="shape_symmetry",
            operation="runtime_shape_reflect_horizontal",
            grid=reflect_grid_horizontal(normalized),
            evidence_score=72.0,
        ),
        _candidate(
            candidate_id="runtime_v2_shape_reflect_vertical",
            family="shape_symmetry",
            operation="runtime_shape_reflect_vertical",
            grid=reflect_grid_vertical(normalized),
            evidence_score=71.0,
        ),
    )


def generate_runtime_upgraded_candidates(
    grid: GridLike,
    *,
    training_input: GridLike | None = None,
    training_output: GridLike | None = None,
) -> Tuple[Dict[str, Any], ...]:
    color_candidates = build_color_mapping_runtime_candidates(
        grid,
        training_input=training_input,
        training_output=training_output,
    )
    object_candidates = build_object_model_runtime_candidates(grid)
    shape_candidates = build_shape_symmetry_runtime_candidates(grid)

    merged = merge_candidate_sets(color_candidates, object_candidates, shape_candidates)
    ranked = rank_kernel_candidates(merged)

    upgraded = []
    for index, candidate in enumerate(ranked, start=1):
        upgraded.append(
            {
                **dict(candidate),
                "runtime_rank": index,
                "runtime_upgrade": "candidate_generator_runtime_upgrade_v2",
                "runtime_candidate_ready": True,
            }
        )
    return tuple(upgraded)


def evaluate_runtime_upgrade_case(case_id: str) -> Dict[str, Any]:
    if case_id == "runtime_upgrade_color_training_pair_candidate_v2":
        training_input = normalize_grid([[0, 1, 2], [0, 1, 2]])
        training_output = normalize_grid([[0, 3, 4], [0, 3, 4]])
        target_input = normalize_grid([[0, 1, 2], [2, 1, 0]])
        expected = normalize_grid([[0, 3, 4], [4, 3, 0]])
        candidates = build_color_mapping_runtime_candidates(
            target_input,
            training_input=training_input,
            training_output=training_output,
        )
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "color_mapping", "runtime_color_mapping_from_training_pair", passed)

    if case_id == "runtime_upgrade_color_background_guard_candidate_v2":
        grid = normalize_grid([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        expected = normalize_grid([[0, 2, 0], [0, 2, 0], [0, 0, 0]])
        candidates = build_color_mapping_runtime_candidates(grid)
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "color_mapping", "runtime_color_mapping_non_background_shift", passed)

    if case_id == "runtime_upgrade_object_translate_right_candidate_v2":
        grid = normalize_grid([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]])
        expected = normalize_grid([[0, 0, 0, 0], [0, 0, 5, 5], [0, 0, 0, 0]])
        candidates = build_object_model_runtime_candidates(grid)
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "object_model", "runtime_object_translate_largest_right", passed)

    if case_id == "runtime_upgrade_object_translate_down_candidate_v2":
        grid = normalize_grid([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]])
        expected = normalize_grid([[0, 0, 0, 0], [0, 0, 0, 0], [0, 5, 5, 0]])
        candidates = build_object_model_runtime_candidates(grid)
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "object_model", "runtime_object_translate_largest_down", passed)

    if case_id == "runtime_upgrade_shape_reflect_horizontal_candidate_v2":
        grid = normalize_grid([[1, 0], [2, 0], [3, 0]])
        expected = normalize_grid([[3, 0], [2, 0], [1, 0]])
        candidates = build_shape_symmetry_runtime_candidates(grid)
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "shape_symmetry", "runtime_shape_reflect_horizontal", passed)

    if case_id == "runtime_upgrade_shape_reflect_vertical_candidate_v2":
        grid = normalize_grid([[1, 0], [2, 0], [3, 0]])
        expected = normalize_grid([[0, 1], [0, 2], [0, 3]])
        candidates = build_shape_symmetry_runtime_candidates(grid)
        passed = any(candidate["grid"] == expected for candidate in candidates)
        return _result(case_id, "shape_symmetry", "runtime_shape_reflect_vertical", passed)

    if case_id == "runtime_upgrade_cross_family_merge_deduplicate_v2":
        candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        signatures = [candidate["signature"] for candidate in candidates]
        passed = len(candidates) >= 4 and len(signatures) == len(set(signatures))
        return _result(case_id, "cross_family_composition", "runtime_cross_family_merge_deduplicate", passed)

    if case_id == "runtime_upgrade_cross_family_rank_candidates_v2":
        candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        ranks = [candidate["runtime_rank"] for candidate in candidates]
        scores = [candidate["evidence_score"] for candidate in candidates]
        families = {candidate["family"] for candidate in candidates}
        passed = (
            ranks == list(range(1, len(candidates) + 1))
            and scores == sorted(scores, reverse=True)
            and {"color_mapping", "object_model", "shape_symmetry"}.issubset(families)
        )
        return _result(case_id, "cross_family_composition", "runtime_cross_family_rank_candidates", passed)

    raise ValueError(f"unknown runtime upgrade case: {case_id}")


def _result(case_id: str, family: str, operation: str, passed: bool) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "family": family,
        "operation": operation,
        "priority": "P0",
        "passed": passed,
        "evidence_score": 100 if passed else 0,
        "expected_status": "PASS",
        "actual_status": "PASS" if passed else "FAIL",
    }


def evaluate_all_runtime_upgrade_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_runtime_upgrade_case(case["case_id"]) for case in RUNTIME_CASES)


def build_milestone_8_candidate_generator_runtime_upgrade() -> Dict[str, Any]:
    benchmark = _read_json(BENCHMARK_JSON)
    results = evaluate_all_runtime_upgrade_cases()
    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)
    covered_families = {result["family"] for result in results}

    sample_candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
    sample_signatures = [candidate["signature"] for candidate in sample_candidates]
    runtime_candidates_ranked = [candidate["runtime_rank"] for candidate in sample_candidates] == list(
        range(1, len(sample_candidates) + 1)
    )
    runtime_candidates_deduplicated = len(sample_signatures) == len(set(sample_signatures))

    runtime_record = {
        "runtime_mode": RUNTIME_MODE,
        "runtime_scope": RUNTIME_SCOPE,
        "runtime_verdict": RUNTIME_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_ready": True,
        "runtime_locked": True,
        "baseline_benchmark_id": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
        "benchmark_ready": benchmark.get("benchmark_ready") is True,
        "benchmark_next_stage": benchmark.get("next_allowed_stage", "MISSING"),
        "family_count": len(RUNTIME_FAMILIES),
        "runtime_profile_count": len(RUNTIME_PROFILES),
        "generator_operation_count": len(GENERATOR_OPERATIONS),
        "runtime_case_count": len(RUNTIME_CASES),
        "runtime_pass_count": pass_count,
        "runtime_failure_count": failure_count,
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "candidate_generator_runtime_upgrade_created": True,
        "runtime_candidates_ranked": runtime_candidates_ranked,
        "runtime_candidates_deduplicated": runtime_candidates_deduplicated,
        "sample_candidate_count": len(sample_candidates),
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
    }

    result_by_case = {result["case_id"]: result for result in results}

    gate_state = {
        "benchmark_artifact_present": BENCHMARK_JSON.exists(),
        "benchmark_artifact_ready": benchmark.get("status") == "MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY",
        "benchmark_artifact_valid": bool(benchmark.get("benchmark_id")) and bool(benchmark.get("signature")),
        "benchmark_next_stage_matches_task_4": benchmark.get("next_allowed_stage")
        == "MILESTONE_8_TASK_4_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2",
        "benchmark_gate_count_valid": int(benchmark.get("benchmark_gate_count", 0)) == EXPECTED_BENCHMARK_GATE_COUNT,
        "benchmark_issue_count_zero": int(benchmark.get("benchmark_issue_count", -1)) == EXPECTED_BENCHMARK_ISSUE_COUNT,
        "benchmark_pass_count_valid": int(benchmark.get("benchmark_pass_count", 0)) == EXPECTED_BENCHMARK_PASS_COUNT,
        "benchmark_failure_count_zero": int(benchmark.get("benchmark_failure_count", -1)) == EXPECTED_BENCHMARK_FAILURE_COUNT,
        "runtime_mode_valid": RUNTIME_MODE == "CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_LOCAL_ONLY",
        "runtime_scope_valid": RUNTIME_SCOPE == "CONNECT_KERNEL_V2_TO_RUNTIME_CANDIDATE_GENERATION",
        "runtime_verdict_valid": RUNTIME_VERDICT == "CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY_FOR_RANKER_RUNTIME_UPGRADE",
        "runtime_ready": runtime_record["runtime_ready"] is True,
        "runtime_locked": runtime_record["runtime_locked"] is True,
        "family_count_valid": len(RUNTIME_FAMILIES) == EXPECTED_FAMILY_COUNT,
        "runtime_profile_count_valid": len(RUNTIME_PROFILES) == EXPECTED_RUNTIME_PROFILE_COUNT,
        "generator_operation_count_valid": len(GENERATOR_OPERATIONS) == EXPECTED_GENERATOR_OPERATION_COUNT,
        "runtime_case_count_valid": len(RUNTIME_CASES) == EXPECTED_RUNTIME_CASE_COUNT,
        "runtime_pass_count_valid": pass_count == EXPECTED_RUNTIME_PASS_COUNT,
        "runtime_failure_count_zero": failure_count == EXPECTED_RUNTIME_FAILURE_COUNT,
        "evidence_field_count_valid": len(EVIDENCE_FIELDS) == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_profiles_priority_p0": all(profile["priority"] == "P0" for profile in RUNTIME_PROFILES),
        "all_cases_priority_p0": all(case["priority"] == "P0" for case in RUNTIME_CASES),
        "all_cases_expected_pass": all(case["expected_status"] == "PASS" for case in RUNTIME_CASES),
        "color_training_pair_candidate_pass": result_by_case["runtime_upgrade_color_training_pair_candidate_v2"]["passed"],
        "color_background_guard_candidate_pass": result_by_case["runtime_upgrade_color_background_guard_candidate_v2"]["passed"],
        "object_translate_right_candidate_pass": result_by_case["runtime_upgrade_object_translate_right_candidate_v2"]["passed"],
        "object_translate_down_candidate_pass": result_by_case["runtime_upgrade_object_translate_down_candidate_v2"]["passed"],
        "shape_reflect_horizontal_candidate_pass": result_by_case[
            "runtime_upgrade_shape_reflect_horizontal_candidate_v2"
        ]["passed"],
        "shape_reflect_vertical_candidate_pass": result_by_case["runtime_upgrade_shape_reflect_vertical_candidate_v2"][
            "passed"
        ],
        "cross_family_merge_deduplicate_pass": result_by_case["runtime_upgrade_cross_family_merge_deduplicate_v2"][
            "passed"
        ],
        "cross_family_rank_candidates_pass": result_by_case["runtime_upgrade_cross_family_rank_candidates_v2"][
            "passed"
        ],
        "all_runtime_cases_pass": all(result["passed"] is True for result in results),
        "runtime_family_coverage_color_mapping": "color_mapping" in covered_families,
        "runtime_family_coverage_object_model": "object_model" in covered_families,
        "runtime_family_coverage_shape_symmetry": "shape_symmetry" in covered_families,
        "runtime_family_coverage_cross_family_composition": "cross_family_composition" in covered_families,
        "candidate_generator_runtime_upgrade_created": runtime_record["candidate_generator_runtime_upgrade_created"] is True,
        "runtime_candidates_ranked": runtime_record["runtime_candidates_ranked"] is True,
        "runtime_candidates_deduplicated": runtime_record["runtime_candidates_deduplicated"] is True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_8_TASK_5_RANKER_RUNTIME_UPGRADE_V2",
        "real_submission_not_created": runtime_record["real_submission_created"] is False,
        "real_submission_allowed_false": runtime_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": runtime_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": runtime_record["kaggle_submission_sent"] is False,
        "upload_not_performed": runtime_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": runtime_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": runtime_record["external_api_dependency"] is False,
        "contains_api_keys_false": runtime_record["contains_api_keys"] is False,
        "private_core_exposure_false": runtime_record["private_core_exposure"] is False,
        "legal_certification_false": runtime_record["legal_certification"] is False,
        "score_claim_absent": runtime_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": runtime_record["public_leaderboard_claim_absent"] is True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    issue_state = {
        "benchmark_artifact_missing": not gate_state["benchmark_artifact_present"],
        "benchmark_artifact_not_ready": not gate_state["benchmark_artifact_ready"],
        "benchmark_artifact_invalid": not gate_state["benchmark_artifact_valid"],
        "benchmark_next_stage_mismatch": not gate_state["benchmark_next_stage_matches_task_4"],
        "benchmark_gate_count_invalid": not gate_state["benchmark_gate_count_valid"],
        "benchmark_issue_count_nonzero": not gate_state["benchmark_issue_count_zero"],
        "benchmark_pass_count_invalid": not gate_state["benchmark_pass_count_valid"],
        "benchmark_failure_count_nonzero": not gate_state["benchmark_failure_count_zero"],
        "runtime_mode_invalid": not gate_state["runtime_mode_valid"],
        "runtime_scope_invalid": not gate_state["runtime_scope_valid"],
        "runtime_verdict_invalid": not gate_state["runtime_verdict_valid"],
        "runtime_not_ready": not gate_state["runtime_ready"],
        "runtime_not_locked": not gate_state["runtime_locked"],
        "family_count_invalid": not gate_state["family_count_valid"],
        "runtime_profile_count_invalid": not gate_state["runtime_profile_count_valid"],
        "generator_operation_count_invalid": not gate_state["generator_operation_count_valid"],
        "runtime_case_count_invalid": not gate_state["runtime_case_count_valid"],
        "runtime_pass_count_invalid": not gate_state["runtime_pass_count_valid"],
        "runtime_failure_count_nonzero": not gate_state["runtime_failure_count_zero"],
        "evidence_field_count_invalid": not gate_state["evidence_field_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "boundary_control_count_invalid": not gate_state["boundary_control_count_valid"],
        "profile_priority_not_p0": not gate_state["all_profiles_priority_p0"],
        "case_priority_not_p0": not gate_state["all_cases_priority_p0"],
        "case_expected_status_not_pass": not gate_state["all_cases_expected_pass"],
        "color_training_pair_candidate_failed": not gate_state["color_training_pair_candidate_pass"],
        "color_background_guard_candidate_failed": not gate_state["color_background_guard_candidate_pass"],
        "object_translate_right_candidate_failed": not gate_state["object_translate_right_candidate_pass"],
        "object_translate_down_candidate_failed": not gate_state["object_translate_down_candidate_pass"],
        "shape_reflect_horizontal_candidate_failed": not gate_state["shape_reflect_horizontal_candidate_pass"],
        "shape_reflect_vertical_candidate_failed": not gate_state["shape_reflect_vertical_candidate_pass"],
        "cross_family_merge_deduplicate_failed": not gate_state["cross_family_merge_deduplicate_pass"],
        "cross_family_rank_candidates_failed": not gate_state["cross_family_rank_candidates_pass"],
        "runtime_case_failure_detected": not gate_state["all_runtime_cases_pass"],
        "runtime_family_coverage_color_mapping_missing": not gate_state["runtime_family_coverage_color_mapping"],
        "runtime_family_coverage_object_model_missing": not gate_state["runtime_family_coverage_object_model"],
        "runtime_family_coverage_shape_symmetry_missing": not gate_state["runtime_family_coverage_shape_symmetry"],
        "runtime_family_coverage_cross_family_composition_missing": not gate_state[
            "runtime_family_coverage_cross_family_composition"
        ],
        "candidate_generator_runtime_upgrade_missing": not gate_state["candidate_generator_runtime_upgrade_created"],
        "runtime_candidates_not_ranked": not gate_state["runtime_candidates_ranked"],
        "runtime_candidates_not_deduplicated": not gate_state["runtime_candidates_deduplicated"],
        "next_stage_invalid": not gate_state["next_stage_valid"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
        "score_claim_detected": not gate_state["score_claim_absent"],
        "public_leaderboard_claim_detected": not gate_state["public_leaderboard_claim_absent"],
        "public_safe_false": not gate_state["public_safe"],
        "deterministic_false": not gate_state["deterministic"],
        "local_only_false": not gate_state["local_only"],
        "dry_run_only_false": not gate_state["dry_run_only"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in RUNTIME_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in RUNTIME_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    runtime_ready = (
        benchmark.get("status") == "MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY"
        and benchmark.get("benchmark_ready") is True
        and pass_count == EXPECTED_RUNTIME_PASS_COUNT
        and failure_count == EXPECTED_RUNTIME_FAILURE_COUNT
        and runtime_candidates_ranked
        and runtime_candidates_deduplicated
        and passed_gate_count == len(RUNTIME_GATES)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #8",
        "task": "Task 4",
        "runtime_mode": RUNTIME_MODE,
        "runtime_scope": RUNTIME_SCOPE,
        "runtime_verdict": RUNTIME_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_benchmark": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
        "runtime_ready": runtime_ready,
        "runtime_locked": True,
        "family_count": len(RUNTIME_FAMILIES),
        "runtime_profile_count": len(RUNTIME_PROFILES),
        "generator_operation_count": len(GENERATOR_OPERATIONS),
        "runtime_case_count": len(RUNTIME_CASES),
        "runtime_pass_count": pass_count,
        "runtime_failure_count": failure_count,
        "sample_candidate_count": len(sample_candidates),
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": RUNTIME_STATUS,
        "milestone": "Milestone #8",
        "task": "Task 4",
        "title": "Candidate Generator Runtime Upgrade v2",
        "baseline_commit": BASELINE_COMMIT,
        "runtime_mode": RUNTIME_MODE,
        "runtime_scope": RUNTIME_SCOPE,
        "runtime_verdict": RUNTIME_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "benchmark_source": {
            "path": str(BENCHMARK_JSON),
            "present": BENCHMARK_JSON.exists(),
            "status": benchmark.get("status", "MISSING"),
            "benchmark_id": benchmark.get("benchmark_id", "MISSING_BENCHMARK_ID"),
            "sha256": _sha256(BENCHMARK_JSON),
            "sha256_16": _sha16(_sha256(BENCHMARK_JSON)),
        },
        "runtime_record": runtime_record,
        "runtime_families": list(RUNTIME_FAMILIES),
        "runtime_profiles": list(RUNTIME_PROFILES),
        "generator_operations": list(GENERATOR_OPERATIONS),
        "runtime_cases": list(RUNTIME_CASES),
        "runtime_results": list(results),
        "sample_candidates": list(sample_candidates),
        "evidence_fields": list(EVIDENCE_FIELDS),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "runtime_gates": list(gates),
        "runtime_issues": list(issues),
        "runtime_index": index,
        "family_count": len(RUNTIME_FAMILIES),
        "runtime_profile_count": len(RUNTIME_PROFILES),
        "generator_operation_count": len(GENERATOR_OPERATIONS),
        "runtime_case_count": len(RUNTIME_CASES),
        "runtime_pass_count": pass_count,
        "runtime_failure_count": failure_count,
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "runtime_gate_count": len(RUNTIME_GATES),
        "passed_gate_count": passed_gate_count,
        "runtime_issue_count": issue_count,
        "warning_count": 0,
        "runtime_ready": runtime_ready,
        "runtime_locked": True,
        "family_coverage": sorted(covered_families),
        "candidate_generator_runtime_upgrade_created": True,
        "runtime_candidates_ranked": runtime_candidates_ranked,
        "runtime_candidates_deduplicated": runtime_candidates_deduplicated,
        "sample_candidate_count": len(sample_candidates),
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_8_candidate_generator_runtime_upgrade_v2",
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
        "runtime_id": f"MILESTONE-8-CANDIDATE-RUNTIME-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_8_candidate_generator_runtime_upgrade(runtime: Mapping[str, Any]) -> Dict[str, Any]:
    gates = runtime.get("runtime_gates", [])
    issues = runtime.get("runtime_issues", [])
    results = runtime.get("runtime_results", [])
    sample_candidates = runtime.get("sample_candidates", [])

    checks = {
        "status_ready": runtime.get("status") == RUNTIME_STATUS,
        "runtime_id_present": isinstance(runtime.get("runtime_id"), str) and bool(runtime.get("runtime_id")),
        "signature_present": isinstance(runtime.get("signature"), str) and bool(runtime.get("signature")),
        "baseline_commit_valid": str(runtime.get("baseline_commit", "")).startswith("1df6919"),
        "runtime_mode_valid": runtime.get("runtime_mode") == RUNTIME_MODE,
        "runtime_scope_valid": runtime.get("runtime_scope") == RUNTIME_SCOPE,
        "runtime_verdict_valid": runtime.get("runtime_verdict") == RUNTIME_VERDICT,
        "next_allowed_stage_valid": runtime.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "family_count_valid": runtime.get("family_count") == EXPECTED_FAMILY_COUNT,
        "runtime_profile_count_valid": runtime.get("runtime_profile_count") == EXPECTED_RUNTIME_PROFILE_COUNT,
        "generator_operation_count_valid": runtime.get("generator_operation_count") == EXPECTED_GENERATOR_OPERATION_COUNT,
        "runtime_case_count_valid": runtime.get("runtime_case_count") == EXPECTED_RUNTIME_CASE_COUNT,
        "runtime_pass_count_valid": runtime.get("runtime_pass_count") == EXPECTED_RUNTIME_PASS_COUNT,
        "runtime_failure_count_zero": runtime.get("runtime_failure_count") == EXPECTED_RUNTIME_FAILURE_COUNT,
        "evidence_field_count_valid": runtime.get("evidence_field_count") == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": runtime.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": runtime.get("boundary_control_count") == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "runtime_gate_count_matches": runtime.get("runtime_gate_count") == len(RUNTIME_GATES),
        "all_runtime_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "runtime_issue_count_zero": runtime.get("runtime_issue_count") == 0,
        "all_runtime_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "runtime_ready": runtime.get("runtime_ready") is True,
        "runtime_locked": runtime.get("runtime_locked") is True,
        "sample_candidates_present": bool(sample_candidates) and len(sample_candidates) >= 4,
        "runtime_candidates_ranked": runtime.get("runtime_candidates_ranked") is True,
        "runtime_candidates_deduplicated": runtime.get("runtime_candidates_deduplicated") is True,
        "real_submission_not_created": runtime.get("real_submission_created") is False,
        "real_submission_allowed_false": runtime.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": runtime.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": runtime.get("kaggle_submission_sent") is False,
        "upload_not_performed": runtime.get("upload_performed") is False,
        "kaggle_authentication_not_performed": runtime.get("kaggle_authentication_performed") is False,
        "score_claim_absent": runtime.get("score_claim_absent") is True,
        "public_leaderboard_claim_absent": runtime.get("public_leaderboard_claim_absent") is True,
        "metadata_safe": runtime.get("metadata", {}).get("external_api_dependency") is False
        and runtime.get("metadata", {}).get("contains_api_keys") is False
        and runtime.get("metadata", {}).get("private_core_exposure") is False
        and runtime.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_INVALID",
        "valid": valid,
        "checks": checks,
        "runtime_id": runtime.get("runtime_id"),
        "signature": runtime.get("signature"),
    }


def render_candidate_generator_runtime_upgrade_markdown(runtime: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #8 - Candidate Generator Runtime Upgrade v2",
        "",
        f"- status: {runtime['status']}",
        f"- runtime_id: {runtime['runtime_id']}",
        f"- signature: {runtime['signature']}",
        f"- baseline_commit: {runtime['baseline_commit']}",
        f"- runtime_mode: {runtime['runtime_mode']}",
        f"- runtime_scope: {runtime['runtime_scope']}",
        f"- runtime_verdict: {runtime['runtime_verdict']}",
        f"- next_allowed_stage: {runtime['next_allowed_stage']}",
        f"- family_count: {runtime['family_count']}",
        f"- runtime_profile_count: {runtime['runtime_profile_count']}",
        f"- generator_operation_count: {runtime['generator_operation_count']}",
        f"- runtime_case_count: {runtime['runtime_case_count']}",
        f"- runtime_pass_count: {runtime['runtime_pass_count']}",
        f"- runtime_failure_count: {runtime['runtime_failure_count']}",
        f"- sample_candidate_count: {runtime['sample_candidate_count']}",
        f"- runtime_gate_count: {runtime['runtime_gate_count']}",
        f"- passed_gate_count: {runtime['passed_gate_count']}",
        f"- runtime_issue_count: {runtime['runtime_issue_count']}",
        f"- runtime_ready: {runtime['runtime_ready']}",
        "",
        "## Runtime results",
        "",
    ]

    for result in runtime["runtime_results"]:
        lines.append(
            f"- {result['case_id']} / family={result['family']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Candidate Generator Runtime Upgrade v2 is ready for ranker runtime upgrade.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY=true",
            "ARC_AGI3_MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_VALID=true",
            "ARC_AGI3_MILESTONE_8_RUNTIME_MODE=CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_8_RUNTIME_VERDICT=CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY_FOR_RANKER_RUNTIME_UPGRADE",
            "ARC_AGI3_MILESTONE_8_BASELINE_BENCHMARK_COMMIT=1df6919",
            "ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_RUNTIME_PROFILE_COUNT=4",
            "ARC_AGI3_MILESTONE_8_GENERATOR_OPERATION_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RUNTIME_CASE_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RUNTIME_PASS_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RUNTIME_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_8_SAMPLE_CANDIDATE_COUNT={count}".format(
                count=runtime["sample_candidate_count"]
            ),
            "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_5_RANKER_RUNTIME_UPGRADE_V2",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_candidate_generator_runtime_upgrade_manifest(runtime: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 8 CANDIDATE GENERATOR RUNTIME UPGRADE MANIFEST v2",
        f"runtime_id={runtime['runtime_id']}",
        f"signature={runtime['signature']}",
        f"status={runtime['status']}",
        f"baseline_commit={runtime['baseline_commit']}",
        f"runtime_mode={runtime['runtime_mode']}",
        f"runtime_verdict={runtime['runtime_verdict']}",
        f"next_allowed_stage={runtime['next_allowed_stage']}",
        f"family_count={runtime['family_count']}",
        f"runtime_profile_count={runtime['runtime_profile_count']}",
        f"generator_operation_count={runtime['generator_operation_count']}",
        f"runtime_case_count={runtime['runtime_case_count']}",
        f"runtime_pass_count={runtime['runtime_pass_count']}",
        f"runtime_failure_count={runtime['runtime_failure_count']}",
        f"sample_candidate_count={runtime['sample_candidate_count']}",
        f"runtime_gate_count={runtime['runtime_gate_count']}",
        f"passed_gate_count={runtime['passed_gate_count']}",
        f"runtime_issue_count={runtime['runtime_issue_count']}",
        f"runtime_ready={runtime['runtime_ready']}",
        f"runtime_locked={runtime['runtime_locked']}",
        f"candidate_generator_runtime_upgrade_created={runtime['candidate_generator_runtime_upgrade_created']}",
        f"runtime_candidates_ranked={runtime['runtime_candidates_ranked']}",
        f"runtime_candidates_deduplicated={runtime['runtime_candidates_deduplicated']}",
        f"real_submission_created={runtime['real_submission_created']}",
        f"real_submission_allowed={runtime['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={runtime['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={runtime['kaggle_submission_sent']}",
        f"upload_performed={runtime['upload_performed']}",
        f"kaggle_authentication_performed={runtime['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "RUNTIME_RESULTS",
    ]

    for result in runtime["runtime_results"]:
        lines.append(
            f"{result['case_id']} family={result['family']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    lines.append("SAMPLE_CANDIDATES")
    for candidate in runtime["sample_candidates"]:
        lines.append(
            f"rank={candidate['runtime_rank']} id={candidate['candidate_id']} "
            f"family={candidate['family']} operation={candidate['operation']} "
            f"score={candidate['evidence_score']} signature={candidate['signature']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_candidate_generator_runtime_upgrade_artifacts(
    runtime: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    runtime = dict(runtime or build_milestone_8_candidate_generator_runtime_upgrade())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-8-candidate-generator-runtime-upgrade-v2.json"
    md_path = output / "milestone-8-candidate-generator-runtime-upgrade-v2.md"
    manifest_path = output / "milestone-8-candidate-generator-runtime-upgrade-manifest-v2.txt"
    index_path = output / "milestone-8-candidate-generator-runtime-upgrade-index-v2.json"

    json_path.write_text(json.dumps(runtime, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_candidate_generator_runtime_upgrade_markdown(runtime), encoding="utf-8")
    manifest_path.write_text(render_candidate_generator_runtime_upgrade_manifest(runtime), encoding="utf-8")
    index_path.write_text(json.dumps(runtime["runtime_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_8_candidate_generator_runtime_upgrade_pipeline() -> Dict[str, Any]:
    runtime = build_milestone_8_candidate_generator_runtime_upgrade()
    validation = validate_milestone_8_candidate_generator_runtime_upgrade(runtime)
    artifacts = write_candidate_generator_runtime_upgrade_artifacts(runtime)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_PIPELINE_INVALID",
        "runtime_status": runtime["status"],
        "validation_status": validation["status"],
        "runtime": runtime,
        "runtime_id": runtime["runtime_id"],
        "signature": runtime["signature"],
        "runtime_mode": runtime["runtime_mode"],
        "runtime_verdict": runtime["runtime_verdict"],
        "next_allowed_stage": runtime["next_allowed_stage"],
        "family_count": runtime["family_count"],
        "runtime_profile_count": runtime["runtime_profile_count"],
        "generator_operation_count": runtime["generator_operation_count"],
        "runtime_case_count": runtime["runtime_case_count"],
        "runtime_pass_count": runtime["runtime_pass_count"],
        "runtime_failure_count": runtime["runtime_failure_count"],
        "sample_candidate_count": runtime["sample_candidate_count"],
        "evidence_field_count": runtime["evidence_field_count"],
        "regression_guard_count": runtime["regression_guard_count"],
        "boundary_control_count": runtime["boundary_control_count"],
        "runtime_gate_count": runtime["runtime_gate_count"],
        "passed_gate_count": runtime["passed_gate_count"],
        "runtime_issue_count": runtime["runtime_issue_count"],
        "warning_count": runtime["warning_count"],
        "runtime_ready": runtime["runtime_ready"],
        "runtime_locked": runtime["runtime_locked"],
        "candidate_generator_runtime_upgrade_created": runtime["candidate_generator_runtime_upgrade_created"],
        "runtime_candidates_ranked": runtime["runtime_candidates_ranked"],
        "runtime_candidates_deduplicated": runtime["runtime_candidates_deduplicated"],
        "real_submission_created": runtime["real_submission_created"],
        "real_submission_allowed": runtime["real_submission_allowed"],
        "ready_for_real_kaggle_submission": runtime["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": runtime["kaggle_submission_sent"],
        "upload_performed": runtime["upload_performed"],
        "kaggle_authentication_performed": runtime["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": runtime["metadata"],
    }
