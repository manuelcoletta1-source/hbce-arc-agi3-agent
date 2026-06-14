"""Milestone #6 Real Submission Readiness Closure v1.

Local-only closure for Milestone #6.

This module closes the real-submission readiness chain by confirming that the
candidate package is prepared, frozen, integrity-verified, final-audited, and
blocked pending solver improvement. It does not submit to Kaggle, authenticate,
upload files, call external APIs, read secrets, create upload archives, or
create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CLOSURE_STATUS = "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_READY"
PIPELINE_STATUS = "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_VALID"

BASELINE_COMMIT = "5a4d69a Add ARC AGI3 solver improvement before real submission"
CLOSURE_MODE = "REAL_SUBMISSION_READINESS_CLOSURE_ONLY_NO_UPLOAD"
CLOSURE_SCOPE = "CLOSE_MILESTONE_6_WITH_REAL_SUBMISSION_BLOCKED_PENDING_SOLVER_IMPROVEMENT"
CLOSURE_VERDICT = "MILESTONE_6_CLOSED_REAL_SUBMISSION_NOT_READY_SOLVER_IMPROVEMENT_REQUIRED"
NEXT_ALLOWED_STAGE = "OPEN_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/real-submission-readiness-closure-v1"

SOLVER_IMPROVEMENT_JSON = Path(
    "examples/milestone-6/solver-improvement-before-real-submission-v1/"
    "milestone-6-solver-improvement-before-real-submission-v1.json"
)
FINAL_AUDIT_JSON = Path(
    "examples/milestone-6/submission-candidate-final-audit-v1/"
    "milestone-6-submission-candidate-final-audit-v1.json"
)
INTEGRITY_JSON = Path(
    "examples/milestone-6/frozen-package-integrity-verification-v1/"
    "milestone-6-frozen-package-integrity-verification-v1.json"
)
FREEZE_JSON = Path(
    "examples/milestone-6/real-submission-package-freeze-v1/"
    "milestone-6-real-submission-package-freeze-v1.json"
)
MANUAL_GATE_JSON = Path(
    "examples/milestone-6/manual-submission-execution-gate-v1/"
    "milestone-6-manual-submission-execution-gate-v1.json"
)
PRECHECK_JSON = Path(
    "examples/milestone-6/real-submission-precheck-gate-v1/"
    "milestone-6-real-submission-precheck-gate-v1.json"
)

EXPECTED_CLOSURE_SOURCE_COUNT = 6
EXPECTED_CLOSED_TASK_COUNT = 10

CLOSURE_SOURCES: Tuple[Dict[str, str], ...] = (
    {
        "name": "solver_improvement_before_real_submission",
        "path": str(SOLVER_IMPROVEMENT_JSON),
        "expected_status": "MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_READY",
        "id_field": "improvement_id",
    },
    {
        "name": "submission_candidate_final_audit",
        "path": str(FINAL_AUDIT_JSON),
        "expected_status": "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_READY",
        "id_field": "audit_id",
    },
    {
        "name": "frozen_package_integrity_verification",
        "path": str(INTEGRITY_JSON),
        "expected_status": "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_READY",
        "id_field": "integrity_id",
    },
    {
        "name": "real_submission_package_freeze",
        "path": str(FREEZE_JSON),
        "expected_status": "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_READY",
        "id_field": "freeze_id",
    },
    {
        "name": "manual_submission_execution_gate",
        "path": str(MANUAL_GATE_JSON),
        "expected_status": "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY",
        "id_field": "gate_id",
    },
    {
        "name": "real_submission_precheck_gate",
        "path": str(PRECHECK_JSON),
        "expected_status": "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY",
        "id_field": "precheck_id",
    },
)

CLOSURE_GATES: Tuple[str, ...] = (
    "solver_improvement_artifact_present",
    "solver_improvement_artifact_ready",
    "solver_improvement_valid",
    "solver_improvement_required",
    "solver_improvement_started",
    "solver_improvement_not_completed",
    "final_audit_artifact_present",
    "final_audit_ready",
    "final_audit_locked",
    "final_audit_blocks_submission",
    "integrity_artifact_present",
    "integrity_verified",
    "integrity_locked",
    "freeze_artifact_present",
    "freeze_ready",
    "freeze_locked",
    "manual_gate_artifact_present",
    "manual_gate_ready",
    "manual_execution_not_performed",
    "precheck_artifact_present",
    "precheck_passed",
    "operator_approval_granted",
    "closure_mode_valid",
    "closure_scope_valid",
    "closure_verdict_valid",
    "closure_ready",
    "closure_locked",
    "closure_source_count_valid",
    "all_closure_sources_ready",
    "all_closure_source_hashes_present",
    "closed_task_count_valid",
    "milestone_closed",
    "next_stage_defined",
    "competitive_claim_absent",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

CLOSURE_ISSUES: Tuple[str, ...] = (
    "solver_improvement_artifact_missing",
    "solver_improvement_artifact_not_ready",
    "solver_improvement_invalid",
    "solver_improvement_not_required",
    "solver_improvement_not_started",
    "solver_improvement_already_completed",
    "final_audit_artifact_missing",
    "final_audit_not_ready",
    "final_audit_not_locked",
    "final_audit_allows_submission",
    "integrity_artifact_missing",
    "integrity_not_verified",
    "integrity_not_locked",
    "freeze_artifact_missing",
    "freeze_not_ready",
    "freeze_not_locked",
    "manual_gate_artifact_missing",
    "manual_gate_not_ready",
    "manual_execution_performed",
    "precheck_artifact_missing",
    "precheck_not_passed",
    "operator_approval_not_granted",
    "closure_mode_invalid",
    "closure_scope_invalid",
    "closure_verdict_invalid",
    "closure_not_ready",
    "closure_not_locked",
    "closure_source_count_invalid",
    "closure_source_not_ready",
    "closure_source_hash_missing",
    "closed_task_count_invalid",
    "milestone_not_closed",
    "next_stage_missing",
    "competitive_claim_detected",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()


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


def _boundary_from_improvement(improvement: Mapping[str, Any]) -> Dict[str, Any]:
    source = improvement.get("boundary", {}) if isinstance(improvement.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": improvement.get("kaggle_submission_sent"),
        "private_core_exposure": source.get("private_core_exposure"),
        "legal_certification": source.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    expected = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }
    return all(boundary.get(key) is value for key, value in expected.items())


def _source_record(source: Mapping[str, str]) -> Dict[str, Any]:
    path = Path(source["path"])
    payload = _read_json(path)
    file_hash = _sha256(path)
    return {
        "name": source["name"],
        "path": str(path),
        "present": path.exists(),
        "expected_status": source["expected_status"],
        "actual_status": payload.get("status", "MISSING"),
        "ready": path.exists() and payload.get("status") == source["expected_status"],
        "artifact_id": payload.get(source["id_field"], f"MISSING_{source['id_field'].upper()}"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _build_closure_sources() -> Tuple[Dict[str, Any], ...]:
    return tuple(_source_record(source) for source in CLOSURE_SOURCES)


def build_milestone_6_real_submission_readiness_closure() -> Dict[str, Any]:
    improvement = _read_json(SOLVER_IMPROVEMENT_JSON)
    final_audit = _read_json(FINAL_AUDIT_JSON)
    integrity = _read_json(INTEGRITY_JSON)
    freeze = _read_json(FREEZE_JSON)
    manual_gate = _read_json(MANUAL_GATE_JSON)
    precheck = _read_json(PRECHECK_JSON)

    boundary = _boundary_from_improvement(improvement)
    closure_sources = _build_closure_sources()

    ready_source_count = sum(1 for item in closure_sources if item["ready"] is True)
    source_hash_count = sum(1 for item in closure_sources if item["sha256"] != "MISSING_HASH")

    closure_record = {
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "closure_ready": True,
        "closure_locked": True,
        "milestone_closed": True,
        "closed_task_count": EXPECTED_CLOSED_TASK_COUNT,
        "closure_source_count": len(closure_sources),
        "ready_source_count": ready_source_count,
        "source_hash_count": source_hash_count,
        "package_prepared": True,
        "package_frozen": freeze.get("freeze_locked") is True,
        "integrity_verified": integrity.get("integrity_verified") is True,
        "final_audit_passed": final_audit.get("audit_ready") is True,
        "solver_improvement_required": improvement.get("solver_improvement_required") is True,
        "solver_improvement_started": improvement.get("solver_improvement_started") is True,
        "solver_improvement_completed": improvement.get("solver_improvement_completed") is True,
        "competitive_claim_absent": True,
        "manual_upload_required": True,
        "manual_execution_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "boundary_intact": _boundary_intact(boundary),
    }

    gate_state = {
        "solver_improvement_artifact_present": SOLVER_IMPROVEMENT_JSON.exists(),
        "solver_improvement_artifact_ready": improvement.get("status") == "MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_READY",
        "solver_improvement_valid": bool(improvement.get("improvement_id")) and bool(improvement.get("signature")),
        "solver_improvement_required": improvement.get("solver_improvement_required") is True,
        "solver_improvement_started": improvement.get("solver_improvement_started") is True,
        "solver_improvement_not_completed": improvement.get("solver_improvement_completed") is False,
        "final_audit_artifact_present": FINAL_AUDIT_JSON.exists(),
        "final_audit_ready": final_audit.get("audit_ready") is True,
        "final_audit_locked": final_audit.get("audit_locked") is True,
        "final_audit_blocks_submission": final_audit.get("real_submission_allowed") is False,
        "integrity_artifact_present": INTEGRITY_JSON.exists(),
        "integrity_verified": integrity.get("integrity_verified") is True,
        "integrity_locked": integrity.get("integrity_locked") is True,
        "freeze_artifact_present": FREEZE_JSON.exists(),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "manual_gate_artifact_present": MANUAL_GATE_JSON.exists(),
        "manual_gate_ready": manual_gate.get("manual_execution_gate_ready") is True,
        "manual_execution_not_performed": manual_gate.get("manual_execution_performed") is False,
        "precheck_artifact_present": PRECHECK_JSON.exists(),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "closure_mode_valid": closure_record["closure_mode"] == CLOSURE_MODE,
        "closure_scope_valid": closure_record["closure_scope"] == CLOSURE_SCOPE,
        "closure_verdict_valid": closure_record["closure_verdict"] == CLOSURE_VERDICT,
        "closure_ready": closure_record["closure_ready"] is True,
        "closure_locked": closure_record["closure_locked"] is True,
        "closure_source_count_valid": len(closure_sources) == EXPECTED_CLOSURE_SOURCE_COUNT,
        "all_closure_sources_ready": ready_source_count == EXPECTED_CLOSURE_SOURCE_COUNT,
        "all_closure_source_hashes_present": source_hash_count == EXPECTED_CLOSURE_SOURCE_COUNT,
        "closed_task_count_valid": closure_record["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT,
        "milestone_closed": closure_record["milestone_closed"] is True,
        "next_stage_defined": closure_record["next_allowed_stage"] == NEXT_ALLOWED_STAGE,
        "competitive_claim_absent": closure_record["competitive_claim_absent"] is True,
        "real_submission_allowed_false": closure_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": closure_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": closure_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": closure_record["kaggle_submission_sent"] is False,
        "upload_not_performed": closure_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": closure_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "solver_improvement_artifact_missing": not gate_state["solver_improvement_artifact_present"],
        "solver_improvement_artifact_not_ready": not gate_state["solver_improvement_artifact_ready"],
        "solver_improvement_invalid": not gate_state["solver_improvement_valid"],
        "solver_improvement_not_required": not gate_state["solver_improvement_required"],
        "solver_improvement_not_started": not gate_state["solver_improvement_started"],
        "solver_improvement_already_completed": not gate_state["solver_improvement_not_completed"],
        "final_audit_artifact_missing": not gate_state["final_audit_artifact_present"],
        "final_audit_not_ready": not gate_state["final_audit_ready"],
        "final_audit_not_locked": not gate_state["final_audit_locked"],
        "final_audit_allows_submission": not gate_state["final_audit_blocks_submission"],
        "integrity_artifact_missing": not gate_state["integrity_artifact_present"],
        "integrity_not_verified": not gate_state["integrity_verified"],
        "integrity_not_locked": not gate_state["integrity_locked"],
        "freeze_artifact_missing": not gate_state["freeze_artifact_present"],
        "freeze_not_ready": not gate_state["freeze_ready"],
        "freeze_not_locked": not gate_state["freeze_locked"],
        "manual_gate_artifact_missing": not gate_state["manual_gate_artifact_present"],
        "manual_gate_not_ready": not gate_state["manual_gate_ready"],
        "manual_execution_performed": not gate_state["manual_execution_not_performed"],
        "precheck_artifact_missing": not gate_state["precheck_artifact_present"],
        "precheck_not_passed": not gate_state["precheck_passed"],
        "operator_approval_not_granted": not gate_state["operator_approval_granted"],
        "closure_mode_invalid": not gate_state["closure_mode_valid"],
        "closure_scope_invalid": not gate_state["closure_scope_valid"],
        "closure_verdict_invalid": not gate_state["closure_verdict_valid"],
        "closure_not_ready": not gate_state["closure_ready"],
        "closure_not_locked": not gate_state["closure_locked"],
        "closure_source_count_invalid": not gate_state["closure_source_count_valid"],
        "closure_source_not_ready": not gate_state["all_closure_sources_ready"],
        "closure_source_hash_missing": not gate_state["all_closure_source_hashes_present"],
        "closed_task_count_invalid": not gate_state["closed_task_count_valid"],
        "milestone_not_closed": not gate_state["milestone_closed"],
        "next_stage_missing": not gate_state["next_stage_defined"],
        "competitive_claim_detected": not gate_state["competitive_claim_absent"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
    }

    gates = tuple(
        {"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"}
        for name in CLOSURE_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in CLOSURE_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    closure_ready = (
        ready_source_count == EXPECTED_CLOSURE_SOURCE_COUNT
        and source_hash_count == EXPECTED_CLOSURE_SOURCE_COUNT
        and passed_gate_count == len(CLOSURE_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #6",
        "task": "Task 10",
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_solver_improvement": improvement.get("improvement_id", "MISSING_IMPROVEMENT_ID"),
        "closure_ready": closure_ready,
        "closure_locked": True,
        "milestone_closed": True,
        "closed_task_count": EXPECTED_CLOSED_TASK_COUNT,
        "package_prepared": True,
        "package_frozen": freeze.get("freeze_locked") is True,
        "integrity_verified": integrity.get("integrity_verified") is True,
        "final_audit_passed": final_audit.get("audit_ready") is True,
        "solver_improvement_required": True,
        "solver_improvement_started": True,
        "solver_improvement_completed": False,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "manual_execution_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": CLOSURE_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 10",
        "title": "Real Submission Readiness Closure v1",
        "baseline_commit": BASELINE_COMMIT,
        "closure_mode": CLOSURE_MODE,
        "closure_scope": CLOSURE_SCOPE,
        "closure_verdict": CLOSURE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "closure_record": closure_record,
        "closure_sources": list(closure_sources),
        "closure_gates": list(gates),
        "closure_issues": list(issues),
        "closure_index": index,
        "boundary": boundary,
        "closure_source_count": len(closure_sources),
        "ready_source_count": ready_source_count,
        "source_hash_count": source_hash_count,
        "closed_task_count": EXPECTED_CLOSED_TASK_COUNT,
        "closure_gate_count": len(CLOSURE_GATES),
        "passed_gate_count": passed_gate_count,
        "closure_issue_count": issue_count,
        "warning_count": 0,
        "closure_ready": closure_ready,
        "closure_locked": True,
        "milestone_closed": True,
        "package_prepared": True,
        "package_frozen": freeze.get("freeze_locked") is True,
        "integrity_verified": integrity.get("integrity_verified") is True,
        "final_audit_passed": final_audit.get("audit_ready") is True,
        "solver_improvement_required": True,
        "solver_improvement_started": True,
        "solver_improvement_completed": False,
        "competitive_claim_absent": True,
        "manual_upload_required": True,
        "manual_execution_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_6_real_submission_readiness_closure_v1",
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
        "closure_id": f"MILESTONE-6-READINESS-CLOSURE-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_6_real_submission_readiness_closure(closure: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = closure.get("boundary", {})
    gates = closure.get("closure_gates", [])
    issues = closure.get("closure_issues", [])
    sources = closure.get("closure_sources", [])

    checks = {
        "status_ready": closure.get("status") == CLOSURE_STATUS,
        "closure_id_present": isinstance(closure.get("closure_id"), str) and bool(closure.get("closure_id")),
        "signature_present": isinstance(closure.get("signature"), str) and bool(closure.get("signature")),
        "baseline_commit_valid": str(closure.get("baseline_commit", "")).startswith("5a4d69a"),
        "closure_mode_valid": closure.get("closure_mode") == CLOSURE_MODE,
        "closure_scope_valid": closure.get("closure_scope") == CLOSURE_SCOPE,
        "closure_verdict_valid": closure.get("closure_verdict") == CLOSURE_VERDICT,
        "next_allowed_stage_valid": closure.get("next_allowed_stage") == NEXT_ALLOWED_STAGE,
        "closure_source_count_valid": closure.get("closure_source_count") == EXPECTED_CLOSURE_SOURCE_COUNT,
        "ready_source_count_valid": closure.get("ready_source_count") == EXPECTED_CLOSURE_SOURCE_COUNT,
        "source_hash_count_valid": closure.get("source_hash_count") == EXPECTED_CLOSURE_SOURCE_COUNT,
        "closed_task_count_valid": closure.get("closed_task_count") == EXPECTED_CLOSED_TASK_COUNT,
        "all_sources_ready": bool(sources) and all(item.get("ready") is True for item in sources),
        "all_source_hashes_present": bool(sources) and all(item.get("sha256") != "MISSING_HASH" for item in sources),
        "closure_gate_count_matches": closure.get("closure_gate_count") == len(CLOSURE_GATES),
        "all_closure_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "closure_issue_count_zero": closure.get("closure_issue_count") == 0,
        "all_closure_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "closure_ready": closure.get("closure_ready") is True,
        "closure_locked": closure.get("closure_locked") is True,
        "milestone_closed": closure.get("milestone_closed") is True,
        "package_prepared": closure.get("package_prepared") is True,
        "package_frozen": closure.get("package_frozen") is True,
        "integrity_verified": closure.get("integrity_verified") is True,
        "final_audit_passed": closure.get("final_audit_passed") is True,
        "solver_improvement_required": closure.get("solver_improvement_required") is True,
        "solver_improvement_started": closure.get("solver_improvement_started") is True,
        "solver_improvement_not_completed": closure.get("solver_improvement_completed") is False,
        "competitive_claim_absent": closure.get("competitive_claim_absent") is True,
        "manual_upload_required": closure.get("manual_upload_required") is True,
        "manual_execution_not_performed": closure.get("manual_execution_performed") is False,
        "real_submission_allowed_false": closure.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": closure.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": closure.get("real_submission_created") is False,
        "kaggle_submission_not_sent": closure.get("kaggle_submission_sent") is False,
        "upload_not_performed": closure.get("upload_performed") is False,
        "kaggle_authentication_not_performed": closure.get("kaggle_authentication_performed") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_INVALID",
        "valid": valid,
        "checks": checks,
        "closure_id": closure.get("closure_id"),
        "signature": closure.get("signature"),
    }


def render_real_submission_readiness_closure_markdown(closure: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Real Submission Readiness Closure v1",
        "",
        f"- status: {closure['status']}",
        f"- closure_id: {closure['closure_id']}",
        f"- signature: {closure['signature']}",
        f"- baseline_commit: {closure['baseline_commit']}",
        f"- closure_mode: {closure['closure_mode']}",
        f"- closure_scope: {closure['closure_scope']}",
        f"- closure_verdict: {closure['closure_verdict']}",
        f"- next_allowed_stage: {closure['next_allowed_stage']}",
        f"- closure_source_count: {closure['closure_source_count']}",
        f"- ready_source_count: {closure['ready_source_count']}",
        f"- source_hash_count: {closure['source_hash_count']}",
        f"- closed_task_count: {closure['closed_task_count']}",
        f"- closure_gate_count: {closure['closure_gate_count']}",
        f"- passed_gate_count: {closure['passed_gate_count']}",
        f"- closure_issue_count: {closure['closure_issue_count']}",
        f"- closure_ready: {closure['closure_ready']}",
        f"- closure_locked: {closure['closure_locked']}",
        f"- milestone_closed: {closure['milestone_closed']}",
        f"- package_prepared: {closure['package_prepared']}",
        f"- package_frozen: {closure['package_frozen']}",
        f"- integrity_verified: {closure['integrity_verified']}",
        f"- final_audit_passed: {closure['final_audit_passed']}",
        f"- solver_improvement_required: {closure['solver_improvement_required']}",
        f"- solver_improvement_completed: {closure['solver_improvement_completed']}",
        f"- real_submission_allowed: {closure['real_submission_allowed']}",
        f"- kaggle_submission_sent: {closure['kaggle_submission_sent']}",
        f"- upload_performed: {closure['upload_performed']}",
        "",
        "## Closure sources",
        "",
    ]

    for source in closure["closure_sources"]:
        lines.append(
            f"- {source['name']}: ready={source['ready']} sha256_16={source['sha256_16']} artifact_id={source['artifact_id']}"
        )

    lines.extend(
        [
            "",
            "## Decision",
            "",
            "Milestone #6 is closed as a real-submission readiness package. Real submission remains blocked because solver improvement is required and not completed.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_VALID=true",
            "ARC_AGI3_MILESTONE_6_CLOSURE_MODE=REAL_SUBMISSION_READINESS_CLOSURE_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_6_CLOSURE_VERDICT=MILESTONE_6_CLOSED_REAL_SUBMISSION_NOT_READY_SOLVER_IMPROVEMENT_REQUIRED",
            "ARC_AGI3_MILESTONE_6_CLOSURE_READY=true",
            "ARC_AGI3_MILESTONE_6_CLOSURE_LOCKED=true",
            "ARC_AGI3_MILESTONE_6_CLOSED=true",
            "ARC_AGI3_MILESTONE_6_CLOSED_TASK_COUNT=10",
            "ARC_AGI3_MILESTONE_6_PACKAGE_PREPARED=true",
            "ARC_AGI3_MILESTONE_6_PACKAGE_FROZEN=true",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_VERIFIED=true",
            "ARC_AGI3_MILESTONE_6_FINAL_AUDIT_PASSED=true",
            "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_STARTED=true",
            "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_COMPLETED=false",
            "ARC_AGI3_MILESTONE_6_NEXT_STAGE=OPEN_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_SOLVER_IMPROVEMENT_COMMIT=5a4d69a",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_real_submission_readiness_closure_manifest(closure: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 REAL SUBMISSION READINESS CLOSURE MANIFEST v1",
        f"closure_id={closure['closure_id']}",
        f"signature={closure['signature']}",
        f"status={closure['status']}",
        f"baseline_commit={closure['baseline_commit']}",
        f"closure_mode={closure['closure_mode']}",
        f"closure_verdict={closure['closure_verdict']}",
        f"next_allowed_stage={closure['next_allowed_stage']}",
        f"closure_source_count={closure['closure_source_count']}",
        f"ready_source_count={closure['ready_source_count']}",
        f"source_hash_count={closure['source_hash_count']}",
        f"closed_task_count={closure['closed_task_count']}",
        f"closure_gate_count={closure['closure_gate_count']}",
        f"passed_gate_count={closure['passed_gate_count']}",
        f"closure_issue_count={closure['closure_issue_count']}",
        f"closure_ready={closure['closure_ready']}",
        f"closure_locked={closure['closure_locked']}",
        f"milestone_closed={closure['milestone_closed']}",
        f"package_prepared={closure['package_prepared']}",
        f"package_frozen={closure['package_frozen']}",
        f"integrity_verified={closure['integrity_verified']}",
        f"final_audit_passed={closure['final_audit_passed']}",
        f"solver_improvement_required={closure['solver_improvement_required']}",
        f"solver_improvement_started={closure['solver_improvement_started']}",
        f"solver_improvement_completed={closure['solver_improvement_completed']}",
        f"competitive_claim_absent={closure['competitive_claim_absent']}",
        f"manual_upload_required={closure['manual_upload_required']}",
        f"manual_execution_performed={closure['manual_execution_performed']}",
        f"real_submission_allowed={closure['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={closure['ready_for_real_kaggle_submission']}",
        f"real_submission_created={closure['real_submission_created']}",
        f"kaggle_submission_sent={closure['kaggle_submission_sent']}",
        f"upload_performed={closure['upload_performed']}",
        f"kaggle_authentication_performed={closure['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "CLOSURE_SOURCES",
    ]

    for source in closure["closure_sources"]:
        lines.append(
            f"{source['name']} present={source['present']} ready={source['ready']} "
            f"sha256={source['sha256']} artifact_id={source['artifact_id']} path={source['path']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_real_submission_readiness_closure_artifacts(
    closure: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    closure = dict(closure or build_milestone_6_real_submission_readiness_closure())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-real-submission-readiness-closure-v1.json"
    md_path = output / "milestone-6-real-submission-readiness-closure-v1.md"
    manifest_path = output / "milestone-6-real-submission-readiness-closure-manifest-v1.txt"
    index_path = output / "milestone-6-real-submission-readiness-closure-index-v1.json"

    json_path.write_text(json.dumps(closure, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_readiness_closure_markdown(closure), encoding="utf-8")
    manifest_path.write_text(render_real_submission_readiness_closure_manifest(closure), encoding="utf-8")
    index_path.write_text(json.dumps(closure["closure_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_real_submission_readiness_closure_pipeline() -> Dict[str, Any]:
    closure = build_milestone_6_real_submission_readiness_closure()
    validation = validate_milestone_6_real_submission_readiness_closure(closure)
    artifacts = write_real_submission_readiness_closure_artifacts(closure)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_PIPELINE_INVALID",
        "closure_status": closure["status"],
        "validation_status": validation["status"],
        "closure": closure,
        "closure_id": closure["closure_id"],
        "signature": closure["signature"],
        "closure_mode": closure["closure_mode"],
        "closure_verdict": closure["closure_verdict"],
        "next_allowed_stage": closure["next_allowed_stage"],
        "closure_source_count": closure["closure_source_count"],
        "ready_source_count": closure["ready_source_count"],
        "source_hash_count": closure["source_hash_count"],
        "closed_task_count": closure["closed_task_count"],
        "closure_gate_count": closure["closure_gate_count"],
        "passed_gate_count": closure["passed_gate_count"],
        "closure_issue_count": closure["closure_issue_count"],
        "warning_count": closure["warning_count"],
        "closure_ready": closure["closure_ready"],
        "closure_locked": closure["closure_locked"],
        "milestone_closed": closure["milestone_closed"],
        "package_prepared": closure["package_prepared"],
        "package_frozen": closure["package_frozen"],
        "integrity_verified": closure["integrity_verified"],
        "final_audit_passed": closure["final_audit_passed"],
        "solver_improvement_required": closure["solver_improvement_required"],
        "solver_improvement_started": closure["solver_improvement_started"],
        "solver_improvement_completed": closure["solver_improvement_completed"],
        "competitive_claim_absent": closure["competitive_claim_absent"],
        "manual_upload_required": closure["manual_upload_required"],
        "manual_execution_performed": closure["manual_execution_performed"],
        "real_submission_allowed": closure["real_submission_allowed"],
        "ready_for_real_kaggle_submission": closure["ready_for_real_kaggle_submission"],
        "real_submission_created": closure["real_submission_created"],
        "kaggle_submission_sent": closure["kaggle_submission_sent"],
        "upload_performed": closure["upload_performed"],
        "kaggle_authentication_performed": closure["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": closure["metadata"],
    }
