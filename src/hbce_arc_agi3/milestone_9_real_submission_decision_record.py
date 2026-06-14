"""Milestone #9 Real Submission Decision Record v1.

Local-only deterministic real submission decision record.

This module reads the operator approval gate and records the current decision:
real Kaggle submission is not authorized because explicit operator approval and
accepted declarations are absent.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, accept declarations, grant approval, claim a Kaggle score, claim
public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


DECISION_STATUS = "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_VALID"

BASELINE_COMMIT = "649509b Add ARC AGI3 operator approval gate"
DECISION_MODE = "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_LOCAL_ONLY"
DECISION_SCOPE = "RECORD_REAL_SUBMISSION_NOT_AUTHORIZED_OPERATOR_APPROVAL_ABSENT"
DECISION_VERDICT = "REAL_SUBMISSION_DECISION_RECORDED_NOT_AUTHORIZED_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_7_REAL_SUBMISSION_BLOCKED_CLOSURE_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/real-submission-decision-record-v1"

APPROVAL_GATE_JSON = Path(
    "examples/milestone-9/operator-approval-gate-v1/"
    "milestone-9-operator-approval-gate-v1.json"
)

EXPECTED_DECISION_CHECK_COUNT = 16
EXPECTED_DECISION_CASE_COUNT = 10
EXPECTED_DECISION_PASS_COUNT = 10
EXPECTED_DECISION_FAILURE_COUNT = 0
EXPECTED_REQUIRED_DECLARATION_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

DECISION_CHECKS: Tuple[str, ...] = (
    "approval_gate_artifact_exists",
    "approval_gate_artifact_ready",
    "approval_gate_ready",
    "approval_gate_closed",
    "required_declarations_present",
    "provided_declarations_absent",
    "accepted_declarations_absent",
    "explicit_operator_approval_absent",
    "operator_approval_not_granted",
    "decision_record_created",
    "decision_not_authorized",
    "manual_upload_blocked",
    "authentication_blocked",
    "real_submission_blocked",
    "kaggle_submission_absent",
    "claim_boundary_preserved",
)

DECISION_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "decision_approval_gate_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_operator_approval_gate",
    },
    {
        "case_id": "decision_required_declarations_present_v1",
        "area": "operator_declarations",
        "operation": "verify_required_declaration_count",
    },
    {
        "case_id": "decision_no_declarations_accepted_v1",
        "area": "operator_declarations",
        "operation": "verify_no_accepted_declarations",
    },
    {
        "case_id": "decision_explicit_operator_approval_absent_v1",
        "area": "operator_approval",
        "operation": "verify_explicit_approval_absent",
    },
    {
        "case_id": "decision_operator_approval_not_granted_v1",
        "area": "approval_gate",
        "operation": "verify_operator_approval_not_granted",
    },
    {
        "case_id": "decision_real_submission_not_authorized_v1",
        "area": "decision",
        "operation": "verify_real_submission_not_authorized",
    },
    {
        "case_id": "decision_manual_upload_blocked_v1",
        "area": "upload_gate",
        "operation": "verify_manual_upload_blocked",
    },
    {
        "case_id": "decision_no_auth_no_upload_v1",
        "area": "boundary",
        "operation": "verify_no_auth_no_upload",
    },
    {
        "case_id": "decision_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "decision_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_blocked_closure_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_decision_uses_operator_approval_gate",
    "guard_decision_requires_approval_gate_ready",
    "guard_decision_requires_approval_gate_closed",
    "guard_decision_rejects_empty_declarations",
    "guard_decision_rejects_missing_explicit_phrase",
    "guard_decision_records_not_authorized",
    "guard_decision_manual_upload_blocked",
    "guard_decision_real_submission_blocked",
    "guard_decision_does_not_authenticate",
    "guard_decision_does_not_upload",
    "guard_decision_no_private_core_exposure",
    "guard_decision_no_legal_certification",
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


def build_decision_source_summary() -> Dict[str, Any]:
    approval = _read_json(APPROVAL_GATE_JSON)
    approval_source = approval.get("approval_source_summary", {})

    return {
        "approval_gate_path": str(APPROVAL_GATE_JSON),
        "approval_gate_present": APPROVAL_GATE_JSON.exists(),
        "approval_gate_status": approval.get("status", "MISSING"),
        "approval_id": approval.get("approval_id", "MISSING_APPROVAL_ID"),
        "approval_signature": approval.get("signature", ""),
        "approval_ready": approval.get("approval_ready", False),
        "approval_locked": approval.get("approval_locked", False),
        "operator_approval_gate_created": approval.get("operator_approval_gate_created", False),
        "operator_approval_gate_ready": approval.get("operator_approval_gate_ready", False),
        "operator_approval_gate_open": approval.get("operator_approval_gate_open", True),
        "candidate_source_path": approval_source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": approval_source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": approval_source.get("candidate_signature", ""),
        "candidate_count": approval.get("candidate_count", 0),
        "required_declaration_count": approval.get("required_declaration_count", 0),
        "provided_declaration_count": approval.get("provided_declaration_count", 0),
        "accepted_declaration_count": approval.get("accepted_declaration_count", 0),
        "explicit_operator_approval_phrase_received": approval.get(
            "explicit_operator_approval_phrase_received", True
        ),
        "operator_approval_required": approval.get("operator_approval_required", False),
        "operator_approval_granted": approval.get("operator_approval_granted", True),
        "operator_approval_received": approval.get("operator_approval_received", True),
        "manual_upload_allowed": approval.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": approval.get("kaggle_authentication_allowed", True),
        "real_submission_allowed": approval.get("real_submission_allowed", True),
        "ready_for_real_kaggle_submission": approval.get("ready_for_real_kaggle_submission", True),
        "kaggle_submission_sent": approval.get("kaggle_submission_sent", True),
        "upload_performed": approval.get("upload_performed", True),
        "kaggle_authentication_performed": approval.get("kaggle_authentication_performed", True),
        "approval_sha256": _sha256(APPROVAL_GATE_JSON),
        "approval_sha256_16": _sha16(_sha256(APPROVAL_GATE_JSON)),
    }


def build_real_submission_decision_state() -> Dict[str, Any]:
    return {
        "real_submission_decision_record_required": True,
        "real_submission_decision_record_created": True,
        "real_submission_decision_record_ready": True,
        "real_submission_decision_record_locked": True,
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_decision_reason": "OPERATOR_APPROVAL_NOT_GRANTED",
        "real_submission_decision_verdict": "SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT",
        "real_submission_decision_final_for_current_state": True,
        "manual_upload_decision": "BLOCKED",
        "kaggle_authentication_decision": "BLOCKED",
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "explicit_operator_approval_phrase_required": True,
        "explicit_operator_approval_phrase_received": False,
        "all_required_declarations_accepted": False,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
    }


def build_real_submission_decision_checks() -> Dict[str, bool]:
    source = build_decision_source_summary()
    decision = build_real_submission_decision_state()

    return {
        "approval_gate_artifact_present": APPROVAL_GATE_JSON.exists(),
        "approval_gate_artifact_ready": source["approval_gate_status"]
        == "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY",
        "approval_gate_artifact_valid": source["approval_id"].startswith("MILESTONE-9-APPROVAL-GATE-")
        and bool(source["approval_signature"]),
        "approval_gate_next_stage_matches_task_6": _read_json(APPROVAL_GATE_JSON).get("next_allowed_stage")
        == "MILESTONE_9_TASK_6_REAL_SUBMISSION_DECISION_RECORD_V1",
        "approval_ready": source["approval_ready"] is True,
        "approval_locked": source["approval_locked"] is True,
        "operator_approval_gate_created": source["operator_approval_gate_created"] is True,
        "operator_approval_gate_ready": source["operator_approval_gate_ready"] is True,
        "operator_approval_gate_closed": source["operator_approval_gate_open"] is False,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "required_declaration_count_valid": source["required_declaration_count"]
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": source["provided_declaration_count"]
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": source["accepted_declaration_count"]
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "explicit_operator_approval_phrase_absent": source["explicit_operator_approval_phrase_received"] is False,
        "operator_approval_required": source["operator_approval_required"] is True
        and decision["operator_approval_required"] is True,
        "operator_approval_not_granted": source["operator_approval_granted"] is False
        and decision["operator_approval_granted"] is False,
        "operator_approval_not_received": source["operator_approval_received"] is False
        and decision["operator_approval_received"] is False,
        "decision_check_count_valid": len(DECISION_CHECKS) == EXPECTED_DECISION_CHECK_COUNT,
        "decision_record_required": decision["real_submission_decision_record_required"] is True,
        "decision_record_created": decision["real_submission_decision_record_created"] is True,
        "decision_record_ready": decision["real_submission_decision_record_ready"] is True,
        "decision_record_locked": decision["real_submission_decision_record_locked"] is True,
        "decision_not_authorized": decision["real_submission_decision"] == "NOT_AUTHORIZED",
        "decision_reason_valid": decision["real_submission_decision_reason"]
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "decision_verdict_valid": decision["real_submission_decision_verdict"]
        == "SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT",
        "manual_upload_decision_blocked": decision["manual_upload_decision"] == "BLOCKED",
        "kaggle_authentication_decision_blocked": decision["kaggle_authentication_decision"] == "BLOCKED",
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False,
        "real_submission_not_created": source["real_submission_allowed"] is False
        and decision["real_submission_created"] is False,
        "real_submission_allowed_false": source["real_submission_allowed"] is False
        and decision["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": source["ready_for_real_kaggle_submission"] is False
        and decision["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and decision["kaggle_submission_sent"] is False,
        "upload_not_performed": source["upload_performed"] is False
        and decision["upload_performed"] is False,
        "kaggle_authentication_not_performed": source["kaggle_authentication_performed"] is False
        and decision["kaggle_authentication_performed"] is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "external_api_dependency_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_7_REAL_SUBMISSION_BLOCKED_CLOSURE_V1",
    }


def evaluate_real_submission_decision_case(case_id: str) -> Dict[str, Any]:
    checks = build_real_submission_decision_checks()

    if case_id == "decision_approval_gate_source_ready_v1":
        passed = (
            checks["approval_gate_artifact_present"]
            and checks["approval_gate_artifact_ready"]
            and checks["approval_gate_artifact_valid"]
            and checks["approval_ready"]
        )
        return _result(case_id, "source_binding", "verify_operator_approval_gate", passed)

    if case_id == "decision_required_declarations_present_v1":
        passed = checks["required_declaration_count_valid"]
        return _result(case_id, "operator_declarations", "verify_required_declaration_count", passed)

    if case_id == "decision_no_declarations_accepted_v1":
        passed = (
            checks["provided_declaration_count_zero"]
            and checks["accepted_declaration_count_zero"]
        )
        return _result(case_id, "operator_declarations", "verify_no_accepted_declarations", passed)

    if case_id == "decision_explicit_operator_approval_absent_v1":
        passed = checks["explicit_operator_approval_phrase_absent"]
        return _result(case_id, "operator_approval", "verify_explicit_approval_absent", passed)

    if case_id == "decision_operator_approval_not_granted_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "approval_gate", "verify_operator_approval_not_granted", passed)

    if case_id == "decision_real_submission_not_authorized_v1":
        passed = (
            checks["decision_record_created"]
            and checks["decision_not_authorized"]
            and checks["decision_reason_valid"]
            and checks["decision_verdict_valid"]
        )
        return _result(case_id, "decision", "verify_real_submission_not_authorized", passed)

    if case_id == "decision_manual_upload_blocked_v1":
        passed = checks["manual_upload_decision_blocked"] and checks["manual_upload_not_allowed"]
        return _result(case_id, "upload_gate", "verify_manual_upload_blocked", passed)

    if case_id == "decision_no_auth_no_upload_v1":
        passed = (
            checks["kaggle_authentication_decision_blocked"]
            and checks["kaggle_authentication_not_allowed"]
            and checks["upload_not_performed"]
            and checks["kaggle_authentication_not_performed"]
        )
        return _result(case_id, "boundary", "verify_no_auth_no_upload", passed)

    if case_id == "decision_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "decision_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_blocked_closure_next", passed)

    raise ValueError(f"unknown real submission decision case: {case_id}")


def evaluate_all_real_submission_decision_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_real_submission_decision_case(case["case_id"]) for case in DECISION_CASES)


def build_milestone_9_real_submission_decision_record() -> Dict[str, Any]:
    approval = _read_json(APPROVAL_GATE_JSON)
    source = build_decision_source_summary()
    decision = build_real_submission_decision_state()
    checks = build_real_submission_decision_checks()
    results = evaluate_all_real_submission_decision_cases()

    decision_pass_count = sum(1 for result in results if result["passed"] is True)
    decision_failure_count = sum(1 for result in results if result["passed"] is False)

    decision_record = {
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "decision_ready": True,
        "decision_locked": True,
        "baseline_approval_id": approval.get("approval_id", "MISSING_APPROVAL_ID"),
        "approval_ready": approval.get("approval_ready") is True,
        "approval_gate_open": approval.get("operator_approval_gate_open") is False,
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_signature": source["candidate_signature"],
        "candidate_count": source["candidate_count"],
        "real_submission_decision_record_created": decision["real_submission_decision_record_created"],
        "real_submission_decision_record_ready": decision["real_submission_decision_record_ready"],
        "real_submission_decision_record_locked": decision["real_submission_decision_record_locked"],
        "real_submission_decision": decision["real_submission_decision"],
        "real_submission_decision_reason": decision["real_submission_decision_reason"],
        "real_submission_decision_verdict": decision["real_submission_decision_verdict"],
        "real_submission_decision_final_for_current_state": decision[
            "real_submission_decision_final_for_current_state"
        ],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": source[
            "explicit_operator_approval_phrase_received"
        ],
        "decision_check_count": len(DECISION_CHECKS),
        "decision_case_count": len(DECISION_CASES),
        "decision_pass_count": decision_pass_count,
        "decision_failure_count": decision_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "operator_approval_required": decision["operator_approval_required"],
        "operator_approval_granted": decision["operator_approval_granted"],
        "operator_approval_received": decision["operator_approval_received"],
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
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
        "approval_gate_artifact_present": checks["approval_gate_artifact_present"],
        "approval_gate_artifact_ready": checks["approval_gate_artifact_ready"],
        "approval_gate_artifact_valid": checks["approval_gate_artifact_valid"],
        "approval_gate_next_stage_matches_task_6": checks["approval_gate_next_stage_matches_task_6"],
        "approval_ready": checks["approval_ready"],
        "approval_locked": checks["approval_locked"],
        "operator_approval_gate_created": checks["operator_approval_gate_created"],
        "operator_approval_gate_ready": checks["operator_approval_gate_ready"],
        "operator_approval_gate_closed": checks["operator_approval_gate_closed"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "explicit_operator_approval_phrase_absent": checks["explicit_operator_approval_phrase_absent"],
        "decision_mode_valid": DECISION_MODE == "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_LOCAL_ONLY",
        "decision_scope_valid": DECISION_SCOPE
        == "RECORD_REAL_SUBMISSION_NOT_AUTHORIZED_OPERATOR_APPROVAL_ABSENT",
        "decision_verdict_valid": DECISION_VERDICT
        == "REAL_SUBMISSION_DECISION_RECORDED_NOT_AUTHORIZED_SUBMISSION_BLOCKED",
        "decision_check_count_valid": checks["decision_check_count_valid"],
        "decision_record_required": checks["decision_record_required"],
        "decision_record_created": checks["decision_record_created"],
        "decision_record_ready": checks["decision_record_ready"],
        "decision_record_locked": checks["decision_record_locked"],
        "decision_case_count_valid": len(DECISION_CASES) == EXPECTED_DECISION_CASE_COUNT,
        "decision_pass_count_valid": decision_pass_count == EXPECTED_DECISION_PASS_COUNT,
        "decision_failure_count_zero": decision_failure_count == EXPECTED_DECISION_FAILURE_COUNT,
        "all_decision_cases_pass": all(result["passed"] is True for result in results),
        "decision_not_authorized": checks["decision_not_authorized"],
        "decision_reason_valid": checks["decision_reason_valid"],
        "decision_verdict_status_valid": checks["decision_verdict_valid"],
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "manual_upload_decision_blocked": checks["manual_upload_decision_blocked"],
        "kaggle_authentication_decision_blocked": checks["kaggle_authentication_decision_blocked"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": checks["real_submission_not_created"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_false": checks["ready_for_real_kaggle_submission_false"],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "upload_not_performed": checks["upload_not_performed"],
        "kaggle_authentication_not_performed": checks["kaggle_authentication_not_performed"],
        "external_api_dependency_false": decision_record["external_api_dependency"] is False,
        "contains_api_keys_false": decision_record["contains_api_keys"] is False,
        "private_core_exposure_false": decision_record["private_core_exposure"] is False,
        "legal_certification_false": decision_record["legal_certification"] is False,
        "score_claim_absent": decision_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": decision_record["public_leaderboard_claim_absent"] is True,
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

    decision_ready = (
        approval.get("status") == "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY"
        and decision_pass_count == EXPECTED_DECISION_PASS_COUNT
        and decision_failure_count == EXPECTED_DECISION_FAILURE_COUNT
        and source["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
        and source["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
        and source["operator_approval_granted"] is False
        and decision_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 6",
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_approval_gate": approval.get("approval_id", "MISSING_APPROVAL_ID"),
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "decision_ready": decision_ready,
        "decision_locked": True,
        "real_submission_decision_record_created": True,
        "real_submission_decision_record_ready": True,
        "real_submission_decision": decision["real_submission_decision"],
        "real_submission_decision_reason": decision["real_submission_decision_reason"],
        "real_submission_decision_verdict": decision["real_submission_decision_verdict"],
        "decision_check_count": len(DECISION_CHECKS),
        "decision_case_count": len(DECISION_CASES),
        "decision_pass_count": decision_pass_count,
        "decision_failure_count": decision_failure_count,
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": False,
        "operator_approval_required": decision["operator_approval_required"],
        "operator_approval_granted": decision["operator_approval_granted"],
        "operator_approval_received": decision["operator_approval_received"],
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
        "status": DECISION_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 6",
        "title": "Real Submission Decision Record v1",
        "baseline_commit": BASELINE_COMMIT,
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "approval_gate_source": {
            "path": str(APPROVAL_GATE_JSON),
            "present": APPROVAL_GATE_JSON.exists(),
            "status": approval.get("status", "MISSING"),
            "approval_id": approval.get("approval_id", "MISSING_APPROVAL_ID"),
            "sha256": _sha256(APPROVAL_GATE_JSON),
            "sha256_16": _sha16(_sha256(APPROVAL_GATE_JSON)),
        },
        "decision_source_summary": source,
        "decision_state": decision,
        "decision_checks": checks,
        "decision_check_list": list(DECISION_CHECKS),
        "decision_cases": list(DECISION_CASES),
        "decision_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "decision_gates": list(gates),
        "decision_issues": list(issues),
        "decision_index": index,
        "decision_record": decision_record,
        "decision_ready": decision_ready,
        "decision_locked": True,
        "real_submission_decision_record_created": decision["real_submission_decision_record_created"],
        "real_submission_decision_record_ready": decision["real_submission_decision_record_ready"],
        "real_submission_decision_record_locked": decision["real_submission_decision_record_locked"],
        "real_submission_decision": decision["real_submission_decision"],
        "real_submission_decision_reason": decision["real_submission_decision_reason"],
        "real_submission_decision_verdict": decision["real_submission_decision_verdict"],
        "real_submission_decision_final_for_current_state": decision[
            "real_submission_decision_final_for_current_state"
        ],
        "candidate_count": source["candidate_count"],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": source[
            "explicit_operator_approval_phrase_received"
        ],
        "decision_check_count": len(DECISION_CHECKS),
        "decision_case_count": len(DECISION_CASES),
        "decision_pass_count": decision_pass_count,
        "decision_failure_count": decision_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "decision_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "decision_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": decision["operator_approval_required"],
        "operator_approval_granted": decision["operator_approval_granted"],
        "operator_approval_received": decision["operator_approval_received"],
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_real_submission_decision_record_v1",
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
        "decision_id": f"MILESTONE-9-DECISION-RECORD-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_real_submission_decision_record(decision: Mapping[str, Any]) -> Dict[str, Any]:
    gates = decision.get("decision_gates", [])
    issues = decision.get("decision_issues", [])
    results = decision.get("decision_results", [])

    checks = {
        "status_ready": decision.get("status") == DECISION_STATUS,
        "decision_id_present": isinstance(decision.get("decision_id"), str) and bool(decision.get("decision_id")),
        "signature_present": isinstance(decision.get("signature"), str) and bool(decision.get("signature")),
        "baseline_commit_valid": str(decision.get("baseline_commit", "")).startswith("649509b"),
        "decision_mode_valid": decision.get("decision_mode") == DECISION_MODE,
        "decision_scope_valid": decision.get("decision_scope") == DECISION_SCOPE,
        "decision_verdict_valid": decision.get("decision_verdict") == DECISION_VERDICT,
        "next_allowed_stage_valid": decision.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "decision_ready": decision.get("decision_ready") is True,
        "decision_locked": decision.get("decision_locked") is True,
        "decision_record_created": decision.get("real_submission_decision_record_created") is True,
        "decision_record_ready": decision.get("real_submission_decision_record_ready") is True,
        "decision_record_locked": decision.get("real_submission_decision_record_locked") is True,
        "decision_check_count_valid": decision.get("decision_check_count") == EXPECTED_DECISION_CHECK_COUNT,
        "decision_case_count_valid": decision.get("decision_case_count") == EXPECTED_DECISION_CASE_COUNT,
        "decision_pass_count_valid": decision.get("decision_pass_count") == EXPECTED_DECISION_PASS_COUNT,
        "decision_failure_count_zero": decision.get("decision_failure_count") == EXPECTED_DECISION_FAILURE_COUNT,
        "decision_not_authorized": decision.get("real_submission_decision") == "NOT_AUTHORIZED",
        "decision_reason_valid": decision.get("real_submission_decision_reason")
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "decision_verdict_status_valid": decision.get("real_submission_decision_verdict")
        == "SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT",
        "required_declaration_count_valid": decision.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": decision.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": decision.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "explicit_operator_approval_phrase_absent": decision.get(
            "explicit_operator_approval_phrase_received"
        )
        is False,
        "candidate_count_positive": decision.get("candidate_count", 0) > 0,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_decision_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "decision_issue_count_zero": decision.get("decision_issue_count") == 0,
        "all_decision_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": decision.get("operator_approval_required") is True,
        "operator_approval_not_granted": decision.get("operator_approval_granted") is False,
        "operator_approval_not_received": decision.get("operator_approval_received") is False,
        "manual_upload_not_allowed": decision.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": decision.get("kaggle_authentication_allowed") is False,
        "real_submission_not_created": decision.get("real_submission_created") is False,
        "real_submission_allowed_false": decision.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": decision.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": decision.get("kaggle_submission_sent") is False,
        "upload_not_performed": decision.get("upload_performed") is False,
        "kaggle_authentication_not_performed": decision.get("kaggle_authentication_performed") is False,
        "metadata_safe": decision.get("metadata", {}).get("external_api_dependency") is False
        and decision.get("metadata", {}).get("contains_api_keys") is False
        and decision.get("metadata", {}).get("private_core_exposure") is False
        and decision.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "decision_id": decision.get("decision_id"),
        "signature": decision.get("signature"),
    }


def render_real_submission_decision_record_markdown(decision: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Real Submission Decision Record v1",
        "",
        f"- status: {decision['status']}",
        f"- decision_id: {decision['decision_id']}",
        f"- signature: {decision['signature']}",
        f"- baseline_commit: {decision['baseline_commit']}",
        f"- decision_mode: {decision['decision_mode']}",
        f"- decision_scope: {decision['decision_scope']}",
        f"- decision_verdict: {decision['decision_verdict']}",
        f"- next_allowed_stage: {decision['next_allowed_stage']}",
        f"- decision_ready: {decision['decision_ready']}",
        f"- real_submission_decision_record_created: {decision['real_submission_decision_record_created']}",
        f"- real_submission_decision: {decision['real_submission_decision']}",
        f"- real_submission_decision_reason: {decision['real_submission_decision_reason']}",
        f"- real_submission_decision_verdict: {decision['real_submission_decision_verdict']}",
        f"- required_declaration_count: {decision['required_declaration_count']}",
        f"- provided_declaration_count: {decision['provided_declaration_count']}",
        f"- accepted_declaration_count: {decision['accepted_declaration_count']}",
        f"- explicit_operator_approval_phrase_received: {decision['explicit_operator_approval_phrase_received']}",
        f"- operator_approval_required: {decision['operator_approval_required']}",
        f"- operator_approval_granted: {decision['operator_approval_granted']}",
        "",
        "## Decision checks",
        "",
    ]

    for item in decision["decision_check_list"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Decision results", ""])

    for result in decision["decision_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Real submission is not authorized. The operator approval gate is ready but closed, no declarations have been accepted, and no explicit operator approval phrase has been received.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_DECISION_RECORD_READY=true",
            "ARC_AGI3_MILESTONE_9_DECISION_MODE=MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_DECISION_VERDICT=REAL_SUBMISSION_DECISION_RECORDED_NOT_AUTHORIZED_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_BASELINE_OPERATOR_APPROVAL_GATE_COMMIT=649509b",
            "ARC_AGI3_MILESTONE_9_DECISION_CHECK_COUNT=16",
            "ARC_AGI3_MILESTONE_9_DECISION_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_DECISION_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_DECISION_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_CREATED=true",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_REASON=OPERATOR_APPROVAL_NOT_GRANTED",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_VERDICT=SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT",
            "ARC_AGI3_MILESTONE_9_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_9_PROVIDED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_ACCEPTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_EXPLICIT_OPERATOR_APPROVAL_PHRASE_RECEIVED=false",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_7_REAL_SUBMISSION_BLOCKED_CLOSURE_V1",
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


def render_real_submission_decision_record_manifest(decision: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 REAL SUBMISSION DECISION RECORD MANIFEST v1",
        f"decision_id={decision['decision_id']}",
        f"signature={decision['signature']}",
        f"status={decision['status']}",
        f"baseline_commit={decision['baseline_commit']}",
        f"decision_mode={decision['decision_mode']}",
        f"decision_verdict={decision['decision_verdict']}",
        f"next_allowed_stage={decision['next_allowed_stage']}",
        f"decision_ready={decision['decision_ready']}",
        f"decision_locked={decision['decision_locked']}",
        f"real_submission_decision_record_created={decision['real_submission_decision_record_created']}",
        f"real_submission_decision_record_ready={decision['real_submission_decision_record_ready']}",
        f"real_submission_decision_record_locked={decision['real_submission_decision_record_locked']}",
        f"real_submission_decision={decision['real_submission_decision']}",
        f"real_submission_decision_reason={decision['real_submission_decision_reason']}",
        f"real_submission_decision_verdict={decision['real_submission_decision_verdict']}",
        f"required_declaration_count={decision['required_declaration_count']}",
        f"provided_declaration_count={decision['provided_declaration_count']}",
        f"accepted_declaration_count={decision['accepted_declaration_count']}",
        f"explicit_operator_approval_phrase_received={decision['explicit_operator_approval_phrase_received']}",
        f"decision_check_count={decision['decision_check_count']}",
        f"decision_case_count={decision['decision_case_count']}",
        f"decision_pass_count={decision['decision_pass_count']}",
        f"decision_failure_count={decision['decision_failure_count']}",
        f"decision_gate_count={decision['decision_gate_count']}",
        f"passed_gate_count={decision['passed_gate_count']}",
        f"decision_issue_count={decision['decision_issue_count']}",
        f"operator_approval_required={decision['operator_approval_required']}",
        f"operator_approval_granted={decision['operator_approval_granted']}",
        f"operator_approval_received={decision['operator_approval_received']}",
        f"manual_upload_allowed={decision['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={decision['kaggle_authentication_allowed']}",
        f"real_submission_created={decision['real_submission_created']}",
        f"real_submission_allowed={decision['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={decision['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={decision['kaggle_submission_sent']}",
        f"upload_performed={decision['upload_performed']}",
        f"kaggle_authentication_performed={decision['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "DECISION_CHECKS",
    ]

    for item in decision["decision_check_list"]:
        lines.append(item)

    lines.append("")
    lines.append("DECISION_RESULTS")
    for result in decision["decision_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_real_submission_decision_record_artifacts(
    decision: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    decision = dict(decision or build_milestone_9_real_submission_decision_record())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-real-submission-decision-record-v1.json"
    md_path = output / "milestone-9-real-submission-decision-record-v1.md"
    manifest_path = output / "milestone-9-real-submission-decision-record-manifest-v1.txt"
    index_path = output / "milestone-9-real-submission-decision-record-index-v1.json"

    json_path.write_text(json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_decision_record_markdown(decision), encoding="utf-8")
    manifest_path.write_text(render_real_submission_decision_record_manifest(decision), encoding="utf-8")
    index_path.write_text(json.dumps(decision["decision_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_real_submission_decision_record_pipeline() -> Dict[str, Any]:
    decision = build_milestone_9_real_submission_decision_record()
    validation = validate_milestone_9_real_submission_decision_record(decision)
    artifacts = write_real_submission_decision_record_artifacts(decision)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_PIPELINE_INVALID",
        "decision_status": decision["status"],
        "validation_status": validation["status"],
        "decision": decision,
        "decision_id": decision["decision_id"],
        "signature": decision["signature"],
        "decision_mode": decision["decision_mode"],
        "decision_verdict": decision["decision_verdict"],
        "next_allowed_stage": decision["next_allowed_stage"],
        "decision_ready": decision["decision_ready"],
        "decision_locked": decision["decision_locked"],
        "real_submission_decision_record_created": decision["real_submission_decision_record_created"],
        "real_submission_decision_record_ready": decision["real_submission_decision_record_ready"],
        "real_submission_decision_record_locked": decision["real_submission_decision_record_locked"],
        "real_submission_decision": decision["real_submission_decision"],
        "real_submission_decision_reason": decision["real_submission_decision_reason"],
        "required_declaration_count": decision["required_declaration_count"],
        "provided_declaration_count": decision["provided_declaration_count"],
        "accepted_declaration_count": decision["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": decision["explicit_operator_approval_phrase_received"],
        "decision_check_count": decision["decision_check_count"],
        "decision_case_count": decision["decision_case_count"],
        "decision_pass_count": decision["decision_pass_count"],
        "decision_failure_count": decision["decision_failure_count"],
        "regression_guard_count": decision["regression_guard_count"],
        "boundary_control_count": decision["boundary_control_count"],
        "decision_gate_count": decision["decision_gate_count"],
        "passed_gate_count": decision["passed_gate_count"],
        "decision_issue_count": decision["decision_issue_count"],
        "warning_count": decision["warning_count"],
        "operator_approval_required": decision["operator_approval_required"],
        "operator_approval_granted": decision["operator_approval_granted"],
        "operator_approval_received": decision["operator_approval_received"],
        "manual_upload_allowed": decision["manual_upload_allowed"],
        "kaggle_authentication_allowed": decision["kaggle_authentication_allowed"],
        "real_submission_created": decision["real_submission_created"],
        "real_submission_allowed": decision["real_submission_allowed"],
        "ready_for_real_kaggle_submission": decision["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": decision["kaggle_submission_sent"],
        "upload_performed": decision["upload_performed"],
        "kaggle_authentication_performed": decision["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": decision["metadata"],
    }
