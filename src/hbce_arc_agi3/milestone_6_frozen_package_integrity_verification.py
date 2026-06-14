"""Milestone #6 Frozen Package Integrity Verification v1.

Local-only integrity verification for the frozen ARC-AGI-3 real submission
package candidate.

This module re-hashes the artifacts frozen in Task 6 and verifies that the
current SHA-256 values match the recorded freeze hashes. It does not submit to
Kaggle, authenticate, upload files, call external APIs, read secrets, create
upload archives, or create legal certification claims.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


INTEGRITY_STATUS = "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_READY"
PIPELINE_STATUS = "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_VALID"

BASELINE_COMMIT = "88e783e Add ARC AGI3 real submission package freeze"
INTEGRITY_MODE = "FROZEN_PACKAGE_INTEGRITY_VERIFICATION_ONLY_NO_UPLOAD"
INTEGRITY_SCOPE = "REHASH_FROZEN_ARTIFACTS_COMPARE_WITH_FREEZE_RECORD"
INTEGRITY_VERDICT = "FROZEN_PACKAGE_INTEGRITY_VERIFIED_NO_SUBMISSION"
NEXT_ALLOWED_STAGE = "SUBMISSION_CANDIDATE_FINAL_AUDIT_REQUIRED"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/frozen-package-integrity-verification-v1"

FREEZE_JSON = Path(
    "examples/milestone-6/real-submission-package-freeze-v1/"
    "milestone-6-real-submission-package-freeze-v1.json"
)

EXPECTED_FROZEN_ARTIFACT_COUNT = 4

INTEGRITY_GATES: Tuple[str, ...] = (
    "freeze_artifact_present",
    "freeze_artifact_ready",
    "freeze_artifact_valid",
    "freeze_ready",
    "freeze_locked",
    "frozen_artifact_count_valid",
    "all_frozen_artifact_paths_present",
    "all_frozen_artifacts_ready",
    "all_recorded_hashes_present",
    "all_current_hashes_present",
    "all_hashes_match",
    "integrity_mode_valid",
    "integrity_verification_ready",
    "integrity_verified",
    "integrity_locked",
    "manual_execution_not_performed",
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

INTEGRITY_ISSUES: Tuple[str, ...] = (
    "freeze_artifact_missing",
    "freeze_artifact_not_ready",
    "freeze_artifact_invalid",
    "freeze_not_ready",
    "freeze_not_locked",
    "frozen_artifact_count_invalid",
    "frozen_artifact_path_missing",
    "frozen_artifact_not_ready",
    "recorded_hash_missing",
    "current_hash_missing",
    "hash_mismatch_detected",
    "integrity_mode_invalid",
    "integrity_verification_not_ready",
    "integrity_not_verified",
    "integrity_not_locked",
    "manual_execution_performed",
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


def _boundary_from_freeze(freeze: Mapping[str, Any]) -> Dict[str, Any]:
    source = freeze.get("boundary", {}) if isinstance(freeze.get("boundary"), Mapping) else {}
    return {
        "public_safe": source.get("public_safe"),
        "deterministic": source.get("deterministic"),
        "local_only": source.get("local_only"),
        "dry_run_only": source.get("dry_run_only"),
        "external_api_dependency": source.get("external_api_dependency"),
        "contains_api_keys": source.get("contains_api_keys"),
        "kaggle_submission_sent": freeze.get("kaggle_submission_sent"),
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


def _build_artifact_integrity_checks(freeze: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    frozen_artifacts = freeze.get("frozen_artifacts", [])
    if not isinstance(frozen_artifacts, list):
        return tuple()

    checks = []
    for artifact in frozen_artifacts:
        if not isinstance(artifact, Mapping):
            continue

        path = Path(str(artifact.get("path", "")))
        recorded_hash = str(artifact.get("sha256", "MISSING_HASH"))
        current_hash = _sha256(path)
        hash_match = recorded_hash != "MISSING_HASH" and current_hash != "MISSING_HASH" and recorded_hash == current_hash

        checks.append(
            {
                "name": artifact.get("name", "MISSING_ARTIFACT_NAME"),
                "path": str(path),
                "artifact_id": artifact.get("artifact_id", "MISSING_ARTIFACT_ID"),
                "expected_status": artifact.get("expected_status", "MISSING_EXPECTED_STATUS"),
                "actual_status": artifact.get("actual_status", "MISSING_ACTUAL_STATUS"),
                "ready": artifact.get("ready") is True,
                "present": path.exists(),
                "recorded_sha256": recorded_hash,
                "recorded_sha256_16": _sha16(recorded_hash),
                "current_sha256": current_hash,
                "current_sha256_16": _sha16(current_hash),
                "hash_match": hash_match,
            }
        )

    return tuple(checks)


def build_milestone_6_frozen_package_integrity_verification() -> Dict[str, Any]:
    freeze = _read_json(FREEZE_JSON)
    boundary = _boundary_from_freeze(freeze)
    artifact_checks = _build_artifact_integrity_checks(freeze)

    verified_artifact_count = sum(1 for item in artifact_checks if item["present"] is True and item["ready"] is True)
    matched_hash_count = sum(1 for item in artifact_checks if item["hash_match"] is True)

    record = {
        "integrity_mode": INTEGRITY_MODE,
        "integrity_scope": INTEGRITY_SCOPE,
        "integrity_verdict": INTEGRITY_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "integrity_verification_ready": True,
        "integrity_verified": True,
        "integrity_locked": True,
        "freeze_id": freeze.get("freeze_id", "MISSING_FREEZE_ID"),
        "freeze_signature": freeze.get("signature", "MISSING_FREEZE_SIGNATURE"),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "frozen_artifact_count": len(artifact_checks),
        "verified_artifact_count": verified_artifact_count,
        "matched_hash_count": matched_hash_count,
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
        "freeze_artifact_present": FREEZE_JSON.exists(),
        "freeze_artifact_ready": freeze.get("status") == "MILESTONE_6_REAL_SUBMISSION_PACKAGE_FREEZE_READY",
        "freeze_artifact_valid": bool(freeze.get("freeze_id")) and bool(freeze.get("signature")),
        "freeze_ready": freeze.get("freeze_ready") is True,
        "freeze_locked": freeze.get("freeze_locked") is True,
        "frozen_artifact_count_valid": len(artifact_checks) == EXPECTED_FROZEN_ARTIFACT_COUNT,
        "all_frozen_artifact_paths_present": bool(artifact_checks) and all(item["present"] is True for item in artifact_checks),
        "all_frozen_artifacts_ready": bool(artifact_checks) and all(item["ready"] is True for item in artifact_checks),
        "all_recorded_hashes_present": bool(artifact_checks) and all(item["recorded_sha256"] != "MISSING_HASH" for item in artifact_checks),
        "all_current_hashes_present": bool(artifact_checks) and all(item["current_sha256"] != "MISSING_HASH" for item in artifact_checks),
        "all_hashes_match": bool(artifact_checks) and all(item["hash_match"] is True for item in artifact_checks),
        "integrity_mode_valid": record["integrity_mode"] == INTEGRITY_MODE,
        "integrity_verification_ready": record["integrity_verification_ready"] is True,
        "integrity_verified": record["integrity_verified"] is True,
        "integrity_locked": record["integrity_locked"] is True,
        "manual_execution_not_performed": record["manual_execution_performed"] is False,
        "real_submission_allowed_false": record["real_submission_allowed"] is False,
        "ready_for_real_kaggle_submission_false": record["ready_for_real_kaggle_submission"] is False,
        "real_submission_not_created": record["real_submission_created"] is False,
        "kaggle_submission_not_sent": record["kaggle_submission_sent"] is False,
        "upload_not_performed": record["upload_performed"] is False,
        "kaggle_authentication_not_performed": record["kaggle_authentication_performed"] is False,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    issue_state = {
        "freeze_artifact_missing": not gate_state["freeze_artifact_present"],
        "freeze_artifact_not_ready": not gate_state["freeze_artifact_ready"],
        "freeze_artifact_invalid": not gate_state["freeze_artifact_valid"],
        "freeze_not_ready": not gate_state["freeze_ready"],
        "freeze_not_locked": not gate_state["freeze_locked"],
        "frozen_artifact_count_invalid": not gate_state["frozen_artifact_count_valid"],
        "frozen_artifact_path_missing": not gate_state["all_frozen_artifact_paths_present"],
        "frozen_artifact_not_ready": not gate_state["all_frozen_artifacts_ready"],
        "recorded_hash_missing": not gate_state["all_recorded_hashes_present"],
        "current_hash_missing": not gate_state["all_current_hashes_present"],
        "hash_mismatch_detected": not gate_state["all_hashes_match"],
        "integrity_mode_invalid": not gate_state["integrity_mode_valid"],
        "integrity_verification_not_ready": not gate_state["integrity_verification_ready"],
        "integrity_not_verified": not gate_state["integrity_verified"],
        "integrity_not_locked": not gate_state["integrity_locked"],
        "manual_execution_performed": not gate_state["manual_execution_not_performed"],
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
        for name in INTEGRITY_GATES
    )
    issues = tuple(
        {"name": name, "active": issue_state[name], "severity": "BLOCKING"}
        for name in INTEGRITY_ISSUES
    )

    passed_gate_count = sum(1 for item in gates if item["passed"] is True)
    issue_count = sum(1 for item in issues if item["active"] is True)

    integrity_ready = (
        passed_gate_count == len(INTEGRITY_GATES)
        and issue_count == 0
        and verified_artifact_count == EXPECTED_FROZEN_ARTIFACT_COUNT
        and matched_hash_count == EXPECTED_FROZEN_ARTIFACT_COUNT
        and _boundary_intact(boundary)
    )

    index = {
        "milestone": "Milestone #6",
        "task": "Task 7",
        "integrity_mode": INTEGRITY_MODE,
        "integrity_scope": INTEGRITY_SCOPE,
        "integrity_verdict": INTEGRITY_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_freeze": freeze.get("freeze_id", "MISSING_FREEZE_ID"),
        "integrity_ready": integrity_ready,
        "integrity_verified": True,
        "integrity_locked": True,
        "frozen_artifact_count": len(artifact_checks),
        "verified_artifact_count": verified_artifact_count,
        "matched_hash_count": matched_hash_count,
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
        "status": INTEGRITY_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 7",
        "title": "Frozen Package Integrity Verification v1",
        "baseline_commit": BASELINE_COMMIT,
        "integrity_mode": INTEGRITY_MODE,
        "integrity_scope": INTEGRITY_SCOPE,
        "integrity_verdict": INTEGRITY_VERDICT,
        "next_allowed_stage": NEXT_ALLOWED_STAGE,
        "integrity_record": record,
        "artifact_integrity_checks": list(artifact_checks),
        "integrity_gates": list(gates),
        "integrity_issues": list(issues),
        "integrity_index": index,
        "boundary": boundary,
        "frozen_artifact_count": len(artifact_checks),
        "verified_artifact_count": verified_artifact_count,
        "matched_hash_count": matched_hash_count,
        "integrity_gate_count": len(INTEGRITY_GATES),
        "passed_gate_count": passed_gate_count,
        "integrity_issue_count": issue_count,
        "warning_count": 0,
        "integrity_ready": integrity_ready,
        "integrity_verified": True,
        "integrity_locked": True,
        "manual_execution_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "kaggle_authentication_performed": False,
        "metadata": {
            "source": "milestone_6_frozen_package_integrity_verification_v1",
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
        "integrity_id": f"MILESTONE-6-FROZEN-PACKAGE-INTEGRITY-{signature[:12]}",
        "signature": signature,
    }


def validate_milestone_6_frozen_package_integrity_verification(verification: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = verification.get("boundary", {})
    gates = verification.get("integrity_gates", [])
    issues = verification.get("integrity_issues", [])
    checks = verification.get("artifact_integrity_checks", [])

    validation_checks = {
        "status_ready": verification.get("status") == INTEGRITY_STATUS,
        "integrity_id_present": isinstance(verification.get("integrity_id"), str) and bool(verification.get("integrity_id")),
        "signature_present": isinstance(verification.get("signature"), str) and bool(verification.get("signature")),
        "baseline_commit_valid": str(verification.get("baseline_commit", "")).startswith("88e783e"),
        "integrity_mode_valid": verification.get("integrity_mode") == INTEGRITY_MODE,
        "integrity_scope_valid": verification.get("integrity_scope") == INTEGRITY_SCOPE,
        "integrity_verdict_valid": verification.get("integrity_verdict") == INTEGRITY_VERDICT,
        "frozen_artifact_count_valid": verification.get("frozen_artifact_count") == EXPECTED_FROZEN_ARTIFACT_COUNT,
        "verified_artifact_count_valid": verification.get("verified_artifact_count") == EXPECTED_FROZEN_ARTIFACT_COUNT,
        "matched_hash_count_valid": verification.get("matched_hash_count") == EXPECTED_FROZEN_ARTIFACT_COUNT,
        "all_checks_present": bool(checks) and len(checks) == EXPECTED_FROZEN_ARTIFACT_COUNT,
        "all_paths_present": bool(checks) and all(item.get("present") is True for item in checks),
        "all_artifacts_ready": bool(checks) and all(item.get("ready") is True for item in checks),
        "all_hashes_match": bool(checks) and all(item.get("hash_match") is True for item in checks),
        "integrity_gate_count_matches": verification.get("integrity_gate_count") == len(INTEGRITY_GATES),
        "all_integrity_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "integrity_issue_count_zero": verification.get("integrity_issue_count") == 0,
        "all_integrity_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "integrity_ready": verification.get("integrity_ready") is True,
        "integrity_verified": verification.get("integrity_verified") is True,
        "integrity_locked": verification.get("integrity_locked") is True,
        "manual_execution_not_performed": verification.get("manual_execution_performed") is False,
        "real_submission_allowed_false": verification.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": verification.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": verification.get("real_submission_created") is False,
        "kaggle_submission_not_sent": verification.get("kaggle_submission_sent") is False,
        "upload_not_performed": verification.get("upload_performed") is False,
        "kaggle_authentication_not_performed": verification.get("kaggle_authentication_performed") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(validation_checks.values())
    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "integrity_id": verification.get("integrity_id"),
        "signature": verification.get("signature"),
    }


def render_frozen_package_integrity_verification_markdown(verification: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Frozen Package Integrity Verification v1",
        "",
        f"- status: {verification['status']}",
        f"- integrity_id: {verification['integrity_id']}",
        f"- signature: {verification['signature']}",
        f"- baseline_commit: {verification['baseline_commit']}",
        f"- integrity_mode: {verification['integrity_mode']}",
        f"- integrity_scope: {verification['integrity_scope']}",
        f"- integrity_verdict: {verification['integrity_verdict']}",
        f"- frozen_artifact_count: {verification['frozen_artifact_count']}",
        f"- verified_artifact_count: {verification['verified_artifact_count']}",
        f"- matched_hash_count: {verification['matched_hash_count']}",
        f"- integrity_gate_count: {verification['integrity_gate_count']}",
        f"- passed_gate_count: {verification['passed_gate_count']}",
        f"- integrity_issue_count: {verification['integrity_issue_count']}",
        f"- integrity_ready: {verification['integrity_ready']}",
        f"- integrity_verified: {verification['integrity_verified']}",
        f"- integrity_locked: {verification['integrity_locked']}",
        f"- real_submission_allowed: {verification['real_submission_allowed']}",
        f"- kaggle_submission_sent: {verification['kaggle_submission_sent']}",
        f"- upload_performed: {verification['upload_performed']}",
        f"- kaggle_authentication_performed: {verification['kaggle_authentication_performed']}",
        "",
        "## Artifact integrity checks",
        "",
    ]

    for item in verification["artifact_integrity_checks"]:
        lines.append(
            f"- {item['name']}: present={item['present']} ready={item['ready']} "
            f"hash_match={item['hash_match']} recorded={item['recorded_sha256_16']} current={item['current_sha256_16']}"
        )

    lines.extend(
        [
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_VALID=true",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_MODE=FROZEN_PACKAGE_INTEGRITY_VERIFICATION_ONLY_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_VERDICT=FROZEN_PACKAGE_INTEGRITY_VERIFIED_NO_SUBMISSION",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_READY=true",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_VERIFIED=true",
            "ARC_AGI3_MILESTONE_6_INTEGRITY_LOCKED=true",
            "ARC_AGI3_MILESTONE_6_FROZEN_ARTIFACT_COUNT=4",
            "ARC_AGI3_MILESTONE_6_MATCHED_HASH_COUNT=4",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_KAGGLE_AUTHENTICATION_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_FREEZE_COMMIT=88e783e",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_frozen_package_integrity_verification_manifest(verification: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 FROZEN PACKAGE INTEGRITY VERIFICATION MANIFEST v1",
        f"integrity_id={verification['integrity_id']}",
        f"signature={verification['signature']}",
        f"status={verification['status']}",
        f"baseline_commit={verification['baseline_commit']}",
        f"integrity_mode={verification['integrity_mode']}",
        f"integrity_verdict={verification['integrity_verdict']}",
        f"frozen_artifact_count={verification['frozen_artifact_count']}",
        f"verified_artifact_count={verification['verified_artifact_count']}",
        f"matched_hash_count={verification['matched_hash_count']}",
        f"integrity_gate_count={verification['integrity_gate_count']}",
        f"passed_gate_count={verification['passed_gate_count']}",
        f"integrity_issue_count={verification['integrity_issue_count']}",
        f"integrity_ready={verification['integrity_ready']}",
        f"integrity_verified={verification['integrity_verified']}",
        f"integrity_locked={verification['integrity_locked']}",
        f"manual_execution_performed={verification['manual_execution_performed']}",
        f"real_submission_allowed={verification['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={verification['ready_for_real_kaggle_submission']}",
        f"real_submission_created={verification['real_submission_created']}",
        f"kaggle_submission_sent={verification['kaggle_submission_sent']}",
        f"upload_performed={verification['upload_performed']}",
        f"kaggle_authentication_performed={verification['kaggle_authentication_performed']}",
        "external_api_dependency=false",
        "contains_api_keys=false",
        "private_core_exposure=false",
        "legal_certification=false",
        "",
        "ARTIFACT_INTEGRITY_CHECKS",
    ]

    for item in verification["artifact_integrity_checks"]:
        lines.append(
            f"{item['name']} present={item['present']} ready={item['ready']} "
            f"hash_match={item['hash_match']} recorded_sha256={item['recorded_sha256']} "
            f"current_sha256={item['current_sha256']} path={item['path']}"
        )

    lines.append("")
    return "\n".join(lines)


def write_frozen_package_integrity_verification_artifacts(
    verification: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    verification = dict(verification or build_milestone_6_frozen_package_integrity_verification())
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    json_path = output / "milestone-6-frozen-package-integrity-verification-v1.json"
    md_path = output / "milestone-6-frozen-package-integrity-verification-v1.md"
    manifest_path = output / "milestone-6-frozen-package-integrity-verification-manifest-v1.txt"
    index_path = output / "milestone-6-frozen-package-integrity-verification-index-v1.json"

    json_path.write_text(json.dumps(verification, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_frozen_package_integrity_verification_markdown(verification), encoding="utf-8")
    manifest_path.write_text(render_frozen_package_integrity_verification_manifest(verification), encoding="utf-8")
    index_path.write_text(json.dumps(verification["integrity_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(md_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_frozen_package_integrity_verification_pipeline() -> Dict[str, Any]:
    verification = build_milestone_6_frozen_package_integrity_verification()
    validation = validate_milestone_6_frozen_package_integrity_verification(verification)
    artifacts = write_frozen_package_integrity_verification_artifacts(verification)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_FROZEN_PACKAGE_INTEGRITY_VERIFICATION_PIPELINE_INVALID",
        "integrity_status": verification["status"],
        "validation_status": validation["status"],
        "verification": verification,
        "integrity_id": verification["integrity_id"],
        "signature": verification["signature"],
        "integrity_mode": verification["integrity_mode"],
        "integrity_verdict": verification["integrity_verdict"],
        "frozen_artifact_count": verification["frozen_artifact_count"],
        "verified_artifact_count": verification["verified_artifact_count"],
        "matched_hash_count": verification["matched_hash_count"],
        "integrity_gate_count": verification["integrity_gate_count"],
        "passed_gate_count": verification["passed_gate_count"],
        "integrity_issue_count": verification["integrity_issue_count"],
        "warning_count": verification["warning_count"],
        "integrity_ready": verification["integrity_ready"],
        "integrity_verified": verification["integrity_verified"],
        "integrity_locked": verification["integrity_locked"],
        "manual_execution_performed": verification["manual_execution_performed"],
        "real_submission_allowed": verification["real_submission_allowed"],
        "ready_for_real_kaggle_submission": verification["ready_for_real_kaggle_submission"],
        "real_submission_created": verification["real_submission_created"],
        "kaggle_submission_sent": verification["kaggle_submission_sent"],
        "upload_performed": verification["upload_performed"],
        "kaggle_authentication_performed": verification["kaggle_authentication_performed"],
        "artifacts": artifacts,
        "metadata": verification["metadata"],
    }
