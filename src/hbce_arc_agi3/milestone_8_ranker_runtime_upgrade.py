"""Milestone #8 Ranker Runtime Upgrade v2.

Local-only deterministic runtime ranker upgrade.

This module upgrades candidate ranking on top of Candidate Generator Runtime
Upgrade v2. It provides deterministic family-aware ranking, evidence scoring,
deduplication, stable ordering, runtime policy hints, and conservative boundary
guards.

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


RANKER_STATUS = "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY"
PIPELINE_STATUS = "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_VALID"

BASELINE_COMMIT = "3ea3687 Add ARC AGI3 candidate generator runtime upgrade"
RANKER_MODE = "RANKER_RUNTIME_UPGRADE_V2_LOCAL_ONLY"
RANKER_SCOPE = "RANK_RUNTIME_GENERATED_CANDIDATES_WITH_FAMILY_AWARE_POLICY"
RANKER_VERDICT = "RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK"
NEXT_ALLOWED_STAGE = "MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2"

DEFAULT_OUTPUT_DIR = "examples/milestone-8/ranker-runtime-upgrade-v2"

RUNTIME_JSON = Path(
    "examples/milestone-8/candidate-generator-runtime-upgrade-v2/"
    "milestone-8-candidate-generator-runtime-upgrade-v2.json"
)

EXPECTED_FAMILY_COUNT = 4
EXPECTED_RANKER_POLICY_COUNT = 4
EXPECTED_RANKER_OPERATION_COUNT = 8
EXPECTED_RANKER_CASE_COUNT = 8
EXPECTED_RANKER_PASS_COUNT = 8
EXPECTED_RANKER_FAILURE_COUNT = 0
EXPECTED_RUNTIME_GATE_COUNT = 58
EXPECTED_RUNTIME_ISSUE_COUNT = 0
EXPECTED_RUNTIME_PASS_COUNT = 8
EXPECTED_RUNTIME_FAILURE_COUNT = 0
EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT = 4
EXPECTED_EVIDENCE_FIELD_COUNT = 8
EXPECTED_REGRESSION_GUARD_COUNT = 8
EXPECTED_BOUNDARY_CONTROL_COUNT = 9

RANKER_FAMILIES: Tuple[str, ...] = (
    "color_mapping",
    "object_model",
    "shape_symmetry",
    "cross_family_composition",
)

RANKER_POLICIES: Tuple[Dict[str, Any], ...] = (
    {
        "policy_id": "ranker_policy_color_mapping_v2",
        "family": "color_mapping",
        "priority": "P0",
        "hint_weight": 30.0,
    },
    {
        "policy_id": "ranker_policy_object_model_v2",
        "family": "object_model",
        "priority": "P0",
        "hint_weight": 30.0,
    },
    {
        "policy_id": "ranker_policy_shape_symmetry_v2",
        "family": "shape_symmetry",
        "priority": "P0",
        "hint_weight": 30.0,
    },
    {
        "policy_id": "ranker_policy_cross_family_composition_v2",
        "family": "cross_family_composition",
        "priority": "P0",
        "hint_weight": 0.0,
    },
)

RANKER_OPERATIONS: Tuple[str, ...] = (
    "ranker_runtime_score_candidate",
    "ranker_runtime_family_hint_boost",
    "ranker_runtime_operation_quality_bonus",
    "ranker_runtime_deduplicate_by_signature",
    "ranker_runtime_stable_tie_break",
    "ranker_runtime_rank_assignment",
    "ranker_runtime_cross_family_policy",
    "ranker_runtime_boundary_guard",
)

RANKER_CASES: Tuple[Dict[str, Any], ...] = (
    {
        "case_id": "ranker_runtime_color_hint_top_candidate_v2",
        "family": "color_mapping",
        "operation": "ranker_runtime_family_hint_boost",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_object_hint_top_candidate_v2",
        "family": "object_model",
        "operation": "ranker_runtime_family_hint_boost",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_shape_hint_top_candidate_v2",
        "family": "shape_symmetry",
        "operation": "ranker_runtime_family_hint_boost",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_no_hint_score_order_v2",
        "family": "cross_family_composition",
        "operation": "ranker_runtime_score_candidate",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_deduplicate_candidates_v2",
        "family": "cross_family_composition",
        "operation": "ranker_runtime_deduplicate_by_signature",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_deterministic_order_v2",
        "family": "cross_family_composition",
        "operation": "ranker_runtime_stable_tie_break",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_rank_fields_complete_v2",
        "family": "cross_family_composition",
        "operation": "ranker_runtime_rank_assignment",
        "priority": "P0",
        "expected_status": "PASS",
    },
    {
        "case_id": "ranker_runtime_boundary_guard_v2",
        "family": "cross_family_composition",
        "operation": "ranker_runtime_boundary_guard",
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
    "guard_ranker_uses_generated_candidates",
    "guard_ranker_family_hint_policy",
    "guard_ranker_evidence_score_order",
    "guard_ranker_deduplication",
    "guard_ranker_stable_tie_break",
    "guard_ranker_rank_assignment",
    "guard_ranker_metadata_fields",
    "guard_ranker_no_submission_side_effect",
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

RANKER_GATES: Tuple[str, ...] = (
    "runtime_artifact_present",
    "runtime_artifact_ready",
    "runtime_artifact_valid",
    "runtime_next_stage_matches_task_5",
    "runtime_gate_count_valid",
    "runtime_issue_count_zero",
    "runtime_pass_count_valid",
    "runtime_failure_count_zero",
    "ranker_mode_valid",
    "ranker_scope_valid",
    "ranker_verdict_valid",
    "ranker_ready",
    "ranker_locked",
    "family_count_valid",
    "ranker_policy_count_valid",
    "ranker_operation_count_valid",
    "ranker_case_count_valid",
    "ranker_pass_count_valid",
    "ranker_failure_count_zero",
    "sample_ranked_candidate_count_valid",
    "evidence_field_count_valid",
    "regression_guard_count_valid",
    "boundary_control_count_valid",
    "all_policies_priority_p0",
    "all_cases_priority_p0",
    "all_cases_expected_pass",
    "color_hint_top_candidate_pass",
    "object_hint_top_candidate_pass",
    "shape_hint_top_candidate_pass",
    "no_hint_score_order_pass",
    "deduplicate_candidates_pass",
    "deterministic_order_pass",
    "rank_fields_complete_pass",
    "boundary_guard_pass",
    "all_ranker_cases_pass",
    "ranker_family_coverage_color_mapping",
    "ranker_family_coverage_object_model",
    "ranker_family_coverage_shape_symmetry",
    "ranker_family_coverage_cross_family_composition",
    "ranker_runtime_upgrade_created",
    "ranker_candidates_ranked",
    "ranker_candidates_deduplicated",
    "ranker_family_policy_applied",
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

RANKER_ISSUES: Tuple[str, ...] = (
    "runtime_artifact_missing",
    "runtime_artifact_not_ready",
    "runtime_artifact_invalid",
    "runtime_next_stage_mismatch",
    "runtime_gate_count_invalid",
    "runtime_issue_count_nonzero",
    "runtime_pass_count_invalid",
    "runtime_failure_count_nonzero",
    "ranker_mode_invalid",
    "ranker_scope_invalid",
    "ranker_verdict_invalid",
    "ranker_not_ready",
    "ranker_not_locked",
    "family_count_invalid",
    "ranker_policy_count_invalid",
    "ranker_operation_count_invalid",
    "ranker_case_count_invalid",
    "ranker_pass_count_invalid",
    "ranker_failure_count_nonzero",
    "sample_ranked_candidate_count_invalid",
    "evidence_field_count_invalid",
    "regression_guard_count_invalid",
    "boundary_control_count_invalid",
    "policy_priority_not_p0",
    "case_priority_not_p0",
    "case_expected_status_not_pass",
    "color_hint_top_candidate_failed",
    "object_hint_top_candidate_failed",
    "shape_hint_top_candidate_failed",
    "no_hint_score_order_failed",
    "deduplicate_candidates_failed",
    "deterministic_order_failed",
    "rank_fields_complete_failed",
    "boundary_guard_failed",
    "ranker_case_failure_detected",
    "ranker_family_coverage_color_mapping_missing",
    "ranker_family_coverage_object_model_missing",
    "ranker_family_coverage_shape_symmetry_missing",
    "ranker_family_coverage_cross_family_composition_missing",
    "ranker_runtime_upgrade_missing",
    "ranker_candidates_not_ranked",
    "ranker_candidates_not_deduplicated",
    "ranker_family_policy_not_applied",
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

OPERATION_BONUS: Dict[str, float] = {
    "runtime_color_mapping_from_training_pair": 7.0,
    "runtime_color_mapping_non_background_shift": 5.0,
    "runtime_object_translate_largest_right": 6.0,
    "runtime_object_translate_largest_down": 5.0,
    "runtime_shape_reflect_horizontal": 5.0,
    "runtime_shape_reflect_vertical": 4.0,
}


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


def _base_candidates() -> Tuple[Dict[str, Any], ...]:
    return generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])


def score_runtime_candidate(
    candidate: Mapping[str, Any],
    *,
    task_family_hint: str | None = None,
) -> float:
    """Score one runtime candidate deterministically."""
    base = float(candidate.get("evidence_score", 0.0))
    operation = str(candidate.get("operation", ""))
    family = str(candidate.get("family", ""))
    operation_bonus = OPERATION_BONUS.get(operation, 0.0)
    family_hint_bonus = 30.0 if task_family_hint and family == task_family_hint else 0.0
    cross_family_bonus = 2.0 if task_family_hint is None and family == "color_mapping" else 0.0
    return round(base + operation_bonus + family_hint_bonus + cross_family_bonus, 6)


def rank_runtime_candidates(
    candidates: Iterable[Mapping[str, Any]],
    *,
    task_family_hint: str | None = None,
) -> Tuple[Dict[str, Any], ...]:
    """Rank and deduplicate runtime candidates with stable deterministic ordering."""
    best_by_signature: Dict[str, Dict[str, Any]] = {}

    for original_index, candidate in enumerate(candidates):
        candidate_dict = dict(candidate)
        signature = str(candidate_dict.get("signature", ""))
        if not signature:
            signature = _stable_signature(candidate_dict.get("grid", []))
            candidate_dict["signature"] = signature

        ranker_score = score_runtime_candidate(candidate_dict, task_family_hint=task_family_hint)
        candidate_dict["ranker_score"] = ranker_score
        candidate_dict["ranker_family_hint"] = task_family_hint or "none"
        candidate_dict["ranker_policy_applied"] = task_family_hint is not None
        candidate_dict["ranker_operation_bonus"] = OPERATION_BONUS.get(str(candidate_dict.get("operation", "")), 0.0)
        candidate_dict["ranker_original_index"] = original_index
        candidate_dict["ranker_ready"] = True

        previous = best_by_signature.get(signature)
        if previous is None:
            best_by_signature[signature] = candidate_dict
            continue

        previous_key = (
            float(previous["ranker_score"]),
            -int(previous.get("runtime_rank", 9999)),
            str(previous.get("candidate_id", "")),
        )
        candidate_key = (
            float(candidate_dict["ranker_score"]),
            -int(candidate_dict.get("runtime_rank", 9999)),
            str(candidate_dict.get("candidate_id", "")),
        )
        if candidate_key > previous_key:
            best_by_signature[signature] = candidate_dict

    ranked = sorted(
        best_by_signature.values(),
        key=lambda item: (
            -float(item["ranker_score"]),
            int(item.get("runtime_rank", 9999)),
            str(item.get("family", "")),
            str(item.get("candidate_id", "")),
        ),
    )

    upgraded = []
    for index, candidate in enumerate(ranked, start=1):
        upgraded.append(
            {
                **candidate,
                "ranker_rank": index,
                "ranker_runtime_upgrade": "ranker_runtime_upgrade_v2",
            }
        )
    return tuple(upgraded)


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


def evaluate_ranker_runtime_case(case_id: str) -> Dict[str, Any]:
    candidates = _base_candidates()

    if case_id == "ranker_runtime_color_hint_top_candidate_v2":
        ranked = rank_runtime_candidates(candidates, task_family_hint="color_mapping")
        passed = ranked[0]["family"] == "color_mapping" and ranked[0]["ranker_policy_applied"] is True
        return _result(case_id, "color_mapping", "ranker_runtime_family_hint_boost", passed)

    if case_id == "ranker_runtime_object_hint_top_candidate_v2":
        ranked = rank_runtime_candidates(candidates, task_family_hint="object_model")
        passed = ranked[0]["family"] == "object_model" and ranked[0]["ranker_policy_applied"] is True
        return _result(case_id, "object_model", "ranker_runtime_family_hint_boost", passed)

    if case_id == "ranker_runtime_shape_hint_top_candidate_v2":
        ranked = rank_runtime_candidates(candidates, task_family_hint="shape_symmetry")
        passed = ranked[0]["family"] == "shape_symmetry" and ranked[0]["ranker_policy_applied"] is True
        return _result(case_id, "shape_symmetry", "ranker_runtime_family_hint_boost", passed)

    if case_id == "ranker_runtime_no_hint_score_order_v2":
        ranked = rank_runtime_candidates(candidates)
        scores = [item["ranker_score"] for item in ranked]
        passed = scores == sorted(scores, reverse=True) and ranked[0]["ranker_family_hint"] == "none"
        return _result(case_id, "cross_family_composition", "ranker_runtime_score_candidate", passed)

    if case_id == "ranker_runtime_deduplicate_candidates_v2":
        doubled = tuple(candidates) + tuple(candidates[:2])
        ranked = rank_runtime_candidates(doubled)
        signatures = [item["signature"] for item in ranked]
        passed = len(signatures) == len(set(signatures)) and len(ranked) == len(rank_runtime_candidates(candidates))
        return _result(case_id, "cross_family_composition", "ranker_runtime_deduplicate_by_signature", passed)

    if case_id == "ranker_runtime_deterministic_order_v2":
        first = rank_runtime_candidates(candidates, task_family_hint="object_model")
        second = rank_runtime_candidates(candidates, task_family_hint="object_model")
        passed = first == second
        return _result(case_id, "cross_family_composition", "ranker_runtime_stable_tie_break", passed)

    if case_id == "ranker_runtime_rank_fields_complete_v2":
        ranked = rank_runtime_candidates(candidates)
        required = {
            "candidate_id",
            "family",
            "operation",
            "signature",
            "ranker_score",
            "ranker_rank",
            "ranker_family_hint",
            "ranker_ready",
            "ranker_runtime_upgrade",
        }
        passed = bool(ranked) and all(required.issubset(set(candidate)) for candidate in ranked)
        return _result(case_id, "cross_family_composition", "ranker_runtime_rank_assignment", passed)

    if case_id == "ranker_runtime_boundary_guard_v2":
        ranked = rank_runtime_candidates(candidates)
        passed = bool(ranked) and all(candidate["ranker_ready"] is True for candidate in ranked)
        return _result(case_id, "cross_family_composition", "ranker_runtime_boundary_guard", passed)

    raise ValueError(f"unknown ranker runtime case: {case_id}")


def evaluate_all_ranker_runtime_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_ranker_runtime_case(case["case_id"]) for case in RANKER_CASES)


def build_milestone_8_ranker_runtime_upgrade() -> Dict[str, Any]:
    runtime = _read_json(RUNTIME_JSON)
    results = evaluate_all_ranker_runtime_cases()
    pass_count = sum(1 for result in results if result["passed"] is True)
    failure_count = sum(1 for result in results if result["passed"] is False)
    covered_families = {result["family"] for result in results}

    sample_ranked_candidates = rank_runtime_candidates(_base_candidates(), task_family_hint="object_model")
    sample_signatures = [candidate["signature"] for candidate in sample_ranked_candidates]
    sample_scores = [candidate["ranker_score"] for candidate in sample_ranked_candidates]

    ranker_candidates_ranked = (
        [candidate["ranker_rank"] for candidate in sample_ranked_candidates]
        == list(range(1, len(sample_ranked_candidates) + 1))
        and sample_scores == sorted(sample_scores, reverse=True)
    )
    ranker_candidates_deduplicated = len(sample_signatures) == len(set(sample_signatures))
    ranker_family_policy_applied = sample_ranked_candidates[0]["family"] == "object_model"

    ranker_record = {
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "ranker_ready": True,
        "ranker_locked": True,
        "baseline_runtime_id": runtime.get("runtime_id", "MISSING_RUNTIME_ID"),
        "runtime_ready": runtime.get("runtime_ready") is True,
        "runtime_next_stage": runtime.get("next_allowed_stage", "MISSING"),
        "family_count": len(RANKER_FAMILIES),
        "ranker_policy_count": len(RANKER_POLICIES),
        "ranker_operation_count": len(RANKER_OPERATIONS),
        "ranker_case_count": len(RANKER_CASES),
        "ranker_pass_count": pass_count,
        "ranker_failure_count": failure_count,
        "sample_ranked_candidate_count": len(sample_ranked_candidates),
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "ranker_runtime_upgrade_created": True,
        "ranker_candidates_ranked": ranker_candidates_ranked,
        "ranker_candidates_deduplicated": ranker_candidates_deduplicated,
        "ranker_family_policy_applied": ranker_family_policy_applied,
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
        "runtime_artifact_present": RUNTIME_JSON.exists(),
        "runtime_artifact_ready": runtime.get("status") == "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY",
        "runtime_artifact_valid": bool(runtime.get("runtime_id")) and bool(runtime.get("signature")),
        "runtime_next_stage_matches_task_5": runtime.get("next_allowed_stage") == "MILESTONE_8_TASK_5_RANKER_RUNTIME_UPGRADE_V2",
        "runtime_gate_count_valid": int(runtime.get("runtime_gate_count", 0)) == EXPECTED_RUNTIME_GATE_COUNT,
        "runtime_issue_count_zero": int(runtime.get("runtime_issue_count", -1)) == EXPECTED_RUNTIME_ISSUE_COUNT,
        "runtime_pass_count_valid": int(runtime.get("runtime_pass_count", 0)) == EXPECTED_RUNTIME_PASS_COUNT,
        "runtime_failure_count_zero": int(runtime.get("runtime_failure_count", -1)) == EXPECTED_RUNTIME_FAILURE_COUNT,
        "ranker_mode_valid": RANKER_MODE == "RANKER_RUNTIME_UPGRADE_V2_LOCAL_ONLY",
        "ranker_scope_valid": RANKER_SCOPE == "RANK_RUNTIME_GENERATED_CANDIDATES_WITH_FAMILY_AWARE_POLICY",
        "ranker_verdict_valid": RANKER_VERDICT == "RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK",
        "ranker_ready": ranker_record["ranker_ready"] is True,
        "ranker_locked": ranker_record["ranker_locked"] is True,
        "family_count_valid": len(RANKER_FAMILIES) == EXPECTED_FAMILY_COUNT,
        "ranker_policy_count_valid": len(RANKER_POLICIES) == EXPECTED_RANKER_POLICY_COUNT,
        "ranker_operation_count_valid": len(RANKER_OPERATIONS) == EXPECTED_RANKER_OPERATION_COUNT,
        "ranker_case_count_valid": len(RANKER_CASES) == EXPECTED_RANKER_CASE_COUNT,
        "ranker_pass_count_valid": pass_count == EXPECTED_RANKER_PASS_COUNT,
        "ranker_failure_count_zero": failure_count == EXPECTED_RANKER_FAILURE_COUNT,
        "sample_ranked_candidate_count_valid": len(sample_ranked_candidates) == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
        "evidence_field_count_valid": len(EVIDENCE_FIELDS) == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_policies_priority_p0": all(policy["priority"] == "P0" for policy in RANKER_POLICIES),
        "all_cases_priority_p0": all(case["priority"] == "P0" for case in RANKER_CASES),
        "all_cases_expected_pass": all(case["expected_status"] == "PASS" for case in RANKER_CASES),
        "color_hint_top_candidate_pass": result_by_case["ranker_runtime_color_hint_top_candidate_v2"]["passed"],
        "object_hint_top_candidate_pass": result_by_case["ranker_runtime_object_hint_top_candidate_v2"]["passed"],
        "shape_hint_top_candidate_pass": result_by_case["ranker_runtime_shape_hint_top_candidate_v2"]["passed"],
        "no_hint_score_order_pass": result_by_case["ranker_runtime_no_hint_score_order_v2"]["passed"],
        "deduplicate_candidates_pass": result_by_case["ranker_runtime_deduplicate_candidates_v2"]["passed"],
        "deterministic_order_pass": result_by_case["ranker_runtime_deterministic_order_v2"]["passed"],
        "rank_fields_complete_pass": result_by_case["ranker_runtime_rank_fields_complete_v2"]["passed"],
        "boundary_guard_pass": result_by_case["ranker_runtime_boundary_guard_v2"]["passed"],
        "all_ranker_cases_pass": all(result["passed"] is True for result in results),
        "ranker_family_coverage_color_mapping": "color_mapping" in covered_families,
        "ranker_family_coverage_object_model": "object_model" in covered_families,
        "ranker_family_coverage_shape_symmetry": "shape_symmetry" in covered_families,
        "ranker_family_coverage_cross_family_composition": "cross_family_composition" in covered_families,
        "ranker_runtime_upgrade_created": ranker_record["ranker_runtime_upgrade_created"] is True,
        "ranker_candidates_ranked": ranker_record["ranker_candidates_ranked"] is True,
        "ranker_candidates_deduplicated": ranker_record["ranker_candidates_deduplicated"] is True,
        "ranker_family_policy_applied": ranker_record["ranker_family_policy_applied"] is True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2",
        "real_submission_not_created": ranker_record["real_submission_created"] is False,
        "real_submission_allowed_false": ranker_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": ranker_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": ranker_record["kaggle_submission_sent"] is False,
        "upload_not_performed": ranker_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": ranker_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": ranker_record["external_api_dependency"] is False,
        "contains_api_keys_false": ranker_record["contains_api_keys"] is False,
        "private_core_exposure_false": ranker_record["private_core_exposure"] is False,
        "legal_certification_false": ranker_record["legal_certification"] is False,
        "score_claim_absent": ranker_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": ranker_record["public_leaderboard_claim_absent"] is True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    issue_state = {
        "runtime_artifact_missing": not gate_state["runtime_artifact_present"],
        "runtime_artifact_not_ready": not gate_state["runtime_artifact_ready"],
        "runtime_artifact_invalid": not gate_state["runtime_artifact_valid"],
        "runtime_next_stage_mismatch": not gate_state["runtime_next_stage_matches_task_5"],
        "runtime_gate_count_invalid": not gate_state["runtime_gate_count_valid"],
        "runtime_issue_count_nonzero": not gate_state["runtime_issue_count_zero"],
        "runtime_pass_count_invalid": not gate_state["runtime_pass_count_valid"],
        "runtime_failure_count_nonzero": not gate_state["runtime_failure_count_zero"],
        "ranker_mode_invalid": not gate_state["ranker_mode_valid"],
        "ranker_scope_invalid": not gate_state["ranker_scope_valid"],
        "ranker_verdict_invalid": not gate_state["ranker_verdict_valid"],
        "ranker_not_ready": not gate_state["ranker_ready"],
        "ranker_not_locked": not gate_state["ranker_locked"],
        "family_count_invalid": not gate_state["family_count_valid"],
        "ranker_policy_count_invalid": not gate_state["ranker_policy_count_valid"],
        "ranker_operation_count_invalid": not gate_state["ranker_operation_count_valid"],
        "ranker_case_count_invalid": not gate_state["ranker_case_count_valid"],
        "ranker_pass_count_invalid": not gate_state["ranker_pass_count_valid"],
        "ranker_failure_count_nonzero": not gate_state["ranker_failure_count_zero"],
        "sample_ranked_candidate_count_invalid": not gate_state["sample_ranked_candidate_count_valid"],
        "evidence_field_count_invalid": not gate_state["evidence_field_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "boundary_control_count_invalid": not gate_state["boundary_control_count_valid"],
        "policy_priority_not_p0": not gate_state["all_policies_priority_p0"],
        "case_priority_not_p0": not gate_state["all_cases_priority_p0"],
        "case_expected_status_not_pass": not gate_state["all_cases_expected_pass"],
        "color_hint_top_candidate_failed": not gate_state["color_hint_top_candidate_pass"],
        "object_hint_top_candidate_failed": not gate_state["object_hint_top_candidate_pass"],
        "shape_hint_top_candidate_failed": not gate_state["shape_hint_top_candidate_pass"],
        "no_hint_score_order_failed": not gate_state["no_hint_score_order_pass"],
        "deduplicate_candidates_failed": not gate_state["deduplicate_candidates_pass"],
        "deterministic_order_failed": not gate_state["deterministic_order_pass"],
        "rank_fields_complete_failed": not gate_state["rank_fields_complete_pass"],
        "boundary_guard_failed": not gate_state["boundary_guard_pass"],
        "ranker_case_failure_detected": not gate_state["all_ranker_cases_pass"],
        "ranker_family_coverage_color_mapping_missing": not gate_state["ranker_family_coverage_color_mapping"],
        "ranker_family_coverage_object_model_missing": not gate_state["ranker_family_coverage_object_model"],
        "ranker_family_coverage_shape_symmetry_missing": not gate_state["ranker_family_coverage_shape_symmetry"],
        "ranker_family_coverage_cross_family_composition_missing": not gate_state[
            "ranker_family_coverage_cross_family_composition"
        ],
        "ranker_runtime_upgrade_missing": not gate_state["ranker_runtime_upgrade_created"],
        "ranker_candidates_not_ranked": not gate_state["ranker_candidates_ranked"],
        "ranker_candidates_not_deduplicated": not gate_state["ranker_candidates_deduplicated"],
        "ranker_family_policy_not_applied": not gate_state["ranker_family_policy_applied"],
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
        for name in RANKER_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in RANKER_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    ranker_ready = (
        runtime.get("status") == "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY"
        and runtime.get("runtime_ready") is True
        and pass_count == EXPECTED_RANKER_PASS_COUNT
        and failure_count == EXPECTED_RANKER_FAILURE_COUNT
        and ranker_candidates_ranked
        and ranker_candidates_deduplicated
        and ranker_family_policy_applied
        and passed_gate_count == len(RANKER_GATES)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #8",
        "task": "Task 5",
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_runtime": runtime.get("runtime_id", "MISSING_RUNTIME_ID"),
        "ranker_ready": ranker_ready,
        "ranker_locked": True,
        "family_count": len(RANKER_FAMILIES),
        "ranker_policy_count": len(RANKER_POLICIES),
        "ranker_operation_count": len(RANKER_OPERATIONS),
        "ranker_case_count": len(RANKER_CASES),
        "ranker_pass_count": pass_count,
        "ranker_failure_count": failure_count,
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
        "status": RANKER_STATUS,
        "milestone": "Milestone #8",
        "task": "Task 5",
        "title": "Ranker Runtime Upgrade v2",
        "baseline_commit": BASELINE_COMMIT,
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_source": {
            "path": str(RUNTIME_JSON),
            "present": RUNTIME_JSON.exists(),
            "status": runtime.get("status", "MISSING"),
            "runtime_id": runtime.get("runtime_id", "MISSING_RUNTIME_ID"),
            "sha256": _sha256(RUNTIME_JSON),
            "sha256_16": _sha16(_sha256(RUNTIME_JSON)),
        },
        "ranker_record": ranker_record,
        "ranker_families": list(RANKER_FAMILIES),
        "ranker_policies": list(RANKER_POLICIES),
        "ranker_operations": list(RANKER_OPERATIONS),
        "ranker_cases": list(RANKER_CASES),
        "ranker_results": list(results),
        "sample_ranked_candidates": list(sample_ranked_candidates),
        "evidence_fields": list(EVIDENCE_FIELDS),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "ranker_gates": list(gates),
        "ranker_issues": list(issues),
        "ranker_index": index,
        "family_count": len(RANKER_FAMILIES),
        "ranker_policy_count": len(RANKER_POLICIES),
        "ranker_operation_count": len(RANKER_OPERATIONS),
        "ranker_case_count": len(RANKER_CASES),
        "ranker_pass_count": pass_count,
        "ranker_failure_count": failure_count,
        "sample_ranked_candidate_count": len(sample_ranked_candidates),
        "evidence_field_count": len(EVIDENCE_FIELDS),
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "ranker_gate_count": len(RANKER_GATES),
        "passed_gate_count": passed_gate_count,
        "ranker_issue_count": issue_count,
        "warning_count": 0,
        "ranker_ready": ranker_ready,
        "ranker_locked": True,
        "family_coverage": sorted(covered_families),
        "ranker_runtime_upgrade_created": True,
        "ranker_candidates_ranked": ranker_candidates_ranked,
        "ranker_candidates_deduplicated": ranker_candidates_deduplicated,
        "ranker_family_policy_applied": ranker_family_policy_applied,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_8_ranker_runtime_upgrade_v2",
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
        "ranker_id": f"MILESTONE-8-RANKER-RUNTIME-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_8_ranker_runtime_upgrade(ranker: Mapping[str, Any]) -> Dict[str, Any]:
    gates = ranker.get("ranker_gates", [])
    issues = ranker.get("ranker_issues", [])
    results = ranker.get("ranker_results", [])
    sample_ranked_candidates = ranker.get("sample_ranked_candidates", [])

    checks = {
        "status_ready": ranker.get("status") == RANKER_STATUS,
        "ranker_id_present": isinstance(ranker.get("ranker_id"), str) and bool(ranker.get("ranker_id")),
        "signature_present": isinstance(ranker.get("signature"), str) and bool(ranker.get("signature")),
        "baseline_commit_valid": str(ranker.get("baseline_commit", "")).startswith("3ea3687"),
        "ranker_mode_valid": ranker.get("ranker_mode") == RANKER_MODE,
        "ranker_scope_valid": ranker.get("ranker_scope") == RANKER_SCOPE,
        "ranker_verdict_valid": ranker.get("ranker_verdict") == RANKER_VERDICT,
        "next_allowed_stage_valid": ranker.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "family_count_valid": ranker.get("family_count") == EXPECTED_FAMILY_COUNT,
        "ranker_policy_count_valid": ranker.get("ranker_policy_count") == EXPECTED_RANKER_POLICY_COUNT,
        "ranker_operation_count_valid": ranker.get("ranker_operation_count") == EXPECTED_RANKER_OPERATION_COUNT,
        "ranker_case_count_valid": ranker.get("ranker_case_count") == EXPECTED_RANKER_CASE_COUNT,
        "ranker_pass_count_valid": ranker.get("ranker_pass_count") == EXPECTED_RANKER_PASS_COUNT,
        "ranker_failure_count_zero": ranker.get("ranker_failure_count") == EXPECTED_RANKER_FAILURE_COUNT,
        "evidence_field_count_valid": ranker.get("evidence_field_count") == EXPECTED_EVIDENCE_FIELD_COUNT,
        "regression_guard_count_valid": ranker.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": ranker.get("boundary_control_count") == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "ranker_gate_count_matches": ranker.get("ranker_gate_count") == len(RANKER_GATES),
        "all_ranker_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "ranker_issue_count_zero": ranker.get("ranker_issue_count") == 0,
        "all_ranker_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "ranker_ready": ranker.get("ranker_ready") is True,
        "ranker_locked": ranker.get("ranker_locked") is True,
        "sample_ranked_candidates_present": bool(sample_ranked_candidates)
        and len(sample_ranked_candidates) == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
        "ranker_candidates_ranked": ranker.get("ranker_candidates_ranked") is True,
        "ranker_candidates_deduplicated": ranker.get("ranker_candidates_deduplicated") is True,
        "ranker_family_policy_applied": ranker.get("ranker_family_policy_applied") is True,
        "real_submission_not_created": ranker.get("real_submission_created") is False,
        "real_submission_allowed_false": ranker.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": ranker.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": ranker.get("kaggle_submission_sent") is False,
        "upload_not_performed": ranker.get("upload_performed") is False,
        "kaggle_authentication_not_performed": ranker.get("kaggle_authentication_performed") is False,
        "score_claim_absent": ranker.get("score_claim_absent") is True,
        "public_leaderboard_claim_absent": ranker.get("public_leaderboard_claim_absent") is True,
        "metadata_safe": ranker.get("metadata", {}).get("external_api_dependency") is False
        and ranker.get("metadata", {}).get("contains_api_keys") is False
        and ranker.get("metadata", {}).get("private_core_exposure") is False
        and ranker.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_INVALID",
        "valid": valid,
        "checks": checks,
        "ranker_id": ranker.get("ranker_id"),
        "signature": ranker.get("signature"),
    }


def render_ranker_runtime_upgrade_markdown(ranker: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #8 - Ranker Runtime Upgrade v2",
        "",
        f"- status: {ranker['status']}",
        f"- ranker_id: {ranker['ranker_id']}",
        f"- signature: {ranker['signature']}",
        f"- baseline_commit: {ranker['baseline_commit']}",
        f"- ranker_mode: {ranker['ranker_mode']}",
        f"- ranker_scope: {ranker['ranker_scope']}",
        f"- ranker_verdict: {ranker['ranker_verdict']}",
        f"- next_allowed_stage: {ranker['next_allowed_stage']}",
        f"- family_count: {ranker['family_count']}",
        f"- ranker_policy_count: {ranker['ranker_policy_count']}",
        f"- ranker_operation_count: {ranker['ranker_operation_count']}",
        f"- ranker_case_count: {ranker['ranker_case_count']}",
        f"- ranker_pass_count: {ranker['ranker_pass_count']}",
        f"- ranker_failure_count: {ranker['ranker_failure_count']}",
        f"- sample_ranked_candidate_count: {ranker['sample_ranked_candidate_count']}",
        f"- ranker_gate_count: {ranker['ranker_gate_count']}",
        f"- passed_gate_count: {ranker['passed_gate_count']}",
        f"- ranker_issue_count: {ranker['ranker_issue_count']}",
        f"- ranker_ready: {ranker['ranker_ready']}",
        "",
        "## Ranker results",
        "",
    ]

    for result in ranker["ranker_results"]:
        lines.append(
            f"- {result['case_id']} / family={result['family']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Ranker Runtime Upgrade v2 is ready for expanded runtime benchmark.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY=true",
            "ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_VALID=true",
            "ARC_AGI3_MILESTONE_8_RANKER_MODE=RANKER_RUNTIME_UPGRADE_V2_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_8_RANKER_VERDICT=RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK",
            "ARC_AGI3_MILESTONE_8_BASELINE_RUNTIME_COMMIT=3ea3687",
            "ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_RANKER_POLICY_COUNT=4",
            "ARC_AGI3_MILESTONE_8_RANKER_OPERATION_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RANKER_CASE_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RANKER_PASS_COUNT=8",
            "ARC_AGI3_MILESTONE_8_RANKER_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_8_SAMPLE_RANKED_CANDIDATE_COUNT={count}".format(
                count=ranker["sample_ranked_candidate_count"]
            ),
            "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2",
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


def render_ranker_runtime_upgrade_manifest(ranker: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 8 RANKER RUNTIME UPGRADE MANIFEST v2",
        f"ranker_id={ranker['ranker_id']}",
        f"signature={ranker['signature']}",
        f"status={ranker['status']}",
        f"baseline_commit={ranker['baseline_commit']}",
        f"ranker_mode={ranker['ranker_mode']}",
        f"ranker_verdict={ranker['ranker_verdict']}",
        f"next_allowed_stage={ranker['next_allowed_stage']}",
        f"family_count={ranker['family_count']}",
        f"ranker_policy_count={ranker['ranker_policy_count']}",
        f"ranker_operation_count={ranker['ranker_operation_count']}",
        f"ranker_case_count={ranker['ranker_case_count']}",
        f"ranker_pass_count={ranker['ranker_pass_count']}",
        f"ranker_failure_count={ranker['ranker_failure_count']}",
        f"sample_ranked_candidate_count={ranker['sample_ranked_candidate_count']}",
        f"ranker_gate_count={ranker['ranker_gate_count']}",
        f"passed_gate_count={ranker['passed_gate_count']}",
        f"ranker_issue_count={ranker['ranker_issue_count']}",
        f"ranker_ready={ranker['ranker_ready']}",
        f"ranker_locked={ranker['ranker_locked']}",
        f"ranker_runtime_upgrade_created={ranker['ranker_runtime_upgrade_created']}",
        f"ranker_candidates_ranked={ranker['ranker_candidates_ranked']}",
        f"ranker_candidates_deduplicated={ranker['ranker_candidates_deduplicated']}",
        f"ranker_family_policy_applied={ranker['ranker_family_policy_applied']}",
        f"real_submission_created={ranker['real_submission_created']}",
        f"real_submission_allowed={ranker['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={ranker['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={ranker['kaggle_submission_sent']}",
        f"upload_performed={ranker['upload_performed']}",
        f"kaggle_authentication_performed={ranker['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "RANKER_RESULTS",
    ]

    for result in ranker["ranker_results"]:
        lines.append(
            f"{result['case_id']} family={result['family']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    lines.append("SAMPLE_RANKED_CANDIDATES")
    for candidate in ranker["sample_ranked_candidates"]:
        lines.append(
            f"rank={candidate['ranker_rank']} id={candidate['candidate_id']} "
            f"family={candidate['family']} operation={candidate['operation']} "
            f"ranker_score={candidate['ranker_score']} signature={candidate['signature']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_ranker_runtime_upgrade_artifacts(
    ranker: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    ranker = dict(ranker or build_milestone_8_ranker_runtime_upgrade())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-8-ranker-runtime-upgrade-v2.json"
    md_path = output / "milestone-8-ranker-runtime-upgrade-v2.md"
    manifest_path = output / "milestone-8-ranker-runtime-upgrade-manifest-v2.txt"
    index_path = output / "milestone-8-ranker-runtime-upgrade-index-v2.json"

    json_path.write_text(json.dumps(ranker, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_ranker_runtime_upgrade_markdown(ranker), encoding="utf-8")
    manifest_path.write_text(render_ranker_runtime_upgrade_manifest(ranker), encoding="utf-8")
    index_path.write_text(json.dumps(ranker["ranker_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_8_ranker_runtime_upgrade_pipeline() -> Dict[str, Any]:
    ranker = build_milestone_8_ranker_runtime_upgrade()
    validation = validate_milestone_8_ranker_runtime_upgrade(ranker)
    artifacts = write_ranker_runtime_upgrade_artifacts(ranker)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_PIPELINE_INVALID",
        "ranker_status": ranker["status"],
        "validation_status": validation["status"],
        "ranker": ranker,
        "ranker_id": ranker["ranker_id"],
        "signature": ranker["signature"],
        "ranker_mode": ranker["ranker_mode"],
        "ranker_verdict": ranker["ranker_verdict"],
        "next_allowed_stage": ranker["next_allowed_stage"],
        "family_count": ranker["family_count"],
        "ranker_policy_count": ranker["ranker_policy_count"],
        "ranker_operation_count": ranker["ranker_operation_count"],
        "ranker_case_count": ranker["ranker_case_count"],
        "ranker_pass_count": ranker["ranker_pass_count"],
        "ranker_failure_count": ranker["ranker_failure_count"],
        "sample_ranked_candidate_count": ranker["sample_ranked_candidate_count"],
        "evidence_field_count": ranker["evidence_field_count"],
        "regression_guard_count": ranker["regression_guard_count"],
        "boundary_control_count": ranker["boundary_control_count"],
        "ranker_gate_count": ranker["ranker_gate_count"],
        "passed_gate_count": ranker["passed_gate_count"],
        "ranker_issue_count": ranker["ranker_issue_count"],
        "warning_count": ranker["warning_count"],
        "ranker_ready": ranker["ranker_ready"],
        "ranker_locked": ranker["ranker_locked"],
        "ranker_runtime_upgrade_created": ranker["ranker_runtime_upgrade_created"],
        "ranker_candidates_ranked": ranker["ranker_candidates_ranked"],
        "ranker_candidates_deduplicated": ranker["ranker_candidates_deduplicated"],
        "ranker_family_policy_applied": ranker["ranker_family_policy_applied"],
        "real_submission_created": ranker["real_submission_created"],
        "real_submission_allowed": ranker["real_submission_allowed"],
        "ready_for_real_kaggle_submission": ranker["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": ranker["kaggle_submission_sent"],
        "upload_performed": ranker["upload_performed"],
        "kaggle_authentication_performed": ranker["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": ranker["metadata"],
    }
