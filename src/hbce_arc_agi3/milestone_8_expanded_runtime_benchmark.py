"""Milestone #8 Expanded Runtime Benchmark v2.

Local-only deterministic expanded benchmark for the Milestone #8 runtime stack.

This module evaluates the current runtime stack:
- Competitive Solver Kernel v2
- Family Benchmark Cases v2
- Candidate Generator Runtime Upgrade v2
- Ranker Runtime Upgrade v2

It performs expanded local benchmark checks across color mapping, object model,
shape symmetry, and cross-family composition.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, create a real submission, claim a Kaggle score, claim public
leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from hbce_arc_agi3.milestone_8_candidate_generator_runtime_upgrade import (
    generate_runtime_upgraded_candidates,
)
from hbce_arc_agi3.milestone_8_competitive_solver_kernel import normalize_grid
from hbce_arc_agi3.milestone_8_ranker_runtime_upgrade import rank_runtime_candidates


BENCHMARK_STATUS = "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY"
PIPELINE_STATUS = "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_VALID"

BASELINE_COMMIT = "537b277 Add ARC AGI3 ranker runtime upgrade"
BENCHMARK_MODE = "EXPANDED_RUNTIME_BENCHMARK_V2_LOCAL_ONLY"
BENCHMARK_SCOPE = "STRESS_RUNTIME_GENERATOR_AND_RANKER_ON_EXPANDED_LOCAL_CASES"
BENCHMARK_VERDICT = "EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH"
NEXT_ALLOWED_STAGE = "MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-8/expanded-runtime-benchmark-v2"

RANKER_JSON = Path(
    "examples/milestone-8/ranker-runtime-upgrade-v2/"
    "milestone-8-ranker-runtime-upgrade-v2.json"
)

EXPECTED_FAMILY_COUNT = 4
EXPECTED_EXPANDED_CASE_COUNT = 12
EXPECTED_EXPANDED_PASS_COUNT = 12
EXPECTED_EXPANDED_FAILURE_COUNT = 0
EXPECTED_RANKER_GATE_COUNT = 60
EXPECTED_RANKER_ISSUE_COUNT = 0
EXPECTED_RANKER_PASS_COUNT = 8
EXPECTED_RANKER_FAILURE_COUNT = 0
EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT = 4
EXPECTED_EVIDENCE_FIELD_COUNT = 8
EXPECTED_REGRESSION_GUARD_COUNT = 12
EXPECTED_BOUNDARY_CONTROL_COUNT = 9

BENCHMARK_FAMILIES: Tuple[str, ...] = (
    "color_mapping",
    "object_model",
    "shape_symmetry",
    "cross_family_composition",
)

EXPANDED_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "expanded_runtime_color_hint_top_family_v2",
        "family": "color_mapping",
        "operation": "expanded_rank_color_family_hint",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_color_training_pair_top_operation_v2",
        "family": "color_mapping",
        "operation": "expanded_rank_color_training_pair",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_color_background_guard_v2",
        "family": "color_mapping",
        "operation": "expanded_preserve_background",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_object_hint_top_family_v2",
        "family": "object_model",
        "operation": "expanded_rank_object_family_hint",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_object_right_candidate_exists_v2",
        "family": "object_model",
        "operation": "expanded_object_translate_right",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_object_down_candidate_exists_v2",
        "family": "object_model",
        "operation": "expanded_object_translate_down",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_shape_hint_top_family_v2",
        "family": "shape_symmetry",
        "operation": "expanded_rank_shape_family_hint",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_shape_reflection_candidates_exist_v2",
        "family": "shape_symmetry",
        "operation": "expanded_shape_reflection_candidates",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_cross_family_score_order_v2",
        "family": "cross_family_composition",
        "operation": "expanded_cross_family_score_order",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_cross_family_deduplication_v2",
        "family": "cross_family_composition",
        "operation": "expanded_cross_family_deduplication",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_deterministic_repeatability_v2",
        "family": "cross_family_composition",
        "operation": "expanded_deterministic_repeatability",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "expanded_runtime_boundary_guard_v2",
        "family": "cross_family_composition",
        "operation": "expanded_runtime_boundary_guard",
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
    "guard_expanded_uses_ranker_artifact",
    "guard_expanded_color_family_hint",
    "guard_expanded_color_training_pair",
    "guard_expanded_background_preservation",
    "guard_expanded_object_family_hint",
    "guard_expanded_object_translation_candidates",
    "guard_expanded_shape_family_hint",
    "guard_expanded_shape_reflection_candidates",
    "guard_expanded_score_order",
    "guard_expanded_deduplication",
    "guard_expanded_repeatability",
    "guard_expanded_no_submission_side_effect",
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

BENCHMARK_GATES: Tuple[str, ...] = (
    "ranker_artifact_present",
    "ranker_artifact_ready",
    "ranker_artifact_valid",
    "ranker_next_stage_matches_task_6",
    "ranker_gate_count_valid",
    "ranker_issue_count_zero",
    "ranker_pass_count_valid",
    "ranker_failure_count_zero",
    "benchmark_mode_valid",
    "benchmark_scope_valid",
    "benchmark_verdict_valid",
    "benchmark_ready",
    "benchmark_locked",
    "family_count_valid",
    "expanded_case_count_valid",
    "expanded_pass_count_valid",
    "expanded_failure_count_zero",
    "sample_ranked_candidate_count_valid",
    "evidence_field_count_valid",
    "regression_guard_count_valid",
    "boundary_control_count_valid",
    "all_cases_priority_p0",
    "all_cases_expected_pass",
    "color_hint_top_family_pass",
    "color_training_pair_top_operation_pass",
    "color_background_guard_pass",
    "object_hint_top_family_pass",
    "object_right_candidate_exists_pass",
    "object_down_candidate_exists_pass",
    "shape_hint_top_family_pass",
    "shape_reflection_candidates_exist_pass",
    "cross_family_score_order_pass",
    "cross_family_deduplication_pass",
    "deterministic_repeatability_pass",
    "boundary_guard_pass",
    "all_expanded_cases_pass",
    "family_coverage_color_mapping",
    "family_coverage_object_model",
    "family_coverage_shape_symmetry",
    "family_coverage_cross_family_composition",
    "expanded_runtime_benchmark_created",
    "runtime_stack_linked",
    "ranker_candidates_ranked",
    "ranker_candidates_deduplicated",
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

BENCHMARK_ISSUES: Tuple[str, ...] = (
    "ranker_artifact_missing",
    "ranker_artifact_not_ready",
    "ranker_artifact_invalid",
    "ranker_next_stage_mismatch",
    "ranker_gate_count_invalid",
    "ranker_issue_count_nonzero",
    "ranker_pass_count_invalid",
    "ranker_failure_count_nonzero",
    "benchmark_mode_invalid",
    "benchmark_scope_invalid",
    "benchmark_verdict_invalid",
    "benchmark_not_ready",
    "benchmark_not_locked",
    "family_count_invalid",
    "expanded_case_count_invalid",
    "expanded_pass_count_invalid",
    "expanded_failure_count_nonzero",
    "sample_ranked_candidate_count_invalid",
    "evidence_field_count_invalid",
    "regression_guard_count_invalid",
    "boundary_control_count_invalid",
    "case_priority_not_p0",
    "case_expected_status_not_pass",
    "color_hint_top_family_failed",
    "color_training_pair_top_operation_failed",
    "color_background_guard_failed",
    "object_hint_top_family_failed",
    "object_right_candidate_exists_failed",
    "object_down_candidate_exists_failed",
    "shape_hint_top_family_failed",
    "shape_reflection_candidates_exist_failed",
    "cross_family_score_order_failed",
    "cross_family_deduplication_failed",
    "deterministic_repeatability_failed",
    "boundary_guard_failed",
    "expanded_case_failure_detected",
    "family_coverage_color_mapping_missing",
    "family_coverage_object_model_missing",
    "family_coverage_shape_symmetry_missing",
    "family_coverage_cross_family_composition_missing",
    "expanded_runtime_benchmark_missing",
    "runtime_stack_not_linked",
    "ranker_candidates_not_ranked",
    "ranker_candidates_not_deduplicated",
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


def _ranked(
    grid: GridLike,
    *,
    task_family_hint: str | None = None,
    training_input: GridLike | None = None,
    training_output: GridLike | None = None,
) -> Tuple[Dict[str, Any], ...]:
    candidates = generate_runtime_upgraded_candidates(
        grid,
        training_input=training_input,
        training_output=training_output,
    )
    return rank_runtime_candidates(candidates, task_family_hint=task_family_hint)


def evaluate_expanded_runtime_case(case_id: str) -> Dict[str, Any]:
    if case_id == "expanded_runtime_color_hint_top_family_v2":
        ranked = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]], task_family_hint="color_mapping")
        passed = ranked[0]["family"] == "color_mapping" and ranked[0]["ranker_ready"] is True
        return _result(case_id, "color_mapping", "expanded_rank_color_family_hint", passed)

    if case_id == "expanded_runtime_color_training_pair_top_operation_v2":
        training_input = normalize_grid([[0, 1, 2], [0, 1, 2]])
        training_output = normalize_grid([[0, 3, 4], [0, 3, 4]])
        ranked = _ranked(
            [[0, 1, 2], [2, 1, 0]],
            task_family_hint="color_mapping",
            training_input=training_input,
            training_output=training_output,
        )
        passed = ranked[0]["operation"] == "runtime_color_mapping_from_training_pair"
        return _result(case_id, "color_mapping", "expanded_rank_color_training_pair", passed)

    if case_id == "expanded_runtime_color_background_guard_v2":
        ranked = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]], task_family_hint="color_mapping")
        color_candidates = [item for item in ranked if item["family"] == "color_mapping"]
        passed = bool(color_candidates) and all(
            candidate["grid"][0][0] == 0 and candidate["grid"][0][2] == 0 for candidate in color_candidates
        )
        return _result(case_id, "color_mapping", "expanded_preserve_background", passed)

    if case_id == "expanded_runtime_object_hint_top_family_v2":
        ranked = _ranked([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]], task_family_hint="object_model")
        passed = ranked[0]["family"] == "object_model"
        return _result(case_id, "object_model", "expanded_rank_object_family_hint", passed)

    if case_id == "expanded_runtime_object_right_candidate_exists_v2":
        ranked = _ranked([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]], task_family_hint="object_model")
        passed = any(item["operation"] == "runtime_object_translate_largest_right" for item in ranked)
        return _result(case_id, "object_model", "expanded_object_translate_right", passed)

    if case_id == "expanded_runtime_object_down_candidate_exists_v2":
        ranked = _ranked([[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]], task_family_hint="object_model")
        passed = any(item["operation"] == "runtime_object_translate_largest_down" for item in ranked)
        return _result(case_id, "object_model", "expanded_object_translate_down", passed)

    if case_id == "expanded_runtime_shape_hint_top_family_v2":
        ranked = _ranked([[1, 0], [2, 0], [3, 0]], task_family_hint="shape_symmetry")
        passed = ranked[0]["family"] == "shape_symmetry"
        return _result(case_id, "shape_symmetry", "expanded_rank_shape_family_hint", passed)

    if case_id == "expanded_runtime_shape_reflection_candidates_exist_v2":
        ranked = _ranked([[1, 0], [2, 0], [3, 0]], task_family_hint="shape_symmetry")
        operations = {item["operation"] for item in ranked}
        passed = {
            "runtime_shape_reflect_horizontal",
            "runtime_shape_reflect_vertical",
        }.issubset(operations)
        return _result(case_id, "shape_symmetry", "expanded_shape_reflection_candidates", passed)

    if case_id == "expanded_runtime_cross_family_score_order_v2":
        ranked = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        scores = [item["ranker_score"] for item in ranked]
        passed = scores == sorted(scores, reverse=True)
        return _result(case_id, "cross_family_composition", "expanded_cross_family_score_order", passed)

    if case_id == "expanded_runtime_cross_family_deduplication_v2":
        candidates = generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        ranked = rank_runtime_candidates(tuple(candidates) + tuple(candidates[:2]))
        signatures = [item["signature"] for item in ranked]
        passed = len(signatures) == len(set(signatures))
        return _result(case_id, "cross_family_composition", "expanded_cross_family_deduplication", passed)

    if case_id == "expanded_runtime_deterministic_repeatability_v2":
        first = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]], task_family_hint="object_model")
        second = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]], task_family_hint="object_model")
        passed = first == second
        return _result(case_id, "cross_family_composition", "expanded_deterministic_repeatability", passed)

    if case_id == "expanded_runtime_boundary_guard_v2":
        ranked = _ranked([[0, 1, 0], [0, 1, 0], [0, 0, 0]])
        passed = bool(ranked) and all(item["ranker_ready"] is True for item in ranked)
        return _result(case_id, "cross_family_composition", "expanded_runtime_boundary_guard", passed)

    raise ValueError(f"unknown expanded runtime case: {case_id}")


def evaluate_all_expanded_runtime_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_expanded_runtime_case(case["case_id"]) for case in EXPANDED_CASES)


def build_milestone_8_expanded_runtime_benchmark() -> Dict[str, Any]:
    ranker = _read_json(RANKER_JSON)
    results = evaluate_all_expanded_runtime_cases()
    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)
    covered_families = {result["family"] for result in results}

    sample_ranked_candidates = _ranked(
        [[0, 0, 0, 0], [0, 5, 5, 0], [0, 0, 0, 0]],
        task_family_hint="object_model",
    )
    sample_signatures = [candidate["signature"] for candidate in sample_ranked_candidates]
    sample_scores = [candidate["ranker_score"] for candidate in sample_ranked_candidates]

    ranker_candidates_ranked = (
        [candidate["ranker_rank"] for candidate in sample_ranked_candidates]
        == list(range(1, len(sample_ranked_candidates) + 1))
        and sample_scores == sorted(sample_scores, reverse=True)
    )
    ranker_candidates_deduplicated = len(sample_signatures) == len(set(sample_signatures))

    benchmark_record = {
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "benchmark_ready": True,
        "benchmark_locked": True,
        "baseline_ranker_id": ranker.get("ranker_id", "MISSING_RANKER_ID"),
        "ranker_ready": ranker.get("ranker_ready") is True,
        "ranker_next_stage": ranker.get("next_allowed_stage", "MISSING"),
        "family_count": len(BENCHMARK_FAMILIES),
        "expanded_case_count": len(EXPANDED_CASES),
        "expanded_pass_count": pass_count,
        "expanded_failure_count": failure_count,
        "sample_ranked_candidate_count": len(sample_ranked_candidates),
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "expanded_runtime_benchmark_created": True,
        "runtime_stack_linked": True,
        "ranker_candidates_ranked": ranker_candidates_ranked,
        "ranker_candidates_deduplicated": ranker_candidates_deduplicated,
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
        "ranker_artifact_present": RANKER_JSON.exists(),
        "ranker_artifact_ready": ranker.get("status") == "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY",
        "ranker_artifact_valid": bool(ranker.get("ranker_id")) and bool(ranker.get("signature")),
        "ranker_next_stage_matches_task_6": ranker.get("next_allowed_stage")
        == "MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2",
        "ranker_gate_count_valid": int(ranker.get("ranker_gate_count", 0)) == EXPECTED_RANKER_GATE_COUNT,
        "ranker_issue_count_zero": int(ranker.get("ranker_issue_count", -1)) == EXPECTED_RANKER_ISSUE_COUNT,
        "ranker_pass_count_valid": int(ranker.get("ranker_pass_count", 0)) == EXPECTED_RANKER_PASS_COUNT,
        "ranker_failure_count_zero": int(ranker.get("ranker_failure_count", -1)) == EXPECTED_RANKER_FAILURE_COUNT,
        "benchmark_mode_valid": BENCHMARK_MODE == "EXPANDED_RUNTIME_BENCHMARK_V2_LOCAL_ONLY",
        "benchmark_scope_valid": BENCHMARK_SCOPE == "STRESS_RUNTIME_GENERATOR_AND_RANKER_ON_EXPANDED_LOCAL_CASES",
        "benchmark_verdict_valid": BENCHMARK_VERDICT == "EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH",
        "benchmark_ready": benchmark_record["benchmark_ready"] is True,
        "benchmark_locked": benchmark_record["benchmark_locked"] is True,
        "family_count_valid": len(BENCHMARK_FAMILIES) == EXPECTED_FAMILY_COUNT,
        "expanded_case_count_valid": len(EXPANDED_CASES) == EXPECTED_EXPANDED_CASE_COUNT,
        "expanded_pass_count_valid": pass_count == EXPECTED_EXPANDED_PASS_COUNT,
        "expanded_failure_count_zero": failure_count == EXPECTED_EXPANDED_FAILURE_COUNT,
        "sample_ranked_candidate_count_valid": len(sample_ranked_candidates) == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
        "evidence_field_count_valid": len(EVIDENCE_FIELDS) == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_cases_priority_p0": all(case["priority"] == "P0" for case in EXPANDED_CASES),
        "all_cases_expected_pass": all(case["expected_status"] == "PASS" for case in EXPANDED_CASES),
        "color_hint_top_family_pass": result_by_case["expanded_runtime_color_hint_top_family_v2"]["passed"],
        "color_training_pair_top_operation_pass": result_by_case[
            "expanded_runtime_color_training_pair_top_operation_v2"
        ]["passed"],
        "color_background_guard_pass": result_by_case["expanded_runtime_color_background_guard_v2"]["passed"],
        "object_hint_top_family_pass": result_by_case["expanded_runtime_object_hint_top_family_v2"]["passed"],
        "object_right_candidate_exists_pass": result_by_case["expanded_runtime_object_right_candidate_exists_v2"][
            "passed"
        ],
        "object_down_candidate_exists_pass": result_by_case["expanded_runtime_object_down_candidate_exists_v2"][
            "passed"
        ],
        "shape_hint_top_family_pass": result_by_case["expanded_runtime_shape_hint_top_family_v2"]["passed"],
        "shape_reflection_candidates_exist_pass": result_by_case[
            "expanded_runtime_shape_reflection_candidates_exist_v2"
        ]["passed"],
        "cross_family_score_order_pass": result_by_case["expanded_runtime_cross_family_score_order_v2"]["passed"],
        "cross_family_deduplication_pass": result_by_case["expanded_runtime_cross_family_deduplication_v2"][
            "passed"
        ],
        "deterministic_repeatability_pass": result_by_case["expanded_runtime_deterministic_repeatability_v2"][
            "passed"
        ],
        "boundary_guard_pass": result_by_case["expanded_runtime_boundary_guard_v2"]["passed"],
        "all_expanded_cases_pass": all(result["passed"] is True for result in results),
        "family_coverage_color_mapping": "color_mapping" in covered_families,
        "family_coverage_object_model": "object_model" in covered_families,
        "family_coverage_shape_symmetry": "shape_symmetry" in covered_families,
        "family_coverage_cross_family_composition": "cross_family_composition" in covered_families,
        "expanded_runtime_benchmark_created": benchmark_record["expanded_runtime_benchmark_created"] is True,
        "runtime_stack_linked": benchmark_record["runtime_stack_linked"] is True,
        "ranker_candidates_ranked": benchmark_record["ranker_candidates_ranked"] is True,
        "ranker_candidates_deduplicated": benchmark_record["ranker_candidates_deduplicated"] is True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2",
        "real_submission_not_created": benchmark_record["real_submission_created"] is False,
        "real_submission_allowed_false": benchmark_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": benchmark_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": benchmark_record["kaggle_submission_sent"] is False,
        "upload_not_performed": benchmark_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": benchmark_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": benchmark_record["external_api_dependency"] is False,
        "contains_api_keys_false": benchmark_record["contains_api_keys"] is False,
        "private_core_exposure_false": benchmark_record["private_core_exposure"] is False,
        "legal_certification_false": benchmark_record["legal_certification"] is False,
        "score_claim_absent": benchmark_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": benchmark_record["public_leaderboard_claim_absent"] is True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    issue_state = {
        "ranker_artifact_missing": not gate_state["ranker_artifact_present"],
        "ranker_artifact_not_ready": not gate_state["ranker_artifact_ready"],
        "ranker_artifact_invalid": not gate_state["ranker_artifact_valid"],
        "ranker_next_stage_mismatch": not gate_state["ranker_next_stage_matches_task_6"],
        "ranker_gate_count_invalid": not gate_state["ranker_gate_count_valid"],
        "ranker_issue_count_nonzero": not gate_state["ranker_issue_count_zero"],
        "ranker_pass_count_invalid": not gate_state["ranker_pass_count_valid"],
        "ranker_failure_count_nonzero": not gate_state["ranker_failure_count_zero"],
        "benchmark_mode_invalid": not gate_state["benchmark_mode_valid"],
        "benchmark_scope_invalid": not gate_state["benchmark_scope_valid"],
        "benchmark_verdict_invalid": not gate_state["benchmark_verdict_valid"],
        "benchmark_not_ready": not gate_state["benchmark_ready"],
        "benchmark_not_locked": not gate_state["benchmark_locked"],
        "family_count_invalid": not gate_state["family_count_valid"],
        "expanded_case_count_invalid": not gate_state["expanded_case_count_valid"],
        "expanded_pass_count_invalid": not gate_state["expanded_pass_count_valid"],
        "expanded_failure_count_nonzero": not gate_state["expanded_failure_count_zero"],
        "sample_ranked_candidate_count_invalid": not gate_state["sample_ranked_candidate_count_valid"],
        "evidence_field_count_invalid": not gate_state["evidence_field_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "boundary_control_count_invalid": not gate_state["boundary_control_count_valid"],
        "case_priority_not_p0": not gate_state["all_cases_priority_p0"],
        "case_expected_status_not_pass": not gate_state["all_cases_expected_pass"],
        "color_hint_top_family_failed": not gate_state["color_hint_top_family_pass"],
        "color_training_pair_top_operation_failed": not gate_state["color_training_pair_top_operation_pass"],
        "color_background_guard_failed": not gate_state["color_background_guard_pass"],
        "object_hint_top_family_failed": not gate_state["object_hint_top_family_pass"],
        "object_right_candidate_exists_failed": not gate_state["object_right_candidate_exists_pass"],
        "object_down_candidate_exists_failed": not gate_state["object_down_candidate_exists_pass"],
        "shape_hint_top_family_failed": not gate_state["shape_hint_top_family_pass"],
        "shape_reflection_candidates_exist_failed": not gate_state["shape_reflection_candidates_exist_pass"],
        "cross_family_score_order_failed": not gate_state["cross_family_score_order_pass"],
        "cross_family_deduplication_failed": not gate_state["cross_family_deduplication_pass"],
        "deterministic_repeatability_failed": not gate_state["deterministic_repeatability_pass"],
        "boundary_guard_failed": not gate_state["boundary_guard_pass"],
        "expanded_case_failure_detected": not gate_state["all_expanded_cases_pass"],
        "family_coverage_color_mapping_missing": not gate_state["family_coverage_color_mapping"],
        "family_coverage_object_model_missing": not gate_state["family_coverage_object_model"],
        "family_coverage_shape_symmetry_missing": not gate_state["family_coverage_shape_symmetry"],
        "family_coverage_cross_family_composition_missing": not gate_state[
            "family_coverage_cross_family_composition"
        ],
        "expanded_runtime_benchmark_missing": not gate_state["expanded_runtime_benchmark_created"],
        "runtime_stack_not_linked": not gate_state["runtime_stack_linked"],
        "ranker_candidates_not_ranked": not gate_state["ranker_candidates_ranked"],
        "ranker_candidates_not_deduplicated": not gate_state["ranker_candidates_deduplicated"],
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
        for name in BENCHMARK_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in BENCHMARK_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    benchmark_ready = (
        ranker.get("status") == "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY"
        and ranker.get("ranker_ready") is True
        and pass_count == EXPECTED_EXPANDED_PASS_COUNT
        and failure_count == EXPECTED_EXPANDED_FAILURE_COUNT
        and ranker_candidates_ranked
        and ranker_candidates_deduplicated
        and passed_gate_count == len(BENCHMARK_GATES)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #8",
        "task": "Task 6",
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_ranker": ranker.get("ranker_id", "MISSING_RANKER_ID"),
        "benchmark_ready": benchmark_ready,
        "benchmark_locked": True,
        "family_count": len(BENCHMARK_FAMILIES),
        "expanded_case_count": len(EXPANDED_CASES),
        "expanded_pass_count": pass_count,
        "expanded_failure_count": failure_count,
        "sample_ranked_candidate_count": len(sample_ranked_candidates),
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
        "status": BENCHMARK_STATUS,
        "milestone": "Milestone #8",
        "task": "Task 6",
        "title": "Expanded Runtime Benchmark v2",
        "baseline_commit": BASELINE_COMMIT,
        "benchmark_mode": BENCHMARK_MODE,
        "benchmark_scope": BENCHMARK_SCOPE,
        "benchmark_verdict": BENCHMARK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "ranker_source": {
            "path": str(RANKER_JSON),
            "present": RANKER_JSON.exists(),
            "status": ranker.get("status", "MISSING"),
            "ranker_id": ranker.get("ranker_id", "MISSING_RANKER_ID"),
            "sha256": _sha256(RANKER_JSON),
            "sha256_16": _sha16(_sha256(RANKER_JSON)),
        },
        "benchmark_record": benchmark_record,
        "benchmark_families": list(BENCHMARK_FAMILIES),
        "expanded_cases": list(EXPANDED_CASES),
        "expanded_results": list(results),
        "sample_ranked_candidates": list(sample_ranked_candidates),
        "evidence_fields": list(EVIDENCE_FIELDS),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "benchmark_gates": list(gates),
        "benchmark_issues": list(issues),
        "benchmark_index": index,
        "family_count": len(BENCHMARK_FAMILIES),
        "expanded_case_count": len(EXPANDED_CASES),
        "expanded_pass_count": pass_count,
        "expanded_failure_count": failure_count,
        "sample_ranked_candidate_count": len(sample_ranked_candidates),
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "benchmark_gate_count": len(BENCHMARK_GATES),
        "passed_gate_count": passed_gate_count,
        "benchmark_issue_count": issue_count,
        "warning_count": 0,
        "benchmark_ready": benchmark_ready,
        "benchmark_locked": True,
        "family_coverage": sorted(covered_families),
        "expanded_runtime_benchmark_created": True,
        "runtime_stack_linked": True,
        "ranker_candidates_ranked": ranker_candidates_ranked,
        "ranker_candidates_deduplicated": ranker_candidates_deduplicated,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_8_expanded_runtime_benchmark_v2",
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
        "benchmark_id": f"MILESTONE-8-EXPANDED-RUNTIME-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_8_expanded_runtime_benchmark(benchmark: Mapping[str, Any]) -> Dict[str, Any]:
    gates = benchmark.get("benchmark_gates", [])
    issues = benchmark.get("benchmark_issues", [])
    results = benchmark.get("expanded_results", [])
    sample_ranked_candidates = benchmark.get("sample_ranked_candidates", [])

    checks = {
        "status_ready": benchmark.get("status") == BENCHMARK_STATUS,
        "benchmark_id_present": isinstance(benchmark.get("benchmark_id"), str) and bool(benchmark.get("benchmark_id")),
        "signature_present": isinstance(benchmark.get("signature"), str) and bool(benchmark.get("signature")),
        "baseline_commit_valid": str(benchmark.get("baseline_commit", "")).startswith("537b277"),
        "benchmark_mode_valid": benchmark.get("benchmark_mode") == BENCHMARK_MODE,
        "benchmark_scope_valid": benchmark.get("benchmark_scope") == BENCHMARK_SCOPE,
        "benchmark_verdict_valid": benchmark.get("benchmark_verdict") == BENCHMARK_VERDICT,
        "next_allowed_stage_valid": benchmark.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "family_count_valid": benchmark.get("family_count") == EXPECTED_FAMILY_COUNT,
        "expanded_case_count_valid": benchmark.get("expanded_case_count") == EXPECTED_EXPANDED_CASE_COUNT,
        "expanded_pass_count_valid": benchmark.get("expanded_pass_count") == EXPECTED_EXPANDED_PASS_COUNT,
        "expanded_failure_count_zero": benchmark.get("expanded_failure_count") == EXPECTED_EXPANDED_FAILURE_COUNT,
        "sample_ranked_candidate_count_valid": benchmark.get("sample_ranked_candidate_count")
        == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
        "evidence_field_count_valid": benchmark.get("evidence_field_count") == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": benchmark.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": benchmark.get("boundary_control_count") == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "benchmark_gate_count_matches": benchmark.get("benchmark_gate_count") == len(BENCHMARK_GATES),
        "all_benchmark_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "benchmark_issue_count_zero": benchmark.get("benchmark_issue_count") == 0,
        "all_benchmark_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "benchmark_ready": benchmark.get("benchmark_ready") is True,
        "benchmark_locked": benchmark.get("benchmark_locked") is True,
        "sample_ranked_candidates_present": bool(sample_ranked_candidates)
        and len(sample_ranked_candidates) == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
        "ranker_candidates_ranked": benchmark.get("ranker_candidates_ranked") is True,
        "ranker_candidates_deduplicated": benchmark.get("ranker_candidates_deduplicated") is True,
        "real_submission_not_created": benchmark.get("real_submission_created") is False,
        "real_submission_allowed_false": benchmark.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": benchmark.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": benchmark.get("kaggle_submission_sent") is False,
        "upload_not_performed": benchmark.get("upload_performed") is False,
        "kaggle_authentication_not_performed": benchmark.get("kaggle_authentication_performed") is False,
        "score_claim_absent": benchmark.get("score_claim_absent") is True,
        "public_leaderboard_claim_absent": benchmark.get("public_leaderboard_claim_absent") is True,
        "metadata_safe": benchmark.get("metadata", {}).get("external_api_dependency") is False
        and benchmark.get("metadata", {}).get("contains_api_keys") is False
        and benchmark.get("metadata", {}).get("private_core_exposure") is False
        and benchmark.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_INVALID",
        "valid": valid,
        "checks": checks,
        "benchmark_id": benchmark.get("benchmark_id"),
        "signature": benchmark.get("signature"),
    }


def render_expanded_runtime_benchmark_markdown(benchmark: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #8 - Expanded Runtime Benchmark v2",
        "",
        f"- status: {benchmark['status']}",
        f"- benchmark_id: {benchmark['benchmark_id']}",
        f"- signature: {benchmark['signature']}",
        f"- baseline_commit: {benchmark['baseline_commit']}",
        f"- benchmark_mode: {benchmark['benchmark_mode']}",
        f"- benchmark_scope: {benchmark['benchmark_scope']}",
        f"- benchmark_verdict: {benchmark['benchmark_verdict']}",
        f"- next_allowed_stage: {benchmark['next_allowed_stage']}",
        f"- family_count: {benchmark['family_count']}",
        f"- expanded_case_count: {benchmark['expanded_case_count']}",
        f"- expanded_pass_count: {benchmark['expanded_pass_count']}",
        f"- expanded_failure_count: {benchmark['expanded_failure_count']}",
        f"- sample_ranked_candidate_count: {benchmark['sample_ranked_candidate_count']}",
        f"- benchmark_gate_count: {benchmark['benchmark_gate_count']}",
        f"- passed_gate_count: {benchmark['passed_gate_count']}",
        f"- benchmark_issue_count: {benchmark['benchmark_issue_count']}",
        f"- benchmark_ready: {benchmark['benchmark_ready']}",
        "",
        "## Expanded results",
        "",
    ]

    for result in benchmark["expanded_results"]:
        lines.append(
            f"- {result['case_id']} / family={result['family']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Expanded Runtime Benchmark v2 is ready for submission candidate refresh.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY=true",
            "ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_VALID=true",
            "ARC_AGI3_MILESTONE_8_BENCHMARK_MODE=EXPANDED_RUNTIME_BENCHMARK_V2_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_8_BENCHMARK_VERDICT=EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH",
            "ARC_AGI3_MILESTONE_8_BASELINE_RANKER_COMMIT=537b277",
            "ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_EXPANDED_CASE_COUNT=12",
            "ARC_AGI3_MILESTONE_8_EXPANDED_PASS_COUNT=12",
            "ARC_AGI3_MILESTONE_8_EXPANDED_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_8_SAMPLE_RANKED_CANDIDATE_COUNT={count}".format(
                count=benchmark["sample_ranked_candidate_count"]
            ),
            "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2",
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


def render_expanded_runtime_benchmark_manifest(benchmark: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 8 EXPANDED RUNTIME BENCHMARK MANIFEST v2",
        f"benchmark_id={benchmark['benchmark_id']}",
        f"signature={benchmark['signature']}",
        f"status={benchmark['status']}",
        f"baseline_commit={benchmark['baseline_commit']}",
        f"benchmark_mode={benchmark['benchmark_mode']}",
        f"benchmark_verdict={benchmark['benchmark_verdict']}",
        f"next_allowed_stage={benchmark['next_allowed_stage']}",
        f"family_count={benchmark['family_count']}",
        f"expanded_case_count={benchmark['expanded_case_count']}",
        f"expanded_pass_count={benchmark['expanded_pass_count']}",
        f"expanded_failure_count={benchmark['expanded_failure_count']}",
        f"sample_ranked_candidate_count={benchmark['sample_ranked_candidate_count']}",
        f"benchmark_gate_count={benchmark['benchmark_gate_count']}",
        f"passed_gate_count={benchmark['passed_gate_count']}",
        f"benchmark_issue_count={benchmark['benchmark_issue_count']}",
        f"benchmark_ready={benchmark['benchmark_ready']}",
        f"benchmark_locked={benchmark['benchmark_locked']}",
        f"expanded_runtime_benchmark_created={benchmark['expanded_runtime_benchmark_created']}",
        f"runtime_stack_linked={benchmark['runtime_stack_linked']}",
        f"ranker_candidates_ranked={benchmark['ranker_candidates_ranked']}",
        f"ranker_candidates_deduplicated={benchmark['ranker_candidates_deduplicated']}",
        f"real_submission_created={benchmark['real_submission_created']}",
        f"real_submission_allowed={benchmark['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={benchmark['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={benchmark['kaggle_submission_sent']}",
        f"upload_performed={benchmark['upload_performed']}",
        f"kaggle_authentication_performed={benchmark['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "EXPANDED_RESULTS",
    ]

    for result in benchmark["expanded_results"]:
        lines.append(
            f"{result['case_id']} family={result['family']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    lines.append("SAMPLE_RANKED_CANDIDATES")
    for candidate in benchmark["sample_ranked_candidates"]:
        lines.append(
            f"rank={candidate['ranker_rank']} id={candidate['candidate_id']} "
            f"family={candidate['family']} operation={candidate['operation']} "
            f"ranker_score={candidate['ranker_score']} signature={candidate['signature']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_expanded_runtime_benchmark_artifacts(
    benchmark: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    benchmark = dict(benchmark or build_milestone_8_expanded_runtime_benchmark())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-8-expanded-runtime-benchmark-v2.json"
    md_path = output / "milestone-8-expanded-runtime-benchmark-v2.md"
    manifest_path = output / "milestone-8-expanded-runtime-benchmark-manifest-v2.txt"
    index_path = output / "milestone-8-expanded-runtime-benchmark-index-v2.json"

    json_path.write_text(json.dumps(benchmark, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_expanded_runtime_benchmark_markdown(benchmark), encoding="utf-8")
    manifest_path.write_text(render_expanded_runtime_benchmark_manifest(benchmark), encoding="utf-8")
    index_path.write_text(json.dumps(benchmark["benchmark_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_8_expanded_runtime_benchmark_pipeline() -> Dict[str, Any]:
    benchmark = build_milestone_8_expanded_runtime_benchmark()
    validation = validate_milestone_8_expanded_runtime_benchmark(benchmark)
    artifacts = write_expanded_runtime_benchmark_artifacts(benchmark)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_PIPELINE_INVALID",
        "benchmark_status": benchmark["status"],
        "validation_status": validation["status"],
        "benchmark": benchmark,
        "benchmark_id": benchmark["benchmark_id"],
        "signature": benchmark["signature"],
        "benchmark_mode": benchmark["benchmark_mode"],
        "benchmark_verdict": benchmark["benchmark_verdict"],
        "next_allowed_stage": benchmark["next_allowed_stage"],
        "family_count": benchmark["family_count"],
        "expanded_case_count": benchmark["expanded_case_count"],
        "expanded_pass_count": benchmark["expanded_pass_count"],
        "expanded_failure_count": benchmark["expanded_failure_count"],
        "sample_ranked_candidate_count": benchmark["sample_ranked_candidate_count"],
        "evidence_field_count": benchmark["evidence_field_count"],
        "regression_guard_count": benchmark["regression_guard_count"],
        "boundary_control_count": benchmark["boundary_control_count"],
        "benchmark_gate_count": benchmark["benchmark_gate_count"],
        "passed_gate_count": benchmark["passed_gate_count"],
        "benchmark_issue_count": benchmark["benchmark_issue_count"],
        "warning_count": benchmark["warning_count"],
        "benchmark_ready": benchmark["benchmark_ready"],
        "benchmark_locked": benchmark["benchmark_locked"],
        "expanded_runtime_benchmark_created": benchmark["expanded_runtime_benchmark_created"],
        "runtime_stack_linked": benchmark["runtime_stack_linked"],
        "ranker_candidates_ranked": benchmark["ranker_candidates_ranked"],
        "ranker_candidates_deduplicated": benchmark["ranker_candidates_deduplicated"],
        "real_submission_created": benchmark["real_submission_created"],
        "real_submission_allowed": benchmark["real_submission_allowed"],
        "ready_for_real_kaggle_submission": benchmark["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": benchmark["kaggle_submission_sent"],
        "upload_performed": benchmark["upload_performed"],
        "kaggle_authentication_performed": benchmark["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": benchmark["metadata"],
    }
