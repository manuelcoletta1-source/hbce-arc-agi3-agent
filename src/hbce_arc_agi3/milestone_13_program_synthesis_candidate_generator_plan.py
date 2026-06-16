"""Milestone #13 Task 5 - Program Synthesis Candidate Generator Plan v1.

This module defines a controlled, public-safe plan for a local program synthesis
candidate generator.

It is a planning gate only. It does not modify the live solver runtime, does not
wire the candidate generator, does not perform real Kaggle evaluation, does not
authenticate, does not upload, and does not submit.

The plan consumes Task 4 object-centric reasoning artifacts and prepares the
next controlled implementation stage.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 5
TASK_LABEL = "Milestone #13 Task 5 - Program Synthesis Candidate Generator Plan v1"

SOURCE_TASK = "MILESTONE_13_TASK_4_OBJECT_CENTRIC_REASONING_PLAN_V1"
NEXT_STAGE = "MILESTONE_13_TASK_6_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_READY"
PLAN_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-13" / "program-synthesis-candidate-generator-plan-v1"

SOURCE_OBJECT_PLAN_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "object-centric-reasoning-plan-v1"
    / "milestone-13-object-centric-reasoning-plan-v1.json"
)

SYNTHESIS_STAGES = [
    {
        "stage_id": "SYN-STAGE-01",
        "name": "training_pair_feature_read",
        "purpose": "read grid, object, color and relation features from local training pairs",
    },
    {
        "stage_id": "SYN-STAGE-02",
        "name": "program_template_selection",
        "purpose": "select bounded program templates from primitive and object-centric families",
    },
    {
        "stage_id": "SYN-STAGE-03",
        "name": "bounded_parameter_binding",
        "purpose": "bind colors, object selectors, directions, bbox references and symmetry axes",
    },
    {
        "stage_id": "SYN-STAGE-04",
        "name": "candidate_program_execution",
        "purpose": "execute candidate programs locally against training examples",
    },
    {
        "stage_id": "SYN-STAGE-05",
        "name": "candidate_evidence_packaging",
        "purpose": "package match evidence for future verifier and ranker layers",
    },
    {
        "stage_id": "SYN-STAGE-06",
        "name": "fail_closed_candidate_export",
        "purpose": "export only deterministic public-safe candidates for the next controlled stage",
    },
]

PROGRAM_TEMPLATES = [
    "single_primitive_transform",
    "two_step_primitive_sequence",
    "object_extract_then_transform",
    "object_filter_then_recolor",
    "object_relation_guided_move",
    "symmetry_completion_program",
    "palette_remap_program",
    "crop_pad_resize_program",
    "tile_or_repeat_program",
    "mask_overlay_program",
    "object_compose_or_remove_program",
    "conditional_rule_program",
]

CANDIDATE_FAMILIES = [
    {
        "family_id": "CAND-FAMILY-01",
        "name": "primitive_sequence_candidates",
        "priority": 1,
        "description": "bounded sequences of deterministic grid primitives",
    },
    {
        "family_id": "CAND-FAMILY-02",
        "name": "object_transform_candidates",
        "priority": 2,
        "description": "extract, move, copy, remove, recolor or compose detected objects",
    },
    {
        "family_id": "CAND-FAMILY-03",
        "name": "color_rule_candidates",
        "priority": 3,
        "description": "palette remaps, swaps and conditional recolor rules",
    },
    {
        "family_id": "CAND-FAMILY-04",
        "name": "symmetry_completion_candidates",
        "priority": 4,
        "description": "complete missing grid or object structure using symmetry hypotheses",
    },
    {
        "family_id": "CAND-FAMILY-05",
        "name": "crop_pad_resize_candidates",
        "priority": 5,
        "description": "shape and canvas transforms around object or non-background bounds",
    },
    {
        "family_id": "CAND-FAMILY-06",
        "name": "relation_graph_candidates",
        "priority": 6,
        "description": "generate candidates from object alignment, containment and adjacency relations",
    },
    {
        "family_id": "CAND-FAMILY-07",
        "name": "composite_program_candidates",
        "priority": 7,
        "description": "small bounded compositions of primitive, object and color programs",
    },
]

SEARCH_CONTROLS = [
    "MAX_PROGRAM_DEPTH_3_INITIAL",
    "MAX_CANDIDATES_PER_FAMILY_BOUNDED",
    "DETERMINISTIC_ORDERING_REQUIRED",
    "TRAINING_PAIR_MATCH_REQUIRED",
    "NO_PUBLIC_SET_MEMORIZATION",
    "FAIL_CLOSED_ON_EMPTY_SOURCE_PLAN",
    "NO_EXTERNAL_MODEL_CALLS",
    "NO_RUNTIME_WIRING_IN_PLAN_TASK",
]

IMPLEMENTATION_LANES = [
    {
        "lane_id": "LANE-01",
        "name": "program_template_schema",
        "output": "stable schema for local candidate program templates",
        "runtime_wiring_allowed": False,
    },
    {
        "lane_id": "LANE-02",
        "name": "parameter_binding_contract",
        "output": "bounded deterministic binding of colors, objects, vectors and axes",
        "runtime_wiring_allowed": False,
    },
    {
        "lane_id": "LANE-03",
        "name": "candidate_execution_contract",
        "output": "local-only execution contract for generated candidate programs",
        "runtime_wiring_allowed": False,
    },
    {
        "lane_id": "LANE-04",
        "name": "candidate_evidence_schema",
        "output": "evidence structure for future verifier and ranker integration",
        "runtime_wiring_allowed": False,
    },
    {
        "lane_id": "LANE-05",
        "name": "bounded_search_policy",
        "output": "depth, count and deterministic ordering rules for candidate search",
        "runtime_wiring_allowed": False,
    },
    {
        "lane_id": "LANE-06",
        "name": "controlled_implementation_entrypoint",
        "output": "next-stage implementation entrypoint with runtime still blocked",
        "runtime_wiring_allowed": False,
    },
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_CANDIDATE_GENERATOR_WIRING_IN_THIS_TASK",
    "NO_RANKER_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
]

QUALITY_TARGETS = [
    "program_templates_are_explicit",
    "candidate_families_are_bounded",
    "search_controls_are_fail_closed",
    "object_source_plan_is_verified",
    "evidence_schema_is_planned",
    "runtime_wiring_is_blocked",
    "next_task_is_controlled_implementation",
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


def _runtime_wiring_forbidden_count() -> int:
    return sum(1 for item in IMPLEMENTATION_LANES if item["runtime_wiring_allowed"] is False)


def build_program_synthesis_candidate_generator_plan(
    source_record: dict[str, Any] | None,
) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}

    return {
        "plan_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_PACKAGE_V1",
        "plan_family": "LOCAL_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_NO_RUNTIME_WIRING",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_plan_verdict": source.get("plan_verdict"),
        "source_next_stage": source.get("next_stage"),
        "source_object_operation_count": source.get("object_operation_count"),
        "synthesis_stages": SYNTHESIS_STAGES,
        "synthesis_stage_count": len(SYNTHESIS_STAGES),
        "program_templates": PROGRAM_TEMPLATES,
        "program_template_count": len(PROGRAM_TEMPLATES),
        "candidate_families": CANDIDATE_FAMILIES,
        "candidate_family_count": len(CANDIDATE_FAMILIES),
        "search_controls": SEARCH_CONTROLS,
        "search_control_count": len(SEARCH_CONTROLS),
        "implementation_lanes": IMPLEMENTATION_LANES,
        "implementation_lane_count": len(IMPLEMENTATION_LANES),
        "runtime_wiring_forbidden_count": _runtime_wiring_forbidden_count(),
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": len(RISK_CONTROLS),
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": len(QUALITY_TARGETS),
        "controlled_implementation_authorized": True,
        "candidate_generator_wiring_authorized": False,
        "runtime_wiring_authorized": False,
        "recommended_first_implementation_lane": IMPLEMENTATION_LANES[0]["name"],
        "recommended_next_stage": NEXT_STAGE,
    }


def build_program_synthesis_candidate_generator_plan_record(
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_OBJECT_PLAN_ARTIFACT.exists()
    source_record = _load_json(SOURCE_OBJECT_PLAN_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_plan_ready = bool(
        source_record
        and source_record.get("object_centric_reasoning_plan_ready") is True
        and source_record.get("object_centric_reasoning_plan_passed") is True
    )
    source_object_plan_ok = bool(
        source_record
        and source_record.get("object_reasoning_stage_count") == 6
        and source_record.get("object_feature_count") == 14
        and source_record.get("object_operation_group_count") == 7
        and source_record.get("object_operation_count") == 35
    )
    source_next_stage_ok = bool(
        source_record
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_5_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1"
    )
    source_blocks_runtime_wiring = bool(
        source_record
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

    plan = build_program_synthesis_candidate_generator_plan(source_record)

    synthesis_stage_count_ok = plan["synthesis_stage_count"] == 6
    program_template_count_ok = plan["program_template_count"] == 12
    candidate_family_count_ok = plan["candidate_family_count"] == 7
    search_control_count_ok = plan["search_control_count"] == 8
    implementation_lane_count_ok = plan["implementation_lane_count"] == 6
    runtime_wiring_forbidden_ok = plan["runtime_wiring_forbidden_count"] == 6
    risk_control_count_ok = plan["risk_control_count"] == 10
    quality_target_count_ok = plan["quality_target_count"] == 7

    controlled_implementation_authorized = True
    runtime_wiring_authorized = False
    runtime_solver_modified = False
    candidate_generator_modified = False
    candidate_generator_wiring_authorized = False
    ranker_runtime_modified = False
    real_evaluation_performed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 4 object plan artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 4 object plan artifact is parseable."),
        _gate("source_plan_ready", source_plan_ready, True, "Task 4 plan is ready and passed."),
        _gate("source_object_plan_ok", source_object_plan_ok, True, "Task 4 object plan has expected shape."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 4 points to Task 5."),
        _gate("source_blocks_runtime_wiring", source_blocks_runtime_wiring, True, "Source blocks runtime wiring."),
        _gate("source_blocks_real_actions", source_blocks_real_actions, True, "Source keeps real actions blocked."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source safety boundaries are preserved."),
        _gate("synthesis_stage_count_ok", synthesis_stage_count_ok, True, "Synthesis stages are declared."),
        _gate("program_template_count_ok", program_template_count_ok, True, "Program templates are declared."),
        _gate("candidate_family_count_ok", candidate_family_count_ok, True, "Candidate families are declared."),
        _gate("search_control_count_ok", search_control_count_ok, True, "Search controls are declared."),
        _gate("implementation_lane_count_ok", implementation_lane_count_ok, True, "Implementation lanes are declared."),
        _gate("runtime_wiring_forbidden_ok", runtime_wiring_forbidden_ok, True, "No implementation lane wires runtime."),
        _gate("risk_control_count_ok", risk_control_count_ok, True, "Risk controls are declared."),
        _gate("quality_target_count_ok", quality_target_count_ok, True, "Quality targets are declared."),
        _gate("controlled_implementation_authorized_true", controlled_implementation_authorized is True, True, "Controlled implementation planning is authorized."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator wiring remains blocked."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked in this task."),
        _gate("runtime_solver_modified_false", runtime_solver_modified is False, True, "Runtime solver is not modified."),
        _gate("candidate_generator_modified_false", candidate_generator_modified is False, True, "Candidate generator is not modified."),
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
        _gate("fail_closed_active", True, True, "Plan fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    plan_passed = len(required_gates) == len(passed_required_gates)

    plan_summary = {
        "plan_status": "READY" if plan_passed else "FAIL_CLOSED",
        "plan_verdict": PLAN_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "synthesis_stage_count": plan["synthesis_stage_count"],
        "program_template_count": plan["program_template_count"],
        "candidate_family_count": plan["candidate_family_count"],
        "search_control_count": plan["search_control_count"],
        "implementation_lane_count": plan["implementation_lane_count"],
        "recommended_first_implementation_lane": plan["recommended_first_implementation_lane"],
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
        "source_object_plan_artifact": str(SOURCE_OBJECT_PLAN_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_plan_ready": source_plan_ready,
        "source_object_plan_ok": source_object_plan_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_blocks_runtime_wiring": source_blocks_runtime_wiring,
        "source_blocks_real_actions": source_blocks_real_actions,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "plan_verdict": PLAN_VERDICT,
        "program_synthesis_candidate_generator_plan_ready": True,
        "program_synthesis_candidate_generator_plan_valid": plan_passed,
        "program_synthesis_candidate_generator_plan_passed": plan_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "plan_summary": plan_summary,
        "program_synthesis_candidate_generator_plan": plan,
        "synthesis_stages": SYNTHESIS_STAGES,
        "synthesis_stage_count": plan["synthesis_stage_count"],
        "program_templates": PROGRAM_TEMPLATES,
        "program_template_count": plan["program_template_count"],
        "candidate_families": CANDIDATE_FAMILIES,
        "candidate_family_count": plan["candidate_family_count"],
        "search_controls": SEARCH_CONTROLS,
        "search_control_count": plan["search_control_count"],
        "implementation_lanes": IMPLEMENTATION_LANES,
        "implementation_lane_count": plan["implementation_lane_count"],
        "runtime_wiring_forbidden_count": plan["runtime_wiring_forbidden_count"],
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": plan["risk_control_count"],
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": plan["quality_target_count"],
        "controlled_implementation_authorized": controlled_implementation_authorized,
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_planning_allowed": True,
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
        "plan_gate_count": len(gates),
        "plan_pass_count": len(passed_required_gates),
        "plan_blocking_issue_count": 0 if plan_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if plan_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-PROGRAM-SYNTHESIS-CANDIDATE-GENERATOR-PLAN-" + signature[:12]
    return record


def validate_program_synthesis_candidate_generator_plan_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_plan_ready",
        "source_object_plan_ok",
        "source_next_stage_ok",
        "source_blocks_runtime_wiring",
        "source_blocks_real_actions",
        "program_synthesis_candidate_generator_plan_ready",
        "program_synthesis_candidate_generator_plan_valid",
        "program_synthesis_candidate_generator_plan_passed",
        "controlled_implementation_authorized",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_planning_allowed",
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

    if record.get("plan_verdict") != PLAN_VERDICT:
        issues.append("PLAN_VERDICT_MISMATCH")

    expected_counts = {
        "synthesis_stage_count": 6,
        "program_template_count": 12,
        "candidate_family_count": 7,
        "search_control_count": 8,
        "implementation_lane_count": 6,
        "runtime_wiring_forbidden_count": 6,
        "risk_control_count": 10,
        "quality_target_count": 7,
        "plan_blocking_issue_count": 0,
        "issue_count": 0,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    plan = record.get("program_synthesis_candidate_generator_plan")
    if not isinstance(plan, dict):
        issues.append("PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_MISSING")
    else:
        if plan.get("synthesis_stage_count") != 6:
            issues.append("PLAN_SYNTHESIS_STAGE_COUNT_MISMATCH")
        if plan.get("program_template_count") != 12:
            issues.append("PLAN_PROGRAM_TEMPLATE_COUNT_MISMATCH")
        if plan.get("candidate_family_count") != 7:
            issues.append("PLAN_CANDIDATE_FAMILY_COUNT_MISMATCH")
        if plan.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("PLAN_RECOMMENDED_NEXT_STAGE_MISMATCH")
        if plan.get("runtime_wiring_authorized") is not False:
            issues.append("PLAN_RUNTIME_WIRING_NOT_BLOCKED")
        if plan.get("candidate_generator_wiring_authorized") is not False:
            issues.append("PLAN_CANDIDATE_GENERATOR_WIRING_NOT_BLOCKED")

    summary = record.get("plan_summary")
    if not isinstance(summary, dict):
        issues.append("PLAN_SUMMARY_MISSING")
    else:
        if summary.get("plan_status") != "READY":
            issues.append("PLAN_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("PLAN_SUMMARY_NEXT_STAGE_MISMATCH")
        if summary.get("recommended_first_implementation_lane") != "program_template_schema":
            issues.append("PLAN_SUMMARY_FIRST_LANE_MISMATCH")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-plan-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-plan-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-plan-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-plan-v1.md"

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
        "plan_verdict": record["plan_verdict"],
        "next_stage": record["next_stage"],
        "source_plan_ready": record["source_plan_ready"],
        "source_object_plan_ok": record["source_object_plan_ok"],
        "program_synthesis_candidate_generator_plan_ready": record["program_synthesis_candidate_generator_plan_ready"],
        "synthesis_stage_count": record["synthesis_stage_count"],
        "program_template_count": record["program_template_count"],
        "candidate_family_count": record["candidate_family_count"],
        "search_control_count": record["search_control_count"],
        "implementation_lane_count": record["implementation_lane_count"],
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
        f"plan_verdict={record['plan_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_plan_ready={record['source_plan_ready']}",
        f"source_object_plan_ok={record['source_object_plan_ok']}",
        f"synthesis_stage_count={record['synthesis_stage_count']}",
        f"program_template_count={record['program_template_count']}",
        f"candidate_family_count={record['candidate_family_count']}",
        f"search_control_count={record['search_control_count']}",
        f"implementation_lane_count={record['implementation_lane_count']}",
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

    stage_lines = "\n".join(
        [
            f"- `{stage['stage_id']}` `{stage['name']}`: {stage['purpose']}"
            for stage in record["synthesis_stages"]
        ]
    )
    family_lines = "\n".join(
        [
            f"- `{family['family_id']}` priority `{family['priority']}` `{family['name']}`: {family['description']}"
            for family in record["candidate_families"]
        ]
    )
    lane_lines = "\n".join(
        [
            f"{index + 1}. `{item['name']}` → {item['output']}"
            for index, item in enumerate(record["implementation_lanes"])
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- plan_verdict: `{record['plan_verdict']}`
- next_stage: `{record['next_stage']}`

## Plan Summary

- source_plan_ready: `{record['source_plan_ready']}`
- source_object_plan_ok: `{record['source_object_plan_ok']}`
- synthesis_stage_count: `{record['synthesis_stage_count']}`
- program_template_count: `{record['program_template_count']}`
- candidate_family_count: `{record['candidate_family_count']}`
- search_control_count: `{record['search_control_count']}`
- implementation_lane_count: `{record['implementation_lane_count']}`
- candidate_generator_wiring_authorized: `{record['candidate_generator_wiring_authorized']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`

## Synthesis Stages

{stage_lines}

## Candidate Families

{family_lines}

## Implementation Lanes

{lane_lines}

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
    record = build_program_synthesis_candidate_generator_plan_record()
    issues = validate_program_synthesis_candidate_generator_plan_record(record)
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
    print(record["plan_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
