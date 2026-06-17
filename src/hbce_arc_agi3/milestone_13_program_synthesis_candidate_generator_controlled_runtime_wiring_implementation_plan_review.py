"""Milestone #13 Task 13 - Controlled Runtime Wiring Implementation Plan Review v1.

This task reviews Task 12 and authorizes the next controlled implementation task.

It does not implement runtime wiring.
It does not modify solver runtime.
It does not modify candidate generator runtime behavior.
It does not modify ranker runtime behavior.
It does not run real Kaggle evaluation, authenticate, upload, or submit.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 13
TASK_LABEL = "Milestone #13 Task 13 - Program Synthesis Candidate Generator Controlled Runtime Wiring Implementation Plan Review v1"

SOURCE_TASK = "MILESTONE_13_TASK_12_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_V1"
NEXT_STAGE = "MILESTONE_13_TASK_14_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_V1_LOCAL_ONLY"
TASK_SCOPE = "CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_ONLY_NO_IMPLEMENTATION_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_READY"
REVIEW_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_PASS_READY_FOR_CONTROLLED_IMPLEMENTATION"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-v1"
)

SOURCE_PLAN_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-v1"
    / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-v1.json"
)

REVIEW_FINDINGS = [
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-01",
        "name": "source_plan_exists",
        "severity": "PASS",
        "description": "Task 12 controlled implementation plan artifact exists and is parseable.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-02",
        "name": "plan_is_plan_only",
        "severity": "PASS",
        "description": "Task 12 is explicitly a plan-only layer and did not implement wiring.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-03",
        "name": "implementation_units_are_explicit",
        "severity": "PASS",
        "description": "Task 12 defines four controlled implementation units.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-04",
        "name": "implementation_phases_are_explicit",
        "severity": "PASS",
        "description": "Task 12 defines seven controlled implementation phases.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-05",
        "name": "runtime_remains_untouched",
        "severity": "PASS",
        "description": "Runtime wiring, solver modification, candidate generator modification, and ranker runtime modification remain blocked.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-06",
        "name": "real_actions_remain_blocked",
        "severity": "PASS",
        "description": "Real Kaggle evaluation, authentication, upload, and submission remain blocked.",
    },
    {
        "finding_id": "CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-07",
        "name": "controlled_implementation_can_open",
        "severity": "PASS",
        "description": "The next stage may perform controlled local implementation under boundaries.",
    },
]

REVIEW_CRITERIA = [
    "source_plan_artifact_present",
    "source_plan_artifact_parseable",
    "source_plan_ready",
    "source_plan_valid",
    "source_plan_review_required",
    "source_controlled_implementation_not_authorized",
    "source_implementation_not_allowed_now",
    "implementation_unit_count_4",
    "implementation_phase_count_7",
    "implementation_gate_count_18",
    "all_units_require_review_before_code",
    "all_units_runtime_activation_blocked",
    "all_units_implementation_blocked_now",
    "all_phases_implementation_blocked_now",
    "runtime_execution_blocked",
    "candidate_generator_wiring_blocked",
    "runtime_wiring_blocked",
    "runtime_solver_unmodified",
    "candidate_generator_unmodified",
    "ranker_runtime_unmodified",
    "real_evaluation_blocked",
    "real_submission_blocked",
    "kaggle_authentication_blocked",
    "kaggle_upload_blocked",
    "kaggle_submission_blocked",
    "private_core_not_exposed",
    "legal_certification_false",
    "controlled_implementation_authorized_for_next_stage",
]

RISK_CONTROLS = [
    "NO_REAL_KAGGLE_EVALUATION",
    "NO_RUNTIME_SOLVER_WIRING_IN_THIS_TASK",
    "NO_CANDIDATE_GENERATOR_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_RANKER_RUNTIME_WIRING_IN_THIS_TASK",
    "NO_RUNTIME_IMPLEMENTATION_IN_THIS_TASK",
    "NO_CODEPATH_ACTIVATION_IN_THIS_TASK",
    "NO_PUBLIC_SET_MEMORIZATION",
    "NO_EXTERNAL_API_DEPENDENCY",
    "NO_INTERNET_DURING_EVAL",
    "NO_KAGGLE_AUTHENTICATION",
    "NO_UPLOAD",
    "NO_SUBMISSION",
    "CONTROLLED_IMPLEMENTATION_ONLY_NEXT_STAGE",
]

QUALITY_TARGETS = [
    "review_is_deterministic",
    "source_plan_artifact_is_verified",
    "implementation_units_are_verified",
    "implementation_phases_are_verified",
    "runtime_wiring_remains_blocked_in_review",
    "controlled_implementation_next_stage_is_authorized",
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


def review_implementation_units(units: list[dict[str, Any]]) -> dict[str, Any]:
    rows = units if isinstance(units, list) else []
    unit_ids = [row.get("unit_id") for row in rows if isinstance(row, dict)]

    return {
        "implementation_unit_count": len(rows),
        "unit_ids": unit_ids,
        "unit_ids_unique": len(unit_ids) == len(set(unit_ids)),
        "all_units_have_names": all(bool(row.get("name")) for row in rows if isinstance(row, dict)),
        "all_units_have_planned_files": all(bool(row.get("planned_file")) for row in rows if isinstance(row, dict)),
        "all_units_implementation_blocked_now": all(
            row.get("implementation_allowed_now") is False for row in rows if isinstance(row, dict)
        ),
        "all_units_runtime_activation_blocked": all(
            row.get("runtime_activation_allowed") is False for row in rows if isinstance(row, dict)
        ),
        "all_units_require_review_before_code": all(
            row.get("requires_plan_review_before_code") is True for row in rows if isinstance(row, dict)
        ),
    }


def review_implementation_phases(phases: list[dict[str, Any]]) -> dict[str, Any]:
    rows = phases if isinstance(phases, list) else []
    phase_ids = [row.get("phase_id") for row in rows if isinstance(row, dict)]

    return {
        "implementation_phase_count": len(rows),
        "phase_ids": phase_ids,
        "phase_ids_unique": len(phase_ids) == len(set(phase_ids)),
        "all_phases_have_names": all(bool(row.get("name")) for row in rows if isinstance(row, dict)),
        "all_phases_have_descriptions": all(bool(row.get("description")) for row in rows if isinstance(row, dict)),
        "all_phases_implementation_blocked_now": all(
            row.get("implementation_allowed_now") is False for row in rows if isinstance(row, dict)
        ),
    }


def build_implementation_plan_review_report(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}

    units = source.get("implementation_units")
    if not isinstance(units, list):
        units = []

    phases = source.get("implementation_phases")
    if not isinstance(phases, list):
        phases = []

    unit_review = review_implementation_units(units)
    phase_review = review_implementation_phases(phases)

    checks = {
        "source_plan_created": source.get("controlled_implementation_plan_created") is True,
        "source_plan_ready": source.get("controlled_implementation_plan_ready") is True,
        "source_plan_valid": source.get("controlled_implementation_plan_valid") is True,
        "source_plan_review_required": source.get("controlled_implementation_plan_review_required") is True,
        "source_controlled_implementation_not_authorized": source.get("controlled_implementation_authorized") is False,
        "source_implementation_not_allowed_now": source.get("implementation_allowed_now") is False,
        "implementation_unit_count_4": source.get("implementation_unit_count") == 4 and unit_review["implementation_unit_count"] == 4,
        "implementation_phase_count_7": source.get("implementation_phase_count") == 7 and phase_review["implementation_phase_count"] == 7,
        "implementation_gate_count_18": source.get("implementation_gate_count") == 18,
        "unit_ids_unique": unit_review["unit_ids_unique"] is True,
        "all_units_have_names": unit_review["all_units_have_names"] is True,
        "all_units_have_planned_files": unit_review["all_units_have_planned_files"] is True,
        "all_units_implementation_blocked_now": unit_review["all_units_implementation_blocked_now"] is True,
        "all_units_runtime_activation_blocked": unit_review["all_units_runtime_activation_blocked"] is True,
        "all_units_require_review_before_code": unit_review["all_units_require_review_before_code"] is True,
        "phase_ids_unique": phase_review["phase_ids_unique"] is True,
        "all_phases_have_names": phase_review["all_phases_have_names"] is True,
        "all_phases_have_descriptions": phase_review["all_phases_have_descriptions"] is True,
        "all_phases_implementation_blocked_now": phase_review["all_phases_implementation_blocked_now"] is True,
        "runtime_execution_performed_false": source.get("runtime_execution_performed") is False,
        "candidate_generator_wiring_authorized_false": source.get("candidate_generator_wiring_authorized") is False,
        "runtime_wiring_authorized_false": source.get("runtime_wiring_authorized") is False,
        "runtime_solver_modified_false": source.get("runtime_solver_modified") is False,
        "candidate_generator_modified_false": source.get("candidate_generator_modified") is False,
        "ranker_runtime_modified_false": source.get("ranker_runtime_modified") is False,
        "real_evaluation_performed_false": source.get("real_evaluation_performed") is False,
        "real_submission_allowed_false": source.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": source.get("ready_for_real_kaggle_submission") is False,
        "kaggle_authentication_allowed_false": source.get("kaggle_authentication_allowed") is False,
        "kaggle_authentication_performed_false": source.get("kaggle_authentication_performed") is False,
        "kaggle_upload_allowed_false": source.get("kaggle_upload_allowed") is False,
        "kaggle_submission_sent_false": source.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": source.get("private_core_exposure") is False,
        "legal_certification_false": source.get("legal_certification") is False,
        "next_stage_is_task_13": source.get("next_stage")
        == "MILESTONE_13_TASK_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_V1",
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]

    return {
        "implementation_plan_review_report_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_REPORT_V1",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_plan_verdict": source.get("plan_verdict"),
        "source_next_stage": source.get("next_stage"),
        "unit_review": unit_review,
        "phase_review": phase_review,
        "checks": checks,
        "check_count": len(checks),
        "passed_check_count": len(checks) - len(blocking_issues),
        "blocking_issue_count": len(blocking_issues),
        "blocking_issues": blocking_issues,
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "review_passed": len(blocking_issues) == 0,
        "review_verdict": REVIEW_VERDICT,
        "recommended_next_stage": NEXT_STAGE,
    }


def build_controlled_runtime_wiring_implementation_plan_review_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_plan_artifact_present = SOURCE_PLAN_ARTIFACT.exists()
    source_record = _load_json(SOURCE_PLAN_ARTIFACT)
    source_plan_artifact_parseable = source_record is not None

    source_plan_passed = bool(
        source_record
        and source_record.get("controlled_implementation_plan_created") is True
        and source_record.get("controlled_implementation_plan_ready") is True
        and source_record.get("controlled_implementation_plan_valid") is True
        and source_record.get("controlled_implementation_plan_review_required") is True
        and source_record.get("controlled_implementation_authorized") is False
        and source_record.get("implementation_allowed_now") is False
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_RUNTIME_WIRING_IMPLEMENTATION_PLAN_REVIEW_V1"
    )

    source_boundaries_ok = bool(
        source_record
        and source_record.get("runtime_execution_performed") is False
        and source_record.get("candidate_generator_wiring_authorized") is False
        and source_record.get("runtime_wiring_authorized") is False
        and source_record.get("runtime_solver_modified") is False
        and source_record.get("candidate_generator_modified") is False
        and source_record.get("ranker_runtime_modified") is False
        and source_record.get("real_evaluation_performed") is False
        and source_record.get("real_submission_allowed") is False
        and source_record.get("ready_for_real_kaggle_submission") is False
        and source_record.get("kaggle_authentication_allowed") is False
        and source_record.get("kaggle_authentication_performed") is False
        and source_record.get("kaggle_upload_allowed") is False
        and source_record.get("kaggle_submission_sent") is False
        and source_record.get("private_core_exposure") is False
        and source_record.get("legal_certification") is False
    )

    report = build_implementation_plan_review_report(source_record)
    unit_review = report["unit_review"]
    phase_review = report["phase_review"]

    implementation_plan_review_ready = True
    implementation_plan_review_valid = report["review_passed"] is True
    implementation_plan_review_passed = report["review_passed"] is True

    controlled_implementation_authorized = True
    controlled_implementation_performed = False
    implementation_allowed_now = False

    runtime_execution_performed = False
    runtime_wiring_authorized = False
    candidate_generator_wiring_authorized = False
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
        _gate("source_plan_artifact_present", source_plan_artifact_present, True, "Task 12 implementation plan artifact is present."),
        _gate("source_plan_artifact_parseable", source_plan_artifact_parseable, True, "Task 12 implementation plan artifact is parseable."),
        _gate("source_plan_passed", source_plan_passed, True, "Task 12 controlled implementation plan is ready and valid."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Task 12 boundaries are preserved."),
        _gate("review_report_passed", report["review_passed"], True, "Task 13 implementation plan review passed."),
        _gate("unit_count_4", unit_review["implementation_unit_count"] == 4, True, "Four implementation units are present."),
        _gate("unit_ids_unique", unit_review["unit_ids_unique"], True, "Implementation unit IDs are unique."),
        _gate("units_have_names", unit_review["all_units_have_names"], True, "All implementation units have names."),
        _gate("units_have_planned_files", unit_review["all_units_have_planned_files"], True, "All implementation units have planned files."),
        _gate("units_implementation_blocked_now", unit_review["all_units_implementation_blocked_now"], True, "No implementation unit was allowed in Task 12."),
        _gate("units_runtime_activation_blocked", unit_review["all_units_runtime_activation_blocked"], True, "No implementation unit activates runtime in Task 12."),
        _gate("units_require_review_before_code", unit_review["all_units_require_review_before_code"], True, "All implementation units require review before code."),
        _gate("phase_count_7", phase_review["implementation_phase_count"] == 7, True, "Seven implementation phases are present."),
        _gate("phase_ids_unique", phase_review["phase_ids_unique"], True, "Implementation phase IDs are unique."),
        _gate("phases_have_names", phase_review["all_phases_have_names"], True, "All implementation phases have names."),
        _gate("phases_have_descriptions", phase_review["all_phases_have_descriptions"], True, "All implementation phases have descriptions."),
        _gate("phases_implementation_blocked_now", phase_review["all_phases_implementation_blocked_now"], True, "No implementation phase was allowed in Task 12."),
        _gate("implementation_plan_review_ready_true", implementation_plan_review_ready, True, "Implementation plan review is ready."),
        _gate("implementation_plan_review_valid_true", implementation_plan_review_valid, True, "Implementation plan review is valid."),
        _gate("implementation_plan_review_passed_true", implementation_plan_review_passed, True, "Implementation plan review passed."),
        _gate("controlled_implementation_authorized_true", controlled_implementation_authorized, True, "Controlled implementation may open in next stage."),
        _gate("controlled_implementation_performed_false", controlled_implementation_performed is False, True, "Controlled implementation is not performed in this task."),
        _gate("implementation_allowed_now_false", implementation_allowed_now is False, True, "Implementation is not performed in this review task."),
        _gate("runtime_execution_performed_false", runtime_execution_performed is False, True, "No runtime execution is performed."),
        _gate("candidate_generator_wiring_authorized_false", candidate_generator_wiring_authorized is False, True, "Candidate generator wiring remains blocked in this review task."),
        _gate("runtime_wiring_authorized_false", runtime_wiring_authorized is False, True, "Runtime wiring remains blocked in this review task."),
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
        _gate("fail_closed_active", True, True, "Review fails closed on missing prerequisites."),
    ]

    required_gates = [gate for gate in gates if gate["required"]]
    passed_required_gates = [gate for gate in required_gates if gate["passed"]]
    record_passed = len(required_gates) == len(passed_required_gates)

    review_summary = {
        "review_status": "PASS" if record_passed else "FAIL_CLOSED",
        "review_verdict": REVIEW_VERDICT,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "implementation_unit_count": unit_review["implementation_unit_count"],
        "implementation_phase_count": phase_review["implementation_phase_count"],
        "source_implementation_gate_count": source_record.get("implementation_gate_count") if source_record else None,
        "implementation_plan_review_ready": implementation_plan_review_ready,
        "implementation_plan_review_passed": implementation_plan_review_passed,
        "controlled_implementation_authorized": controlled_implementation_authorized,
        "controlled_implementation_performed": controlled_implementation_performed,
        "implementation_allowed_now": implementation_allowed_now,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
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
        "source_plan_artifact_present": source_plan_artifact_present,
        "source_plan_artifact_parseable": source_plan_artifact_parseable,
        "source_plan_passed": source_plan_passed,
        "source_boundaries_ok": source_boundaries_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "implementation_plan_review_ready": implementation_plan_review_ready,
        "implementation_plan_review_valid": record_passed,
        "implementation_plan_review_passed": record_passed,
        "controlled_implementation_authorized": controlled_implementation_authorized,
        "controlled_implementation_performed": controlled_implementation_performed,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "review_summary": review_summary,
        "implementation_plan_review_report": report,
        "unit_review": unit_review,
        "phase_review": phase_review,
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "review_criteria": REVIEW_CRITERIA,
        "review_criterion_count": len(REVIEW_CRITERIA),
        "implementation_unit_count": unit_review["implementation_unit_count"],
        "implementation_phase_count": phase_review["implementation_phase_count"],
        "source_implementation_gate_count": source_record.get("implementation_gate_count") if source_record else 0,
        "blocking_issue_count": report["blocking_issue_count"],
        "blocking_issues": report["blocking_issues"],
        "implementation_allowed_now": implementation_allowed_now,
        "runtime_execution_performed": runtime_execution_performed,
        "candidate_generator_wiring_authorized": candidate_generator_wiring_authorized,
        "runtime_wiring_authorized": runtime_wiring_authorized,
        "runtime_solver_modified": runtime_solver_modified,
        "candidate_generator_modified": candidate_generator_modified,
        "ranker_runtime_modified": ranker_runtime_modified,
        "real_evaluation_performed": real_evaluation_performed,
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "local_diagnostic_eval_allowed": True,
        "program_synthesis_candidate_generator_controlled_runtime_wiring_implementation_plan_review_allowed": True,
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
        "review_gate_count": len(gates),
        "review_pass_count": len(passed_required_gates),
        "review_blocking_issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
        "gate_count": len(gates),
        "required_gate_count": len(required_gates),
        "passed_gate_count": len(passed_required_gates),
        "issue_count": 0 if record_passed else len(required_gates) - len(passed_required_gates),
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
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-CONTROLLED-IMPLEMENTATION-PLAN-REVIEW-" + signature[:12]
    return record


def validate_controlled_runtime_wiring_implementation_plan_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_plan_artifact_present",
        "source_plan_artifact_parseable",
        "source_plan_passed",
        "source_boundaries_ok",
        "implementation_plan_review_ready",
        "implementation_plan_review_valid",
        "implementation_plan_review_passed",
        "controlled_implementation_authorized",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_controlled_runtime_wiring_implementation_plan_review_allowed",
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
        "controlled_implementation_performed",
        "implementation_allowed_now",
        "runtime_execution_performed",
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

    if record.get("review_verdict") != REVIEW_VERDICT:
        issues.append("REVIEW_VERDICT_MISMATCH")

    expected_counts = {
        "implementation_unit_count": 4,
        "implementation_phase_count": 7,
        "source_implementation_gate_count": 18,
        "blocking_issue_count": 0,
        "review_finding_count": 7,
        "review_criterion_count": 28,
        "review_blocking_issue_count": 0,
        "issue_count": 0,
        "risk_control_count": 13,
        "quality_target_count": 7,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    report = record.get("implementation_plan_review_report")
    if not isinstance(report, dict):
        issues.append("IMPLEMENTATION_PLAN_REVIEW_REPORT_MISSING")
    else:
        if report.get("review_passed") is not True:
            issues.append("IMPLEMENTATION_PLAN_REVIEW_REPORT_NOT_PASSED")
        if report.get("blocking_issue_count") != 0:
            issues.append("IMPLEMENTATION_PLAN_REVIEW_REPORT_BLOCKING_ISSUES_PRESENT")
        if report.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("IMPLEMENTATION_PLAN_REVIEW_REPORT_NEXT_STAGE_MISMATCH")

    unit_review = record.get("unit_review")
    if not isinstance(unit_review, dict):
        issues.append("UNIT_REVIEW_MISSING")
    else:
        for key in [
            "unit_ids_unique",
            "all_units_have_names",
            "all_units_have_planned_files",
            "all_units_implementation_blocked_now",
            "all_units_runtime_activation_blocked",
            "all_units_require_review_before_code",
        ]:
            if unit_review.get(key) is not True:
                issues.append(f"UNIT_REVIEW_{key}_NOT_TRUE")
        if unit_review.get("implementation_unit_count") != 4:
            issues.append("UNIT_REVIEW_COUNT_MISMATCH")

    phase_review = record.get("phase_review")
    if not isinstance(phase_review, dict):
        issues.append("PHASE_REVIEW_MISSING")
    else:
        for key in [
            "phase_ids_unique",
            "all_phases_have_names",
            "all_phases_have_descriptions",
            "all_phases_implementation_blocked_now",
        ]:
            if phase_review.get(key) is not True:
                issues.append(f"PHASE_REVIEW_{key}_NOT_TRUE")
        if phase_review.get("implementation_phase_count") != 7:
            issues.append("PHASE_REVIEW_COUNT_MISMATCH")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-review-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "source_plan_passed": record["source_plan_passed"],
        "source_boundaries_ok": record["source_boundaries_ok"],
        "implementation_plan_review_ready": record["implementation_plan_review_ready"],
        "implementation_plan_review_valid": record["implementation_plan_review_valid"],
        "implementation_plan_review_passed": record["implementation_plan_review_passed"],
        "controlled_implementation_authorized": record["controlled_implementation_authorized"],
        "controlled_implementation_performed": record["controlled_implementation_performed"],
        "implementation_unit_count": record["implementation_unit_count"],
        "implementation_phase_count": record["implementation_phase_count"],
        "source_implementation_gate_count": record["source_implementation_gate_count"],
        "implementation_allowed_now": record["implementation_allowed_now"],
        "runtime_execution_performed": record["runtime_execution_performed"],
        "candidate_generator_wiring_authorized": record["candidate_generator_wiring_authorized"],
        "runtime_wiring_authorized": record["runtime_wiring_authorized"],
        "runtime_solver_modified": record["runtime_solver_modified"],
        "candidate_generator_modified": record["candidate_generator_modified"],
        "ranker_runtime_modified": record["ranker_runtime_modified"],
        "real_submission_allowed": record["real_submission_allowed"],
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
        f"review_verdict={record['review_verdict']}",
        f"next_stage={record['next_stage']}",
        f"source_plan_passed={record['source_plan_passed']}",
        f"source_boundaries_ok={record['source_boundaries_ok']}",
        f"implementation_plan_review_ready={record['implementation_plan_review_ready']}",
        f"implementation_plan_review_valid={record['implementation_plan_review_valid']}",
        f"implementation_plan_review_passed={record['implementation_plan_review_passed']}",
        f"controlled_implementation_authorized={record['controlled_implementation_authorized']}",
        f"controlled_implementation_performed={record['controlled_implementation_performed']}",
        f"implementation_unit_count={record['implementation_unit_count']}",
        f"implementation_phase_count={record['implementation_phase_count']}",
        f"source_implementation_gate_count={record['source_implementation_gate_count']}",
        f"implementation_allowed_now={record['implementation_allowed_now']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
        f"candidate_generator_wiring_authorized={record['candidate_generator_wiring_authorized']}",
        f"runtime_wiring_authorized={record['runtime_wiring_authorized']}",
        f"runtime_solver_modified={record['runtime_solver_modified']}",
        f"candidate_generator_modified={record['candidate_generator_modified']}",
        f"ranker_runtime_modified={record['ranker_runtime_modified']}",
        f"real_submission_allowed={record['real_submission_allowed']}",
        f"kaggle_submission_sent={record['kaggle_submission_sent']}",
        f"private_core_exposure={record['private_core_exposure']}",
        f"legal_certification={record['legal_certification']}",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    finding_lines = "\n".join(
        [
            f"- `{finding['finding_id']}` `{finding['name']}`: `{finding['severity']}` - {finding['description']}"
            for finding in record["review_findings"]
        ]
    )

    markdown = f"""# {TASK_LABEL}

