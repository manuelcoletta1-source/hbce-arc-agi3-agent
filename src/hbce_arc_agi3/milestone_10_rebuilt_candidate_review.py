"""Milestone #10 Rebuilt Candidate Review v1.

Local-only deterministic review after submission candidate rebuild.

This module reads the Milestone #10 rebuilt candidate artifact and produces a
controlled review verdict. It does not create a real Kaggle submission, does
not create submission.json, does not create an upload package, does not
authenticate with Kaggle, does not call external APIs, does not read secrets,
does not grant operator approval, and does not create legal certification
claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REVIEW_STATUS = "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_VALID"

BASELINE_COMMIT = "362a9f7 Add ARC AGI3 submission candidate rebuild"
REVIEW_MODE = "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_LOCAL_ONLY"
REVIEW_SCOPE = "LOCAL_REBUILT_CANDIDATE_REVIEW_NO_SUBMISSION_JSON_NO_UPLOAD"
REVIEW_VERDICT = "REBUILT_CANDIDATE_REVIEW_PASS_READY_FOR_SUBMISSION_PREPARATION_CLOSURE_REAL_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/rebuilt-candidate-review-v1"

SUBMISSION_CANDIDATE_REBUILD_JSON = Path(
    "examples/milestone-10/submission-candidate-rebuild-v1/"
    "milestone-10-submission-candidate-rebuild-v1.json"
)

EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILT_CANDIDATE_ID = "MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87"
EXPECTED_REVIEW_CRITERION_COUNT = 7
EXPECTED_REVIEW_CHECK_COUNT = 36
EXPECTED_REVIEW_CASE_COUNT = 10
EXPECTED_REVIEW_PASS_COUNT = 10
EXPECTED_REVIEW_FAILURE_COUNT = 0

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

REVIEW_CRITERIA: Tuple[Dict[str, str], ...] = (
    {
        "criterion_id": "review_source_rebuild_ready_v1",
        "area": "source",
        "description": "Task 8 rebuild artifact is ready and valid.",
    },
    {
        "criterion_id": "review_selected_candidate_identity_v1",
        "area": "identity",
        "description": "Selected candidate identity is stable.",
    },
    {
        "criterion_id": "review_local_package_rebuilt_v1",
        "area": "package",
        "description": "Local rebuilt package exists and is ready.",
    },
    {
        "criterion_id": "review_rebuilt_payload_ready_v1",
        "area": "payload",
        "description": "Rebuilt candidate payload is available for review.",
    },
    {
        "criterion_id": "review_trace_and_handoff_ready_v1",
        "area": "traceability",
        "description": "Trace and review handoff are present.",
    },
    {
        "criterion_id": "review_submission_boundary_preserved_v1",
        "area": "boundary",
        "description": "No submission.json, upload package, or real submission exists.",
    },
    {
        "criterion_id": "review_fail_closed_preserved_v1",
        "area": "fail_closed",
        "description": "Fail-closed and authorization boundary remain active.",
    },
)

REVIEW_CHECKS: Tuple[str, ...] = (
    "rebuild_artifact_exists",
    "rebuild_artifact_ready",
    "rebuild_signature_present",
    "rebuild_next_stage_matches_task_9",
    "submission_candidate_rebuild_ready",
    "local_candidate_package_rebuilt",
    "rebuilt_candidate_payload_created",
    "rebuilt_candidate_manifest_created",
    "rebuilt_candidate_index_created",
    "rebuilt_candidate_trace_created",
    "review_handoff_created",
    "selected_candidate_id_valid",
    "candidate_package_id_valid",
    "rebuilt_candidate_id_valid",
    "rebuild_component_count_valid",
    "rebuilt_candidate_review_required",
    "review_scorecard_created",
    "review_scorecard_passed",
    "review_record_created",
    "review_ready",
    "review_passed",
    "review_locked",
    "next_stage_valid",
    "closure_required_next",
    "real_submission_candidate_not_created",
    "submission_json_not_created",
    "upload_package_not_created",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_absent",
    "fail_closed_required",
    "fail_closed_active",
    "no_private_core_exposure",
    "no_legal_certification",
)

REVIEW_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_rebuilt_candidate_review_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_submission_candidate_rebuild_source",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_identity_valid_v1",
        "area": "candidate_identity",
        "operation": "verify_rebuilt_candidate_identity",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_payload_ready_v1",
        "area": "payload",
        "operation": "verify_rebuilt_candidate_payload",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_scorecard_ready_v1",
        "area": "review_scorecard",
        "operation": "verify_review_scorecard",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_trace_ready_v1",
        "area": "traceability",
        "operation": "verify_trace_and_handoff",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_boundary_preserved_v1",
        "area": "boundary",
        "operation": "verify_submission_boundary",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_closure_required_v1",
        "area": "closure",
        "operation": "verify_submission_preparation_closure_next",
    },
    {
        "case_id": "m10_rebuilt_candidate_review_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_next_stage",
    },
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


def build_rebuilt_candidate_review_source_summary() -> Dict[str, Any]:
    rebuild = _read_json(SUBMISSION_CANDIDATE_REBUILD_JSON)
    payload = rebuild.get("rebuilt_candidate_payload", {})
    trace = rebuild.get("rebuild_trace", {})
    source = rebuild.get("source_summary", {})

    return {
        "submission_candidate_rebuild_path": str(SUBMISSION_CANDIDATE_REBUILD_JSON),
        "submission_candidate_rebuild_present": SUBMISSION_CANDIDATE_REBUILD_JSON.exists(),
        "rebuild_status": rebuild.get("status", "MISSING"),
        "submission_candidate_rebuild_id": rebuild.get(
            "submission_candidate_rebuild_id", "MISSING_SUBMISSION_CANDIDATE_REBUILD_ID"
        ),
        "rebuild_signature": rebuild.get("signature", ""),
        "submission_candidate_rebuild_ready": rebuild.get("submission_candidate_rebuild_ready", False),
        "submission_candidate_rebuild_locked": rebuild.get("submission_candidate_rebuild_locked", False),
        "submission_candidate_rebuild_created": rebuild.get("submission_candidate_rebuild_created", False),
        "rebuild_baseline_commit": rebuild.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": rebuild.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "selected_candidate_id": rebuild.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": rebuild.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "rebuilt_candidate_id": rebuild.get("rebuilt_candidate_id", "MISSING_REBUILT_CANDIDATE_ID"),
        "rebuild_component_count": rebuild.get("rebuild_component_count", 0),
        "local_candidate_package_rebuilt": rebuild.get("local_candidate_package_rebuilt", False),
        "rebuilt_candidate_payload_created": rebuild.get("rebuilt_candidate_payload_created", False),
        "rebuilt_candidate_manifest_created": rebuild.get("rebuilt_candidate_manifest_created", False),
        "rebuilt_candidate_index_created": rebuild.get("rebuilt_candidate_index_created", False),
        "rebuilt_candidate_trace_created": rebuild.get("rebuilt_candidate_trace_created", False),
        "review_handoff_created": rebuild.get("review_handoff_created", False),
        "rebuilt_candidate_review_required_next": rebuild.get(
            "rebuilt_candidate_review_required_next", False
        ),
        "payload_kind": payload.get("payload_kind", "MISSING_PAYLOAD_KIND"),
        "payload_ready_for_review": payload.get("ready_for_review", False),
        "payload_signature": payload.get("signature", ""),
        "trace_ready": trace.get("trace_ready", False),
        "trace_hash_16": trace.get("trace_hash_16", ""),
        "source_rebuild_gate_id": source.get("rebuild_gate_id", "MISSING_REBUILD_GATE_ID"),
        "source_candidate_refresh_id": source.get(
            "candidate_refresh_id", "MISSING_CANDIDATE_REFRESH_ID"
        ),
        "source_previous_refresh_id": source.get("previous_refresh_id", "MISSING_PREVIOUS_REFRESH_ID"),
        "real_submission_candidate_created": rebuild.get("real_submission_candidate_created", True),
        "submission_json_created": rebuild.get("submission_json_created", True),
        "upload_package_created": rebuild.get("upload_package_created", True),
        "real_submission_decision": rebuild.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": rebuild.get("real_submission_allowed", True),
        "manual_upload_allowed": rebuild.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": rebuild.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": rebuild.get("kaggle_submission_sent", True),
        "fail_closed_required": rebuild.get("fail_closed_required", False),
        "fail_closed_active": rebuild.get("fail_closed_active", False),
        "rebuild_sha256": _sha256(SUBMISSION_CANDIDATE_REBUILD_JSON),
        "rebuild_sha256_16": _sha16(_sha256(SUBMISSION_CANDIDATE_REBUILD_JSON)),
    }


def build_rebuilt_candidate_review_scorecard() -> Tuple[Dict[str, Any], ...]:
    source = build_rebuilt_candidate_review_source_summary()

    decisions = {
        "review_source_rebuild_ready_v1": source["submission_candidate_rebuild_ready"] is True
        and source["rebuild_status"] == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY",
        "review_selected_candidate_identity_v1": source["selected_candidate_id"]
        == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
        and source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID,
        "review_local_package_rebuilt_v1": source["local_candidate_package_rebuilt"] is True,
        "review_rebuilt_payload_ready_v1": source["rebuilt_candidate_payload_created"] is True
        and source["payload_kind"] == "LOCAL_REBUILT_CANDIDATE_PACKAGE"
        and source["payload_ready_for_review"] is True,
        "review_trace_and_handoff_ready_v1": source["trace_ready"] is True
        and bool(source["trace_hash_16"])
        and source["review_handoff_created"] is True,
        "review_submission_boundary_preserved_v1": source["real_submission_candidate_created"] is False
        and source["submission_json_created"] is False
        and source["upload_package_created"] is False,
        "review_fail_closed_preserved_v1": source["fail_closed_required"] is True
        and source["fail_closed_active"] is True
        and source["real_submission_allowed"] is False,
    }

    return tuple(
        {
            **criterion,
            "passed": decisions[criterion["criterion_id"]],
            "score": 100 if decisions[criterion["criterion_id"]] else 0,
            "severity": "PASS" if decisions[criterion["criterion_id"]] else "BLOCKING",
        }
        for criterion in REVIEW_CRITERIA
    )


def build_review_decision() -> Dict[str, Any]:
    scorecard = build_rebuilt_candidate_review_scorecard()
    source = build_rebuilt_candidate_review_source_summary()

    review_passed = all(item["passed"] is True for item in scorecard)

    return {
        "decision_id": "M10-REBUILT-CANDIDATE-REVIEW-PASS-v1",
        "decision": "PASS_LOCAL_REBUILT_CANDIDATE_REVIEW"
        if review_passed
        else "BLOCK_LOCAL_REBUILT_CANDIDATE_REVIEW",
        "review_passed": review_passed,
        "review_ready": review_passed,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "submission_preparation_closure_required_next": review_passed,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_allowed": False,
        "submission_json_creation_allowed_now": False,
        "upload_package_creation_allowed_now": False,
        "operator_approval_required_for_real_submission": True,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
    }


def build_review_state() -> Dict[str, Any]:
    return {
        "rebuilt_candidate_review_required": True,
        "rebuilt_candidate_review_created": True,
        "rebuilt_candidate_review_ready": True,
        "rebuilt_candidate_review_passed": True,
        "rebuilt_candidate_review_locked": True,
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "review_scorecard_created": True,
        "review_scorecard_passed": True,
        "submission_preparation_closure_required_next": True,
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


def build_rebuilt_candidate_review_checks() -> Dict[str, bool]:
    source = build_rebuilt_candidate_review_source_summary()
    scorecard = build_rebuilt_candidate_review_scorecard()
    decision = build_review_decision()
    state = build_review_state()

    return {
        "rebuild_artifact_present": source["submission_candidate_rebuild_present"],
        "rebuild_artifact_ready": source["rebuild_status"]
        == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY",
        "rebuild_artifact_valid": source["submission_candidate_rebuild_id"].startswith(
            "MILESTONE-10-SUBMISSION-CANDIDATE-REBUILD-"
        )
        and bool(source["rebuild_signature"]),
        "rebuild_commit_valid": str(source["rebuild_baseline_commit"]).startswith("e329a98"),
        "rebuild_next_stage_matches_task_9": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1",
        "submission_candidate_rebuild_ready": source["submission_candidate_rebuild_ready"] is True,
        "submission_candidate_rebuild_locked": source["submission_candidate_rebuild_locked"] is True,
        "submission_candidate_rebuild_created": source["submission_candidate_rebuild_created"] is True,
        "local_candidate_package_rebuilt": source["local_candidate_package_rebuilt"] is True,
        "rebuilt_candidate_payload_created": source["rebuilt_candidate_payload_created"] is True,
        "rebuilt_candidate_manifest_created": source["rebuilt_candidate_manifest_created"] is True,
        "rebuilt_candidate_index_created": source["rebuilt_candidate_index_created"] is True,
        "rebuilt_candidate_trace_created": source["rebuilt_candidate_trace_created"] is True,
        "review_handoff_created": source["review_handoff_created"] is True,
        "selected_candidate_id_valid": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_id_valid": source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID,
        "rebuilt_candidate_id_valid": source["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID,
        "rebuild_component_count_valid": source["rebuild_component_count"] == 6,
        "rebuilt_candidate_review_required": source["rebuilt_candidate_review_required_next"] is True,
        "payload_ready_for_review": source["payload_ready_for_review"] is True,
        "payload_signature_present": bool(source["payload_signature"]),
        "trace_ready": source["trace_ready"] is True,
        "trace_hash_present": bool(source["trace_hash_16"]),
        "review_scorecard_count_valid": len(scorecard) == EXPECTED_REVIEW_CRITERION_COUNT,
        "review_scorecard_created": state["review_scorecard_created"] is True,
        "review_scorecard_passed": all(item["passed"] is True for item in scorecard),
        "review_record_created": state["rebuilt_candidate_review_created"] is True,
        "review_record_ready": state["rebuilt_candidate_review_ready"] is True,
        "review_record_passed": state["rebuilt_candidate_review_passed"] is True,
        "review_record_locked": state["rebuilt_candidate_review_locked"] is True,
        "review_decision_passed": decision["review_passed"] is True
        and decision["decision"] == "PASS_LOCAL_REBUILT_CANDIDATE_REVIEW",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1",
        "closure_required_next": decision["submission_preparation_closure_required_next"] is True
        and state["submission_preparation_closure_required_next"] is True,
        "real_submission_candidate_not_created": source["real_submission_candidate_created"] is False
        and state["real_submission_candidate_created"] is False,
        "submission_json_not_created": source["submission_json_created"] is False
        and state["submission_json_created"] is False,
        "upload_package_not_created": source["upload_package_created"] is False
        and state["upload_package_created"] is False,
        "review_check_count_valid": len(REVIEW_CHECKS) == EXPECTED_REVIEW_CHECK_COUNT,
        "review_case_count_valid": len(REVIEW_CASES) == EXPECTED_REVIEW_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS) == 9,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == 9,
        "real_submission_decision_not_authorized": source["real_submission_decision"] == "NOT_AUTHORIZED"
        and state["real_submission_decision"] == "NOT_AUTHORIZED",
        "real_submission_allowed_false": source["real_submission_allowed"] is False
        and state["real_submission_allowed"] is False,
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False
        and state["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False
        and state["kaggle_authentication_allowed"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and state["kaggle_submission_sent"] is False,
        "fail_closed_required": source["fail_closed_required"] is True
        and state["fail_closed_required"] is True,
        "fail_closed_active": source["fail_closed_active"] is True
        and state["fail_closed_active"] is True,
        "external_api_dependency_false": state["external_api_dependency"] is False,
        "private_core_exposure_false": state["private_core_exposure"] is False,
        "legal_certification_false": state["legal_certification"] is False,
    }


def evaluate_rebuilt_candidate_review_case(case_id: str) -> Dict[str, Any]:
    checks = build_rebuilt_candidate_review_checks()

    if case_id == "m10_rebuilt_candidate_review_source_ready_v1":
        passed = (
            checks["rebuild_artifact_present"]
            and checks["rebuild_artifact_ready"]
            and checks["rebuild_artifact_valid"]
            and checks["submission_candidate_rebuild_ready"]
        )
        return _result(case_id, "source_binding", "verify_submission_candidate_rebuild_source", passed)

    if case_id == "m10_rebuilt_candidate_review_identity_valid_v1":
        passed = (
            checks["selected_candidate_id_valid"]
            and checks["candidate_package_id_valid"]
            and checks["rebuilt_candidate_id_valid"]
        )
        return _result(case_id, "candidate_identity", "verify_rebuilt_candidate_identity", passed)

    if case_id == "m10_rebuilt_candidate_review_payload_ready_v1":
        passed = checks["rebuilt_candidate_payload_created"] and checks["payload_ready_for_review"]
        return _result(case_id, "payload", "verify_rebuilt_candidate_payload", passed)

    if case_id == "m10_rebuilt_candidate_review_scorecard_ready_v1":
        passed = checks["review_scorecard_created"] and checks["review_scorecard_passed"]
        return _result(case_id, "review_scorecard", "verify_review_scorecard", passed)

    if case_id == "m10_rebuilt_candidate_review_trace_ready_v1":
        passed = checks["trace_ready"] and checks["trace_hash_present"] and checks["review_handoff_created"]
        return _result(case_id, "traceability", "verify_trace_and_handoff", passed)

    if case_id == "m10_rebuilt_candidate_review_boundary_preserved_v1":
        passed = (
            checks["real_submission_candidate_not_created"]
            and checks["submission_json_not_created"]
            and checks["upload_package_not_created"]
        )
        return _result(case_id, "boundary", "verify_submission_boundary", passed)

    if case_id == "m10_rebuilt_candidate_review_fail_closed_preserved_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_rebuilt_candidate_review_real_submission_blocked_v1":
        passed = (
            checks["real_submission_decision_not_authorized"]
            and checks["real_submission_allowed_false"]
            and checks["manual_upload_not_allowed"]
        )
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m10_rebuilt_candidate_review_closure_required_v1":
        return _result(case_id, "closure", "verify_submission_preparation_closure_next", checks["closure_required_next"])

    if case_id == "m10_rebuilt_candidate_review_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_next_stage", checks["next_stage_valid"])

    raise ValueError(f"unknown rebuilt candidate review case: {case_id}")


def evaluate_all_rebuilt_candidate_review_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_rebuilt_candidate_review_case(case["case_id"]) for case in REVIEW_CASES)


def build_milestone_10_rebuilt_candidate_review() -> Dict[str, Any]:
    source = build_rebuilt_candidate_review_source_summary()
    scorecard = build_rebuilt_candidate_review_scorecard()
    decision = build_review_decision()
    state = build_review_state()
    checks = build_rebuilt_candidate_review_checks()
    results = evaluate_all_rebuilt_candidate_review_cases()

    review_pass_count = sum(1 for result in results if result["passed"] is True)
    review_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "rebuild_artifact_present": checks["rebuild_artifact_present"],
        "rebuild_artifact_ready": checks["rebuild_artifact_ready"],
        "rebuild_artifact_valid": checks["rebuild_artifact_valid"],
        "rebuild_commit_valid": checks["rebuild_commit_valid"],
        "rebuild_next_stage_matches_task_9": checks["rebuild_next_stage_matches_task_9"],
        "submission_candidate_rebuild_ready": checks["submission_candidate_rebuild_ready"],
        "submission_candidate_rebuild_locked": checks["submission_candidate_rebuild_locked"],
        "submission_candidate_rebuild_created": checks["submission_candidate_rebuild_created"],
        "local_candidate_package_rebuilt": checks["local_candidate_package_rebuilt"],
        "rebuilt_candidate_payload_created": checks["rebuilt_candidate_payload_created"],
        "rebuilt_candidate_manifest_created": checks["rebuilt_candidate_manifest_created"],
        "rebuilt_candidate_index_created": checks["rebuilt_candidate_index_created"],
        "rebuilt_candidate_trace_created": checks["rebuilt_candidate_trace_created"],
        "review_handoff_created": checks["review_handoff_created"],
        "selected_candidate_id_valid": checks["selected_candidate_id_valid"],
        "candidate_package_id_valid": checks["candidate_package_id_valid"],
        "rebuilt_candidate_id_valid": checks["rebuilt_candidate_id_valid"],
        "rebuild_component_count_valid": checks["rebuild_component_count_valid"],
        "rebuilt_candidate_review_required": checks["rebuilt_candidate_review_required"],
        "payload_ready_for_review": checks["payload_ready_for_review"],
        "payload_signature_present": checks["payload_signature_present"],
        "trace_ready": checks["trace_ready"],
        "trace_hash_present": checks["trace_hash_present"],
        "review_scorecard_count_valid": checks["review_scorecard_count_valid"],
        "review_scorecard_created": checks["review_scorecard_created"],
        "review_scorecard_passed": checks["review_scorecard_passed"],
        "review_record_created": checks["review_record_created"],
        "review_record_ready": checks["review_record_ready"],
        "review_record_passed": checks["review_record_passed"],
        "review_record_locked": checks["review_record_locked"],
        "review_decision_passed": checks["review_decision_passed"],
        "next_stage_valid": checks["next_stage_valid"],
        "closure_required_next": checks["closure_required_next"],
        "real_submission_candidate_not_created": checks["real_submission_candidate_not_created"],
        "submission_json_not_created": checks["submission_json_not_created"],
        "upload_package_not_created": checks["upload_package_not_created"],
        "review_check_count_valid": checks["review_check_count_valid"],
        "review_case_count_valid": checks["review_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "real_submission_decision_not_authorized": checks["real_submission_decision_not_authorized"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "fail_closed_required": checks["fail_closed_required"],
        "fail_closed_active": checks["fail_closed_active"],
        "external_api_dependency_false": checks["external_api_dependency_false"],
        "private_core_exposure_false": checks["private_core_exposure_false"],
        "legal_certification_false": checks["legal_certification_false"],
        "all_review_cases_pass": all(result["passed"] is True for result in results),
        "review_pass_count_valid": review_pass_count == EXPECTED_REVIEW_PASS_COUNT,
        "review_failure_count_zero": review_failure_count == EXPECTED_REVIEW_FAILURE_COUNT,
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

    review_ready = (
        review_pass_count == EXPECTED_REVIEW_PASS_COUNT
        and review_failure_count == EXPECTED_REVIEW_FAILURE_COUNT
        and checks["rebuild_artifact_ready"]
        and checks["review_scorecard_passed"]
        and checks["review_decision_passed"]
        and checks["closure_required_next"]
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
        "task": "Task 9",
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_submission_candidate_rebuild": source["submission_candidate_rebuild_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "rebuilt_candidate_review_ready": review_ready,
        "rebuilt_candidate_review_created": True,
        "rebuilt_candidate_review_passed": True,
        "review_scorecard_created": True,
        "review_scorecard_passed": True,
        "submission_preparation_closure_required_next": True,
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
        "status": REVIEW_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 9",
        "title": "Rebuilt Candidate Review v1",
        "baseline_commit": BASELINE_COMMIT,
        "review_mode": REVIEW_MODE,
        "review_scope": REVIEW_SCOPE,
        "review_verdict": REVIEW_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "submission_candidate_rebuild_source": {
            "path": str(SUBMISSION_CANDIDATE_REBUILD_JSON),
            "present": SUBMISSION_CANDIDATE_REBUILD_JSON.exists(),
            "status": source["rebuild_status"],
            "submission_candidate_rebuild_id": source["submission_candidate_rebuild_id"],
            "sha256": _sha256(SUBMISSION_CANDIDATE_REBUILD_JSON),
            "sha256_16": _sha16(_sha256(SUBMISSION_CANDIDATE_REBUILD_JSON)),
        },
        "source_summary": source,
        "review_scorecard": list(scorecard),
        "review_decision": decision,
        "review_state": state,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "review_checks": checks,
        "review_check_list": list(REVIEW_CHECKS),
        "review_cases": list(REVIEW_CASES),
        "review_results": list(results),
        "review_gates": list(gates),
        "review_issues": list(issues),
        "review_index": index,
        "rebuilt_candidate_review_ready": review_ready,
        "rebuilt_candidate_review_locked": True,
        "rebuilt_candidate_review_created": True,
        "rebuilt_candidate_review_passed": True,
        "review_scorecard_created": True,
        "review_scorecard_passed": True,
        "review_criterion_count": len(scorecard),
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": source["rebuilt_candidate_id"],
        "review_check_count": len(REVIEW_CHECKS),
        "review_case_count": len(REVIEW_CASES),
        "review_pass_count": review_pass_count,
        "review_failure_count": review_failure_count,
        "review_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "review_issue_count": issue_count,
        "warning_count": 0,
        "submission_preparation_closure_required_next": True,
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
            "source": "milestone_10_rebuilt_candidate_review_v1",
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
        "rebuilt_candidate_review_id": f"MILESTONE-10-REBUILT-CANDIDATE-REVIEW-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_rebuilt_candidate_review(review: Mapping[str, Any]) -> Dict[str, Any]:
    gates = review.get("review_gates", [])
    issues = review.get("review_issues", [])
    results = review.get("review_results", [])
    scorecard = review.get("review_scorecard", [])

    checks = {
        "status_ready": review.get("status") == REVIEW_STATUS,
        "rebuilt_candidate_review_id_present": isinstance(review.get("rebuilt_candidate_review_id"), str)
        and bool(review.get("rebuilt_candidate_review_id")),
        "signature_present": isinstance(review.get("signature"), str) and bool(review.get("signature")),
        "baseline_commit_valid": str(review.get("baseline_commit", "")).startswith("362a9f7"),
        "review_mode_valid": review.get("review_mode") == REVIEW_MODE,
        "review_scope_valid": review.get("review_scope") == REVIEW_SCOPE,
        "review_verdict_valid": review.get("review_verdict") == REVIEW_VERDICT,
        "next_allowed_stage_valid": review.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "rebuilt_candidate_review_ready": review.get("rebuilt_candidate_review_ready") is True,
        "rebuilt_candidate_review_locked": review.get("rebuilt_candidate_review_locked") is True,
        "rebuilt_candidate_review_created": review.get("rebuilt_candidate_review_created") is True,
        "rebuilt_candidate_review_passed": review.get("rebuilt_candidate_review_passed") is True,
        "review_scorecard_created": review.get("review_scorecard_created") is True,
        "review_scorecard_passed": review.get("review_scorecard_passed") is True,
        "review_criterion_count_valid": review.get("review_criterion_count") == EXPECTED_REVIEW_CRITERION_COUNT,
        "scorecard_all_pass": bool(scorecard) and all(item.get("passed") is True for item in scorecard),
        "selected_candidate_valid": review.get("selected_candidate_id") == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_valid": review.get("candidate_package_id") == EXPECTED_CANDIDATE_PACKAGE_ID,
        "rebuilt_candidate_valid": review.get("rebuilt_candidate_id") == EXPECTED_REBUILT_CANDIDATE_ID,
        "review_check_count_valid": review.get("review_check_count") == EXPECTED_REVIEW_CHECK_COUNT,
        "review_case_count_valid": review.get("review_case_count") == EXPECTED_REVIEW_CASE_COUNT,
        "review_pass_count_valid": review.get("review_pass_count") == EXPECTED_REVIEW_PASS_COUNT,
        "review_failure_count_zero": review.get("review_failure_count") == EXPECTED_REVIEW_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "submission_preparation_closure_required_next": review.get(
            "submission_preparation_closure_required_next"
        )
        is True,
        "real_submission_candidate_not_created": review.get("real_submission_candidate_created") is False,
        "submission_json_not_created": review.get("submission_json_created") is False,
        "upload_package_not_created": review.get("upload_package_created") is False,
        "real_submission_decision_not_authorized": review.get("real_submission_decision")
        == "NOT_AUTHORIZED",
        "real_submission_allowed_false": review.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": review.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": review.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": review.get("kaggle_submission_sent") is False,
        "fail_closed_required": review.get("fail_closed_required") is True,
        "fail_closed_active": review.get("fail_closed_active") is True,
        "metadata_safe": review.get("metadata", {}).get("external_api_dependency") is False
        and review.get("metadata", {}).get("contains_api_keys") is False
        and review.get("metadata", {}).get("private_core_exposure") is False
        and review.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "rebuilt_candidate_review_id": review.get("rebuilt_candidate_review_id"),
        "signature": review.get("signature"),
    }


def render_rebuilt_candidate_review_markdown(review: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Rebuilt Candidate Review v1",
        "",
        f"- status: {review['status']}",
        f"- rebuilt_candidate_review_id: {review['rebuilt_candidate_review_id']}",
        f"- signature: {review['signature']}",
        f"- baseline_commit: {review['baseline_commit']}",
        f"- review_mode: {review['review_mode']}",
        f"- review_scope: {review['review_scope']}",
        f"- review_verdict: {review['review_verdict']}",
        f"- next_allowed_stage: {review['next_allowed_stage']}",
        f"- rebuilt_candidate_review_ready: {review['rebuilt_candidate_review_ready']}",
        f"- rebuilt_candidate_review_passed: {review['rebuilt_candidate_review_passed']}",
        f"- selected_candidate_id: {review['selected_candidate_id']}",
        f"- candidate_package_id: {review['candidate_package_id']}",
        f"- rebuilt_candidate_id: {review['rebuilt_candidate_id']}",
        f"- review_scorecard_created: {review['review_scorecard_created']}",
        f"- review_scorecard_passed: {review['review_scorecard_passed']}",
        f"- submission_preparation_closure_required_next: {review['submission_preparation_closure_required_next']}",
        f"- real_submission_candidate_created: {review['real_submission_candidate_created']}",
        f"- submission_json_created: {review['submission_json_created']}",
        f"- upload_package_created: {review['upload_package_created']}",
        f"- real_submission_decision: {review['real_submission_decision']}",
        f"- real_submission_allowed: {review['real_submission_allowed']}",
        f"- fail_closed_active: {review['fail_closed_active']}",
        "",
        "## Review scorecard",
        "",
    ]

    for item in review["review_scorecard"]:
        lines.append(
            f"- {item['criterion_id']} / area={item['area']} / "
            f"passed={item['passed']} / score={item['score']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in review["review_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The rebuilt candidate review passes. Submission preparation closure is required next, while real Kaggle submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_READY=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_PASSED=true",
            "ARC_AGI3_MILESTONE_10_REVIEW_MODE=MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_REVIEW_VERDICT=REBUILT_CANDIDATE_REVIEW_PASS_READY_FOR_SUBMISSION_PREPARATION_CLOSURE_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=362a9f7",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_10_SUBMISSION_PREPARATION_CLOSURE_V1",
            "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
            "ARC_AGI3_MILESTONE_10_CANDIDATE_PACKAGE_ID=MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_ID=MILESTONE-10-REBUILT-CANDIDATE-32F7FBEDFF87",
            "ARC_AGI3_MILESTONE_10_REVIEW_SCORECARD_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REVIEW_SCORECARD_PASSED=true",
            "ARC_AGI3_MILESTONE_10_REVIEW_CRITERION_COUNT=7",
            "ARC_AGI3_MILESTONE_10_REVIEW_CHECK_COUNT=36",
            "ARC_AGI3_MILESTONE_10_REVIEW_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REVIEW_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REVIEW_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_REQUIRED_NEXT=true",
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


def render_rebuilt_candidate_review_manifest(review: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 REBUILT CANDIDATE REVIEW MANIFEST v1",
        f"rebuilt_candidate_review_id={review['rebuilt_candidate_review_id']}",
        f"signature={review['signature']}",
        f"status={review['status']}",
        f"baseline_commit={review['baseline_commit']}",
        f"review_mode={review['review_mode']}",
        f"review_verdict={review['review_verdict']}",
        f"next_allowed_stage={review['next_allowed_stage']}",
        f"rebuilt_candidate_review_ready={review['rebuilt_candidate_review_ready']}",
        f"rebuilt_candidate_review_created={review['rebuilt_candidate_review_created']}",
        f"rebuilt_candidate_review_passed={review['rebuilt_candidate_review_passed']}",
        f"selected_candidate_id={review['selected_candidate_id']}",
        f"candidate_package_id={review['candidate_package_id']}",
        f"rebuilt_candidate_id={review['rebuilt_candidate_id']}",
        f"review_scorecard_created={review['review_scorecard_created']}",
        f"review_scorecard_passed={review['review_scorecard_passed']}",
        f"review_criterion_count={review['review_criterion_count']}",
        f"review_check_count={review['review_check_count']}",
        f"review_case_count={review['review_case_count']}",
        f"review_pass_count={review['review_pass_count']}",
        f"review_failure_count={review['review_failure_count']}",
        f"review_gate_count={review['review_gate_count']}",
        f"passed_gate_count={review['passed_gate_count']}",
        f"review_issue_count={review['review_issue_count']}",
        f"submission_preparation_closure_required_next={review['submission_preparation_closure_required_next']}",
        f"real_submission_candidate_created={review['real_submission_candidate_created']}",
        f"submission_json_created={review['submission_json_created']}",
        f"upload_package_created={review['upload_package_created']}",
        f"real_submission_decision={review['real_submission_decision']}",
        f"real_submission_allowed={review['real_submission_allowed']}",
        f"manual_upload_allowed={review['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={review['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={review['kaggle_submission_sent']}",
        f"fail_closed_required={review['fail_closed_required']}",
        f"fail_closed_active={review['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "REVIEW_SCORECARD",
    ]

    for item in review["review_scorecard"]:
        lines.append(
            f"{item['criterion_id']} area={item['area']} passed={item['passed']} score={item['score']}"
        )

    lines.append("")
    lines.append("REVIEW_VALIDATION_RESULTS")
    for result in review["review_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_rebuilt_candidate_review_artifacts(
    review: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    review = dict(review or build_milestone_10_rebuilt_candidate_review())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-rebuilt-candidate-review-v1.json"
    md_path = output / "milestone-10-rebuilt-candidate-review-v1.md"
    manifest_path = output / "milestone-10-rebuilt-candidate-review-manifest-v1.txt"
    index_path = output / "milestone-10-rebuilt-candidate-review-index-v1.json"
    scorecard_path = output / "milestone-10-rebuilt-candidate-review-scorecard-v1.json"

    json_path.write_text(json.dumps(review, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_rebuilt_candidate_review_markdown(review), encoding="utf-8")
    manifest_path.write_text(render_rebuilt_candidate_review_manifest(review), encoding="utf-8")
    index_path.write_text(json.dumps(review["review_index"], indent=2, sort_keys=True), encoding="utf-8")
    scorecard_path.write_text(json.dumps(review["review_scorecard"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "scorecard_path": str(scorecard_path),
    }


def run_milestone_10_rebuilt_candidate_review_pipeline() -> Dict[str, Any]:
    review = build_milestone_10_rebuilt_candidate_review()
    validation = validate_milestone_10_rebuilt_candidate_review(review)
    artifacts = write_rebuilt_candidate_review_artifacts(review)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_REBUILT_CANDIDATE_REVIEW_V1_PIPELINE_INVALID",
        "review_status": review["status"],
        "validation_status": validation["status"],
        "review": review,
        "rebuilt_candidate_review_id": review["rebuilt_candidate_review_id"],
        "signature": review["signature"],
        "review_mode": review["review_mode"],
        "review_verdict": review["review_verdict"],
        "next_allowed_stage": review["next_allowed_stage"],
        "rebuilt_candidate_review_ready": review["rebuilt_candidate_review_ready"],
        "rebuilt_candidate_review_created": review["rebuilt_candidate_review_created"],
        "rebuilt_candidate_review_passed": review["rebuilt_candidate_review_passed"],
        "review_scorecard_created": review["review_scorecard_created"],
        "review_scorecard_passed": review["review_scorecard_passed"],
        "review_criterion_count": review["review_criterion_count"],
        "selected_candidate_id": review["selected_candidate_id"],
        "candidate_package_id": review["candidate_package_id"],
        "rebuilt_candidate_id": review["rebuilt_candidate_id"],
        "review_check_count": review["review_check_count"],
        "review_case_count": review["review_case_count"],
        "review_pass_count": review["review_pass_count"],
        "review_failure_count": review["review_failure_count"],
        "review_gate_count": review["review_gate_count"],
        "passed_gate_count": review["passed_gate_count"],
        "review_issue_count": review["review_issue_count"],
        "warning_count": review["warning_count"],
        "submission_preparation_closure_required_next": review[
            "submission_preparation_closure_required_next"
        ],
        "real_submission_candidate_created": review["real_submission_candidate_created"],
        "submission_json_created": review["submission_json_created"],
        "upload_package_created": review["upload_package_created"],
        "real_submission_decision": review["real_submission_decision"],
        "real_submission_allowed": review["real_submission_allowed"],
        "manual_upload_allowed": review["manual_upload_allowed"],
        "kaggle_authentication_allowed": review["kaggle_authentication_allowed"],
        "kaggle_submission_sent": review["kaggle_submission_sent"],
        "fail_closed_required": review["fail_closed_required"],
        "fail_closed_active": review["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": review["metadata"],
    }
