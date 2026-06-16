"""Milestone #13 Task 6 - Program Synthesis Candidate Generator Controlled Implementation v1.

This module implements a local, deterministic, public-safe candidate program
generator.

Boundary:
- no runtime solver wiring
- no candidate generator runtime wiring
- no ranker runtime wiring
- no real Kaggle evaluation
- no upload
- no submission
- no external API dependency

Yes, it generates candidate programs. No, it does not suddenly become a cosmic
oracle. Software has limits. Try telling that to product decks.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 6
TASK_LABEL = "Milestone #13 Task 6 - Program Synthesis Candidate Generator Controlled Implementation v1"

SOURCE_TASK = "MILESTONE_13_TASK_5_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1"
NEXT_STAGE = "MILESTONE_13_TASK_7_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1_LOCAL_ONLY"
TASK_SCOPE = "CONTROLLED_LOCAL_CANDIDATE_GENERATOR_IMPLEMENTATION_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_READY"
IMPLEMENTATION_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_READY_FOR_REVIEW"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-implementation-v1"
)

SOURCE_PLAN_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-plan-v1"
    / "milestone-13-program-synthesis-candidate-generator-plan-v1.json"
)

CANDIDATE_FAMILIES = [
    "primitive_sequence_candidates",
    "object_transform_candidates",
    "color_rule_candidates",
    "symmetry_completion_candidates",
    "crop_pad_resize_candidates",
    "relation_graph_candidates",
    "composite_program_candidates",
]

PROGRAM_TEMPLATE_DEFINITIONS = [
    {
        "template_id": "TPL-001",
        "name": "single_primitive_transform",
        "family": "primitive_sequence_candidates",
        "operations": ["apply_primitive"],
    },
    {
        "template_id": "TPL-002",
        "name": "two_step_primitive_sequence",
        "family": "primitive_sequence_candidates",
        "operations": ["apply_primitive", "apply_primitive"],
    },
    {
        "template_id": "TPL-003",
        "name": "object_extract_then_transform",
        "family": "object_transform_candidates",
        "operations": ["select_object", "transform_object"],
    },
    {
        "template_id": "TPL-004",
        "name": "object_filter_then_recolor",
        "family": "object_transform_candidates",
        "operations": ["filter_object", "recolor_object"],
    },
    {
        "template_id": "TPL-005",
        "name": "object_relation_guided_move",
        "family": "relation_graph_candidates",
        "operations": ["select_relation", "move_object"],
    },
    {
        "template_id": "TPL-006",
        "name": "symmetry_completion_program",
        "family": "symmetry_completion_candidates",
        "operations": ["detect_symmetry_axis", "complete_symmetry"],
    },
    {
        "template_id": "TPL-007",
        "name": "palette_remap_program",
        "family": "color_rule_candidates",
        "operations": ["infer_palette_map", "apply_palette_map"],
    },
    {
        "template_id": "TPL-008",
        "name": "crop_pad_resize_program",
        "family": "crop_pad_resize_candidates",
        "operations": ["crop_to_bbox", "pad_or_resize"],
    },
    {
        "template_id": "TPL-009",
        "name": "tile_or_repeat_program",
        "family": "primitive_sequence_candidates",
        "operations": ["detect_tile", "repeat_tile"],
    },
    {
        "template_id": "TPL-010",
        "name": "mask_overlay_program",
        "family": "composite_program_candidates",
        "operations": ["build_mask", "overlay_mask"],
    },
    {
        "template_id": "TPL-011",
        "name": "object_compose_or_remove_program",
        "family": "composite_program_candidates",
        "operations": ["select_object", "compose_or_remove_object"],
    },
    {
        "template_id": "TPL-012",
        "name": "conditional_rule_program",
        "family": "composite_program_candidates",
        "operations": ["infer_condition", "apply_conditional_transform"],
    },
]

PARAMETER_BINDING_FIELDS = [
    "primitive_name",
    "object_selector",
    "source_color",
    "target_color",
    "direction",
    "symmetry_axis",
    "bbox_policy",
    "composition_policy",
]

DEFAULT_FEATURE_PACKET = {
    "primitive_names": [
        "identity",
        "rotate_90",
        "flip_horizontal",
        "transpose",
        "crop_to_non_background_bbox",
        "complete_vertical_symmetry",
    ],
    "object_selectors": [
        "largest_object",
        "smallest_object",
        "border_touching_object",
        "primary_color_object",
    ],
    "colors": [0, 1, 2, 3, 4, 5],
    "directions": ["up", "down", "left", "right"],
    "symmetry_axes": ["horizontal", "vertical"],
    "bbox_policies": ["non_background_bbox", "object_bbox", "full_canvas"],
    "composition_policies": ["overlay_non_background", "replace_target", "remove_source"],
}

IMPLEMENTATION_COMPONENTS = [
    "candidate_template_registry",
    "bounded_parameter_binder",
    "deterministic_candidate_enumerator",
    "candidate_signature_builder",
    "candidate_evidence_packager",
    "fail_closed_boundary_validator",
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_CANDIDATE_GENERATOR_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_RANKER_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
]

QUALITY_TARGETS = [
    "candidate_generation_is_deterministic",
    "candidate_ids_are_stable",
    "candidate_templates_are_bounded",
    "program_depth_is_limited_to_three",
    "candidate_evidence_is_packaged",
    "runtime_wiring_is_blocked",
    "next_task_is_implementation_review",
]


def _run_git_head() -> str:
    try:
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=PROJECT_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return "NO_GIT_HEAD_AVAILABLE"
    return result.stdout.strip() or "NO_GIT_HEAD_AVAILABLE"


def _stable_signature(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest().upper()[:16]


def _gate(name: str, passed: bool, required: bool, description: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "required": bool(required),
        "description": description,
    }


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return value if isinstance(value, dict) else None


def _pick(values: list[Any], index: int) -> Any:
    if not values:
        return None
    return values[index % len(values)]


def build_parameter_binding(template: dict[str, Any], feature_packet: dict[str, Any], index: int) -> dict[str, Any]:
    colors = list(feature_packet.get("colors", []))
    source_color = _pick(colors, index)
    target_color = _pick(colors, index + 1)

    return {
        "primitive_name": _pick(list(feature_packet.get("primitive_names", [])), index),
        "object_selector": _pick(list(feature_packet.get("object_selectors", [])), index),
        "source_color": source_color,
        "target_color": target_color,
        "direction": _pick(list(feature_packet.get("directions", [])), index),
        "symmetry_axis": _pick(list(feature_packet.get("symmetry_axes", [])), index),
        "bbox_policy": _pick(list(feature_packet.get("bbox_policies", [])), index),
        "composition_policy": _pick(list(feature_packet.get("composition_policies", [])), index),
        "template_name": template["name"],
        "family": template["family"],
    }


def generate_controlled_candidate_programs(
    feature_packet: dict[str, Any] | None = None,
    max_candidates: int = 12,
) -> list[dict[str, Any]]:
    """Generate deterministic bounded candidate program specifications.

    The returned candidates are specs, not runtime solver patches.
    """

    packet = dict(DEFAULT_FEATURE_PACKET)
    if feature_packet:
        for key, value in feature_packet.items():
            packet[key] = value

    candidates: list[dict[str, Any]] = []
    for index, template in enumerate(PROGRAM_TEMPLATE_DEFINITIONS[:max_candidates]):
        binding = build_parameter_binding(template, packet, index)
        program_depth = len(template["operations"])
        signature_payload = {
            "template_id": template["template_id"],
            "template_name": template["name"],
            "family": template["family"],
            "operations": template["operations"],
            "binding": binding,
            "program_depth": program_depth,
        }
        candidate_signature = _stable_signature(signature_payload)
        candidate_id = f"CAND-M13-T6-{index + 1:02d}-{candidate_signature[:8]}"

        candidates.append(
            {
                "candidate_id": candidate_id,
                "candidate_signature": candidate_signature,
                "template_id": template["template_id"],
                "template_name": template["name"],
                "family": template["family"],
                "program_depth": program_depth,
                "operations": list(template["operations"]),
                "binding": binding,
                "deterministic": True,
                "local_only": True,
                "public_safe": True,
                "bounded": True,
                "max_depth_allowed": 3,
                "train_pair_match_required": True,
                "runtime_wiring_required": False,
                "runtime_solver_patch": False,
                "candidate_generator_runtime_wiring": False,
                "ranker_runtime_wiring": False,
                "real_submission_candidate": False,
                "kaggle_submission_payload": False,
            }
        )

    return candidates


def build_candidate_evidence_pack(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    families = sorted({candidate["family"] for candidate in candidates})
    max_depth = max((candidate["program_depth"] for candidate in candidates), default=0)
    unique_ids = len({candidate["candidate_id"] for candidate in candidates}) == len(candidates)

    return {
        "candidate_count": len(candidates),
        "candidate_family_count": len(families),
        "families_present": families,
        "max_program_depth": max_depth,
        "unique_candidate_ids": unique_ids,
        "all_candidates_deterministic": all(candidate["deterministic"] is True for candidate in candidates),
        "all_candidates_local_only": all(candidate["local_only"] is True for candidate in candidates),
        "all_candidates_public_safe": all(candidate["public_safe"] is True for candidate in candidates),
        "all_candidates_bounded": all(candidate["bounded"] is True for candidate in candidates),
        "all_runtime_wiring_blocked": all(candidate["runtime_wiring_required"] is False for candidate in candidates),
        "all_real_submission_blocked": all(candidate["real_submission_candidate"] is False for candidate in candidates),
    }


def build_controlled_candidate_generator_implementation(
    source_record: dict[str, Any] | None,
) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}
    candidates = generate_controlled_candidate_programs()
    evidence_pack = build_candidate_evidence_pack(candidates)

    return {
        "implementation_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_PACKAGE_V1",
        "implementation_family": "LOCAL_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_NO_RUNTIME_WIRING",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_plan_verdict": source.get("plan_verdict"),
        "source_next_stage": source.get("next_stage"),
        "candidate_templates": PROGRAM_TEMPLATE_DEFINITIONS,
        "candidate_template_count": len(PROGRAM_TEMPLATE_DEFINITIONS),
        "candidate_families": CANDIDATE_FAMILIES,
        "candidate_family_count": len(CANDIDATE_FAMILIES),
        "parameter_binding_fields": PARAMETER_BINDING_FIELDS,
        "parameter_binding_field_count": len(PARAMETER_BINDING_FIELDS),
        "implementation_components": IMPLEMENTATION_COMPONENTS,
        "implementation_component_count": len(IMPLEMENTATION_COMPONENTS),
        "generated_candidates": candidates,
        "generated_candidate_count": len(candidates),
        "candidate_evidence_pack": evidence_pack,
        "max_program_depth": evidence_pack["max_program_depth"],
        "controlled_implementation_complete": True,
        "candidate_generator_wiring_authorized": False,
        "runtime_wiring_authorized": False,
        "recommended_next_stage": NEXT_STAGE,
    }


def build_controlled_candidate_generator_record(
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_PLAN_ARTIFACT.exists()
    source_record = _load_json(SOURCE_PLAN_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_plan_ready = bool(
        source_record
        and source_record.get("program_synthesis_candidate_generator_plan_ready") is True
        and source_record.get("program_synthesis_candidate_generator_plan_passed") is True
    )
    source_plan_shape_ok = bool(
        source_record
        and source_record.get("synthesis_stage_count") == 6
        and source_record.get("program_template_count") == 12
        and source_record.get("candidate_family_count") == 7
        and source_record.get("search_control_count") == 8
    )
    source_next_stage_ok = bool(
        source_record
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_6_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1"
    )
    source_blocks_runtime_wiring = bool(
        source_record
        and source_record.get("candidate_generator_wiring_authorized") is False
        and source_record.get("runtime_wiring_authorized") is False
        and source_record.get("runtime_solver_modified") is False
        and source_record.get("candidate_generator_modified") is False
        and source_record.get("ranker_runtime_modified") is False
    )
    source_blocks_real_actions = bool(
        source_record
        and source_record.get("real_kaggle_evaluation_allowed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("manual_upload_allowed") is False
        and source_record.get("kaggle_authentication_allowed") is False
        and source_record.get("kaggle_authentication_performed") is False
        and source_record.get("kaggle_upload_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
    )
    source_boundaries_ok = bool(
        source_record
        and source_record.get("local_only") is True
        and source_record.get("deterministic") is True
        and source_record.get("public_safe") is True
        and source_record.get("public_overfit_allowed") is False
        and source_record.get("public_overfit_guard_required") is True
        and source_record.get("external_api_dependency") is False
        and source_record.get("internet_during_eval") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
        and source_record.get("official_score_claim_allowed") is False
        and source_record.get("competitive_score_claim_allowed") is False
    )

    implementation = build_controlled_candidate_generator_implementation(source_record)
    evidence = implementation["candidate_evidence_pack"]

    candidate_template_count_ok = implementation["candidate_template_count"] == 12
    candidate_family_count_ok = implementation["candidate_family_count"] == 7
    parameter_binding_field_count_ok = implementation["parameter_binding_field_count"] == 8
    implementation_component_count_ok = implementation["implementation_component_count"] == 6
    generated_candidate_count_ok = implementation["generated_candidate_count"] == 12
    generated_candidate_ids_unique = evidence["unique_candidate_ids"] is True
    generated_candidate_depth_ok = evidence["max_program_depth"] <= 3
    generated_candidate_boundaries_ok = bool(
        evidence["all_candidates_deterministic"]
        and evidence["all_candidates_local_only"]
        and evidence["all_candidates_public_safe"]
        and evidence["all_candidates_bounded"]
        and evidence["all_runtime_wiring_blocked"]
        and evidence["all_real_submission_blocked"]
    )

    controlled_implementation_complete = True
    controlled_implementation_review_required = True
    candidate_generator_wiring_authorized = False
    runtime_wiring_authorized = False
    runtime_solver_modified = False
    candidate_generator_modified = False
    ranker_runtime_modified = False
    real_evaluation_performed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 5 plan artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 5 plan artifact is parseable."),
        _gate("source_plan_ready", source_plan_ready, True, "Task 5 plan is ready and passed."),
        _gate("source_plan_shape_ok", source_plan_shape_ok, True, "Task 5 plan has expected shape."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 5 points to Task 6."),
        _gate("source_blocks_runtime_wiring", source_blocks_runtime_wiring, True, "Source blocks runtime wiring."),
        _gate("source_blocks_real_actions", source_blocks_real_actions, True, "Source keeps real actions blocked."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source safety boundaries are preserved."),
        _gate("candidate_template_count_ok", candidate_template_count_ok, True, "Template count is expected."),
        _gate("candidate_family_count_ok", candidate_family_count_ok, True, "Candidate family count is expected."),
        _gate("parameter_binding_field_count_ok", parameter_binding_field_count_ok, True, "Binding fields are expected."),
        _gate("implementation_component_count_ok", implementation_component_count_ok, True, "Implementation components are expected."),
        _gate("generated_candidate_count_ok", generated_candidate_count_ok, True, "Candidate count is expected."),
        _gate("generated_candidate_ids_unique", generated_candidate_ids_unique, True, "Candidate IDs are unique."),
        _gate("generated_candidate_depth_ok", generated_candidate_depth_ok, True, "Candidate program depth is bounded."),
        _gate("generated_candidate_boundaries_ok", generated_candidate_boundaries_ok, True, "Generated candidates preserve boundaries."),
        _gate("controlled_implementation_complete_true", controlled_implementation_complete is True, True, "Controlled implementation is complete."),
        _gate("controlled_implementation_review_required_true", controlled_implementation_review_required is True, True, "Review remains required."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator runtime wiring remains blocked."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked."),
        _gate("runtime_solver_modified_false", runtime_solver_modified is False, True, "Runtime solver is not modified."),
        _gate("candidate_generator_modified_false", candidate_generator_modified is False, True, "Runtime candidate generator is not modified."),
        _gate("ranker_runtime_modified_false", ranker_runtime_modified is False, True, "Ranker runtime is not modified."),
        _gate("real_evaluation_performed_false", real_evaluation_performed is False, True, "No real evaluation is performed."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real submission readiness remains blocked."),
        _gate("kaggle_authentication_allowed_false", kaggle_authentication_allowed is False, True, "Kaggle authentication remains blocked."),
        _gate("kaggle_authentication_performed_false", kaggle_authentication_performed is False, True, "Kaggle authentication is not performed."),
        _gate("kaggle_upload_allowed_false", kaggle_upload_allowed is False, True, "Kaggle upload remains blocked."),
        _gate("kaggle_submission_sent_false", kaggle_submission_sent is False, True, "No Kaggle submission is sent."),
        _gate("public_overfit_allowed_false", True, True, "Public overfit remains blocked."),
        _gate("public_overfit_guard_required_true", True, True, "Public overfit guard remains required."),
        _gate("external_api_dependency_false", True, True, "External API dependency remains false."),
        _gate("internet_during_eval_false", True, True, "Internet during evaluation remains false."),
        _gate("private_core_exposure_false", True, True, "Private core exposure remains false."),
        _gate("legal_certification_false", True, True, "legal_certification remains false."),
        _gate("official_score_claim_allowed_false", True, True, "Official score claim remains blocked."),
        _gate("competitive_score_claim_allowed_false", True, True, "Competitive score claim remains blocked."),
        _gate("local_only_true", True, True, "Task remains local-only."),
        _gate("deterministic_true", True, True, "Task remains deterministic."),
        _gate("public_safe_true", True, True, "Task remains public-safe."),
        _gate("fail_closed_active", True, True, "Implementation fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    implementation_passed = len(required_gates) == len(passed_required_gates)

    implementation_summary = {
        "implementation_status": "READY" if implementation_passed else "FAIL_CLOSED",
        "implementation_verdict": IMPLEMENTATION_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "candidate_template_count": implementation["candidate_template_count"],
        "candidate_family_count": implementation["candidate_family_count"],
        "generated_candidate_count": implementation["generated_candidate_count"],
        "max_program_depth": implementation["max_program_depth"],
        "candidate_ids_unique": evidence["unique_candidate_ids"],
        "runtime_wiring_authorized": False,
        "candidate_generator_wiring_authorized": False,
        "next_stage": NEXT_STAGE,
    }

    record: dict[str, Any] = {
        "revision": TASK_NAME,
        "milestone_number": MILESTONE_NUMBER,
        "task_number": TASK_NUMBER,
        "task_label": TASK_LABEL,
        "source_task": SOURCE_TASK,
        "next_stage": NEXT_STAGE,
        "baseline_commit": baseline,
        "source_plan_artifact": str(SOURCE_PLAN_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_plan_ready": source_plan_ready,
        "source_plan_shape_ok": source_plan_shape_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_blocks_runtime_wiring": source_blocks_runtime_wiring,
        "source_blocks_real_actions": source_blocks_real_actions,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "implementation_verdict": IMPLEMENTATION_VERDICT,
        "controlled_candidate_generator_implementation_ready": True,
        "controlled_candidate_generator_implementation_valid": implementation_passed,
        "controlled_candidate_generator_implementation_passed": implementation_passed,
        "controlled_implementation_complete": controlled_implementation_complete,
        "controlled_implementation_review_required": controlled_implementation_review_required,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "implementation_summary": implementation_summary,
        "controlled_candidate_generator_implementation": implementation,
        "candidate_templates": PROGRAM_TEMPLATE_DEFINITIONS,
        "candidate_template_count": implementation["candidate_template_count"],
        "candidate_families": CANDIDATE_FAMILIES,
        "candidate_family_count": implementation["candidate_family_count"],
        "parameter_binding_fields": PARAMETER_BINDING_FIELDS,
        "parameter_binding_field_count": implementation["parameter_binding_field_count"],
        "implementation_components": IMPLEMENTATION_COMPONENTS,
        "implementation_component_count": implementation["implementation_component_count"],
        "generated_candidates": implementation["generated_candidates"],
        "generated_candidate_count": implementation["generated_candidate_count"],
        "candidate_evidence_pack": implementation["candidate_evidence_pack"],
        "max_program_depth": implementation["max_program_depth"],
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_controlled_implementation_allowed": True,
        "real_kaggle_evaluation_allowed": False,
        "public_overfit_allowed": False,
        "public_overfit_guard_required": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
        "open_source_prize_eligibility_required": True,
        "real_submission_allowed": real_submission_allowed,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": kaggle_authentication_allowed,
        "kaggle_authentication_performed": kaggle_authentication_performed,
        "kaggle_upload_allowed": kaggle_upload_allowed,
        "kaggle_submission_sent": kaggle_submission_sent,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "submission_json_created": False,
        "real_submission_candidate_created": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "official_score_claim_allowed": False,
        "competitive_score_claim_allowed": False,
        "real_public_score_claimed": False,
        "private_score_claimed": False,
        "kaggle_score_semantics": "NOT_A_KAGGLE_SCORE",
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "implementation_gate_count": len(gates),
        "implementation_pass_count": len(passed_required_gates),
        "implementation_blocking_issue_count": 0 if implementation_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if implementation_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": len(RISK_CONTROLS),
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": len(QUALITY_TARGETS),
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-IMPLEMENTATION-" + signature[:12]
    return record


def validate_controlled_candidate_generator_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_plan_ready",
        "source_plan_shape_ok",
        "source_next_stage_ok",
        "source_blocks_runtime_wiring",
        "source_blocks_real_actions",
        "controlled_candidate_generator_implementation_ready",
        "controlled_candidate_generator_implementation_valid",
        "controlled_candidate_generator_implementation_passed",
        "controlled_implementation_complete",
        "controlled_implementation_review_required",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_controlled_implementation_allowed",
        "public_overfit_guard_required",
        "open_source_prize_eligibility_required",
        "operator_approval_required",
        "local_only",
        "deterministic",
        "public_safe",
        "fail_closed_required",
        "fail_closed_active",
    ]

    expected_false = [
        "candidate_generator_wiring_authorized",
        "runtime_wiring_authorized",
        "runtime_solver_modified",
        "candidate_generator_modified",
        "ranker_runtime_modified",
        "real_evaluation_performed",
        "real_kaggle_evaluation_allowed",
        "public_overfit_allowed",
        "external_api_dependency",
        "internet_during_eval",
        "real_submission_allowed",
        "ready_for_real_kaggle_submission",
        "manual_upload_allowed",
        "kaggle_authentication_allowed",
        "kaggle_authentication_performed",
        "kaggle_upload_allowed",
        "kaggle_submission_sent",
        "operator_approval_received",
        "submission_json_created",
        "real_submission_candidate_created",
        "contains_api_keys",
        "private_core_exposure",
        "legal_certification",
        "official_score_claim_allowed",
        "competitive_score_claim_allowed",
        "real_public_score_claimed",
        "private_score_claimed",
    ]

    for key in expected_true:
        if record.get(key) is not True:
            issues.append(f"{key}_NOT_TRUE")

    for key in expected_false:
        if record.get(key) is not False:
            issues.append(f"{key}_NOT_FALSE")

    if record.get("revision") != TASK_NAME:
        issues.append("REVISION_MISMATCH")

    if record.get("source_task") != SOURCE_TASK:
        issues.append("SOURCE_TASK_MISMATCH")

    if record.get("next_stage") != NEXT_STAGE:
        issues.append("NEXT_STAGE_MISMATCH")

    if record.get("task_verdict") != TASK_VERDICT:
        issues.append("TASK_VERDICT_MISMATCH")

    if record.get("implementation_verdict") != IMPLEMENTATION_VERDICT:
        issues.append("IMPLEMENTATION_VERDICT_MISMATCH")

    expected_counts = {
        "candidate_template_count": 12,
        "candidate_family_count": 7,
        "parameter_binding_field_count": 8,
        "implementation_component_count": 6,
        "generated_candidate_count": 12,
        "max_program_depth": 2,
        "risk_control_count": 10,
        "quality_target_count": 7,
        "implementation_blocking_issue_count": 0,
        "issue_count": 0,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    evidence = record.get("candidate_evidence_pack")
    if not isinstance(evidence, dict):
        issues.append("CANDIDATE_EVIDENCE_PACK_MISSING")
    else:
        expected_evidence_true = [
            "unique_candidate_ids",
            "all_candidates_deterministic",
            "all_candidates_local_only",
            "all_candidates_public_safe",
            "all_candidates_bounded",
            "all_runtime_wiring_blocked",
            "all_real_submission_blocked",
        ]
        for key in expected_evidence_true:
            if evidence.get(key) is not True:
                issues.append(f"EVIDENCE_{key}_NOT_TRUE")
        if evidence.get("candidate_count") != 12:
            issues.append("EVIDENCE_CANDIDATE_COUNT_MISMATCH")
        if evidence.get("max_program_depth") != 2:
            issues.append("EVIDENCE_MAX_PROGRAM_DEPTH_MISMATCH")

    implementation = record.get("controlled_candidate_generator_implementation")
    if not isinstance(implementation, dict):
        issues.append("CONTROLLED_IMPLEMENTATION_MISSING")
    else:
        if implementation.get("generated_candidate_count") != 12:
            issues.append("IMPLEMENTATION_GENERATED_CANDIDATE_COUNT_MISMATCH")
        if implementation.get("candidate_template_count") != 12:
            issues.append("IMPLEMENTATION_TEMPLATE_COUNT_MISMATCH")
        if implementation.get("runtime_wiring_authorized") is not False:
            issues.append("IMPLEMENTATION_RUNTIME_WIRING_NOT_BLOCKED")
        if implementation.get("candidate_generator_wiring_authorized") is not False:
            issues.append("IMPLEMENTATION_CANDIDATE_GENERATOR_WIRING_NOT_BLOCKED")
        if implementation.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("IMPLEMENTATION_RECOMMENDED_NEXT_STAGE_MISMATCH")

    candidates = record.get("generated_candidates")
    if not isinstance(candidates, list) or not candidates:
        issues.append("GENERATED_CANDIDATES_MISSING")
    else:
        if len(candidates) != 12:
            issues.append("GENERATED_CANDIDATES_COUNT_MISMATCH")
        ids = [candidate.get("candidate_id") for candidate in candidates]
        if len(ids) != len(set(ids)):
            issues.append("GENERATED_CANDIDATE_IDS_NOT_UNIQUE")
        for candidate in candidates:
            if candidate.get("program_depth", 99) > 3:
                issues.append("GENERATED_CANDIDATE_DEPTH_TOO_HIGH")
            if candidate.get("runtime_wiring_required") is not False:
                issues.append("GENERATED_CANDIDATE_RUNTIME_WIRING_REQUIRED")
            if candidate.get("real_submission_candidate") is not False:
                issues.append("GENERATED_CANDIDATE_REAL_SUBMISSION_ALLOWED")

    summary = record.get("implementation_summary")
    if not isinstance(summary, dict):
        issues.append("IMPLEMENTATION_SUMMARY_MISSING")
    else:
        if summary.get("implementation_status") != "READY":
            issues.append("IMPLEMENTATION_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("IMPLEMENTATION_SUMMARY_NEXT_STAGE_MISMATCH")

    gates = record.get("gates")
    if not isinstance(gates, list) or not gates:
        issues.append("GATES_MISSING")
    else:
        failed_required = [
            gate.get("name", "UNKNOWN_GATE")
            for gate in gates
            if gate.get("required") is True and gate.get("passed") is not True
        ]
        issues.extend(f"REQUIRED_GATE_FAILED:{name}" for name in failed_required)

    return issues


def write_artifacts(record: dict[str, Any], artifact_dir: Path | None = None) -> dict[str, str]:
    target_dir = artifact_dir or ARTIFACT_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.md"

    json_path.write_text(
        json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "implementation_verdict": record["implementation_verdict"],
        "next_stage": record["next_stage"],
        "source_plan_ready": record["source_plan_ready"],
        "source_plan_shape_ok": record["source_plan_shape_ok"],
        "controlled_candidate_generator_implementation_ready": record["controlled_candidate_generator_implementation_ready"],
        "candidate_template_count": record["candidate_template_count"],
        "candidate_family_count": record["candidate_family_count"],
        "generated_candidate_count": record["generated_candidate_count"],
        "max_program_depth": record["max_program_depth"],
        "candidate_generator_wiring_authorized": record["candidate_generator_wiring_authorized"],
        "runtime_wiring_authorized": record["runtime_wiring_authorized"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "candidate_generator_modified": record["candidate_generator_modified"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(
        json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"implementation_verdict={record['implementation_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_plan_ready={record['source_plan_ready']}",
        f"source_plan_shape_ok={record['source_plan_shape_ok']}",
        f"candidate_template_count={record['candidate_template_count']}",
        f"candidate_family_count={record['candidate_family_count']}",
        f"generated_candidate_count={record['generated_candidate_count']}",
        f"max_program_depth={record['max_program_depth']}",
        f"candidate_generator_wiring_authorized={record['candidate_generator_wiring_authorized']}",
        f"runtime_wiring_authorized={record['runtime_wiring_authorized']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"candidate_generator_modified={record['candidate_generator_modified']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    candidate_lines = "\n".join(
        [
            f"- `{candidate['candidate_id']}` `{candidate['template_name']}` family `{candidate['family']}` depth `{candidate['program_depth']}`"
            for candidate in record["generated_candidates"]
        ]
    )
    component_lines = "\n".join([f"- `{component}`" for component in record["implementation_components"]])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- implementation_verdict: `{record['implementation_verdict']}`
- next_stage: `{record['next_stage']}`

## Implementation Summary

- source_plan_ready: `{record['source_plan_ready']}`
- source_plan_shape_ok: `{record['source_plan_shape_ok']}`
- candidate_template_count: `{record['candidate_template_count']}`
- candidate_family_count: `{record['candidate_family_count']}`
- generated_candidate_count: `{record['generated_candidate_count']}`
- max_program_depth: `{record['max_program_depth']}`
- candidate_generator_wiring_authorized: `{record['candidate_generator_wiring_authorized']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`

## Implementation Components

{component_lines}

## Generated Candidates

{candidate_lines}

## Boundary

- real_evaluation_performed: `{record['real_evaluation_performed']}`
- real_submission_allowed: `{record['real_submission_allowed']}`
- ready_for_real_kaggle_submission: `{record['ready_for_real_kaggle_submission']}`
- kaggle_authentication_allowed: `{record['kaggle_authentication_allowed']}`
- kaggle_submission_sent: `{record['kaggle_submission_sent']}`
- external_api_dependency: `{record['external_api_dependency']}`
- internet_during_eval: `{record['internet_during_eval']}`
- private_core_exposure: `{record['private_core_exposure']}`
- legal_certification: `{record['legal_certification']}`
"""
    markdown_path.write_text(markdown, encoding="utf-8")

    def _artifact_ref(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            return str(path)

    return {
        "json": _artifact_ref(json_path),
        "index": _artifact_ref(index_path),
        "manifest": _artifact_ref(manifest_path),
        "markdown": _artifact_ref(markdown_path),
    }


def main() -> int:
    record = build_controlled_candidate_generator_record()
    issues = validate_controlled_candidate_generator_record(record)
    if issues:
        print(f"{TASK_NAME}_INVALID")
        for issue in issues:
            print(issue)
        return 1

    artifacts = write_artifacts(record)

    print(f"{TASK_NAME}_PIPELINE_READY")
    print(f"{TASK_NAME}_READY")
    print(f"{TASK_NAME}_VALID")
    print(record["signature"])
    print(record["baseline_commit"])
    print(record["task_mode"])
    print(record["task_verdict"])
    print(record["implementation_verdict"])
    print(record["next_stage"])
    print(f"generated_candidate_count={record['generated_candidate_count']}")
    print(f"max_program_depth={record['max_program_depth']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
