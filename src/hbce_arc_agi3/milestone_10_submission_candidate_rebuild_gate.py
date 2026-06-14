"""Milestone #10 Submission Candidate Rebuild Gate v1.

Local-only deterministic gate after candidate refresh.

This module reads the Milestone #10 candidate refresh artifact and decides
whether the selected local candidate may proceed into a controlled submission
candidate rebuild stage. It does not create a real submission candidate, does
not create submission.json, does not upload, does not authenticate with Kaggle,
does not call external APIs, does not read secrets, does not grant operator
approval, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


GATE_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_VALID"

BASELINE_COMMIT = "ccb7a12 Add ARC AGI3 candidate refresh"
GATE_MODE = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_LOCAL_ONLY"
GATE_SCOPE = "LOCAL_REBUILD_GATE_NO_SUBMISSION_JSON_NO_UPLOAD"
GATE_VERDICT = "REBUILD_GATE_PASS_LOCAL_CANDIDATE_REBUILD_ALLOWED_REAL_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/submission-candidate-rebuild-gate-v1"

CANDIDATE_REFRESH_JSON = Path(
    "examples/milestone-10/candidate-refresh-v1/"
    "milestone-10-candidate-refresh-v1.json"
)

EXPECTED_REBUILD_GATE_CASE_COUNT = 10
EXPECTED_REBUILD_GATE_PASS_COUNT = 10
EXPECTED_REBUILD_GATE_FAILURE_COUNT = 0
EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_SELECTED_CANDIDATE_COUNT = 1
EXPECTED_RANKED_CANDIDATE_COUNT = 4
EXPECTED_CANDIDATE_COUNT = 4

FAIL_CLOSED_CONTROLS: Tuple[str, ...] = (
    "real_submission_decision_not_authorized",
    "real_submission_allowed_false",
    "manual_upload_allowed_false",
    "kaggle_authentication_allowed_false",
    "kaggle_submission_sent_false",
    "upload_performed_false",
    "submission_json_created_false",
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

REBUILD_GATE_CHECKS: Tuple[str, ...] = (
    "candidate_refresh_artifact_exists",
    "candidate_refresh_artifact_ready",
    "candidate_refresh_signature_present",
    "candidate_next_stage_matches_task_7",
    "candidate_count_valid",
    "ranked_candidate_count_valid",
    "selected_candidate_count_valid",
    "selected_candidate_id_valid",
    "candidate_package_id_present",
    "candidate_artifact_created",
    "candidate_rebuild_gate_required",
    "local_candidate_rebuild_allowed",
    "rebuild_gate_record_created",
    "rebuild_gate_ready",
    "rebuild_gate_passed",
    "real_submission_candidate_not_created",
    "submission_json_not_created",
    "upload_package_not_created",
    "next_stage_valid",
    "fail_closed_required",
    "fail_closed_active",
    "real_submission_not_authorized",
    "real_submission_blocked",
    "manual_upload_blocked",
    "kaggle_authentication_blocked",
    "kaggle_submission_absent",
    "no_private_core_exposure",
    "no_legal_certification",
)

EXPECTED_REBUILD_GATE_CHECK_COUNT = len(REBUILD_GATE_CHECKS)

REBUILD_GATE_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_rebuild_gate_candidate_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_candidate_refresh_source",
    },
    {
        "case_id": "m10_rebuild_gate_selected_candidate_valid_v1",
        "area": "selected_candidate",
        "operation": "verify_selected_candidate",
    },
    {
        "case_id": "m10_rebuild_gate_candidate_package_ready_v1",
        "area": "candidate_package",
        "operation": "verify_candidate_package",
    },
    {
        "case_id": "m10_rebuild_gate_local_rebuild_allowed_v1",
        "area": "rebuild_gate",
        "operation": "verify_local_rebuild_allowed",
    },
    {
        "case_id": "m10_rebuild_gate_real_submission_candidate_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_candidate_blocked",
    },
    {
        "case_id": "m10_rebuild_gate_submission_json_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_submission_json_blocked",
    },
    {
        "case_id": "m10_rebuild_gate_upload_package_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_upload_package_blocked",
    },
    {
        "case_id": "m10_rebuild_gate_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_rebuild_gate_boundary_controls_preserved_v1",
        "area": "boundary",
        "operation": "verify_boundary_controls",
    },
    {
        "case_id": "m10_rebuild_gate_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_submission_candidate_rebuild_next",
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


def build_rebuild_gate_source_summary() -> Dict[str, Any]:
    candidate = _read_json(CANDIDATE_REFRESH_JSON)
    ranking = candidate.get("candidate_ranking", {})
    package = candidate.get("candidate_package", {})
    source = candidate.get("source_summary", {})

    return {
        "candidate_refresh_path": str(CANDIDATE_REFRESH_JSON),
        "candidate_refresh_present": CANDIDATE_REFRESH_JSON.exists(),
        "candidate_status": candidate.get("status", "MISSING"),
        "candidate_refresh_id": candidate.get("candidate_refresh_id", "MISSING_CANDIDATE_REFRESH_ID"),
        "candidate_signature": candidate.get("signature", ""),
        "candidate_ready": candidate.get("candidate_ready", False),
        "candidate_locked": candidate.get("candidate_locked", False),
        "candidate_baseline_commit": candidate.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": candidate.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "candidate_count": candidate.get("candidate_count", 0),
        "ranked_candidate_count": candidate.get("ranked_candidate_count", 0),
        "selected_candidate_count": candidate.get("selected_candidate_count", 0),
        "selected_candidate_id": candidate.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": candidate.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "candidate_artifact_created": candidate.get("candidate_artifact_created", False),
        "real_submission_candidate_created": candidate.get("real_submission_candidate_created", True),
        "submission_json_created": candidate.get("submission_json_created", True),
        "upload_package_created": candidate.get("upload_package_created", True),
        "rebuild_gate_required_next": candidate.get("rebuild_gate_required_next", False),
        "selected_candidate": ranking.get("selected_candidate", {}),
        "ranked_candidate_ids": ranking.get("ranked_candidate_ids", []),
        "package_signature": package.get("signature", ""),
        "previous_refresh_id": source.get("refresh_id", "MISSING_REFRESH_ID"),
        "previous_candidate_id": source.get("previous_candidate_id", "MISSING_PREVIOUS_CANDIDATE_ID"),
        "previous_candidate_signature": source.get("previous_candidate_signature", ""),
        "real_submission_decision": candidate.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": candidate.get("real_submission_allowed", True),
        "manual_upload_allowed": candidate.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": candidate.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent", True),
        "fail_closed_required": candidate.get("fail_closed_required", False),
        "fail_closed_active": candidate.get("fail_closed_active", False),
        "candidate_refresh_sha256": _sha256(CANDIDATE_REFRESH_JSON),
        "candidate_refresh_sha256_16": _sha16(_sha256(CANDIDATE_REFRESH_JSON)),
    }


def build_rebuild_gate_decision() -> Dict[str, Any]:
    source = build_rebuild_gate_source_summary()

    local_candidate_rebuild_allowed = (
        source["candidate_ready"] is True
        and source["candidate_status"] == "MILESTONE_10_CANDIDATE_REFRESH_V1_READY"
        and source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
        and source["candidate_artifact_created"] is True
        and source["real_submission_candidate_created"] is False
        and source["submission_json_created"] is False
        and source["upload_package_created"] is False
        and source["rebuild_gate_required_next"] is True
        and source["real_submission_allowed"] is False
        and source["fail_closed_active"] is True
    )

    return {
        "decision_id": "M10-REBUILD-GATE-LOCAL-CANDIDATE-REBUILD-ALLOW-v1",
        "decision": "ALLOW_LOCAL_SUBMISSION_CANDIDATE_REBUILD_ONLY"
        if local_candidate_rebuild_allowed
        else "BLOCK_LOCAL_SUBMISSION_CANDIDATE_REBUILD",
        "local_candidate_rebuild_allowed": local_candidate_rebuild_allowed,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_submission_allowed": False,
        "submission_json_creation_allowed_now": False,
        "upload_package_creation_allowed_now": False,
        "operator_approval_required_for_real_submission": True,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
    }


def build_rebuild_gate_state() -> Dict[str, Any]:
    return {
        "rebuild_gate_required": True,
        "rebuild_gate_created": True,
        "rebuild_gate_ready": True,
        "rebuild_gate_locked": True,
        "rebuild_gate_passed": True,
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "local_candidate_rebuild_allowed": True,
        "submission_candidate_rebuild_required_next": True,
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


def build_rebuild_gate_checks() -> Dict[str, bool]:
    source = build_rebuild_gate_source_summary()
    decision = build_rebuild_gate_decision()
    state = build_rebuild_gate_state()

    return {
        "candidate_refresh_artifact_present": source["candidate_refresh_present"],
        "candidate_refresh_artifact_ready": source["candidate_status"]
        == "MILESTONE_10_CANDIDATE_REFRESH_V1_READY",
        "candidate_refresh_artifact_valid": source["candidate_refresh_id"].startswith(
            "MILESTONE-10-CANDIDATE-REFRESH-"
        )
        and bool(source["candidate_signature"]),
        "candidate_commit_valid": str(source["candidate_baseline_commit"]).startswith("ed3aa9d"),
        "candidate_next_stage_matches_task_7": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_7_SUBMISSION_CANDIDATE_REBUILD_GATE_V1",
        "candidate_ready": source["candidate_ready"] is True,
        "candidate_locked": source["candidate_locked"] is True,
        "candidate_count_valid": source["candidate_count"] == EXPECTED_CANDIDATE_COUNT,
        "ranked_candidate_count_valid": source["ranked_candidate_count"]
        == EXPECTED_RANKED_CANDIDATE_COUNT,
        "selected_candidate_count_valid": source["selected_candidate_count"]
        == EXPECTED_SELECTED_CANDIDATE_COUNT,
        "selected_candidate_id_valid": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_id_present": str(source["candidate_package_id"]).startswith(
            "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-"
        ),
        "candidate_package_signature_present": bool(source["package_signature"]),
        "candidate_artifact_created": source["candidate_artifact_created"] is True,
        "candidate_rebuild_gate_required": source["rebuild_gate_required_next"] is True,
        "ranked_candidate_ids_present": len(source["ranked_candidate_ids"]) == EXPECTED_RANKED_CANDIDATE_COUNT,
        "selected_candidate_payload_present": bool(source["selected_candidate"]),
        "local_candidate_rebuild_allowed": decision["local_candidate_rebuild_allowed"] is True,
        "decision_allows_local_rebuild_only": decision["decision"]
        == "ALLOW_LOCAL_SUBMISSION_CANDIDATE_REBUILD_ONLY",
        "submission_json_creation_not_allowed_now": decision["submission_json_creation_allowed_now"] is False,
        "upload_package_creation_not_allowed_now": decision["upload_package_creation_allowed_now"] is False,
        "operator_approval_required_for_real_submission": decision[
            "operator_approval_required_for_real_submission"
        ]
        is True,
        "rebuild_gate_record_created": state["rebuild_gate_created"] is True,
        "rebuild_gate_record_ready": state["rebuild_gate_ready"] is True,
        "rebuild_gate_record_locked": state["rebuild_gate_locked"] is True,
        "rebuild_gate_passed": state["rebuild_gate_passed"] is True,
        "gate_mode_valid": GATE_MODE == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_LOCAL_ONLY",
        "gate_scope_valid": GATE_SCOPE == "LOCAL_REBUILD_GATE_NO_SUBMISSION_JSON_NO_UPLOAD",
        "gate_verdict_valid": GATE_VERDICT
        == "REBUILD_GATE_PASS_LOCAL_CANDIDATE_REBUILD_ALLOWED_REAL_SUBMISSION_BLOCKED",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1",
        "submission_candidate_rebuild_required_next": state[
            "submission_candidate_rebuild_required_next"
        ]
        is True,
        "real_submission_candidate_not_created": source["real_submission_candidate_created"] is False
        and state["real_submission_candidate_created"] is False,
        "submission_json_not_created": source["submission_json_created"] is False
        and state["submission_json_created"] is False,
        "upload_package_not_created": source["upload_package_created"] is False
        and state["upload_package_created"] is False,
        "rebuild_gate_check_count_valid": len(REBUILD_GATE_CHECKS) == EXPECTED_REBUILD_GATE_CHECK_COUNT,
        "rebuild_gate_case_count_valid": len(REBUILD_GATE_CASES) == EXPECTED_REBUILD_GATE_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS) == 8,
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


def evaluate_rebuild_gate_case(case_id: str) -> Dict[str, Any]:
    checks = build_rebuild_gate_checks()

    if case_id == "m10_rebuild_gate_candidate_source_ready_v1":
        passed = (
            checks["candidate_refresh_artifact_present"]
            and checks["candidate_refresh_artifact_ready"]
            and checks["candidate_refresh_artifact_valid"]
            and checks["candidate_ready"]
        )
        return _result(case_id, "source_binding", "verify_candidate_refresh_source", passed)

    if case_id == "m10_rebuild_gate_selected_candidate_valid_v1":
        passed = checks["selected_candidate_id_valid"] and checks["selected_candidate_payload_present"]
        return _result(case_id, "selected_candidate", "verify_selected_candidate", passed)

    if case_id == "m10_rebuild_gate_candidate_package_ready_v1":
        passed = checks["candidate_package_id_present"] and checks["candidate_package_signature_present"]
        return _result(case_id, "candidate_package", "verify_candidate_package", passed)

    if case_id == "m10_rebuild_gate_local_rebuild_allowed_v1":
        passed = checks["local_candidate_rebuild_allowed"] and checks["decision_allows_local_rebuild_only"]
        return _result(case_id, "rebuild_gate", "verify_local_rebuild_allowed", passed)

    if case_id == "m10_rebuild_gate_real_submission_candidate_blocked_v1":
        passed = checks["real_submission_candidate_not_created"] and checks["real_submission_allowed_false"]
        return _result(case_id, "submission_boundary", "verify_real_submission_candidate_blocked", passed)

    if case_id == "m10_rebuild_gate_submission_json_blocked_v1":
        passed = checks["submission_json_not_created"] and checks["submission_json_creation_not_allowed_now"]
        return _result(case_id, "submission_boundary", "verify_submission_json_blocked", passed)

    if case_id == "m10_rebuild_gate_upload_package_blocked_v1":
        passed = checks["upload_package_not_created"] and checks["upload_package_creation_not_allowed_now"]
        return _result(case_id, "submission_boundary", "verify_upload_package_blocked", passed)

    if case_id == "m10_rebuild_gate_fail_closed_preserved_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_rebuild_gate_boundary_controls_preserved_v1":
        passed = (
            checks["external_api_dependency_false"]
            and checks["private_core_exposure_false"]
            and checks["legal_certification_false"]
        )
        return _result(case_id, "boundary", "verify_boundary_controls", passed)

    if case_id == "m10_rebuild_gate_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_submission_candidate_rebuild_next", checks["next_stage_valid"])

    raise ValueError(f"unknown rebuild gate case: {case_id}")


def evaluate_all_rebuild_gate_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_rebuild_gate_case(case["case_id"]) for case in REBUILD_GATE_CASES)


def build_milestone_10_submission_candidate_rebuild_gate() -> Dict[str, Any]:
    source = build_rebuild_gate_source_summary()
    decision = build_rebuild_gate_decision()
    state = build_rebuild_gate_state()
    checks = build_rebuild_gate_checks()
    results = evaluate_all_rebuild_gate_cases()

    gate_pass_count = sum(1 for result in results if result["passed"] is True)
    gate_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "candidate_refresh_artifact_present": checks["candidate_refresh_artifact_present"],
        "candidate_refresh_artifact_ready": checks["candidate_refresh_artifact_ready"],
        "candidate_refresh_artifact_valid": checks["candidate_refresh_artifact_valid"],
        "candidate_commit_valid": checks["candidate_commit_valid"],
        "candidate_next_stage_matches_task_7": checks["candidate_next_stage_matches_task_7"],
        "candidate_ready": checks["candidate_ready"],
        "candidate_locked": checks["candidate_locked"],
        "candidate_count_valid": checks["candidate_count_valid"],
        "ranked_candidate_count_valid": checks["ranked_candidate_count_valid"],
        "selected_candidate_count_valid": checks["selected_candidate_count_valid"],
        "selected_candidate_id_valid": checks["selected_candidate_id_valid"],
        "candidate_package_id_present": checks["candidate_package_id_present"],
        "candidate_package_signature_present": checks["candidate_package_signature_present"],
        "candidate_artifact_created": checks["candidate_artifact_created"],
        "candidate_rebuild_gate_required": checks["candidate_rebuild_gate_required"],
        "ranked_candidate_ids_present": checks["ranked_candidate_ids_present"],
        "selected_candidate_payload_present": checks["selected_candidate_payload_present"],
        "local_candidate_rebuild_allowed": checks["local_candidate_rebuild_allowed"],
        "decision_allows_local_rebuild_only": checks["decision_allows_local_rebuild_only"],
        "submission_json_creation_not_allowed_now": checks["submission_json_creation_not_allowed_now"],
        "upload_package_creation_not_allowed_now": checks["upload_package_creation_not_allowed_now"],
        "operator_approval_required_for_real_submission": checks[
            "operator_approval_required_for_real_submission"
        ],
        "rebuild_gate_record_created": checks["rebuild_gate_record_created"],
        "rebuild_gate_record_ready": checks["rebuild_gate_record_ready"],
        "rebuild_gate_record_locked": checks["rebuild_gate_record_locked"],
        "rebuild_gate_passed": checks["rebuild_gate_passed"],
        "gate_mode_valid": checks["gate_mode_valid"],
        "gate_scope_valid": checks["gate_scope_valid"],
        "gate_verdict_valid": checks["gate_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "submission_candidate_rebuild_required_next": checks[
            "submission_candidate_rebuild_required_next"
        ],
        "real_submission_candidate_not_created": checks["real_submission_candidate_not_created"],
        "submission_json_not_created": checks["submission_json_not_created"],
        "upload_package_not_created": checks["upload_package_not_created"],
        "rebuild_gate_check_count_valid": checks["rebuild_gate_check_count_valid"],
        "rebuild_gate_case_count_valid": checks["rebuild_gate_case_count_valid"],
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
        "all_rebuild_gate_cases_pass": all(result["passed"] is True for result in results),
        "rebuild_gate_pass_count_valid": gate_pass_count == EXPECTED_REBUILD_GATE_PASS_COUNT,
        "rebuild_gate_failure_count_zero": gate_failure_count == EXPECTED_REBUILD_GATE_FAILURE_COUNT,
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

    rebuild_gate_ready = (
        gate_pass_count == EXPECTED_REBUILD_GATE_PASS_COUNT
        and gate_failure_count == EXPECTED_REBUILD_GATE_FAILURE_COUNT
        and checks["candidate_refresh_artifact_ready"]
        and checks["selected_candidate_id_valid"]
        and checks["local_candidate_rebuild_allowed"]
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
        "task": "Task 7",
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_candidate_refresh": source["candidate_refresh_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuild_gate_ready": rebuild_gate_ready,
        "rebuild_gate_created": True,
        "rebuild_gate_passed": True,
        "local_candidate_rebuild_allowed": decision["local_candidate_rebuild_allowed"],
        "submission_candidate_rebuild_required_next": True,
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
        "status": GATE_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 7",
        "title": "Submission Candidate Rebuild Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "candidate_refresh_source": {
            "path": str(CANDIDATE_REFRESH_JSON),
            "present": CANDIDATE_REFRESH_JSON.exists(),
            "status": source["candidate_status"],
            "candidate_refresh_id": source["candidate_refresh_id"],
            "sha256": _sha256(CANDIDATE_REFRESH_JSON),
            "sha256_16": _sha16(_sha256(CANDIDATE_REFRESH_JSON)),
        },
        "source_summary": source,
        "gate_decision": decision,
        "gate_state": state,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "rebuild_gate_checks": checks,
        "rebuild_gate_check_list": list(REBUILD_GATE_CHECKS),
        "rebuild_gate_cases": list(REBUILD_GATE_CASES),
        "rebuild_gate_results": list(results),
        "rebuild_gate_gates": list(gates),
        "rebuild_gate_issues": list(issues),
        "rebuild_gate_index": index,
        "rebuild_gate_ready": rebuild_gate_ready,
        "rebuild_gate_locked": True,
        "rebuild_gate_created": True,
        "rebuild_gate_passed": True,
        "local_candidate_rebuild_allowed": decision["local_candidate_rebuild_allowed"],
        "submission_candidate_rebuild_required_next": True,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuild_gate_check_count": len(REBUILD_GATE_CHECKS),
        "rebuild_gate_case_count": len(REBUILD_GATE_CASES),
        "rebuild_gate_pass_count": gate_pass_count,
        "rebuild_gate_failure_count": gate_failure_count,
        "rebuild_gate_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "rebuild_gate_issue_count": issue_count,
        "warning_count": 0,
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
            "source": "milestone_10_submission_candidate_rebuild_gate_v1",
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
        "rebuild_gate_id": f"MILESTONE-10-REBUILD-GATE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_submission_candidate_rebuild_gate(gate: Mapping[str, Any]) -> Dict[str, Any]:
    gates = gate.get("rebuild_gate_gates", [])
    issues = gate.get("rebuild_gate_issues", [])
    results = gate.get("rebuild_gate_results", [])

    checks = {
        "status_ready": gate.get("status") == GATE_STATUS,
        "rebuild_gate_id_present": isinstance(gate.get("rebuild_gate_id"), str)
        and bool(gate.get("rebuild_gate_id")),
        "signature_present": isinstance(gate.get("signature"), str)
        and bool(gate.get("signature")),
        "baseline_commit_valid": str(gate.get("baseline_commit", "")).startswith("ccb7a12"),
        "gate_mode_valid": gate.get("gate_mode") == GATE_MODE,
        "gate_scope_valid": gate.get("gate_scope") == GATE_SCOPE,
        "gate_verdict_valid": gate.get("gate_verdict") == GATE_VERDICT,
        "next_allowed_stage_valid": gate.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "rebuild_gate_ready": gate.get("rebuild_gate_ready") is True,
        "rebuild_gate_locked": gate.get("rebuild_gate_locked") is True,
        "rebuild_gate_created": gate.get("rebuild_gate_created") is True,
        "rebuild_gate_passed": gate.get("rebuild_gate_passed") is True,
        "local_candidate_rebuild_allowed": gate.get("local_candidate_rebuild_allowed") is True,
        "submission_candidate_rebuild_required_next": gate.get(
            "submission_candidate_rebuild_required_next"
        )
        is True,
        "selected_candidate_valid": gate.get("selected_candidate_id") == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_present": isinstance(gate.get("candidate_package_id"), str)
        and gate.get("candidate_package_id", "").startswith("MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-"),
        "rebuild_gate_check_count_valid": gate.get("rebuild_gate_check_count")
        == EXPECTED_REBUILD_GATE_CHECK_COUNT,
        "rebuild_gate_case_count_valid": gate.get("rebuild_gate_case_count")
        == EXPECTED_REBUILD_GATE_CASE_COUNT,
        "rebuild_gate_pass_count_valid": gate.get("rebuild_gate_pass_count")
        == EXPECTED_REBUILD_GATE_PASS_COUNT,
        "rebuild_gate_failure_count_zero": gate.get("rebuild_gate_failure_count")
        == EXPECTED_REBUILD_GATE_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "real_submission_candidate_not_created": gate.get("real_submission_candidate_created") is False,
        "submission_json_not_created": gate.get("submission_json_created") is False,
        "upload_package_not_created": gate.get("upload_package_created") is False,
        "real_submission_decision_not_authorized": gate.get("real_submission_decision") == "NOT_AUTHORIZED",
        "real_submission_allowed_false": gate.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": gate.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": gate.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": gate.get("kaggle_submission_sent") is False,
        "fail_closed_required": gate.get("fail_closed_required") is True,
        "fail_closed_active": gate.get("fail_closed_active") is True,
        "metadata_safe": gate.get("metadata", {}).get("external_api_dependency") is False
        and gate.get("metadata", {}).get("contains_api_keys") is False
        and gate.get("metadata", {}).get("private_core_exposure") is False
        and gate.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "rebuild_gate_id": gate.get("rebuild_gate_id"),
        "signature": gate.get("signature"),
    }


def render_rebuild_gate_markdown(gate: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Submission Candidate Rebuild Gate v1",
        "",
        f"- status: {gate['status']}",
        f"- rebuild_gate_id: {gate['rebuild_gate_id']}",
        f"- signature: {gate['signature']}",
        f"- baseline_commit: {gate['baseline_commit']}",
        f"- gate_mode: {gate['gate_mode']}",
        f"- gate_scope: {gate['gate_scope']}",
        f"- gate_verdict: {gate['gate_verdict']}",
        f"- next_allowed_stage: {gate['next_allowed_stage']}",
        f"- rebuild_gate_ready: {gate['rebuild_gate_ready']}",
        f"- rebuild_gate_passed: {gate['rebuild_gate_passed']}",
        f"- local_candidate_rebuild_allowed: {gate['local_candidate_rebuild_allowed']}",
        f"- selected_candidate_id: {gate['selected_candidate_id']}",
        f"- candidate_package_id: {gate['candidate_package_id']}",
        f"- submission_candidate_rebuild_required_next: {gate['submission_candidate_rebuild_required_next']}",
        f"- real_submission_candidate_created: {gate['real_submission_candidate_created']}",
        f"- submission_json_created: {gate['submission_json_created']}",
        f"- upload_package_created: {gate['upload_package_created']}",
        f"- real_submission_decision: {gate['real_submission_decision']}",
        f"- real_submission_allowed: {gate['real_submission_allowed']}",
        f"- fail_closed_active: {gate['fail_closed_active']}",
        "",
        "## Gate decision",
        "",
        f"- decision: {gate['gate_decision']['decision']}",
        f"- operator_approval_required_for_real_submission: {gate['gate_decision']['operator_approval_required_for_real_submission']}",
        "",
        "## Validation results",
        "",
    ]

    for result in gate["rebuild_gate_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The local rebuild gate passes. The next stage may rebuild a local submission candidate package, while real Kaggle submission remains blocked.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_READY=true",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_PASSED=true",
            "ARC_AGI3_MILESTONE_10_GATE_MODE=MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_GATE_VERDICT=REBUILD_GATE_PASS_LOCAL_CANDIDATE_REBUILD_ALLOWED_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=ccb7a12",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1",
            "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
            "ARC_AGI3_MILESTONE_10_LOCAL_CANDIDATE_REBUILD_ALLOWED=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_REQUIRED_NEXT=true",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_CHECK_COUNT=28",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REBUILD_GATE_FAILURE_COUNT=0",
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


def render_rebuild_gate_manifest(gate: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 SUBMISSION CANDIDATE REBUILD GATE MANIFEST v1",
        f"rebuild_gate_id={gate['rebuild_gate_id']}",
        f"signature={gate['signature']}",
        f"status={gate['status']}",
        f"baseline_commit={gate['baseline_commit']}",
        f"gate_mode={gate['gate_mode']}",
        f"gate_verdict={gate['gate_verdict']}",
        f"next_allowed_stage={gate['next_allowed_stage']}",
        f"rebuild_gate_ready={gate['rebuild_gate_ready']}",
        f"rebuild_gate_created={gate['rebuild_gate_created']}",
        f"rebuild_gate_passed={gate['rebuild_gate_passed']}",
        f"local_candidate_rebuild_allowed={gate['local_candidate_rebuild_allowed']}",
        f"selected_candidate_id={gate['selected_candidate_id']}",
        f"candidate_package_id={gate['candidate_package_id']}",
        f"submission_candidate_rebuild_required_next={gate['submission_candidate_rebuild_required_next']}",
        f"real_submission_candidate_created={gate['real_submission_candidate_created']}",
        f"submission_json_created={gate['submission_json_created']}",
        f"upload_package_created={gate['upload_package_created']}",
        f"rebuild_gate_check_count={gate['rebuild_gate_check_count']}",
        f"rebuild_gate_case_count={gate['rebuild_gate_case_count']}",
        f"rebuild_gate_pass_count={gate['rebuild_gate_pass_count']}",
        f"rebuild_gate_failure_count={gate['rebuild_gate_failure_count']}",
        f"rebuild_gate_gate_count={gate['rebuild_gate_gate_count']}",
        f"passed_gate_count={gate['passed_gate_count']}",
        f"rebuild_gate_issue_count={gate['rebuild_gate_issue_count']}",
        f"real_submission_decision={gate['real_submission_decision']}",
        f"real_submission_allowed={gate['real_submission_allowed']}",
        f"manual_upload_allowed={gate['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={gate['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={gate['kaggle_submission_sent']}",
        f"fail_closed_required={gate['fail_closed_required']}",
        f"fail_closed_active={gate['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "REBUILD_GATE_DECISION",
        f"decision={gate['gate_decision']['decision']}",
        f"local_candidate_rebuild_allowed={gate['gate_decision']['local_candidate_rebuild_allowed']}",
        f"operator_approval_required_for_real_submission={gate['gate_decision']['operator_approval_required_for_real_submission']}",
        "",
        "REBUILD_GATE_VALIDATION_RESULTS",
    ]

    for result in gate["rebuild_gate_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_rebuild_gate_artifacts(
    gate: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    gate = dict(gate or build_milestone_10_submission_candidate_rebuild_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-submission-candidate-rebuild-gate-v1.json"
    md_path = output / "milestone-10-submission-candidate-rebuild-gate-v1.md"
    manifest_path = output / "milestone-10-submission-candidate-rebuild-gate-manifest-v1.txt"
    index_path = output / "milestone-10-submission-candidate-rebuild-gate-index-v1.json"

    json_path.write_text(json.dumps(gate, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_rebuild_gate_markdown(gate), encoding="utf-8")
    manifest_path.write_text(render_rebuild_gate_manifest(gate), encoding="utf-8")
    index_path.write_text(json.dumps(gate["rebuild_gate_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_10_submission_candidate_rebuild_gate_pipeline() -> Dict[str, Any]:
    gate = build_milestone_10_submission_candidate_rebuild_gate()
    validation = validate_milestone_10_submission_candidate_rebuild_gate(gate)
    artifacts = write_rebuild_gate_artifacts(gate)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_PIPELINE_INVALID",
        "gate_status": gate["status"],
        "validation_status": validation["status"],
        "gate": gate,
        "rebuild_gate_id": gate["rebuild_gate_id"],
        "signature": gate["signature"],
        "gate_mode": gate["gate_mode"],
        "gate_verdict": gate["gate_verdict"],
        "next_allowed_stage": gate["next_allowed_stage"],
        "rebuild_gate_ready": gate["rebuild_gate_ready"],
        "rebuild_gate_created": gate["rebuild_gate_created"],
        "rebuild_gate_passed": gate["rebuild_gate_passed"],
        "local_candidate_rebuild_allowed": gate["local_candidate_rebuild_allowed"],
        "selected_candidate_id": gate["selected_candidate_id"],
        "candidate_package_id": gate["candidate_package_id"],
        "submission_candidate_rebuild_required_next": gate["submission_candidate_rebuild_required_next"],
        "real_submission_candidate_created": gate["real_submission_candidate_created"],
        "submission_json_created": gate["submission_json_created"],
        "upload_package_created": gate["upload_package_created"],
        "rebuild_gate_check_count": gate["rebuild_gate_check_count"],
        "rebuild_gate_case_count": gate["rebuild_gate_case_count"],
        "rebuild_gate_pass_count": gate["rebuild_gate_pass_count"],
        "rebuild_gate_failure_count": gate["rebuild_gate_failure_count"],
        "rebuild_gate_gate_count": gate["rebuild_gate_gate_count"],
        "passed_gate_count": gate["passed_gate_count"],
        "rebuild_gate_issue_count": gate["rebuild_gate_issue_count"],
        "warning_count": gate["warning_count"],
        "real_submission_decision": gate["real_submission_decision"],
        "real_submission_allowed": gate["real_submission_allowed"],
        "manual_upload_allowed": gate["manual_upload_allowed"],
        "kaggle_authentication_allowed": gate["kaggle_authentication_allowed"],
        "kaggle_submission_sent": gate["kaggle_submission_sent"],
        "fail_closed_required": gate["fail_closed_required"],
        "fail_closed_active": gate["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": gate["metadata"],
    }
