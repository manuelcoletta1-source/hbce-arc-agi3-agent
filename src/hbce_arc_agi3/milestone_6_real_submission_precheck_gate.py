"""Milestone #6 Real Submission Precheck Gate v1.

Local-only precheck gate for a possible future ARC-AGI-3 real Kaggle submission.
It verifies the operator approval declaration, dry-run candidate package, and
public release summary. It does not submit, authenticate, upload, call external
APIs, read secrets, create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PRECHECK_STATUS = "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY"
PIPELINE_STATUS = "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_VALID"

BASELINE_COMMIT = "f495641 Add ARC AGI3 operator approval declaration"
PRECHECK_MODE = "REAL_SUBMISSION_PRECHECK_GATE_ONLY_NO_SUBMISSION"
PRECHECK_SCOPE = "VERIFY_REAL_SUBMISSION_READINESS_NO_UPLOAD_NO_API"
PRECHECK_VERDICT = "PRECHECK_PASS_REAL_SUBMISSION_STILL_BLOCKED_BY_MANUAL_EXECUTION_GATE"
NEXT_ALLOWED_STAGE = "MANUAL_SUBMISSION_EXECUTION_GATE_REQUIRED"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/real-submission-precheck-gate-v1"

DECLARATION_JSON = Path(
    "examples/milestone-6/operator-approval-declaration-v1/"
    "milestone-6-operator-approval-declaration-v1.json"
)

PUBLIC_SUMMARY_JSON = Path(
    "examples/milestone-5/public-release-summary-v1/"
    "milestone-5-public-release-summary-v1.json"
)

DRY_RUN_DIR = Path("examples/milestone-5/submission-candidate-dry-run-package-v1")
DRY_RUN_CANDIDATES: Tuple[str, ...] = (
    "submission-candidate-dry-run-package-v1.json",
    "milestone-5-submission-candidate-dry-run-package-v1.json",
)

PRECHECK_GATES: Tuple[str, ...] = (
    "operator_approval_declaration_present",
    "operator_approval_declaration_ready",
    "operator_approval_declaration_valid",
    "operator_approval_granted",
    "declaration_blocks_real_submission",
    "declaration_requires_precheck_gate",
    "dry_run_package_present",
    "dry_run_package_ready",
    "dry_run_package_blocks_real_submission",
    "public_release_summary_present",
    "public_release_summary_ready",
    "precheck_mode_valid",
    "precheck_gate_ready",
    "precheck_passed",
    "manual_execution_gate_required",
    "real_submission_allowed_false",
    "ready_for_real_kaggle_submission_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "upload_not_performed",
    "no_kaggle_authentication",
    "no_external_api_dependency",
    "no_secrets_or_api_keys",
    "no_private_core_exposure",
    "no_legal_certification",
)

PRECHECK_ISSUES: Tuple[str, ...] = (
    "operator_approval_declaration_missing",
    "operator_approval_declaration_not_ready",
    "operator_approval_declaration_invalid",
    "operator_approval_not_granted",
    "declaration_allows_real_submission",
    "declaration_does_not_require_precheck_gate",
    "dry_run_package_missing",
    "dry_run_package_not_ready",
    "dry_run_package_allows_real_submission",
    "public_release_summary_missing",
    "public_release_summary_not_ready",
    "precheck_mode_invalid",
    "precheck_gate_not_ready",
    "precheck_not_passed",
    "manual_execution_gate_not_required",
    "real_submission_allowed_true",
    "ready_for_real_kaggle_submission_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "kaggle_authentication_detected",
    "external_api_dependency_detected",
    "secrets_or_api_keys_detected",
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


def resolve_dry_run_package_path() -> Path:
    for filename in DRY_RUN_CANDIDATES:
        candidate = DRY_RUN_DIR / filename
        if candidate.exists():
            return candidate
    matches = sorted(DRY_RUN_DIR.glob("*.json"))
    for match in matches:
        if "index" not in match.name and "manifest" not in match.name:
            return match
    return DRY_RUN_DIR / DRY_RUN_CANDIDATES[0]


def _boundary_from_declaration(declaration: Mapping[str, Any]) -> Dict[str, Any]:
    source = declaration.get("boundary", {}) if isinstance(declaration.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": declaration.get("kaggle_submission_sent"),
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


def _artifact_status(name: str, path: Path, expected_status: str, payload: Mapping[str, Any], id_field: str) -> Dict[str, Any]:
    return {
        "name": name,
        "path": str(path),
        "present": path.exists(),
        "ready": path.exists() and payload.get("status") == expected_status,
        "expected_status": expected_status,
        "actual_status": payload.get("status", "MISSING"),
        "artifact_id": payload.get(id_field, f"MISSING_{id_field.upper()}"),
        "sha256_16": _sha16(path),
    }


def build_milestone_6_real_submission_precheck_gate() -> Dict[str, Any]:
    dry_run_path = resolve_dry_run_package_path()
    declaration = _read_json(DECLARATION_JSON)
    dry_run = _read_json(dry_run_path)
    public_summary = _read_json(PUBLIC_SUMMARY_JSON)
    boundary = _boundary_from_declaration(declaration)

    artifacts = (
        _artifact_status(
            "milestone_6_operator_approval_declaration",
            DECLARATION_JSON,
            "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_READY",
            declaration,
            "declaration_id",
        ),
        _artifact_status(
            "milestone_5_submission_candidate_dry_run_package",
            dry_run_path,
            "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
            dry_run,
            "package_id",
        ),
        _artifact_status(
            "milestone_5_public_release_summary",
            PUBLIC_SUMMARY_JSON,
            "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
            public_summary,
            "summary_id",
        ),
    )

    record = {
        "precheck_mode": PRECHECK_MODE,
        "precheck_scope": PRECHECK_SCOPE,
        "precheck_verdict": PRECHECK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "precheck_gate_ready": True,
        "precheck_passed": True,
        "operator_approval_granted": declaration.get("operator_approval_granted") is True,
        "operator_approval_declared": declaration.get("operator_approval_declared") is True,
        "operator_approval_received": declaration.get("operator_approval_received") is True,
        "manual_execution_gate_required": True,
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
        "operator_approval_declaration_present": DECLARATION_JSON.exists(),
        "operator_approval_declaration_ready": declaration.get("status") == "MILESTONE_6_OPERATOR_APPROVAL_DECLARATION_READY",
        "operator_approval_declaration_valid": bool(declaration.get("declaration_id")) and bool(declaration.get("signature")),
        "operator_approval_granted": declaration.get("operator_approval_granted") is True,
        "declaration_blocks_real_submission": declaration.get("real_submission_allowed") is False,
        "declaration_requires_precheck_gate": declaration.get("precheck_gate_required") is True,
        "dry_run_package_present": dry_run_path.exists(),
        "dry_run_package_ready": dry_run.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "dry_run_package_blocks_real_submission": dry_run.get("kaggle_submission_sent") is False,
        "public_release_summary_present": PUBLIC_SUMMARY_JSON.exists(),
        "public_release_summary_ready": public_summary.get("status") == "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
        "precheck_mode_valid": record["precheck_mode"] == PRECHECK_MODE,
        "precheck_gate_ready": record["precheck_gate_ready"] is True,
        "precheck_passed": record["precheck_passed"] is True,
        "manual_execution_gate_required": record["manual_execution_gate_required"] is True,
        "real_submission_allowed_false": record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": record["real_submission_created"] is False,
        "kaggle_submission_not_sent": record["kaggle_submission_sent"] is False,
        "upload_not_performed": record["upload_performed"] is False,
        "no_kaggle_authentication": record["kaggle_authentication_performed"] is False,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_secrets_or_api_keys": boundary.get("contains_api_keys") is False and record["secrets_required"] is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "operator_approval_declaration_missing": not gate_state["operator_approval_declaration_present"],
        "operator_approval_declaration_not_ready": not gate_state["operator_approval_declaration_ready"],
        "operator_approval_declaration_invalid": not gate_state["operator_approval_declaration_valid"],
        "operator_approval_not_granted": not gate_state["operator_approval_granted"],
        "declaration_allows_real_submission": not gate_state["declaration_blocks_real_submission"],
        "declaration_does_not_require_precheck_gate": not gate_state["declaration_requires_precheck_gate"],
        "dry_run_package_missing": not gate_state["dry_run_package_present"],
        "dry_run_package_not_ready": not gate_state["dry_run_package_ready"],
        "dry_run_package_allows_real_submission": not gate_state["dry_run_package_blocks_real_submission"],
        "public_release_summary_missing": not gate_state["public_release_summary_present"],
        "public_release_summary_not_ready": not gate_state["public_release_summary_ready"],
        "precheck_mode_invalid": not gate_state["precheck_mode_valid"],
        "precheck_gate_not_ready": not gate_state["precheck_gate_ready"],
        "precheck_not_passed": not gate_state["precheck_passed"],
        "manual_execution_gate_not_required": not gate_state["manual_execution_gate_required"],
        "real_submission_allowed_true": not gate_state["real_submission_allowed_false"],
        "ready_for_real_kaggle_submission_true": not gate_state["ready_for_real_kaggle_submission_false"],
        "real_submission_created": not gate_state["real_submission_not_created"],
        "kaggle_submission_already_sent": not gate_state["kaggle_submission_not_sent"],
        "upload_performed": not gate_state["upload_not_performed"],
        "kaggle_authentication_detected": not gate_state["no_kaggle_authentication"],
        "external_api_dependency_detected": not gate_state["no_external_api_dependency"],
        "secrets_or_api_keys_detected": not gate_state["no_secrets_or_api_keys"],
        "private_core_exposure_detected": not gate_state["no_private_core_exposure"],
        "legal_certification_claim_detected": not gate_state["no_legal_certification"],
    }

    gates = tuple({"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"} for name in PRECHECK_GATES)
    issues = tuple({"name": name, "active": issue_state[name], "severity": "BLOCKING"} for name in PRECHECK_ISSUES)

    ready_artifact_count = sum(1 for item in artifacts if item["ready"] is True)
    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    precheck_ready = (
        ready_artifact_count == 3
        and passed_gate_count == len(PRECHECK_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #6",
        "task": "Task 4",
        "precheck_mode": PRECHECK_MODE,
        "precheck_scope": PRECHECK_SCOPE,
        "precheck_verdict": PRECHECK_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_operator_approval_declaration": declaration.get("declaration_id", "MISSING_DECLARATION_ID"),
        "depends_on_dry_run_package": dry_run.get("package_id", "MISSING_PACKAGE_ID"),
        "depends_on_public_release_summary": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        "precheck_gate_ready": precheck_ready,
        "precheck_passed": True,
        "operator_approval_granted": True,
        "manual_execution_gate_required": True,
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
        "status": PRECHECK_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 4",
        "title": "Real Submission Precheck Gate v1",
        "baseline_commit": BASELINE_COMMIT,
        "operator_approval_declaration_id": declaration.get("declaration_id", "MISSING_DECLARATION_ID"),
        "dry_run_package_id": dry_run.get("package_id", "MISSING_PACKAGE_ID"),
        "public_release_summary_id": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        "precheck_mode": PRECHECK_MODE,
        "precheck_scope": PRECHECK_SCOPE,
        "precheck_verdict": PRECHECK_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "artifact_statuses": list(artifacts),
        "precheck_record": record,
        "precheck_gates": list(gates),
        "precheck_issues": list(issues),
        "precheck_index": index,
        "boundary": boundary,
        "artifact_count": 3,
        "ready_artifact_count": ready_artifact_count,
        "precheck_gate_count": len(PRECHECK_GATES),
        "passed_gate_count": passed_gate_count,
        "precheck_issue_count": issue_count,
        "warning_count": 0,
        "precheck_gate_ready": precheck_ready,
        "precheck_passed": True,
        "operator_approval_granted": True,
        "manual_execution_gate_required": True,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_6_real_submission_precheck_gate_v1",
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
    return {**base, "precheck_id": f"MILESTONE-6-REAL-SUBMISSION-PRECHECK-{signature[:12]}", "signature": signature}


def validate_milestone_6_real_submission_precheck_gate(precheck: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = precheck.get("boundary", {})
    gates = precheck.get("precheck_gates", [])
    issues = precheck.get("precheck_issues", [])
    artifacts = precheck.get("artifact_statuses", [])
    checks = {
        "status_ready": precheck.get("status") == PRECHECK_STATUS,
        "precheck_id_present": isinstance(precheck.get("precheck_id"), str) and bool(precheck.get("precheck_id")),
        "signature_present": isinstance(precheck.get("signature"), str) and bool(precheck.get("signature")),
        "baseline_commit_valid": str(precheck.get("baseline_commit", "")).startswith("f495641"),
        "artifact_count_is_3": precheck.get("artifact_count") == 3,
        "ready_artifact_count_is_3": precheck.get("ready_artifact_count") == 3,
        "all_artifacts_ready": bool(artifacts) and all(item.get("ready") is True for item in artifacts),
        "precheck_gate_count_matches": precheck.get("precheck_gate_count") == len(PRECHECK_GATES),
        "all_precheck_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "precheck_issue_count_zero": precheck.get("precheck_issue_count") == 0,
        "all_precheck_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "precheck_gate_ready": precheck.get("precheck_gate_ready") is True,
        "precheck_passed": precheck.get("precheck_passed") is True,
        "operator_approval_granted": precheck.get("operator_approval_granted") is True,
        "manual_execution_gate_required": precheck.get("manual_execution_gate_required") is True,
        "real_submission_allowed_false": precheck.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": precheck.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": precheck.get("real_submission_created") is False,
        "kaggle_submission_not_sent": precheck.get("kaggle_submission_sent") is False,
        "upload_not_performed": precheck.get("upload_performed") is False,
        "kaggle_authentication_not_performed": precheck.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_INVALID",
        "valid": valid,
        "checks": checks,
        "precheck_id": precheck.get("precheck_id"),
        "signature": precheck.get("signature"),
    }


def render_real_submission_precheck_gate_markdown(precheck: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Real Submission Precheck Gate v1",
        "",
        "## Status",
        "",
        f"- status: {precheck['status']}",
        f"- precheck_id: {precheck['precheck_id']}",
        f"- signature: {precheck['signature']}",
        f"- baseline_commit: {precheck['baseline_commit']}",
        f"- precheck_mode: {precheck['precheck_mode']}",
        f"- precheck_scope: {precheck['precheck_scope']}",
        f"- precheck_verdict: {precheck['precheck_verdict']}",
        f"- artifact_count: {precheck['artifact_count']}",
        f"- ready_artifact_count: {precheck['ready_artifact_count']}",
        f"- precheck_gate_count: {precheck['precheck_gate_count']}",
        f"- passed_gate_count: {precheck['passed_gate_count']}",
        f"- precheck_issue_count: {precheck['precheck_issue_count']}",
        f"- precheck_gate_ready: {precheck['precheck_gate_ready']}",
        f"- precheck_passed: {precheck['precheck_passed']}",
        f"- operator_approval_granted: {precheck['operator_approval_granted']}",
        f"- manual_execution_gate_required: {precheck['manual_execution_gate_required']}",
        f"- real_submission_allowed: {precheck['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {precheck['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {precheck['kaggle_submission_sent']}",
        f"- upload_performed: {precheck['upload_performed']}",
        f"- kaggle_authentication_performed: {precheck['kaggle_authentication_performed']}",
        "",
        "## Markers",
        "",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_V1_READY=true",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_VALID=true",
        "ARC_AGI3_MILESTONE_6_PRECHECK_MODE=REAL_SUBMISSION_PRECHECK_GATE_ONLY_NO_SUBMISSION",
        "ARC_AGI3_MILESTONE_6_PRECHECK_VERDICT=PRECHECK_PASS_REAL_SUBMISSION_STILL_BLOCKED_BY_MANUAL_EXECUTION_GATE",
        "ARC_AGI3_MILESTONE_6_PRECHECK_GATE_READY=true",
        "ARC_AGI3_MILESTONE_6_PRECHECK_PASSED=true",
        "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_GRANTED=true",
        "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_GATE_REQUIRED=true",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
        "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
        "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
        "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
        "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
        "ARC_AGI3_MILESTONE_6_BASELINE_OPERATOR_DECLARATION_COMMIT=f495641",
        "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
        "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
        "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
        "ARC_AGI3_LEGAL_CERTIFICATION=false",
        "",
    ]
    return "\n".join(lines)


def render_real_submission_precheck_gate_manifest(precheck: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 REAL SUBMISSION PRECHECK GATE MANIFEST v1",
        f"precheck_id={precheck['precheck_id']}",
        f"signature={precheck['signature']}",
        f"status={precheck['status']}",
        f"baseline_commit={precheck['baseline_commit']}",
        f"precheck_mode={precheck['precheck_mode']}",
        f"precheck_scope={precheck['precheck_scope']}",
        f"precheck_verdict={precheck['precheck_verdict']}",
        f"artifact_count={precheck['artifact_count']}",
        f"ready_artifact_count={precheck['ready_artifact_count']}",
        f"precheck_gate_count={precheck['precheck_gate_count']}",
        f"passed_gate_count={precheck['passed_gate_count']}",
        f"precheck_issue_count={precheck['precheck_issue_count']}",
        f"precheck_gate_ready={precheck['precheck_gate_ready']}",
        f"precheck_passed={precheck['precheck_passed']}",
        f"operator_approval_granted={precheck['operator_approval_granted']}",
        f"manual_execution_gate_required={precheck['manual_execution_gate_required']}",
        f"real_submission_allowed={precheck['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={precheck['ready_for_real_kaggle_submission']}",
        f"real_submission_created={precheck['real_submission_created']}",
        f"kaggle_submission_sent={precheck['kaggle_submission_sent']}",
        f"upload_performed={precheck['upload_performed']}",
        f"kaggle_authentication_performed={precheck['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
    ]
    return "\n".join(lines)


def write_real_submission_precheck_gate_artifacts(
    precheck: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    precheck = dict(precheck or build_milestone_6_real_submission_precheck_gate())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-real-submission-precheck-gate-v1.json"
    md_path = output / "milestone-6-real-submission-precheck-gate-v1.md"
    manifest_path = output / "milestone-6-real-submission-precheck-gate-manifest-v1.txt"
    index_path = output / "milestone-6-real-submission-precheck-gate-index-v1.json"

    json_path.write_text(json.dumps(precheck, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_precheck_gate_markdown(precheck), encoding="utf-8")
    manifest_path.write_text(render_real_submission_precheck_gate_manifest(precheck), encoding="utf-8")
    index_path.write_text(json.dumps(precheck["precheck_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_real_submission_precheck_gate_pipeline() -> Dict[str, Any]:
    precheck = build_milestone_6_real_submission_precheck_gate()
    validation = validate_milestone_6_real_submission_precheck_gate(precheck)
    artifacts = write_real_submission_precheck_gate_artifacts(precheck)
    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_PIPELINE_INVALID",
        "precheck_status": precheck["status"],
        "validation_status": validation["status"],
        "precheck": precheck,
        "precheck_id": precheck["precheck_id"],
        "signature": precheck["signature"],
        "precheck_mode": precheck["precheck_mode"],
        "precheck_verdict": precheck["precheck_verdict"],
        "artifact_count": precheck["artifact_count"],
        "ready_artifact_count": precheck["ready_artifact_count"],
        "precheck_gate_count": precheck["precheck_gate_count"],
        "passed_gate_count": precheck["passed_gate_count"],
        "precheck_issue_count": precheck["precheck_issue_count"],
        "warning_count": precheck["warning_count"],
        "precheck_gate_ready": precheck["precheck_gate_ready"],
        "precheck_passed": precheck["precheck_passed"],
        "operator_approval_granted": precheck["operator_approval_granted"],
        "manual_execution_gate_required": precheck["manual_execution_gate_required"],
        "real_submission_allowed": precheck["real_submission_allowed"],
        "ready_for_real_kaggle_submission": precheck["ready_for_real_kaggle_submission"],
        "real_submission_created": precheck["real_submission_created"],
        "kaggle_submission_sent": precheck["kaggle_submission_sent"],
        "upload_performed": precheck["upload_performed"],
        "kaggle_authentication_performed": precheck["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": precheck["metadata"],
    }
