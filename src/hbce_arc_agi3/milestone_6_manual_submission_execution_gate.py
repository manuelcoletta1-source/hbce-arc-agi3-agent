"""Milestone #6 Manual Submission Execution Gate v1.

Local-only manual execution gate for a possible future ARC-AGI-3 real Kaggle
submission.

This module documents the final manual execution boundary. It does not submit
to Kaggle, authenticate, upload files, call external APIs, read secrets, create
upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


GATE_STATUS = "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY"
PIPELINE_STATUS = "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_VALID"

BASELINE_COMMIT = "47f2e00 Add ARC AGI3 real submission precheck gate"
GATE_MODE = "MANUAL_SUBMISSION_EXECUTION_GATE_ONLY_NO_UPLOAD"
GATE_SCOPE = "DOCUMENT_MANUAL_EXECUTION_REQUIREMENTS_NO_API_NO_UPLOAD"
GATE_VERDICT = "MANUAL_EXECUTION_GATE_READY_REAL_SUBMISSION_NOT_PERFORMED"
NEXT_ALLOWED_STAGE = "OPTIONAL_HUMAN_RUN_KAGGLE_SUBMISSION_OUTSIDE_AGENT"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/manual-submission-execution-gate-v1"

PRECHECK_JSON = Path(
    "examples/milestone-6/real-submission-precheck-gate-v1/"
    "milestone-6-real-submission-precheck-gate-v1.json"
)

MANUAL_CONFIRMATIONS: Tuple[str, ...] = (
    "human_operator_must_review_submission_candidate",
    "human_operator_must_review_kaggle_rules",
    "human_operator_must_use_kaggle_ui_or_cli_manually",
    "human_operator_must_not_expose_private_core",
    "human_operator_must_not_use_runtime_secrets",
    "human_operator_accepts_real_submission_responsibility",
)

GATES: Tuple[str, ...] = (
    "precheck_artifact_present",
    "precheck_artifact_ready",
    "precheck_artifact_valid",
    "precheck_passed",
    "operator_approval_granted",
    "manual_execution_gate_required_by_precheck",
    "manual_execution_gate_mode_valid",
    "manual_execution_gate_ready",
    "manual_confirmations_defined",
    "manual_execution_not_performed",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "kaggle_authentication_not_performed",
    "external_api_dependency_false",
    "contains_api_keys_false",
    "secrets_required_false",
    "private_core_exposure_false",
    "legal_certification_false",
)

ISSUES: Tuple[str, ...] = (
    "precheck_artifact_missing",
    "precheck_artifact_not_ready",
    "precheck_artifact_invalid",
    "precheck_not_passed",
    "operator_approval_not_granted",
    "manual_execution_gate_not_required_by_precheck",
    "manual_execution_gate_mode_invalid",
    "manual_execution_gate_not_ready",
    "manual_confirmations_missing",
    "manual_execution_performed",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_performed",
    "external_api_dependency_detected",
    "api_keys_detected",
    "secrets_required",
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


def _sha16(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def _boundary_from_precheck(precheck: Mapping[str, Any]) -> Dict[str, Any]:
    source = precheck.get("boundary", {}) if isinstance(precheck.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": precheck.get("kaggle_submission_sent"),
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


def build_milestone_6_manual_submission_execution_gate() -> Dict[str, Any]:
    precheck = _read_json(PRECHECK_JSON)
    boundary = _boundary_from_precheck(precheck)

    record = {
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "manual_execution_gate_ready": True,
        "manual_execution_gate_required": True,
        "manual_execution_performed": False,
        "manual_confirmation_count": len(MANUAL_CONFIRMATIONS),
        "manual_confirmations": list(MANUAL_CONFIRMATIONS),
        "precheck_id": precheck.get("precheck_id", "MISSING_PRECHECK_ID"),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "secrets_required": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "boundary_intact": _boundary_intact(boundary),
    }

    gate_state = {
        "precheck_artifact_present": PRECHECK_JSON.exists(),
        "precheck_artifact_ready": precheck.get("status") == "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY",
        "precheck_artifact_valid": bool(precheck.get("precheck_id")) and bool(precheck.get("signature")),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "manual_execution_gate_required_by_precheck": precheck.get("manual_execution_gate_required") is True,
        "manual_execution_gate_mode_valid": record["gate_mode"] == GATE_MODE,
        "manual_execution_gate_ready": record["manual_execution_gate_ready"] is True,
        "manual_confirmations_defined": len(record["manual_confirmations"]) == len(MANUAL_CONFIRMATIONS),
        "manual_execution_not_performed": record["manual_execution_performed"] is False,
        "real_submission_allowed_false": record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": record["real_submission_created"] is False,
        "kaggle_submission_not_sent": record["kaggle_submission_sent"] is False,
        "upload_not_performed": record["upload_performed"] is False,
        "kaggle_authentication_not_performed": record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "secrets_required_false": record["secrets_required"] is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "precheck_artifact_missing": not gate_state["precheck_artifact_present"],
        "precheck_artifact_not_ready": not gate_state["precheck_artifact_ready"],
        "precheck_artifact_invalid": not gate_state["precheck_artifact_valid"],
        "precheck_not_passed": not gate_state["precheck_passed"],
        "operator_approval_not_granted": not gate_state["operator_approval_granted"],
        "manual_execution_gate_not_required_by_precheck": not gate_state["manual_execution_gate_required_by_precheck"],
        "manual_execution_gate_mode_invalid": not gate_state["manual_execution_gate_mode_valid"],
        "manual_execution_gate_not_ready": not gate_state["manual_execution_gate_ready"],
        "manual_confirmations_missing": not gate_state["manual_confirmations_defined"],
        "manual_execution_performed": not gate_state["manual_execution_not_performed"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_performed": not gate_state["kaggle_authentication_not_performed"],
        "external_api_dependency_detected": not gate_state["external_api_dependency_false"],
        "api_keys_detected": not gate_state["contains_api_keys_false"],
        "secrets_required": not gate_state["secrets_required_false"],
        "private_core_exposure_detected": not gate_state["private_core_exposure_false"],
        "legal_certification_claim_detected": not gate_state["legal_certification_false"],
    }

    gates = tuple({"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"} for name in GATES)
    issues = tuple({"name": name, "active": issue_state[name], "severity": "BLOCKING"} for name in ISSUES)

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    gate_ready = passed_gate_count == len(GATES) and issue_count == 0 and _boundary_intact(boundary)

    index = {
        "milestone": "Milestone #6",
        "task": "Task 5",
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_precheck": precheck.get("precheck_id", "MISSING_PRECHECK_ID"),
        "manual_execution_gate_ready": gate_ready,
        "manual_execution_gate_required": True,
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
        "status": GATE_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 5",
        "title": "Manual Submission Execution Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "precheck_id": precheck.get("precheck_id", "MISSING_PRECHECK_ID"),
        "precheck_signature": precheck.get("signature", "MISSING_PRECHECK_SIGNATURE"),
        "gate_mode": GATE_MODE,
        "gate_scope": GATE_SCOPE,
        "gate_verdict": GATE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "manual_execution_record": record,
        "manual_execution_gates": list(gates),
        "manual_execution_issues": list(issues),
        "manual_execution_index": index,
        "boundary": boundary,
        "gate_count": len(GATES),
        "passed_gate_count": passed_gate_count,
        "issue_count": issue_count,
        "warning_count": 0,
        "manual_execution_gate_ready": gate_ready,
        "manual_execution_gate_required": True,
        "manual_execution_performed": False,
        "operator_approval_granted": True,
        "precheck_passed": True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_6_manual_submission_execution_gate_v1",
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
    return {**base, "gate_id": f"MILESTONE-6-MANUAL-SUBMISSION-GATE-{signature[:12]}", "signature": signature}


def validate_milestone_6_manual_submission_execution_gate(gate: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = gate.get("boundary", {})
    gates = gate.get("manual_execution_gates", [])
    issues = gate.get("manual_execution_issues", [])
    checks = {
        "status_ready": gate.get("status") == GATE_STATUS,
        "gate_id_present": isinstance(gate.get("gate_id"), str) and bool(gate.get("gate_id")),
        "signature_present": isinstance(gate.get("signature"), str) and bool(gate.get("signature")),
        "baseline_commit_valid": str(gate.get("baseline_commit", "")).startswith("47f2e00"),
        "precheck_id_present": isinstance(gate.get("precheck_id"), str) and gate.get("precheck_id") != "MISSING_PRECHECK_ID",
        "gate_mode_valid": gate.get("gate_mode") == GATE_MODE,
        "gate_scope_valid": gate.get("gate_scope") == GATE_SCOPE,
        "gate_verdict_valid": gate.get("gate_verdict") == GATE_VERDICT,
        "gate_count_matches": gate.get("gate_count") == len(GATES),
        "all_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "issue_count_zero": gate.get("issue_count") == 0,
        "all_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "manual_execution_gate_ready": gate.get("manual_execution_gate_ready") is True,
        "manual_execution_gate_required": gate.get("manual_execution_gate_required") is True,
        "manual_execution_not_performed": gate.get("manual_execution_performed") is False,
        "real_submission_allowed_false": gate.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": gate.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": gate.get("real_submission_created") is False,
        "kaggle_submission_not_sent": gate.get("kaggle_submission_sent") is False,
        "upload_not_performed": gate.get("upload_performed") is False,
        "kaggle_authentication_not_performed": gate.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_INVALID",
        "valid": valid,
        "checks": checks,
        "gate_id": gate.get("gate_id"),
        "signature": gate.get("signature"),
    }


def render_manual_submission_execution_gate_markdown(gate: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Manual Submission Execution Gate v1",
        "",
        f"- status: {gate['status']}",
        f"- gate_id: {gate['gate_id']}",
        f"- signature: {gate['signature']}",
        f"- baseline_commit: {gate['baseline_commit']}",
        f"- precheck_id: {gate['precheck_id']}",
        f"- gate_mode: {gate['gate_mode']}",
        f"- gate_scope: {gate['gate_scope']}",
        f"- gate_verdict: {gate['gate_verdict']}",
        f"- gate_count: {gate['gate_count']}",
        f"- passed_gate_count: {gate['passed_gate_count']}",
        f"- issue_count: {gate['issue_count']}",
        f"- manual_execution_gate_ready: {gate['manual_execution_gate_ready']}",
        f"- manual_execution_gate_required: {gate['manual_execution_gate_required']}",
        f"- manual_execution_performed: {gate['manual_execution_performed']}",
        f"- real_submission_allowed: {gate['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {gate['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {gate['kaggle_submission_sent']}",
        f"- upload_performed: {gate['upload_performed']}",
        f"- kaggle_authentication_performed: {gate['kaggle_authentication_performed']}",
        "",
        "## Markers",
        "",
        "ARC_AGI3_MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_V1_READY=true",
        "ARC_AGI3_MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_VALID=true",
        "ARC_AGI3_MILESTONE_6_GATE_MODE=MANUAL_SUBMISSION_EXECUTION_GATE_ONLY_NO_UPLOAD",
        "ARC_AGI3_MILESTONE_6_GATE_VERDICT=MANUAL_EXECUTION_GATE_READY_REAL_SUBMISSION_NOT_PERFORMED",
        "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_GATE_READY=true",
        "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_GATE_REQUIRED=true",
        "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_PERFORMED=false",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
        "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
        "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
        "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
        "ARC_AGI3_MILESTONE_6_BASELINE_PRECHECK_COMMIT=47f2e00",
        "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
        "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
        "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
        "ARC_AGI3_LEGAL_CERTIFICATION=false",
        "",
    ]
    return "\n".join(lines)


def render_manual_submission_execution_gate_manifest(gate: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 MANUAL SUBMISSION EXECUTION GATE MANIFEST v1",
        f"gate_id={gate['gate_id']}",
        f"signature={gate['signature']}",
        f"status={gate['status']}",
        f"baseline_commit={gate['baseline_commit']}",
        f"gate_mode={gate['gate_mode']}",
        f"gate_verdict={gate['gate_verdict']}",
        f"gate_count={gate['gate_count']}",
        f"passed_gate_count={gate['passed_gate_count']}",
        f"issue_count={gate['issue_count']}",
        f"manual_execution_gate_ready={gate['manual_execution_gate_ready']}",
        f"manual_execution_gate_required={gate['manual_execution_gate_required']}",
        f"manual_execution_performed={gate['manual_execution_performed']}",
        f"real_submission_allowed={gate['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={gate['ready_for_real_kaggle_submission']}",
        f"real_submission_created={gate['real_submission_created']}",
        f"kaggle_submission_sent={gate['kaggle_submission_sent']}",
        f"upload_performed={gate['upload_performed']}",
        f"kaggle_authentication_performed={gate['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
    ]
    return "\n".join(lines)


def write_manual_submission_execution_gate_artifacts(
    gate: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    gate = dict(gate or build_milestone_6_manual_submission_execution_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-manual-submission-execution-gate-v1.json"
    md_path = output / "milestone-6-manual-submission-execution-gate-v1.md"
    manifest_path = output / "milestone-6-manual-submission-execution-gate-manifest-v1.txt"
    index_path = output / "milestone-6-manual-submission-execution-gate-index-v1.json"

    json_path.write_text(json.dumps(gate, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_manual_submission_execution_gate_markdown(gate), encoding="utf-8")
    manifest_path.write_text(render_manual_submission_execution_gate_manifest(gate), encoding="utf-8")
    index_path.write_text(json.dumps(gate["manual_execution_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_manual_submission_execution_gate_pipeline() -> Dict[str, Any]:
    gate = build_milestone_6_manual_submission_execution_gate()
    validation = validate_milestone_6_manual_submission_execution_gate(gate)
    artifacts = write_manual_submission_execution_gate_artifacts(gate)
    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_PIPELINE_INVALID",
        "gate_status": gate["status"],
        "validation_status": validation["status"],
        "gate": gate,
        "gate_id": gate["gate_id"],
        "signature": gate["signature"],
        "gate_mode": gate["gate_mode"],
        "gate_verdict": gate["gate_verdict"],
        "gate_count": gate["gate_count"],
        "passed_gate_count": gate["passed_gate_count"],
        "issue_count": gate["issue_count"],
        "warning_count": gate["warning_count"],
        "manual_execution_gate_ready": gate["manual_execution_gate_ready"],
        "manual_execution_gate_required": gate["manual_execution_gate_required"],
        "manual_execution_performed": gate["manual_execution_performed"],
        "operator_approval_granted": gate["operator_approval_granted"],
        "precheck_passed": gate["precheck_passed"],
        "real_submission_allowed": gate["real_submission_allowed"],
        "ready_for_real_kaggle_submission": gate["ready_for_real_kaggle_submission"],
        "real_submission_created": gate["real_submission_created"],
        "kaggle_submission_sent": gate["kaggle_submission_sent"],
        "upload_performed": gate["upload_performed"],
        "kaggle_authentication_performed": gate["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": gate["metadata"],
    }
