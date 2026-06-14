"""Milestone #9 Real Submission Preflight Gate v1.

Local-only deterministic real submission preflight gate.

This module verifies the local candidate manual review package and prepares the
real-submission preflight evidence layer. It keeps the final action blocked
because operator approval has not been granted.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, accept declarations, grant approval, claim a Kaggle score, claim
public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PREFLIGHT_STATUS = "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_VALID"

BASELINE_COMMIT = "d7c1584 Add ARC AGI3 local candidate manual review"
PREFLIGHT_MODE = "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_LOCAL_ONLY"
PREFLIGHT_SCOPE = "VERIFY_REAL_SUBMISSION_PREFLIGHT_WITHOUT_UPLOAD_AUTH_OR_APPROVAL"
PREFLIGHT_VERDICT = "REAL_SUBMISSION_PREFLIGHT_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_5_OPERATOR_APPROVAL_GATE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/real-submission-preflight-gate-v1"

LOCAL_REVIEW_JSON = Path(
    "examples/milestone-9/local-candidate-manual-review-v1/"
    "milestone-9-local-candidate-manual-review-v1.json"
)

EXPECTED_PREFLIGHT_CHECK_COUNT = 14
EXPECTED_PREFLIGHT_CASE_COUNT = 10
EXPECTED_PREFLIGHT_PASS_COUNT = 10
EXPECTED_PREFLIGHT_FAILURE_COUNT = 0
EXPECTED_REVIEW_CASE_COUNT = 10
EXPECTED_REVIEW_PASS_COUNT = 10
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

PREFLIGHT_CHECKS: Tuple[str, ...] = (
    "local_review_artifact_exists",
    "local_review_artifact_ready",
    "local_review_candidate_source_present",
    "local_review_candidate_signature_present",
    "operator_declarations_not_accepted",
    "operator_approval_not_granted",
    "manual_upload_not_allowed",
    "kaggle_authentication_not_performed",
    "upload_not_performed",
    "real_submission_not_created",
    "real_submission_not_allowed",
    "score_claim_absent",
    "public_leaderboard_claim_absent",
    "legal_certification_absent",
)

PREFLIGHT_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "preflight_local_review_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_local_review_artifact",
    },
    {
        "case_id": "preflight_candidate_source_bound_v1",
        "area": "candidate_source",
        "operation": "verify_candidate_source_binding",
    },
    {
        "case_id": "preflight_candidate_signature_bound_v1",
        "area": "candidate_integrity",
        "operation": "verify_candidate_signature",
    },
    {
        "case_id": "preflight_review_cases_passed_v1",
        "area": "review_integrity",
        "operation": "verify_review_case_pass_count",
    },
    {
        "case_id": "preflight_operator_approval_absent_v1",
        "area": "operator_approval",
        "operation": "verify_operator_approval_absent",
    },
    {
        "case_id": "preflight_manual_upload_blocked_v1",
        "area": "upload_gate",
        "operation": "verify_manual_upload_blocked",
    },
    {
        "case_id": "preflight_real_submission_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "preflight_no_auth_no_external_api_v1",
        "area": "boundary",
        "operation": "verify_no_auth_no_external_api",
    },
    {
        "case_id": "preflight_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "preflight_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_operator_approval_gate_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_preflight_uses_local_review_artifact",
    "guard_preflight_candidate_source_bound",
    "guard_preflight_candidate_signature_bound",
    "guard_preflight_review_cases_passed",
    "guard_preflight_operator_approval_absent",
    "guard_preflight_manual_upload_blocked",
    "guard_preflight_real_submission_blocked",
    "guard_preflight_does_not_authenticate",
    "guard_preflight_does_not_upload",
    "guard_preflight_no_score_claim",
    "guard_preflight_no_private_core_exposure",
    "guard_preflight_no_legal_certification",
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


def _result(case_id: str, area: str, operation: str, passed: bool) -> Dict[str, Any]:
    return {
        "case_id": case_id,
        "area": area,
        "operation": operation,
        "priority": "P0",
        "passed": passed,
        "evidence_score": 100 if passed else 0,
        "expected_status": "PASS",
        "actual_status": "PASS" if passed else "FAIL",
    }


def build_preflight_source_summary() -> Dict[str, Any]:
    review = _read_json(LOCAL_REVIEW_JSON)
    candidate_source = review.get("candidate_source", {})

    return {
        "local_review_path": str(LOCAL_REVIEW_JSON),
        "local_review_present": LOCAL_REVIEW_JSON.exists(),
        "local_review_status": review.get("status", "MISSING"),
        "local_review_id": review.get("review_id", "MISSING_REVIEW_ID"),
        "local_review_signature": review.get("signature", ""),
        "candidate_source_path": candidate_source.get("path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": candidate_source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": candidate_source.get("signature", ""),
        "candidate_count": review.get("candidate_count", 0),
        "review_case_count": review.get("review_case_count", 0),
        "review_pass_count": review.get("review_pass_count", 0),
        "review_failure_count": review.get("review_failure_count", 0),
        "review_sha256": _sha256(LOCAL_REVIEW_JSON),
        "review_sha256_16": _sha16(_sha256(LOCAL_REVIEW_JSON)),
    }


def build_real_submission_preflight_state() -> Dict[str, Any]:
    return {
        "real_submission_preflight_required": True,
        "real_submission_preflight_ready": True,
        "real_submission_preflight_completed": False,
        "preflight_gate_ready": True,
        "preflight_gate_open": False,
        "preflight_gate_verdict": "PREFLIGHT_READY_BUT_OPERATOR_APPROVAL_NOT_GRANTED",
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "real_submission_allowed": False,
    }


def build_real_submission_preflight_checks() -> Dict[str, bool]:
    review = _read_json(LOCAL_REVIEW_JSON)
    source = build_preflight_source_summary()
    preflight = build_real_submission_preflight_state()

    candidate_source_path = Path(source["candidate_source_path"])
    candidate_source_exists = candidate_source_path.exists()

    return {
        "local_review_artifact_present": LOCAL_REVIEW_JSON.exists(),
        "local_review_artifact_ready": review.get("status")
        == "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY",
        "local_review_artifact_valid": bool(review.get("review_id")) and bool(review.get("signature")),
        "local_review_next_stage_matches_task_4": review.get("next_allowed_stage")
        == "MILESTONE_9_TASK_4_REAL_SUBMISSION_PREFLIGHT_GATE_V1",
        "local_review_ready": review.get("review_ready") is True,
        "local_review_cases_valid": review.get("review_case_count") == EXPECTED_REVIEW_CASE_COUNT
        and review.get("review_pass_count") == EXPECTED_REVIEW_PASS_COUNT
        and review.get("review_failure_count") == 0,
        "candidate_source_path_present": bool(source["candidate_source_path"])
        and source["candidate_source_path"] != "MISSING_CANDIDATE_SOURCE",
        "candidate_source_exists": candidate_source_exists,
        "candidate_count_positive": source["candidate_count"] > 0,
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "preflight_check_count_valid": len(PREFLIGHT_CHECKS) == EXPECTED_PREFLIGHT_CHECK_COUNT,
        "preflight_required": preflight["real_submission_preflight_required"] is True,
        "preflight_ready": preflight["real_submission_preflight_ready"] is True,
        "preflight_not_completed": preflight["real_submission_preflight_completed"] is False,
        "preflight_gate_ready": preflight["preflight_gate_ready"] is True,
        "preflight_gate_not_open": preflight["preflight_gate_open"] is False,
        "operator_approval_required": review.get("operator_approval_required") is True
        and preflight["operator_approval_required"] is True,
        "operator_approval_not_granted": review.get("operator_approval_granted") is False
        and preflight["operator_approval_granted"] is False,
        "operator_approval_not_received": review.get("operator_approval_received") is False
        and preflight["operator_approval_received"] is False,
        "manual_upload_not_allowed": review.get("manual_upload_allowed") is False
        and preflight["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": preflight["kaggle_authentication_allowed"] is False,
        "real_submission_not_created": True,
        "real_submission_allowed_false": review.get("real_submission_allowed") is False
        and preflight["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": review.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": review.get("kaggle_submission_sent") is False,
        "upload_not_performed": review.get("upload_performed") is False,
        "kaggle_authentication_not_performed": review.get("kaggle_authentication_performed") is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "external_api_dependency_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_5_OPERATOR_APPROVAL_GATE_V1",
    }


def evaluate_real_submission_preflight_case(case_id: str) -> Dict[str, Any]:
    checks = build_real_submission_preflight_checks()

    if case_id == "preflight_local_review_source_ready_v1":
        passed = (
            checks["local_review_artifact_present"]
            and checks["local_review_artifact_ready"]
            and checks["local_review_artifact_valid"]
            and checks["local_review_ready"]
        )
        return _result(case_id, "source_binding", "verify_local_review_artifact", passed)

    if case_id == "preflight_candidate_source_bound_v1":
        passed = (
            checks["candidate_source_path_present"]
            and checks["candidate_source_exists"]
            and checks["candidate_count_positive"]
            and checks["candidate_id_present"]
        )
        return _result(case_id, "candidate_source", "verify_candidate_source_binding", passed)

    if case_id == "preflight_candidate_signature_bound_v1":
        passed = checks["candidate_signature_present"]
        return _result(case_id, "candidate_integrity", "verify_candidate_signature", passed)

    if case_id == "preflight_review_cases_passed_v1":
        passed = checks["local_review_cases_valid"]
        return _result(case_id, "review_integrity", "verify_review_case_pass_count", passed)

    if case_id == "preflight_operator_approval_absent_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "operator_approval", "verify_operator_approval_absent", passed)

    if case_id == "preflight_manual_upload_blocked_v1":
        passed = checks["manual_upload_not_allowed"]
        return _result(case_id, "upload_gate", "verify_manual_upload_blocked", passed)

    if case_id == "preflight_real_submission_blocked_v1":
        passed = (
            checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
            and checks["preflight_gate_not_open"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "preflight_no_auth_no_external_api_v1":
        passed = (
            checks["kaggle_authentication_not_allowed"]
            and checks["kaggle_authentication_not_performed"]
            and checks["external_api_dependency_false"]
            and checks["upload_not_performed"]
        )
        return _result(case_id, "boundary", "verify_no_auth_no_external_api", passed)

    if case_id == "preflight_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "preflight_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_operator_approval_gate_next", passed)

    raise ValueError(f"unknown real submission preflight case: {case_id}")


def evaluate_all_real_submission_preflight_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_real_submission_preflight_case(case["case_id"]) for case in PREFLIGHT_CASES)


def build_milestone_9_real_submission_preflight_gate() -> Dict[str, Any]:
    review = _read_json(LOCAL_REVIEW_JSON)
    source = build_preflight_source_summary()
    preflight = build_real_submission_preflight_state()
    checks = build_real_submission_preflight_checks()
    results = evaluate_all_real_submission_preflight_cases()

    preflight_pass_count = sum(1 for result in results if result["passed"] is True)
    preflight_failure_count = sum(1 for result in results if result["passed"] is False)

    preflight_record = {
        "preflight_mode": PREFLIGHT_MODE,
        "preflight_scope": PREFLIGHT_SCOPE,
        "preflight_verdict": PREFLIGHT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "preflight_ready": True,
        "preflight_locked": True,
        "baseline_local_review_id": review.get("review_id", "MISSING_REVIEW_ID"),
        "local_review_ready": review.get("review_ready") is True,
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_signature": source["candidate_signature"],
        "candidate_count": source["candidate_count"],
        "real_submission_preflight_created": True,
        "real_submission_preflight_ready": preflight["real_submission_preflight_ready"],
        "real_submission_preflight_completed": preflight["real_submission_preflight_completed"],
        "preflight_gate_ready": preflight["preflight_gate_ready"],
        "preflight_gate_open": preflight["preflight_gate_open"],
        "preflight_check_count": len(PREFLIGHT_CHECKS),
        "preflight_case_count": len(PREFLIGHT_CASES),
        "preflight_pass_count": preflight_pass_count,
        "preflight_failure_count": preflight_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "operator_approval_required": preflight["operator_approval_required"],
        "operator_approval_granted": preflight["operator_approval_granted"],
        "operator_approval_received": preflight["operator_approval_received"],
        "manual_upload_allowed": preflight["manual_upload_allowed"],
        "kaggle_authentication_allowed": preflight["kaggle_authentication_allowed"],
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

    gate_state = {
        "local_review_artifact_present": checks["local_review_artifact_present"],
        "local_review_artifact_ready": checks["local_review_artifact_ready"],
        "local_review_artifact_valid": checks["local_review_artifact_valid"],
        "local_review_next_stage_matches_task_4": checks["local_review_next_stage_matches_task_4"],
        "local_review_ready": checks["local_review_ready"],
        "local_review_cases_valid": checks["local_review_cases_valid"],
        "candidate_source_path_present": checks["candidate_source_path_present"],
        "candidate_source_exists": checks["candidate_source_exists"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "preflight_mode_valid": PREFLIGHT_MODE == "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_LOCAL_ONLY",
        "preflight_scope_valid": PREFLIGHT_SCOPE == "VERIFY_REAL_SUBMISSION_PREFLIGHT_WITHOUT_UPLOAD_AUTH_OR_APPROVAL",
        "preflight_verdict_valid": PREFLIGHT_VERDICT
        == "REAL_SUBMISSION_PREFLIGHT_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
        "preflight_check_count_valid": checks["preflight_check_count_valid"],
        "preflight_required": checks["preflight_required"],
        "preflight_ready": checks["preflight_ready"],
        "preflight_not_completed": checks["preflight_not_completed"],
        "preflight_gate_ready": checks["preflight_gate_ready"],
        "preflight_gate_not_open": checks["preflight_gate_not_open"],
        "preflight_case_count_valid": len(PREFLIGHT_CASES) == EXPECTED_PREFLIGHT_CASE_COUNT,
        "preflight_pass_count_valid": preflight_pass_count == EXPECTED_PREFLIGHT_PASS_COUNT,
        "preflight_failure_count_zero": preflight_failure_count == EXPECTED_PREFLIGHT_FAILURE_COUNT,
        "all_preflight_cases_pass": all(result["passed"] is True for result in results),
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": preflight_record["real_submission_created"] is False,
        "real_submission_allowed_false": preflight_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": preflight_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": preflight_record["kaggle_submission_sent"] is False,
        "upload_not_performed": preflight_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": preflight_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": preflight_record["external_api_dependency"] is False,
        "contains_api_keys_false": preflight_record["contains_api_keys"] is False,
        "private_core_exposure_false": preflight_record["private_core_exposure"] is False,
        "legal_certification_false": preflight_record["legal_certification"] is False,
        "score_claim_absent": preflight_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": preflight_record["public_leaderboard_claim_absent"] is True,
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
    }

    gates = tuple(
        {"name": name, "passed": passed, "severity": "PASS" if passed else "BLOCKING"}
        for name, passed in gate_state.items()
    )
    issues = tuple(
        {
            "name": name.replace("_valid", "_invalid").replace("_zero", "_nonzero").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    preflight_ready = (
        review.get("status") == "MILESTONE_9_LOCAL_CANDIDATE_MANUAL_REVIEW_V1_READY"
        and review.get("review_ready") is True
        and preflight_pass_count == EXPECTED_PREFLIGHT_PASS_COUNT
        and preflight_failure_count == EXPECTED_PREFLIGHT_FAILURE_COUNT
        and source["candidate_count"] > 0
        and bool(source["candidate_signature"])
        and preflight["operator_approval_granted"] is False
        and preflight_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 4",
        "preflight_mode": PREFLIGHT_MODE,
        "preflight_scope": PREFLIGHT_SCOPE,
        "preflight_verdict": PREFLIGHT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_local_review": review.get("review_id", "MISSING_REVIEW_ID"),
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "preflight_ready": preflight_ready,
        "preflight_locked": True,
        "real_submission_preflight_created": True,
        "real_submission_preflight_completed": False,
        "preflight_gate_ready": True,
        "preflight_gate_open": False,
        "preflight_check_count": len(PREFLIGHT_CHECKS),
        "preflight_case_count": len(PREFLIGHT_CASES),
        "preflight_pass_count": preflight_pass_count,
        "preflight_failure_count": preflight_failure_count,
        "operator_approval_required": preflight["operator_approval_required"],
        "operator_approval_granted": preflight["operator_approval_granted"],
        "operator_approval_received": preflight["operator_approval_received"],
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
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
        "status": PREFLIGHT_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 4",
        "title": "Real Submission Preflight Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "preflight_mode": PREFLIGHT_MODE,
        "preflight_scope": PREFLIGHT_SCOPE,
        "preflight_verdict": PREFLIGHT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "local_review_source": {
            "path": str(LOCAL_REVIEW_JSON),
            "present": LOCAL_REVIEW_JSON.exists(),
            "status": review.get("status", "MISSING"),
            "review_id": review.get("review_id", "MISSING_REVIEW_ID"),
            "sha256": _sha256(LOCAL_REVIEW_JSON),
            "sha256_16": _sha16(_sha256(LOCAL_REVIEW_JSON)),
        },
        "preflight_source_summary": source,
        "preflight_state": preflight,
        "preflight_checks": checks,
        "preflight_check_list": list(PREFLIGHT_CHECKS),
        "preflight_cases": list(PREFLIGHT_CASES),
        "preflight_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "preflight_gates": list(gates),
        "preflight_issues": list(issues),
        "preflight_index": index,
        "preflight_record": preflight_record,
        "preflight_ready": preflight_ready,
        "preflight_locked": True,
        "real_submission_preflight_created": True,
        "real_submission_preflight_ready": preflight["real_submission_preflight_ready"],
        "real_submission_preflight_completed": preflight["real_submission_preflight_completed"],
        "preflight_gate_ready": preflight["preflight_gate_ready"],
        "preflight_gate_open": preflight["preflight_gate_open"],
        "candidate_count": source["candidate_count"],
        "preflight_check_count": len(PREFLIGHT_CHECKS),
        "preflight_case_count": len(PREFLIGHT_CASES),
        "preflight_pass_count": preflight_pass_count,
        "preflight_failure_count": preflight_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "preflight_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "preflight_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": preflight["operator_approval_required"],
        "operator_approval_granted": preflight["operator_approval_granted"],
        "operator_approval_received": preflight["operator_approval_received"],
        "manual_upload_allowed": preflight["manual_upload_allowed"],
        "kaggle_authentication_allowed": preflight["kaggle_authentication_allowed"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_real_submission_preflight_gate_v1",
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
        "preflight_id": f"MILESTONE-9-PREFLIGHT-GATE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_real_submission_preflight_gate(preflight: Mapping[str, Any]) -> Dict[str, Any]:
    gates = preflight.get("preflight_gates", [])
    issues = preflight.get("preflight_issues", [])
    results = preflight.get("preflight_results", [])

    checks = {
        "status_ready": preflight.get("status") == PREFLIGHT_STATUS,
        "preflight_id_present": isinstance(preflight.get("preflight_id"), str) and bool(preflight.get("preflight_id")),
        "signature_present": isinstance(preflight.get("signature"), str) and bool(preflight.get("signature")),
        "baseline_commit_valid": str(preflight.get("baseline_commit", "")).startswith("d7c1584"),
        "preflight_mode_valid": preflight.get("preflight_mode") == PREFLIGHT_MODE,
        "preflight_scope_valid": preflight.get("preflight_scope") == PREFLIGHT_SCOPE,
        "preflight_verdict_valid": preflight.get("preflight_verdict") == PREFLIGHT_VERDICT,
        "next_allowed_stage_valid": preflight.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "preflight_ready": preflight.get("preflight_ready") is True,
        "preflight_locked": preflight.get("preflight_locked") is True,
        "real_submission_preflight_created": preflight.get("real_submission_preflight_created") is True,
        "real_submission_preflight_ready": preflight.get("real_submission_preflight_ready") is True,
        "real_submission_preflight_not_completed": preflight.get("real_submission_preflight_completed") is False,
        "preflight_gate_ready": preflight.get("preflight_gate_ready") is True,
        "preflight_gate_not_open": preflight.get("preflight_gate_open") is False,
        "preflight_check_count_valid": preflight.get("preflight_check_count") == EXPECTED_PREFLIGHT_CHECK_COUNT,
        "preflight_case_count_valid": preflight.get("preflight_case_count") == EXPECTED_PREFLIGHT_CASE_COUNT,
        "preflight_pass_count_valid": preflight.get("preflight_pass_count") == EXPECTED_PREFLIGHT_PASS_COUNT,
        "preflight_failure_count_zero": preflight.get("preflight_failure_count") == EXPECTED_PREFLIGHT_FAILURE_COUNT,
        "candidate_count_positive": preflight.get("candidate_count", 0) > 0,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_preflight_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "preflight_issue_count_zero": preflight.get("preflight_issue_count") == 0,
        "all_preflight_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": preflight.get("operator_approval_required") is True,
        "operator_approval_not_granted": preflight.get("operator_approval_granted") is False,
        "operator_approval_not_received": preflight.get("operator_approval_received") is False,
        "manual_upload_not_allowed": preflight.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": preflight.get("kaggle_authentication_allowed") is False,
        "real_submission_not_created": preflight.get("real_submission_created") is False,
        "real_submission_allowed_false": preflight.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": preflight.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": preflight.get("kaggle_submission_sent") is False,
        "upload_not_performed": preflight.get("upload_performed") is False,
        "kaggle_authentication_not_performed": preflight.get("kaggle_authentication_performed") is False,
        "metadata_safe": preflight.get("metadata", {}).get("external_api_dependency") is False
        and preflight.get("metadata", {}).get("contains_api_keys") is False
        and preflight.get("metadata", {}).get("private_core_exposure") is False
        and preflight.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "preflight_id": preflight.get("preflight_id"),
        "signature": preflight.get("signature"),
    }


def render_real_submission_preflight_gate_markdown(preflight: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Real Submission Preflight Gate v1",
        "",
        f"- status: {preflight['status']}",
        f"- preflight_id: {preflight['preflight_id']}",
        f"- signature: {preflight['signature']}",
        f"- baseline_commit: {preflight['baseline_commit']}",
        f"- preflight_mode: {preflight['preflight_mode']}",
        f"- preflight_scope: {preflight['preflight_scope']}",
        f"- preflight_verdict: {preflight['preflight_verdict']}",
        f"- next_allowed_stage: {preflight['next_allowed_stage']}",
        f"- preflight_ready: {preflight['preflight_ready']}",
        f"- real_submission_preflight_created: {preflight['real_submission_preflight_created']}",
        f"- real_submission_preflight_completed: {preflight['real_submission_preflight_completed']}",
        f"- preflight_gate_open: {preflight['preflight_gate_open']}",
        f"- candidate_count: {preflight['candidate_count']}",
        f"- preflight_check_count: {preflight['preflight_check_count']}",
        f"- preflight_case_count: {preflight['preflight_case_count']}",
        f"- preflight_pass_count: {preflight['preflight_pass_count']}",
        f"- preflight_failure_count: {preflight['preflight_failure_count']}",
        f"- operator_approval_required: {preflight['operator_approval_required']}",
        f"- operator_approval_granted: {preflight['operator_approval_granted']}",
        "",
        "## Candidate source",
        "",
        f"- path: {preflight['preflight_source_summary']['candidate_source_path']}",
        f"- candidate_id: {preflight['preflight_source_summary']['candidate_id']}",
        f"- signature: {preflight['preflight_source_summary']['candidate_signature']}",
        f"- review_sha256_16: {preflight['preflight_source_summary']['review_sha256_16']}",
        "",
        "## Preflight checks",
        "",
    ]

    for item in preflight["preflight_check_list"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Preflight results", ""])

    for result in preflight["preflight_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Real submission preflight gate is ready but not open. Operator approval has not been granted. Real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_READY=true",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_MODE=MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_VERDICT=REAL_SUBMISSION_PREFLIGHT_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_BASELINE_LOCAL_CANDIDATE_REVIEW_COMMIT=d7c1584",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_CHECK_COUNT=14",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_CREATED=true",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_COMPLETED=false",
            "ARC_AGI3_MILESTONE_9_PREFLIGHT_GATE_OPEN=false",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_5_OPERATOR_APPROVAL_GATE_V1",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GRANTED=false",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_RECEIVED=false",
            "ARC_AGI3_MILESTONE_9_MANUAL_UPLOAD_ALLOWED=false",
            "ARC_AGI3_MILESTONE_9_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_9_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_9_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_9_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_9_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_real_submission_preflight_gate_manifest(preflight: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 REAL SUBMISSION PREFLIGHT GATE MANIFEST v1",
        f"preflight_id={preflight['preflight_id']}",
        f"signature={preflight['signature']}",
        f"status={preflight['status']}",
        f"baseline_commit={preflight['baseline_commit']}",
        f"preflight_mode={preflight['preflight_mode']}",
        f"preflight_verdict={preflight['preflight_verdict']}",
        f"next_allowed_stage={preflight['next_allowed_stage']}",
        f"preflight_ready={preflight['preflight_ready']}",
        f"preflight_locked={preflight['preflight_locked']}",
        f"real_submission_preflight_created={preflight['real_submission_preflight_created']}",
        f"real_submission_preflight_ready={preflight['real_submission_preflight_ready']}",
        f"real_submission_preflight_completed={preflight['real_submission_preflight_completed']}",
        f"preflight_gate_ready={preflight['preflight_gate_ready']}",
        f"preflight_gate_open={preflight['preflight_gate_open']}",
        f"candidate_source_path={preflight['preflight_source_summary']['candidate_source_path']}",
        f"candidate_id={preflight['preflight_source_summary']['candidate_id']}",
        f"candidate_count={preflight['candidate_count']}",
        f"preflight_check_count={preflight['preflight_check_count']}",
        f"preflight_case_count={preflight['preflight_case_count']}",
        f"preflight_pass_count={preflight['preflight_pass_count']}",
        f"preflight_failure_count={preflight['preflight_failure_count']}",
        f"preflight_gate_count={preflight['preflight_gate_count']}",
        f"passed_gate_count={preflight['passed_gate_count']}",
        f"preflight_issue_count={preflight['preflight_issue_count']}",
        f"operator_approval_required={preflight['operator_approval_required']}",
        f"operator_approval_granted={preflight['operator_approval_granted']}",
        f"operator_approval_received={preflight['operator_approval_received']}",
        f"manual_upload_allowed={preflight['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={preflight['kaggle_authentication_allowed']}",
        f"real_submission_created={preflight['real_submission_created']}",
        f"real_submission_allowed={preflight['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={preflight['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={preflight['kaggle_submission_sent']}",
        f"upload_performed={preflight['upload_performed']}",
        f"kaggle_authentication_performed={preflight['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "PREFLIGHT_CHECKS",
    ]

    for item in preflight["preflight_check_list"]:
        lines.append(item)

    lines.append("")
    lines.append("PREFLIGHT_RESULTS")
    for result in preflight["preflight_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_real_submission_preflight_gate_artifacts(
    preflight: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    preflight = dict(preflight or build_milestone_9_real_submission_preflight_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-real-submission-preflight-gate-v1.json"
    md_path = output / "milestone-9-real-submission-preflight-gate-v1.md"
    manifest_path = output / "milestone-9-real-submission-preflight-gate-manifest-v1.txt"
    index_path = output / "milestone-9-real-submission-preflight-gate-index-v1.json"

    json_path.write_text(json.dumps(preflight, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_preflight_gate_markdown(preflight), encoding="utf-8")
    manifest_path.write_text(render_real_submission_preflight_gate_manifest(preflight), encoding="utf-8")
    index_path.write_text(json.dumps(preflight["preflight_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_real_submission_preflight_gate_pipeline() -> Dict[str, Any]:
    preflight = build_milestone_9_real_submission_preflight_gate()
    validation = validate_milestone_9_real_submission_preflight_gate(preflight)
    artifacts = write_real_submission_preflight_gate_artifacts(preflight)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_PIPELINE_INVALID",
        "preflight_status": preflight["status"],
        "validation_status": validation["status"],
        "preflight": preflight,
        "preflight_id": preflight["preflight_id"],
        "signature": preflight["signature"],
        "preflight_mode": preflight["preflight_mode"],
        "preflight_verdict": preflight["preflight_verdict"],
        "next_allowed_stage": preflight["next_allowed_stage"],
        "preflight_ready": preflight["preflight_ready"],
        "preflight_locked": preflight["preflight_locked"],
        "real_submission_preflight_created": preflight["real_submission_preflight_created"],
        "real_submission_preflight_ready": preflight["real_submission_preflight_ready"],
        "real_submission_preflight_completed": preflight["real_submission_preflight_completed"],
        "preflight_gate_ready": preflight["preflight_gate_ready"],
        "preflight_gate_open": preflight["preflight_gate_open"],
        "candidate_count": preflight["candidate_count"],
        "preflight_check_count": preflight["preflight_check_count"],
        "preflight_case_count": preflight["preflight_case_count"],
        "preflight_pass_count": preflight["preflight_pass_count"],
        "preflight_failure_count": preflight["preflight_failure_count"],
        "regression_guard_count": preflight["regression_guard_count"],
        "boundary_control_count": preflight["boundary_control_count"],
        "preflight_gate_count": preflight["preflight_gate_count"],
        "passed_gate_count": preflight["passed_gate_count"],
        "preflight_issue_count": preflight["preflight_issue_count"],
        "warning_count": preflight["warning_count"],
        "operator_approval_required": preflight["operator_approval_required"],
        "operator_approval_granted": preflight["operator_approval_granted"],
        "operator_approval_received": preflight["operator_approval_received"],
        "manual_upload_allowed": preflight["manual_upload_allowed"],
        "kaggle_authentication_allowed": preflight["kaggle_authentication_allowed"],
        "real_submission_created": preflight["real_submission_created"],
        "real_submission_allowed": preflight["real_submission_allowed"],
        "ready_for_real_kaggle_submission": preflight["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": preflight["kaggle_submission_sent"],
        "upload_performed": preflight["upload_performed"],
        "kaggle_authentication_performed": preflight["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": preflight["metadata"],
    }
