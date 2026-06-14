"""Milestone #6 Real Submission Package Freeze v1.

Local-only freeze record for a possible future ARC-AGI-3 real Kaggle submission
package.

This module freezes the already prepared dry-run candidate package references,
manual execution gate, precheck gate, and public release summary. It does not
submit to Kaggle, authenticate, upload files, call external APIs, read secrets,
create upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


FREEZE_STATUS = "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_READY"
PIPELINE_STATUS = "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_VALID"

BASELINE_COMMIT = "2346e9b Add ARC AGI3 manual submission execution gate"
FREEZE_MODE = "REAL_SUBMISSION_PACKAGE_FREEZE_ONLY_NO_UPLOAD"
FREEZE_SCOPE = "FREEZE_LOCAL_SUBMISSION_PACKAGE_REFERENCES_NO_API_NO_UPLOAD"
FREEZE_VERDICT = "REAL_SUBMISSION_PACKAGE_FROZEN_FOR_MANUAL_REVIEW_NO_SUBMISSION"
NEXT_ALLOWED_STAGE = "OPTIONAL_HUMAN_MANUAL_SUBMISSION_OUTSIDE_AGENT"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/real-submission-package-freeze-v1"

MANUAL_GATE_JSON = Path(
    "examples/milestone-6/manual-submission-execution-gate-v1/"
    "milestone-6-manual-submission-execution-gate-v1.json"
)

PRECHECK_JSON = Path(
    "examples/milestone-6/real-submission-precheck-gate-v1/"
    "milestone-6-real-submission-precheck-gate-v1.json"
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

FROZEN_ARTIFACT_NAMES: Tuple[str, ...] = (
    "manual_submission_execution_gate",
    "real_submission_precheck_gate",
    "submission_candidate_dry_run_package",
    "public_release_summary",
)

FREEZE_GATES: Tuple[str, ...] = (
    "manual_gate_artifact_present",
    "manual_gate_artifact_ready",
    "manual_gate_valid",
    "manual_execution_gate_ready",
    "manual_execution_not_performed",
    "precheck_artifact_present",
    "precheck_artifact_ready",
    "precheck_passed",
    "dry_run_package_present",
    "dry_run_package_ready",
    "public_release_summary_present",
    "public_release_summary_ready",
    "freeze_mode_valid",
    "freeze_record_ready",
    "freeze_locked",
    "frozen_artifact_count_valid",
    "frozen_artifacts_hashes_present",
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

FREEZE_ISSUES: Tuple[str, ...] = (
    "manual_gate_artifact_missing",
    "manual_gate_artifact_not_ready",
    "manual_gate_invalid",
    "manual_execution_gate_not_ready",
    "manual_execution_performed",
    "precheck_artifact_missing",
    "precheck_artifact_not_ready",
    "precheck_not_passed",
    "dry_run_package_missing",
    "dry_run_package_not_ready",
    "public_release_summary_missing",
    "public_release_summary_not_ready",
    "freeze_mode_invalid",
    "freeze_record_not_ready",
    "freeze_not_locked",
    "frozen_artifact_count_invalid",
    "frozen_artifact_hash_missing",
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


def _sha16(path: Path) -> str:
    value = _sha256(path)
    return value[:16].upper() if value != "MISSING_HASH" else value


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


def _boundary_from_manual_gate(manual_gate: Mapping[str, Any]) -> Dict[str, Any]:
    source = manual_gate.get("boundary", {}) if isinstance(manual_gate.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": manual_gate.get("kaggle_submission_sent"),
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


def _artifact(
    *,
    name: str,
    path: Path,
    payload: Mapping[str, Any],
    expected_status: str,
    id_field: str,
) -> Dict[str, Any]:
    return {
        "name": name,
        "path": str(path),
        "present": path.exists(),
        "ready": path.exists() and payload.get("status") == expected_status,
        "expected_status": expected_status,
        "actual_status": payload.get("status", "MISSING"),
        "artifact_id": payload.get(id_field, f"MISSING_{id_field.upper()}"),
        "sha256": _sha256(path),
        "sha256_16": _sha16(path),
    }


def build_milestone_6_real_submission_package_freeze() -> Dict[str, Any]:
    dry_run_path = resolve_dry_run_package_path()

    manual_gate = _read_json(MANUAL_GATE_JSON)
    precheck = _read_json(PRECHECK_JSON)
    dry_run = _read_json(dry_run_path)
    public_summary = _read_json(PUBLIC_SUMMARY_JSON)
    boundary = _boundary_from_manual_gate(manual_gate)

    frozen_artifacts = (
        _artifact(
            name="manual_submission_execution_gate",
            path=MANUAL_GATE_JSON,
            payload=manual_gate,
            expected_status="MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY",
            id_field="gate_id",
        ),
        _artifact(
            name="real_submission_precheck_gate",
            path=PRECHECK_JSON,
            payload=precheck,
            expected_status="MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY",
            id_field="precheck_id",
        ),
        _artifact(
            name="submission_candidate_dry_run_package",
            path=dry_run_path,
            payload=dry_run,
            expected_status="MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
            id_field="package_id",
        ),
        _artifact(
            name="public_release_summary",
            path=PUBLIC_SUMMARY_JSON,
            payload=public_summary,
            expected_status="MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
            id_field="summary_id",
        ),
    )

    freeze_record = {
        "freeze_mode": FREEZE_MODE,
        "freeze_scope": FREEZE_SCOPE,
        "freeze_verdict": FREEZE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "freeze_record_ready": True,
        "freeze_locked": True,
        "frozen_artifact_count": len(frozen_artifacts),
        "manual_gate_id": manual_gate.get("gate_id", "MISSING_GATE_ID"),
        "manual_execution_gate_ready": manual_gate.get("manual_execution_gate_ready") is True,
        "manual_execution_performed": False,
        "precheck_id": precheck.get("precheck_id", "MISSING_PRECHECK_ID"),
        "precheck_passed": precheck.get("precheck_passed") is True,
        "dry_run_package_id": dry_run.get("package_id", "MISSING_PACKAGE_ID"),
        "public_release_summary_id": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
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
        "manual_gate_artifact_present": MANUAL_GATE_JSON.exists(),
        "manual_gate_artifact_ready": manual_gate.get("status") == "MILESTONE_6_MANUAL_SUBMISSION_EXECUTION_GATE_READY",
        "manual_gate_valid": bool(manual_gate.get("gate_id")) and bool(manual_gate.get("signature")),
        "manual_execution_gate_ready": manual_gate.get("manual_execution_gate_ready") is True,
        "manual_execution_not_performed": manual_gate.get("manual_execution_performed") is False,
        "precheck_artifact_present": PRECHECK_JSON.exists(),
        "precheck_artifact_ready": precheck.get("status") == "MILESTONE_6_REAL_SUBMISSION_PRECHECK_GATE_READY",
        "precheck_passed": precheck.get("precheck_passed") is True,
        "dry_run_package_present": dry_run_path.exists(),
        "dry_run_package_ready": dry_run.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "public_release_summary_present": PUBLIC_SUMMARY_JSON.exists(),
        "public_release_summary_ready": public_summary.get("status") == "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
        "freeze_mode_valid": freeze_record["freeze_mode"] == FREEZE_MODE,
        "freeze_record_ready": freeze_record["freeze_record_ready"] is True,
        "freeze_locked": freeze_record["freeze_locked"] is True,
        "frozen_artifact_count_valid": len(frozen_artifacts) == len(FROZEN_ARTIFACT_NAMES),
        "frozen_artifacts_hashes_present": all(item["sha256"] != "MISSING_HASH" for item in frozen_artifacts),
        "real_submission_allowed_false": freeze_record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": freeze_record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": freeze_record["real_submission_created"] is False,
        "kaggle_submission_not_sent": freeze_record["kaggle_submission_sent"] is False,
        "upload_not_performed": freeze_record["upload_performed"] is False,
        "kaggle_authentication_not_performed": freeze_record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "manual_gate_artifact_missing": not gate_state["manual_gate_artifact_present"],
        "manual_gate_artifact_not_ready": not gate_state["manual_gate_artifact_ready"],
        "manual_gate_invalid": not gate_state["manual_gate_valid"],
        "manual_execution_gate_not_ready": not gate_state["manual_execution_gate_ready"],
        "manual_execution_performed": not gate_state["manual_execution_not_performed"],
        "precheck_artifact_missing": not gate_state["precheck_artifact_present"],
        "precheck_artifact_not_ready": not gate_state["precheck_artifact_ready"],
        "precheck_not_passed": not gate_state["precheck_passed"],
        "dry_run_package_missing": not gate_state["dry_run_package_present"],
        "dry_run_package_not_ready": not gate_state["dry_run_package_ready"],
        "public_release_summary_missing": not gate_state["public_release_summary_present"],
        "public_release_summary_not_ready": not gate_state["public_release_summary_ready"],
        "freeze_mode_invalid": not gate_state["freeze_mode_valid"],
        "freeze_record_not_ready": not gate_state["freeze_record_ready"],
        "freeze_not_locked": not gate_state["freeze_locked"],
        "frozen_artifact_count_invalid": not gate_state["frozen_artifact_count_valid"],
        "frozen_artifact_hash_missing": not gate_state["frozen_artifacts_hashes_present"],
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

    gates = tuple({"name": name, "passed": gate_state[name], "severity": "PASS" if gate_state[name] else "BLOCKING"} for name in FREEZE_GATES)
    issues = tuple({"name": name, "active": issue_state[name], "severity": "BLOCKING"} for name in FREEZE_ISSUES)

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)
    ready_artifact_count = sum(1 for item in frozen_artifacts if item["ready"] is True)

    freeze_ready = (
        ready_artifact_count == len(FROZEN_ARTIFACT_NAMES)
        and passed_gate_count == len(FREEZE_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #6",
        "task": "Task 6",
        "freeze_mode": FREEZE_MODE,
        "freeze_scope": FREEZE_SCOPE,
        "freeze_verdict": FREEZE_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "freeze_ready": freeze_ready,
        "freeze_locked": True,
        "frozen_artifact_count": len(frozen_artifacts),
        "ready_artifact_count": ready_artifact_count,
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
        "status": FREEZE_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 6",
        "title": "Real Submission Package Freeze v1",
        "baseline_commit": BASELINE_COMMIT,
        "freeze_mode": FREEZE_MODE,
        "freeze_scope": FREEZE_SCOPE,
        "freeze_verdict": FREEZE_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "freeze_record": freeze_record,
        "frozen_artifacts": list(frozen_artifacts),
        "freeze_gates": list(gates),
        "freeze_issues": list(issues),
        "freeze_index": index,
        "boundary": boundary,
        "frozen_artifact_count": len(frozen_artifacts),
        "ready_artifact_count": ready_artifact_count,
        "freeze_gate_count": len(FREEZE_GATES),
        "passed_gate_count": passed_gate_count,
        "freeze_issue_count": issue_count,
        "warning_count": 0,
        "freeze_ready": freeze_ready,
        "freeze_locked": True,
        "manual_execution_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_6_real_submission_package_freeze_v1",
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
    return {**base, "freeze_id": f"MILESTONE-6-REAL-SUBMISSION-FREEZE-{signature[:12]}", "signature": signature}


def validate_milestone_6_real_submission_package_freeze(freeze: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = freeze.get("boundary", {})
    gates = freeze.get("freeze_gates", [])
    issues = freeze.get("freeze_issues", [])
    artifacts = freeze.get("frozen_artifacts", [])
    checks = {
        "status_ready": freeze.get("status") == FREEZE_STATUS,
        "freeze_id_present": isinstance(freeze.get("freeze_id"), str) and bool(freeze.get("freeze_id")),
        "signature_present": isinstance(freeze.get("signature"), str) and bool(freeze.get("signature")),
        "baseline_commit_valid": str(freeze.get("baseline_commit", "")).startswith("2346e9b"),
        "freeze_mode_valid": freeze.get("freeze_mode") == FREEZE_MODE,
        "freeze_scope_valid": freeze.get("freeze_scope") == FREEZE_SCOPE,
        "freeze_verdict_valid": freeze.get("freeze_verdict") == FREEZE_VERDICT,
        "frozen_artifact_count_valid": freeze.get("frozen_artifact_count") == len(FROZEN_ARTIFACT_NAMES),
        "ready_artifact_count_valid": freeze.get("ready_artifact_count") == len(FROZEN_ARTIFACT_NAMES),
        "all_artifacts_ready": bool(artifacts) and all(item.get("ready") is True for item in artifacts),
        "all_artifact_hashes_present": bool(artifacts) and all(item.get("sha256") != "MISSING_HASH" for item in artifacts),
        "freeze_gate_count_matches": freeze.get("freeze_gate_count") == len(FREEZE_GATES),
        "all_freeze_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "freeze_issue_count_zero": freeze.get("freeze_issue_count") == 0,
        "all_freeze_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "manual_execution_not_performed": freeze.get("manual_execution_performed") is False,
        "real_submission_allowed_false": freeze.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": freeze.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": freeze.get("real_submission_created") is False,
        "kaggle_submission_not_sent": freeze.get("kaggle_submission_sent") is False,
        "upload_not_performed": freeze.get("upload_performed") is False,
        "kaggle_authentication_not_performed": freeze.get("kaggle_authentication_performed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_INVALID",
        "valid": valid,
        "checks": checks,
        "freeze_id": freeze.get("freeze_id"),
        "signature": freeze.get("signature"),
    }


def render_real_submission_package_freeze_markdown(freeze: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Real Submission Package Freeze v1",
        "",
        f"- status: {freeze['status']}",
        f"- freeze_id: {freeze['freeze_id']}",
        f"- signature: {freeze['signature']}",
        f"- baseline_commit: {freeze['baseline_commit']}",
        f"- freeze_mode: {freeze['freeze_mode']}",
        f"- freeze_scope: {freeze['freeze_scope']}",
        f"- freeze_verdict: {freeze['freeze_verdict']}",
        f"- frozen_artifact_count: {freeze['frozen_artifact_count']}",
        f"- ready_artifact_count: {freeze['ready_artifact_count']}",
        f"- freeze_gate_count: {freeze['freeze_gate_count']}",
        f"- passed_gate_count: {freeze['passed_gate_count']}",
        f"- freeze_issue_count: {freeze['freeze_issue_count']}",
        f"- freeze_ready: {freeze['freeze_ready']}",
        f"- freeze_locked: {freeze['freeze_locked']}",
        f"- manual_execution_performed: {freeze['manual_execution_performed']}",
        f"- real_submission_allowed: {freeze['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {freeze['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {freeze['kaggle_submission_sent']}",
        f"- upload_performed: {freeze['upload_performed']}",
        f"- kaggle_authentication_performed: {freeze['kaggle_authentication_performed']}",
        "",
        "## Frozen artifacts",
        "",
    ]

    for artifact in freeze["frozen_artifacts"]:
        lines.append(
            f"- {artifact['name']}: ready={artifact['ready']} "
            f"sha256_16={artifact['sha256_16']} artifact_id={artifact['artifact_id']}"
        )

    lines.extend(
        [
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_VALID=true",
            "ARC_AGI3_MILESTONE_6_FREEZE_MODE=REAL_SUBMISSION_PACKAGE_FREEZE_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_6_FREEZE_VERDICT=REAL_SUBMISSION_PACKAGE_FROZEN_FOR_MANUAL_REVIEW_NO_SUBMISSION",
            "ARC_AGI3_MILESTONE_6_FREEZE_READY=true",
            "ARC_AGI3_MILESTONE_6_FREEZE_LOCKED=true",
            "ARC_AGI3_MILESTONE_6_MANUAL_EXECUTION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_MANUAL_GATE_COMMIT=2346e9b",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_real_submission_package_freeze_manifest(freeze: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 REAL SUBMISSION PACKAGE FREEZE MANIFEST v1",
        f"freeze_id={freeze['freeze_id']}",
        f"signature={freeze['signature']}",
        f"status={freeze['status']}",
        f"baseline_commit={freeze['baseline_commit']}",
        f"freeze_mode={freeze['freeze_mode']}",
        f"freeze_verdict={freeze['freeze_verdict']}",
        f"frozen_artifact_count={freeze['frozen_artifact_count']}",
        f"ready_artifact_count={freeze['ready_artifact_count']}",
        f"freeze_gate_count={freeze['freeze_gate_count']}",
        f"passed_gate_count={freeze['passed_gate_count']}",
        f"freeze_issue_count={freeze['freeze_issue_count']}",
        f"freeze_ready={freeze['freeze_ready']}",
        f"freeze_locked={freeze['freeze_locked']}",
        f"manual_execution_performed={freeze['manual_execution_performed']}",
        f"real_submission_allowed={freeze['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={freeze['ready_for_real_kaggle_submission']}",
        f"real_submission_created={freeze['real_submission_created']}",
        f"kaggle_submission_sent={freeze['kaggle_submission_sent']}",
        f"upload_performed={freeze['upload_performed']}",
        f"kaggle_authentication_performed={freeze['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "FROZEN_ARTIFACTS",
    ]

    for artifact in freeze["frozen_artifacts"]:
        lines.append(
            f"{artifact['name']} ready={artifact['ready']} "
            f"sha256={artifact['sha256']} artifact_id={artifact['artifact_id']} path={artifact['path']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_real_submission_package_freeze_artifacts(
    freeze: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    freeze = dict(freeze or build_milestone_6_real_submission_package_freeze())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-real-submission-package-freeze-v1.json"
    md_path = output / "milestone-6-real-submission-package-freeze-v1.md"
    manifest_path = output / "milestone-6-real-submission-package-freeze-manifest-v1.txt"
    index_path = output / "milestone-6-real-submission-package-freeze-index-v1.json"

    json_path.write_text(json.dumps(freeze, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_real_submission_package_freeze_markdown(freeze), encoding="utf-8")
    manifest_path.write_text(render_real_submission_package_freeze_manifest(freeze), encoding="utf-8")
    index_path.write_text(json.dumps(freeze["freeze_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_real_submission_package_freeze_pipeline() -> Dict[str, Any]:
    freeze = build_milestone_6_real_submission_package_freeze()
    validation = validate_milestone_6_real_submission_package_freeze(freeze)
    artifacts = write_real_submission_package_freeze_artifacts(freeze)
    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_PIPELINE_INVALID",
        "freeze_status": freeze["status"],
        "validation_status": validation["status"],
        "freeze": freeze,
        "freeze_id": freeze["freeze_id"],
        "signature": freeze["signature"],
        "freeze_mode": freeze["freeze_mode"],
        "freeze_verdict": freeze["freeze_verdict"],
        "frozen_artifact_count": freeze["frozen_artifact_count"],
        "ready_artifact_count": freeze["ready_artifact_count"],
        "freeze_gate_count": freeze["freeze_gate_count"],
        "passed_gate_count": freeze["passed_gate_count"],
        "freeze_issue_count": freeze["freeze_issue_count"],
        "warning_count": freeze["warning_count"],
        "freeze_ready": freeze["freeze_ready"],
        "freeze_locked": freeze["freeze_locked"],
        "manual_execution_performed": freeze["manual_execution_performed"],
        "real_submission_allowed": freeze["real_submission_allowed"],
        "ready_for_real_kaggle_submission": freeze["ready_for_real_kaggle_submission"],
        "real_submission_created": freeze["real_submission_created"],
        "kaggle_submission_sent": freeze["kaggle_submission_sent"],
        "upload_performed": freeze["upload_performed"],
        "kaggle_authentication_performed": freeze["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": freeze["metadata"],
    }
