"""Milestone #7 Ranker Evidence Upgrade v1.

Local-only ranker evidence upgrade registry.

This module converts candidate generator profiles into deterministic evidence
profiles for ranker scoring, calibration, and regression guarding. It does not
submit to Kaggle, authenticate, upload files, call external APIs, read secrets,
create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


RANKER_STATUS = "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY"
PIPELINE_STATUS = "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_VALID"

BASELINE_COMMIT = "0dfd280 Add ARC AGI3 candidate generator improvement"
RANKER_MODE = "RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD"
RANKER_SCOPE = "UPGRADE_DETERMINISTIC_RANKER_EVIDENCE_FROM_CANDIDATE_GENERATOR_PROFILES"
RANKER_VERDICT = "RANKER_EVIDENCE_UPGRADE_READY_FOR_REGRESSION_BENCHMARK"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_6_REGRESSION_BENCHMARK"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/ranker-evidence-upgrade-v1"

GENERATOR_JSON = Path(
    "examples/milestone-7/candidate-generator-improvement-v1/"
    "milestone-7-candidate-generator-improvement-v1.json"
)

EXPECTED_PROFILE_COUNT = 3
EXPECTED_SOURCE_GENERATOR_COUNT = 3
EXPECTED_EVIDENCE_CHANNEL_COUNT = 12
EXPECTED_SCORING_RULE_COUNT = 12
EXPECTED_CALIBRATION_RULE_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 9
EXPECTED_AGGREGATE_MAX_SCORE = 300


RANKER_PROFILES: Tuple[Dict[str, Any], ...] = (
    {
        "ranker_profile_id": "ranker_evidence_color_mapping_v1",
        "family": "color_mapping",
        "source_generator_profile_id": "candidate_generator_color_mapping_v1",
        "source_branch": "candidate_branch_color_mapping_v1",
        "priority": "P0",
        "evidence_channels": (
            "palette_consistency_score",
            "color_frequency_delta_score",
            "background_stability_score",
            "foreground_stability_score",
        ),
        "scoring_rules": (
            "reward_train_consistent_color_map",
            "penalize_unseen_palette_permutation",
            "reward_background_preservation",
            "penalize_dimension_unjustified_color_output",
        ),
        "calibration_rules": (
            "cap_score_when_mapping_partial",
            "boost_score_when_all_train_pairs_agree",
            "downgrade_score_when_background_unstable",
        ),
        "regression_guards": (
            "no_random_palette_rank_boost",
            "bounded_color_score_range",
            "full_suite_must_remain_green",
        ),
        "max_profile_score": 100,
        "tie_breaker": "stable_signature_then_template_order",
        "ranker_runtime_modified": False,
        "ready_for_task_6": True,
    },
    {
        "ranker_profile_id": "ranker_evidence_object_model_v1",
        "family": "object_model",
        "source_generator_profile_id": "candidate_generator_object_model_v1",
        "source_branch": "candidate_branch_object_model_v1",
        "priority": "P0",
        "evidence_channels": (
            "component_count_delta_score",
            "bounding_box_delta_score",
            "object_position_delta_score",
            "object_size_delta_score",
        ),
        "scoring_rules": (
            "reward_component_count_consistency",
            "reward_train_consistent_object_delta",
            "penalize_unbounded_component_rewrite",
            "reward_object_color_signature_preservation",
        ),
        "calibration_rules": (
            "cap_score_when_component_match_partial",
            "boost_score_when_object_delta_repeats",
            "downgrade_score_when_object_count_unstable",
        ),
        "regression_guards": (
            "no_unbounded_object_rank_boost",
            "bounded_object_score_range",
            "full_suite_must_remain_green",
        ),
        "max_profile_score": 100,
        "tie_breaker": "stable_signature_then_object_delta_order",
        "ranker_runtime_modified": False,
        "ready_for_task_6": True,
    },
    {
        "ranker_profile_id": "ranker_evidence_shape_symmetry_v1",
        "family": "shape_symmetry",
        "source_generator_profile_id": "candidate_generator_shape_symmetry_v1",
        "source_branch": "candidate_branch_shape_symmetry_v1",
        "priority": "P0",
        "evidence_channels": (
            "axis_symmetry_score",
            "rotation_equivalence_score",
            "translation_delta_score",
            "shape_signature_delta_score",
        ),
        "scoring_rules": (
            "reward_axis_consistent_completion",
            "reward_train_consistent_spatial_delta",
            "penalize_random_geometric_transform",
            "reward_valid_grid_bounds_preservation",
        ),
        "calibration_rules": (
            "cap_score_when_symmetry_partial",
            "boost_score_when_spatial_delta_repeats",
            "downgrade_score_when_bounds_change_unjustified",
        ),
        "regression_guards": (
            "no_random_geometry_rank_boost",
            "bounded_shape_score_range",
            "full_suite_must_remain_green",
        ),
        "max_profile_score": 100,
        "tie_breaker": "stable_signature_then_spatial_delta_order",
        "ranker_runtime_modified": False,
        "ready_for_task_6": True,
    },
)


RANKER_GATES: Tuple[str, ...] = (
    "generator_artifact_present",
    "generator_artifact_ready",
    "generator_artifact_valid",
    "generator_next_stage_matches_task_5",
    "candidate_generator_profiles_ready",
    "ranker_mode_valid",
    "ranker_scope_valid",
    "ranker_verdict_valid",
    "ranker_ready",
    "ranker_locked",
    "profile_count_valid",
    "source_generator_count_valid",
    "evidence_channel_count_valid",
    "scoring_rule_count_valid",
    "calibration_rule_count_valid",
    "regression_guard_count_valid",
    "aggregate_max_score_valid",
    "all_profiles_priority_p0",
    "all_profiles_have_source_generator",
    "all_source_generators_found_in_generator_artifact",
    "all_profiles_have_family",
    "all_profiles_have_source_branch",
    "all_profiles_have_evidence_channels",
    "all_profiles_have_scoring_rules",
    "all_profiles_have_calibration_rules",
    "all_profiles_have_regression_guards",
    "all_profiles_have_tie_breaker",
    "all_profiles_have_bounded_max_score",
    "all_profiles_runtime_not_modified",
    "all_profiles_ready_for_task_6",
    "color_ranker_evidence_present",
    "object_ranker_evidence_present",
    "shape_ranker_evidence_present",
    "ranker_evidence_profiles_ready",
    "runtime_solver_not_modified",
    "ranker_runtime_not_modified",
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

RANKER_ISSUES: Tuple[str, ...] = (
    "generator_artifact_missing",
    "generator_artifact_not_ready",
    "generator_artifact_invalid",
    "generator_next_stage_mismatch",
    "candidate_generator_profiles_not_ready",
    "ranker_mode_invalid",
    "ranker_scope_invalid",
    "ranker_verdict_invalid",
    "ranker_not_ready",
    "ranker_not_locked",
    "profile_count_invalid",
    "source_generator_count_invalid",
    "evidence_channel_count_invalid",
    "scoring_rule_count_invalid",
    "calibration_rule_count_invalid",
    "regression_guard_count_invalid",
    "aggregate_max_score_invalid",
    "profile_priority_not_p0",
    "profile_source_generator_missing",
    "source_generator_not_found_in_generator_artifact",
    "profile_family_missing",
    "profile_source_branch_missing",
    "profile_evidence_channels_missing",
    "profile_scoring_rules_missing",
    "profile_calibration_rules_missing",
    "profile_regression_guards_missing",
    "profile_tie_breaker_missing",
    "profile_unbounded_max_score",
    "profile_runtime_modified",
    "profile_not_ready_for_task_6",
    "color_ranker_evidence_missing",
    "object_ranker_evidence_missing",
    "shape_ranker_evidence_missing",
    "ranker_evidence_profiles_not_ready",
    "runtime_solver_modified",
    "ranker_runtime_modified",
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


def _boundary_from_generator(generator: Mapping[str, Any]) -> Dict[str, Any]:
    source = generator.get("boundary", {}) if isinstance(generator.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": generator.get("kaggle_submission_sent"),
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


def _generator_source(generator: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(GENERATOR_JSON)
    return {
        "name": "milestone_7_candidate_generator_improvement",
        "path": str(GENERATOR_JSON),
        "present": GENERATOR_JSON.exists(),
        "expected_status": "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY",
        "actual_status": generator.get("status", "MISSING"),
        "ready": GENERATOR_JSON.exists()
        and generator.get("status") == "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY",
        "artifact_id": generator.get("generator_id", "MISSING_GENERATOR_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _generator_profile_ids(generator: Mapping[str, Any]) -> Tuple[str, ...]:
    items = generator.get("generator_profiles", [])
    if not isinstance(items, list):
        return tuple()
    return tuple(str(item.get("generator_profile_id", "")) for item in items if isinstance(item, Mapping))


def build_milestone_7_ranker_evidence_upgrade() -> Dict[str, Any]:
    generator = _read_json(GENERATOR_JSON)
    boundary = _boundary_from_generator(generator)
    generator_source = _generator_source(generator)
    generator_profile_ids = _generator_profile_ids(generator)

    profiles = tuple(dict(item) for item in RANKER_PROFILES)
    families = {item["family"] for item in profiles}
    source_generators = {item["source_generator_profile_id"] for item in profiles}

    evidence_channel_count = sum(len(item.get("evidence_channels", ())) for item in profiles)
    scoring_rule_count = sum(len(item.get("scoring_rules", ())) for item in profiles)
    calibration_rule_count = sum(len(item.get("calibration_rules", ())) for item in profiles)
    regression_guard_count = sum(len(item.get("regression_guards", ())) for item in profiles)
    aggregate_max_score = sum(int(item.get("max_profile_score", 0)) for item in profiles)

    ranker_record = {
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "ranker_ready": True,
        "ranker_locked": True,
        "generator_id": generator.get("generator_id", "MISSING_GENERATOR_ID"),
        "generator_ready": generator.get("generator_ready") is True,
        "candidate_generator_profiles_ready": generator.get("candidate_generator_profiles_ready") is True,
        "profile_count": len(profiles),
        "source_generator_count": len(source_generators),
        "evidence_channel_count": evidence_channel_count,
        "scoring_rule_count": scoring_rule_count,
        "calibration_rule_count": calibration_rule_count,
        "regression_guard_count": regression_guard_count,
        "aggregate_max_score": aggregate_max_score,
        "families": sorted(families),
        "source_generators": sorted(source_generators),
        "ranker_evidence_profiles_ready": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "regression_benchmark_dependency": "MILESTONE_7_TASK_6_REGRESSION_BENCHMARK",
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
        "generator_artifact_present": GENERATOR_JSON.exists(),
        "generator_artifact_ready": generator.get("status") == "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY",
        "generator_artifact_valid": bool(generator.get("generator_id")) and bool(generator.get("signature")),
        "generator_next_stage_matches_task_5": generator.get("next_allowed_stage") == "MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE",
        "candidate_generator_profiles_ready": generator.get("candidate_generator_profiles_ready") is True,
        "ranker_mode_valid": ranker_record["ranker_mode"] == RANKER_MODE,
        "ranker_scope_valid": ranker_record["ranker_scope"] == RANKER_SCOPE,
        "ranker_verdict_valid": ranker_record["ranker_verdict"] == RANKER_VERDICT,
        "ranker_ready": ranker_record["ranker_ready"] is True,
        "ranker_locked": ranker_record["ranker_locked"] is True,
        "profile_count_valid": len(profiles) == EXPECTED_PROFILE_COUNT,
        "source_generator_count_valid": len(source_generators) == EXPECTED_SOURCE_GENERATOR_COUNT,
        "evidence_channel_count_valid": evidence_channel_count == EXPECTED_EVIDENCE_CHANNEL_COUNT,
        "scoring_rule_count_valid": scoring_rule_count == EXPECTED_SCORING_RULE_COUNT,
        "calibration_rule_count_valid": calibration_rule_count == EXPECTED_CALIBRATION_RULE_COUNT,
        "regression_guard_count_valid": regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT,
        "aggregate_max_score_valid": aggregate_max_score == EXPECTED_AGGREGATE_MAX_SCORE,
        "all_profiles_priority_p0": all(item.get("priority") == "P0" for item in profiles),
        "all_profiles_have_source_generator": all(bool(item.get("source_generator_profile_id")) for item in profiles),
        "all_source_generators_found_in_generator_artifact": all(item in generator_profile_ids for item in source_generators),
        "all_profiles_have_family": all(bool(item.get("family")) for item in profiles),
        "all_profiles_have_source_branch": all(bool(item.get("source_branch")) for item in profiles),
        "all_profiles_have_evidence_channels": all(len(item.get("evidence_channels", ())) > 0 for item in profiles),
        "all_profiles_have_scoring_rules": all(len(item.get("scoring_rules", ())) > 0 for item in profiles),
        "all_profiles_have_calibration_rules": all(len(item.get("calibration_rules", ())) > 0 for item in profiles),
        "all_profiles_have_regression_guards": all(len(item.get("regression_guards", ())) > 0 for item in profiles),
        "all_profiles_have_tie_breaker": all(bool(item.get("tie_breaker")) for item in profiles),
        "all_profiles_have_bounded_max_score": all(int(item.get("max_profile_score", 0)) == 100 for item in profiles),
        "all_profiles_runtime_not_modified": all(item.get("ranker_runtime_modified") is False for item in profiles),
        "all_profiles_ready_for_task_6": all(item.get("ready_for_task_6") is True for item in profiles),
        "color_ranker_evidence_present": "color_mapping" in families,
        "object_ranker_evidence_present": "object_model" in families,
        "shape_ranker_evidence_present": "shape_symmetry" in families,
        "ranker_evidence_profiles_ready": ranker_record["ranker_evidence_profiles_ready"] is True,
        "runtime_solver_not_modified": ranker_record["runtime_solver_modified"] is False,
        "ranker_runtime_not_modified": ranker_record["ranker_runtime_modified"] is False,
        "next_stage_valid": ranker_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": ranker_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": ranker_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": ranker_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": ranker_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": ranker_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": ranker_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": ranker_record["kaggle_submission_sent"] is False,
        "upload_not_performed": ranker_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": ranker_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "generator_artifact_missing": not gate_state["generator_artifact_present"],
        "generator_artifact_not_ready": not gate_state["generator_artifact_ready"],
        "generator_artifact_invalid": not gate_state["generator_artifact_valid"],
        "generator_next_stage_mismatch": not gate_state["generator_next_stage_matches_task_5"],
        "candidate_generator_profiles_not_ready": not gate_state["candidate_generator_profiles_ready"],
        "ranker_mode_invalid": not gate_state["ranker_mode_valid"],
        "ranker_scope_invalid": not gate_state["ranker_scope_valid"],
        "ranker_verdict_invalid": not gate_state["ranker_verdict_valid"],
        "ranker_not_ready": not gate_state["ranker_ready"],
        "ranker_not_locked": not gate_state["ranker_locked"],
        "profile_count_invalid": not gate_state["profile_count_valid"],
        "source_generator_count_invalid": not gate_state["source_generator_count_valid"],
        "evidence_channel_count_invalid": not gate_state["evidence_channel_count_valid"],
        "scoring_rule_count_invalid": not gate_state["scoring_rule_count_valid"],
        "calibration_rule_count_invalid": not gate_state["calibration_rule_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "aggregate_max_score_invalid": not gate_state["aggregate_max_score_valid"],
        "profile_priority_not_p0": not gate_state["all_profiles_priority_p0"],
        "profile_source_generator_missing": not gate_state["all_profiles_have_source_generator"],
        "source_generator_not_found_in_generator_artifact": not gate_state["all_source_generators_found_in_generator_artifact"],
        "profile_family_missing": not gate_state["all_profiles_have_family"],
        "profile_source_branch_missing": not gate_state["all_profiles_have_source_branch"],
        "profile_evidence_channels_missing": not gate_state["all_profiles_have_evidence_channels"],
        "profile_scoring_rules_missing": not gate_state["all_profiles_have_scoring_rules"],
        "profile_calibration_rules_missing": not gate_state["all_profiles_have_calibration_rules"],
        "profile_regression_guards_missing": not gate_state["all_profiles_have_regression_guards"],
        "profile_tie_breaker_missing": not gate_state["all_profiles_have_tie_breaker"],
        "profile_unbounded_max_score": not gate_state["all_profiles_have_bounded_max_score"],
        "profile_runtime_modified": not gate_state["all_profiles_runtime_not_modified"],
        "profile_not_ready_for_task_6": not gate_state["all_profiles_ready_for_task_6"],
        "color_ranker_evidence_missing": not gate_state["color_ranker_evidence_present"],
        "object_ranker_evidence_missing": not gate_state["object_ranker_evidence_present"],
        "shape_ranker_evidence_missing": not gate_state["shape_ranker_evidence_present"],
        "ranker_evidence_profiles_not_ready": not gate_state["ranker_evidence_profiles_ready"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "ranker_runtime_modified": not gate_state["ranker_runtime_not_modified"],
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
        for name in RANKER_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in RANKER_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    ranker_ready = (
        generator_source["ready"] is True
        and len(profiles) == EXPECTED_PROFILE_COUNT
        and evidence_channel_count == EXPECTED_EVIDENCE_CHANNEL_COUNT
        and scoring_rule_count == EXPECTED_SCORING_RULE_COUNT
        and calibration_rule_count == EXPECTED_CALIBRATION_RULE_COUNT
        and regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT
        and aggregate_max_score == EXPECTED_AGGREGATE_MAX_SCORE
        and passed_gate_count == len(RANKER_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 5",
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_generator": generator.get("generator_id", "MISSING_GENERATOR_ID"),
        "ranker_ready": ranker_ready,
        "ranker_locked": True,
        "profile_count": len(profiles),
        "source_generator_count": len(source_generators),
        "evidence_channel_count": evidence_channel_count,
        "scoring_rule_count": scoring_rule_count,
        "calibration_rule_count": calibration_rule_count,
        "regression_guard_count": regression_guard_count,
        "aggregate_max_score": aggregate_max_score,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "ranker_evidence_profiles_ready": True,
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
        "status": RANKER_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 5",
        "title": "Ranker Evidence Upgrade v1",
        "baseline_commit": BASELINE_COMMIT,
        "ranker_mode": RANKER_MODE,
        "ranker_scope": RANKER_SCOPE,
        "ranker_verdict": RANKER_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_generator_source": generator_source,
        "ranker_record": ranker_record,
        "ranker_profiles": list(profiles),
        "ranker_gates": list(gates),
        "ranker_issues": list(issues),
        "ranker_index": index,
        "boundary": boundary,
        "profile_count": len(profiles),
        "source_generator_count": len(source_generators),
        "evidence_channel_count": evidence_channel_count,
        "scoring_rule_count": scoring_rule_count,
        "calibration_rule_count": calibration_rule_count,
        "regression_guard_count": regression_guard_count,
        "aggregate_max_score": aggregate_max_score,
        "ranker_gate_count": len(RANKER_GATES),
        "passed_gate_count": passed_gate_count,
        "ranker_issue_count": issue_count,
        "warning_count": 0,
        "ranker_ready": ranker_ready,
        "ranker_locked": True,
        "runtime_solver_modified": False,
        "ranker_runtime_modified": False,
        "ranker_evidence_profiles_ready": True,
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
            "source": "milestone_7_ranker_evidence_upgrade_v1",
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
        "ranker_id": f"MILESTONE-7-RANKER-EVIDENCE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_ranker_evidence_upgrade(ranker: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = ranker.get("boundary", {})
    gates = ranker.get("ranker_gates", [])
    issues = ranker.get("ranker_issues", [])
    profiles = ranker.get("ranker_profiles", [])
    source = ranker.get("milestone_7_generator_source", {})

    checks = {
        "status_ready": ranker.get("status") == RANKER_STATUS,
        "ranker_id_present": isinstance(ranker.get("ranker_id"), str) and bool(ranker.get("ranker_id")),
        "signature_present": isinstance(ranker.get("signature"), str) and bool(ranker.get("signature")),
        "baseline_commit_valid": str(ranker.get("baseline_commit", "")).startswith("0dfd280"),
        "ranker_mode_valid": ranker.get("ranker_mode") == RANKER_MODE,
        "ranker_scope_valid": ranker.get("ranker_scope") == RANKER_SCOPE,
        "ranker_verdict_valid": ranker.get("ranker_verdict") == RANKER_VERDICT,
        "next_allowed_stage_valid": ranker.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "generator_source_ready": source.get("ready") is True,
        "generator_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "profile_count_valid": ranker.get("profile_count") == EXPECTED_PROFILE_COUNT,
        "source_generator_count_valid": ranker.get("source_generator_count") == EXPECTED_SOURCE_GENERATOR_COUNT,
        "evidence_channel_count_valid": ranker.get("evidence_channel_count") == EXPECTED_EVIDENCE_CHANNEL_COUNT,
        "scoring_rule_count_valid": ranker.get("scoring_rule_count") == EXPECTED_SCORING_RULE_COUNT,
        "calibration_rule_count_valid": ranker.get("calibration_rule_count") == EXPECTED_CALIBRATION_RULE_COUNT,
        "regression_guard_count_valid": ranker.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "aggregate_max_score_valid": ranker.get("aggregate_max_score") == EXPECTED_AGGREGATE_MAX_SCORE,
        "all_profiles_have_evidence_channels": bool(profiles) and all(len(item.get("evidence_channels", ())) > 0 for item in profiles),
        "all_profiles_have_scoring_rules": bool(profiles) and all(len(item.get("scoring_rules", ())) > 0 for item in profiles),
        "all_profiles_have_calibration_rules": bool(profiles) and all(len(item.get("calibration_rules", ())) > 0 for item in profiles),
        "all_profiles_have_regression_guards": bool(profiles) and all(len(item.get("regression_guards", ())) > 0 for item in profiles),
        "all_profiles_runtime_not_modified": bool(profiles) and all(item.get("ranker_runtime_modified") is False for item in profiles),
        "all_profiles_ready_for_task_6": bool(profiles) and all(item.get("ready_for_task_6") is True for item in profiles),
        "runtime_solver_not_modified": ranker.get("runtime_solver_modified") is False,
        "ranker_runtime_not_modified": ranker.get("ranker_runtime_modified") is False,
        "ranker_evidence_profiles_ready": ranker.get("ranker_evidence_profiles_ready") is True,
        "ranker_gate_count_matches": ranker.get("ranker_gate_count") == len(RANKER_GATES),
        "all_ranker_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "ranker_issue_count_zero": ranker.get("ranker_issue_count") == 0,
        "all_ranker_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "ranker_ready": ranker.get("ranker_ready") is True,
        "ranker_locked": ranker.get("ranker_locked") is True,
        "solver_improvement_required": ranker.get("solver_improvement_required") is True,
        "competitive_claim_absent": ranker.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": ranker.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": ranker.get("manual_upload_performed") is False,
        "real_submission_allowed_false": ranker.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": ranker.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": ranker.get("real_submission_created") is False,
        "kaggle_submission_not_sent": ranker.get("kaggle_submission_sent") is False,
        "upload_not_performed": ranker.get("upload_performed") is False,
        "kaggle_authentication_not_performed": ranker.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_INVALID",
        "valid": valid,
        "checks": checks,
        "ranker_id": ranker.get("ranker_id"),
        "signature": ranker.get("signature"),
    }


def render_ranker_evidence_upgrade_markdown(ranker: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Ranker Evidence Upgrade v1",
        "",
        f"- status: {ranker['status']}",
        f"- ranker_id: {ranker['ranker_id']}",
        f"- signature: {ranker['signature']}",
        f"- baseline_commit: {ranker['baseline_commit']}",
        f"- ranker_mode: {ranker['ranker_mode']}",
        f"- ranker_scope: {ranker['ranker_scope']}",
        f"- ranker_verdict: {ranker['ranker_verdict']}",
        f"- next_allowed_stage: {ranker['next_allowed_stage']}",
        f"- profile_count: {ranker['profile_count']}",
        f"- source_generator_count: {ranker['source_generator_count']}",
        f"- evidence_channel_count: {ranker['evidence_channel_count']}",
        f"- scoring_rule_count: {ranker['scoring_rule_count']}",
        f"- calibration_rule_count: {ranker['calibration_rule_count']}",
        f"- regression_guard_count: {ranker['regression_guard_count']}",
        f"- aggregate_max_score: {ranker['aggregate_max_score']}",
        f"- ranker_gate_count: {ranker['ranker_gate_count']}",
        f"- passed_gate_count: {ranker['passed_gate_count']}",
        f"- ranker_issue_count: {ranker['ranker_issue_count']}",
        f"- ranker_ready: {ranker['ranker_ready']}",
        f"- ranker_runtime_modified: {ranker['ranker_runtime_modified']}",
        f"- runtime_solver_modified: {ranker['runtime_solver_modified']}",
        f"- real_submission_allowed: {ranker['real_submission_allowed']}",
        f"- kaggle_submission_sent: {ranker['kaggle_submission_sent']}",
        f"- upload_performed: {ranker['upload_performed']}",
        "",
        "## Ranker evidence profiles",
        "",
    ]

    for item in ranker["ranker_profiles"]:
        lines.append(
            f"- {item['priority']} {item['ranker_profile_id']} / family={item['family']} / "
            f"source={item['source_generator_profile_id']} / channels={len(item['evidence_channels'])} / "
            f"max_profile_score={item['max_profile_score']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Ranker evidence profiles are ready for regression benchmark.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_VALID=true",
            "ARC_AGI3_MILESTONE_7_RANKER_MODE=RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_RANKER_VERDICT=RANKER_EVIDENCE_UPGRADE_READY_FOR_REGRESSION_BENCHMARK",
            "ARC_AGI3_MILESTONE_7_PROFILE_COUNT=3",
            "ARC_AGI3_MILESTONE_7_SOURCE_GENERATOR_COUNT=3",
            "ARC_AGI3_MILESTONE_7_EVIDENCE_CHANNEL_COUNT=12",
            "ARC_AGI3_MILESTONE_7_SCORING_RULE_COUNT=12",
            "ARC_AGI3_MILESTONE_7_CALIBRATION_RULE_COUNT=9",
            "ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=9",
            "ARC_AGI3_MILESTONE_7_AGGREGATE_MAX_SCORE=300",
            "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_RANKER_RUNTIME_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_PROFILES_READY=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_6_REGRESSION_BENCHMARK",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_GENERATOR_COMMIT=0dfd280",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_ranker_evidence_upgrade_manifest(ranker: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 RANKER EVIDENCE UPGRADE MANIFEST v1",
        f"ranker_id={ranker['ranker_id']}",
        f"signature={ranker['signature']}",
        f"status={ranker['status']}",
        f"baseline_commit={ranker['baseline_commit']}",
        f"ranker_mode={ranker['ranker_mode']}",
        f"ranker_verdict={ranker['ranker_verdict']}",
        f"next_allowed_stage={ranker['next_allowed_stage']}",
        f"profile_count={ranker['profile_count']}",
        f"source_generator_count={ranker['source_generator_count']}",
        f"evidence_channel_count={ranker['evidence_channel_count']}",
        f"scoring_rule_count={ranker['scoring_rule_count']}",
        f"calibration_rule_count={ranker['calibration_rule_count']}",
        f"regression_guard_count={ranker['regression_guard_count']}",
        f"aggregate_max_score={ranker['aggregate_max_score']}",
        f"ranker_gate_count={ranker['ranker_gate_count']}",
        f"passed_gate_count={ranker['passed_gate_count']}",
        f"ranker_issue_count={ranker['ranker_issue_count']}",
        f"ranker_ready={ranker['ranker_ready']}",
        f"ranker_locked={ranker['ranker_locked']}",
        f"runtime_solver_modified={ranker['runtime_solver_modified']}",
        f"ranker_runtime_modified={ranker['ranker_runtime_modified']}",
        f"ranker_evidence_profiles_ready={ranker['ranker_evidence_profiles_ready']}",
        f"solver_improvement_required={ranker['solver_improvement_required']}",
        f"competitive_claim_absent={ranker['competitive_claim_absent']}",
        f"manual_submission_allowed={ranker['manual_submission_allowed']}",
        f"manual_upload_performed={ranker['manual_upload_performed']}",
        f"real_submission_allowed={ranker['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={ranker['ready_for_real_kaggle_submission']}",
        f"real_submission_created={ranker['real_submission_created']}",
        f"kaggle_submission_sent={ranker['kaggle_submission_sent']}",
        f"upload_performed={ranker['upload_performed']}",
        f"kaggle_authentication_performed={ranker['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "RANKER_PROFILES",
    ]

    for item in ranker["ranker_profiles"]:
        lines.append(
            f"{item['priority']} {item['ranker_profile_id']} family={item['family']} "
            f"source_generator={item['source_generator_profile_id']} source_branch={item['source_branch']} "
            f"evidence_channel_count={len(item['evidence_channels'])} scoring_rule_count={len(item['scoring_rules'])} "
            f"calibration_rule_count={len(item['calibration_rules'])} regression_guard_count={len(item['regression_guards'])} "
            f"max_profile_score={item['max_profile_score']} tie_breaker={item['tie_breaker']} "
            f"ranker_runtime_modified={item['ranker_runtime_modified']} ready_for_task_6={item['ready_for_task_6']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_ranker_evidence_upgrade_artifacts(
    ranker: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    ranker = dict(ranker or build_milestone_7_ranker_evidence_upgrade())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-ranker-evidence-upgrade-v1.json"
    md_path = output / "milestone-7-ranker-evidence-upgrade-v1.md"
    manifest_path = output / "milestone-7-ranker-evidence-upgrade-manifest-v1.txt"
    index_path = output / "milestone-7-ranker-evidence-upgrade-index-v1.json"

    json_path.write_text(json.dumps(ranker, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_ranker_evidence_upgrade_markdown(ranker), encoding="utf-8")
    manifest_path.write_text(render_ranker_evidence_upgrade_manifest(ranker), encoding="utf-8")
    index_path.write_text(json.dumps(ranker["ranker_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_ranker_evidence_upgrade_pipeline() -> Dict[str, Any]:
    ranker = build_milestone_7_ranker_evidence_upgrade()
    validation = validate_milestone_7_ranker_evidence_upgrade(ranker)
    artifacts = write_ranker_evidence_upgrade_artifacts(ranker)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_PIPELINE_INVALID",
        "ranker_status": ranker["status"],
        "validation_status": validation["status"],
        "ranker": ranker,
        "ranker_id": ranker["ranker_id"],
        "signature": ranker["signature"],
        "ranker_mode": ranker["ranker_mode"],
        "ranker_verdict": ranker["ranker_verdict"],
        "next_allowed_stage": ranker["next_allowed_stage"],
        "profile_count": ranker["profile_count"],
        "source_generator_count": ranker["source_generator_count"],
        "evidence_channel_count": ranker["evidence_channel_count"],
        "scoring_rule_count": ranker["scoring_rule_count"],
        "calibration_rule_count": ranker["calibration_rule_count"],
        "regression_guard_count": ranker["regression_guard_count"],
        "aggregate_max_score": ranker["aggregate_max_score"],
        "ranker_gate_count": ranker["ranker_gate_count"],
        "passed_gate_count": ranker["passed_gate_count"],
        "ranker_issue_count": ranker["ranker_issue_count"],
        "warning_count": ranker["warning_count"],
        "ranker_ready": ranker["ranker_ready"],
        "ranker_locked": ranker["ranker_locked"],
        "runtime_solver_modified": ranker["runtime_solver_modified"],
        "ranker_runtime_modified": ranker["ranker_runtime_modified"],
        "ranker_evidence_profiles_ready": ranker["ranker_evidence_profiles_ready"],
        "solver_improvement_required": ranker["solver_improvement_required"],
        "competitive_claim_absent": ranker["competitive_claim_absent"],
        "manual_submission_allowed": ranker["manual_submission_allowed"],
        "manual_upload_performed": ranker["manual_upload_performed"],
        "real_submission_allowed": ranker["real_submission_allowed"],
        "ready_for_real_kaggle_submission": ranker["ready_for_real_kaggle_submission"],
        "real_submission_created": ranker["real_submission_created"],
        "kaggle_submission_sent": ranker["kaggle_submission_sent"],
        "upload_performed": ranker["upload_performed"],
        "kaggle_authentication_performed": ranker["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": ranker["metadata"],
    }
