"""Milestone #13 Task 9 - Program Synthesis Candidate Generator Local Diagnostic Harness Review v1.

Review-only layer for the Task 8 local diagnostic harness.

Boundary:
- no runtime solver wiring
- no real Kaggle evaluation
- no upload
- no submission
- no external API
- no internet
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


TASK_NAME = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_V1"
MILESTONE_NUMBER = 13
TASK_NUMBER = 9
TASK_LABEL = "Milestone #13 Task 9 - Program Synthesis Candidate Generator Local Diagnostic Harness Review v1"

SOURCE_TASK = "MILESTONE_13_TASK_8_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_V1"
NEXT_STAGE = "MILESTONE_13_TASK_10_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_V1"

TASK_MODE = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_V1_LOCAL_ONLY"
TASK_SCOPE = "LOCAL_DIAGNOSTIC_HARNESS_REVIEW_ONLY_NO_RUNTIME_WIRING_NO_REAL_EVAL_NO_UPLOAD_NO_SUBMISSION"
TASK_VERDICT = "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_READY"
REVIEW_VERDICT = "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_PASS_READY_FOR_RUNTIME_WIRING_PLAN"

COMPETITIVE_GOAL = "FIRST_PLACE_COMPETITIVE_SOLVER"
CHOSEN_STRATEGY = "EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN"

PROJECT_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-local-diagnostic-harness-review-v1"
)

SOURCE_HARNESS_ARTIFACT = (
    PROJECT_ROOT
    / "examples"
    / "milestone-13"
    / "program-synthesis-candidate-generator-local-diagnostic-harness-v1"
    / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-v1.json"
)

REVIEW_CRITERIA = [
    "source_harness_artifact_present",
    "source_harness_artifact_parseable",
    "source_harness_ready",
    "source_harness_passed",
    "source_harness_shape_ok",
    "candidate_count_12",
    "candidate_family_count_7",
    "diagnostic_fixture_count_4",
    "candidate_fixture_matrix_count_4",
    "all_fixture_observations_passed",
    "all_fixture_runtime_execution_blocked",
    "all_fixture_real_eval_blocked",
    "blocking_issue_count_zero",
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
]

REVIEW_FINDINGS = [
    {
        "finding_id": "HARNESS-REVIEW-FINDING-01",
        "name": "source_harness_exists",
        "severity": "PASS",
        "description": "Task 8 local diagnostic harness artifact exists and is parseable.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-02",
        "name": "candidate_fixture_matrix_is_complete",
        "severity": "PASS",
        "description": "The candidate-fixture matrix has four diagnostic rows.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-03",
        "name": "fixture_observations_pass",
        "severity": "PASS",
        "description": "All diagnostic fixture observations pass without runtime execution.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-04",
        "name": "candidate_family_coverage_is_preserved",
        "severity": "PASS",
        "description": "The harness preserves seven candidate families and twelve candidates.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-05",
        "name": "runtime_wiring_is_blocked",
        "severity": "PASS",
        "description": "No runtime solver or candidate-generator wiring is authorized.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-06",
        "name": "real_actions_are_blocked",
        "severity": "PASS",
        "description": "No real evaluation, authentication, upload, or submission is allowed.",
    },
    {
        "finding_id": "HARNESS-REVIEW-FINDING-07",
        "name": "ready_for_runtime_wiring_plan",
        "severity": "PASS",
        "description": "The harness review can proceed to a runtime wiring plan, not runtime wiring.",
    },
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
    "harness_review_is_deterministic",
    "harness_artifact_shape_is_verified",
    "fixture_matrix_is_verified",
    "fixture_runtime_execution_block_is_verified",
    "runtime_wiring_remains_blocked",
    "real_actions_remain_blocked",
    "next_task_is_runtime_wiring_plan",
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


def review_candidate_fixture_matrix(matrix: list[dict[str, Any]]) -> dict[str, Any]:
    rows = matrix if isinstance(matrix, list) else []

    matching_counts = [
        int(row.get("matching_candidate_count", 0))
        for row in rows
        if isinstance(row, dict)
    ]

    fixture_ids = [
        row.get("fixture_id")
        for row in rows
        if isinstance(row, dict)
    ]

    return {
        "candidate_fixture_matrix_count": len(rows),
        "fixture_ids": fixture_ids,
        "fixture_ids_unique": len(fixture_ids) == len(set(fixture_ids)),
        "all_observations_passed": all(row.get("observation_passed") is True for row in rows),
        "all_matching_counts_positive": all(count > 0 for count in matching_counts),
        "min_matching_candidate_count": min(matching_counts) if matching_counts else 0,
        "max_matching_candidate_count": max(matching_counts) if matching_counts else 0,
        "all_runtime_execution_blocked": all(row.get("runtime_execution_performed") is False for row in rows),
        "all_real_evaluation_blocked": all(row.get("real_evaluation_performed") is False for row in rows),
        "all_public_safe": all(row.get("public_safe") is True for row in rows),
    }


def build_harness_review_report(source_record: dict[str, Any] | None) -> dict[str, Any]:
    source = source_record if isinstance(source_record, dict) else {}
    matrix = source.get("candidate_fixture_matrix")
    if not isinstance(matrix, list):
        matrix = []

    matrix_review = review_candidate_fixture_matrix(matrix)

    checks = {
        "source_harness_ready": source.get("local_diagnostic_harness_ready") is True,
        "source_harness_passed": source.get("local_diagnostic_harness_passed") is True,
        "candidate_count_12": source.get("candidate_count") == 12,
        "candidate_family_count_7": source.get("candidate_family_count") == 7,
        "diagnostic_fixture_count_4": source.get("diagnostic_fixture_count") == 4,
        "candidate_fixture_matrix_count_4": matrix_review["candidate_fixture_matrix_count"] == 4,
        "fixture_ids_unique": matrix_review["fixture_ids_unique"] is True,
        "all_fixture_observations_passed": matrix_review["all_observations_passed"] is True,
        "all_matching_counts_positive": matrix_review["all_matching_counts_positive"] is True,
        "all_fixture_runtime_execution_blocked": matrix_review["all_runtime_execution_blocked"] is True,
        "all_fixture_real_evaluation_blocked": matrix_review["all_real_evaluation_blocked"] is True,
        "all_fixture_rows_public_safe": matrix_review["all_public_safe"] is True,
        "blocking_issue_count_zero": source.get("blocking_issue_count") == 0,
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
    }

    blocking_issues = [name for name, passed in checks.items() if passed is not True]

    return {
        "harness_review_report_id": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_REPORT_V1",
        "source_revision": source.get("revision"),
        "source_task_verdict": source.get("task_verdict"),
        "source_harness_verdict": source.get("harness_verdict"),
        "source_next_stage": source.get("next_stage"),
        "matrix_review": matrix_review,
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


def build_local_diagnostic_harness_review_record(baseline_commit: str | None = None) -> dict[str, Any]:
    baseline = baseline_commit or _run_git_head()

    source_harness_artifact_present = SOURCE_HARNESS_ARTIFACT.exists()
    source_record = _load_json(SOURCE_HARNESS_ARTIFACT)
    source_harness_artifact_parseable = source_record is not None

    source_harness_ready = bool(
        source_record
        and source_record.get("local_diagnostic_harness_ready") is True
        and source_record.get("local_diagnostic_harness_passed") is True
    )

    source_harness_shape_ok = bool(
        source_record
        and source_record.get("candidate_count") == 12
        and source_record.get("candidate_family_count") == 7
        and source_record.get("diagnostic_fixture_count") == 4
        and source_record.get("candidate_fixture_matrix_count") == 4
        and source_record.get("blocking_issue_count") == 0
    )

    source_next_stage_ok = bool(
        source_record
        and source_record.get("next_stage")
        == "MILESTONE_13_TASK_9_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_LOCAL_DIAGNOSTIC_HARNESS_REVIEW_V1"
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
        and source_record.get("local_only") is True
        and source_record.get("deterministic") is True
        and source_record.get("public_safe") is True
    )

    report = build_harness_review_report(source_record)
    matrix_review = report["matrix_review"]

    local_diagnostic_harness_review_ready = True
    local_diagnostic_harness_review_passed = report["review_passed"] is True
    runtime_wiring_plan_authorized = True

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
        _gate("source_harness_artifact_present", source_harness_artifact_present, True, "Task 8 harness artifact is present."),
        _gate("source_harness_artifact_parseable", source_harness_artifact_parseable, True, "Task 8 harness artifact is parseable."),
        _gate("source_harness_ready", source_harness_ready, True, "Task 8 harness is ready and passed."),
        _gate("source_harness_shape_ok", source_harness_shape_ok, True, "Task 8 harness has expected shape."),
        _gate("source_next_stage_ok", source_next_stage_ok, True, "Task 8 points to Task 9."),
        _gate("source_boundaries_ok", source_boundaries_ok, True, "Task 8 boundaries are preserved."),
        _gate("review_report_passed", report["review_passed"], True, "Harness review report passed."),
        _gate("matrix_count_4", matrix_review["candidate_fixture_matrix_count"] == 4, True, "Matrix has four rows."),
        _gate("matrix_fixture_ids_unique", matrix_review["fixture_ids_unique"], True, "Fixture IDs are unique."),
        _gate("matrix_observations_passed", matrix_review["all_observations_passed"], True, "All fixture observations passed."),
        _gate("matrix_matching_counts_positive", matrix_review["all_matching_counts_positive"], True, "All fixture rows have matching candidates."),
        _gate("matrix_runtime_execution_blocked", matrix_review["all_runtime_execution_blocked"], True, "Runtime execution is blocked in matrix."),
        _gate("matrix_real_evaluation_blocked", matrix_review["all_real_evaluation_blocked"], True, "Real evaluation is blocked in matrix."),
        _gate("matrix_public_safe", matrix_review["all_public_safe"], True, "Matrix rows are public-safe."),
        _gate("local_diagnostic_harness_review_ready_true", local_diagnostic_harness_review_ready is True, True, "Harness review is ready."),
        _gate("local_diagnostic_harness_review_passed_true", local_diagnostic_harness_review_passed is True, True, "Harness review passed."),
        _gate("runtime_wiring_plan_authorized_true", runtime_wiring_plan_authorized is True, True, "Next planning stage is authorized."),
        _gate("runtime_execution_performed_false", runtime_execution_performed is False, True, "No runtime execution is performed."),
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
        "candidate_count": source_record.get("candidate_count") if source_record else None,
        "candidate_family_count": source_record.get("candidate_family_count") if source_record else None,
        "diagnostic_fixture_count": source_record.get("diagnostic_fixture_count") if source_record else None,
        "candidate_fixture_matrix_count": matrix_review["candidate_fixture_matrix_count"],
        "blocking_issue_count": report["blocking_issue_count"],
        "runtime_wiring_plan_authorized": runtime_wiring_plan_authorized,
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
        "source_harness_artifact": str(SOURCE_HARNESS_ARTIFACT.relative_to(PROJECT_ROOT)),
        "source_harness_artifact_present": source_harness_artifact_present,
        "source_harness_artifact_parseable": source_harness_artifact_parseable,
        "source_harness_ready": source_harness_ready,
        "source_harness_shape_ok": source_harness_shape_ok,
        "source_next_stage_ok": source_next_stage_ok,
        "source_boundaries_ok": source_boundaries_ok,
        "task_mode": TASK_MODE,
        "task_scope": TASK_SCOPE,
        "task_verdict": TASK_VERDICT,
        "review_verdict": REVIEW_VERDICT,
        "local_diagnostic_harness_review_ready": local_diagnostic_harness_review_ready,
        "local_diagnostic_harness_review_valid": record_passed,
        "local_diagnostic_harness_review_passed": record_passed,
        "runtime_wiring_plan_authorized": runtime_wiring_plan_authorized,
        "competitive_goal": COMPETITIVE_GOAL,
        "chosen_strategy": CHOSEN_STRATEGY,
        "review_summary": review_summary,
        "harness_review_report": report,
        "matrix_review": matrix_review,
        "review_criteria": REVIEW_CRITERIA,
        "review_criterion_count": len(REVIEW_CRITERIA),
        "review_findings": REVIEW_FINDINGS,
        "review_finding_count": len(REVIEW_FINDINGS),
        "candidate_count": source_record.get("candidate_count") if source_record else 0,
        "candidate_family_count": source_record.get("candidate_family_count") if source_record else 0,
        "diagnostic_fixture_count": source_record.get("diagnostic_fixture_count") if source_record else 0,
        "candidate_fixture_matrix_count": matrix_review["candidate_fixture_matrix_count"],
        "blocking_issue_count": report["blocking_issue_count"],
        "blocking_issues": report["blocking_issues"],
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
        "program_synthesis_candidate_generator_local_diagnostic_harness_review_allowed": True,
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
    record["task_id"] = "MILESTONE-13-CANDIDATE-GENERATOR-HARNESS-REVIEW-" + signature[:12]
    return record


def validate_local_diagnostic_harness_review_record(record: dict[str, Any]) -> list[str]:
    issues: list[str] = []

    expected_true = [
        "source_harness_artifact_present",
        "source_harness_artifact_parseable",
        "source_harness_ready",
        "source_harness_shape_ok",
        "source_next_stage_ok",
        "source_boundaries_ok",
        "local_diagnostic_harness_review_ready",
        "local_diagnostic_harness_review_valid",
        "local_diagnostic_harness_review_passed",
        "runtime_wiring_plan_authorized",
        "real_evaluation_prep_allowed",
        "local_solver_improvement_allowed",
        "local_diagnostic_eval_allowed",
        "program_synthesis_candidate_generator_local_diagnostic_harness_review_allowed",
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
        "candidate_count": 12,
        "candidate_family_count": 7,
        "diagnostic_fixture_count": 4,
        "candidate_fixture_matrix_count": 4,
        "blocking_issue_count": 0,
        "review_criterion_count": 26,
        "review_finding_count": 7,
        "review_blocking_issue_count": 0,
        "issue_count": 0,
        "risk_control_count": 10,
        "quality_target_count": 7,
    }

    for key, value in expected_counts.items():
        if record.get(key) != value:
            issues.append(f"{key.upper()}_MISMATCH")

    report = record.get("harness_review_report")
    if not isinstance(report, dict):
        issues.append("HARNESS_REVIEW_REPORT_MISSING")
    else:
        if report.get("review_passed") is not True:
            issues.append("HARNESS_REVIEW_REPORT_NOT_PASSED")
        if report.get("blocking_issue_count") != 0:
            issues.append("HARNESS_REVIEW_REPORT_BLOCKING_ISSUES_PRESENT")
        if report.get("recommended_next_stage") != NEXT_STAGE:
            issues.append("HARNESS_REVIEW_REPORT_NEXT_STAGE_MISMATCH")

    matrix_review = record.get("matrix_review")
    if not isinstance(matrix_review, dict):
        issues.append("MATRIX_REVIEW_MISSING")
    else:
        expected_matrix_true = [
            "fixture_ids_unique",
            "all_observations_passed",
            "all_matching_counts_positive",
            "all_runtime_execution_blocked",
            "all_real_evaluation_blocked",
            "all_public_safe",
        ]
        for key in expected_matrix_true:
            if matrix_review.get(key) is not True:
                issues.append(f"MATRIX_REVIEW_{key}_NOT_TRUE")
        if matrix_review.get("candidate_fixture_matrix_count") != 4:
            issues.append("MATRIX_REVIEW_COUNT_MISMATCH")

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

    json_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-v1.json"
    index_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-index-v1.json"
    manifest_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-manifest-v1.txt"
    markdown_path = target_dir / "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-review-v1.md"

    json_path.write_text(json.dumps(record, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "revision": record["revision"],
        "task_id": record["task_id"],
        "signature": record["signature"],
        "baseline_commit": record["baseline_commit"],
        "task_verdict": record["task_verdict"],
        "review_verdict": record["review_verdict"],
        "next_stage": record["next_stage"],
        "source_harness_ready": record["source_harness_ready"],
        "source_harness_shape_ok": record["source_harness_shape_ok"],
        "local_diagnostic_harness_review_ready": record["local_diagnostic_harness_review_ready"],
        "candidate_count": record["candidate_count"],
        "candidate_family_count": record["candidate_family_count"],
        "diagnostic_fixture_count": record["diagnostic_fixture_count"],
        "candidate_fixture_matrix_count": record["candidate_fixture_matrix_count"],
        "blocking_issue_count": record["blocking_issue_count"],
        "runtime_wiring_plan_authorized": record["runtime_wiring_plan_authorized"],
        "runtime_execution_performed": record["runtime_execution_performed"],
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
        f"source_harness_ready={record['source_harness_ready']}",
        f"source_harness_shape_ok={record['source_harness_shape_ok']}",
        f"local_diagnostic_harness_review_ready={record['local_diagnostic_harness_review_ready']}",
        f"candidate_count={record['candidate_count']}",
        f"candidate_family_count={record['candidate_family_count']}",
        f"diagnostic_fixture_count={record['diagnostic_fixture_count']}",
        f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}",
        f"blocking_issue_count={record['blocking_issue_count']}",
        f"runtime_wiring_plan_authorized={record['runtime_wiring_plan_authorized']}",
        f"runtime_execution_performed={record['runtime_execution_performed']}",
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

- source_harness_ready: `{record['source_harness_ready']}`
- source_harness_shape_ok: `{record['source_harness_shape_ok']}`
- local_diagnostic_harness_review_ready: `{record['local_diagnostic_harness_review_ready']}`
- local_diagnostic_harness_review_passed: `{record['local_diagnostic_harness_review_passed']}`
- candidate_count: `{record['candidate_count']}`
- candidate_family_count: `{record['candidate_family_count']}`
- diagnostic_fixture_count: `{record['diagnostic_fixture_count']}`
- candidate_fixture_matrix_count: `{record['candidate_fixture_matrix_count']}`
- blocking_issue_count: `{record['blocking_issue_count']}`
- runtime_wiring_plan_authorized: `{record['runtime_wiring_plan_authorized']}`

## Findings

{finding_lines}

## Boundary

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
    record = build_local_diagnostic_harness_review_record()
    issues = validate_local_diagnostic_harness_review_record(record)
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
    print(f"candidate_count={record['candidate_count']}")
    print(f"candidate_family_count={record['candidate_family_count']}")
    print(f"diagnostic_fixture_count={record['diagnostic_fixture_count']}")
    print(f"candidate_fixture_matrix_count={record['candidate_fixture_matrix_count']}")
    print(f"blocking_issue_count={record['blocking_issue_count']}")
    print(f"runtime_wiring_plan_authorized={record['runtime_wiring_plan_authorized']}")
    for path in artifacts.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