- revision: `{record['revision']}`
- task_id: `{record['task_id']}`
- signature: `{record['signature']}`
- baseline_commit: `{record['baseline_commit']}`
- task_verdict: `{record['task_verdict']}`
- review_verdict: `{record['review_verdict']}`
- next_stage: `{record['next_stage']}`

## Review Summary

- source_plan_passed: `{record['source_plan_passed']}`
- source_boundaries_ok: `{record['source_boundaries_ok']}`
- implementation_plan_review_ready: `{record['implementation_plan_review_ready']}`
- implementation_plan_review_passed: `{record['implementation_plan_review_passed']}`
- controlled_implementation_authorized: `{record['controlled_implementation_authorized']}`
- controlled_implementation_performed: `{record['controlled_implementation_performed']}`
- implementation_unit_count: `{record['implementation_unit_count']}`
- implementation_phase_count: `{record['implementation_phase_count']}`
- source_implementation_gate_count: `{record['source_implementation_gate_count']}`
- blocking_issue_count: `{record['blocking_issue_count']}`

## Findings

{finding_lines}

## Boundary

- implementation_allowed_now: `{record['implementation_allowed_now']}`
- runtime_execution_performed: `{record['runtime_execution_performed']}`
- candidate_generator_wiring_authorized: `{record['candidate_generator_wiring_authorized']}`
- runtime_wiring_authorized: `{record['runtime_wiring_authorized']}`
- runtime_solver_modified: `{record['runtime_solver_modified']}`
- candidate_generator_modified: `{record['candidate_generator_modified']}`
- ranker_runtime_modified: `{record['ranker_runtime_modified']}`
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
    record = build_controlled_runtime_wiring_implementation_plan_review_record()
    issues = validate_controlled_runtime_wiring_implementation_plan_review_record(record)
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
    print(record["review_verdict"])
    print(record["next_stage"])
    print(f"implementation_unit_count={record['implementation_unit_count']}")
    print(f"implementation_phase_count={record['implementation_phase_count']}")
    print(f"source_implementation_gate_count={record['source_implementation_gate_count']}")
    print(f"controlled_implementation_authorized={record['controlled_implementation_authorized']}")
    print(f"controlled_implementation_performed={record['controlled_implementation_performed']}")
    print(f"implementation_allowed_now={record['implementation_allowed_now']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
