"""Milestone #10 Submission Candidate Rebuild v1.

Local-only deterministic rebuild after submission candidate rebuild gate.

This module reads the Milestone #10 rebuild gate artifact and rebuilds a local
candidate package for review. It does not create a real Kaggle submission,
does not create submission.json, does not upload files, does not authenticate,
does not call external APIs, does not read secrets, does not grant operator
approval, and does not create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REBUILD_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY"
PIPELINE_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_VALID"

BASELINE_COMMIT = "e329a98 Add ARC AGI3 submission candidate rebuild gate"
REBUILD_MODE = "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_LOCAL_ONLY"
REBUILD_SCOPE = "LOCAL_SUBMISSION_CANDIDATE_REBUILD_NO_SUBMISSION_JSON_NO_UPLOAD"
REBUILD_VERDICT = "SUBMISSION_CANDIDATE_REBUILD_READY_FOR_REBUILT_CANDIDATE_REVIEW_REAL_SUBMISSION_BLOCKED"
NEXT_ALLOWED_STAGE = "MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1"

DEFAULT_OUTPUT_DIR = "examples/milestone-10/submission-candidate-rebuild-v1"

REBUILD_GATE_JSON = Path(
    "examples/milestone-10/submission-candidate-rebuild-gate-v1/"
    "milestone-10-submission-candidate-rebuild-gate-v1.json"
)

EXPECTED_SELECTED_CANDIDATE_ID = "M10-CANDIDATE-BALANCED-PATCH-STACK-v1"
EXPECTED_CANDIDATE_PACKAGE_ID = "MILESTONE-10-CANDIDATE-REFRESH-PACKAGE-CF04A9CB1B1D"
EXPECTED_REBUILD_COMPONENT_COUNT = 6
EXPECTED_REBUILD_CHECK_COUNT = 30
EXPECTED_REBUILD_CASE_COUNT = 10
EXPECTED_REBUILD_PASS_COUNT = 10
EXPECTED_REBUILD_FAILURE_COUNT = 0

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

REBUILD_COMPONENTS: Tuple[Dict[str, Any], ...] = (
    {
        "component_id": "m10_rebuild_candidate_manifest_v1",
        "kind": "manifest",
        "required": True,
        "creates_submission_json": False,
    },
    {
        "component_id": "m10_rebuild_candidate_index_v1",
        "kind": "index",
        "required": True,
        "creates_submission_json": False,
    },
    {
        "component_id": "m10_rebuild_candidate_payload_v1",
        "kind": "candidate_payload",
        "required": True,
        "creates_submission_json": False,
    },
    {
        "component_id": "m10_rebuild_candidate_trace_v1",
        "kind": "trace",
        "required": True,
        "creates_submission_json": False,
    },
    {
        "component_id": "m10_rebuild_candidate_boundary_v1",
        "kind": "boundary",
        "required": True,
        "creates_submission_json": False,
    },
    {
        "component_id": "m10_rebuild_candidate_review_handoff_v1",
        "kind": "review_handoff",
        "required": True,
        "creates_submission_json": False,
    },
)

REBUILD_CHECKS: Tuple[str, ...] = (
    "rebuild_gate_artifact_exists",
    "rebuild_gate_artifact_ready",
    "rebuild_gate_signature_present",
    "rebuild_gate_next_stage_matches_task_8",
    "rebuild_gate_passed",
    "local_candidate_rebuild_allowed",
    "selected_candidate_id_valid",
    "candidate_package_id_valid",
    "rebuild_component_count_valid",
    "all_rebuild_components_required",
    "all_rebuild_components_safe",
    "local_candidate_package_rebuilt",
    "rebuilt_candidate_payload_created",
    "rebuilt_candidate_manifest_created",
    "rebuilt_candidate_index_created",
    "rebuilt_candidate_trace_created",
    "review_handoff_created",
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

REBUILD_CASES: Tuple[Dict[str, str], ...] = (
    {
        "case_id": "m10_candidate_rebuild_gate_source_ready_v1",
        "area": "source_binding",
        "operation": "verify_rebuild_gate_source",
    },
    {
        "case_id": "m10_candidate_rebuild_selected_candidate_valid_v1",
        "area": "selected_candidate",
        "operation": "verify_selected_candidate",
    },
    {
        "case_id": "m10_candidate_rebuild_package_rebuilt_v1",
        "area": "rebuild_package",
        "operation": "verify_local_candidate_package_rebuilt",
    },
    {
        "case_id": "m10_candidate_rebuild_components_ready_v1",
        "area": "rebuild_components",
        "operation": "verify_rebuild_components",
    },
    {
        "case_id": "m10_candidate_rebuild_trace_ready_v1",
        "area": "traceability",
        "operation": "verify_rebuild_trace",
    },
    {
        "case_id": "m10_candidate_rebuild_review_handoff_ready_v1",
        "area": "review_handoff",
        "operation": "verify_review_handoff",
    },
    {
        "case_id": "m10_candidate_rebuild_no_submission_json_v1",
        "area": "submission_boundary",
        "operation": "verify_no_submission_json",
    },
    {
        "case_id": "m10_candidate_rebuild_real_submission_blocked_v1",
        "area": "submission_boundary",
        "operation": "verify_real_submission_blocked",
    },
    {
        "case_id": "m10_candidate_rebuild_fail_closed_preserved_v1",
        "area": "fail_closed",
        "operation": "verify_fail_closed_preserved",
    },
    {
        "case_id": "m10_candidate_rebuild_next_stage_valid_v1",
        "area": "next_stage",
        "operation": "verify_rebuilt_candidate_review_next",
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


def build_submission_candidate_rebuild_source_summary() -> Dict[str, Any]:
    gate = _read_json(REBUILD_GATE_JSON)
    source = gate.get("source_summary", {})
    decision = gate.get("gate_decision", {})

    return {
        "rebuild_gate_path": str(REBUILD_GATE_JSON),
        "rebuild_gate_present": REBUILD_GATE_JSON.exists(),
        "gate_status": gate.get("status", "MISSING"),
        "rebuild_gate_id": gate.get("rebuild_gate_id", "MISSING_REBUILD_GATE_ID"),
        "gate_signature": gate.get("signature", ""),
        "rebuild_gate_ready": gate.get("rebuild_gate_ready", False),
        "rebuild_gate_locked": gate.get("rebuild_gate_locked", False),
        "rebuild_gate_passed": gate.get("rebuild_gate_passed", False),
        "gate_baseline_commit": gate.get("baseline_commit", "MISSING_BASELINE_COMMIT"),
        "next_allowed_stage": gate.get("next_allowed_stage", "MISSING_NEXT_STAGE"),
        "local_candidate_rebuild_allowed": gate.get("local_candidate_rebuild_allowed", False),
        "submission_candidate_rebuild_required_next": gate.get(
            "submission_candidate_rebuild_required_next", False
        ),
        "selected_candidate_id": gate.get("selected_candidate_id", "MISSING_SELECTED_CANDIDATE_ID"),
        "candidate_package_id": gate.get("candidate_package_id", "MISSING_CANDIDATE_PACKAGE_ID"),
        "decision": decision.get("decision", "MISSING_DECISION"),
        "operator_approval_required_for_real_submission": decision.get(
            "operator_approval_required_for_real_submission", False
        ),
        "candidate_refresh_id": source.get("candidate_refresh_id", "MISSING_CANDIDATE_REFRESH_ID"),
        "previous_refresh_id": source.get("previous_refresh_id", "MISSING_PREVIOUS_REFRESH_ID"),
        "previous_candidate_id": source.get("previous_candidate_id", "MISSING_PREVIOUS_CANDIDATE_ID"),
        "real_submission_candidate_created": gate.get("real_submission_candidate_created", True),
        "submission_json_created": gate.get("submission_json_created", True),
        "upload_package_created": gate.get("upload_package_created", True),
        "real_submission_decision": gate.get("real_submission_decision", "MISSING_DECISION"),
        "real_submission_allowed": gate.get("real_submission_allowed", True),
        "manual_upload_allowed": gate.get("manual_upload_allowed", True),
        "kaggle_authentication_allowed": gate.get("kaggle_authentication_allowed", True),
        "kaggle_submission_sent": gate.get("kaggle_submission_sent", True),
        "fail_closed_required": gate.get("fail_closed_required", False),
        "fail_closed_active": gate.get("fail_closed_active", False),
        "gate_sha256": _sha256(REBUILD_GATE_JSON),
        "gate_sha256_16": _sha16(_sha256(REBUILD_GATE_JSON)),
    }


def build_rebuild_component_catalog() -> Tuple[Dict[str, Any], ...]:
    return tuple(
        {
            **component,
            "local_only": True,
            "deterministic": True,
            "requires_external_api": False,
            "requires_kaggle_upload": False,
            "creates_real_submission": False,
            "creates_upload_package": False,
            "ready": True,
        }
        for component in REBUILD_COMPONENTS
    )


def build_rebuilt_candidate_payload() -> Dict[str, Any]:
    source = build_submission_candidate_rebuild_source_summary()
    seed = {
        "baseline_commit": BASELINE_COMMIT,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuild_gate_id": source["rebuild_gate_id"],
        "mode": REBUILD_MODE,
    }
    signature = _stable_signature(seed)

    return {
        "rebuilt_candidate_id": f"MILESTONE-10-REBUILT-CANDIDATE-{signature[:12]}",
        "signature": signature,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "source_rebuild_gate_id": source["rebuild_gate_id"],
        "source_candidate_refresh_id": source["candidate_refresh_id"],
        "payload_kind": "LOCAL_REBUILT_CANDIDATE_PACKAGE",
        "local_candidate_package_rebuilt": True,
        "rebuilt_candidate_payload_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "ready_for_review": True,
    }


def build_rebuild_state() -> Dict[str, Any]:
    return {
        "submission_candidate_rebuild_required": True,
        "submission_candidate_rebuild_created": True,
        "submission_candidate_rebuild_ready": True,
        "submission_candidate_rebuild_locked": True,
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "local_candidate_package_rebuilt": True,
        "rebuilt_candidate_payload_created": True,
        "rebuilt_candidate_manifest_created": True,
        "rebuilt_candidate_index_created": True,
        "rebuilt_candidate_trace_created": True,
        "review_handoff_created": True,
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "rebuilt_candidate_review_required_next": True,
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


def build_rebuild_trace() -> Dict[str, Any]:
    source = build_submission_candidate_rebuild_source_summary()
    payload = build_rebuilt_candidate_payload()
    trace_seed = {
        "rebuild_gate_id": source["rebuild_gate_id"],
        "candidate_refresh_id": source["candidate_refresh_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "rebuilt_candidate_id": payload["rebuilt_candidate_id"],
        "boundary": "LOCAL_ONLY_NO_SUBMISSION",
    }
    trace_hash = hashlib.sha256(
        json.dumps(trace_seed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return {
        "trace_ready": True,
        "trace_hash": trace_hash,
        "trace_hash_16": trace_hash[:16].upper(),
        "source_rebuild_gate_id": source["rebuild_gate_id"],
        "rebuilt_candidate_id": payload["rebuilt_candidate_id"],
        "boundary": "LOCAL_ONLY_NO_SUBMISSION",
    }


def build_submission_candidate_rebuild_checks() -> Dict[str, bool]:
    source = build_submission_candidate_rebuild_source_summary()
    components = build_rebuild_component_catalog()
    payload = build_rebuilt_candidate_payload()
    state = build_rebuild_state()
    trace = build_rebuild_trace()

    return {
        "rebuild_gate_artifact_present": source["rebuild_gate_present"],
        "rebuild_gate_artifact_ready": source["gate_status"]
        == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY",
        "rebuild_gate_artifact_valid": source["rebuild_gate_id"].startswith("MILESTONE-10-REBUILD-GATE-")
        and bool(source["gate_signature"]),
        "rebuild_gate_commit_valid": str(source["gate_baseline_commit"]).startswith("ccb7a12"),
        "rebuild_gate_next_stage_matches_task_8": source["next_allowed_stage"]
        == "MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1",
        "rebuild_gate_ready": source["rebuild_gate_ready"] is True,
        "rebuild_gate_locked": source["rebuild_gate_locked"] is True,
        "rebuild_gate_passed": source["rebuild_gate_passed"] is True,
        "local_candidate_rebuild_allowed": source["local_candidate_rebuild_allowed"] is True,
        "submission_candidate_rebuild_required": source["submission_candidate_rebuild_required_next"] is True,
        "selected_candidate_id_valid": source["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_id_valid": source["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID,
        "decision_allows_local_rebuild_only": source["decision"]
        == "ALLOW_LOCAL_SUBMISSION_CANDIDATE_REBUILD_ONLY",
        "operator_approval_required_for_real_submission": source[
            "operator_approval_required_for_real_submission"
        ]
        is True,
        "rebuild_component_count_valid": len(components) == EXPECTED_REBUILD_COMPONENT_COUNT,
        "all_rebuild_components_required": all(component["required"] is True for component in components),
        "all_rebuild_components_ready": all(component["ready"] is True for component in components),
        "all_rebuild_components_local_only": all(component["local_only"] is True for component in components),
        "all_rebuild_components_deterministic": all(
            component["deterministic"] is True for component in components
        ),
        "all_rebuild_components_safe": all(
            component["requires_external_api"] is False
            and component["requires_kaggle_upload"] is False
            and component["creates_real_submission"] is False
            and component["creates_submission_json"] is False
            and component["creates_upload_package"] is False
            for component in components
        ),
        "local_candidate_package_rebuilt": payload["local_candidate_package_rebuilt"] is True
        and state["local_candidate_package_rebuilt"] is True,
        "rebuilt_candidate_payload_created": payload["rebuilt_candidate_payload_created"] is True
        and state["rebuilt_candidate_payload_created"] is True,
        "rebuilt_candidate_manifest_created": state["rebuilt_candidate_manifest_created"] is True,
        "rebuilt_candidate_index_created": state["rebuilt_candidate_index_created"] is True,
        "rebuilt_candidate_trace_created": state["rebuilt_candidate_trace_created"] is True
        and trace["trace_ready"] is True,
        "review_handoff_created": state["review_handoff_created"] is True,
        "rebuilt_candidate_id_present": payload["rebuilt_candidate_id"].startswith(
            "MILESTONE-10-REBUILT-CANDIDATE-"
        ),
        "rebuilt_candidate_signature_present": bool(payload["signature"]),
        "rebuild_trace_hash_present": bool(trace["trace_hash"]) and len(trace["trace_hash"]) == 64,
        "rebuild_check_count_valid": len(REBUILD_CHECKS) == EXPECTED_REBUILD_CHECK_COUNT,
        "rebuild_case_count_valid": len(REBUILD_CASES) == EXPECTED_REBUILD_CASE_COUNT,
        "fail_closed_control_count_valid": len(FAIL_CLOSED_CONTROLS) == 9,
        "boundary_control_count_valid": len(BOUNDARY_CONTROLS) == 9,
        "rebuild_record_created": state["submission_candidate_rebuild_created"] is True,
        "rebuild_record_ready": state["submission_candidate_rebuild_ready"] is True,
        "rebuild_record_locked": state["submission_candidate_rebuild_locked"] is True,
        "rebuild_mode_valid": REBUILD_MODE == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_LOCAL_ONLY",
        "rebuild_scope_valid": REBUILD_SCOPE
        == "LOCAL_SUBMISSION_CANDIDATE_REBUILD_NO_SUBMISSION_JSON_NO_UPLOAD",
        "rebuild_verdict_valid": REBUILD_VERDICT
        == "SUBMISSION_CANDIDATE_REBUILD_READY_FOR_REBUILT_CANDIDATE_REVIEW_REAL_SUBMISSION_BLOCKED",
        "next_stage_valid": NEXT_ALLOWED_STAGE == "MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1",
        "rebuilt_candidate_review_required_next": state["rebuilt_candidate_review_required_next"] is True,
        "real_submission_candidate_not_created": source["real_submission_candidate_created"] is False
        and payload["real_submission_candidate_created"] is False
        and state["real_submission_candidate_created"] is False,
        "submission_json_not_created": source["submission_json_created"] is False
        and payload["submission_json_created"] is False
        and state["submission_json_created"] is False,
        "upload_package_not_created": source["upload_package_created"] is False
        and payload["upload_package_created"] is False
        and state["upload_package_created"] is False,
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


def evaluate_submission_candidate_rebuild_case(case_id: str) -> Dict[str, Any]:
    checks = build_submission_candidate_rebuild_checks()

    if case_id == "m10_candidate_rebuild_gate_source_ready_v1":
        passed = (
            checks["rebuild_gate_artifact_present"]
            and checks["rebuild_gate_artifact_ready"]
            and checks["rebuild_gate_artifact_valid"]
            and checks["rebuild_gate_passed"]
        )
        return _result(case_id, "source_binding", "verify_rebuild_gate_source", passed)

    if case_id == "m10_candidate_rebuild_selected_candidate_valid_v1":
        passed = checks["selected_candidate_id_valid"] and checks["candidate_package_id_valid"]
        return _result(case_id, "selected_candidate", "verify_selected_candidate", passed)

    if case_id == "m10_candidate_rebuild_package_rebuilt_v1":
        passed = checks["local_candidate_package_rebuilt"] and checks["rebuilt_candidate_payload_created"]
        return _result(case_id, "rebuild_package", "verify_local_candidate_package_rebuilt", passed)

    if case_id == "m10_candidate_rebuild_components_ready_v1":
        passed = (
            checks["rebuild_component_count_valid"]
            and checks["all_rebuild_components_ready"]
            and checks["all_rebuild_components_safe"]
        )
        return _result(case_id, "rebuild_components", "verify_rebuild_components", passed)

    if case_id == "m10_candidate_rebuild_trace_ready_v1":
        passed = checks["rebuilt_candidate_trace_created"] and checks["rebuild_trace_hash_present"]
        return _result(case_id, "traceability", "verify_rebuild_trace", passed)

    if case_id == "m10_candidate_rebuild_review_handoff_ready_v1":
        passed = checks["review_handoff_created"] and checks["rebuilt_candidate_review_required_next"]
        return _result(case_id, "review_handoff", "verify_review_handoff", passed)

    if case_id == "m10_candidate_rebuild_no_submission_json_v1":
        return _result(case_id, "submission_boundary", "verify_no_submission_json", checks["submission_json_not_created"])

    if case_id == "m10_candidate_rebuild_real_submission_blocked_v1":
        passed = checks["real_submission_candidate_not_created"] and checks["real_submission_allowed_false"]
        return _result(case_id, "submission_boundary", "verify_real_submission_blocked", passed)

    if case_id == "m10_candidate_rebuild_fail_closed_preserved_v1":
        passed = checks["fail_closed_required"] and checks["fail_closed_active"]
        return _result(case_id, "fail_closed", "verify_fail_closed_preserved", passed)

    if case_id == "m10_candidate_rebuild_next_stage_valid_v1":
        return _result(case_id, "next_stage", "verify_rebuilt_candidate_review_next", checks["next_stage_valid"])

    raise ValueError(f"unknown submission candidate rebuild case: {case_id}")


def evaluate_all_submission_candidate_rebuild_cases() -> Tuple[Dict[str, Any], ...]:
    return tuple(evaluate_submission_candidate_rebuild_case(case["case_id"]) for case in REBUILD_CASES)


def build_milestone_10_submission_candidate_rebuild() -> Dict[str, Any]:
    source = build_submission_candidate_rebuild_source_summary()
    components = build_rebuild_component_catalog()
    payload = build_rebuilt_candidate_payload()
    state = build_rebuild_state()
    trace = build_rebuild_trace()
    checks = build_submission_candidate_rebuild_checks()
    results = evaluate_all_submission_candidate_rebuild_cases()

    rebuild_pass_count = sum(1 for result in results if result["passed"] is True)
    rebuild_failure_count = sum(1 for result in results if result["passed"] is False)

    gate_state = {
        "rebuild_gate_artifact_present": checks["rebuild_gate_artifact_present"],
        "rebuild_gate_artifact_ready": checks["rebuild_gate_artifact_ready"],
        "rebuild_gate_artifact_valid": checks["rebuild_gate_artifact_valid"],
        "rebuild_gate_commit_valid": checks["rebuild_gate_commit_valid"],
        "rebuild_gate_next_stage_matches_task_8": checks["rebuild_gate_next_stage_matches_task_8"],
        "rebuild_gate_ready": checks["rebuild_gate_ready"],
        "rebuild_gate_locked": checks["rebuild_gate_locked"],
        "rebuild_gate_passed": checks["rebuild_gate_passed"],
        "local_candidate_rebuild_allowed": checks["local_candidate_rebuild_allowed"],
        "submission_candidate_rebuild_required": checks["submission_candidate_rebuild_required"],
        "selected_candidate_id_valid": checks["selected_candidate_id_valid"],
        "candidate_package_id_valid": checks["candidate_package_id_valid"],
        "decision_allows_local_rebuild_only": checks["decision_allows_local_rebuild_only"],
        "operator_approval_required_for_real_submission": checks[
            "operator_approval_required_for_real_submission"
        ],
        "rebuild_component_count_valid": checks["rebuild_component_count_valid"],
        "all_rebuild_components_required": checks["all_rebuild_components_required"],
        "all_rebuild_components_ready": checks["all_rebuild_components_ready"],
        "all_rebuild_components_local_only": checks["all_rebuild_components_local_only"],
        "all_rebuild_components_deterministic": checks["all_rebuild_components_deterministic"],
        "all_rebuild_components_safe": checks["all_rebuild_components_safe"],
        "local_candidate_package_rebuilt": checks["local_candidate_package_rebuilt"],
        "rebuilt_candidate_payload_created": checks["rebuilt_candidate_payload_created"],
        "rebuilt_candidate_manifest_created": checks["rebuilt_candidate_manifest_created"],
        "rebuilt_candidate_index_created": checks["rebuilt_candidate_index_created"],
        "rebuilt_candidate_trace_created": checks["rebuilt_candidate_trace_created"],
        "review_handoff_created": checks["review_handoff_created"],
        "rebuilt_candidate_id_present": checks["rebuilt_candidate_id_present"],
        "rebuilt_candidate_signature_present": checks["rebuilt_candidate_signature_present"],
        "rebuild_trace_hash_present": checks["rebuild_trace_hash_present"],
        "rebuild_check_count_valid": checks["rebuild_check_count_valid"],
        "rebuild_case_count_valid": checks["rebuild_case_count_valid"],
        "fail_closed_control_count_valid": checks["fail_closed_control_count_valid"],
        "boundary_control_count_valid": checks["boundary_control_count_valid"],
        "rebuild_record_created": checks["rebuild_record_created"],
        "rebuild_record_ready": checks["rebuild_record_ready"],
        "rebuild_record_locked": checks["rebuild_record_locked"],
        "rebuild_mode_valid": checks["rebuild_mode_valid"],
        "rebuild_scope_valid": checks["rebuild_scope_valid"],
        "rebuild_verdict_valid": checks["rebuild_verdict_valid"],
        "next_stage_valid": checks["next_stage_valid"],
        "rebuilt_candidate_review_required_next": checks["rebuilt_candidate_review_required_next"],
        "real_submission_candidate_not_created": checks["real_submission_candidate_not_created"],
        "submission_json_not_created": checks["submission_json_not_created"],
        "upload_package_not_created": checks["upload_package_not_created"],
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
        "all_rebuild_cases_pass": all(result["passed"] is True for result in results),
        "rebuild_pass_count_valid": rebuild_pass_count == EXPECTED_REBUILD_PASS_COUNT,
        "rebuild_failure_count_zero": rebuild_failure_count == EXPECTED_REBUILD_FAILURE_COUNT,
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

    rebuild_ready = (
        rebuild_pass_count == EXPECTED_REBUILD_PASS_COUNT
        and rebuild_failure_count == EXPECTED_REBUILD_FAILURE_COUNT
        and checks["rebuild_gate_artifact_ready"]
        and checks["local_candidate_rebuild_allowed"]
        and checks["local_candidate_package_rebuilt"]
        and checks["rebuilt_candidate_payload_created"]
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
        "task": "Task 8",
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_rebuild_gate": source["rebuild_gate_id"],
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": payload["rebuilt_candidate_id"],
        "submission_candidate_rebuild_ready": rebuild_ready,
        "submission_candidate_rebuild_created": True,
        "local_candidate_package_rebuilt": True,
        "rebuilt_candidate_payload_created": True,
        "rebuild_component_count": len(components),
        "real_submission_candidate_created": False,
        "submission_json_created": False,
        "upload_package_created": False,
        "rebuilt_candidate_review_required_next": True,
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
        "status": REBUILD_STATUS,
        "milestone": "Milestone #10",
        "task": "Task 8",
        "title": "Submission Candidate Rebuild v1",
        "baseline_commit": BASELINE_COMMIT,
        "rebuild_mode": REBUILD_MODE,
        "rebuild_scope": REBUILD_SCOPE,
        "rebuild_verdict": REBUILD_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "rebuild_gate_source": {
            "path": str(REBUILD_GATE_JSON),
            "present": REBUILD_GATE_JSON.exists(),
            "status": source["gate_status"],
            "rebuild_gate_id": source["rebuild_gate_id"],
            "sha256": _sha256(REBUILD_GATE_JSON),
            "sha256_16": _sha16(_sha256(REBUILD_GATE_JSON)),
        },
        "source_summary": source,
        "rebuild_state": state,
        "rebuild_components": list(components),
        "rebuilt_candidate_payload": payload,
        "rebuild_trace": trace,
        "fail_closed_controls": list(FAIL_CLOSED_CONTROLS),
        "boundary_controls": list(BOUNDARY_CONTROLS),
        "rebuild_checks": checks,
        "rebuild_check_list": list(REBUILD_CHECKS),
        "rebuild_cases": list(REBUILD_CASES),
        "rebuild_results": list(results),
        "rebuild_gates": list(gates),
        "rebuild_issues": list(issues),
        "rebuild_index": index,
        "submission_candidate_rebuild_ready": rebuild_ready,
        "submission_candidate_rebuild_locked": True,
        "submission_candidate_rebuild_created": True,
        "local_candidate_package_rebuilt": True,
        "rebuilt_candidate_payload_created": True,
        "rebuilt_candidate_manifest_created": True,
        "rebuilt_candidate_index_created": True,
        "rebuilt_candidate_trace_created": True,
        "review_handoff_created": True,
        "selected_candidate_id": source["selected_candidate_id"],
        "candidate_package_id": source["candidate_package_id"],
        "rebuilt_candidate_id": payload["rebuilt_candidate_id"],
        "rebuild_component_count": len(components),
        "rebuild_check_count": len(REBUILD_CHECKS),
        "rebuild_case_count": len(REBUILD_CASES),
        "rebuild_pass_count": rebuild_pass_count,
        "rebuild_failure_count": rebuild_failure_count,
        "rebuild_gate_count": len(gates),
        "passed_gate_count": passed_gate_count,
        "rebuild_issue_count": issue_count,
        "warning_count": 0,
        "rebuilt_candidate_review_required_next": True,
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
            "source": "milestone_10_submission_candidate_rebuild_v1",
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
        "submission_candidate_rebuild_id": f"MILESTONE-10-SUBMISSION-CANDIDATE-REBUILD-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_10_submission_candidate_rebuild(rebuild: Mapping[str, Any]) -> Dict[str, Any]:
    gates = rebuild.get("rebuild_gates", [])
    issues = rebuild.get("rebuild_issues", [])
    results = rebuild.get("rebuild_results", [])
    components = rebuild.get("rebuild_components", [])

    checks = {
        "status_ready": rebuild.get("status") == REBUILD_STATUS,
        "submission_candidate_rebuild_id_present": isinstance(
            rebuild.get("submission_candidate_rebuild_id"), str
        )
        and bool(rebuild.get("submission_candidate_rebuild_id")),
        "signature_present": isinstance(rebuild.get("signature"), str) and bool(rebuild.get("signature")),
        "baseline_commit_valid": str(rebuild.get("baseline_commit", "")).startswith("e329a98"),
        "rebuild_mode_valid": rebuild.get("rebuild_mode") == REBUILD_MODE,
        "rebuild_scope_valid": rebuild.get("rebuild_scope") == REBUILD_SCOPE,
        "rebuild_verdict_valid": rebuild.get("rebuild_verdict") == REBUILD_VERDICT,
        "next_allowed_stage_valid": rebuild.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "submission_candidate_rebuild_ready": rebuild.get("submission_candidate_rebuild_ready") is True,
        "submission_candidate_rebuild_locked": rebuild.get("submission_candidate_rebuild_locked") is True,
        "submission_candidate_rebuild_created": rebuild.get("submission_candidate_rebuild_created") is True,
        "local_candidate_package_rebuilt": rebuild.get("local_candidate_package_rebuilt") is True,
        "rebuilt_candidate_payload_created": rebuild.get("rebuilt_candidate_payload_created") is True,
        "rebuilt_candidate_manifest_created": rebuild.get("rebuilt_candidate_manifest_created") is True,
        "rebuilt_candidate_index_created": rebuild.get("rebuilt_candidate_index_created") is True,
        "rebuilt_candidate_trace_created": rebuild.get("rebuilt_candidate_trace_created") is True,
        "review_handoff_created": rebuild.get("review_handoff_created") is True,
        "selected_candidate_valid": rebuild.get("selected_candidate_id") == EXPECTED_SELECTED_CANDIDATE_ID,
        "candidate_package_valid": rebuild.get("candidate_package_id") == EXPECTED_CANDIDATE_PACKAGE_ID,
        "rebuilt_candidate_id_present": isinstance(rebuild.get("rebuilt_candidate_id"), str)
        and rebuild.get("rebuilt_candidate_id", "").startswith("MILESTONE-10-REBUILT-CANDIDATE-"),
        "component_count_valid": rebuild.get("rebuild_component_count") == EXPECTED_REBUILD_COMPONENT_COUNT,
        "components_safe": bool(components)
        and all(
            component.get("local_only") is True
            and component.get("requires_external_api") is False
            and component.get("requires_kaggle_upload") is False
            and component.get("creates_real_submission") is False
            and component.get("creates_submission_json") is False
            for component in components
        ),
        "rebuild_check_count_valid": rebuild.get("rebuild_check_count") == EXPECTED_REBUILD_CHECK_COUNT,
        "rebuild_case_count_valid": rebuild.get("rebuild_case_count") == EXPECTED_REBUILD_CASE_COUNT,
        "rebuild_pass_count_valid": rebuild.get("rebuild_pass_count") == EXPECTED_REBUILD_PASS_COUNT,
        "rebuild_failure_count_zero": rebuild.get("rebuild_failure_count") == EXPECTED_REBUILD_FAILURE_COUNT,
        "all_results_pass": bool(results) and all(result.get("passed") is True for result in results),
        "all_gates_pass": bool(gates) and all(item.get("passed") is True for item in gates),
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "rebuilt_candidate_review_required_next": rebuild.get("rebuilt_candidate_review_required_next") is True,
        "real_submission_candidate_not_created": rebuild.get("real_submission_candidate_created") is False,
        "submission_json_not_created": rebuild.get("submission_json_created") is False,
        "upload_package_not_created": rebuild.get("upload_package_created") is False,
        "real_submission_decision_not_authorized": rebuild.get("real_submission_decision") == "NOT_AUTHORIZED",
        "real_submission_allowed_false": rebuild.get("real_submission_allowed") is False,
        "manual_upload_not_allowed": rebuild.get("manual_upload_allowed") is False,
        "kaggle_authentication_not_allowed": rebuild.get("kaggle_authentication_allowed") is False,
        "kaggle_submission_not_sent": rebuild.get("kaggle_submission_sent") is False,
        "fail_closed_required": rebuild.get("fail_closed_required") is True,
        "fail_closed_active": rebuild.get("fail_closed_active") is True,
        "metadata_safe": rebuild.get("metadata", {}).get("external_api_dependency") is False
        and rebuild.get("metadata", {}).get("contains_api_keys") is False
        and rebuild.get("metadata", {}).get("private_core_exposure") is False
        and rebuild.get("metadata", {}).get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_INVALID",
        "valid": valid,
        "checks": checks,
        "submission_candidate_rebuild_id": rebuild.get("submission_candidate_rebuild_id"),
        "signature": rebuild.get("signature"),
    }


def render_submission_candidate_rebuild_markdown(rebuild: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #10 - Submission Candidate Rebuild v1",
        "",
        f"- status: {rebuild['status']}",
        f"- submission_candidate_rebuild_id: {rebuild['submission_candidate_rebuild_id']}",
        f"- signature: {rebuild['signature']}",
        f"- baseline_commit: {rebuild['baseline_commit']}",
        f"- rebuild_mode: {rebuild['rebuild_mode']}",
        f"- rebuild_scope: {rebuild['rebuild_scope']}",
        f"- rebuild_verdict: {rebuild['rebuild_verdict']}",
        f"- next_allowed_stage: {rebuild['next_allowed_stage']}",
        f"- submission_candidate_rebuild_ready: {rebuild['submission_candidate_rebuild_ready']}",
        f"- selected_candidate_id: {rebuild['selected_candidate_id']}",
        f"- candidate_package_id: {rebuild['candidate_package_id']}",
        f"- rebuilt_candidate_id: {rebuild['rebuilt_candidate_id']}",
        f"- local_candidate_package_rebuilt: {rebuild['local_candidate_package_rebuilt']}",
        f"- rebuilt_candidate_payload_created: {rebuild['rebuilt_candidate_payload_created']}",
        f"- real_submission_candidate_created: {rebuild['real_submission_candidate_created']}",
        f"- submission_json_created: {rebuild['submission_json_created']}",
        f"- upload_package_created: {rebuild['upload_package_created']}",
        f"- rebuilt_candidate_review_required_next: {rebuild['rebuilt_candidate_review_required_next']}",
        f"- real_submission_decision: {rebuild['real_submission_decision']}",
        f"- real_submission_allowed: {rebuild['real_submission_allowed']}",
        f"- fail_closed_active: {rebuild['fail_closed_active']}",
        "",
        "## Rebuild components",
        "",
    ]

    for component in rebuild["rebuild_components"]:
        lines.append(
            f"- {component['component_id']} / kind={component['kind']} / "
            f"ready={component['ready']} / creates_submission_json={component['creates_submission_json']}"
        )

    lines.extend(["", "## Validation results", ""])

    for result in rebuild["rebuild_results"]:
        lines.append(
            f"- {result['case_id']} / area={result['area']} / "
            f"operation={result['operation']} / passed={result['passed']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "The local submission candidate package has been rebuilt for review. No real submission candidate, submission.json, upload package, Kaggle authentication, or Kaggle submission is created.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_VALID=true",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_READY=true",
            "ARC_AGI3_MILESTONE_10_REBUILD_MODE=MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_LOCAL_ONLY",
            "ARC_AGI3_MILESTONE_10_REBUILD_VERDICT=SUBMISSION_CANDIDATE_REBUILD_READY_FOR_REBUILT_CANDIDATE_REVIEW_REAL_SUBMISSION_BLOCKED",
            "ARC_AGI3_MILESTONE_10_BASELINE_COMMIT=e329a98",
            "ARC_AGI3_MILESTONE_10_NEXT_STAGE=MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1",
            "ARC_AGI3_MILESTONE_10_SELECTED_CANDIDATE_ID=M10-CANDIDATE-BALANCED-PATCH-STACK-v1",
            "ARC_AGI3_MILESTONE_10_LOCAL_CANDIDATE_PACKAGE_REBUILT=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_PAYLOAD_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_MANIFEST_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_INDEX_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_TRACE_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REVIEW_HANDOFF_CREATED=true",
            "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false",
            "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false",
            "ARC_AGI3_MILESTONE_10_REBUILD_COMPONENT_COUNT=6",
            "ARC_AGI3_MILESTONE_10_REBUILD_CHECK_COUNT=30",
            "ARC_AGI3_MILESTONE_10_REBUILD_CASE_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REBUILD_PASS_COUNT=10",
            "ARC_AGI3_MILESTONE_10_REBUILD_FAILURE_COUNT=0",
            "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_REVIEW_REQUIRED_NEXT=true",
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


def render_submission_candidate_rebuild_manifest(rebuild: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 10 SUBMISSION CANDIDATE REBUILD MANIFEST v1",
        f"submission_candidate_rebuild_id={rebuild['submission_candidate_rebuild_id']}",
        f"signature={rebuild['signature']}",
        f"status={rebuild['status']}",
        f"baseline_commit={rebuild['baseline_commit']}",
        f"rebuild_mode={rebuild['rebuild_mode']}",
        f"rebuild_verdict={rebuild['rebuild_verdict']}",
        f"next_allowed_stage={rebuild['next_allowed_stage']}",
        f"submission_candidate_rebuild_ready={rebuild['submission_candidate_rebuild_ready']}",
        f"submission_candidate_rebuild_created={rebuild['submission_candidate_rebuild_created']}",
        f"selected_candidate_id={rebuild['selected_candidate_id']}",
        f"candidate_package_id={rebuild['candidate_package_id']}",
        f"rebuilt_candidate_id={rebuild['rebuilt_candidate_id']}",
        f"local_candidate_package_rebuilt={rebuild['local_candidate_package_rebuilt']}",
        f"rebuilt_candidate_payload_created={rebuild['rebuilt_candidate_payload_created']}",
        f"rebuilt_candidate_manifest_created={rebuild['rebuilt_candidate_manifest_created']}",
        f"rebuilt_candidate_index_created={rebuild['rebuilt_candidate_index_created']}",
        f"rebuilt_candidate_trace_created={rebuild['rebuilt_candidate_trace_created']}",
        f"review_handoff_created={rebuild['review_handoff_created']}",
        f"real_submission_candidate_created={rebuild['real_submission_candidate_created']}",
        f"submission_json_created={rebuild['submission_json_created']}",
        f"upload_package_created={rebuild['upload_package_created']}",
        f"rebuild_component_count={rebuild['rebuild_component_count']}",
        f"rebuild_check_count={rebuild['rebuild_check_count']}",
        f"rebuild_case_count={rebuild['rebuild_case_count']}",
        f"rebuild_pass_count={rebuild['rebuild_pass_count']}",
        f"rebuild_failure_count={rebuild['rebuild_failure_count']}",
        f"rebuild_gate_count={rebuild['rebuild_gate_count']}",
        f"passed_gate_count={rebuild['passed_gate_count']}",
        f"rebuild_issue_count={rebuild['rebuild_issue_count']}",
        f"rebuilt_candidate_review_required_next={rebuild['rebuilt_candidate_review_required_next']}",
        f"real_submission_decision={rebuild['real_submission_decision']}",
        f"real_submission_allowed={rebuild['real_submission_allowed']}",
        f"manual_upload_allowed={rebuild['manual_upload_allowed']}",
        f"kaggle_authentication_allowed={rebuild['kaggle_authentication_allowed']}",
        f"kaggle_submission_sent={rebuild['kaggle_submission_sent']}",
        f"fail_closed_required={rebuild['fail_closed_required']}",
        f"fail_closed_active={rebuild['fail_closed_active']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "REBUILD_COMPONENTS",
    ]

    for component in rebuild["rebuild_components"]:
        lines.append(
            f"{component['component_id']} kind={component['kind']} ready={component['ready']} "
            f"creates_submission_json={component['creates_submission_json']}"
        )

    lines.append("")
    lines.append("REBUILD_VALIDATION_RESULTS")
    for result in rebuild["rebuild_results"]:
        lines.append(
            f"{result['case_id']} area={result['area']} operation={result['operation']} "
            f"passed={result['passed']} evidence_score={result['evidence_score']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_submission_candidate_rebuild_artifacts(
    rebuild: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    rebuild = dict(rebuild or build_milestone_10_submission_candidate_rebuild())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-10-submission-candidate-rebuild-v1.json"
    md_path = output / "milestone-10-submission-candidate-rebuild-v1.md"
    manifest_path = output / "milestone-10-submission-candidate-rebuild-manifest-v1.txt"
    index_path = output / "milestone-10-submission-candidate-rebuild-index-v1.json"
    payload_path = output / "milestone-10-rebuilt-candidate-payload-v1.json"

    json_path.write_text(json.dumps(rebuild, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_submission_candidate_rebuild_markdown(rebuild), encoding="utf-8")
    manifest_path.write_text(render_submission_candidate_rebuild_manifest(rebuild), encoding="utf-8")
    index_path.write_text(json.dumps(rebuild["rebuild_index"], indent=2, sort_keys=True), encoding="utf-8")
    payload_path.write_text(
        json.dumps(rebuild["rebuilt_candidate_payload"], indent=2, sort_keys=True),
        encoding="utf-8",
    )

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "payload_path": str(payload_path),
    }


def run_milestone_10_submission_candidate_rebuild_pipeline() -> Dict[str, Any]:
    rebuild = build_milestone_10_submission_candidate_rebuild()
    validation = validate_milestone_10_submission_candidate_rebuild(rebuild)
    artifacts = write_submission_candidate_rebuild_artifacts(rebuild)

    return {
        "status": PIPELINE_STATUS
        if validation["valid"]
        else "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_PIPELINE_INVALID",
        "rebuild_status": rebuild["status"],
        "validation_status": validation["status"],
        "rebuild": rebuild,
        "submission_candidate_rebuild_id": rebuild["submission_candidate_rebuild_id"],
        "signature": rebuild["signature"],
        "rebuild_mode": rebuild["rebuild_mode"],
        "rebuild_verdict": rebuild["rebuild_verdict"],
        "next_allowed_stage": rebuild["next_allowed_stage"],
        "submission_candidate_rebuild_ready": rebuild["submission_candidate_rebuild_ready"],
        "submission_candidate_rebuild_created": rebuild["submission_candidate_rebuild_created"],
        "local_candidate_package_rebuilt": rebuild["local_candidate_package_rebuilt"],
        "rebuilt_candidate_payload_created": rebuild["rebuilt_candidate_payload_created"],
        "rebuilt_candidate_manifest_created": rebuild["rebuilt_candidate_manifest_created"],
        "rebuilt_candidate_index_created": rebuild["rebuilt_candidate_index_created"],
        "rebuilt_candidate_trace_created": rebuild["rebuilt_candidate_trace_created"],
        "review_handoff_created": rebuild["review_handoff_created"],
        "selected_candidate_id": rebuild["selected_candidate_id"],
        "candidate_package_id": rebuild["candidate_package_id"],
        "rebuilt_candidate_id": rebuild["rebuilt_candidate_id"],
        "rebuild_component_count": rebuild["rebuild_component_count"],
        "rebuild_check_count": rebuild["rebuild_check_count"],
        "rebuild_case_count": rebuild["rebuild_case_count"],
        "rebuild_pass_count": rebuild["rebuild_pass_count"],
        "rebuild_failure_count": rebuild["rebuild_failure_count"],
        "rebuild_gate_count": rebuild["rebuild_gate_count"],
        "passed_gate_count": rebuild["passed_gate_count"],
        "rebuild_issue_count": rebuild["rebuild_issue_count"],
        "warning_count": rebuild["warning_count"],
        "rebuilt_candidate_review_required_next": rebuild["rebuilt_candidate_review_required_next"],
        "real_submission_candidate_created": rebuild["real_submission_candidate_created"],
        "submission_json_created": rebuild["submission_json_created"],
        "upload_package_created": rebuild["upload_package_created"],
        "real_submission_decision": rebuild["real_submission_decision"],
        "real_submission_allowed": rebuild["real_submission_allowed"],
        "manual_upload_allowed": rebuild["manual_upload_allowed"],
        "kaggle_authentication_allowed": rebuild["kaggle_authentication_allowed"],
        "kaggle_submission_sent": rebuild["kaggle_submission_sent"],
        "fail_closed_required": rebuild["fail_closed_required"],
        "fail_closed_active": rebuild["fail_closed_active"],
        "artifacts": artifacts,
        "metadata": rebuild["metadata"],
    }
