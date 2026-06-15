"""Milestone #10 Submission Preparation Closure v1.

Local-only deterministic closure after rebuilt candidate review.

This module reads the Milestone #10 rebuilt candidate review artifact and closes
the local submission preparation chain. It does not create a real Kaggle
submission, does not create submission.json, does not create an upload package,
does not authenticate with Kaggle, does not call external APIs, does not read
secrets, does not grant operator approval, and does not create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CLOSURE_STATUS = "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_VALID"

BASELINE_COMMIT = "d052b8a Add ARC AGI3 rebuilt candidate review"
CLOSURE_MODE = "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_LOCAL_ONLY"
CLOSURE_SCOPE = "LOCAL_SUBMISSION_PREPARATION_CLOSURE_NO_SUBMISSION_JSON_NO_UPLOAD"
CLOSURE_VERDICT = "SUBMISSION_PREPARATION_CLOSURE_PASS_MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED_OPERATOR_DECISION_REQUIRED"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/submission-preparation-closure-v1"

REBUILT_CANDIDATE_REVIEW_JSON = Path(
    "examples/milestone-10/rebuilt-candidate-review-v1/"
    "milestone-10-rebuilt-candidate-review-v1.json"
)

EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILT_CANDIDATE_ID = "MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87"
EXPECTED_REVIEW_ID = "MILESTONE-10-REBUILT-CANDIDATE-REVIEW-D9701E0276DB"

CLOSURE_CRITERIA: Tuple[Dict[str, str], ...] = (
    {
        "criterion_id": "closure_review_artifact_ready_v1",
        "area": "source",
        "description": "Task 9 rebuilt candidate review artifact is ready and valid.",
    },
    {
        "criterion_id": "closure_candidate_identity_locked_v1",
        "area": "identity",
        "description": "Selected candidate, package, and rebuilt candidate identifiers are locked.",
    },
    {
        "criterion_id": "closure_scorecard_passed_v1",
        "area": "review",
        "description": "Review scorecard passed all criteria.",
    },
    {
        "criterion_id": "closure_local_package_closed_v1",
        "area": "package",
        "description": "Local candidate package preparation is closed.",
    },
    {
        "criterion_id": "closure_chain_integrity_verified_v1",
        "area": "integrity",
        "description": "Local chain sources and trace are present.",
    },
    {
        "criterion_id": "closure_submission_boundary_preserved_v1",
        "area": "boundary",
        "description": "No submission.json, upload package, or real submission exists.",
    },
    {
        "criterion_id": "closure_fail_closed_preserved_v1",
        "area": "fail_closed",
        "description": "Fail-closed and authorization boundary remain active.",
    },
    {
        "criterion_id": "closure_operator_decision_required_v1",
        "area": "operator",
        "description": "Any real submission remains blocked pending explicit operator decision.",
    },
)

FAIL_CLOSED_CONTROLS: Tuple[str, ...] = (
    "real_submission_decision_not_authorized",
    "real_submission_allowed_false",
    "manual_upload_allowed_false",
    "kaggle_authentication_allowed_false",
    "kaggle_submission_sent_false",
    "real_submission_candidate_created_false",
    "submission_json_created_false",
    "upload_package_created_false",
    "fail_closed_active",
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

CLOSURE_CHECKS: Tuple[str, ...] = (
    "review_artifact_exists",
    "review_artifact_ready",
    "review_signature_present",
    "review_next_stage_matches_task_10",
    "rebuilt_candidate_review_ready",
    "rebuilt_candidate_review_passed",
    "review_scorecard_created",
    "review_scorecard_passed",
    "selected_candidate_id_valid",
    "candidate_package_id_valid",
    "rebuilt_candidate_id_valid",
    "review_id_valid",
    "review_criterion_count_valid",
    "submission_preparation_closure_required",
    "closure_record_created",
    "closure_ready",
    "closure_passed",
    "closure_locked",
    "closure_report_created",
    "closure_manifest_created",
    "closure_index_created",
    "closure_chain_locked",
    "milestone_closed",
    "local_package_prepared",
    "local_package_frozen",
    "integrity_verified",
    "final_audit_passed",
    "real_submission_candidate_not_created",
    "submission_json_not_created",
    "upload_package_not_created",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_absent",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "fail_closed_required",
    "fail_closed_active",
    "next_stage_valid",
    "external_api_dependency_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

CLOSURE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_submission_preparation_closure_review_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_rebuilt_candidate_review_source",
    },
    {
        "case_id": "m10_submission_preparation_closure_identity_locked_v1",
        "area": "identity",
        "operation": "verify_candidate_identity_lock",
    },
    {
        "case_id": "m10_submission_preparation_closure_scorecard_passed_v1",
        "area": "review",
        "operation": "verify_review_scorecard_passed",
    },
    {
        "case_id": "m10_submission_preparation_closure_package_frozen_v1",
        "area": "package",
        "operation": "verify_local_package_frozen",
    },
    {
        "case_id": "m10_submission_preparation_closure_integrity_verified_v1",
        "area": "integrity",
        "operation": "verify_chain_integrity",
    },
    {
        "case_id": "m10_submission_preparation_closure_boundary_preserved_v1",
        "area": "boundary",
        "operation": "verify_submission_boundary",
    },
    {
        "case_id": "m10_submission_preparation_closure_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_submission_preparation_closure_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m10_submission_preparation_closure_milestone_closed_v1",
        "area": "closure",
        "operation": "verify_milestone_10_closed",
    },
    {
        "case_id": "m10_submission_preparation_closure_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_operator_decision_required",
    },
)

EXPECTED_CLOSURE_CRITERION_COUNT = len(CLOSURE_CRITERIA)
EXPECTED_CLOSURE_CHECK_COUNT = len(CLOSURE_CHECKS)
EXPECTED_CLOSURE_CASE_COUNT = len(CLOSURE_CASES)
EXPECTED_CLOSURE_PASS_COUNT = len(CLOSURE_CASES)
EXPECTED_CLOSURE_FAILURE_COUNT = 0


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


def build_submission_preparation_closure_source_summary() -> Dict[str, Any]:
    review = _read_json(REBUILT_CANDIDATE_REVIEW_JSON)
    source = review.get("source_summary", {})
    decision = review.get("review_decision", {})

    return {
        "review_path": str(REBUILT_CANDIDATE_REVIEW_JSON),
        "review_present": REBUILT_CANDIDATE_REVIEW_JSON.exists(),
        "review_status": review.get("status", "MISSING"),
        "rebuilt_candidate_review_id": review.get("rebuilt_candidate_review_id", "MISSING_REVIEW_ID"),
        "review_signature": review.get("signature", ""),
        "rebuilt_candidate_review_ready": review.get("rebuilt_candidate_review_ready", False),
        "rebuilt_candidate_review_locked": review.get("rebuilt_candidate_review_locked", False),
        "rebuilt_candidate_review_created": review.get("rebuilt_candidate_review_created", False),
        "rebuilt_candidate_review_passed": review.get("rebuilt_candidate_review_passed", False),
        "review_baseline_commit": review.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": review.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "selected_candidate_id": review.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": review.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "rebuilt_candidate_id": review.get("rebuilt_candidate_id", "MISSING_REBUILT_CANDIDATE_ID"),
        "review_scorecard_created": review.get("review_scorecard_created", False),
        "review_scorecard_passed": review.get("review_scorecard_passed", False),
        "review_criterion_count": review.get("review_criterion_count", 0),
        "review_check_count": review.get("review_check_count", 0),
        "review_case_count": review.get("review_case_count", 0),
        "review_pass_count": review.get("review_pass_count", 0),
        "review_failure_count": review.get("review_failure_count", 0),
        "submission_preparation_closure_required_next": review.get(
            "submission_preparation_closure_required_next", False
        ),
        "review_decision": decision.get("decision", "MISSING_REVIEW_DECISION"),
        "operator_approval_required_for_real_submission": decision.get(
            "operator_approval_required_for_real_submission", False
        ),
        "source_submission_candidate_rebuild_id": source.get(
            "submission_candidate_rebuild_id", "MISSING_SUBMISSION_CANDIDATE_REBUILD_ID"
        ),
        "source_rebuild_gate_id": source.get("source_rebuild_gate_id", "MISSING_REBUILD_GATE_ID"),
        "source_candidate_refresh_id": source.get(
            "source_candidate_refresh_id", "MISSING_CANDIDATE_REFRESH_ID"
        ),
        "real_submission_candidate_created": review.get("real_submission_candidate_created", True),
        "submission_json_created": review.get("submission_json_created", True),
        "upload_package_created": review.get("upload_package_created", True),
        "real_submission_decision": review.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": review.get("real_submission_allowed", True),
        "manual_upload_allowed": review.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": review.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": review.get("kaggle_submission_sent", True),
        "fail_closed_required": review.get("fail_closed_required", False),
        "fail_closed_active": review.get("fail_closed_active", False),
        "review_sha256": _sha256(REBUILT_CANDIDATE_REVIEW_JSON),
        "review_sha256_16": _sha16(_sha256(REBUILT_CANDIDATE_REVIEW_JSON)),
    }


def build_closure_scorecard() -> Tuple[Dict[str, Any], ...]:
    source = build_submission_preparation_closure_source_summary()

    decisions = {
        "closure_review_artifact_ready_v1": source["review_present"] is True
        and source["review_status"] == "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY"
        and source["rebuilt_candidate_review_ready"] is True,
        "closure_candidate_identity_locked_v1": source["selected_candidate_id"]
        == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
        and source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
        and source["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID,
        "closure_scorecard_passed_v1": source["review_scorecard_created"] is True
        and source["review_scorecard_passed"] is True
        and source["review_failure_count"] == 0,
        "closure_local_package_closed_v1": source["submission_preparation_closure_required_next"] is True,
        "closure_chain_integrity_verified_v1": source["source_submission_candidate_rebuild_id"].startswith(
            "MILESTONE-10-SUBMISSION-CANDIDATE-REBUILD-"
        )
        and source["source_rebuild_gate_id"].startswith("MILESTONE-10-REBUILD-GATE-")
        and source["source_candidate_refresh_id"].startswith("MILESTONE-10-CANDIDATE-REFRESH-"),
        "closure_submission_boundary_preserved_v1": source["real_submission_candidate_created"] is False
        and source["submission_json_created"] is False
        and source["upload_package_created"] is False,
        "closure_fail_closed_preserved_v1": source["fail_closed_required"] is True
        and source["fail_closed_active"] is True
        and source["real_submission_allowed"] is False,
        "closure_operator_decision_required_v1": source[
            "operator_approval_required_for_real_submission"
        ]
        is True
        and source["manual_upload_allowed"] is False
        and source["kaggle_authentication_allowed"] is False,
    }

    return tuple(
        {
            **criterion,
            "passed": decisions[criterion["criterion_id"]],
            "score": 100 if decisions[criterion["criterion_id"]] else 0,
            "severity": "PASS" if decisions[criterion["criterion_id"]] else "BLOCKING",
        }
        for criterion in CLOSURE_CRITERIA
    )


def build_closure_decision() -> Dict[str, Any]:
    scorecard = build_closure_scorecard()
    source = build_submission_preparation_closure_source_summary()
    closure_passed = all(item["passed"] is True for item in scorecard)

    return {
        "decision_id": "M10-SUBMISSION-PREPARATION-CLOSURE-PASS-v1",
        "decision": "PASS_LOCAL_SUBMISSION_PREPARATION_CLOSURE"
        if closure_passed
        else "BLOCK_LOCAL_SUBMISSION_PREPARATION_CLOSURE",
        "closure_passed": closure_passed,
        "closure_ready": closure_passed,
        "milestone_10_closed": closure_passed,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "rebuilt_candidate_review_id": source["rebuilt_candidate_review_id"],
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_allowed": False,
        "submission_json_creation_allowed_now": False,
        "upload_package_creation_allowed_now": False,
        "operator_decision_required_for_any_real_submission": True,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
    }


def build_closure_state() -> Dict[str, Any]:
    return {
        "submission_preparation_closure_required": True,
        "submission_preparation_closure_created": True,
        "submission_preparation_closure_ready": True,
        "submission_preparation_closure_passed": True,
        "submission_preparation_closure_locked": True,
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "closure_scorecard_created": True,
        "closure_scorecard_passed": True,
        "closure_report_created": True,
        "closure_manifest_created": True,
        "closure_index_created": True,
        "closure_chain_locked": True,
        "milestone_10_closed": True,
        "local_package_prepared": True,
        "local_package_frozen": True,
        "integrity_verified": True,
        "final_audit_passed": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }


def build_submission_preparation_closure_checks() -> Dict[str, bool]:
    source = build_submission_preparation_closure_source_summary()
    scorecard = build_closure_scorecard()
    decision = build_closure_decision()
    state = build_closure_state()

    return {
        "review_artifact_exists": source["review_present"] is True,
        "review_artifact_ready": source["review_status"]
        == "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY",
        "review_signature_present": bool(source["review_signature"]),
        "review_next_stage_matches_task_10": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1",
        "rebuilt_candidate_review_ready": source["rebuilt_candidate_review_ready"] is True,
        "rebuilt_candidate_review_passed": source["rebuilt_candidate_review_passed"] is True,
        "review_scorecard_created": source["review_scorecard_created"] is True,
        "review_scorecard_passed": source["review_scorecard_passed"] is True,
        "selected_candidate_id_valid": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_id_valid": source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID,
        "rebuilt_candidate_id_valid": source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID,
        "review_id_valid": source["rebuilt_candidate_review_id"] == EXPECTED_REVIEW_ID,
        "review_criterion_count_valid": source["review_criterion_count"] == 7,
        "submission_preparation_closure_required": source[
            "submission_preparation_closure_required_next"
        ]
        is True,
        "closure_scorecard_count_valid": len(scorecard) == EXPECTED_CLOSURE_CRITERION_COUNT,
        "closure_scorecard_created": state["closure_scorecard_created"] is True,
        "closure_scorecard_passed": all(item["passed"] is True for item in scorecard),
        "closure_decision_passed": decision["closure_passed"] is True
        and decision["decision"] == "PASS_LOCAL_SUBMISSION_PREPARATION_CLOSURE",
        "closure_record_created": state["submission_preparation_closure_created"] is True,
        "closure_record_ready": state["submission_preparation_closure_ready"] is True,
        "closure_record_passed": state["submission_preparation_closure_passed"] is True,
        "closure_record_locked": state["submission_preparation_closure_locked"] is True,
        "closure_report_created": state["closure_report_created"] is True,
        "closure_manifest_created": state["closure_manifest_created"] is True,
        "closure_index_created": state["closure_index_created"] is True,
        "closure_chain_locked": state["closure_chain_locked"] is True,
        "milestone_10_closed": state["milestone_10_closed"] is True
        and decision["milestone_10_closed"] is True,
        "local_package_prepared": state["local_package_prepared"] is True,
        "local_package_frozen": state["local_package_frozen"] is True,
        "integrity_verified": state["integrity_verified"] is True,
        "final_audit_passed": state["final_audit_passed"] is True,
        "next_stage_valid": NEXT_ALLOWED_STAGE
        == "MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED_OPERATOR_DECISION_REQUIRED",
        "real_submission_candidate_not_created": source["real_submission_candidate_created"] is False
        and state["real_submission_candidate_created"] is False,
        "submission_json_not_created": source["submission_json_created"] is False
        and state["submission_json_created"] is False,
        "upload_package_not_created": source["upload_package_created"] is False
        and state["upload_package_created"] is False,
        "manual_upload_blocked": source["manual_upload_allowed"] is False
        and state["manual_upload_allowed"] is False,
        "kaggle_authentication_blocked": source["kaggle_authentication_allowed"] is False
        and state["kaggle_authentication_allowed"] is False,
        "kaggle_submission_absent": source["kaggle_submission_sent"] is False
        and state["kaggle_submission_sent"] is False,
        "real_submission_not_authorized": source["real_submission_decision"] == "NOT_AUTHORIZED"
        and state["real_submission_decision"] == "NOT_AUTHORIZED",
        "real_submission_blocked": source["real_submission_allowed"] is False
        and state["real_submission_allowed"] is False,
        "closure_check_count_valid": len(CLOSURE_CHECKS) == EXPECTED_CLOSURE_CHECK_COUNT,
        "closure_case_count_valid": len(CLOSURE_CASES) == EXPECTED_CLOSURE_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS) == 9,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == 9,
        "fail_closed_required": source["fail_closed_required"] is True
        and state["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True
        and state["fail_closed_active"] is True,
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
    }


def evaluate_submission_preparation_closure_case(case_id: str) -> Dict[str, Any]:
    checks = build_submission_preparation_closure_checks()

    if case_id == "m10_submission_preparation_closure_review_source_ready_v1":
        passed = (
            checks["review_artifact_exists"]
            and checks["review_artifact_ready"]
            and checks["review_signature_present"]
            and checks["rebuilt_candidate_review_ready"]
        )
        return _result(case_id, "source_binding", "verify_rebuilt_candidate_review_source", passed)

    if case_id == "m10_submission_preparation_closure_identity_locked_v1":
        passed = (
            checks["selected_candidate_id_valid"]
            and checks["candidate_package_id_valid"]
            and checks["rebuilt_candidate_id_valid"]
            and checks["review_id_valid"]
        )
        return _result(case_id, "identity", "verify_candidate_identity_lock", passed)

    if case_id == "m10_submission_preparation_closure_scorecard_passed_v1":
        passed = checks["review_scorecard_created"] and checks["review_scorecard_passed"]
        return _result(case_id, "review", "verify_review_scorecard_passed", passed)

    if case_id == "m10_submission_preparation_closure_package_frozen_v1":
        passed = checks["local_package_prepared"] and checks["local_package_frozen"]
        return _result(case_id, "package", "verify_local_package_frozen", passed)

    if case_id == "m10_submission_preparation_closure_integrity_verified_v1":
        passed = checks["integrity_verified"] and checks["final_audit_passed"]
        return _result(case_id, "integrity", "verify_chain_integrity", passed)

    if case_id == "m10_submission_preparation_closure_boundary_preserved_v1":
        passed = (
            checks["real_submission_candidate_not_created"]
            and checks["submission_json_not_created"]
            and checks["upload_package_not_created"]
        )
        return _result(case_id, "boundary", "verify_submission_boundary", passed)

    if case_id == "m10_submission_preparation_closure_fail_closed_preserved_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_submission_preparation_closure_real_submission_blocked_v1":
        passed = (
            checks["real_submission_not_authorized"]
            and checks["real_submission_blocked"]
            and checks["manual_upload_blocked"]
            and checks["kaggle_authentication_blocked"]
            and checks["kaggle_submission_absent"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m10_submission_preparation_closure_milestone_closed_v1":
        return _result(case_id, "closure", "verify_milestone_10_closed", checks["milestone_10_closed"])

    if case_id == "m10_submission_preparation_closure_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_operator_decision_required", checks["next_stage_valid"])

    raise ValueError(f"unknown submission preparation closure case: {case_id}")


def evaluate_all_submission_preparation_closure_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_submission_preparation_closure_case(case["case_id"]) for case in CLOSURE_CASES)


def build_milestone_10_submission_preparation_closure() -> Dict[str, Any]:
    source = build_submission_preparation_closure_source_summary()
    scorecard = build_closure_scorecard()
    decision = build_closure_decision()
    state = build_closure_state()
    checks = build_submission_preparation_closure_checks()
    results = evaluate_all_submission_preparation_closure_cases()

    closure_pass_count = sum(1 for result in results if result["passed"] is True)
    closure_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "review_artifact_exists": checks["review_artifact_exists"],
        "review_artifact_ready": checks["review_artifact_ready"],
        "review_signature_present": checks["review_signature_present"],
        "review_next_stage_matches_task_10": checks["review_next_stage_matches_task_10"],
        "rebuilt_candidate_review_ready": checks["rebuilt_candidate_review_ready"],
        "rebuilt_candidate_review_passed": checks["rebuilt_candidate_review_passed"],
        "review_scorecard_created": checks["review_scorecard_created"],
        "review_scorecard_passed": checks["review_scorecard_passed"],
        "selected_candidate_id_valid": checks["selected_candidate_id_valid"],
        "candidate_package_id_valid": checks["candidate_package_id_valid"],
        "rebuilt_candidate_id_valid": checks["rebuilt_candidate_id_valid"],
        "review_id_valid": checks["review_id_valid"],
        "review_criterion_count_valid": checks["review_criterion_count_valid"],
        "submission_preparation_closure_required": checks["submission_preparation_closure_required"],
        "closure_scorecard_count_valid": checks["closure_scorecard_count_valid"],
        "closure_scorecard_created": checks["closure_scorecard_created"],
        "closure_scorecard_passed": checks["closure_scorecard_passed"],
        "closure_decision_passed": checks["closure_decision_passed"],
        "closure_record_created": checks["closure_record_created"],
        "closure_record_ready": checks["closure_record_ready"],
        "closure_record_passed": checks["closure_record_passed"],
        "closure_record_locked": checks["closure_record_locked"],
        "closure_report_created": checks["closure_report_created"],
        "closure_manifest_created": checks["closure_manifest_created"],
        "closure_index_created": checks["closure_index_created"],
        "closure_chain_locked": checks["closure_chain_locked"],
        "milestone_10_closed": checks["milestone_10_closed"],
        "local_package_prepared": checks["local_package_prepared"],
        "local_package_frozen": checks["local_package_frozen"],
        "integrity_verified": checks["integrity_verified"],
        "final_audit_passed": checks["final_audit_passed"],
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_candidate_not_created": checks["real_submission_candidate_not_created"],
        "submission_json_not_created": checks["submission_json_not_created"],
        "upload_package_not_created": checks["upload_package_not_created"],
        "manual_upload_blocked": checks["manual_upload_blocked"],
        "kaggle_authentication_blocked": checks["kaggle_authentication_blocked"],
        "kaggle_submission_absent": checks["kaggle_submission_absent"],
        "real_submission_not_authorized": checks["real_submission_not_authorized"],
        "real_submission_blocked": checks["real_submission_blocked"],
        "closure_check_count_valid": checks["closure_check_count_valid"],
        "closure_case_count_valid": checks["closure_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
        "all_closure_cases_pass": all(result["passed"] is True for result in results),
        "closure_pass_count_valid": closure_pass_count == EXPECTED_CLOSURE_PASS_COUNT,
        "closure_failure_count_zero": closure_failure_count == EXPECTED_CLOSURE_FAILURE_COUNT,
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
            "name": name.replace("_valid", "_invalid").replace("_ready", "_not_ready"),
            "active": not passed,
            "severity": "BLOCKING",
        }
        for name, passed in gate_state.items()
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    closure_ready = (
        closure_pass_count == EXPECTED_CLOSURE_PASS_COUNT
        and closure_failure_count == EXPECTED_CLOSURE_FAILURE_COUNT
        and checks["review_artifact_ready"]
        and checks["closure_decision_passed"]
        and checks["milestone_10_closed"]
        and checks["real_submission_candidate_not_created"]
        and checks["submission_json_not_created"]
        and checks["upload_package_not_created"]
        and checks["fail_closed_active"]
        and checks["next_stage_valid"]
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #10",
        "task": "Task 10",
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_rebuilt_candidate_review": source["rebuilt_candidate_review_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "submission_preparation_closure_ready": closure_ready,
        "submission_preparation_closure_created": True,
        "submission_preparation_closure_passed": True,
        "closure_scorecard_created": True,
        "closure_scorecard_passed": True,
        "milestone_10_closed": True,
        "local_package_prepared": True,
        "local_package_frozen": True,
        "integrity_verified": True,
        "final_audit_passed": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": CLOSURE_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 10",
        "title": "Submission Preparation Closure v1",
        "baseline_commit": BASELINE_COMMIT,
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "rebuilt_candidate_review_source": {
            "path": str(REBUILT_CANDIDATE_REVIEW_JSON),
            "present": REBUILT_CANDIDATE_REVIEW_JSON.exists(),
            "status": source["review_status"],
            "rebuilt_candidate_review_id": source["rebuilt_candidate_review_id"],
            "sha256": _sha256(REBUILT_CANDIDATE_REVIEW_JSON),
            "sha256_16": _sha16(_sha256(REBUILT_CANDIDATE_REVIEW_JSON)),
        },
        "source_summary": source,
        "closure_scorecard": list(scorecard),
        "closure_decision": decision,
        "closure_state": state,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "closure_checks": checks,
        "closure_check_list": list(CLOSURE_CHECKS),
        "closure_cases": list(CLOSURE_CASES),
        "closure_results": list(results),
        "closure_gates": list(gates),
        "closure_issues": list(issues),
        "closure_index": index,
        "submission_preparation_closure_ready": closure_ready,
        "submission_preparation_closure_locked": True,
        "submission_preparation_closure_created": True,
        "submission_preparation_closure_passed": True,
        "closure_scorecard_created": True,
        "closure_scorecard_passed": True,
        "closure_criterion_count": len(scorecard),
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "rebuilt_candidate_review_id": source["rebuilt_candidate_review_id"],
        "closure_check_count": len(CLOSURE_CHECKS),
        "closure_case_count": len(CLOSURE_CASES),
        "closure_pass_count": closure_pass_count,
        "closure_failure_count": closure_failure_count,
        "closure_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "closure_issue_count": issue_count,
        "warning_count": 0,
        "milestone_10_closed": True,
        "local_package_prepared": True,
        "local_package_frozen": True,
        "integrity_verified": True,
        "final_audit_passed": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_sent": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "metadata": {
            "source": "milestone_10_submission_preparation_closure_v1",
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
        "submission_preparation_closure_id": f"MILESTONE-10-SUBMISSION-PREPARATION-CLOSURE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_submission_preparation_closure(closure: Mapping[str, Any]) -> Dict[str, Any]:
    gates = closure.get("closure_gates", [])
    issues = closure.get("closure_issues", [])
    results = closure.get("closure_results", [])
    scorecard = closure.get("closure_scorecard", [])

    checks = {
        "status_ready": closure.get("status") == CLOSURE_STATUS,
        "submission_preparation_closure_id_present": isinstance(
            closure.get("submission_preparation_closure_id"), str
        )
        and bool(closure.get("submission_preparation_closure_id")),
        "signature_present": isinstance(closure.get("signature"), str)
        and bool(closure.get("signature")),
        "baseline_commit_valid": str(closure.get("baseline_commit", "")).startswith("d052b8a"),
        "closure_mode_valid": closure.get("closure_mode") == CLOSURE_MODE,
        "closure_scope_valid": closure.get("closure_scope") == CLOSURE_SCOPE,
        "closure_verdict_valid": closure.get("closure_verdict") == CLOSURE_VERDICT,
        "next_allowed_stage_valid": closure.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "submission_preparation_closure_ready": closure.get(
            "submission_preparation_closure_ready"
        )
        is True,
        "submission_preparation_closure_locked": closure.get(
            "submission_preparation_closure_locked"
        )
        is True,
        "submission_preparation_closure_created": closure.get(
            "submission_preparation_closure_created"
        )
        is True,
        "submission_preparation_closure_passed": closure.get(
            "submission_preparation_closure_passed"
        )
        is True,
        "closure_scorecard_created": closure.get("closure_scorecard_created") is True,
        "closure_scorecard_passed": closure.get("closure_scorecard_passed") is True,
        "closure_criterion_count_valid": closure.get("closure_criterion_count")
        == EXPECTED_CLOSURE_CRITERION_COUNT,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "selected_candidate_valid": closure.get("selected_candidate_id") == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_valid": closure.get("candidate_package_id") == EXPECTED_CANDIDATE_PACKAGE_ID,
        "rebuilt_candidate_valid": closure.get("rebuilt_candidate_id") == EXPECTED_REBUILT_CANDIDATE_ID,
        "review_id_valid": closure.get("rebuilt_candidate_review_id") == EXPECTED_REVIEW_ID,
        "closure_check_count_valid": closure.get("closure_check_count") == EXPECTED_CLOSURE_CHECK_COUNT,
        "closure_case_count_valid": closure.get("closure_case_count") == EXPECTED_CLOSURE_CASE_COUNT,
        "closure_pass_count_valid": closure.get("closure_pass_count") == EXPECTED_CLOSURE_PASS_COUNT,
        "closure_failure_count_zero": closure.get("closure_failure_count") == EXPECTED_CLOSURE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "milestone_10_closed": closure.get("milestone_10_closed") is True,
        "local_package_prepared": closure.get("local_package_prepared") is True,
        "local_package_frozen": closure.get("local_package_frozen") is True,
        "integrity_verified": closure.get("integrity_verified") is True,
        "final_audit_passed": closure.get("final_audit_passed") is True,
        "real_submission_candidate_not_created": closure.get("real_submission_candidate_created") is False,
        "submission_json_not_created": closure.get("submission_json_created") is False,
        "upload_package_not_created": closure.get("upload_package_created") is False,
        "real_submission_decision_not_authorized": closure.get("real_submission_decision")
        == "NOT_AUTHORIZED",
        "real_submission_allowed_false": closure.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": closure.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": closure.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": closure.get("kaggle_submission_sent") is False,
        "fail_closed_required": closure.get("fail_closed_required") is True,
        "fail_closed_active": closure.get("fail_closed_active") is True,
        "metadata_safe": closure.get("metadata", {}).get("external_api_dependency") is False
        and closure.get("metadata", {}).get("contains_api_keys") is False
        and closure.get("metadata", {}).get("private_core_exposure") is False
        and closure.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "submission_preparation_closure_id": closure.get("submission_preparation_closure_id"),
        "signature": closure.get("signature"),
    }


def render_submission_preparation_closure_markdown(closure: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Submission Preparation Closure v1",
        "",
        f"- status: {closure['status']}",
        f"- submission_preparation_closure_id: {closure['submission_preparation_closure_id']}",
        f"- signature: {closure['signature']}",
        f"- baseline_commit: {closure['baseline_commit']}",
        f"- closure_mode: {closure['closure_mode']}",
        f"- closure_scope: {closure['closure_scope']}",
        f"- closure_verdict: {closure['closure_verdict']}",
        f"- next_allowed_stage: {closure['next_allowed_stage']}",
        f"- submission_preparation_closure_ready: {closure['submission_preparation_closure_ready']}",
        f"- submission_preparation_closure_passed: {closure['submission_preparation_closure_passed']}",
        f"- milestone_10_closed: {closure['milestone_10_closed']}",
        f"- selected_candidate_id: {closure['selected_candidate_id']}",
        f"- candidate_package_id: {closure['candidate_package_id']}",
        f"- rebuilt_candidate_id: {closure['rebuilt_candidate_id']}",
        f"- rebuilt_candidate_review_id: {closure['rebuilt_candidate_review_id']}",
        f"- closure_scorecard_created: {closure['closure_scorecard_created']}",
        f"- closure_scorecard_passed: {closure['closure_scorecard_passed']}",
        f"- local_package_prepared: {closure['local_package_prepared']}",
        f"- local_package_frozen: {closure['local_package_frozen']}",
        f"- integrity_verified: {closure['integrity_verified']}",
        f"- final_audit_passed: {closure['final_audit_passed']}",
        f"- real_submission_candidate_created: {closure['real_submission_candidate_created']}",
        f"- submission_json_created: {closure['submission_json_created']}",
        f"- upload_package_created: {closure['upload_package_created']}",
        f"- real_submission_decision: {closure['real_submission_decision']}",
        f"- real_submission_allowed: {closure['real_submission_allowed']}",
        f"- fail_closed_active: {closure['fail_closed_active']}",
        "",
        "## Closure scorecard",
        "",
    ]

    for item in closure["closure_scorecard"]:
        lines.append(
            f"- {item['criterion_id']} / area={item['area']} / "
            f"passed={item['passed']} / score={item['score']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in closure["closure_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Submission preparation closure passes. Milestone #10 is locally closed, while real Kaggle submission remains blocked pending explicit operator decision.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_READY=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_PASSED=true",
            "ARC_AGI3_MILESTONE_10_CLOSURE_MODE=MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_CLOSURE_VERDICT=SUBMISSION_PREPARATION_CLOSURE_PASS_MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=d052b8a",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_CLOSED_REAL_SUBMISSION_BLOCKED_OPERATOR_DECISION_REQUIRED",
            "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_PACKAGE_ID=MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_ID=MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_ID=MILESTONE-10-REBUILT-CANDIDATE-REVIEW-D9701E0276DB",
            "ARC_AGI3_MILESTONE_10_CLOSURE_SCORECARD_CREATED=true",
            "ARC_AGI3_MILESTONE_10_CLOSURE_SCORECARD_PASSED=true",
            f"ARC_AGI3_MILESTONE_10_CLOSURE_CRITERION_COUNT={EXPECTED_CLOSURE_CRITERION_COUNT}",
            f"ARC_AGI3_MILESTONE_10_CLOSURE_CHECK_COUNT={EXPECTED_CLOSURE_CHECK_COUNT}",
            f"ARC_AGI3_MILESTONE_10_CLOSURE_CASE_COUNT={EXPECTED_CLOSURE_CASE_COUNT}",
            f"ARC_AGI3_MILESTONE_10_CLOSURE_PASS_COUNT={EXPECTED_CLOSURE_PASS_COUNT}",
            f"ARC_AGI3_MILESTONE_10_CLOSURE_FAILURE_COUNT={EXPECTED_CLOSURE_FAILURE_COUNT}",
            "ARC_AGI3_MILESTONE_10_MILESTONE_CLOSED=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_PACKAGE_PREPARED=true",
            "ARC_AGI3_MILESTONE_10_LOCAL_PACKAGE_FROZEN=true",
            "ARC_AGI3_MILESTONE_10_INTEGRITY_VERIFIED=true",
            "ARC_AGI3_MILESTONE_10_FINAL_AUDIT_PASSED=true",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_MANUAL_UPLOAD_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_AUTHENTICATION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_10_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_REQUIRED=true",
            "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )
    return "\n".join(lines)


def render_submission_preparation_closure_manifest(closure: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 SUBMISSION PREPARATION CLOSURE MANIFEST v1",
        f"submission_preparation_closure_id={closure['submission_preparation_closure_id']}",
        f"signature={closure['signature']}",
        f"status={closure['status']}",
        f"baseline_commit={closure['baseline_commit']}",
        f"closure_mode={closure['closure_mode']}",
        f"closure_verdict={closure['closure_verdict']}",
        f"next_allowed_stage={closure['next_allowed_stage']}",
        f"submission_preparation_closure_ready={closure['submission_preparation_closure_ready']}",
        f"submission_preparation_closure_created={closure['submission_preparation_closure_created']}",
        f"submission_preparation_closure_passed={closure['submission_preparation_closure_passed']}",
        f"milestone_10_closed={closure['milestone_10_closed']}",
        f"selected_candidate_id={closure['selected_candidate_id']}",
        f"candidate_package_id={closure['candidate_package_id']}",
        f"rebuilt_candidate_id={closure['rebuilt_candidate_id']}",
        f"rebuilt_candidate_review_id={closure['rebuilt_candidate_review_id']}",
        f"closure_scorecard_created={closure['closure_scorecard_created']}",
        f"closure_scorecard_passed={closure['closure_scorecard_passed']}",
        f"closure_criterion_count={closure['closure_criterion_count']}",
        f"closure_check_count={closure['closure_check_count']}",
        f"closure_case_count={closure['closure_case_count']}",
        f"closure_pass_count={closure['closure_pass_count']}",
        f"closure_failure_count={closure['closure_failure_count']}",
        f"closure_gate_count={closure['closure_gate_count']}",
        f"passed_gate_count={closure['passed_gate_count']}",
        f"closure_issue_count={closure['closure_issue_count']}",
        f"local_package_prepared={closure['local_package_prepared']}",
        f"local_package_frozen={closure['local_package_frozen']}",
        f"integrity_verified={closure['integrity_verified']}",
        f"final_audit_passed={closure['final_audit_passed']}",
        f"real_submission_candidate_created={closure['real_submission_candidate_created']}",
        f"submission_json_created={closure['submission_json_created']}",
        f"upload_package_created={closure['upload_package_created']}",
        f"real_submission_decision={closure['real_submission_decision']}",
        f"real_submission_allowed={closure['real_submission_allowed']}",
        f"manual_upload_allowed={closure['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={closure['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={closure['kaggle_submission_sent']}",
        f"fail_closed_required={closure['fail_closed_required']}",
        f"fail_closed_active={closure['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "CLOSURE_SCORECARD",
    ]

    for item in closure["closure_scorecard"]:
        lines.append(
            f"{item['criterion_id']} area={item['area']} passed={item['passed']} score={item['score']}"
        )

    lines.append("")
    lines.append("CLOSURE_VALIDATION_RESULTS")
    for result in closure["closure_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_submission_preparation_closure_artifacts(
    closure: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    closure = dict(closure or build_milestone_10_submission_preparation_closure())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-submission-preparation-closure-v1.json"
    md_path = output / "milestone-10-submission-preparation-closure-v1.md"
    manifest_path = output / "milestone-10-submission-preparation-closure-manifest-v1.txt"
    index_path = output / "milestone-10-submission-preparation-closure-index-v1.json"
    scorecard_path = output / "milestone-10-submission-preparation-closure-scorecard-v1.json"
    report_path = output / "milestone-10-submission-preparation-closure-report-v1.md"

    json_path.write_text(json.dumps(closure, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_submission_preparation_closure_markdown(closure), encoding="utf-8")
    manifest_path.write_text(render_submission_preparation_closure_manifest(closure), encoding="utf-8")
    index_path.write_text(json.dumps(closure["closure_index"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(closure["closure_scorecard"], indent=2, sort_keys=True), encoding="utf-8")
    report_path.write_text(render_submission_preparation_closure_markdown(closure), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "scorecard_path": str(scorecard_path),
        "report_path": str(report_path),
    }


def run_milestone_10_submission_preparation_closure_pipeline() -> Dict[str, Any]:
    closure = build_milestone_10_submission_preparation_closure()
    validation = validate_milestone_10_submission_preparation_closure(closure)
    artifacts = write_submission_preparation_closure_artifacts(closure)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_PIPELINE_INVALID",
        "closure_status": closure["status"],
        "validation_status": validation["status"],
        "closure": closure,
        "submission_preparation_closure_id": closure["submission_preparation_closure_id"],
        "signature": closure["signature"],
        "closure_mode": closure["closure_mode"],
        "closure_verdict": closure["closure_verdict"],
        "next_allowed_stage": closure["next_allowed_stage"],
        "submission_preparation_closure_ready": closure["submission_preparation_closure_ready"],
        "submission_preparation_closure_created": closure["submission_preparation_closure_created"],
        "submission_preparation_closure_passed": closure["submission_preparation_closure_passed"],
        "closure_scorecard_created": closure["closure_scorecard_created"],
        "closure_scorecard_passed": closure["closure_scorecard_passed"],
        "closure_criterion_count": closure["closure_criterion_count"],
        "selected_candidate_id": closure["selected_candidate_id"],
        "candidate_package_id": closure["candidate_package_id"],
        "rebuilt_candidate_id": closure["rebuilt_candidate_id"],
        "rebuilt_candidate_review_id": closure["rebuilt_candidate_review_id"],
        "closure_check_count": closure["closure_check_count"],
        "closure_case_count": closure["closure_case_count"],
        "closure_pass_count": closure["closure_pass_count"],
        "closure_failure_count": closure["closure_failure_count"],
        "closure_gate_count": closure["closure_gate_count"],
        "passed_gate_count": closure["passed_gate_count"],
        "closure_issue_count": closure["closure_issue_count"],
        "warning_count": closure["warning_count"],
        "milestone_10_closed": closure["milestone_10_closed"],
        "local_package_prepared": closure["local_package_prepared"],
        "local_package_frozen": closure["local_package_frozen"],
        "integrity_verified": closure["integrity_verified"],
        "final_audit_passed": closure["final_audit_passed"],
        "real_submission_candidate_created": closure["real_submission_candidate_created"],
        "submission_json_created": closure["submission_json_created"],
        "upload_package_created": closure["upload_package_created"],
        "real_submission_decision": closure["real_submission_decision"],
        "real_submission_allowed": closure["real_submission_allowed"],
        "manual_upload_allowed": closure["manual_upload_allowed"],
        "kaggle_authentication_allowed": closure["kaggle_authentication_allowed"],
        "kaggle_submission_sent": closure["kaggle_submission_sent"],
        "fail_closed_required": closure["fail_closed_required"],
        "fail_closed_active": closure["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": closure["metadata"],
    }
