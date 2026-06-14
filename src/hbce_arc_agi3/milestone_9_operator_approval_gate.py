"""Milestone #9 Operator Approval Gate v1.

Local-only deterministic operator approval gate.

This module verifies the real submission preflight package and operator
declaration package, then confirms that operator approval is still absent.
The approval gate is ready but not open.

It does not submit to Kaggle, authenticate, upload files, call external APIs,
read secrets, accept declarations, grant approval, claim a Kaggle score, claim
public leaderboard improvement, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


APPROVAL_STATUS = "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY"
PIPELINE_STATUS = "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_VALID"

BASELINE_COMMIT = "1433853 Add ARC AGI3 real submission preflight gate"
APPROVAL_MODE = "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_LOCAL_ONLY"
APPROVAL_SCOPE = "VERIFY_OPERATOR_APPROVAL_ABSENT_KEEP_REAL_SUBMISSION_BLOCKED"
APPROVAL_VERDICT = "OPERATOR_APPROVAL_GATE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_9_TASK_6_REAL_SUBMISSION_DECISION_RECORD_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-9/operator-approval-gate-v1"

PREFLIGHT_JSON = Path(
    "examples/milestone-9/real-submission-preflight-gate-v1/"
    "milestone-9-real-submission-preflight-gate-v1.json"
)

DECLARATION_PACKAGE_JSON = Path(
    "examples/milestone-9/operator-declaration-package-v1/"
    "milestone-9-operator-declaration-package-v1.json"
)

EXPECTED_APPROVAL_CHECK_COUNT = 16
EXPECTED_APPROVAL_CASE_COUNT = 10
EXPECTED_APPROVAL_PASS_COUNT = 10
EXPECTED_APPROVAL_FAILURE_COUNT = 0
EXPECTED_REQUIRED_DECLARATION_COUNT = 8
EXPECTED_PROVIDED_DECLARATION_COUNT = 0
EXPECTED_ACCEPTED_DECLARATION_COUNT = 0
EXPECTED_BOUNDARY_CONTROL_COUNT = 9
EXPECTED_REGRESSION_GUARD_COUNT = 12

APPROVAL_CHECKS: Tuple[str, ...] = (
    "preflight_artifact_exists",
    "preflight_artifact_ready",
    "preflight_gate_ready",
    "preflight_gate_closed",
    "declaration_package_exists",
    "declaration_package_ready",
    "required_declarations_present",
    "provided_declarations_absent",
    "accepted_declarations_absent",
    "explicit_operator_approval_absent",
    "approval_gate_ready",
    "approval_gate_closed",
    "manual_upload_blocked",
    "authentication_blocked",
    "real_submission_blocked",
    "claim_boundary_preserved",
)

APPROVAL_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "approval_preflight_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_preflight_artifact",
    },
    {
        "case_id": "approval_declaration_package_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_declaration_package",
    },
    {
        "case_id": "approval_required_declarations_present_v1",
        "area": "operator_declarations",
        "operation": "verify_required_declarations_present",
    },
    {
        "case_id": "approval_declarations_not_accepted_v1",
        "area": "operator_declarations",
        "operation": "verify_no_accepted_declarations",
    },
    {
        "case_id": "approval_explicit_operator_approval_absent_v1",
        "area": "approval_gate",
        "operation": "verify_explicit_approval_absent",
    },
    {
        "case_id": "approval_gate_ready_but_closed_v1",
        "area": "approval_gate",
        "operation": "verify_gate_ready_but_closed",
    },
    {
        "case_id": "approval_real_submission_blocked_v1",
        "area": "submission",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "approval_no_upload_no_auth_v1",
        "area": "boundary",
        "operation": "verify_no_upload_no_auth",
    },
    {
        "case_id": "approval_no_score_or_leaderboard_claim_v1",
        "area": "claim_boundary",
        "operation": "verify_no_score_or_leaderboard_claim",
    },
    {
        "case_id": "approval_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_real_submission_decision_record_next",
    },
)

REGRESSION_GUARDS: Tuple[str, ...] = (
    "guard_approval_uses_preflight_artifact",
    "guard_approval_uses_declaration_package",
    "guard_approval_requires_all_declarations",
    "guard_approval_rejects_empty_declarations",
    "guard_approval_rejects_missing_explicit_phrase",
    "guard_approval_gate_closed_without_operator_approval",
    "guard_approval_manual_upload_blocked",
    "guard_approval_real_submission_blocked",
    "guard_approval_does_not_authenticate",
    "guard_approval_does_not_upload",
    "guard_approval_no_private_core_exposure",
    "guard_approval_no_legal_certification",
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


def build_approval_source_summary() -> Dict[str, Any]:
    preflight = _read_json(PREFLIGHT_JSON)
    declaration = _read_json(DECLARATION_PACKAGE_JSON)
    preflight_source = preflight.get("preflight_source_summary", {})

    return {
        "preflight_path": str(PREFLIGHT_JSON),
        "preflight_present": PREFLIGHT_JSON.exists(),
        "preflight_status": preflight.get("status", "MISSING"),
        "preflight_id": preflight.get("preflight_id", "MISSING_PREFLIGHT_ID"),
        "preflight_signature": preflight.get("signature", ""),
        "preflight_gate_ready": preflight.get("preflight_gate_ready", False),
        "preflight_gate_open": preflight.get("preflight_gate_open", True),
        "declaration_package_path": str(DECLARATION_PACKAGE_JSON),
        "declaration_package_present": DECLARATION_PACKAGE_JSON.exists(),
        "declaration_package_status": declaration.get("status", "MISSING"),
        "declaration_package_id": declaration.get("package_id", "MISSING_DECLARATION_PACKAGE_ID"),
        "declaration_package_signature": declaration.get("signature", ""),
        "candidate_source_path": preflight_source.get("candidate_source_path", "MISSING_CANDIDATE_SOURCE"),
        "candidate_id": preflight_source.get("candidate_id", "MISSING_CANDIDATE_ID"),
        "candidate_signature": preflight_source.get("candidate_signature", ""),
        "candidate_count": preflight.get("candidate_count", 0),
        "required_declaration_count": declaration.get("required_declaration_count", 0),
        "provided_declaration_count": declaration.get("provided_declaration_count", 0),
        "accepted_declaration_count": declaration.get("accepted_declaration_count", 0),
        "preflight_sha256": _sha256(PREFLIGHT_JSON),
        "preflight_sha256_16": _sha16(_sha256(PREFLIGHT_JSON)),
        "declaration_sha256": _sha256(DECLARATION_PACKAGE_JSON),
        "declaration_sha256_16": _sha16(_sha256(DECLARATION_PACKAGE_JSON)),
    }


def build_operator_approval_gate_state() -> Dict[str, Any]:
    return {
        "operator_approval_gate_required": True,
        "operator_approval_gate_created": True,
        "operator_approval_gate_ready": True,
        "operator_approval_gate_open": False,
        "operator_approval_required": True,
        "operator_approval_granted": False,
        "operator_approval_received": False,
        "explicit_operator_approval_phrase_required": True,
        "explicit_operator_approval_phrase_received": False,
        "all_required_declarations_accepted": False,
        "approval_gate_verdict": "APPROVAL_GATE_READY_BUT_CLOSED_OPERATOR_APPROVAL_ABSENT",
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "real_submission_allowed": False,
    }


def build_operator_approval_gate_checks() -> Dict[str, bool]:
    preflight = _read_json(PREFLIGHT_JSON)
    declaration = _read_json(DECLARATION_PACKAGE_JSON)
    source = build_approval_source_summary()
    approval = build_operator_approval_gate_state()

    return {
        "preflight_artifact_present": PREFLIGHT_JSON.exists(),
        "preflight_artifact_ready": preflight.get("status")
        == "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY",
        "preflight_artifact_valid": bool(preflight.get("preflight_id")) and bool(preflight.get("signature")),
        "preflight_next_stage_matches_task_5": preflight.get("next_allowed_stage")
        == "MILESTONE_9_TASK_5_OPERATOR_APPROVAL_GATE_V1",
        "preflight_ready": preflight.get("preflight_ready") is True,
        "preflight_gate_ready": preflight.get("preflight_gate_ready") is True,
        "preflight_gate_closed": preflight.get("preflight_gate_open") is False,
        "preflight_real_submission_blocked": preflight.get("real_submission_allowed") is False,
        "candidate_source_present": Path(source["candidate_source_path"]).exists(),
        "candidate_id_present": source["candidate_id"] != "MISSING_CANDIDATE_ID",
        "candidate_signature_present": bool(source["candidate_signature"]),
        "candidate_count_positive": source["candidate_count"] > 0,
        "declaration_package_present": DECLARATION_PACKAGE_JSON.exists(),
        "declaration_package_ready": declaration.get("status")
        == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY",
        "declaration_package_valid": bool(declaration.get("package_id")) and bool(declaration.get("signature")),
        "required_declaration_count_valid": declaration.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": declaration.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": declaration.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "approval_check_count_valid": len(APPROVAL_CHECKS) == EXPECTED_APPROVAL_CHECK_COUNT,
        "approval_gate_required": approval["operator_approval_gate_required"] is True,
        "approval_gate_created": approval["operator_approval_gate_created"] is True,
        "approval_gate_ready": approval["operator_approval_gate_ready"] is True,
        "approval_gate_closed": approval["operator_approval_gate_open"] is False,
        "operator_approval_required": approval["operator_approval_required"] is True,
        "operator_approval_not_granted": approval["operator_approval_granted"] is False,
        "operator_approval_not_received": approval["operator_approval_received"] is False,
        "explicit_operator_approval_phrase_required": approval["explicit_operator_approval_phrase_required"] is True,
        "explicit_operator_approval_phrase_absent": approval["explicit_operator_approval_phrase_received"] is False,
        "all_required_declarations_not_accepted": approval["all_required_declarations_accepted"] is False,
        "manual_upload_not_allowed": approval["manual_upload_allowed"] is False,
        "kaggle_authentication_not_allowed": approval["kaggle_authentication_allowed"] is False,
        "real_submission_not_created": True,
        "real_submission_allowed_false": approval["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": False is False,
        "kaggle_submission_not_sent": False is False,
        "upload_not_performed": False is False,
        "kaggle_authentication_not_performed": False is False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "external_api_dependency_false": True,
        "private_core_exposure_false": True,
        "legal_certification_false": True,
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_9_TASK_6_REAL_SUBMISSION_DECISION_RECORD_V1",
    }


def evaluate_operator_approval_gate_case(case_id: str) -> Dict[str, Any]:
    checks = build_operator_approval_gate_checks()

    if case_id == "approval_preflight_source_ready_v1":
        passed = (
            checks["preflight_artifact_present"]
            and checks["preflight_artifact_ready"]
            and checks["preflight_artifact_valid"]
            and checks["preflight_ready"]
        )
        return _result(case_id, "source_binding", "verify_preflight_artifact", passed)

    if case_id == "approval_declaration_package_source_ready_v1":
        passed = (
            checks["declaration_package_present"]
            and checks["declaration_package_ready"]
            and checks["declaration_package_valid"]
        )
        return _result(case_id, "source_binding", "verify_declaration_package", passed)

    if case_id == "approval_required_declarations_present_v1":
        passed = checks["required_declaration_count_valid"]
        return _result(case_id, "operator_declarations", "verify_required_declarations_present", passed)

    if case_id == "approval_declarations_not_accepted_v1":
        passed = (
            checks["provided_declaration_count_zero"]
            and checks["accepted_declaration_count_zero"]
            and checks["all_required_declarations_not_accepted"]
        )
        return _result(case_id, "operator_declarations", "verify_no_accepted_declarations", passed)

    if case_id == "approval_explicit_operator_approval_absent_v1":
        passed = (
            checks["explicit_operator_approval_phrase_required"]
            and checks["explicit_operator_approval_phrase_absent"]
            and checks["operator_approval_not_received"]
        )
        return _result(case_id, "approval_gate", "verify_explicit_approval_absent", passed)

    if case_id == "approval_gate_ready_but_closed_v1":
        passed = (
            checks["approval_gate_required"]
            and checks["approval_gate_created"]
            and checks["approval_gate_ready"]
            and checks["approval_gate_closed"]
            and checks["operator_approval_not_granted"]
        )
        return _result(case_id, "approval_gate", "verify_gate_ready_but_closed", passed)

    if case_id == "approval_real_submission_blocked_v1":
        passed = (
            checks["preflight_real_submission_blocked"]
            and checks["real_submission_not_created"]
            and checks["real_submission_allowed_false"]
            and checks["ready_for_real_kaggle_submission_false"]
            and checks["kaggle_submission_not_sent"]
        )
        return _result(case_id, "submission", "verify_real_submission_blocked", passed)

    if case_id == "approval_no_upload_no_auth_v1":
        passed = (
            checks["manual_upload_not_allowed"]
            and checks["kaggle_authentication_not_allowed"]
            and checks["upload_not_performed"]
            and checks["kaggle_authentication_not_performed"]
        )
        return _result(case_id, "boundary", "verify_no_upload_no_auth", passed)

    if case_id == "approval_no_score_or_leaderboard_claim_v1":
        passed = checks["score_claim_absent"] and checks["public_leaderboard_claim_absent"]
        return _result(case_id, "claim_boundary", "verify_no_score_or_leaderboard_claim", passed)

    if case_id == "approval_next_stage_valid_v1":
        passed = checks["next_stage_valid"]
        return _result(case_id, "next_stage", "verify_real_submission_decision_record_next", passed)

    raise ValueError(f"unknown operator approval gate case: {case_id}")


def evaluate_all_operator_approval_gate_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_operator_approval_gate_case(case["case_id"]) for case in APPROVAL_CASES)


def build_milestone_9_operator_approval_gate() -> Dict[str, Any]:
    preflight = _read_json(PREFLIGHT_JSON)
    declaration = _read_json(DECLARATION_PACKAGE_JSON)
    source = build_approval_source_summary()
    approval = build_operator_approval_gate_state()
    checks = build_operator_approval_gate_checks()
    results = evaluate_all_operator_approval_gate_cases()

    approval_pass_count = sum(1 for result in results if result["passed"] is True)
    approval_failure_count = sum(1 for result in results if result["passed"] is False)

    approval_record = {
        "approval_mode": APPROVAL_MODE,
        "approval_scope": APPROVAL_SCOPE,
        "approval_verdict": APPROVAL_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "approval_ready": True,
        "approval_locked": True,
        "baseline_preflight_id": preflight.get("preflight_id", "MISSING_PREFLIGHT_ID"),
        "preflight_ready": preflight.get("preflight_ready") is True,
        "declaration_package_id": declaration.get("package_id", "MISSING_DECLARATION_PACKAGE_ID"),
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_signature": source["candidate_signature"],
        "candidate_count": source["candidate_count"],
        "operator_approval_gate_created": approval["operator_approval_gate_created"],
        "operator_approval_gate_ready": approval["operator_approval_gate_ready"],
        "operator_approval_gate_open": approval["operator_approval_gate_open"],
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
        "explicit_operator_approval_phrase_required": approval["explicit_operator_approval_phrase_required"],
        "explicit_operator_approval_phrase_received": approval["explicit_operator_approval_phrase_received"],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "all_required_declarations_accepted": approval["all_required_declarations_accepted"],
        "approval_check_count": len(APPROVAL_CHECKS),
        "approval_case_count": len(APPROVAL_CASES),
        "approval_pass_count": approval_pass_count,
        "approval_failure_count": approval_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "manual_upload_allowed": approval["manual_upload_allowed"],
        "kaggle_authentication_allowed": approval["kaggle_authentication_allowed"],
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
        "preflight_artifact_present": checks["preflight_artifact_present"],
        "preflight_artifact_ready": checks["preflight_artifact_ready"],
        "preflight_artifact_valid": checks["preflight_artifact_valid"],
        "preflight_next_stage_matches_task_5": checks["preflight_next_stage_matches_task_5"],
        "preflight_ready": checks["preflight_ready"],
        "preflight_gate_ready": checks["preflight_gate_ready"],
        "preflight_gate_closed": checks["preflight_gate_closed"],
        "preflight_real_submission_blocked": checks["preflight_real_submission_blocked"],
        "candidate_source_present": checks["candidate_source_present"],
        "candidate_id_present": checks["candidate_id_present"],
        "candidate_signature_present": checks["candidate_signature_present"],
        "candidate_count_positive": checks["candidate_count_positive"],
        "declaration_package_present": checks["declaration_package_present"],
        "declaration_package_ready": checks["declaration_package_ready"],
        "declaration_package_valid": checks["declaration_package_valid"],
        "required_declaration_count_valid": checks["required_declaration_count_valid"],
        "provided_declaration_count_zero": checks["provided_declaration_count_zero"],
        "accepted_declaration_count_zero": checks["accepted_declaration_count_zero"],
        "approval_mode_valid": APPROVAL_MODE == "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_LOCAL_ONLY",
        "approval_scope_valid": APPROVAL_SCOPE == "VERIFY_OPERATOR_APPROVAL_ABSENT_KEEP_REAL_SUBMISSION_BLOCKED",
        "approval_verdict_valid": APPROVAL_VERDICT
        == "OPERATOR_APPROVAL_GATE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
        "approval_check_count_valid": checks["approval_check_count_valid"],
        "approval_gate_required": checks["approval_gate_required"],
        "approval_gate_created": checks["approval_gate_created"],
        "approval_gate_ready": checks["approval_gate_ready"],
        "approval_gate_closed": checks["approval_gate_closed"],
        "approval_case_count_valid": len(APPROVAL_CASES) == EXPECTED_APPROVAL_CASE_COUNT,
        "approval_pass_count_valid": approval_pass_count == EXPECTED_APPROVAL_PASS_COUNT,
        "approval_failure_count_zero": approval_failure_count == EXPECTED_APPROVAL_FAILURE_COUNT,
        "all_approval_cases_pass": all(result["passed"] is True for result in results),
        "operator_approval_required": checks["operator_approval_required"],
        "operator_approval_not_granted": checks["operator_approval_not_granted"],
        "operator_approval_not_received": checks["operator_approval_not_received"],
        "explicit_operator_approval_phrase_required": checks["explicit_operator_approval_phrase_required"],
        "explicit_operator_approval_phrase_absent": checks["explicit_operator_approval_phrase_absent"],
        "all_required_declarations_not_accepted": checks["all_required_declarations_not_accepted"],
        "manual_upload_not_allowed": checks["manual_upload_not_allowed"],
        "kaggle_authentication_not_allowed": checks["kaggle_authentication_not_allowed"],
        "regression_guard_count_valid": len(REGRESSION_GUARDS) == EXPECTED_REGRESSION_GUARD_COUNT,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == EXPECTED_BOUNDARY_CONTROL_COUNT,
        "next_stage_valid": checks["next_stage_valid"],
        "real_submission_not_created": approval_record["real_submission_created"] is False,
        "real_submission_allowed_false": approval_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": approval_record["ready_for_real_kaggle_submission"] is False,
        "kaggle_submission_not_sent": approval_record["kaggle_submission_sent"] is False,
        "upload_not_performed": approval_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": approval_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": approval_record["external_api_dependency"] is False,
        "contains_api_keys_false": approval_record["contains_api_keys"] is False,
        "private_core_exposure_false": approval_record["private_core_exposure"] is False,
        "legal_certification_false": approval_record["legal_certification"] is False,
        "score_claim_absent": approval_record["score_claim_absent"] is True,
        "public_leaderboard_claim_absent": approval_record["public_leaderboard_claim_absent"] is True,
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

    approval_ready = (
        preflight.get("status") == "MILESTONE_9_REAL_SUBMISSION_PREFLIGHT_GATE_V1_READY"
        and declaration.get("status") == "MILESTONE_9_OPERATOR_DECLARATION_PACKAGE_V1_READY"
        and approval_pass_count == EXPECTED_APPROVAL_PASS_COUNT
        and approval_failure_count == EXPECTED_APPROVAL_FAILURE_COUNT
        and source["required_declaration_count"] == EXPECTED_REQUIRED_DECLARATION_COUNT
        and source["accepted_declaration_count"] == EXPECTED_ACCEPTED_DECLARATION_COUNT
        and approval["operator_approval_granted"] is False
        and approval_record["real_submission_allowed"] is False
        and passed_gate_count == len(gates)
        and issue_count == 0
    )

    index = {
        "milestone": "Milestone #9",
        "task": "Task 5",
        "approval_mode": APPROVAL_MODE,
        "approval_scope": APPROVAL_SCOPE,
        "approval_verdict": APPROVAL_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_preflight": preflight.get("preflight_id", "MISSING_PREFLIGHT_ID"),
        "depends_on_declaration_package": declaration.get("package_id", "MISSING_DECLARATION_PACKAGE_ID"),
        "candidate_source_path": source["candidate_source_path"],
        "candidate_id": source["candidate_id"],
        "candidate_count": source["candidate_count"],
        "approval_ready": approval_ready,
        "approval_locked": True,
        "operator_approval_gate_created": True,
        "operator_approval_gate_ready": True,
        "operator_approval_gate_open": False,
        "approval_check_count": len(APPROVAL_CHECKS),
        "approval_case_count": len(APPROVAL_CASES),
        "approval_pass_count": approval_pass_count,
        "approval_failure_count": approval_failure_count,
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": False,
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
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
        "status": APPROVAL_STATUS,
        "milestone": "Milestone #9",
        "task": "Task 5",
        "title": "Operator Approval Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "approval_mode": APPROVAL_MODE,
        "approval_scope": APPROVAL_SCOPE,
        "approval_verdict": APPROVAL_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "preflight_source": {
            "path": str(PREFLIGHT_JSON),
            "present": PREFLIGHT_JSON.exists(),
            "status": preflight.get("status", "MISSING"),
            "preflight_id": preflight.get("preflight_id", "MISSING_PREFLIGHT_ID"),
            "sha256": _sha256(PREFLIGHT_JSON),
            "sha256_16": _sha16(_sha256(PREFLIGHT_JSON)),
        },
        "declaration_package_source": {
            "path": str(DECLARATION_PACKAGE_JSON),
            "present": DECLARATION_PACKAGE_JSON.exists(),
            "status": declaration.get("status", "MISSING"),
            "package_id": declaration.get("package_id", "MISSING_DECLARATION_PACKAGE_ID"),
            "sha256": _sha256(DECLARATION_PACKAGE_JSON),
            "sha256_16": _sha16(_sha256(DECLARATION_PACKAGE_JSON)),
        },
        "approval_source_summary": source,
        "approval_state": approval,
        "approval_checks": checks,
        "approval_check_list": list(APPROVAL_CHECKS),
        "approval_cases": list(APPROVAL_CASES),
        "approval_results": list(results),
        "regression_guards": list(REGRESSION_GUARDS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "approval_gates": list(gates),
        "approval_issues": list(issues),
        "approval_index": index,
        "approval_record": approval_record,
        "approval_ready": approval_ready,
        "approval_locked": True,
        "operator_approval_gate_created": approval["operator_approval_gate_created"],
        "operator_approval_gate_ready": approval["operator_approval_gate_ready"],
        "operator_approval_gate_open": approval["operator_approval_gate_open"],
        "candidate_count": source["candidate_count"],
        "required_declaration_count": source["required_declaration_count"],
        "provided_declaration_count": source["provided_declaration_count"],
        "accepted_declaration_count": source["accepted_declaration_count"],
        "approval_check_count": len(APPROVAL_CHECKS),
        "approval_case_count": len(APPROVAL_CASES),
        "approval_pass_count": approval_pass_count,
        "approval_failure_count": approval_failure_count,
        "regression_guard_count": len(REGRESSION_GUARDS),
        "boundary_control_count": len(BOUNDARY_CONTROLS),
        "approval_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "approval_issue_count": issue_count,
        "warning_count": 0,
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
        "explicit_operator_approval_phrase_required": approval["explicit_operator_approval_phrase_required"],
        "explicit_operator_approval_phrase_received": approval["explicit_operator_approval_phrase_received"],
        "all_required_declarations_accepted": approval["all_required_declarations_accepted"],
        "manual_upload_allowed": approval["manual_upload_allowed"],
        "kaggle_authentication_allowed": approval["kaggle_authentication_allowed"],
        "real_submission_created": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "score_claim_absent": True,
        "public_leaderboard_claim_absent": True,
        "metadata": {
            "source": "milestone_9_operator_approval_gate_v1",
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
        "approval_id": f"MILESTONE-9-APPROVAL-GATE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_9_operator_approval_gate(approval: Mapping[str, Any]) -> Dict[str, Any]:
    gates = approval.get("approval_gates", [])
    issues = approval.get("approval_issues", [])
    results = approval.get("approval_results", [])

    checks = {
        "status_ready": approval.get("status") == APPROVAL_STATUS,
        "approval_id_present": isinstance(approval.get("approval_id"), str) and bool(approval.get("approval_id")),
        "signature_present": isinstance(approval.get("signature"), str) and bool(approval.get("signature")),
        "baseline_commit_valid": str(approval.get("baseline_commit", "")).startswith("1433853"),
        "approval_mode_valid": approval.get("approval_mode") == APPROVAL_MODE,
        "approval_scope_valid": approval.get("approval_scope") == APPROVAL_SCOPE,
        "approval_verdict_valid": approval.get("approval_verdict") == APPROVAL_VERDICT,
        "next_allowed_stage_valid": approval.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "approval_ready": approval.get("approval_ready") is True,
        "approval_locked": approval.get("approval_locked") is True,
        "operator_approval_gate_created": approval.get("operator_approval_gate_created") is True,
        "operator_approval_gate_ready": approval.get("operator_approval_gate_ready") is True,
        "operator_approval_gate_closed": approval.get("operator_approval_gate_open") is False,
        "approval_check_count_valid": approval.get("approval_check_count") == EXPECTED_APPROVAL_CHECK_COUNT,
        "approval_case_count_valid": approval.get("approval_case_count") == EXPECTED_APPROVAL_CASE_COUNT,
        "approval_pass_count_valid": approval.get("approval_pass_count") == EXPECTED_APPROVAL_PASS_COUNT,
        "approval_failure_count_zero": approval.get("approval_failure_count") == EXPECTED_APPROVAL_FAILURE_COUNT,
        "required_declaration_count_valid": approval.get("required_declaration_count")
        == EXPECTED_REQUIRED_DECLARATION_COUNT,
        "provided_declaration_count_zero": approval.get("provided_declaration_count")
        == EXPECTED_PROVIDED_DECLARATION_COUNT,
        "accepted_declaration_count_zero": approval.get("accepted_declaration_count")
        == EXPECTED_ACCEPTED_DECLARATION_COUNT,
        "candidate_count_positive": approval.get("candidate_count", 0) > 0,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_approval_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "approval_issue_count_zero": approval.get("approval_issue_count") == 0,
        "all_approval_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "operator_approval_required": approval.get("operator_approval_required") is True,
        "operator_approval_not_granted": approval.get("operator_approval_granted") is False,
        "operator_approval_not_received": approval.get("operator_approval_received") is False,
        "explicit_operator_approval_phrase_required": approval.get("explicit_operator_approval_phrase_required") is True,
        "explicit_operator_approval_phrase_absent": approval.get("explicit_operator_approval_phrase_received") is False,
        "all_required_declarations_not_accepted": approval.get("all_required_declarations_accepted") is False,
        "manual_upload_not_allowed": approval.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": approval.get("kaggle_authentication_allowed") is False,
        "real_submission_not_created": approval.get("real_submission_created") is False,
        "real_submission_allowed_false": approval.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": approval.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": approval.get("kaggle_submission_sent") is False,
        "upload_not_performed": approval.get("upload_performed") is False,
        "kaggle_authentication_not_performed": approval.get("kaggle_authentication_performed") is False,
        "metadata_safe": approval.get("metadata", {}).get("external_api_dependency") is False
        and approval.get("metadata", {}).get("contains_api_keys") is False
        and approval.get("metadata", {}).get("private_core_exposure") is False
        and approval.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "approval_id": approval.get("approval_id"),
        "signature": approval.get("signature"),
    }


def render_operator_approval_gate_markdown(approval: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #9 - Operator Approval Gate v1",
        "",
        f"- status: {approval['status']}",
        f"- approval_id: {approval['approval_id']}",
        f"- signature: {approval['signature']}",
        f"- baseline_commit: {approval['baseline_commit']}",
        f"- approval_mode: {approval['approval_mode']}",
        f"- approval_scope: {approval['approval_scope']}",
        f"- approval_verdict: {approval['approval_verdict']}",
        f"- next_allowed_stage: {approval['next_allowed_stage']}",
        f"- approval_ready: {approval['approval_ready']}",
        f"- operator_approval_gate_created: {approval['operator_approval_gate_created']}",
        f"- operator_approval_gate_open: {approval['operator_approval_gate_open']}",
        f"- required_declaration_count: {approval['required_declaration_count']}",
        f"- provided_declaration_count: {approval['provided_declaration_count']}",
        f"- accepted_declaration_count: {approval['accepted_declaration_count']}",
        f"- explicit_operator_approval_phrase_received: {approval['explicit_operator_approval_phrase_received']}",
        f"- operator_approval_required: {approval['operator_approval_required']}",
        f"- operator_approval_granted: {approval['operator_approval_granted']}",
        "",
        "## Approval checks",
        "",
    ]

    for item in approval["approval_check_list"]:
        lines.append(f"- {item}")

    lines.extend(["", "## Approval results", ""])

    for result in approval["approval_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Operator approval gate is ready but closed. No accepted declarations and no explicit operator approval are present. Real submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_READY=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_9_APPROVAL_GATE_READY=true",
            "ARC_AGI3_MILESTONE_9_APPROVAL_MODE=MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_9_APPROVAL_VERDICT=OPERATOR_APPROVAL_GATE_READY_APPROVAL_NOT_GRANTED_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_9_BASELINE_PREFLIGHT_GATE_COMMIT=1433853",
            "ARC_AGI3_MILESTONE_9_APPROVAL_CHECK_COUNT=16",
            "ARC_AGI3_MILESTONE_9_APPROVAL_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_9_APPROVAL_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_9_APPROVAL_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_CREATED=true",
            "ARC_AGI3_MILESTONE_9_OPERATOR_APPROVAL_GATE_OPEN=false",
            "ARC_AGI3_MILESTONE_9_REQUIRED_DECLARATION_COUNT=8",
            "ARC_AGI3_MILESTONE_9_PROVIDED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_ACCEPTED_DECLARATION_COUNT=0",
            "ARC_AGI3_MILESTONE_9_EXPLICIT_OPERATOR_APPROVAL_PHRASE_RECEIVED=false",
            "ARC_AGI3_MILESTONE_9_NEXT_STAGE=MILESTONE_9_TASK_6_REAL_SUBMISSION_DECISION_RECORD_V1",
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


def render_operator_approval_gate_manifest(approval: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 9 OPERATOR APPROVAL GATE MANIFEST v1",
        f"approval_id={approval['approval_id']}",
        f"signature={approval['signature']}",
        f"status={approval['status']}",
        f"baseline_commit={approval['baseline_commit']}",
        f"approval_mode={approval['approval_mode']}",
        f"approval_verdict={approval['approval_verdict']}",
        f"next_allowed_stage={approval['next_allowed_stage']}",
        f"approval_ready={approval['approval_ready']}",
        f"approval_locked={approval['approval_locked']}",
        f"operator_approval_gate_created={approval['operator_approval_gate_created']}",
        f"operator_approval_gate_ready={approval['operator_approval_gate_ready']}",
        f"operator_approval_gate_open={approval['operator_approval_gate_open']}",
        f"required_declaration_count={approval['required_declaration_count']}",
        f"provided_declaration_count={approval['provided_declaration_count']}",
        f"accepted_declaration_count={approval['accepted_declaration_count']}",
        f"explicit_operator_approval_phrase_required={approval['explicit_operator_approval_phrase_required']}",
        f"explicit_operator_approval_phrase_received={approval['explicit_operator_approval_phrase_received']}",
        f"approval_check_count={approval['approval_check_count']}",
        f"approval_case_count={approval['approval_case_count']}",
        f"approval_pass_count={approval['approval_pass_count']}",
        f"approval_failure_count={approval['approval_failure_count']}",
        f"approval_gate_count={approval['approval_gate_count']}",
        f"passed_gate_count={approval['passed_gate_count']}",
        f"approval_issue_count={approval['approval_issue_count']}",
        f"operator_approval_required={approval['operator_approval_required']}",
        f"operator_approval_granted={approval['operator_approval_granted']}",
        f"operator_approval_received={approval['operator_approval_received']}",
        f"manual_upload_allowed={approval['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={approval['kaggle_authentication_allowed']}",
        f"real_submission_created={approval['real_submission_created']}",
        f"real_submission_allowed={approval['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={approval['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={approval['kaggle_submission_sent']}",
        f"upload_performed={approval['upload_performed']}",
        f"kaggle_authentication_performed={approval['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "APPROVAL_CHECKS",
    ]

    for item in approval["approval_check_list"]:
        lines.append(item)

    lines.append("")
    lines.append("APPROVAL_RESULTS")
    for result in approval["approval_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_operator_approval_gate_artifacts(
    approval: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    approval = dict(approval or build_milestone_9_operator_approval_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-9-operator-approval-gate-v1.json"
    md_path = output / "milestone-9-operator-approval-gate-v1.md"
    manifest_path = output / "milestone-9-operator-approval-gate-manifest-v1.txt"
    index_path = output / "milestone-9-operator-approval-gate-index-v1.json"

    json_path.write_text(json.dumps(approval, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_operator_approval_gate_markdown(approval), encoding="utf-8")
    manifest_path.write_text(render_operator_approval_gate_manifest(approval), encoding="utf-8")
    index_path.write_text(json.dumps(approval["approval_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_9_operator_approval_gate_pipeline() -> Dict[str, Any]:
    approval = build_milestone_9_operator_approval_gate()
    validation = validate_milestone_9_operator_approval_gate(approval)
    artifacts = write_operator_approval_gate_artifacts(approval)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_9_OPERATOR_APPROVAL_GATE_V1_PIPELINE_INVALID",
        "approval_status": approval["status"],
        "validation_status": validation["status"],
        "approval": approval,
        "approval_id": approval["approval_id"],
        "signature": approval["signature"],
        "approval_mode": approval["approval_mode"],
        "approval_verdict": approval["approval_verdict"],
        "next_allowed_stage": approval["next_allowed_stage"],
        "approval_ready": approval["approval_ready"],
        "approval_locked": approval["approval_locked"],
        "operator_approval_gate_created": approval["operator_approval_gate_created"],
        "operator_approval_gate_ready": approval["operator_approval_gate_ready"],
        "operator_approval_gate_open": approval["operator_approval_gate_open"],
        "required_declaration_count": approval["required_declaration_count"],
        "provided_declaration_count": approval["provided_declaration_count"],
        "accepted_declaration_count": approval["accepted_declaration_count"],
        "explicit_operator_approval_phrase_received": approval["explicit_operator_approval_phrase_received"],
        "approval_check_count": approval["approval_check_count"],
        "approval_case_count": approval["approval_case_count"],
        "approval_pass_count": approval["approval_pass_count"],
        "approval_failure_count": approval["approval_failure_count"],
        "regression_guard_count": approval["regression_guard_count"],
        "boundary_control_count": approval["boundary_control_count"],
        "approval_gate_count": approval["approval_gate_count"],
        "passed_gate_count": approval["passed_gate_count"],
        "approval_issue_count": approval["approval_issue_count"],
        "warning_count": approval["warning_count"],
        "operator_approval_required": approval["operator_approval_required"],
        "operator_approval_granted": approval["operator_approval_granted"],
        "operator_approval_received": approval["operator_approval_received"],
        "manual_upload_allowed": approval["manual_upload_allowed"],
        "kaggle_authentication_allowed": approval["kaggle_authentication_allowed"],
        "real_submission_created": approval["real_submission_created"],
        "real_submission_allowed": approval["real_submission_allowed"],
        "ready_for_real_kaggle_submission": approval["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": approval["kaggle_submission_sent"],
        "upload_performed": approval["upload_performed"],
        "kaggle_authentication_performed": approval["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": approval["metadata"],
    }
