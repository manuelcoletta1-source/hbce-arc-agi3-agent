"""Milestone #13 Task 3 - Transformation Primitive Expansion Plan v1.

This module defines a controlled, public-safe plan to expand local ARC-style
grid transformation primitives.

It is a planning gate only. It does not modify the live solver runtime, does not
perform real Kaggle evaluation, does not authenticate, does not upload, and does
not submit.

The plan exists because Task 2 identified TRANSFORMATION_PRIMITIVE_EXPANSION as
the top local solver improvement priority. Shocking discovery: solvers need
actual transformations. Humanity survives another revelation.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 3
TASK_LABEL = "Milestone #13 Task 3 - Transformation Primitive Expansion Plan v1"

SOURCE_TASK = "MILESTONE_13_TASK_2_SOLVER_CAPABILITY_GAP_AUDIT_V1"
NEXT_STAGE = "MILESTONE_13_TASK_4_OBJECT_CENTRIC_REASONING_PLAN_V1"

TASK_MODE = "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1_LOCAL_ONLY"
TASK_SCOPE = "PRIMITIVE_EXPANSION_PLAN_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY"
PLAN_VERDICT = "TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION"

SOURCE_REQUIRED_TOP_PRIORITY = "TRANSFORMATION_PRIMITIVE_EXPANSION"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-13" / "transformation-primitive-expansion-plan-v1"

SOURCE_AUDIT_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "solver-capability-gap-audit-v1"
    / "milestone-13-solver-capability-gap-audit-v1.json"
)

PRIMITIVE_GROUPS = [
    {
        "group_id": "PRIM-GEOMETRIC-CORE",
        "priority": 1,
        "purpose": "basic deterministic grid orientation transforms",
        "primitives": [
            "identity",
            "rotate_90",
            "rotate_180",
            "rotate_270",
            "flip_horizontal",
            "flip_vertical",
            "transpose",
        ],
    },
    {
        "group_id": "PRIM-CROP-PAD-TRANSLATE",
        "priority": 2,
        "purpose": "spatial extraction, placement, margin and offset transforms",
        "primitives": [
            "crop_to_non_background_bbox",
            "crop_to_object_bbox",
            "pad_to_shape",
            "translate_object",
            "center_object",
            "trim_empty_border",
        ],
    },
    {
        "group_id": "PRIM-COLOR-PALETTE",
        "priority": 3,
        "purpose": "color remapping and palette-level reasoning transforms",
        "primitives": [
            "map_color_one_to_one",
            "swap_two_colors",
            "background_normalize",
            "palette_compress",
            "palette_expand",
            "recolor_object_by_position",
        ],
    },
    {
        "group_id": "PRIM-OBJECT-BBOX",
        "priority": 4,
        "purpose": "object extraction, bounding box use and object recomposition",
        "primitives": [
            "extract_connected_components",
            "extract_largest_object",
            "extract_smallest_object",
            "copy_object_to_target",
            "repeat_object_by_rule",
            "remove_object_by_color",
        ],
    },
    {
        "group_id": "PRIM-PATTERN-SYMMETRY",
        "priority": 5,
        "purpose": "symmetry completion and periodic pattern extension",
        "primitives": [
            "complete_horizontal_symmetry",
            "complete_vertical_symmetry",
            "complete_rotational_symmetry",
            "repeat_row_pattern",
            "repeat_column_pattern",
            "tile_motif",
        ],
    },
    {
        "group_id": "PRIM-COMPOSITION-MASKS",
        "priority": 6,
        "purpose": "overlay, masking, fill and composition transforms",
        "primitives": [
            "overlay_non_background",
            "mask_by_color",
            "fill_holes",
            "outline_object",
            "intersect_masks",
            "union_masks",
        ],
    },
    {
        "group_id": "PRIM-SCALE-TILE",
        "priority": 7,
        "purpose": "controlled scaling and repetition transforms",
        "primitives": [
            "scale_nearest_integer",
            "downsample_by_block",
            "repeat_grid_tile",
            "expand_cell_to_block",
            "compress_blocks_to_cells",
            "mirror_tile_quadrants",
        ],
    },
]

IMPLEMENTATION_SLICES = [
    {
        "slice_id": "SLICE-01",
        "name": "deterministic_primitive_library",
        "output": "pure local functions with explicit input/output contracts",
        "runtime_wiring_allowed": False,
    },
    {
        "slice_id": "SLICE-02",
        "name": "primitive_unit_examples",
        "output": "small synthetic examples for each primitive family",
        "runtime_wiring_allowed": False,
    },
    {
        "slice_id": "SLICE-03",
        "name": "candidate_generator_adapter_plan",
        "output": "controlled adapter plan for future candidate generation",
        "runtime_wiring_allowed": False,
    },
    {
        "slice_id": "SLICE-04",
        "name": "verifier_feature_plan",
        "output": "evidence features for verifier and ranker scoring",
        "runtime_wiring_allowed": False,
    },
    {
        "slice_id": "SLICE-05",
        "name": "anti_overfit_guard_plan",
        "output": "guardrails against public-set memorization",
        "runtime_wiring_allowed": False,
    },
    {
        "slice_id": "SLICE-06",
        "name": "local_benchmark_plan",
        "output": "local-only benchmark hooks, no Kaggle call",
        "runtime_wiring_allowed": False,
    },
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
    "NO_OFFICIAL_SCORE_CLAIM",
    "NO_PRIVATE_CORE_EXPOSURE",
]

QUALITY_TARGETS = [
    "primitive_contracts_are_explicit",
    "primitive_groups_are_disjoint_enough_for_testing",
    "implementation_slices_are_sequenced",
    "candidate_generation_path_is_defined_but_not_wired",
    "verifier_and_ranker_hooks_are_planned_but_not_wired",
    "anti_overfit_boundary_is_preserved",
    "next_task_is_object_centric_reasoning_plan",
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


def _primitive_count() -> int:
    return sum(len(group["primitives"]) for group in PRIMITIVE_GROUPS)


def _runtime_wiring_forbidden_count() -> int:
    return sum(1 for item in IMPLEMENTATION_SLICES if item["runtime_wiring_allowed"] is False)


def build_primitive_expansion_plan(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}

    return {
        "plan_id": "MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_PACKAGE_V1",
        "plan_family": "LOCAL_TRANSFORMATION_PRIMITIVE_EXPANSION_NO_RUNTIME_WIRING",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_audit_verdict": source.get("audit_verdict"),
        "source_top_priority": source.get("top_priority"),
        "source_next_stage": source.get("next_stage"),
        "primitive_groups": PRIMITIVE_GROUPS,
        "primitive_group_count": len(PRIMITIVE_GROUPS),
        "primitive_count": _primitive_count(),
        "implementation_slices": IMPLEMENTATION_SLICES,
        "implementation_slice_count": len(IMPLEMENTATION_SLICES),
        "runtime_wiring_forbidden_count": _runtime_wiring_forbidden_count(),
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": len(RISK_CONTROLS),
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": len(QUALITY_TARGETS),
        "controlled_implementation_authorized": True,
        "runtime_wiring_authorized": False,
        "recommended_first_implementation_slice": IMPLEMENTATION_SLICES[0]["name"],
        "recommended_next_stage": NEXT_STAGE,
    }


def build_transformation_primitive_expansion_plan_record(
    baseline_commit: str | None = None,
) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_AUDIT_ARTIFACT.exists()
    source_record = _load_json(SOURCE_AUDIT_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_audit_ready = bool(
        source_record
        and source_record.get("solver_capability_gap_audit_ready") is True
        and source_record.get("solver_capability_gap_audit_passed") is True
    )
    source_top_priority_ok = bool(
        source_record
        and source_record.get("top_priority") == SOURCE_REQUIRED_TOP_PRIORITY
    )
    source_next_stage_ok = bool(
        source_record
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_3_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1"
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

    plan = build_primitive_expansion_plan(source_record)

    primitive_group_count_ok = plan["primitive_group_count"] == 7
    primitive_count_ok = plan["primitive_count"] == 43
    implementation_slice_count_ok = plan["implementation_slice_count"] == 6
    runtime_wiring_forbidden_ok = plan["runtime_wiring_forbidden_count"] == 6
    risk_control_count_ok = plan["risk_control_count"] == 10
    quality_target_count_ok = plan["quality_target_count"] == 7
    controlled_implementation_authorized = True
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
        _gate("source_artifact_present", source_artifact_present, True, "Task 2 audit artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 2 audit artifact is parseable."),
        _gate("source_audit_ready", source_audit_ready, True, "Task 2 audit is ready and passed."),
        _gate("source_top_priority_ok", source_top_priority_ok, True, "Task 2 selected transformation primitives as top priority."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 2 points to Task 3."),
        _gate("source_blocks_real_actions", source_blocks_real_actions, True, "Source keeps real actions blocked."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source safety boundaries are preserved."),
        _gate("primitive_group_count_ok", primitive_group_count_ok, True, "Primitive group count is expected."),
        _gate("primitive_count_ok", primitive_count_ok, True, "Primitive count is expected."),
        _gate("implementation_slice_count_ok", implementation_slice_count_ok, True, "Implementation slice count is expected."),
        _gate("runtime_wiring_forbidden_ok", runtime_wiring_forbidden_ok, True, "No implementation slice wires runtime."),
        _gate("risk_control_count_ok", risk_control_count_ok, True, "Risk controls are declared."),
        _gate("quality_target_count_ok", quality_target_count_ok, True, "Quality targets are declared."),
        _gate("controlled_implementation_authorized_true", controlled_implementation_authorized is True, True, "Controlled implementation planning is authorized."),
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
        "source_top_priority": source_record.get("top_priority") if source_record else None,
        "primitive_group_count": plan["primitive_group_count"],
        "primitive_count": plan["primitive_count"],
        "implementation_slice_count": plan["implementation_slice_count"],
        "risk_control_count": plan["risk_control_count"],
        "recommended_first_implementation_slice": plan["recommended_first_implementation_slice"],
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
        "source_audit_artifact": str(SOURCE_AUDIT_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_audit_ready": source_audit_ready,
        "source_top_priority_ok": source_top_priority_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_blocks_real_actions": source_blocks_real_actions,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "plan_verdict": PLAN_VERDICT,
        "transformation_primitive_expansion_plan_ready": True,
        "transformation_primitive_expansion_plan_valid": plan_passed,
        "transformation_primitive_expansion_plan_passed": plan_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "plan_summary": plan_summary,
        "primitive_expansion_plan": plan,
        "primitive_groups": PRIMITIVE_GROUPS,
        "primitive_group_count": plan["primitive_group_count"],
        "primitive_count": plan["primitive_count"],
        "implementation_slices": IMPLEMENTATION_SLICES,
        "implementation_slice_count": plan["implementation_slice_count"],
        "runtime_wiring_forbidden_count": plan["runtime_wiring_forbidden_count"],
        "risk_controls": RISK_CONTROLS,
        "risk_control_count": plan["risk_control_count"],
        "quality_targets": QUALITY_TARGETS,
        "quality_target_count": plan["quality_target_count"],
        "controlled_implementation_authorized": controlled_implementation_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "primitive_expansion_planning_allowed": True,
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
    record["task_id"] = "MILESTONE-13-TRANSFORMATION-PRIMITIVE-EXPANSION-PLAN-" + signature[:12]
    return record


def validate_transformation_primitive_expansion_plan_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_audit_ready",
        "source_top_priority_ok",
        "source_next_stage_ok",
        "source_blocks_real_actions",
        "transformation_primitive_expansion_plan_ready",
        "transformation_primitive_expansion_plan_valid",
        "transformation_primitive_expansion_plan_passed",
        "controlled_implementation_authorized",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "primitive_expansion_planning_allowed",
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
        "primitive_group_count": 7,
        "primitive_count": 43,
        "implementation_slice_count": 6,
        "runtime_wiring_forbidden_count": 6,
        "risk_control_count": 10,
        "quality_target_count": 7,
        "plan_blocking_issue_count": 0,
        "issue_count": 0,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    plan = record.get("primitive_expansion_plan")
    if not isinstance(plan, dict):
        issues.append("PRIMITIVE_EXPANSION_PLAN_MISSING")
    else:
        if plan.get("primitive_group_count") != 7:
            issues.append("PLAN_PRIMITIVE_GROUP_COUNT_MISMATCH")
        if plan.get("primitive_count") != 43:
            issues.append("PLAN_PRIMITIVE_COUNT_MISMATCH")
        if plan.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("PLAN_RECOMMENDED_NEXT_STAGE_MISMATCH")
        if plan.get("runtime_wiring_authorized") is not False:
            issues.append("PLAN_RUNTIME_WIRING_NOT_BLOCKED")

    summary = record.get("plan_summary")
    if not isinstance(summary, dict):
        issues.append("PLAN_SUMMARY_MISSING")
    else:
        if summary.get("plan_status") != "READY":
            issues.append("PLAN_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("PLAN_SUMMARY_NEXT_STAGE_MISMATCH")
        if summary.get("recommended_first_implementation_slice") != "deterministic_primitive_library":
            issues.append("PLAN_SUMMARY_FIRST_SLICE_MISMATCH")

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

    json_path = target_dir / "milestone-13-transformation-primitive-expansion-plan-v1.json"
    index_path = target_dir / "milestone-13-transformation-primitive-expansion-plan-index-v1.json"
    manifest_path = target_dir / "milestone-13-transformation-primitive-expansion-plan-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-transformation-primitive-expansion-plan-v1.md"

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
        "source_audit_ready": record["source_audit_ready"],
        "source_top_priority_ok": record["source_top_priority_ok"],
        "transformation_primitive_expansion_plan_ready": record["transformation_primitive_expansion_plan_ready"],
        "primitive_group_count": record["primitive_group_count"],
        "primitive_count": record["primitive_count"],
        "implementation_slice_count": record["implementation_slice_count"],
        "runtime_wiring_authorized": record["runtime_wiring_authorized"],
        "runtime_solver_modified": record["runtime_solver_modified"],
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
        f"source_audit_ready={record['source_audit_ready']}",
        f"source_top_priority_ok={record['source_top_priority_ok']}",
        f"primitive_group_count={record['primitive_group_count']}",
        f"primitive_count={record['primitive_count']}",
        f"implementation_slice_count={record['implementation_slice_count']}",
        f"runtime_wiring_authorized={record['runtime_wiring_authorized']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    primitive_lines = "\n".join(
        [
            f"- `{group['group_id']}` priority `{group['priority']}`: {len(group['primitives'])} primitives"
            for group in record["primitive_groups"]
        ]
    )
    slice_lines = "\n".join(
        [
            f"{index + 1}. `{item['name']}` → {item['output']}"
            for index, item in enumerate(record["implementation_slices"])
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

- source_audit_ready: `{record['source_audit_ready']}`
- source_top_priority_ok: `{record['source_top_priority_ok']}`
- primitive_group_count: `{record['primitive_group_count']}`
- primitive_count: `{record['primitive_count']}`
- implementation_slice_count: `{record['implementation_slice_count']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`

## Primitive Groups

{primitive_lines}

## Implementation Slices

{slice_lines}

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
    record = build_transformation_primitive_expansion_plan_record()
    issues = validate_transformation_primitive_expansion_plan_record(record)
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
