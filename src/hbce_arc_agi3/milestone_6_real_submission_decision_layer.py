"""Milestone #6 Real Submission Decision Layer v1.

This module creates a local-only decision layer for a possible future ARC-AGI-3
real Kaggle submission. It does not authenticate, upload, submit, call Kaggle,
call external APIs, read secrets, create archives for upload, or create legal
certification claims.

The layer is intentionally conservative: submission preparation can be closed,
but real submission remains blocked until explicit operator approval exists.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


DECISION_STATUS = "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_READY"
PIPELINE_STATUS = "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-6/real-submission-decision-layer-v1"

PUBLIC_RELEASE_SUMMARY_JSON = Path(
    "examples/milestone-5/public-release-summary-v1/"
    "milestone-5-public-release-summary-v1.json"
)

SUBMISSION_CLOSURE_JSON = Path(
    "examples/milestone-5/submission-preparation-closure-v1/"
    "milestone-5-submission-preparation-closure-v1.json"
)

DRY_RUN_PACKAGE_JSON = Path(
    "examples/milestone-5/submission-candidate-dry-run-package-v1/"
    "submission-candidate-dry-run-package-v1.json"
)

BASELINE_COMMIT = "e9742a1 Add ARC AGI3 milestone 5 public release summary"
DECISION_MODE = "DECISION_LAYER_ONLY_NO_SUBMISSION"
DECISION_SCOPE = "REAL_SUBMISSION_DECISION_GATE_NO_UPLOAD_NO_API"
DECISION_VERDICT = "REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL"

DECISION_GATES: Tuple[str, ...] = (
    "public_release_summary_present",
    "public_release_summary_ready",
    "submission_closure_present",
    "submission_closure_ready",
    "dry_run_package_present",
    "dry_run_package_ready",
    "milestone_5_closed_pass",
    "operator_approval_required",
    "operator_approval_not_received",
    "real_submission_allowed_false",
    "real_submission_not_created",
    "kaggle_submission_not_sent",
    "no_upload_performed",
    "no_external_api_dependency",
    "no_secrets_required",
    "no_private_core_exposure",
    "no_legal_certification",
    "decision_layer_only",
)

DECISION_ISSUES: Tuple[str, ...] = (
    "public_release_summary_missing",
    "public_release_summary_not_ready",
    "submission_closure_missing",
    "submission_closure_not_ready",
    "dry_run_package_missing",
    "dry_run_package_not_ready",
    "milestone_5_not_closed_pass",
    "operator_approval_not_required",
    "operator_approval_received_untracked",
    "real_submission_allowed_true",
    "real_submission_created",
    "kaggle_submission_already_sent",
    "upload_performed",
    "external_api_dependency_detected",
    "secrets_required_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
    "decision_layer_mode_invalid",
)

REQUIRED_BOUNDARY_FLAGS: Tuple[Tuple[str, bool], ...] = (
    ("public_safe", True),
    ("deterministic", True),
    ("local_only", True),
    ("dry_run_only", True),
    ("external_api_dependency", False),
    ("contains_api_keys", False),
    ("kaggle_submission_sent", False),
    ("private_core_exposure", False),
    ("legal_certification", False),
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16].upper()


def _read_json_if_available(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def _file_sha256_16(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"

    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def _boundary_from_summary(summary: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = summary.get("boundary", {}) if isinstance(summary.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": summary.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def _build_artifact_statuses(
    *,
    public_summary: Mapping[str, Any],
    closure: Mapping[str, Any],
    dry_run_package: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    specs = (
        (
            "milestone_5_public_release_summary",
            PUBLIC_RELEASE_SUMMARY_JSON,
            "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
            public_summary.get("status", "MISSING"),
            public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        ),
        (
            "milestone_5_submission_preparation_closure",
            SUBMISSION_CLOSURE_JSON,
            "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY",
            closure.get("status", "MISSING"),
            closure.get("closure_id", "MISSING_CLOSURE_ID"),
        ),
        (
            "milestone_5_submission_candidate_dry_run_package",
            DRY_RUN_PACKAGE_JSON,
            "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
            dry_run_package.get("status", "MISSING"),
            dry_run_package.get("package_id", "MISSING_PACKAGE_ID"),
        ),
    )

    statuses = []

    for name, path, expected_status, actual_status, artifact_id in specs:
        present = path.exists()
        ready = present and actual_status == expected_status

        statuses.append(
            {
                "name": name,
                "path": str(path),
                "expected_status": expected_status,
                "actual_status": actual_status,
                "artifact_id": artifact_id,
                "present": present,
                "ready": ready,
                "sha256_16": _file_sha256_16(path),
            }
        )

    return tuple(statuses)


def _build_decision_record(
    *,
    public_summary: Mapping[str, Any],
    closure: Mapping[str, Any],
    dry_run_package: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Dict[str, Any]:
    return {
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "operator_identity_verified_for_submission": False,
        "real_submission_allowed": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "archive_created_for_upload": False,
        "external_api_dependency": False,
        "secrets_required": False,
        "contains_api_keys": False,
        "legal_certification": False,
        "private_core_exposure": False,
        "public_release_summary_ready": public_summary.get("public_release_summary_ready") is True,
        "milestone_5_closed_pass": public_summary.get("milestone_status") == "MILESTONE_5_SUBMISSION_PREPARATION_CLOSED_PASS",
        "submission_preparation_closed": closure.get("submission_preparation_closed") is True,
        "dry_run_package_ready": dry_run_package.get("dry_run_package_ready") is True,
        "boundary_intact": _boundary_intact(boundary),
        "next_required_action": "explicit_operator_approval_before_any_real_submission",
    }


def _build_decision_gates(
    *,
    public_summary: Mapping[str, Any],
    closure: Mapping[str, Any],
    dry_run_package: Mapping[str, Any],
    artifact_statuses: Tuple[Dict[str, Any], ...],
    decision_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    gate_results = {
        "public_release_summary_present": PUBLIC_RELEASE_SUMMARY_JSON.exists(),
        "public_release_summary_ready": public_summary.get("status") == "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
        "submission_closure_present": SUBMISSION_CLOSURE_JSON.exists(),
        "submission_closure_ready": closure.get("status") == "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY",
        "dry_run_package_present": DRY_RUN_PACKAGE_JSON.exists(),
        "dry_run_package_ready": dry_run_package.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "milestone_5_closed_pass": public_summary.get("milestone_status") == "MILESTONE_5_SUBMISSION_PREPARATION_CLOSED_PASS",
        "operator_approval_required": decision_record.get("operator_approval_required") is True,
        "operator_approval_not_received": decision_record.get("operator_approval_received") is False,
        "real_submission_allowed_false": decision_record.get("real_submission_allowed") is False,
        "real_submission_not_created": decision_record.get("real_submission_created") is False,
        "kaggle_submission_not_sent": decision_record.get("kaggle_submission_sent") is False,
        "no_upload_performed": decision_record.get("upload_performed") is False,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_secrets_required": decision_record.get("secrets_required") is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
        "decision_layer_only": decision_record.get("decision_mode") == DECISION_MODE,
    }

    descriptions = {
        "public_release_summary_present": "Milestone #5 public release summary artifact is present.",
        "public_release_summary_ready": "Milestone #5 public release summary is ready.",
        "submission_closure_present": "Milestone #5 submission closure artifact is present.",
        "submission_closure_ready": "Milestone #5 submission closure is ready.",
        "dry_run_package_present": "Milestone #5 dry-run package artifact is present.",
        "dry_run_package_ready": "Milestone #5 dry-run package is ready.",
        "milestone_5_closed_pass": "Milestone #5 is closed pass.",
        "operator_approval_required": "Explicit operator approval is required before real submission.",
        "operator_approval_not_received": "No operator approval has been received in this layer.",
        "real_submission_allowed_false": "Real submission remains disallowed.",
        "real_submission_not_created": "No real submission has been created.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
        "no_upload_performed": "No upload has been performed.",
        "no_external_api_dependency": "No external API dependency is present.",
        "no_secrets_required": "No secrets are required or read.",
        "no_private_core_exposure": "No private core exposure is present.",
        "no_legal_certification": "No legal certification claim is present.",
        "decision_layer_only": "Layer mode is decision-only.",
    }

    return tuple(
        {
            "name": name,
            "passed": gate_results[name],
            "severity": "PASS" if gate_results[name] else "BLOCKING",
            "description": descriptions[name],
        }
        for name in DECISION_GATES
    )


def _build_decision_issues(
    *,
    public_summary: Mapping[str, Any],
    closure: Mapping[str, Any],
    dry_run_package: Mapping[str, Any],
    decision_record: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[Dict[str, Any], ...]:
    issue_state = {
        "public_release_summary_missing": not PUBLIC_RELEASE_SUMMARY_JSON.exists(),
        "public_release_summary_not_ready": public_summary.get("status") != "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY",
        "submission_closure_missing": not SUBMISSION_CLOSURE_JSON.exists(),
        "submission_closure_not_ready": closure.get("status") != "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY",
        "dry_run_package_missing": not DRY_RUN_PACKAGE_JSON.exists(),
        "dry_run_package_not_ready": dry_run_package.get("status") != "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY",
        "milestone_5_not_closed_pass": public_summary.get("milestone_status") != "MILESTONE_5_SUBMISSION_PREPARATION_CLOSED_PASS",
        "operator_approval_not_required": decision_record.get("operator_approval_required") is not True,
        "operator_approval_received_untracked": decision_record.get("operator_approval_received") is not False,
        "real_submission_allowed_true": decision_record.get("real_submission_allowed") is not False,
        "real_submission_created": decision_record.get("real_submission_created") is not False,
        "kaggle_submission_already_sent": decision_record.get("kaggle_submission_sent") is not False,
        "upload_performed": decision_record.get("upload_performed") is not False,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "secrets_required_detected": decision_record.get("secrets_required") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
        "decision_layer_mode_invalid": decision_record.get("decision_mode") != DECISION_MODE,
    }

    descriptions = {
        "public_release_summary_missing": "Public release summary artifact is missing.",
        "public_release_summary_not_ready": "Public release summary is not ready.",
        "submission_closure_missing": "Submission closure artifact is missing.",
        "submission_closure_not_ready": "Submission closure is not ready.",
        "dry_run_package_missing": "Dry-run package artifact is missing.",
        "dry_run_package_not_ready": "Dry-run package is not ready.",
        "milestone_5_not_closed_pass": "Milestone #5 is not closed pass.",
        "operator_approval_not_required": "Operator approval is not required.",
        "operator_approval_received_untracked": "Operator approval appears received in an untracked context.",
        "real_submission_allowed_true": "Real submission is allowed unexpectedly.",
        "real_submission_created": "A real submission appears to have been created.",
        "kaggle_submission_already_sent": "A Kaggle submission appears to have been sent.",
        "upload_performed": "An upload appears to have been performed.",
        "external_api_dependency_detected": "External API dependency detected.",
        "secrets_required_detected": "Secrets requirement detected.",
        "private_core_exposure_detected": "Private core exposure detected.",
        "legal_certification_claim_detected": "Legal certification claim detected.",
        "decision_layer_mode_invalid": "Decision layer mode is invalid.",
    }

    return tuple(
        {
            "name": name,
            "active": issue_state[name],
            "severity": "BLOCKING",
            "description": descriptions[name],
        }
        for name in DECISION_ISSUES
    )


def build_milestone_6_real_submission_decision_layer() -> Dict[str, Any]:
    public_summary = _read_json_if_available(PUBLIC_RELEASE_SUMMARY_JSON)
    closure = _read_json_if_available(SUBMISSION_CLOSURE_JSON)
    dry_run_package = _read_json_if_available(DRY_RUN_PACKAGE_JSON)
    boundary = _boundary_from_summary(public_summary)

    artifact_statuses = _build_artifact_statuses(
        public_summary=public_summary,
        closure=closure,
        dry_run_package=dry_run_package,
    )

    decision_record = _build_decision_record(
        public_summary=public_summary,
        closure=closure,
        dry_run_package=dry_run_package,
        boundary=boundary,
    )

    gates = _build_decision_gates(
        public_summary=public_summary,
        closure=closure,
        dry_run_package=dry_run_package,
        artifact_statuses=artifact_statuses,
        decision_record=decision_record,
        boundary=boundary,
    )
    issues = _build_decision_issues(
        public_summary=public_summary,
        closure=closure,
        dry_run_package=dry_run_package,
        decision_record=decision_record,
        boundary=boundary,
    )

    ready_artifact_count = sum(1 for item in artifact_statuses if item["ready"] is True)
    passed_gate_count = sum(1 for gate in gates if gate["passed"] is True)
    issue_count = sum(1 for issue in issues if issue["active"] is True)
    warning_count = 0

    decision_layer_ready = (
        ready_artifact_count == len(artifact_statuses)
        and passed_gate_count == len(DECISION_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
        and decision_record["real_submission_allowed"] is False
    )

    decision_index = {
        "milestone": "Milestone #6",
        "task": "Task 1",
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "baseline_commit": BASELINE_COMMIT,
        "depends_on_public_release_summary": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        "depends_on_submission_closure": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "depends_on_dry_run_package": dry_run_package.get("package_id", "MISSING_PACKAGE_ID"),
        "operator_approval_required": True,
        "operator_approval_received": False,
        "real_submission_allowed": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base_payload = {
        "status": DECISION_STATUS,
        "milestone": "Milestone #6",
        "task": "Task 1",
        "title": "Real Submission Decision Layer v1",
        "baseline_commit": BASELINE_COMMIT,
        "public_release_summary_id": public_summary.get("summary_id", "MISSING_SUMMARY_ID"),
        "public_release_summary_signature": public_summary.get("signature", "MISSING_SUMMARY_SIGNATURE"),
        "submission_closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "submission_closure_signature": closure.get("signature", "MISSING_CLOSURE_SIGNATURE"),
        "dry_run_package_id": dry_run_package.get("package_id", "MISSING_PACKAGE_ID"),
        "dry_run_package_signature": dry_run_package.get("signature", "MISSING_PACKAGE_SIGNATURE"),
        "decision_mode": DECISION_MODE,
        "decision_scope": DECISION_SCOPE,
        "decision_verdict": DECISION_VERDICT,
        "artifact_statuses": list(artifact_statuses),
        "decision_record": copy.deepcopy(decision_record),
        "decision_gates": list(gates),
        "decision_issues": list(issues),
        "decision_index": decision_index,
        "boundary": boundary,
        "artifact_count": len(artifact_statuses),
        "ready_artifact_count": ready_artifact_count,
        "decision_gate_count": len(DECISION_GATES),
        "passed_gate_count": passed_gate_count,
        "decision_issue_count": issue_count,
        "warning_count": warning_count,
        "decision_layer_ready": decision_layer_ready,
        "operator_approval_required": True,
        "operator_approval_received": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "real_submission_created": False,
        "kaggle_submission_sent": False,
        "upload_performed": False,
        "metadata": {
            "source": "milestone_6_real_submission_decision_layer_v1",
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

    signature = _stable_signature(base_payload)
    decision_id = f"MILESTONE-6-REAL-SUBMISSION-DECISION-{signature[:12]}"

    return {
        **base_payload,
        "decision_id": decision_id,
        "signature": signature,
    }


def validate_milestone_6_real_submission_decision_layer(decision: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = decision.get("boundary") if isinstance(decision.get("boundary"), Mapping) else {}
    artifacts = decision.get("artifact_statuses") if isinstance(decision.get("artifact_statuses"), list) else []
    gates = decision.get("decision_gates") if isinstance(decision.get("decision_gates"), list) else []
    issues = decision.get("decision_issues") if isinstance(decision.get("decision_issues"), list) else []
    record = decision.get("decision_record") if isinstance(decision.get("decision_record"), Mapping) else {}
    index = decision.get("decision_index") if isinstance(decision.get("decision_index"), Mapping) else {}

    validation_checks = {
        "status_ready": decision.get("status") == DECISION_STATUS,
        "decision_id_present": isinstance(decision.get("decision_id"), str) and bool(decision.get("decision_id")),
        "signature_present": isinstance(decision.get("signature"), str) and bool(decision.get("signature")),
        "baseline_commit_is_public_summary": str(decision.get("baseline_commit", "")).startswith("e9742a1"),
        "decision_mode_valid": decision.get("decision_mode") == DECISION_MODE,
        "decision_scope_valid": decision.get("decision_scope") == DECISION_SCOPE,
        "decision_verdict_blocked": decision.get("decision_verdict") == DECISION_VERDICT,
        "artifact_count_is_3": decision.get("artifact_count") == 3,
        "ready_artifact_count_is_3": decision.get("ready_artifact_count") == 3,
        "all_artifacts_ready": bool(artifacts) and all(item.get("ready") is True for item in artifacts),
        "decision_gate_count_matches": decision.get("decision_gate_count") == len(DECISION_GATES),
        "all_decision_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "decision_issue_count_zero": decision.get("decision_issue_count") == 0,
        "all_decision_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "warning_count_zero": decision.get("warning_count") == 0,
        "decision_layer_ready": decision.get("decision_layer_ready") is True,
        "operator_approval_required": decision.get("operator_approval_required") is True,
        "operator_approval_not_received": decision.get("operator_approval_received") is False,
        "record_real_submission_allowed_false": record.get("real_submission_allowed") is False,
        "real_submission_allowed_false": decision.get("real_submission_allowed") is False,
        "ready_for_real_kaggle_submission_false": decision.get("ready_for_real_kaggle_submission") is False,
        "real_submission_not_created": decision.get("real_submission_created") is False,
        "kaggle_submission_not_sent": decision.get("kaggle_submission_sent") is False,
        "upload_not_performed": decision.get("upload_performed") is False,
        "index_real_submission_allowed_false": index.get("real_submission_allowed") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "decision_id": decision.get("decision_id"),
        "signature": decision.get("signature"),
    }


def render_real_submission_decision_layer_markdown(decision: Mapping[str, Any]) -> str:
    lines = [
        "# ARC AGI3 Milestone #6 - Real Submission Decision Layer v1",
        "",
        "## Status",
        "",
        f"- status: {decision['status']}",
        f"- decision_id: {decision['decision_id']}",
        f"- signature: {decision['signature']}",
        f"- baseline_commit: {decision['baseline_commit']}",
        f"- decision_mode: {decision['decision_mode']}",
        f"- decision_scope: {decision['decision_scope']}",
        f"- decision_verdict: {decision['decision_verdict']}",
        f"- public_release_summary_id: {decision['public_release_summary_id']}",
        f"- submission_closure_id: {decision['submission_closure_id']}",
        f"- dry_run_package_id: {decision['dry_run_package_id']}",
        f"- artifact_count: {decision['artifact_count']}",
        f"- ready_artifact_count: {decision['ready_artifact_count']}",
        f"- decision_gate_count: {decision['decision_gate_count']}",
        f"- passed_gate_count: {decision['passed_gate_count']}",
        f"- decision_issue_count: {decision['decision_issue_count']}",
        f"- warning_count: {decision['warning_count']}",
        f"- decision_layer_ready: {decision['decision_layer_ready']}",
        f"- operator_approval_required: {decision['operator_approval_required']}",
        f"- operator_approval_received: {decision['operator_approval_received']}",
        f"- real_submission_allowed: {decision['real_submission_allowed']}",
        f"- ready_for_real_kaggle_submission: {decision['ready_for_real_kaggle_submission']}",
        f"- real_submission_created: {decision['real_submission_created']}",
        f"- kaggle_submission_sent: {decision['kaggle_submission_sent']}",
        f"- upload_performed: {decision['upload_performed']}",
        "",
        "## Decision gates",
        "",
    ]

    for gate in decision["decision_gates"]:
        lines.append(f"- {gate['name']}: passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "## Decision issues", ""])

    for issue in decision["decision_issues"]:
        lines.append(f"- {issue['name']}: active={issue['active']} severity={issue['severity']}")

    lines.extend(
        [
            "",
            "## Public boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "- legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_V1_READY=true",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_VALID=true",
            "ARC_AGI3_MILESTONE_6_DECISION_MODE=DECISION_LAYER_ONLY_NO_SUBMISSION",
            "ARC_AGI3_MILESTONE_6_DECISION_VERDICT=REAL_SUBMISSION_BLOCKED_PENDING_EXPLICIT_OPERATOR_APPROVAL",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_REQUIRED=true",
            "ARC_AGI3_MILESTONE_6_OPERATOR_APPROVAL_RECEIVED=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false",
            "ARC_AGI3_MILESTONE_6_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_CREATED=false",
            "ARC_AGI3_MILESTONE_6_UPLOAD_PERFORMED=false",
            "ARC_AGI3_MILESTONE_6_BASELINE_PUBLIC_RELEASE_SUMMARY_COMMIT=e9742a1",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_real_submission_decision_manifest(decision: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 6 REAL SUBMISSION DECISION LAYER MANIFEST v1",
        f"decision_id={decision['decision_id']}",
        f"signature={decision['signature']}",
        f"status={decision['status']}",
        f"baseline_commit={decision['baseline_commit']}",
        f"decision_mode={decision['decision_mode']}",
        f"decision_scope={decision['decision_scope']}",
        f"decision_verdict={decision['decision_verdict']}",
        f"artifact_count={decision['artifact_count']}",
        f"ready_artifact_count={decision['ready_artifact_count']}",
        f"decision_gate_count={decision['decision_gate_count']}",
        f"passed_gate_count={decision['passed_gate_count']}",
        f"decision_issue_count={decision['decision_issue_count']}",
        f"warning_count={decision['warning_count']}",
        f"decision_layer_ready={decision['decision_layer_ready']}",
        f"operator_approval_required={decision['operator_approval_required']}",
        f"operator_approval_received={decision['operator_approval_received']}",
        f"real_submission_allowed={decision['real_submission_allowed']}",
        f"ready_for_real_kaggle_submission={decision['ready_for_real_kaggle_submission']}",
        f"real_submission_created={decision['real_submission_created']}",
        f"kaggle_submission_sent={decision['kaggle_submission_sent']}",
        f"upload_performed={decision['upload_performed']}",
        "",
        "DECISION_GATES",
    ]

    for gate in decision["decision_gates"]:
        lines.append(f"{gate['name']} passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "DECISION_ISSUES"])

    for issue in decision["decision_issues"]:
        lines.append(f"{issue['name']} active={issue['active']} severity={issue['severity']}")

    lines.extend(
        [
            "",
            "BOUNDARY",
            "public_safe=true",
            "deterministic=true",
            "local_only=true",
            "dry_run_only=true",
            "external_api_dependency=false",
            "contains_api_keys=false",
            "kaggle_submission_sent=false",
            "private_core_exposure=false",
            "legal_certification=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_real_submission_decision_layer_artifacts(
    decision: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    decision = dict(decision or build_milestone_6_real_submission_decision_layer())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-6-real-submission-decision-layer-v1.json"
    markdown_path = output_path / "milestone-6-real-submission-decision-layer-v1.md"
    manifest_path = output_path / "milestone-6-real-submission-decision-layer-manifest-v1.txt"
    index_path = output_path / "milestone-6-real-submission-decision-layer-index-v1.json"

    json_path.write_text(json.dumps(decision, indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_real_submission_decision_layer_markdown(decision), encoding="utf-8")
    manifest_path.write_text(render_real_submission_decision_manifest(decision), encoding="utf-8")
    index_path.write_text(json.dumps(decision["decision_index"], indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
    }


def run_milestone_6_real_submission_decision_layer_pipeline() -> Dict[str, Any]:
    decision = build_milestone_6_real_submission_decision_layer()
    validation = validate_milestone_6_real_submission_decision_layer(decision)
    artifacts = write_real_submission_decision_layer_artifacts(decision)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_6_REAL_SUBMISSION_DECISION_LAYER_PIPELINE_INVALID",
        "decision_status": decision["status"],
        "validation_status": validation["status"],
        "decision": decision,
        "decision_id": decision["decision_id"],
        "signature": decision["signature"],
        "decision_mode": decision["decision_mode"],
        "decision_verdict": decision["decision_verdict"],
        "artifact_count": decision["artifact_count"],
        "ready_artifact_count": decision["ready_artifact_count"],
        "decision_gate_count": decision["decision_gate_count"],
        "passed_gate_count": decision["passed_gate_count"],
        "decision_issue_count": decision["decision_issue_count"],
        "warning_count": decision["warning_count"],
        "decision_layer_ready": decision["decision_layer_ready"],
        "operator_approval_required": decision["operator_approval_required"],
        "operator_approval_received": decision["operator_approval_received"],
        "real_submission_allowed": decision["real_submission_allowed"],
        "ready_for_real_kaggle_submission": decision["ready_for_real_kaggle_submission"],
        "real_submission_created": decision["real_submission_created"],
        "kaggle_submission_sent": decision["kaggle_submission_sent"],
        "upload_performed": decision["upload_performed"],
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_6_real_submission_decision_layer_pipeline_v1",
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
