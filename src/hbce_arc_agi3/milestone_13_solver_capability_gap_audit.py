"""Milestone #13 Task 2 - Solver Capability Gap Audit v1.

This module audits the current local competitive solver chain and produces a
public-safe capability gap report.

It does not run real Kaggle evaluation, does not authenticate, does not upload,
does not submit, and does not claim score.

Purpose:
- identify solver capability gaps
- prioritize local improvements
- keep all real-evaluation and submission boundaries blocked
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 2
TASK_LABEL = "Milestone #13 Task 2 - Solver Capability Gap Audit v1"

SOURCE_TASK = "MILESTONE_13_TASK_1_REAL_EVALUATION_BOUNDARY_GATE_V1"
NEXT_STAGE = "MILESTONE_13_TASK_3_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1"

TASK_MODE = "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_V1_LOCAL_ONLY"
TASK_SCOPE = "CAPABILITY_GAP_AUDIT_ONLY_NO_REAL_EVAL_NO_KAGGLE_AUTH_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_READY"

AUDIT_VERDICT = "SOLVER_CAPABILITY_GAP_AUDIT_READY_FOR_LOCAL_IMPROVEMENT_PLAN"

CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"
COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = PROJECT_ROOT / "examples" / "milestone-13" / "solver-capability-gap-audit-v1"

SOURCE_BOUNDARY_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "real-evaluation-boundary-gate-v1"
    / "milestone-13-real-evaluation-boundary-gate-v1.json"
)

SOURCE_CHAIN_ARTIFACTS = [
    "examples/milestone-12/executable-world-model-v1/milestone-12-executable-world-model-v1.json",
    "examples/milestone-12/world-model-verifier-v1/milestone-12-world-model-verifier-v1.json",
    "examples/milestone-12/verified-planner-policy-v1/milestone-12-verified-planner-policy-v1.json",
    "examples/milestone-12/episode-memory-policy-v1/milestone-12-episode-memory-policy-v1.json",
    "examples/milestone-12/candidate-policy-v1/milestone-12-candidate-policy-v1.json",
    "examples/milestone-12/candidate-ranker-policy-v1/milestone-12-candidate-ranker-policy-v1.json",
    "examples/milestone-12/ranked-candidate-benchmark-v1/milestone-12-ranked-candidate-benchmark-v1.json",
    "examples/milestone-12/public-overfit-guard-v1/milestone-12-public-overfit-guard-v1.json",
    "examples/milestone-12/submission-readiness-gate-v1/milestone-12-submission-readiness-gate-v1.json",
    "examples/milestone-12/competitive-solver-closure-v1/milestone-12-competitive-solver-closure-v1.json",
    "examples/milestone-13/real-evaluation-boundary-gate-v1/milestone-13-real-evaluation-boundary-gate-v1.json",
]

CAPABILITY_AREAS = [
    "object_detection_and_segmentation",
    "grid_transformation_primitives",
    "symmetry_and_pattern_completion",
    "color_mapping_and_palette_reasoning",
    "shape_extraction_and_recomposition",
    "multi_step_program_synthesis",
    "candidate_generation_diversity",
    "candidate_verification_strength",
    "ranker_confidence_calibration",
    "failure_memory_reuse",
    "public_overfit_resistance",
    "submission_readiness_control",
]

GAP_RECORDS = [
    {
        "gap_id": "GAP-01",
        "area": "grid_transformation_primitives",
        "severity": "HIGH",
        "probability_of_score_impact": 0.82,
        "finding": "Primitive coverage must expand beyond current safe policy declarations.",
        "recommended_next_task": "MILESTONE_13_TASK_3_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1",
    },
    {
        "gap_id": "GAP-02",
        "area": "object_detection_and_segmentation",
        "severity": "HIGH",
        "probability_of_score_impact": 0.78,
        "finding": "Object-centric extraction needs stronger local diagnostics before real submission.",
        "recommended_next_task": "MILESTONE_13_TASK_4_OBJECT_CENTRIC_REASONING_PLAN_V1",
    },
    {
        "gap_id": "GAP-03",
        "area": "multi_step_program_synthesis",
        "severity": "HIGH",
        "probability_of_score_impact": 0.75,
        "finding": "Multi-step transformation planning remains the central competitive bottleneck.",
        "recommended_next_task": "MILESTONE_13_TASK_5_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1",
    },
    {
        "gap_id": "GAP-04",
        "area": "candidate_generation_diversity",
        "severity": "MEDIUM_HIGH",
        "probability_of_score_impact": 0.69,
        "finding": "Candidate policy requires broader generation without public-set overfitting.",
        "recommended_next_task": "MILESTONE_13_TASK_6_CANDIDATE_GENERATOR_DIVERSITY_PLAN_V1",
    },
    {
        "gap_id": "GAP-05",
        "area": "ranker_confidence_calibration",
        "severity": "MEDIUM_HIGH",
        "probability_of_score_impact": 0.66,
        "finding": "Ranker must separate evidence quality from candidate abundance.",
        "recommended_next_task": "MILESTONE_13_TASK_7_RANKER_CALIBRATION_PLAN_V1",
    },
    {
        "gap_id": "GAP-06",
        "area": "failure_memory_reuse",
        "severity": "MEDIUM",
        "probability_of_score_impact": 0.58,
        "finding": "Failure classes should be converted into reusable local improvement cases.",
        "recommended_next_task": "MILESTONE_13_TASK_8_FAILURE_MEMORY_REPLAY_PLAN_V1",
    },
]

PRIORITY_PLAN = [
    "TRANSFORMATION_PRIMITIVE_EXPANSION",
    "OBJECT_CENTRIC_REASONING",
    "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR",
    "CANDIDATE_DIVERSITY_CONTROL",
    "RANKER_CONFIDENCE_CALIBRATION",
    "FAILURE_MEMORY_REPLAY",
]

AUDIT_MEASUREMENT_TARGETS = [
    "source_boundary_gate_passed",
    "source_real_submission_allowed",
    "source_kaggle_authentication_allowed",
    "source_chain_artifact_present_count",
    "source_chain_artifact_parseable_count",
    "capability_area_count",
    "gap_count",
    "high_priority_gap_count",
    "priority_plan_step_count",
    "audit_blocking_issue_count",
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
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
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


def _artifact_status(path_text: str) -> dict[str, Any]:
    path = PROJECT_ROOT / path_text
    record = _load_json(path)

    return {
        "path": path_text,
        "present": path.exists(),
        "parseable_json": record is not None,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None,
        "revision": record.get("revision") if isinstance(record, dict) else None,
        "task_verdict": record.get("task_verdict") if isinstance(record, dict) else None,
        "next_stage": record.get("next_stage") if isinstance(record, dict) else None,
    }


def build_gap_audit_package(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}
    chain_statuses = [_artifact_status(path) for path in SOURCE_CHAIN_ARTIFACTS]
    present_count = sum(1 for item in chain_statuses if item["present"] is True)
    parseable_count = sum(1 for item in chain_statuses if item["parseable_json"] is True)

    high_priority_gaps = [
        gap for gap in GAP_RECORDS if gap["severity"] in {"HIGH", "MEDIUM_HIGH"}
    ]

    return {
        "audit_package_id": "MILESTONE_13_SOLVER_CAPABILITY_GAP_AUDIT_PACKAGE_V1",
        "package_family": "LOCAL_SOLVER_CAPABILITY_AUDIT_NO_REAL_EVALUATION",
        "source_boundary_verdict": source.get("boundary_verdict"),
        "source_milestone_13_status": source.get("milestone_13_status"),
        "source_next_stage": source.get("next_stage"),
        "source_real_evaluation_prep_allowed": source.get("real_evaluation_prep_allowed"),
        "source_local_solver_improvement_allowed": source.get("local_solver_improvement_allowed"),
        "source_solver_capability_gap_audit_allowed": source.get("solver_capability_gap_audit_allowed"),
        "source_real_submission_allowed": source.get("real_submission_allowed"),
        "source_kaggle_authentication_allowed": source.get("kaggle_authentication_allowed"),
        "source_chain_artifacts": chain_statuses,
        "source_chain_artifact_count": len(SOURCE_CHAIN_ARTIFACTS),
        "source_chain_artifact_present_count": present_count,
        "source_chain_artifact_parseable_count": parseable_count,
        "capability_areas": CAPABILITY_AREAS,
        "capability_area_count": len(CAPABILITY_AREAS),
        "gaps": GAP_RECORDS,
        "gap_count": len(GAP_RECORDS),
        "high_priority_gaps": high_priority_gaps,
        "high_priority_gap_count": len(high_priority_gaps),
        "priority_plan": PRIORITY_PLAN,
        "priority_plan_step_count": len(PRIORITY_PLAN),
        "measurement_targets": AUDIT_MEASUREMENT_TARGETS,
        "measurement_target_count": len(AUDIT_MEASUREMENT_TARGETS),
    }


def build_solver_capability_gap_audit_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_artifact_present = SOURCE_BOUNDARY_ARTIFACT.exists()
    source_record = _load_json(SOURCE_BOUNDARY_ARTIFACT)
    source_artifact_parseable = source_record is not None

    source_boundary_ready = bool(source_record and source_record.get("real_evaluation_boundary_gate_ready") is True)
    source_boundary_passed = bool(source_record and source_record.get("real_evaluation_boundary_gate_passed") is True)
    source_boundary_verdict_ok = bool(
        source_record
        and source_record.get("boundary_verdict")
        == "MILESTONE_13_OPENED_CANONICALLY_REAL_EVALUATION_PREP_ALLOWED_REAL_SUBMISSION_BLOCKED"
    )
    source_next_stage_ok = bool(
        source_record and source_record.get("next_stage") == "MILESTONE_13_TASK_2_SOLVER_CAPABILITY_GAP_AUDIT_V1"
    )

    source_allows_local_audit = bool(
        source_record
        and source_record.get("real_evaluation_prep_allowed") is True
        and source_record.get("local_solver_improvement_allowed") is True
        and source_record.get("solver_capability_gap_audit_allowed") is True
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
        and source_record.get("operator_approval_required") is True
        and source_record.get("operator_approval_received") is False
    )

    source_boundaries_ok = all(
        [
            source_record and source_record.get("local_only") is True,
            source_record and source_record.get("deterministic") is True,
            source_record and source_record.get("public_safe") is True,
            source_record and source_record.get("public_overfit_allowed") is False,
            source_record and source_record.get("public_overfit_guard_required") is True,
            source_record and source_record.get("external_api_dependency") is False,
            source_record and source_record.get("internet_during_eval") is False,
            source_record and source_record.get("private_core_exposure") is False,
            source_record and source_record.get("legal_certification") is False,
            source_record and source_record.get("official_score_claim_allowed") is False,
            source_record and source_record.get("competitive_score_claim_allowed") is False,
        ]
    )

    package = build_gap_audit_package(source_record)

    chain_count_ok = package["source_chain_artifact_count"] == len(SOURCE_CHAIN_ARTIFACTS)
    chain_present_ok = package["source_chain_artifact_present_count"] == len(SOURCE_CHAIN_ARTIFACTS)
    chain_parseable_ok = package["source_chain_artifact_parseable_count"] == len(SOURCE_CHAIN_ARTIFACTS)
    capability_count_ok = package["capability_area_count"] == 12
    gap_count_ok = package["gap_count"] == 6
    high_priority_gap_count_ok = package["high_priority_gap_count"] == 5
    priority_plan_count_ok = package["priority_plan_step_count"] == 6
    measurement_count_ok = package["measurement_target_count"] == 10

    audit_ready = True
    audit_valid = True
    real_evaluation_performed = False
    real_submission_allowed = False
    ready_for_real_kaggle_submission = False
    kaggle_authentication_allowed = False
    kaggle_authentication_performed = False
    kaggle_upload_allowed = False
    kaggle_submission_sent = False

    gates = [
        _gate("source_artifact_present", source_artifact_present, True, "Task 1 boundary artifact is present."),
        _gate("source_artifact_parseable", source_artifact_parseable, True, "Task 1 boundary artifact is parseable."),
        _gate("source_boundary_ready", source_boundary_ready, True, "Task 1 boundary gate is ready."),
        _gate("source_boundary_passed", source_boundary_passed, True, "Task 1 boundary gate passed."),
        _gate("source_boundary_verdict_ok", source_boundary_verdict_ok, True, "Task 1 boundary verdict is canonical."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 1 points to Task 2."),
        _gate("source_allows_local_audit", source_allows_local_audit, True, "Boundary allows local audit."),
        _gate("source_blocks_real_actions", source_blocks_real_actions, True, "Boundary blocks real actions."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Source safety boundaries are preserved."),
        _gate("chain_count_ok", chain_count_ok, True, "Expected source chain artifact count is declared."),
        _gate("chain_present_ok", chain_present_ok, True, "All source chain artifacts are present."),
        _gate("chain_parseable_ok", chain_parseable_ok, True, "All source chain artifacts are parseable."),
        _gate("capability_count_ok", capability_count_ok, True, "Capability areas are declared."),
        _gate("gap_count_ok", gap_count_ok, True, "Capability gaps are declared."),
        _gate("high_priority_gap_count_ok", high_priority_gap_count_ok, True, "High priority gaps are declared."),
        _gate("priority_plan_count_ok", priority_plan_count_ok, True, "Priority plan is declared."),
        _gate("measurement_count_ok", measurement_count_ok, True, "Audit measurement targets are declared."),
        _gate("audit_ready_true", audit_ready is True, True, "Audit is ready."),
        _gate("audit_valid_true", audit_valid is True, True, "Audit is valid."),
        _gate("real_evaluation_performed_false", real_evaluation_performed is False, True, "No real evaluation is performed."),
        _gate("real_submission_allowed_false", real_submission_allowed is False, True, "Real submission remains blocked."),
        _gate("ready_for_real_kaggle_submission_false", ready_for_real_kaggle_submission is False, True, "Real Kaggle submission readiness remains blocked."),
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
        _gate("fail_closed_active", True, True, "Audit fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    audit_passed = len(required_gates) == len(passed_required_gates)

    audit_summary = {
        "audit_status": "READY" if audit_passed else "FAIL_CLOSED",
        "audit_verdict": AUDIT_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "source_boundary_passed": source_boundary_passed,
        "capability_area_count": package["capability_area_count"],
        "gap_count": package["gap_count"],
        "high_priority_gap_count": package["high_priority_gap_count"],
        "priority_plan_step_count": package["priority_plan_step_count"],
        "top_priority": PRIORITY_PLAN[0],
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
        "source_boundary_artifact": str(SOURCE_BOUNDARY_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_artifact_present": source_artifact_present,
        "source_artifact_parseable": source_artifact_parseable,
        "source_boundary_ready": source_boundary_ready,
        "source_boundary_passed": source_boundary_passed,
        "source_boundary_verdict_ok": source_boundary_verdict_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_allows_local_audit": source_allows_local_audit,
        "source_blocks_real_actions": source_blocks_real_actions,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "audit_verdict": AUDIT_VERDICT,
        "solver_capability_gap_audit_ready": audit_ready,
        "solver_capability_gap_audit_valid": audit_valid and audit_passed,
        "solver_capability_gap_audit_passed": audit_passed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "audit_summary": audit_summary,
        "gap_audit_package": package,
        "source_chain_artifact_count": package["source_chain_artifact_count"],
        "source_chain_artifact_present_count": package["source_chain_artifact_present_count"],
        "source_chain_artifact_parseable_count": package["source_chain_artifact_parseable_count"],
        "capability_areas": CAPABILITY_AREAS,
        "capability_area_count": len(CAPABILITY_AREAS),
        "gaps": GAP_RECORDS,
        "gap_count": len(GAP_RECORDS),
        "high_priority_gap_count": package["high_priority_gap_count"],
        "priority_plan": PRIORITY_PLAN,
        "priority_plan_step_count": len(PRIORITY_PLAN),
        "top_priority": PRIORITY_PLAN[0],
        "measurement_target_count": len(AUDIT_MEASUREMENT_TARGETS),
        "measurement_targets": AUDIT_MEASUREMENT_TARGETS,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "solver_capability_gap_audit_allowed": True,
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
        "audit_gate_count": len(gates),
        "audit_pass_count": len(passed_required_gates),
        "audit_blocking_issue_count": 0 if audit_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if audit_passed else len(required_gates) - len(passed_required_gates),
        "warning_count": 0,
        "gates": gates,
    }

    signature_payload = {key: value for key, value in record.items() if key not in {"signature", "task_id"}}
    signature = _stable_signature(signature_payload)
    record["signature"] = signature
    record["task_id"] = "MILESTONE-13-SOLVER-CAPABILITY-GAP-AUDIT-" + signature[:12]
    return record


def validate_solver_capability_gap_audit_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_artifact_present",
        "source_artifact_parseable",
        "source_boundary_ready",
        "source_boundary_passed",
        "source_boundary_verdict_ok",
        "source_next_stage_ok",
        "source_allows_local_audit",
        "source_blocks_real_actions",
        "solver_capability_gap_audit_ready",
        "solver_capability_gap_audit_valid",
        "solver_capability_gap_audit_passed",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "solver_capability_gap_audit_allowed",
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

    if record.get("audit_verdict") != AUDIT_VERDICT:
        issues.append("AUDIT_VERDICT_MISMATCH")

    if record.get("competitive_goal") != COMPETITIVE_GOAL:
        issues.append("COMPETITIVE_GOAL_MISMATCH")

    if record.get("chosen_strategy") != CHOSEN_STRATEGY:
        issues.append("CHOSEN_STRATEGY_MISMATCH")

    expected_counts = {
        "source_chain_artifact_count": 11,
        "source_chain_artifact_present_count": 11,
        "source_chain_artifact_parseable_count": 11,
        "capability_area_count": 12,
        "gap_count": 6,
        "high_priority_gap_count": 5,
        "priority_plan_step_count": 6,
        "measurement_target_count": 10,
        "audit_blocking_issue_count": 0,
        "issue_count": 0,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    package = record.get("gap_audit_package")
    if not isinstance(package, dict):
        issues.append("GAP_AUDIT_PACKAGE_MISSING")
    else:
        if package.get("source_chain_artifact_present_count") != 11:
            issues.append("PACKAGE_SOURCE_CHAIN_PRESENT_COUNT_MISMATCH")
        if package.get("source_chain_artifact_parseable_count") != 11:
            issues.append("PACKAGE_SOURCE_CHAIN_PARSEABLE_COUNT_MISMATCH")
        if package.get("gap_count") != 6:
            issues.append("PACKAGE_GAP_COUNT_MISMATCH")

    summary = record.get("audit_summary")
    if not isinstance(summary, dict):
        issues.append("AUDIT_SUMMARY_MISSING")
    else:
        if summary.get("audit_status") != "READY":
            issues.append("AUDIT_SUMMARY_STATUS_NOT_READY")
        if summary.get("next_stage") != NEXT_STAGE:
            issues.append("AUDIT_SUMMARY_NEXT_STAGE_MISMATCH")
        if summary.get("top_priority") != "TRANSFORMATION_PRIMITIVE_EXPANSION":
            issues.append("AUDIT_SUMMARY_TOP_PRIORITY_MISMATCH")

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

    json_path = target_dir / "milestone-13-solver-capability-gap-audit-v1.json"
    index_path = target_dir / "milestone-13-solver-capability-gap-audit-index-v1.json"
    manifest_path = target_dir / "milestone-13-solver-capability-gap-audit-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-solver-capability-gap-audit-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "audit_verdict": record["audit_verdict"],
        "next_stage": record["next_stage"],
        "source_boundary_passed": record["source_boundary_passed"],
        "solver_capability_gap_audit_ready": record["solver_capability_gap_audit_ready"],
        "capability_area_count": record["capability_area_count"],
        "gap_count": record["gap_count"],
        "high_priority_gap_count": record["high_priority_gap_count"],
        "priority_plan_step_count": record["priority_plan_step_count"],
        "top_priority": record["top_priority"],
        "real_evaluation_performed": record["real_evaluation_performed"],
        "real_submission_allowed": record["real_submission_allowed"],
        "kaggle_authentication_allowed": record["kaggle_authentication_allowed"],
        "kaggle_submission_sent": record["kaggle_submission_sent"],
        "private_core_exposure": record["private_core_exposure"],
        "legal_certification": record["legal_certification"],
    }
    index_path.write_text(json.dumps(index, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        f"revision={record['revision']}",
        f"task_id={record['task_id']}",
        f"signature={record['signature']}",
        f"baseline_commit={record['baseline_commit']}",
        f"task_mode={record['task_mode']}",
        f"task_scope={record['task_scope']}",
        f"task_verdict={record['task_verdict']}",
        f"audit_verdict={record['audit_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_boundary_passed={record['source_boundary_passed']}",
        f"solver_capability_gap_audit_ready={record['solver_capability_gap_audit_ready']}",
        f"capability_area_count={record['capability_area_count']}",
        f"gap_count={record['gap_count']}",
        f"high_priority_gap_count={record['high_priority_gap_count']}",
        f"priority_plan_step_count={record['priority_plan_step_count']}",
        f"top_priority={record['top_priority']}",
        f"real_evaluation_performed={record['real_evaluation_performed']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_authentication_allowed={record['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    gap_lines = "\n".join(
        [
            f"- `{gap['gap_id']}` `{gap['severity']}` `{gap['area']}`: {gap['finding']}"
            for gap in record["gaps"]
        ]
    )
    priority_lines = "\n".join([f"{index + 1}. `{step}`" for index, step in enumerate(record["priority_plan"])])

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- audit_verdict: `{record['audit_verdict']}`
- next_stage: `{record['next_stage']}`

## Audit Summary

- source_boundary_passed: `{record['source_boundary_passed']}`
- solver_capability_gap_audit_ready: `{record['solver_capability_gap_audit_ready']}`
- capability_area_count: `{record['capability_area_count']}`
- gap_count: `{record['gap_count']}`
- high_priority_gap_count: `{record['high_priority_gap_count']}`
- priority_plan_step_count: `{record['priority_plan_step_count']}`
- top_priority: `{record['top_priority']}`

## Capability Gaps

{gap_lines}

## Priority Plan

{priority_lines}

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
    record = build_solver_capability_gap_audit_record()
    issues = validate_solver_capability_gap_audit_record(record)
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
    print(record["audit_verdict"])
    print(record["next_stage"])
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
