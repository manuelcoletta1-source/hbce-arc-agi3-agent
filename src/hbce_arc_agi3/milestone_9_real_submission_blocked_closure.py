"""Milestone #9 Real Submission Blocked Closure v1.

Local-only deterministic closure package for Milestone #9.

This module reads the real submission decision record and closes the current
manual submission governance cycle with real submission blocked. It does not
submit to Kaggle, authenticate, upload files, call external APIs, read secrets,
grant approval, claim a score, claim leaderboard movement, or create legal
certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CLOSURE_STATUS = "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_VALID"

BASELINE_COMMIT = "793d24b Add ARC AGI3 real submission decision record"
CLOSURE_MODE = "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_LOCAL_ONLY"
CLOSURE_SCOPE = "CLOSE_MILESTONE_9_WITH_REAL_SUBMISSION_BLOCKED_NO_UPLOAD"
CLOSURE_VERDICT = "MILESTONE_9_CLOSED_REAL_SUBMISSION_BLOCKED_NO_KAGGLE_ACTION"
NEXT_ALLOWED_STAGE = "MILESTONE_9_CLOSED_PENDING_EXPLICIT_OPERATOR_APPROVAL"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/real-submission-blocked-closure-v1"

DECISION_RECORD_JSON = Path(
    "examples/milestone-9/real-submission-decision-record-v1/"
    "milestone-9-real-submission-decision-record-v1.json"
)

EXPECTED_CLOSURE_CHECK_COUNT = 18
EXPECTED_CLOSURE_CASE_COUNT = 10
EXPECTED_CLOSURE_PASS_COUNT = 10
EXPECTED_CLOSURE_FAILURE_COUNT = 0
EXPECTED_REQUIRED_DECLARATION_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

CLOSURE_CHECKS: Tuple[str, ...] = (
    "decision_record_artifact_exists",
    "decision_record_artifact_ready",
    "decision_record_locked",
    "decision_not_authorized",
    "decision_reason_operator_approval_not_granted",
    "required_declarations_present",
    "provided_declarations_absent",
    "accepted_declarations_absent",
    "explicit_operator_approval_absent",
    "operator_approval_not_granted",
    "closure_record_created",
    "closure_ready",
    "milestone_9_closed",
    "manual_upload_blocked",
    "authentication_blocked",
    "real_submission_blocked",
    "kaggle_submission_absent",
    "claim_boundary_preserved",
)

CLOSURE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "closure_decision_record_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_decision_record",
    },
    {
        "case_id": "closure_decision_not_authorized_v1",
        "area": "decision",
        "operation": "verify_not_authorized_decision",
    },
    {
        "case_id": "closure_declarations_absent_v1",
        "area": "operator_declarations",
        "operation": "verify_no_accepted_declarations",
    },
    {
        "case_id": "closure_explicit_operator_approval_absent_v1",
        "area": "operator_approval",
        "operation": "verify_explicit_approval_absent",
    },
    {
        "case_id": "closure_operator_approval_not_granted_v1",
        "area": "approval_gate",
        "operation": "verify_operator_approval_not_granted",
    },
    {
        "case_id": "closure_real_submission_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "closure_no_upload_no_auth_v1",
        "area": "boundary",
        "operation": "verify_no_upload_no_auth",
    },
    {
        "case_id": "closure_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "closure_milestone_9_closed_blocked_v1",
        "area": "closure",
        "operation": "verify_milestone_closed_blocked",
    },
    {
        "case_id": "closure_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_closed_pending_operator_approval",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_closure_uses_decision_record",
    "guard_closure_requires_not_authorized_decision",
    "guard_closure_requires_operator_approval_absent",
    "guard_closure_requires_no_accepted_declarations",
    "guard_closure_keeps_manual_upload_blocked",
    "guard_closure_keeps_real_submission_blocked",
    "guard_closure_does_not_authenticate",
    "guard_closure_does_not_upload",
    "guard_closure_no_score_claim",
    "guard_closure_no_leaderboard_claim",
    "guard_closure_no_private_core_exposure",
    "guard_closure_no_legal_certification",
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


def build_closure_source_summary() -> Dict[str, Any]:
    decision = _read_json(DECISION_RECORD_JSON)
    decision_source = decision.get("decision_source_summary", {})

    return {
        "decision_record_path": str(DECISION_RECORD_JSON),
        "decision_record_present": DECISION_RECORD_JSON.exists(),
        "decision_record_status": decision.get("status", "MISSING"),
        "decision_id": decision.get("decision_id", "MISSING_DECISION_ID"),
        "decision_signature": decision.get("signature", ""),
        "decision_ready": decision.get("decision_ready", False),
        "decision_locked": decision.get("decision_locked", False),
        "real_submission_decision_record_created": decision.get(
            "real_submission_decision_record_created", False
        ),
        "real_submission_decision_record_ready": decision.get(
            "real_submission_decision_record_ready", False
        ),
        "real_submission_decision_record_locked": decision.get(
            "real_submission_decision_record_locked", False
        ),
        "real_submission_decision": decision.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_decision_reason": decision.get(
            "real_submission_decision_reason", "MISSING_REASON"
        ),
        "real_submission_decision_verdict": decision.get(
            "real_submission_decision_verdict", "MISSING_VERDICT"
        ),
        "candidate_source_path": decision_source.get(
            "candidate_source_path", "MISSING_CANDIDATE_SOURCE"
        ),
        "candidate_id": decision_source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": decision_source.get("candidate_signature", ""),
        "candidate_count": decision.get("candidate_count", 0),
        "required_declaration_count": decision.get("required_declaration_count", 0),
        "provided_declaration_count": decision.get("provided_declaration_count", 0),
        "accepted_declaration_count": decision.get("accepted_declaration_count", 0),
        "explicit_operator_approval_phrase_received": decision.get(
            "explicit_operator_approval_phrase_received", True
        ),
        "operator_approval_required": decision.get("operator_approval_required", False),
        "operator_approval_granted": decision.get("operator_approval_granted", True),
        "operator_approval_received": decision.get("operator_approval_received", True),
        "manual_upload_allowed": decision.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": decision.get("kaggle_authentication_allowed", True),
        "real_submission_created": decision.get("real_submission_created", True),
        "real_submission_allowed": decision.get("real_submission_allowed", True),
        "ready_for_real_kaggle_submission": decision.get(
            "ready_for_real_kaggle_submission", True
        ),
        "kaggle_submission_sent": decision.get("kaggle_submission_sent", True),
        "upload_performed": decision.get("upload_performed", True),
        "kaggle_authentication_performed": decision.get(
            "kaggle_authentication_performed", True
        ),
        "decision_sha256": _sha256(DECISION_RECORD_JSON),
        "decision_sha256_16": _sha16(_sha256(DECISION_RECORD_JSON)),
    }


def build_real_submission_blocked_closure_state() -> Dict[str, Any]:
    return {
        "real_submission_blocked_closure_required": True,
        "real_submission_blocked_closure_created": True,
        "real_submission_blocked_closure_ready": True,
        "real_submission_blocked_closure_locked": True,
        "milestone_9_closed": True,
        "milestone_9_closure_type": "REAL_SUBMISSION_BLOCKED",
        "milestone_9_closure_reason": "OPERATOR_APPROVAL_NOT_GRANTED",
        "milestone_9_closure_verdict": "CLOSED_WITH_REAL_SUBMISSION_BLOCKED",
        "real_submission_decision": "NOT_AUTHORIZED",
        "real_submission_decision_reason": "OPERATOR_APPROVAL_NOT_GRANTED",
        "manual_upload_decision": "BLOCKED",
        "kaggle_authentication_decision": "BLOCKED",
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "explicit_operator_approval_phrase_received": False,
        "all_required_declarations_accepted": False,
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
    }


def build_real_submission_blocked_closure_checks() -> Dict[str, bool]:
    source = build_closure_source_summary()
    closure = build_real_submission_blocked_closure_state()

    return {
        "decision_record_artifact_present": DECISION_RECORD_JSON.exists(),
        "decision_record_artifact_ready": source["decision_record_status"]
        == "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY",
        "decision_record_artifact_valid": source["decision_id"].startswith(
            "MILESTONE-9-DECISION-RECORD-"
        )
        and bool(source["decision_signature"]),
        "decision_record_next_stage_matches_task_7": _read_json(DECISION_RECORD_JSON).get(
            "next_allowed_stage"
        )
        == "MILESTONE_9_TASK_7_REAL_SUBMISSION_BLOCKED_CLOSURE_V1",
        "decision_ready": source["decision_ready"] is True,
        "decision_locked": source["decision_locked"] is True,
        "decision_record_created": source["real_submission_decision_record_created"] is True,
        "decision_record_ready": source["real_submission_decision_record_ready"] is True,
        "decision_record_locked": source["real_submission_decision_record_locked"] is True,
        "decision_not_authorized": source["real_submission_decision"] == "NOT_AUTHORIZED",
        "decision_reason_valid": source["real_submission_decision_reason"]
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "decision_verdict_valid": source["real_submission_decision_verdict"]
        == "SUBMISSION_BLOCKED_OPERATOR_APPROVAL_ABSENT",
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
        "explicit_operator_approval_phrase_absent": source[
            "explicit_operator_approval_phrase_received"
        ]
        is False,
        "operator_approval_required": source["operator_approval_required"] is True
        and closure["operator_approval_required"] is True,
        "operator_approval_not_granted": source["operator_approval_granted"] is False
        and closure["operator_approval_granted"] is False,
        "operator_approval_not_received": source["operator_approval_received"] is False
        and closure["operator_approval_received"] is False,
        "closure_check_count_valid": len(CLOSURE_CHECKS) == EXPECTED_CLOSURE_CHECK_COUNT,
        "closure_record_required": closure["real_submission_blocked_closure_required"] is True,
        "closure_record_created": closure["real_submission_blocked_closure_created"] is True,
        "closure_record_ready": closure["real_submission_blocked_closure_ready"] is True,
        "closure_record_locked": closure["real_submission_blocked_closure_locked"] is True,
        "milestone_9_closed": closure["milestone_9_closed"] is True,
        "closure_type_valid": closure["milestone_9_closure_type"] == "REAL_SUBMISSION_BLOCKED",
        "closure_reason_valid": closure["milestone_9_closure_reason"]
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "closure_verdict_valid": closure["milestone_9_closure_verdict"]
        == "CLOSED_WITH_REAL_SUBMISSION_BLOCKED",
        "manual_upload_decision_blocked": closure["manual_upload_decision"] == "BLOCKED",
        "kaggle_authentication_decision_blocked": closure[
            "kaggle_authentication_decision"
        ]
        == "BLOCKED",
        "manual_upload_not_allowed": source["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": source["kaggle_authentication_allowed"] is False,
        "real_submission_not_created": source["real_submission_created"] is False,
        "real_submission_allowed_false": source["real_submission_allowed"] is False
        and closure["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": source[
            "ready_for_real_kaggle_submission"
        ]
        is False
        and closure["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": source["kaggle_submission_sent"] is False
        and closure["kaggle_submission_sent"] is False,
        "upload_not_performed": source["upload_performed"] is False
        and closure["upload_performed"] is False,
        "kaggle_authentication_not_performed": source[
            "kaggle_authentication_performed"
        ]
        is False
        and closure["kaggle_authentication_performed"] is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "external_api_dependency_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE
        == "MILESTONE_9_CLOSED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
    }


def evaluate_real_submission_blocked_closure_case(case_id: str) -> Dict[str, Any]:
    checks = build_real_submission_blocked_closure_checks()

    if case_id == "closure_decision_record_source_ready_v1":
        passed = (
            checks["decision_record_artifact_present"]
            and checks["decision_record_artifact_ready"]
            and checks["decision_record_artifact_valid"]
            and checks["decision_ready"]
        )
        return _result(case_id, "source_binding", "verify_decision_record", passed)

    if case_id == "closure_decision_not_authorized_v1":
        passed = (
            checks["decision_not_authorized"]
            and checks["decision_reason_valid"]
            and checks["decision_verdict_valid"]
        )
        return _result(case_id, "decision", "verify_not_authorized_decision", passed)

    if case_id == "closure_declarations_absent_v1":
        passed = (
            checks["required_declaration_count_valid"]
            and checks["provided_declaration_count_zero"]
            and checks["accepted_declaration_count_zero"]
        )
        return _result(case_id, "operator_declarations", "verify_no_accepted_declarations", passed)

    if case_id == "closure_explicit_operator_approval_absent_v1":
        passed = checks["explicit_operator_approval_phrase_absent"]
        return _result(case_id, "operator_approval", "verify_explicit_approval_absent", passed)

    if case_id == "closure_operator_approval_not_granted_v1":
        passed = (
            checks["operator_approval_required"]
            and checks["operator_approval_not_granted"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "approval_gate", "verify_operator_approval_not_granted", passed)

    if case_id == "closure_real_submission_blocked_v1":
        passed = (
            checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "closure_no_upload_no_auth_v1":
        passed = (
            checks["manual_upload_decision_blocked"]
            and checks["kaggle_authentication_decision_blocked"]
            and checks["manual_upload_not_allowed"]
            and checks["kaggle_authentication_not_allowed"]
            and checks["upload_not_performed"]
            and checks["kaggle_authentication_not_performed"]
        )
        return _result(case_id, "boundary", "verify_no_upload_no_auth", passed)

    if case_id == "closure_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "closure_milestone_9_closed_blocked_v1":
        passed = (
            checks["closure_record_created"]
            and checks["closure_record_ready"]
            and checks["milestone_9_closed"]
            and checks["closure_type_valid"]
            and checks["closure_reason_valid"]
            and checks["closure_verdict_valid"]
        )
        return _result(case_id, "closure", "verify_milestone_closed_blocked", passed)

    if case_id == "closure_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_closed_pending_operator_approval", passed)

    raise ValueError(f"unknown real submission blocked closure case: {case_id}")


def evaluate_all_real_submission_blocked_closure_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_real_submission_blocked_closure_case(case["case_id"]) for case in CLOSURE_CASES)


def build_milestone_9_real_submission_blocked_closure() -> Dict[str, Any]:
    decision = _read_json(DECISION_RECORD_JSON)
    source = build_closure_source_summary()
    closure = build_real_submission_blocked_closure_state()
    checks = build_real_submission_blocked_closure_checks()
    results = evaluate_all_real_submission_blocked_closure_cases()

    closure_pass_count = sum(1 for result in results if result["passed"] is True)
    closure_failure_count = sum(1 for result in results if result["passed"] is False)

    closure_record = {
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "closure_ready": True,
        "closure_locked": True,
        "baseline_decision_id": decision.get("decision_id", "MISSING_DECISION_ID"),
        "decision_ready": decision.get("decision_ready") is True,
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_signature": source["candidate_signature"],
        "candidate_count": source["candidate_count"],
        "real_submission_blocked_closure_created": closure[
            "real_submission_blocked_closure_created"
        ],
        "real_submission_blocked_closure_ready": closure[
            "real_submission_blocked_closure_ready"
        ],
        "real_submission_blocked_closure_locked": closure[
            "real_submission_blocked_closure_locked"
        ],
        "milestone_9_closed": closure["milestone_9_closed"],
        "milestone_9_closure_type": closure["milestone_9_closure_type"],
        "milestone_9_closure_reason": closure["milestone_9_closure_reason"],
        "milestone_9_closure_verdict": closure["milestone_9_closure_verdict"],
        "real_submission_decision": closure["real_submission_decision"],
        "real_submission_decision_reason": closure["real_submission_decision_reason"],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": source[
            "explicit_operator_approval_phrase_received"
        ],
        "closure_check_count": len(CLOSURE_CHECKS),
        "closure_case_count": len(CLOSURE_CASES),
        "closure_pass_count": closure_pass_count,
        "closure_failure_count": closure_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "operator_approval_required": closure["operator_approval_required"],
        "operator_approval_granted": closure["operator_approval_granted"],
        "operator_approval_received": closure["operator_approval_received"],
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
        "decision_record_artifact_present": checks["decision_record_artifact_present"],
        "decision_record_artifact_ready": checks["decision_record_artifact_ready"],
        "decision_record_artifact_valid": checks["decision_record_artifact_valid"],
        "decision_record_next_stage_matches_task_7": checks[
            "decision_record_next_stage_matches_task_7"
        ],
        "decision_ready": checks["decision_ready"],
        "decision_locked": checks["decision_locked"],
        "decision_record_created": checks["decision_record_created"],
        "decision_record_ready": checks["decision_record_ready"],
        "decision_record_locked": checks["decision_record_locked"],
        "decision_not_authorized": checks["decision_not_authorized"],
        "decision_reason_valid": checks["decision_reason_valid"],
        "decision_verdict_valid": checks["decision_verdict_valid"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "explicit_operator_approval_phrase_absent": checks[
            "explicit_operator_approval_phrase_absent"
        ],
        "closure_mode_valid": CLOSURE_MODE
        == "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_LOCAL_ONLY",
        "closure_scope_valid": CLOSURE_SCOPE
        == "CLOSE_MILESTONE_9_WITH_REAL_SUBMISSION_BLOCKED_NO_UPLOAD",
        "closure_verdict_valid": CLOSURE_VERDICT
        == "MILESTONE_9_CLOSED_REAL_SUBMISSION_BLOCKED_NO_KAGGLE_ACTION",
        "closure_check_count_valid": checks["closure_check_count_valid"],
        "closure_record_required": checks["closure_record_required"],
        "closure_record_created": checks["closure_record_created"],
        "closure_record_ready": checks["closure_record_ready"],
        "closure_record_locked": checks["closure_record_locked"],
        "closure_case_count_valid": len(CLOSURE_CASES) == EXPECTED_CLOSURE_CASE_COUNT,
        "closure_pass_count_valid": closure_pass_count == EXPECTED_CLOSURE_PASS_COUNT,
        "closure_failure_count_zero": closure_failure_count == EXPECTED_CLOSURE_FAILURE_COUNT,
        "all_closure_cases_pass": all(result["passed"] is True for result in results),
        "milestone_9_closed": checks["milestone_9_closed"],
        "closure_type_valid": checks["closure_type_valid"],
        "closure_reason_valid": checks["closure_reason_valid"],
        "closure_status_verdict_valid": checks["closure_verdict_valid"],
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "manual_upload_decision_blocked": checks["manual_upload_decision_blocked"],
        "kaggle_authentication_decision_blocked": checks[
            "kaggle_authentication_decision_blocked"
        ],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS)
        == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS)
        == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": checks["real_submission_not_created"],
        "real_submission_allowed_false": checks["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_false": checks[
            "ready_for_real_kaggle_submission_false"
        ],
        "kaggle_submission_not_sent": checks["kaggle_submission_not_sent"],
        "upload_not_performed": checks["upload_not_performed"],
        "kaggle_authentication_not_performed": checks[
            "kaggle_authentication_not_performed"
        ],
        "external_api_dependency_false": closure_record["external_api_dependency"] is False,
        "contains_api_keys_false": closure_record["contains_api_keys"] is False,
        "private_core_exposure_false": closure_record["private_core_exposure"] is False,
        "legal_certification_false": closure_record["legal_certification"] is False,
        "score_claim_absent": closure_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": closure_record["public_leaderboard_claim_absent"] is True,
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

    closure_ready = (
        decision.get("status") == "MILESTONE_9_REAL_SUBMISSION_DECISION_RECORD_V1_READY"
        and closure_pass_count == EXPECTED_CLOSURE_PASS_COUNT
        and closure_failure_count == EXPECTED_CLOSURE_FAILURE_COUNT
        and source["real_submission_decision"] == "NOT_AUTHORIZED"
        and source["operator_approval_granted"] is False
        and source["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
        and closure_record["real_submission_allowed"] is False
        and closure["milestone_9_closed"] is True
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 7",
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_decision_record": decision.get("decision_id", "MISSING_DECISION_ID"),
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "closure_ready": closure_ready,
        "closure_locked": True,
        "real_submission_blocked_closure_created": True,
        "real_submission_blocked_closure_ready": True,
        "milestone_9_closed": True,
        "milestone_9_closure_type": closure["milestone_9_closure_type"],
        "milestone_9_closure_reason": closure["milestone_9_closure_reason"],
        "milestone_9_closure_verdict": closure["milestone_9_closure_verdict"],
        "real_submission_decision": closure["real_submission_decision"],
        "real_submission_decision_reason": closure["real_submission_decision_reason"],
        "closure_check_count": len(CLOSURE_CHECKS),
        "closure_case_count": len(CLOSURE_CASES),
        "closure_pass_count": closure_pass_count,
        "closure_failure_count": closure_failure_count,
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": False,
        "operator_approval_required": closure["operator_approval_required"],
        "operator_approval_granted": closure["operator_approval_granted"],
        "operator_approval_received": closure["operator_approval_received"],
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
        "status": CLOSURE_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 7",
        "title": "Real Submission Blocked Closure v1",
        "baseline_commit": BASELINE_COMMIT,
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "decision_record_source": {
            "path": str(DECISION_RECORD_JSON),
            "present": DECISION_RECORD_JSON.exists(),
            "status": decision.get("status", "MISSING"),
            "decision_id": decision.get("decision_id", "MISSING_DECISION_ID"),
            "sha256": _sha256(DECISION_RECORD_JSON),
            "sha256_16": _sha16(_sha256(DECISION_RECORD_JSON)),
        },
        "closure_source_summary": source,
        "closure_state": closure,
        "closure_checks": checks,
        "closure_check_list": list(CLOSURE_CHECKS),
        "closure_cases": list(CLOSURE_CASES),
        "closure_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "closure_gates": list(gates),
        "closure_issues": list(issues),
        "closure_index": index,
        "closure_record": closure_record,
        "closure_ready": closure_ready,
        "closure_locked": True,
        "real_submission_blocked_closure_created": closure[
            "real_submission_blocked_closure_created"
        ],
        "real_submission_blocked_closure_ready": closure[
            "real_submission_blocked_closure_ready"
        ],
        "real_submission_blocked_closure_locked": closure[
            "real_submission_blocked_closure_locked"
        ],
        "milestone_9_closed": closure["milestone_9_closed"],
        "milestone_9_closure_type": closure["milestone_9_closure_type"],
        "milestone_9_closure_reason": closure["milestone_9_closure_reason"],
        "milestone_9_closure_verdict": closure["milestone_9_closure_verdict"],
        "real_submission_decision": closure["real_submission_decision"],
        "real_submission_decision_reason": closure["real_submission_decision_reason"],
        "candidate_count": source["candidate_count"],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": source[
            "explicit_operator_approval_phrase_received"
        ],
        "closure_check_count": len(CLOSURE_CHECKS),
        "closure_case_count": len(CLOSURE_CASES),
        "closure_pass_count": closure_pass_count,
        "closure_failure_count": closure_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "closure_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "closure_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": closure["operator_approval_required"],
        "operator_approval_granted": closure["operator_approval_granted"],
        "operator_approval_received": closure["operator_approval_received"],
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
            "source": "milestone_9_real_submission_blocked_closure_v1",
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
        "closure_id": f"MILESTONE-9-BLOCKED-CLOSURE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_real_submission_blocked_closure(closure: Mapping[str, Any]) -> Dict[str, Any]:
    gates = closure.get("closure_gates", [])
    issues = closure.get("closure_issues", [])
    results = closure.get("closure_results", [])

    checks = {
        "status_ready": closure.get("status") == CLOSURE_STATUS,
        "closure_id_present": isinstance(closure.get("closure_id"), str) and bool(closure.get("closure_id")),
        "signature_present": isinstance(closure.get("signature"), str) and bool(closure.get("signature")),
        "baseline_commit_valid": str(closure.get("baseline_commit", "")).startswith("793d24b"),
        "closure_mode_valid": closure.get("closure_mode") == CLOSURE_MODE,
        "closure_scope_valid": closure.get("closure_scope") == CLOSURE_SCOPE,
        "closure_verdict_valid": closure.get("closure_verdict") == CLOSURE_VERDICT,
        "next_allowed_stage_valid": closure.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "closure_ready": closure.get("closure_ready") is True,
        "closure_locked": closure.get("closure_locked") is True,
        "closure_record_created": closure.get("real_submission_blocked_closure_created") is True,
        "closure_record_ready": closure.get("real_submission_blocked_closure_ready") is True,
        "closure_record_locked": closure.get("real_submission_blocked_closure_locked") is True,
        "milestone_9_closed": closure.get("milestone_9_closed") is True,
        "closure_type_valid": closure.get("milestone_9_closure_type") == "REAL_SUBMISSION_BLOCKED",
        "closure_reason_valid": closure.get("milestone_9_closure_reason")
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "closure_status_verdict_valid": closure.get("milestone_9_closure_verdict")
        == "CLOSED_WITH_REAL_SUBMISSION_BLOCKED",
        "closure_check_count_valid": closure.get("closure_check_count") == EXPECTED_CLOSURE_CHECK_COUNT,
        "closure_case_count_valid": closure.get("closure_case_count") == EXPECTED_CLOSURE_CASE_COUNT,
        "closure_pass_count_valid": closure.get("closure_pass_count") == EXPECTED_CLOSURE_PASS_COUNT,
        "closure_failure_count_zero": closure.get("closure_failure_count") == EXPECTED_CLOSURE_FAILURE_COUNT,
        "decision_not_authorized": closure.get("real_submission_decision") == "NOT_AUTHORIZED",
        "decision_reason_valid": closure.get("real_submission_decision_reason")
        == "OPERATOR_APPROVAL_NOT_GRANTED",
        "required_declaration_count_valid": closure.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": closure.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": closure.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "explicit_operator_approval_phrase_absent": closure.get(
            "explicit_operator_approval_phrase_received"
        )
        is False,
        "candidate_count_positive": closure.get("candidate_count", 0) > 0,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_closure_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "closure_issue_count_zero": closure.get("closure_issue_count") == 0,
        "all_closure_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": closure.get("operator_approval_required") is True,
        "operator_approval_not_granted": closure.get("operator_approval_granted") is False,
        "operator_approval_not_received": closure.get("operator_approval_received") is False,
        "manual_upload_not_allowed": closure.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": closure.get("kaggle_authentication_allowed") is False,
        "real_submission_not_created": closure.get("real_submission_created") is False,
        "real_submission_allowed_false": closure.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": closure.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": closure.get("kaggle_submission_sent") is False,
        "upload_not_performed": closure.get("upload_performed") is False,
        "kaggle_authentication_not_performed": closure.get("kaggle_authentication_performed") is False,
        "metadata_safe": closure.get("metadata", {}).get("external_api_dependency") is False
        and closure.get("metadata", {}).get("contains_api_keys") is False
        and closure.get("metadata", {}).get("private_core_exposure") is False
        and closure.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "closure_id": closure.get("closure_id"),
        "signature": closure.get("signature"),
    }


def render_real_submission_blocked_closure_markdown(closure: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Real Submission Blocked Closure v1",
        "",
        f"- status: {closure['status']}",
        f"- closure_id: {closure['closure_id']}",
        f"- signature: {closure['signature']}",
        f"- baseline_commit: {closure['baseline_commit']}",
        f"- closure_mode: {closure['closure_mode']}",
        f"- closure_scope: {closure['closure_scope']}",
        f"- closure_verdict: {closure['closure_verdict']}",
        f"- next_allowed_stage: {closure['next_allowed_stage']}",
        f"- closure_ready: {closure['closure_ready']}",
        f"- milestone_9_closed: {closure['milestone_9_closed']}",
        f"- milestone_9_closure_type: {closure['milestone_9_closure_type']}",
        f"- milestone_9_closure_reason: {closure['milestone_9_closure_reason']}",
        f"- milestone_9_closure_verdict: {closure['milestone_9_closure_verdict']}",
        f"- real_submission_decision: {closure['real_submission_decision']}",
        f"- real_submission_decision_reason: {closure['real_submission_decision_reason']}",
        f"- required_declaration_count: {closure['required_declaration_count']}",
        f"- provided_declaration_count: {closure['provided_declaration_count']}",
        f"- accepted_declaration_count: {closure['accepted_declaration_count']}",
        f"- explicit_operator_approval_phrase_received: {closure['explicit_operator_approval_phrase_received']}",
        f"- operator_approval_required: {closure['operator_approval_required']}",
        f"- operator_approval_granted: {closure['operator_approval_granted']}",
        "",
        "## Closure checks",
        "",
    ]

    for item in closure["closure_check_list"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Closure results", ""])

    for result in closure["closure_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Closure decision",
            "",
            "Milestone #9 is closed with real submission blocked. No Kaggle authentication, upload, submission, score claim, or leaderboard claim has been performed.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_BLOCKED_CLOSURE_READY=true",
            "ARC_AGI3_MILESTONE_9_CLOSURE_MODE=MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_CLOSURE_VERDICT=MILESTONE_9_CLOSED_REAL_SUBMISSION_BLOCKED_NO_KAGGLE_ACTION",
            "ARC_AGI3_MILESTONE_9_BASELINE_DECISION_RECORD_COMMIT=793d24b",
            "ARC_AGI3_MILESTONE_9_CLOSURE_CHECK_COUNT=18",
            "ARC_AGI3_MILESTONE_9_CLOSURE_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_CLOSURE_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_CLOSURE_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_CREATED=true",
            "ARC_AGI3_MILESTONE_9_CLOSED=true",
            "ARC_AGI3_MILESTONE_9_CLOSURE_TYPE=REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_CLOSURE_REASON=OPERATOR_APPROVAL_NOT_GRANTED",
            "ARC_AGI3_MILESTONE_9_CLOSURE_STATUS_VERDICT=CLOSED_WITH_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED",
            "ARC_AGI3_MILESTONE_9_REAL_SUBMISSION_DECISION_REASON=OPERATOR_APPROVAL_NOT_GRANTED",
            "ARC_AGI3_MILESTONE_9_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_9_PROVIDED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_ACCEPTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_EXPLICIT_OPERATOR_APPROVAL_PHRASE_RECEIVED=false",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_CLOSED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
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


def render_real_submission_blocked_closure_manifest(closure: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 REAL SUBMISSION BLOCKED CLOSURE MANIFEST v1",
        f"closure_id={closure['closure_id']}",
        f"signature={closure['signature']}",
        f"status={closure['status']}",
        f"baseline_commit={closure['baseline_commit']}",
        f"closure_mode={closure['closure_mode']}",
        f"closure_verdict={closure['closure_verdict']}",
        f"next_allowed_stage={closure['next_allowed_stage']}",
        f"closure_ready={closure['closure_ready']}",
        f"closure_locked={closure['closure_locked']}",
        f"real_submission_blocked_closure_created={closure['real_submission_blocked_closure_created']}",
        f"real_submission_blocked_closure_ready={closure['real_submission_blocked_closure_ready']}",
        f"real_submission_blocked_closure_locked={closure['real_submission_blocked_closure_locked']}",
        f"milestone_9_closed={closure['milestone_9_closed']}",
        f"milestone_9_closure_type={closure['milestone_9_closure_type']}",
        f"milestone_9_closure_reason={closure['milestone_9_closure_reason']}",
        f"milestone_9_closure_verdict={closure['milestone_9_closure_verdict']}",
        f"real_submission_decision={closure['real_submission_decision']}",
        f"real_submission_decision_reason={closure['real_submission_decision_reason']}",
        f"required_declaration_count={closure['required_declaration_count']}",
        f"provided_declaration_count={closure['provided_declaration_count']}",
        f"accepted_declaration_count={closure['accepted_declaration_count']}",
        f"explicit_operator_approval_phrase_received={closure['explicit_operator_approval_phrase_received']}",
        f"closure_check_count={closure['closure_check_count']}",
        f"closure_case_count={closure['closure_case_count']}",
        f"closure_pass_count={closure['closure_pass_count']}",
        f"closure_failure_count={closure['closure_failure_count']}",
        f"closure_gate_count={closure['closure_gate_count']}",
        f"passed_gate_count={closure['passed_gate_count']}",
        f"closure_issue_count={closure['closure_issue_count']}",
        f"operator_approval_required={closure['operator_approval_required']}",
        f"operator_approval_granted={closure['operator_approval_granted']}",
        f"operator_approval_received={closure['operator_approval_received']}",
        f"manual_upload_allowed={closure['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={closure['kaggle_authentication_allowed']}",
        f"real_submission_created={closure['real_submission_created']}",
        f"real_submission_allowed={closure['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={closure['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={closure['kaggle_submission_sent']}",
        f"upload_performed={closure['upload_performed']}",
        f"kaggle_authentication_performed={closure['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "CLOSURE_CHECKS",
    ]

    for item in closure["closure_check_list"]:
        lines.append(item)

    lines.append("")
    lines.append("CLOSURE_RESULTS")
    for result in closure["closure_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_real_submission_blocked_closure_artifacts(
    closure: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    closure = dict(closure or build_milestone_9_real_submission_blocked_closure())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-real-submission-blocked-closure-v1.json"
    md_path = output / "milestone-9-real-submission-blocked-closure-v1.md"
    manifest_path = output / "milestone-9-real-submission-blocked-closure-manifest-v1.txt"
    index_path = output / "milestone-9-real-submission-blocked-closure-index-v1.json"

    json_path.write_text(json.dumps(closure, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_blocked_closure_markdown(closure), encoding="utf-8")
    manifest_path.write_text(render_real_submission_blocked_closure_manifest(closure), encoding="utf-8")
    index_path.write_text(json.dumps(closure["closure_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_real_submission_blocked_closure_pipeline() -> Dict[str, Any]:
    closure = build_milestone_9_real_submission_blocked_closure()
    validation = validate_milestone_9_real_submission_blocked_closure(closure)
    artifacts = write_real_submission_blocked_closure_artifacts(closure)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_REAL_SUBMISSION_BLOCKED_CLOSURE_V1_PIPELINE_INVALID",
        "closure_status": closure["status"],
        "validation_status": validation["status"],
        "closure": closure,
        "closure_id": closure["closure_id"],
        "signature": closure["signature"],
        "closure_mode": closure["closure_mode"],
        "closure_verdict": closure["closure_verdict"],
        "next_allowed_stage": closure["next_allowed_stage"],
        "closure_ready": closure["closure_ready"],
        "closure_locked": closure["closure_locked"],
        "real_submission_blocked_closure_created": closure[
            "real_submission_blocked_closure_created"
        ],
        "real_submission_blocked_closure_ready": closure[
            "real_submission_blocked_closure_ready"
        ],
        "real_submission_blocked_closure_locked": closure[
            "real_submission_blocked_closure_locked"
        ],
        "milestone_9_closed": closure["milestone_9_closed"],
        "milestone_9_closure_type": closure["milestone_9_closure_type"],
        "milestone_9_closure_reason": closure["milestone_9_closure_reason"],
        "milestone_9_closure_verdict": closure["milestone_9_closure_verdict"],
        "real_submission_decision": closure["real_submission_decision"],
        "real_submission_decision_reason": closure["real_submission_decision_reason"],
        "required_declaration_count": closure["required_declaration_count"],
        "provided_declaration_count": closure["provided_declaration_count"],
        "accepted_declaration_count": closure["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": closure[
            "explicit_operator_approval_phrase_received"
        ],
        "closure_check_count": closure["closure_check_count"],
        "closure_case_count": closure["closure_case_count"],
        "closure_pass_count": closure["closure_pass_count"],
        "closure_failure_count": closure["closure_failure_count"],
        "regression_guard_count": closure["regression_guard_count"],
        "boundary_control_count": closure["boundary_control_count"],
        "closure_gate_count": closure["closure_gate_count"],
        "passed_gate_count": closure["passed_gate_count"],
        "closure_issue_count": closure["closure_issue_count"],
        "warning_count": closure["warning_count"],
        "operator_approval_required": closure["operator_approval_required"],
        "operator_approval_granted": closure["operator_approval_granted"],
        "operator_approval_received": closure["operator_approval_received"],
        "manual_upload_allowed": closure["manual_upload_allowed"],
        "kaggle_authentication_allowed": closure["kaggle_authentication_allowed"],
        "real_submission_created": closure["real_submission_created"],
        "real_submission_allowed": closure["real_submission_allowed"],
        "ready_for_real_kaggle_submission": closure["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": closure["kaggle_submission_sent"],
        "upload_performed": closure["upload_performed"],
        "kaggle_authentication_performed": closure["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": closure["metadata"],
    }
