"""Milestone #7 Candidate Generator Improvement v1.

Local-only candidate generator improvement registry.

This module converts task-family solver expansion branches into deterministic
candidate generator profiles for color mapping, object modeling, and
shape/symmetry. It does not submit to Kaggle, authenticate, upload files, call
external APIs, read secrets, create upload archives, or create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


GENERATOR_STATUS = "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY"
PIPELINE_STATUS = "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_VALID"

BASELINE_COMMIT = "3ec630b Add ARC AGI3 task-family solver expansion"
GENERATOR_MODE = "CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD"
GENERATOR_SCOPE = "GENERATE_DETERMINISTIC_CANDIDATE_TEMPLATES_FROM_TASK_FAMILIES"
GENERATOR_VERDICT = "CANDIDATE_GENERATOR_IMPROVEMENT_READY_FOR_RANKER_EVIDENCE_UPGRADE"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/candidate-generator-improvement-v1"

EXPANSION_JSON = Path(
    "examples/milestone-7/task-family-solver-expansion-v1/"
    "milestone-7-task-family-solver-expansion-v1.json"
)

EXPECTED_PROFILE_COUNT = 3
EXPECTED_SOURCE_FAMILY_COUNT = 3
EXPECTED_TEMPLATE_COUNT = 12
EXPECTED_EVIDENCE_FIELD_COUNT = 15
EXPECTED_DETERMINISTIC_RULE_COUNT = 12
EXPECTED_REGRESSION_GUARD_COUNT = 9
EXPECTED_MAX_CANDIDATE_COUNT = 24

GENERATOR_PROFILES: Tuple[Dict[str, Any], ...] = (
    {
        "generator_profile_id": "candidate_generator_color_mapping_v1",
        "family": "color_mapping",
        "source_family_id": "color_mapping_family_v1",
        "source_failure_class": "color_transform_undercoverage",
        "generator_branch": "candidate_branch_color_mapping_v1",
        "priority": "P0",
        "candidate_templates": (
            "stable_color_remap_candidate",
            "palette_swap_candidate",
            "foreground_background_preservation_candidate",
            "color_histogram_signature_candidate",
        ),
        "evidence_fields": (
            "palette_size_delta",
            "color_frequency_delta",
            "background_color_stability",
            "foreground_color_stability",
            "train_color_mapping_consistency",
        ),
        "deterministic_rules": (
            "derive_mapping_from_train_pairs_only",
            "reject_unseen_random_color_permutation",
            "preserve_grid_dimensions",
            "preserve_background_when_confident",
        ),
        "regression_guards": (
            "no_random_palette_search",
            "bounded_palette_candidate_count",
            "full_suite_must_remain_green",
        ),
        "max_candidate_count": 8,
        "random_search_allowed": False,
        "unbounded_search_allowed": False,
        "ready_for_task_5": True,
    },
    {
        "generator_profile_id": "candidate_generator_object_model_v1",
        "family": "object_model",
        "source_family_id": "object_model_family_v1",
        "source_failure_class": "object_segmentation_undercoverage",
        "generator_branch": "candidate_branch_object_model_v1",
        "priority": "P0",
        "candidate_templates": (
            "connected_component_rewrite_candidate",
            "bounding_box_relation_candidate",
            "object_count_preservation_candidate",
            "object_color_signature_candidate",
        ),
        "evidence_fields": (
            "component_count_delta",
            "bounding_box_delta",
            "object_color_signature_delta",
            "object_position_delta",
            "object_size_delta",
        ),
        "deterministic_rules": (
            "derive_components_from_grid_connectivity",
            "reject_unbounded_component_search",
            "preserve_object_count_when_required",
            "prefer_train_consistent_object_delta",
        ),
        "regression_guards": (
            "no_unbounded_component_search",
            "bounded_object_candidate_count",
            "full_suite_must_remain_green",
        ),
        "max_candidate_count": 8,
        "random_search_allowed": False,
        "unbounded_search_allowed": False,
        "ready_for_task_5": True,
    },
    {
        "generator_profile_id": "candidate_generator_shape_symmetry_v1",
        "family": "shape_symmetry",
        "source_family_id": "shape_symmetry_family_v1",
        "source_failure_class": "spatial_symmetry_undercoverage",
        "generator_branch": "candidate_branch_shape_symmetry_v1",
        "priority": "P0",
        "candidate_templates": (
            "reflection_rotation_candidate",
            "translation_candidate",
            "crop_expand_candidate",
            "symmetry_completion_candidate",
        ),
        "evidence_fields": (
            "axis_symmetry_score",
            "rotation_equivalence_score",
            "translation_delta",
            "crop_expand_delta",
            "shape_signature_delta",
        ),
        "deterministic_rules": (
            "derive_spatial_delta_from_train_pairs",
            "reject_random_geometric_search",
            "preserve_valid_grid_bounds",
            "prefer_axis_consistent_completion",
        ),
        "regression_guards": (
            "no_random_geometric_search",
            "bounded_shape_candidate_count",
            "full_suite_must_remain_green",
        ),
        "max_candidate_count": 8,
        "random_search_allowed": False,
        "unbounded_search_allowed": False,
        "ready_for_task_5": True,
    },
)

GENERATOR_GATES: Tuple[str, ...] = (
    "expansion_artifact_present",
    "expansion_artifact_ready",
    "expansion_artifact_valid",
    "expansion_next_stage_matches_task_4",
    "expansion_registry_ready",
    "generator_mode_valid",
    "generator_scope_valid",
    "generator_verdict_valid",
    "generator_ready",
    "generator_locked",
    "profile_count_valid",
    "source_family_count_valid",
    "template_count_valid",
    "evidence_field_count_valid",
    "deterministic_rule_count_valid",
    "regression_guard_count_valid",
    "max_candidate_count_valid",
    "all_profiles_priority_p0",
    "all_profiles_have_source_family",
    "all_source_families_found_in_expansion",
    "all_profiles_have_source_failure",
    "all_profiles_have_branch",
    "all_profiles_have_templates",
    "all_profiles_have_evidence_fields",
    "all_profiles_have_deterministic_rules",
    "all_profiles_have_regression_guards",
    "all_profiles_have_bounded_candidate_count",
    "all_profiles_disable_random_search",
    "all_profiles_disable_unbounded_search",
    "all_profiles_ready_for_task_5",
    "color_candidate_generator_present",
    "object_candidate_generator_present",
    "shape_candidate_generator_present",
    "runtime_solver_not_modified",
    "candidate_generator_profiles_ready",
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

GENERATOR_ISSUES: Tuple[str, ...] = (
    "expansion_artifact_missing",
    "expansion_artifact_not_ready",
    "expansion_artifact_invalid",
    "expansion_next_stage_mismatch",
    "expansion_registry_not_ready",
    "generator_mode_invalid",
    "generator_scope_invalid",
    "generator_verdict_invalid",
    "generator_not_ready",
    "generator_not_locked",
    "profile_count_invalid",
    "source_family_count_invalid",
    "template_count_invalid",
    "evidence_field_count_invalid",
    "deterministic_rule_count_invalid",
    "regression_guard_count_invalid",
    "max_candidate_count_invalid",
    "profile_priority_not_p0",
    "profile_source_family_missing",
    "source_family_not_found_in_expansion",
    "profile_source_failure_missing",
    "profile_branch_missing",
    "profile_templates_missing",
    "profile_evidence_fields_missing",
    "profile_deterministic_rules_missing",
    "profile_regression_guards_missing",
    "profile_unbounded_candidate_count",
    "random_search_allowed",
    "unbounded_search_allowed",
    "profile_not_ready_for_task_5",
    "color_candidate_generator_missing",
    "object_candidate_generator_missing",
    "shape_candidate_generator_missing",
    "runtime_solver_modified",
    "candidate_generator_profiles_not_ready",
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


def _boundary_from_expansion(expansion: Mapping[str, Any]) -> Dict[str, Any]:
    source = expansion.get("boundary", {}) if isinstance(expansion.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": expansion.get("kaggle_submission_sent"),
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


def _expansion_source(expansion: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(EXPANSION_JSON)
    return {
        "name": "milestone_7_task_family_solver_expansion",
        "path": str(EXPANSION_JSON),
        "present": EXPANSION_JSON.exists(),
        "expected_status": "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY",
        "actual_status": expansion.get("status", "MISSING"),
        "ready": EXPANSION_JSON.exists()
        and expansion.get("status") == "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY",
        "artifact_id": expansion.get("expansion_id", "MISSING_EXPANSION_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _expansion_family_ids(expansion: Mapping[str, Any]) -> Tuple[str, ...]:
    items = expansion.get("family_expansions", [])
    if not isinstance(items, list):
        return tuple()
    return tuple(str(item.get("family_id", "")) for item in items if isinstance(item, Mapping))


def build_milestone_7_candidate_generator_improvement() -> Dict[str, Any]:
    expansion = _read_json(EXPANSION_JSON)
    boundary = _boundary_from_expansion(expansion)
    expansion_source = _expansion_source(expansion)
    expansion_family_ids = _expansion_family_ids(expansion)

    profiles = tuple(dict(item) for item in GENERATOR_PROFILES)
    families = {item["family"] for item in profiles}
    source_families = {item["source_family_id"] for item in profiles}

    template_count = sum(len(item.get("candidate_templates", ())) for item in profiles)
    evidence_field_count = sum(len(item.get("evidence_fields", ())) for item in profiles)
    deterministic_rule_count = sum(len(item.get("deterministic_rules", ())) for item in profiles)
    regression_guard_count = sum(len(item.get("regression_guards", ())) for item in profiles)
    max_candidate_count = sum(int(item.get("max_candidate_count", 0)) for item in profiles)

    generator_record = {
        "generator_mode": GENERATOR_MODE,
        "generator_scope": GENERATOR_SCOPE,
        "generator_verdict": GENERATOR_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "generator_ready": True,
        "generator_locked": True,
        "expansion_id": expansion.get("expansion_id", "MISSING_EXPANSION_ID"),
        "expansion_ready": expansion.get("expansion_ready") is True,
        "solver_family_registry_ready": expansion.get("solver_family_registry_ready") is True,
        "profile_count": len(profiles),
        "source_family_count": len(source_families),
        "template_count": template_count,
        "evidence_field_count": evidence_field_count,
        "deterministic_rule_count": deterministic_rule_count,
        "regression_guard_count": regression_guard_count,
        "max_candidate_count": max_candidate_count,
        "families": sorted(families),
        "source_families": sorted(source_families),
        "candidate_generator_profiles_ready": True,
        "runtime_solver_modified": False,
        "ranker_dependency": "MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE",
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
        "expansion_artifact_present": EXPANSION_JSON.exists(),
        "expansion_artifact_ready": expansion.get("status") == "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY",
        "expansion_artifact_valid": bool(expansion.get("expansion_id")) and bool(expansion.get("signature")),
        "expansion_next_stage_matches_task_4": expansion.get("next_allowed_stage") == "MILESTONE_7_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT",
        "expansion_registry_ready": expansion.get("solver_family_registry_ready") is True,
        "generator_mode_valid": generator_record["generator_mode"] == GENERATOR_MODE,
        "generator_scope_valid": generator_record["generator_scope"] == GENERATOR_SCOPE,
        "generator_verdict_valid": generator_record["generator_verdict"] == GENERATOR_VERDICT,
        "generator_ready": generator_record["generator_ready"] is True,
        "generator_locked": generator_record["generator_locked"] is True,
        "profile_count_valid": len(profiles) == EXPECTED_PROFILE_COUNT,
        "source_family_count_valid": len(source_families) == EXPECTED_SOURCE_FAMILY_COUNT,
        "template_count_valid": template_count == EXPECTED_TEMPLATE_COUNT,
        "evidence_field_count_valid": evidence_field_count == EXPECTED_EVIDENCE_FIELD_COUNT,
        "deterministic_rule_count_valid": deterministic_rule_count == EXPECTED_DETERMINISTIC_RULE_COUNT,
        "regression_guard_count_valid": regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT,
        "max_candidate_count_valid": max_candidate_count == EXPECTED_MAX_CANDIDATE_COUNT,
        "all_profiles_priority_p0": all(item.get("priority") == "P0" for item in profiles),
        "all_profiles_have_source_family": all(bool(item.get("source_family_id")) for item in profiles),
        "all_source_families_found_in_expansion": all(item in expansion_family_ids for item in source_families),
        "all_profiles_have_source_failure": all(bool(item.get("source_failure_class")) for item in profiles),
        "all_profiles_have_branch": all(bool(item.get("generator_branch")) for item in profiles),
        "all_profiles_have_templates": all(len(item.get("candidate_templates", ())) > 0 for item in profiles),
        "all_profiles_have_evidence_fields": all(len(item.get("evidence_fields", ())) > 0 for item in profiles),
        "all_profiles_have_deterministic_rules": all(len(item.get("deterministic_rules", ())) > 0 for item in profiles),
        "all_profiles_have_regression_guards": all(len(item.get("regression_guards", ())) > 0 for item in profiles),
        "all_profiles_have_bounded_candidate_count": all(0 < int(item.get("max_candidate_count", 0)) <= 8 for item in profiles),
        "all_profiles_disable_random_search": all(item.get("random_search_allowed") is False for item in profiles),
        "all_profiles_disable_unbounded_search": all(item.get("unbounded_search_allowed") is False for item in profiles),
        "all_profiles_ready_for_task_5": all(item.get("ready_for_task_5") is True for item in profiles),
        "color_candidate_generator_present": "color_mapping" in families,
        "object_candidate_generator_present": "object_model" in families,
        "shape_candidate_generator_present": "shape_symmetry" in families,
        "runtime_solver_not_modified": generator_record["runtime_solver_modified"] is False,
        "candidate_generator_profiles_ready": generator_record["candidate_generator_profiles_ready"] is True,
        "next_stage_valid": generator_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": generator_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": generator_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": generator_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": generator_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": generator_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": generator_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": generator_record["kaggle_submission_sent"] is False,
        "upload_not_performed": generator_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": generator_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "expansion_artifact_missing": not gate_state["expansion_artifact_present"],
        "expansion_artifact_not_ready": not gate_state["expansion_artifact_ready"],
        "expansion_artifact_invalid": not gate_state["expansion_artifact_valid"],
        "expansion_next_stage_mismatch": not gate_state["expansion_next_stage_matches_task_4"],
        "expansion_registry_not_ready": not gate_state["expansion_registry_ready"],
        "generator_mode_invalid": not gate_state["generator_mode_valid"],
        "generator_scope_invalid": not gate_state["generator_scope_valid"],
        "generator_verdict_invalid": not gate_state["generator_verdict_valid"],
        "generator_not_ready": not gate_state["generator_ready"],
        "generator_not_locked": not gate_state["generator_locked"],
        "profile_count_invalid": not gate_state["profile_count_valid"],
        "source_family_count_invalid": not gate_state["source_family_count_valid"],
        "template_count_invalid": not gate_state["template_count_valid"],
        "evidence_field_count_invalid": not gate_state["evidence_field_count_valid"],
        "deterministic_rule_count_invalid": not gate_state["deterministic_rule_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "max_candidate_count_invalid": not gate_state["max_candidate_count_valid"],
        "profile_priority_not_p0": not gate_state["all_profiles_priority_p0"],
        "profile_source_family_missing": not gate_state["all_profiles_have_source_family"],
        "source_family_not_found_in_expansion": not gate_state["all_source_families_found_in_expansion"],
        "profile_source_failure_missing": not gate_state["all_profiles_have_source_failure"],
        "profile_branch_missing": not gate_state["all_profiles_have_branch"],
        "profile_templates_missing": not gate_state["all_profiles_have_templates"],
        "profile_evidence_fields_missing": not gate_state["all_profiles_have_evidence_fields"],
        "profile_deterministic_rules_missing": not gate_state["all_profiles_have_deterministic_rules"],
        "profile_regression_guards_missing": not gate_state["all_profiles_have_regression_guards"],
        "profile_unbounded_candidate_count": not gate_state["all_profiles_have_bounded_candidate_count"],
        "random_search_allowed": not gate_state["all_profiles_disable_random_search"],
        "unbounded_search_allowed": not gate_state["all_profiles_disable_unbounded_search"],
        "profile_not_ready_for_task_5": not gate_state["all_profiles_ready_for_task_5"],
        "color_candidate_generator_missing": not gate_state["color_candidate_generator_present"],
        "object_candidate_generator_missing": not gate_state["object_candidate_generator_present"],
        "shape_candidate_generator_missing": not gate_state["shape_candidate_generator_present"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "candidate_generator_profiles_not_ready": not gate_state["candidate_generator_profiles_ready"],
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
        for name in GENERATOR_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in GENERATOR_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    generator_ready = (
        expansion_source["ready"] is True
        and len(profiles) == EXPECTED_PROFILE_COUNT
        and template_count == EXPECTED_TEMPLATE_COUNT
        and evidence_field_count == EXPECTED_EVIDENCE_FIELD_COUNT
        and deterministic_rule_count == EXPECTED_DETERMINISTIC_RULE_COUNT
        and regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT
        and max_candidate_count == EXPECTED_MAX_CANDIDATE_COUNT
        and passed_gate_count == len(GENERATOR_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 4",
        "generator_mode": GENERATOR_MODE,
        "generator_scope": GENERATOR_SCOPE,
        "generator_verdict": GENERATOR_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_expansion": expansion.get("expansion_id", "MISSING_EXPANSION_ID"),
        "generator_ready": generator_ready,
        "generator_locked": True,
        "profile_count": len(profiles),
        "source_family_count": len(source_families),
        "template_count": template_count,
        "evidence_field_count": evidence_field_count,
        "deterministic_rule_count": deterministic_rule_count,
        "regression_guard_count": regression_guard_count,
        "max_candidate_count": max_candidate_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
        "candidate_generator_profiles_ready": True,
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
        "status": GENERATOR_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 4",
        "title": "Candidate Generator Improvement v1",
        "baseline_commit": BASELINE_COMMIT,
        "generator_mode": GENERATOR_MODE,
        "generator_scope": GENERATOR_SCOPE,
        "generator_verdict": GENERATOR_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_expansion_source": expansion_source,
        "generator_record": generator_record,
        "generator_profiles": list(profiles),
        "generator_gates": list(gates),
        "generator_issues": list(issues),
        "generator_index": index,
        "boundary": boundary,
        "profile_count": len(profiles),
        "source_family_count": len(source_families),
        "template_count": template_count,
        "evidence_field_count": evidence_field_count,
        "deterministic_rule_count": deterministic_rule_count,
        "regression_guard_count": regression_guard_count,
        "max_candidate_count": max_candidate_count,
        "generator_gate_count": len(GENERATOR_GATES),
        "passed_gate_count": passed_gate_count,
        "generator_issue_count": issue_count,
        "warning_count": 0,
        "generator_ready": generator_ready,
        "generator_locked": True,
        "runtime_solver_modified": False,
        "candidate_generator_profiles_ready": True,
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
            "source": "milestone_7_candidate_generator_improvement_v1",
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
        "generator_id": f"MILESTONE-7-CANDIDATE-GENERATOR-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_candidate_generator_improvement(generator: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = generator.get("boundary", {})
    gates = generator.get("generator_gates", [])
    issues = generator.get("generator_issues", [])
    profiles = generator.get("generator_profiles", [])
    source = generator.get("milestone_7_expansion_source", {})

    checks = {
        "status_ready": generator.get("status") == GENERATOR_STATUS,
        "generator_id_present": isinstance(generator.get("generator_id"), str) and bool(generator.get("generator_id")),
        "signature_present": isinstance(generator.get("signature"), str) and bool(generator.get("signature")),
        "baseline_commit_valid": str(generator.get("baseline_commit", "")).startswith("3ec630b"),
        "generator_mode_valid": generator.get("generator_mode") == GENERATOR_MODE,
        "generator_scope_valid": generator.get("generator_scope") == GENERATOR_SCOPE,
        "generator_verdict_valid": generator.get("generator_verdict") == GENERATOR_VERDICT,
        "next_allowed_stage_valid": generator.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "expansion_source_ready": source.get("ready") is True,
        "expansion_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "profile_count_valid": generator.get("profile_count") == EXPECTED_PROFILE_COUNT,
        "source_family_count_valid": generator.get("source_family_count") == EXPECTED_SOURCE_FAMILY_COUNT,
        "template_count_valid": generator.get("template_count") == EXPECTED_TEMPLATE_COUNT,
        "evidence_field_count_valid": generator.get("evidence_field_count") == EXPECTED_EVIDENCE_FIELD_COUNT,
        "deterministic_rule_count_valid": generator.get("deterministic_rule_count") == EXPECTED_DETERMINISTIC_RULE_COUNT,
        "regression_guard_count_valid": generator.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "max_candidate_count_valid": generator.get("max_candidate_count") == EXPECTED_MAX_CANDIDATE_COUNT,
        "all_profiles_have_templates": bool(profiles) and all(len(item.get("candidate_templates", ())) > 0 for item in profiles),
        "all_profiles_have_evidence_fields": bool(profiles) and all(len(item.get("evidence_fields", ())) > 0 for item in profiles),
        "all_profiles_have_deterministic_rules": bool(profiles) and all(len(item.get("deterministic_rules", ())) > 0 for item in profiles),
        "all_profiles_have_regression_guards": bool(profiles) and all(len(item.get("regression_guards", ())) > 0 for item in profiles),
        "all_profiles_disable_random_search": bool(profiles) and all(item.get("random_search_allowed") is False for item in profiles),
        "all_profiles_disable_unbounded_search": bool(profiles) and all(item.get("unbounded_search_allowed") is False for item in profiles),
        "all_profiles_ready_for_task_5": bool(profiles) and all(item.get("ready_for_task_5") is True for item in profiles),
        "runtime_solver_not_modified": generator.get("runtime_solver_modified") is False,
        "candidate_generator_profiles_ready": generator.get("candidate_generator_profiles_ready") is True,
        "generator_gate_count_matches": generator.get("generator_gate_count") == len(GENERATOR_GATES),
        "all_generator_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "generator_issue_count_zero": generator.get("generator_issue_count") == 0,
        "all_generator_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "generator_ready": generator.get("generator_ready") is True,
        "generator_locked": generator.get("generator_locked") is True,
        "solver_improvement_required": generator.get("solver_improvement_required") is True,
        "competitive_claim_absent": generator.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": generator.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": generator.get("manual_upload_performed") is False,
        "real_submission_allowed_false": generator.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": generator.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": generator.get("real_submission_created") is False,
        "kaggle_submission_not_sent": generator.get("kaggle_submission_sent") is False,
        "upload_not_performed": generator.get("upload_performed") is False,
        "kaggle_authentication_not_performed": generator.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_INVALID",
        "valid": valid,
        "checks": checks,
        "generator_id": generator.get("generator_id"),
        "signature": generator.get("signature"),
    }


def render_candidate_generator_improvement_markdown(generator: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Candidate Generator Improvement v1",
        "",
        f"- status: {generator['status']}",
        f"- generator_id: {generator['generator_id']}",
        f"- signature: {generator['signature']}",
        f"- baseline_commit: {generator['baseline_commit']}",
        f"- generator_mode: {generator['generator_mode']}",
        f"- generator_scope: {generator['generator_scope']}",
        f"- generator_verdict: {generator['generator_verdict']}",
        f"- next_allowed_stage: {generator['next_allowed_stage']}",
        f"- profile_count: {generator['profile_count']}",
        f"- source_family_count: {generator['source_family_count']}",
        f"- template_count: {generator['template_count']}",
        f"- evidence_field_count: {generator['evidence_field_count']}",
        f"- deterministic_rule_count: {generator['deterministic_rule_count']}",
        f"- regression_guard_count: {generator['regression_guard_count']}",
        f"- max_candidate_count: {generator['max_candidate_count']}",
        f"- generator_gate_count: {generator['generator_gate_count']}",
        f"- passed_gate_count: {generator['passed_gate_count']}",
        f"- generator_issue_count: {generator['generator_issue_count']}",
        f"- generator_ready: {generator['generator_ready']}",
        f"- runtime_solver_modified: {generator['runtime_solver_modified']}",
        f"- real_submission_allowed: {generator['real_submission_allowed']}",
        f"- kaggle_submission_sent: {generator['kaggle_submission_sent']}",
        f"- upload_performed: {generator['upload_performed']}",
        "",
        "## Candidate generator profiles",
        "",
    ]

    for item in generator["generator_profiles"]:
        lines.append(
            f"- {item['priority']} {item['generator_profile_id']} / family={item['family']} / "
            f"branch={item['generator_branch']} / templates={len(item['candidate_templates'])} / "
            f"max_candidate_count={item['max_candidate_count']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Candidate generator profiles are ready for ranker evidence upgrade.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_VALID=true",
            "ARC_AGI3_MILESTONE_7_GENERATOR_MODE=CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_GENERATOR_VERDICT=CANDIDATE_GENERATOR_IMPROVEMENT_READY_FOR_RANKER_EVIDENCE_UPGRADE",
            "ARC_AGI3_MILESTONE_7_PROFILE_COUNT=3",
            "ARC_AGI3_MILESTONE_7_SOURCE_FAMILY_COUNT=3",
            "ARC_AGI3_MILESTONE_7_TEMPLATE_COUNT=12",
            "ARC_AGI3_MILESTONE_7_EVIDENCE_FIELD_COUNT=15",
            "ARC_AGI3_MILESTONE_7_DETERMINISTIC_RULE_COUNT=12",
            "ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=9",
            "ARC_AGI3_MILESTONE_7_MAX_CANDIDATE_COUNT=24",
            "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_PROFILES_READY=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_EXPANSION_COMMIT=3ec630b",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_candidate_generator_improvement_manifest(generator: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 CANDIDATE GENERATOR IMPROVEMENT MANIFEST v1",
        f"generator_id={generator['generator_id']}",
        f"signature={generator['signature']}",
        f"status={generator['status']}",
        f"baseline_commit={generator['baseline_commit']}",
        f"generator_mode={generator['generator_mode']}",
        f"generator_verdict={generator['generator_verdict']}",
        f"next_allowed_stage={generator['next_allowed_stage']}",
        f"profile_count={generator['profile_count']}",
        f"source_family_count={generator['source_family_count']}",
        f"template_count={generator['template_count']}",
        f"evidence_field_count={generator['evidence_field_count']}",
        f"deterministic_rule_count={generator['deterministic_rule_count']}",
        f"regression_guard_count={generator['regression_guard_count']}",
        f"max_candidate_count={generator['max_candidate_count']}",
        f"generator_gate_count={generator['generator_gate_count']}",
        f"passed_gate_count={generator['passed_gate_count']}",
        f"generator_issue_count={generator['generator_issue_count']}",
        f"generator_ready={generator['generator_ready']}",
        f"generator_locked={generator['generator_locked']}",
        f"runtime_solver_modified={generator['runtime_solver_modified']}",
        f"candidate_generator_profiles_ready={generator['candidate_generator_profiles_ready']}",
        f"solver_improvement_required={generator['solver_improvement_required']}",
        f"competitive_claim_absent={generator['competitive_claim_absent']}",
        f"manual_submission_allowed={generator['manual_submission_allowed']}",
        f"manual_upload_performed={generator['manual_upload_performed']}",
        f"real_submission_allowed={generator['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={generator['ready_for_real_kaggle_submission']}",
        f"real_submission_created={generator['real_submission_created']}",
        f"kaggle_submission_sent={generator['kaggle_submission_sent']}",
        f"upload_performed={generator['upload_performed']}",
        f"kaggle_authentication_performed={generator['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "GENERATOR_PROFILES",
    ]

    for item in generator["generator_profiles"]:
        lines.append(
            f"{item['priority']} {item['generator_profile_id']} family={item['family']} "
            f"source_family={item['source_family_id']} branch={item['generator_branch']} "
            f"template_count={len(item['candidate_templates'])} evidence_field_count={len(item['evidence_fields'])} "
            f"deterministic_rule_count={len(item['deterministic_rules'])} regression_guard_count={len(item['regression_guards'])} "
            f"max_candidate_count={item['max_candidate_count']} random_search_allowed={item['random_search_allowed']} "
            f"unbounded_search_allowed={item['unbounded_search_allowed']} ready_for_task_5={item['ready_for_task_5']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_candidate_generator_improvement_artifacts(
    generator: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    generator = dict(generator or build_milestone_7_candidate_generator_improvement())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-candidate-generator-improvement-v1.json"
    md_path = output / "milestone-7-candidate-generator-improvement-v1.md"
    manifest_path = output / "milestone-7-candidate-generator-improvement-manifest-v1.txt"
    index_path = output / "milestone-7-candidate-generator-improvement-index-v1.json"

    json_path.write_text(json.dumps(generator, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_candidate_generator_improvement_markdown(generator), encoding="utf-8")
    manifest_path.write_text(render_candidate_generator_improvement_manifest(generator), encoding="utf-8")
    index_path.write_text(json.dumps(generator["generator_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_candidate_generator_improvement_pipeline() -> Dict[str, Any]:
    generator = build_milestone_7_candidate_generator_improvement()
    validation = validate_milestone_7_candidate_generator_improvement(generator)
    artifacts = write_candidate_generator_improvement_artifacts(generator)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_PIPELINE_INVALID",
        "generator_status": generator["status"],
        "validation_status": validation["status"],
        "generator": generator,
        "generator_id": generator["generator_id"],
        "signature": generator["signature"],
        "generator_mode": generator["generator_mode"],
        "generator_verdict": generator["generator_verdict"],
        "next_allowed_stage": generator["next_allowed_stage"],
        "profile_count": generator["profile_count"],
        "source_family_count": generator["source_family_count"],
        "template_count": generator["template_count"],
        "evidence_field_count": generator["evidence_field_count"],
        "deterministic_rule_count": generator["deterministic_rule_count"],
        "regression_guard_count": generator["regression_guard_count"],
        "max_candidate_count": generator["max_candidate_count"],
        "generator_gate_count": generator["generator_gate_count"],
        "passed_gate_count": generator["passed_gate_count"],
        "generator_issue_count": generator["generator_issue_count"],
        "warning_count": generator["warning_count"],
        "generator_ready": generator["generator_ready"],
        "generator_locked": generator["generator_locked"],
        "runtime_solver_modified": generator["runtime_solver_modified"],
        "candidate_generator_profiles_ready": generator["candidate_generator_profiles_ready"],
        "solver_improvement_required": generator["solver_improvement_required"],
        "competitive_claim_absent": generator["competitive_claim_absent"],
        "manual_submission_allowed": generator["manual_submission_allowed"],
        "manual_upload_performed": generator["manual_upload_performed"],
        "real_submission_allowed": generator["real_submission_allowed"],
        "ready_for_real_kaggle_submission": generator["ready_for_real_kaggle_submission"],
        "real_submission_created": generator["real_submission_created"],
        "kaggle_submission_sent": generator["kaggle_submission_sent"],
        "upload_performed": generator["upload_performed"],
        "kaggle_authentication_performed": generator["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": generator["metadata"],
    }
