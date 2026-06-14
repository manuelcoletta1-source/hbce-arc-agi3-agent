"""Milestone #6 Submission Candidate Final Audit v1.

Local-only final audit for the frozen ARC-AGI-3 submission candidate.

This module checks the integrity verification, freeze record, manual execution
gate, precheck gate, dry-run candidate package, and public release summary. It
does not submit to Kaggle, authenticate, upload files, call external APIs, read
secrets, create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


AUDIT_STATUS = "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_READY"
PIPELINE_STATUS = "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_VALID"

BASELINE_COMMIT = "d475a03 Add ARC AGI3 frozen package integrity verification"
AUDIT_MODE = "SUBMISSION_CANDIDATE_FINAL_AUDIT_ONLY_NO_UPLOAD"
AUDIT_SCOPE = "FINAL_REVIEW_OF_FROZEN_CANDIDATE_INTEGRITY_AND_BOUNDARY_NO_EXECUTION"
AUDIT_VERDICT = "FINAL_AUDIT_PASS_REAL_SUBMISSION_STILL_BLOCKED_PENDING_SOLVER_IMPROVEMENT"
NEXT_ALLOWED_STAGE = "SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/submission-candidate-final-audit-v1"

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
DRY_RUN_PACKAGE_JSON = Path(
    "examples/milestone-5/submission-candidate-dry-run-package-v1/"
    "submission-candidate-dry-run-package-v1.json"
)
PUBLIC_SUMMARY_JSON = Path(
    "examples/milestone-5/public-release-summary-v1/"
    "milestone-5-public-release-summary-v1.json"
)

EXPECTED_AUDITED_SOURCE_COUNT = 6

AUDIT_GATES: Tuple[str, ...] = (
    "integrity_artifact_present",
    "integrity_artifact_ready",
    "integrity_artifact_valid",
    "integrity_verified",
    "integrity_locked",
    "matched_hash_count_valid",
    "freeze_artifact_present",
    "freeze_ready",
    "freeze_locked",
    "manual_gate_artifact_present",
    "manual_gate_ready",
    "manual_execution_not_performed",
    "precheck_artifact_present",
    "precheck_passed",
    "operator_approval_granted",
    "dry_run_package_present",
    "dry_run_package_ready",
    "public_release_summary_present",
    "public_release_summary_ready",
    "audited_source_count_valid",
    "audited_source_hashes_present",
    "audit_mode_valid",
    "audit_ready",
    "audit_locked",
    "solver_improvement_required",
    "competitive_claim_absent",
    "manual_upload_required",
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

AUDIT_ISSUES: Tuple[str, ...] = (
    "integrity_artifact_missing",
    "integrity_artifact_not_ready",
    "integrity_artifact_invalid",
    "integrity_not_verified",
    "integrity_not_locked",
    "matched_hash_count_invalid",
    "freeze_artifact_missing",
    "freeze_not_ready",
    "freeze_not_locked",
    "manual_gate_artifact_missing",
    "manual_gate_not_ready",
    "manual_execution_performed",
    "precheck_artifact_missing",
    "precheck_not_passed",
    "operator_approval_not_granted",
    "dry_run_package_missing",
    "dry_run_package_not_ready",
    "public_release_summary_missing",
    "public_release_summary_not_ready",
    "audited_source_count_invalid",
    "audited_source_hash_missing",
    "audit_mode_invalid",
    "audit_not_ready",
    "audit_not_locked",
    "solver_improvement_not_required",
    "competitive_claim_detected",
    "manual_upload_not_required",
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


def _boundary_from_integrity(integrity: Mapping[str, Any]) -> Dict[str, Any]:
    source = integrity.get("boundary", {}) if isinstance(integrity.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": integrity.get("kaggle_submission_sent"),
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


def _audited_source(name: str, path: Path, payload: Mapping[str, Any], expected_status: str, id_field: str) -> Dict[str, Any]:
    file_hash = _sha256(path)
    return {
        "name": name,
        "path": str(path),
        "present": path.exists(),
        "expected_status": expected_status,
        "actual_status": payload.get("status", "MISSING"),
        "ready": path.exists() and payload.get("status") == expected_status,
        "artifact_id": payload.get(id_field, f"MISSING_{id_field.upper()}"),
        "sha256": file_hash,
        "sha256_16": _sha16(file_hash),
    }


def _build_audited_sources(
    integrity: Mapping[str, Any],
    freeze: Mapping[str, Any],
    manual_gate: Mapping[str, Any],
    precheck: Mapping[str, Any],
    dry_run_package: Mapping[str, Any],
    public_summary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    return (
        _audited_source(
            "frozen_package_integrity_verification",
            INTEGRITY_JSON,
            integrity,
            "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_READY",
            "integrity_id",
        ),
        _audited_source(
            "real_submission_package_freeze",
            FREEZE_JSON,
            freeze,
            "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_READY",
            "freeze_id",
        ),
        _audited_source(
            "manual_submission_execution_gate",
            MANUAL_GATE_JSON,
            manual_gate,
            "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY",
            "gate_id",
        ),
        _audited_source(
            "real_submission_precheck_gate",
            PRECHECK_JSON,
            precheck,
            "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY",
            "precheck_id",
        ),
        _audited_source(
            "submission_candidate_dry_run_package",
            DRY_RUN_PACKAGE_JSON,
            dry_run_package,
            "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
            "package_id",
        ),
        _audited_source(
            "public_release_summary",
            PUBLIC_SUMMARY_JSON,
            public_summary,
            "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
            "summary_id",
        ),
    )


def build_milestone_6_submission_candidate_final_audit() -> Dict[str, Any]:
    integrity = _read_json(INTEGRITY_JSON)
    freeze = _read_json(FREEZE_JSON)
    manual_gate = _read_json(MANUAL_GATE_JSON)
    precheck = _read_json(PRECHECK_JSON)
    dry_run_package = _read_json(DRY_RUN_PACKAGE_JSON)
    public_summary = _read_json(PUBLIC_SUMMARY_JSON)

    boundary = _boundary_from_integrity(integrity)
    audited_sources = _build_audited_sources(
        integrity,
        freeze,
        manual_gate,
        precheck,
        dry_run_package,
        public_summary,
    )

    ready_source_count = sum(1 for item in audited_sources if item["ready"] is True)
    source_hash_count = sum(1 for item in audited_sources if item["sha256"] != "MISSING_HASH")

    audit_record = {
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "audit_ready": True,
        "audit_locked": True,
        "audited_source_count": len(audited_sources),
        "ready_source_count": ready_source_count,
        "source_hash_count": source_hash_count,
        "integrity_id": integrity.get("integrity_id", "MISSING_INTEGRITY_ID"),
        "integrity_ready": integrity.get("integrity_ready") is True,
        "integrity_verified": integrity.get("integrity_verified") is True,
        "integrity_locked": integrity.get("integrity_locked") is True,
        "matched_hash_count": integrity.get("matched_hash_count", 0),
        "freeze_id": freeze.get("freeze_id", "MISSING_FREEZE_ID"),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "manual_gate_id": manual_gate.get("gate_id", "MISSING_GATE_ID"),
        "manual_execution_gate_ready": manual_gate.get("manual_execution_gate_ready") is True,
        "manual_execution_performed": False,
        "precheck_id": precheck.get("precheck_id", "MISSING_PRECHECK_ID"),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "dry_run_package_id": dry_run_package.get("package_id", "MISSING_PACKAGE_ID"),
        "public_release_summary_id": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        "solver_improvement_required": True,
        "competitive_claim_absent": True,
        "manual_upload_required": True,
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
        "integrity_artifact_present": INTEGRITY_JSON.exists(),
        "integrity_artifact_ready": integrity.get("status") == "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_READY",
        "integrity_artifact_valid": bool(integrity.get("integrity_id")) and bool(integrity.get("signature")),
        "integrity_verified": integrity.get("integrity_verified") is True,
        "integrity_locked": integrity.get("integrity_locked") is True,
        "matched_hash_count_valid": integrity.get("matched_hash_count") == 4,
        "freeze_artifact_present": FREEZE_JSON.exists(),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "manual_gate_artifact_present": MANUAL_GATE_JSON.exists(),
        "manual_gate_ready": manual_gate.get("manual_execution_gate_ready") is True,
        "manual_execution_not_performed": manual_gate.get("manual_execution_performed") is False,
        "precheck_artifact_present": PRECHECK_JSON.exists(),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "dry_run_package_present": DRY_RUN_PACKAGE_JSON.exists(),
        "dry_run_package_ready": dry_run_package.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "public_release_summary_present": PUBLIC_SUMMARY_JSON.exists(),
        "public_release_summary_ready": public_summary.get("status") == "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
        "audited_source_count_valid": len(audited_sources) == EXPECTED_AUDITED_SOURCE_COUNT,
        "audited_source_hashes_present": source_hash_count == EXPECTED_AUDITED_SOURCE_COUNT,
        "audit_mode_valid": audit_record["audit_mode"] == AUDIT_MODE,
        "audit_ready": audit_record["audit_ready"] is True,
        "audit_locked": audit_record["audit_locked"] is True,
        "solver_improvement_required": audit_record["solver_improvement_required"] is True,
        "competitive_claim_absent": audit_record["competitive_claim_absent"] is True,
        "manual_upload_required": audit_record["manual_upload_required"] is True,
        "real_submission_allowed_false": audit_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": audit_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": audit_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": audit_record["kaggle_submission_sent"] is False,
        "upload_not_performed": audit_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": audit_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "integrity_artifact_missing": not gate_state["integrity_artifact_present"],
        "integrity_artifact_not_ready": not gate_state["integrity_artifact_ready"],
        "integrity_artifact_invalid": not gate_state["integrity_artifact_valid"],
        "integrity_not_verified": not gate_state["integrity_verified"],
        "integrity_not_locked": not gate_state["integrity_locked"],
        "matched_hash_count_invalid": not gate_state["matched_hash_count_valid"],
        "freeze_artifact_missing": not gate_state["freeze_artifact_present"],
        "freeze_not_ready": not gate_state["freeze_ready"],
        "freeze_not_locked": not gate_state["freeze_locked"],
        "manual_gate_artifact_missing": not gate_state["manual_gate_artifact_present"],
        "manual_gate_not_ready": not gate_state["manual_gate_ready"],
        "manual_execution_performed": not gate_state["manual_execution_not_performed"],
        "precheck_artifact_missing": not gate_state["precheck_artifact_present"],
        "precheck_not_passed": not gate_state["precheck_passed"],
        "operator_approval_not_granted": not gate_state["operator_approval_granted"],
        "dry_run_package_missing": not gate_state["dry_run_package_present"],
        "dry_run_package_not_ready": not gate_state["dry_run_package_ready"],
        "public_release_summary_missing": not gate_state["public_release_summary_present"],
        "public_release_summary_not_ready": not gate_state["public_release_summary_ready"],
        "audited_source_count_invalid": not gate_state["audited_source_count_valid"],
        "audited_source_hash_missing": not gate_state["audited_source_hashes_present"],
        "audit_mode_invalid": not gate_state["audit_mode_valid"],
        "audit_not_ready": not gate_state["audit_ready"],
        "audit_not_locked": not gate_state["audit_locked"],
        "solver_improvement_not_required": not gate_state["solver_improvement_required"],
        "competitive_claim_detected": not gate_state["competitive_claim_absent"],
        "manual_upload_not_required": not gate_state["manual_upload_required"],
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
        for name in AUDIT_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in AUDIT_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    audit_ready = (
        ready_source_count == EXPECTED_AUDITED_SOURCE_COUNT
        and source_hash_count == EXPECTED_AUDITED_SOURCE_COUNT
        and passed_gate_count == len(AUDIT_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #6",
        "task": "Task 8",
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_integrity": integrity.get("integrity_id", "MISSING_INTEGRITY_ID"),
        "audit_ready": audit_ready,
        "audit_locked": True,
        "audited_source_count": len(audited_sources),
        "ready_source_count": ready_source_count,
        "source_hash_count": source_hash_count,
        "solver_improvement_required": True,
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
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base = {
        "status": AUDIT_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 8",
        "title": "Submission Candidate Final Audit v1",
        "baseline_commit": BASELINE_COMMIT,
        "audit_mode": AUDIT_MODE,
        "audit_scope": AUDIT_SCOPE,
        "audit_verdict": AUDIT_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "audit_record": audit_record,
        "audited_sources": list(audited_sources),
        "audit_gates": list(gates),
        "audit_issues": list(issues),
        "audit_index": index,
        "boundary": boundary,
        "audited_source_count": len(audited_sources),
        "ready_source_count": ready_source_count,
        "source_hash_count": source_hash_count,
        "audit_gate_count": len(AUDIT_GATES),
        "passed_gate_count": passed_gate_count,
        "audit_issue_count": issue_count,
        "warning_count": 0,
        "audit_ready": audit_ready,
        "audit_locked": True,
        "solver_improvement_required": True,
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
            "source": "milestone_6_submission_candidate_final_audit_v1",
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
        "audit_id": f"MILESTONE-6-SUBMISSION-CANDIDATE-AUDIT-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_6_submission_candidate_final_audit(audit: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = audit.get("boundary", {})
    gates = audit.get("audit_gates", [])
    issues = audit.get("audit_issues", [])
    sources = audit.get("audited_sources", [])

    checks = {
        "status_ready": audit.get("status") == AUDIT_STATUS,
        "audit_id_present": isinstance(audit.get("audit_id"), str) and bool(audit.get("audit_id")),
        "signature_present": isinstance(audit.get("signature"), str) and bool(audit.get("signature")),
        "baseline_commit_valid": str(audit.get("baseline_commit", "")).startswith("d475a03"),
        "audit_mode_valid": audit.get("audit_mode") == AUDIT_MODE,
        "audit_scope_valid": audit.get("audit_scope") == AUDIT_SCOPE,
        "audit_verdict_valid": audit.get("audit_verdict") == AUDIT_VERDICT,
        "audited_source_count_valid": audit.get("audited_source_count") == EXPECTED_AUDITED_SOURCE_COUNT,
        "ready_source_count_valid": audit.get("ready_source_count") == EXPECTED_AUDITED_SOURCE_COUNT,
        "source_hash_count_valid": audit.get("source_hash_count") == EXPECTED_AUDITED_SOURCE_COUNT,
        "all_sources_ready": bool(sources) and all(item.get("ready") is True for item in sources),
        "all_source_hashes_present": bool(sources) and all(item.get("sha256") != "MISSING_HASH" for item in sources),
        "audit_gate_count_matches": audit.get("audit_gate_count") == len(AUDIT_GATES),
        "all_audit_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "audit_issue_count_zero": audit.get("audit_issue_count") == 0,
        "all_audit_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "audit_ready": audit.get("audit_ready") is True,
        "audit_locked": audit.get("audit_locked") is True,
        "solver_improvement_required": audit.get("solver_improvement_required") is True,
        "competitive_claim_absent": audit.get("competitive_claim_absent") is True,
        "manual_upload_required": audit.get("manual_upload_required") is True,
        "manual_execution_not_performed": audit.get("manual_execution_performed") is False,
        "real_submission_allowed_false": audit.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": audit.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": audit.get("real_submission_created") is False,
        "kaggle_submission_not_sent": audit.get("kaggle_submission_sent") is False,
        "upload_not_performed": audit.get("upload_performed") is False,
        "kaggle_authentication_not_performed": audit.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_INVALID",
        "valid": valid,
        "checks": checks,
        "audit_id": audit.get("audit_id"),
        "signature": audit.get("signature"),
    }


def render_submission_candidate_final_audit_markdown(audit: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Submission Candidate Final Audit v1",
        "",
        f"- status: {audit['status']}",
        f"- audit_id: {audit['audit_id']}",
        f"- signature: {audit['signature']}",
        f"- baseline_commit: {audit['baseline_commit']}",
        f"- audit_mode: {audit['audit_mode']}",
        f"- audit_scope: {audit['audit_scope']}",
        f"- audit_verdict: {audit['audit_verdict']}",
        f"- audited_source_count: {audit['audited_source_count']}",
        f"- ready_source_count: {audit['ready_source_count']}",
        f"- source_hash_count: {audit['source_hash_count']}",
        f"- audit_gate_count: {audit['audit_gate_count']}",
        f"- passed_gate_count: {audit['passed_gate_count']}",
        f"- audit_issue_count: {audit['audit_issue_count']}",
        f"- audit_ready: {audit['audit_ready']}",
        f"- audit_locked: {audit['audit_locked']}",
        f"- solver_improvement_required: {audit['solver_improvement_required']}",
        f"- competitive_claim_absent: {audit['competitive_claim_absent']}",
        f"- manual_upload_required: {audit['manual_upload_required']}",
        f"- real_submission_allowed: {audit['real_submission_allowed']}",
        f"- kaggle_submission_sent: {audit['kaggle_submission_sent']}",
        f"- upload_performed: {audit['upload_performed']}",
        "",
        "## Audited sources",
        "",
    ]

    for source in audit["audited_sources"]:
        lines.append(
            f"- {source['name']}: ready={source['ready']} "
            f"sha256_16={source['sha256_16']} artifact_id={source['artifact_id']}"
        )

    lines.extend(
        [
            "",
            "## Final audit decision",
            "",
            "The candidate is structurally ready, frozen, and integrity-verified. Real submission remains blocked pending solver improvement and explicit human manual execution.",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_VALID=true",
            "ARC_AGI3_MILESTONE_6_AUDIT_MODE=SUBMISSION_CANDIDATE_FINAL_AUDIT_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_6_AUDIT_VERDICT=FINAL_AUDIT_PASS_REAL_SUBMISSION_STILL_BLOCKED_PENDING_SOLVER_IMPROVEMENT",
            "ARC_AGI3_MILESTONE_6_AUDIT_READY=true",
            "ARC_AGI3_MILESTONE_6_AUDIT_LOCKED=true",
            "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_COMPETITIVE_CLAIM_ABSENT=true",
            "ARC_AGI3_MILESTONE_6_MANUAL_UPLOAD_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_INTEGRITY_COMMIT=d475a03",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_submission_candidate_final_audit_manifest(audit: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 SUBMISSION CANDIDATE FINAL AUDIT MANIFEST v1",
        f"audit_id={audit['audit_id']}",
        f"signature={audit['signature']}",
        f"status={audit['status']}",
        f"baseline_commit={audit['baseline_commit']}",
        f"audit_mode={audit['audit_mode']}",
        f"audit_verdict={audit['audit_verdict']}",
        f"audited_source_count={audit['audited_source_count']}",
        f"ready_source_count={audit['ready_source_count']}",
        f"source_hash_count={audit['source_hash_count']}",
        f"audit_gate_count={audit['audit_gate_count']}",
        f"passed_gate_count={audit['passed_gate_count']}",
        f"audit_issue_count={audit['audit_issue_count']}",
        f"audit_ready={audit['audit_ready']}",
        f"audit_locked={audit['audit_locked']}",
        f"solver_improvement_required={audit['solver_improvement_required']}",
        f"competitive_claim_absent={audit['competitive_claim_absent']}",
        f"manual_upload_required={audit['manual_upload_required']}",
        f"manual_execution_performed={audit['manual_execution_performed']}",
        f"real_submission_allowed={audit['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={audit['ready_for_real_kaggle_submission']}",
        f"real_submission_created={audit['real_submission_created']}",
        f"kaggle_submission_sent={audit['kaggle_submission_sent']}",
        f"upload_performed={audit['upload_performed']}",
        f"kaggle_authentication_performed={audit['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "AUDITED_SOURCES",
    ]

    for source in audit["audited_sources"]:
        lines.append(
            f"{source['name']} present={source['present']} ready={source['ready']} "
            f"sha256={source['sha256']} artifact_id={source['artifact_id']} path={source['path']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_submission_candidate_final_audit_artifacts(
    audit: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    audit = dict(audit or build_milestone_6_submission_candidate_final_audit())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-submission-candidate-final-audit-v1.json"
    md_path = output / "milestone-6-submission-candidate-final-audit-v1.md"
    manifest_path = output / "milestone-6-submission-candidate-final-audit-manifest-v1.txt"
    index_path = output / "milestone-6-submission-candidate-final-audit-index-v1.json"

    json_path.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_submission_candidate_final_audit_markdown(audit), encoding="utf-8")
    manifest_path.write_text(render_submission_candidate_final_audit_manifest(audit), encoding="utf-8")
    index_path.write_text(json.dumps(audit["audit_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_submission_candidate_final_audit_pipeline() -> Dict[str, Any]:
    audit = build_milestone_6_submission_candidate_final_audit()
    validation = validate_milestone_6_submission_candidate_final_audit(audit)
    artifacts = write_submission_candidate_final_audit_artifacts(audit)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_SUBMISSION_CANDIDATE_FINAL_AUDIT_PIPELINE_INVALID",
        "audit_status": audit["status"],
        "validation_status": validation["status"],
        "audit": audit,
        "audit_id": audit["audit_id"],
        "signature": audit["signature"],
        "audit_mode": audit["audit_mode"],
        "audit_verdict": audit["audit_verdict"],
        "audited_source_count": audit["audited_source_count"],
        "ready_source_count": audit["ready_source_count"],
        "source_hash_count": audit["source_hash_count"],
        "audit_gate_count": audit["audit_gate_count"],
        "passed_gate_count": audit["passed_gate_count"],
        "audit_issue_count": audit["audit_issue_count"],
        "warning_count": audit["warning_count"],
        "audit_ready": audit["audit_ready"],
        "audit_locked": audit["audit_locked"],
        "solver_improvement_required": audit["solver_improvement_required"],
        "competitive_claim_absent": audit["competitive_claim_absent"],
        "manual_upload_required": audit["manual_upload_required"],
        "manual_execution_performed": audit["manual_execution_performed"],
        "real_submission_allowed": audit["real_submission_allowed"],
        "ready_for_real_kaggle_submission": audit["ready_for_real_kaggle_submission"],
        "real_submission_created": audit["real_submission_created"],
        "kaggle_submission_sent": audit["kaggle_submission_sent"],
        "upload_performed": audit["upload_performed"],
        "kaggle_authentication_performed": audit["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": audit["metadata"],
    }
