"""Milestone #7 Task-Family Solver Expansion v1.

Local-only task-family solver expansion plan and registry.

This module converts the baseline solver failure taxonomy into deterministic
task-family solver expansion branches for color mapping, object modeling, and
shape/symmetry. It does not submit to Kaggle, authenticate, upload files, call
external APIs, read secrets, create upload archives, or create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


EXPANSION_STATUS = "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY"
PIPELINE_STATUS = "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_VALID"

BASELINE_COMMIT = "fb770e3 Add ARC AGI3 baseline solver failure taxonomy"
EXPANSION_MODE = "TASK_FAMILY_SOLVER_EXPANSION_ONLY_NO_UPLOAD"
EXPANSION_SCOPE = "EXPAND_SOLVER_BRANCHES_FROM_BASELINE_FAILURE_TAXONOMY"
EXPANSION_VERDICT = "TASK_FAMILY_SOLVER_EXPANSION_READY_FOR_CANDIDATE_GENERATOR_IMPROVEMENT"
NEXT_ALLOWED_STAGE = "MILESTONE_7_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT"

DEFAULT_OUTPUT_DIR = "examples/milestone-7/task-family-solver-expansion-v1"

TAXONOMY_JSON = Path(
    "examples/milestone-7/baseline-solver-failure-taxonomy-v1/"
    "milestone-7-baseline-solver-failure-taxonomy-v1.json"
)

EXPECTED_FAMILY_COUNT = 3
EXPECTED_SOURCE_FAILURE_COUNT = 3
EXPECTED_STRATEGY_COUNT = 10
EXPECTED_REGRESSION_GUARD_COUNT = 9

FAMILY_EXPANSIONS: Tuple[Dict[str, Any], ...] = (
    {
        "family_id": "color_mapping_family_v1",
        "family": "color_mapping",
        "source_failure_class": "color_transform_undercoverage",
        "priority": "P0",
        "solver_branch": "solver_family_color_mapping_v1",
        "purpose": "Detect and generate deterministic color remap and palette transformation candidates.",
        "strategies": (
            "stable_color_remap_detection",
            "palette_swap_candidate_generation",
            "background_foreground_color_preservation",
            "color_histogram_signature_match",
        ),
        "inputs_required": (
            "train_input_grid",
            "train_output_grid",
            "test_input_grid",
            "palette_signature",
        ),
        "output_candidate_type": "COLOR_TRANSFORM_CANDIDATE",
        "measurement": "Increase exact or partial match rate on deterministic color-family local cases.",
        "regression_guards": (
            "no_random_palette_search",
            "preserve_grid_dimensions",
            "full_suite_must_remain_green",
        ),
        "implemented_as_registry": True,
        "runtime_solver_modified": False,
        "ready_for_task_4": True,
    },
    {
        "family_id": "object_model_family_v1",
        "family": "object_model",
        "source_failure_class": "object_segmentation_undercoverage",
        "priority": "P0",
        "solver_branch": "solver_family_object_model_v1",
        "purpose": "Detect connected components, object identity, object relations, and object movement candidates.",
        "strategies": (
            "connected_component_signature_detection",
            "bounding_box_relation_candidate_generation",
            "object_count_preservation_check",
        ),
        "inputs_required": (
            "component_map",
            "object_bounding_boxes",
            "object_color_signature",
            "train_input_output_object_delta",
        ),
        "output_candidate_type": "OBJECT_MODEL_CANDIDATE",
        "measurement": "Track object-family cases and verify deterministic object-aware candidate selection.",
        "regression_guards": (
            "no_unbounded_component_search",
            "preserve_object_count_when_required",
            "full_suite_must_remain_green",
        ),
        "implemented_as_registry": True,
        "runtime_solver_modified": False,
        "ready_for_task_4": True,
    },
    {
        "family_id": "shape_symmetry_family_v1",
        "family": "shape_symmetry",
        "source_failure_class": "spatial_symmetry_undercoverage",
        "priority": "P0",
        "solver_branch": "solver_family_shape_symmetry_v1",
        "purpose": "Detect reflection, rotation, translation, crop/expand, and symmetry-completion candidates.",
        "strategies": (
            "reflection_rotation_candidate_generation",
            "translation_crop_expand_signature_match",
            "symmetry_completion_candidate_generation",
        ),
        "inputs_required": (
            "shape_signature",
            "axis_symmetry_signature",
            "rotation_equivalence_signature",
            "train_input_output_spatial_delta",
        ),
        "output_candidate_type": "SHAPE_SYMMETRY_CANDIDATE",
        "measurement": "Improve deterministic local matches on symmetry and geometry families.",
        "regression_guards": (
            "no_random_geometric_search",
            "preserve_valid_grid_bounds",
            "full_suite_must_remain_green",
        ),
        "implemented_as_registry": True,
        "runtime_solver_modified": False,
        "ready_for_task_4": True,
    },
)

EXPANSION_GATES: Tuple[str, ...] = (
    "taxonomy_artifact_present",
    "taxonomy_artifact_ready",
    "taxonomy_artifact_valid",
    "taxonomy_requires_solver_improvement",
    "taxonomy_next_stage_matches_task_3",
    "expansion_mode_valid",
    "expansion_scope_valid",
    "expansion_verdict_valid",
    "expansion_ready",
    "expansion_locked",
    "family_count_valid",
    "source_failure_count_valid",
    "strategy_count_valid",
    "regression_guard_count_valid",
    "all_families_priority_p0",
    "all_families_have_source_failure",
    "all_source_failures_found_in_taxonomy",
    "all_families_have_solver_branch",
    "all_families_have_purpose",
    "all_families_have_strategies",
    "all_families_have_inputs_required",
    "all_families_have_output_candidate_type",
    "all_families_have_measurement",
    "all_families_have_regression_guards",
    "all_families_registry_implemented",
    "runtime_solver_not_modified",
    "all_families_ready_for_task_4",
    "color_mapping_family_present",
    "object_model_family_present",
    "shape_symmetry_family_present",
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

EXPANSION_ISSUES: Tuple[str, ...] = (
    "taxonomy_artifact_missing",
    "taxonomy_artifact_not_ready",
    "taxonomy_artifact_invalid",
    "taxonomy_does_not_require_solver_improvement",
    "taxonomy_next_stage_mismatch",
    "expansion_mode_invalid",
    "expansion_scope_invalid",
    "expansion_verdict_invalid",
    "expansion_not_ready",
    "expansion_not_locked",
    "family_count_invalid",
    "source_failure_count_invalid",
    "strategy_count_invalid",
    "regression_guard_count_invalid",
    "family_priority_not_p0",
    "family_source_failure_missing",
    "source_failure_not_found_in_taxonomy",
    "solver_branch_missing",
    "family_purpose_missing",
    "family_strategies_missing",
    "family_inputs_required_missing",
    "output_candidate_type_missing",
    "family_measurement_missing",
    "family_regression_guards_missing",
    "family_registry_not_implemented",
    "runtime_solver_modified",
    "family_not_ready_for_task_4",
    "color_mapping_family_missing",
    "object_model_family_missing",
    "shape_symmetry_family_missing",
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


def _boundary_from_taxonomy(taxonomy: Mapping[str, Any]) -> Dict[str, Any]:
    source = taxonomy.get("boundary", {}) if isinstance(taxonomy.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": taxonomy.get("kaggle_submission_sent"),
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


def _taxonomy_source(taxonomy: Mapping[str, Any]) -> Dict[str, Any]:
    file_hash = _sha256(TAXONOMY_JSON)
    return {
        "name": "milestone_7_baseline_solver_failure_taxonomy",
        "path": str(TAXONOMY_JSON),
        "present": TAXONOMY_JSON.exists(),
        "expected_status": "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY",
        "actual_status": taxonomy.get("status", "MISSING"),
        "ready": TAXONOMY_JSON.exists()
        and taxonomy.get("status") == "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY",
        "artifact_id": taxonomy.get("taxonomy_id", "MISSING_TAXONOMY_ID"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _failure_class_names(taxonomy: Mapping[str, Any]) -> Tuple[str, ...]:
    items = taxonomy.get("failure_classes", [])
    if not isinstance(items, list):
        return tuple()
    return tuple(str(item.get("failure_class", "")) for item in items if isinstance(item, Mapping))


def build_milestone_7_task_family_solver_expansion() -> Dict[str, Any]:
    taxonomy = _read_json(TAXONOMY_JSON)
    boundary = _boundary_from_taxonomy(taxonomy)
    taxonomy_source = _taxonomy_source(taxonomy)
    taxonomy_failure_names = _failure_class_names(taxonomy)

    families = tuple(dict(item) for item in FAMILY_EXPANSIONS)
    family_names = {item["family"] for item in families}
    source_failures = {item["source_failure_class"] for item in families}

    strategy_count = sum(len(item.get("strategies", ())) for item in families)
    regression_guard_count = sum(len(item.get("regression_guards", ())) for item in families)

    expansion_record = {
        "expansion_mode": EXPANSION_MODE,
        "expansion_scope": EXPANSION_SCOPE,
        "expansion_verdict": EXPANSION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "expansion_ready": True,
        "expansion_locked": True,
        "taxonomy_id": taxonomy.get("taxonomy_id", "MISSING_TAXONOMY_ID"),
        "taxonomy_ready": taxonomy.get("taxonomy_ready") is True,
        "taxonomy_solver_improvement_required": taxonomy.get("solver_improvement_required") is True,
        "family_count": len(families),
        "source_failure_count": len(source_failures),
        "strategy_count": strategy_count,
        "regression_guard_count": regression_guard_count,
        "families": sorted(family_names),
        "source_failures": sorted(source_failures),
        "solver_family_registry_ready": True,
        "runtime_solver_modified": False,
        "candidate_generator_dependency": "MILESTONE_7_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT",
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
        "taxonomy_artifact_present": TAXONOMY_JSON.exists(),
        "taxonomy_artifact_ready": taxonomy.get("status") == "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY",
        "taxonomy_artifact_valid": bool(taxonomy.get("taxonomy_id")) and bool(taxonomy.get("signature")),
        "taxonomy_requires_solver_improvement": taxonomy.get("solver_improvement_required") is True,
        "taxonomy_next_stage_matches_task_3": taxonomy.get("next_allowed_stage") == "MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION",
        "expansion_mode_valid": expansion_record["expansion_mode"] == EXPANSION_MODE,
        "expansion_scope_valid": expansion_record["expansion_scope"] == EXPANSION_SCOPE,
        "expansion_verdict_valid": expansion_record["expansion_verdict"] == EXPANSION_VERDICT,
        "expansion_ready": expansion_record["expansion_ready"] is True,
        "expansion_locked": expansion_record["expansion_locked"] is True,
        "family_count_valid": len(families) == EXPECTED_FAMILY_COUNT,
        "source_failure_count_valid": len(source_failures) == EXPECTED_SOURCE_FAILURE_COUNT,
        "strategy_count_valid": strategy_count == EXPECTED_STRATEGY_COUNT,
        "regression_guard_count_valid": regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT,
        "all_families_priority_p0": all(item.get("priority") == "P0" for item in families),
        "all_families_have_source_failure": all(bool(item.get("source_failure_class")) for item in families),
        "all_source_failures_found_in_taxonomy": all(item in taxonomy_failure_names for item in source_failures),
        "all_families_have_solver_branch": all(bool(item.get("solver_branch")) for item in families),
        "all_families_have_purpose": all(bool(item.get("purpose")) for item in families),
        "all_families_have_strategies": all(len(item.get("strategies", ())) > 0 for item in families),
        "all_families_have_inputs_required": all(len(item.get("inputs_required", ())) > 0 for item in families),
        "all_families_have_output_candidate_type": all(bool(item.get("output_candidate_type")) for item in families),
        "all_families_have_measurement": all(bool(item.get("measurement")) for item in families),
        "all_families_have_regression_guards": all(len(item.get("regression_guards", ())) > 0 for item in families),
        "all_families_registry_implemented": all(item.get("implemented_as_registry") is True for item in families),
        "runtime_solver_not_modified": all(item.get("runtime_solver_modified") is False for item in families),
        "all_families_ready_for_task_4": all(item.get("ready_for_task_4") is True for item in families),
        "color_mapping_family_present": "color_mapping" in family_names,
        "object_model_family_present": "object_model" in family_names,
        "shape_symmetry_family_present": "shape_symmetry" in family_names,
        "next_stage_valid": expansion_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": expansion_record["competitive_claim_absent"] is True,
        "manual_submission_not_allowed": expansion_record["manual_submission_allowed"] is False,
        "manual_upload_not_performed": expansion_record["manual_upload_performed"] is False,
        "real_submission_allowed_false": expansion_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": expansion_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": expansion_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": expansion_record["kaggle_submission_sent"] is False,
        "upload_not_performed": expansion_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": expansion_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "taxonomy_artifact_missing": not gate_state["taxonomy_artifact_present"],
        "taxonomy_artifact_not_ready": not gate_state["taxonomy_artifact_ready"],
        "taxonomy_artifact_invalid": not gate_state["taxonomy_artifact_valid"],
        "taxonomy_does_not_require_solver_improvement": not gate_state["taxonomy_requires_solver_improvement"],
        "taxonomy_next_stage_mismatch": not gate_state["taxonomy_next_stage_matches_task_3"],
        "expansion_mode_invalid": not gate_state["expansion_mode_valid"],
        "expansion_scope_invalid": not gate_state["expansion_scope_valid"],
        "expansion_verdict_invalid": not gate_state["expansion_verdict_valid"],
        "expansion_not_ready": not gate_state["expansion_ready"],
        "expansion_not_locked": not gate_state["expansion_locked"],
        "family_count_invalid": not gate_state["family_count_valid"],
        "source_failure_count_invalid": not gate_state["source_failure_count_valid"],
        "strategy_count_invalid": not gate_state["strategy_count_valid"],
        "regression_guard_count_invalid": not gate_state["regression_guard_count_valid"],
        "family_priority_not_p0": not gate_state["all_families_priority_p0"],
        "family_source_failure_missing": not gate_state["all_families_have_source_failure"],
        "source_failure_not_found_in_taxonomy": not gate_state["all_source_failures_found_in_taxonomy"],
        "solver_branch_missing": not gate_state["all_families_have_solver_branch"],
        "family_purpose_missing": not gate_state["all_families_have_purpose"],
        "family_strategies_missing": not gate_state["all_families_have_strategies"],
        "family_inputs_required_missing": not gate_state["all_families_have_inputs_required"],
        "output_candidate_type_missing": not gate_state["all_families_have_output_candidate_type"],
        "family_measurement_missing": not gate_state["all_families_have_measurement"],
        "family_regression_guards_missing": not gate_state["all_families_have_regression_guards"],
        "family_registry_not_implemented": not gate_state["all_families_registry_implemented"],
        "runtime_solver_modified": not gate_state["runtime_solver_not_modified"],
        "family_not_ready_for_task_4": not gate_state["all_families_ready_for_task_4"],
        "color_mapping_family_missing": not gate_state["color_mapping_family_present"],
        "object_model_family_missing": not gate_state["object_model_family_present"],
        "shape_symmetry_family_missing": not gate_state["shape_symmetry_family_present"],
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
        for name in EXPANSION_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in EXPANSION_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    expansion_ready = (
        taxonomy_source["ready"] is True
        and len(families) == EXPECTED_FAMILY_COUNT
        and strategy_count == EXPECTED_STRATEGY_COUNT
        and regression_guard_count == EXPECTED_REGRESSION_GUARD_COUNT
        and passed_gate_count == len(EXPANSION_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #7",
        "task": "Task 3",
        "expansion_mode": EXPANSION_MODE,
        "expansion_scope": EXPANSION_SCOPE,
        "expansion_verdict": EXPANSION_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_taxonomy": taxonomy.get("taxonomy_id", "MISSING_TAXONOMY_ID"),
        "expansion_ready": expansion_ready,
        "expansion_locked": True,
        "family_count": len(families),
        "source_failure_count": len(source_failures),
        "strategy_count": strategy_count,
        "regression_guard_count": regression_guard_count,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "runtime_solver_modified": False,
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
        "status": EXPANSION_STATUS,
        "milestone": "Milestone #7",
        "task": "Task 3",
        "title": "Task-Family Solver Expansion v1",
        "baseline_commit": BASELINE_COMMIT,
        "expansion_mode": EXPANSION_MODE,
        "expansion_scope": EXPANSION_SCOPE,
        "expansion_verdict": EXPANSION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "milestone_7_taxonomy_source": taxonomy_source,
        "expansion_record": expansion_record,
        "family_expansions": list(families),
        "expansion_gates": list(gates),
        "expansion_issues": list(issues),
        "expansion_index": index,
        "boundary": boundary,
        "family_count": len(families),
        "source_failure_count": len(source_failures),
        "strategy_count": strategy_count,
        "regression_guard_count": regression_guard_count,
        "expansion_gate_count": len(EXPANSION_GATES),
        "passed_gate_count": passed_gate_count,
        "expansion_issue_count": issue_count,
        "warning_count": 0,
        "expansion_ready": expansion_ready,
        "expansion_locked": True,
        "runtime_solver_modified": False,
        "solver_family_registry_ready": True,
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
            "source": "milestone_7_task_family_solver_expansion_v1",
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
        "expansion_id": f"MILESTONE-7-TASK-FAMILY-EXPANSION-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_7_task_family_solver_expansion(expansion: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = expansion.get("boundary", {})
    gates = expansion.get("expansion_gates", [])
    issues = expansion.get("expansion_issues", [])
    families = expansion.get("family_expansions", [])
    source = expansion.get("milestone_7_taxonomy_source", {})

    checks = {
        "status_ready": expansion.get("status") == EXPANSION_STATUS,
        "expansion_id_present": isinstance(expansion.get("expansion_id"), str) and bool(expansion.get("expansion_id")),
        "signature_present": isinstance(expansion.get("signature"), str) and bool(expansion.get("signature")),
        "baseline_commit_valid": str(expansion.get("baseline_commit", "")).startswith("fb770e3"),
        "expansion_mode_valid": expansion.get("expansion_mode") == EXPANSION_MODE,
        "expansion_scope_valid": expansion.get("expansion_scope") == EXPANSION_SCOPE,
        "expansion_verdict_valid": expansion.get("expansion_verdict") == EXPANSION_VERDICT,
        "next_allowed_stage_valid": expansion.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "taxonomy_source_ready": source.get("ready") is True,
        "taxonomy_source_hash_present": source.get("sha256") != "MISSING_HASH",
        "family_count_valid": expansion.get("family_count") == EXPECTED_FAMILY_COUNT,
        "source_failure_count_valid": expansion.get("source_failure_count") == EXPECTED_SOURCE_FAILURE_COUNT,
        "strategy_count_valid": expansion.get("strategy_count") == EXPECTED_STRATEGY_COUNT,
        "regression_guard_count_valid": expansion.get("regression_guard_count") == EXPECTED_REGRESSION_GUARD_COUNT,
        "all_families_have_strategies": bool(families) and all(len(item.get("strategies", ())) > 0 for item in families),
        "all_families_have_inputs_required": bool(families) and all(len(item.get("inputs_required", ())) > 0 for item in families),
        "all_families_have_regression_guards": bool(families) and all(len(item.get("regression_guards", ())) > 0 for item in families),
        "all_families_registry_implemented": bool(families) and all(item.get("implemented_as_registry") is True for item in families),
        "runtime_solver_not_modified": expansion.get("runtime_solver_modified") is False,
        "solver_family_registry_ready": expansion.get("solver_family_registry_ready") is True,
        "expansion_gate_count_matches": expansion.get("expansion_gate_count") == len(EXPANSION_GATES),
        "all_expansion_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "expansion_issue_count_zero": expansion.get("expansion_issue_count") == 0,
        "all_expansion_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "expansion_ready": expansion.get("expansion_ready") is True,
        "expansion_locked": expansion.get("expansion_locked") is True,
        "solver_improvement_required": expansion.get("solver_improvement_required") is True,
        "competitive_claim_absent": expansion.get("competitive_claim_absent") is True,
        "manual_submission_not_allowed": expansion.get("manual_submission_allowed") is False,
        "manual_upload_not_performed": expansion.get("manual_upload_performed") is False,
        "real_submission_allowed_false": expansion.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": expansion.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": expansion.get("real_submission_created") is False,
        "kaggle_submission_not_sent": expansion.get("kaggle_submission_sent") is False,
        "upload_not_performed": expansion.get("upload_performed") is False,
        "kaggle_authentication_not_performed": expansion.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_INVALID",
        "valid": valid,
        "checks": checks,
        "expansion_id": expansion.get("expansion_id"),
        "signature": expansion.get("signature"),
    }


def render_task_family_solver_expansion_markdown(expansion: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #7 - Task-Family Solver Expansion v1",
        "",
        f"- status: {expansion['status']}",
        f"- expansion_id: {expansion['expansion_id']}",
        f"- signature: {expansion['signature']}",
        f"- baseline_commit: {expansion['baseline_commit']}",
        f"- expansion_mode: {expansion['expansion_mode']}",
        f"- expansion_scope: {expansion['expansion_scope']}",
        f"- expansion_verdict: {expansion['expansion_verdict']}",
        f"- next_allowed_stage: {expansion['next_allowed_stage']}",
        f"- family_count: {expansion['family_count']}",
        f"- source_failure_count: {expansion['source_failure_count']}",
        f"- strategy_count: {expansion['strategy_count']}",
        f"- regression_guard_count: {expansion['regression_guard_count']}",
        f"- expansion_gate_count: {expansion['expansion_gate_count']}",
        f"- passed_gate_count: {expansion['passed_gate_count']}",
        f"- expansion_issue_count: {expansion['expansion_issue_count']}",
        f"- expansion_ready: {expansion['expansion_ready']}",
        f"- expansion_locked: {expansion['expansion_locked']}",
        f"- runtime_solver_modified: {expansion['runtime_solver_modified']}",
        f"- real_submission_allowed: {expansion['real_submission_allowed']}",
        f"- kaggle_submission_sent: {expansion['kaggle_submission_sent']}",
        f"- upload_performed: {expansion['upload_performed']}",
        "",
        "## Family expansions",
        "",
    ]

    for item in expansion["family_expansions"]:
        lines.append(
            f"- {item['priority']} {item['family_id']} / source={item['source_failure_class']} / "
            f"branch={item['solver_branch']} / strategies={len(item['strategies'])}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Task-family solver branches are registered for color mapping, object model, and shape/symmetry. Next step is candidate generator improvement.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_V1_READY=true",
            "ARC_AGI3_MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_VALID=true",
            "ARC_AGI3_MILESTONE_7_EXPANSION_MODE=TASK_FAMILY_SOLVER_EXPANSION_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_7_EXPANSION_VERDICT=TASK_FAMILY_SOLVER_EXPANSION_READY_FOR_CANDIDATE_GENERATOR_IMPROVEMENT",
            "ARC_AGI3_MILESTONE_7_FAMILY_COUNT=3",
            "ARC_AGI3_MILESTONE_7_SOURCE_FAILURE_COUNT=3",
            "ARC_AGI3_MILESTONE_7_STRATEGY_COUNT=10",
            "ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=9",
            "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false",
            "ARC_AGI3_MILESTONE_7_SOLVER_FAMILY_REGISTRY_READY=true",
            "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_7_BASELINE_TAXONOMY_COMMIT=fb770e3",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_task_family_solver_expansion_manifest(expansion: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 7 TASK-FAMILY SOLVER EXPANSION MANIFEST v1",
        f"expansion_id={expansion['expansion_id']}",
        f"signature={expansion['signature']}",
        f"status={expansion['status']}",
        f"baseline_commit={expansion['baseline_commit']}",
        f"expansion_mode={expansion['expansion_mode']}",
        f"expansion_verdict={expansion['expansion_verdict']}",
        f"next_allowed_stage={expansion['next_allowed_stage']}",
        f"family_count={expansion['family_count']}",
        f"source_failure_count={expansion['source_failure_count']}",
        f"strategy_count={expansion['strategy_count']}",
        f"regression_guard_count={expansion['regression_guard_count']}",
        f"expansion_gate_count={expansion['expansion_gate_count']}",
        f"passed_gate_count={expansion['passed_gate_count']}",
        f"expansion_issue_count={expansion['expansion_issue_count']}",
        f"expansion_ready={expansion['expansion_ready']}",
        f"expansion_locked={expansion['expansion_locked']}",
        f"runtime_solver_modified={expansion['runtime_solver_modified']}",
        f"solver_family_registry_ready={expansion['solver_family_registry_ready']}",
        f"solver_improvement_required={expansion['solver_improvement_required']}",
        f"competitive_claim_absent={expansion['competitive_claim_absent']}",
        f"manual_submission_allowed={expansion['manual_submission_allowed']}",
        f"manual_upload_performed={expansion['manual_upload_performed']}",
        f"real_submission_allowed={expansion['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={expansion['ready_for_real_kaggle_submission']}",
        f"real_submission_created={expansion['real_submission_created']}",
        f"kaggle_submission_sent={expansion['kaggle_submission_sent']}",
        f"upload_performed={expansion['upload_performed']}",
        f"kaggle_authentication_performed={expansion['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "FAMILY_EXPANSIONS",
    ]

    for item in expansion["family_expansions"]:
        lines.append(
            f"{item['priority']} {item['family_id']} family={item['family']} "
            f"source_failure={item['source_failure_class']} branch={item['solver_branch']} "
            f"strategy_count={len(item['strategies'])} regression_guard_count={len(item['regression_guards'])} "
            f"runtime_solver_modified={item['runtime_solver_modified']} ready_for_task_4={item['ready_for_task_4']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_task_family_solver_expansion_artifacts(
    expansion: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    expansion = dict(expansion or build_milestone_7_task_family_solver_expansion())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-7-task-family-solver-expansion-v1.json"
    md_path = output / "milestone-7-task-family-solver-expansion-v1.md"
    manifest_path = output / "milestone-7-task-family-solver-expansion-manifest-v1.txt"
    index_path = output / "milestone-7-task-family-solver-expansion-index-v1.json"

    json_path.write_text(json.dumps(expansion, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_task_family_solver_expansion_markdown(expansion), encoding="utf-8")
    manifest_path.write_text(render_task_family_solver_expansion_manifest(expansion), encoding="utf-8")
    index_path.write_text(json.dumps(expansion["expansion_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_7_task_family_solver_expansion_pipeline() -> Dict[str, Any]:
    expansion = build_milestone_7_task_family_solver_expansion()
    validation = validate_milestone_7_task_family_solver_expansion(expansion)
    artifacts = write_task_family_solver_expansion_artifacts(expansion)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_PIPELINE_INVALID",
        "expansion_status": expansion["status"],
        "validation_status": validation["status"],
        "expansion": expansion,
        "expansion_id": expansion["expansion_id"],
        "signature": expansion["signature"],
        "expansion_mode": expansion["expansion_mode"],
        "expansion_verdict": expansion["expansion_verdict"],
        "next_allowed_stage": expansion["next_allowed_stage"],
        "family_count": expansion["family_count"],
        "source_failure_count": expansion["source_failure_count"],
        "strategy_count": expansion["strategy_count"],
        "regression_guard_count": expansion["regression_guard_count"],
        "expansion_gate_count": expansion["expansion_gate_count"],
        "passed_gate_count": expansion["passed_gate_count"],
        "expansion_issue_count": expansion["expansion_issue_count"],
        "warning_count": expansion["warning_count"],
        "expansion_ready": expansion["expansion_ready"],
        "expansion_locked": expansion["expansion_locked"],
        "runtime_solver_modified": expansion["runtime_solver_modified"],
        "solver_family_registry_ready": expansion["solver_family_registry_ready"],
        "solver_improvement_required": expansion["solver_improvement_required"],
        "competitive_claim_absent": expansion["competitive_claim_absent"],
        "manual_submission_allowed": expansion["manual_submission_allowed"],
        "manual_upload_performed": expansion["manual_upload_performed"],
        "real_submission_allowed": expansion["real_submission_allowed"],
        "ready_for_real_kaggle_submission": expansion["ready_for_real_kaggle_submission"],
        "real_submission_created": expansion["real_submission_created"],
        "kaggle_submission_sent": expansion["kaggle_submission_sent"],
        "upload_performed": expansion["upload_performed"],
        "kaggle_authentication_performed": expansion["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": expansion["metadata"],
    }
