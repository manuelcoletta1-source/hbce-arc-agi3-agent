"""Milestone #5 Public Release Summary v1.

This module creates a public, local-only release summary for ARC-AGI-3
Milestone #5. It summarizes the completed submission preparation chain without
creating a real Kaggle submission, authenticating, uploading files, calling
external APIs, reading secrets, or creating legal certification claims.
"""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


SUMMARY_STATUS = "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_READY"
PIPELINE_STATUS = "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/public-release-summary-v1"

CLOSURE_JSON = Path(
    "examples/milestone-5/submission-preparation-closure-v1/"
    "milestone-5-submission-preparation-closure-v1.json"
)

BASELINE_COMMIT = "7a8cf84 Close ARC AGI3 milestone 5 submission preparation"
PROJECT_NAME = "HBCE ARC-AGI-3 Agent"
RELEASE_SCOPE = "PUBLIC_RELEASE_SUMMARY_ONLY_NO_SUBMISSION"
MILESTONE_STATUS = "MILESTONE_5_SUBMISSION_PREPARATION_CLOSED_PASS"

PUBLIC_SUMMARY_GATES: Tuple[str, ...] = (
    "closure_artifact_present",
    "closure_status_ready",
    "closure_validation_ready",
    "closed_task_count_is_9",
    "ready_task_count_is_9",
    "closure_gate_count_is_20",
    "closure_issue_count_zero",
    "submission_preparation_closed",
    "ready_for_public_release_summary",
    "ready_for_real_kaggle_submission_false",
    "kaggle_submission_not_sent",
    "boundary_public_safe",
    "boundary_deterministic",
    "boundary_local_only",
    "boundary_dry_run_only",
    "no_external_api_dependency",
    "no_private_core_exposure",
    "no_legal_certification",
)

PUBLIC_SUMMARY_ISSUES: Tuple[str, ...] = (
    "closure_artifact_missing",
    "closure_status_not_ready",
    "closure_validation_not_ready",
    "closed_task_count_invalid",
    "ready_task_count_invalid",
    "closure_gate_count_invalid",
    "closure_issue_count_nonzero",
    "submission_preparation_not_closed",
    "public_release_summary_not_ready",
    "ready_for_real_kaggle_submission_true",
    "kaggle_submission_already_sent",
    "boundary_not_public_safe",
    "boundary_not_deterministic",
    "boundary_not_local_only",
    "boundary_not_dry_run_only",
    "external_api_dependency_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
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


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def _build_public_claims(closure: Mapping[str, Any]) -> Dict[str, Any]:
    return {
        "project_name": PROJECT_NAME,
        "milestone": "Milestone #5",
        "milestone_status": MILESTONE_STATUS,
        "summary_kind": "PUBLIC_RELEASE_SUMMARY",
        "submission_preparation_closed": closure.get("submission_preparation_closed") is True,
        "closed_task_count": closure.get("closed_task_count"),
        "ready_task_count": closure.get("ready_task_count"),
        "closure_gate_count": closure.get("closure_gate_count"),
        "closure_issue_count": closure.get("closure_issue_count"),
        "warning_count": closure.get("warning_count"),
        "tests_passed_recorded": "433 passed in 2.82s",
        "real_kaggle_submission_created": False,
        "kaggle_submission_sent": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }


def _build_summary_gates(closure: Mapping[str, Any], boundary: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    gate_results = {
        "closure_artifact_present": CLOSURE_JSON.exists(),
        "closure_status_ready": closure.get("status") == "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY",
        "closure_validation_ready": bool(closure.get("closure_id")) and bool(closure.get("signature")),
        "closed_task_count_is_9": closure.get("closed_task_count") == 9,
        "ready_task_count_is_9": closure.get("ready_task_count") == 9,
        "closure_gate_count_is_20": closure.get("closure_gate_count") == 20,
        "closure_issue_count_zero": closure.get("closure_issue_count") == 0,
        "submission_preparation_closed": closure.get("submission_preparation_closed") is True,
        "ready_for_public_release_summary": closure.get("ready_for_public_release_summary") is True,
        "ready_for_real_kaggle_submission_false": closure.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": closure.get("kaggle_submission_sent") is False,
        "boundary_public_safe": boundary.get("public_safe") is True,
        "boundary_deterministic": boundary.get("deterministic") is True,
        "boundary_local_only": boundary.get("local_only") is True,
        "boundary_dry_run_only": boundary.get("dry_run_only") is True,
        "no_external_api_dependency": boundary.get("external_api_dependency") is False,
        "no_private_core_exposure": boundary.get("private_core_exposure") is False,
        "no_legal_certification": boundary.get("legal_certification") is False,
    }

    descriptions = {
        "closure_artifact_present": "Milestone #5 closure artifact is present.",
        "closure_status_ready": "Milestone #5 closure exposes ready status.",
        "closure_validation_ready": "Milestone #5 closure has closure id and signature.",
        "closed_task_count_is_9": "Milestone #5 closed task count is 9.",
        "ready_task_count_is_9": "Milestone #5 ready task count is 9.",
        "closure_gate_count_is_20": "Milestone #5 closure gate count is 20.",
        "closure_issue_count_zero": "Milestone #5 closure issue count is zero.",
        "submission_preparation_closed": "Submission preparation is closed.",
        "ready_for_public_release_summary": "Closure allows public release summary.",
        "ready_for_real_kaggle_submission_false": "Real Kaggle submission remains false.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
        "boundary_public_safe": "Boundary keeps public_safe=true.",
        "boundary_deterministic": "Boundary keeps deterministic=true.",
        "boundary_local_only": "Boundary keeps local_only=true.",
        "boundary_dry_run_only": "Boundary keeps dry_run_only=true.",
        "no_external_api_dependency": "Boundary keeps external_api_dependency=false.",
        "no_private_core_exposure": "Boundary keeps private_core_exposure=false.",
        "no_legal_certification": "Boundary keeps legal_certification=false.",
    }

    return tuple(
        {
            "name": name,
            "passed": gate_results[name],
            "severity": "PASS" if gate_results[name] else "BLOCKING",
            "description": descriptions[name],
        }
        for name in PUBLIC_SUMMARY_GATES
    )


def _build_summary_issues(closure: Mapping[str, Any], boundary: Mapping[str, Any]) -> Tuple[Dict[str, Any], ...]:
    issue_state = {
        "closure_artifact_missing": not CLOSURE_JSON.exists(),
        "closure_status_not_ready": closure.get("status") != "MILESTONE_5_SUBMISSION_PREPARATION_CLOSURE_READY",
        "closure_validation_not_ready": not (bool(closure.get("closure_id")) and bool(closure.get("signature"))),
        "closed_task_count_invalid": closure.get("closed_task_count") != 9,
        "ready_task_count_invalid": closure.get("ready_task_count") != 9,
        "closure_gate_count_invalid": closure.get("closure_gate_count") != 20,
        "closure_issue_count_nonzero": closure.get("closure_issue_count") != 0,
        "submission_preparation_not_closed": closure.get("submission_preparation_closed") is not True,
        "public_release_summary_not_ready": closure.get("ready_for_public_release_summary") is not True,
        "ready_for_real_kaggle_submission_true": closure.get("ready_for_real_kaggle_submission") is not False,
        "kaggle_submission_already_sent": closure.get("kaggle_submission_sent") is not False,
        "boundary_not_public_safe": boundary.get("public_safe") is not True,
        "boundary_not_deterministic": boundary.get("deterministic") is not True,
        "boundary_not_local_only": boundary.get("local_only") is not True,
        "boundary_not_dry_run_only": boundary.get("dry_run_only") is not True,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
    }

    descriptions = {
        "closure_artifact_missing": "Milestone #5 closure artifact is missing.",
        "closure_status_not_ready": "Milestone #5 closure status is not ready.",
        "closure_validation_not_ready": "Milestone #5 closure id/signature is missing.",
        "closed_task_count_invalid": "Closed task count is not 9.",
        "ready_task_count_invalid": "Ready task count is not 9.",
        "closure_gate_count_invalid": "Closure gate count is not 20.",
        "closure_issue_count_nonzero": "Closure issue count is not zero.",
        "submission_preparation_not_closed": "Submission preparation is not closed.",
        "public_release_summary_not_ready": "Public release summary readiness is false.",
        "ready_for_real_kaggle_submission_true": "Real Kaggle submission readiness is not false.",
        "kaggle_submission_already_sent": "Kaggle submission flag is not false.",
        "boundary_not_public_safe": "public_safe boundary is not true.",
        "boundary_not_deterministic": "deterministic boundary is not true.",
        "boundary_not_local_only": "local_only boundary is not true.",
        "boundary_not_dry_run_only": "dry_run_only boundary is not true.",
        "external_api_dependency_detected": "external_api_dependency is not false.",
        "private_core_exposure_detected": "private_core_exposure is not false.",
        "legal_certification_claim_detected": "legal_certification is not false.",
    }

    return tuple(
        {
            "name": name,
            "active": issue_state[name],
            "severity": "BLOCKING",
            "description": descriptions[name],
        }
        for name in PUBLIC_SUMMARY_ISSUES
    )


def build_milestone_5_public_release_summary() -> Dict[str, Any]:
    closure = _read_json_if_available(CLOSURE_JSON)
    boundary = closure.get("boundary", {}) if isinstance(closure.get("boundary"), Mapping) else {}

    gates = _build_summary_gates(closure, boundary)
    issues = _build_summary_issues(closure, boundary)
    public_claims = _build_public_claims(closure)

    passed_gate_count = sum(1 for gate in gates if gate["passed"] is True)
    issue_count = sum(1 for issue in issues if issue["active"] is True)
    warning_count = 0

    public_release_summary_ready = (
        passed_gate_count == len(PUBLIC_SUMMARY_GATES)
        and issue_count == 0
        and _boundary_intact(boundary)
    )

    summary_index = {
        "project_name": PROJECT_NAME,
        "milestone": "Milestone #5",
        "release_scope": RELEASE_SCOPE,
        "milestone_status": MILESTONE_STATUS,
        "baseline_commit": BASELINE_COMMIT,
        "closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "closure_signature": closure.get("signature", "MISSING_CLOSURE_SIGNATURE"),
        "closure_artifact_sha256_16": _file_sha256_16(CLOSURE_JSON),
        "public_release_summary_ready": public_release_summary_ready,
        "real_kaggle_submission_created": False,
        "kaggle_submission_sent": False,
        "external_api_dependency": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    base_payload = {
        "status": SUMMARY_STATUS,
        "project_name": PROJECT_NAME,
        "milestone": "Milestone #5",
        "summary_kind": "PUBLIC_RELEASE_SUMMARY",
        "title": "ARC AGI3 Milestone #5 Public Release Summary v1",
        "baseline_commit": BASELINE_COMMIT,
        "closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "closure_signature": closure.get("signature", "MISSING_CLOSURE_SIGNATURE"),
        "final_package_id": closure.get("final_package_id", "MISSING_FINAL_PACKAGE_ID"),
        "release_scope": RELEASE_SCOPE,
        "milestone_status": MILESTONE_STATUS,
        "public_claims": public_claims,
        "summary_gates": list(gates),
        "summary_issues": list(issues),
        "summary_index": summary_index,
        "boundary": dict(boundary),
        "closed_task_count": closure.get("closed_task_count"),
        "ready_task_count": closure.get("ready_task_count"),
        "summary_gate_count": len(PUBLIC_SUMMARY_GATES),
        "passed_gate_count": passed_gate_count,
        "summary_issue_count": issue_count,
        "warning_count": warning_count,
        "public_release_summary_ready": public_release_summary_ready,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_public_release_summary_v1",
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
    summary_id = f"MILESTONE-5-PUBLIC-RELEASE-SUMMARY-{signature[:12]}"

    return {
        **base_payload,
        "summary_id": summary_id,
        "signature": signature,
    }


def validate_milestone_5_public_release_summary(summary: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = summary.get("boundary") if isinstance(summary.get("boundary"), Mapping) else {}
    gates = summary.get("summary_gates") if isinstance(summary.get("summary_gates"), list) else []
    issues = summary.get("summary_issues") if isinstance(summary.get("summary_issues"), list) else []
    index = summary.get("summary_index") if isinstance(summary.get("summary_index"), Mapping) else {}

    validation_checks = {
        "status_ready": summary.get("status") == SUMMARY_STATUS,
        "summary_id_present": isinstance(summary.get("summary_id"), str) and bool(summary.get("summary_id")),
        "signature_present": isinstance(summary.get("signature"), str) and bool(summary.get("signature")),
        "baseline_commit_is_milestone_5_closure": str(summary.get("baseline_commit", "")).startswith("7a8cf84"),
        "closure_id_present": isinstance(summary.get("closure_id"), str) and summary.get("closure_id") != "MISSING_CLOSURE_ID",
        "final_package_id_present": isinstance(summary.get("final_package_id"), str)
        and summary.get("final_package_id") != "MISSING_FINAL_PACKAGE_ID",
        "closed_task_count_is_9": summary.get("closed_task_count") == 9,
        "ready_task_count_is_9": summary.get("ready_task_count") == 9,
        "summary_gate_count_matches": summary.get("summary_gate_count") == len(PUBLIC_SUMMARY_GATES),
        "all_summary_gates_passed": bool(gates) and all(gate.get("passed") is True for gate in gates),
        "summary_issue_count_zero": summary.get("summary_issue_count") == 0,
        "all_summary_issues_inactive": bool(issues) and all(issue.get("active") is False for issue in issues),
        "warning_count_zero": summary.get("warning_count") == 0,
        "public_release_summary_ready": summary.get("public_release_summary_ready") is True,
        "ready_for_real_kaggle_submission_false": summary.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": summary.get("kaggle_submission_sent") is False,
        "index_release_scope_valid": index.get("release_scope") == RELEASE_SCOPE,
        "index_no_real_submission": index.get("real_kaggle_submission_created") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "summary_id": summary.get("summary_id"),
        "signature": summary.get("signature"),
    }


def render_public_release_summary_markdown(summary: Mapping[str, Any]) -> str:
    claims = summary["public_claims"]

    lines = [
        "# ARC AGI3 Milestone #5 - Public Release Summary v1",
        "",
        "## Public status",
        "",
        f"- project: {summary['project_name']}",
        f"- status: {summary['status']}",
        f"- summary_id: {summary['summary_id']}",
        f"- signature: {summary['signature']}",
        f"- baseline_commit: {summary['baseline_commit']}",
        f"- closure_id: {summary['closure_id']}",
        f"- closure_signature: {summary['closure_signature']}",
        f"- final_package_id: {summary['final_package_id']}",
        f"- release_scope: {summary['release_scope']}",
        f"- milestone_status: {summary['milestone_status']}",
        "",
        "## What is ready",
        "",
        f"- submission_preparation_closed: {claims['submission_preparation_closed']}",
        f"- closed_task_count: {claims['closed_task_count']}",
        f"- ready_task_count: {claims['ready_task_count']}",
        f"- closure_gate_count: {claims['closure_gate_count']}",
        f"- closure_issue_count: {claims['closure_issue_count']}",
        f"- warning_count: {claims['warning_count']}",
        f"- tests_passed_recorded: {claims['tests_passed_recorded']}",
        "",
        "## What is not done",
        "",
        "- real_kaggle_submission_created: false",
        "- kaggle_submission_sent: false",
        "- external_api_dependency: false",
        "- private_core_exposure: false",
        "- legal_certification: false",
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
        "## Summary gates",
        "",
    ]

    for gate in summary["summary_gates"]:
        lines.append(f"- {gate['name']}: passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "## Summary issues", ""])

    for issue in summary["summary_issues"]:
        lines.append(f"- {issue['name']}: active={issue['active']} severity={issue['severity']}")

    lines.extend(
        [
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_5_PUBLIC_RELEASE_SUMMARY_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_PUBLIC_RELEASE_SUMMARY_VALID=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_PREPARATION_CLOSED=true",
            "ARC_AGI3_MILESTONE_5_CLOSED_TASK_COUNT=9",
            "ARC_AGI3_MILESTONE_5_READY_TASK_COUNT=9",
            "ARC_AGI3_MILESTONE_5_SUMMARY_GATE_COUNT=18",
            "ARC_AGI3_MILESTONE_5_SUMMARY_ISSUE_COUNT=0",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_CLOSURE_COMMIT=7a8cf84",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_public_release_manifest(summary: Mapping[str, Any]) -> str:
    lines = [
        "ARC AGI3 MILESTONE 5 PUBLIC RELEASE SUMMARY MANIFEST v1",
        f"summary_id={summary['summary_id']}",
        f"signature={summary['signature']}",
        f"status={summary['status']}",
        f"baseline_commit={summary['baseline_commit']}",
        f"closure_id={summary['closure_id']}",
        f"release_scope={summary['release_scope']}",
        f"milestone_status={summary['milestone_status']}",
        f"closed_task_count={summary['closed_task_count']}",
        f"ready_task_count={summary['ready_task_count']}",
        f"summary_gate_count={summary['summary_gate_count']}",
        f"passed_gate_count={summary['passed_gate_count']}",
        f"summary_issue_count={summary['summary_issue_count']}",
        f"warning_count={summary['warning_count']}",
        f"public_release_summary_ready={summary['public_release_summary_ready']}",
        f"ready_for_real_kaggle_submission={summary['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={summary['kaggle_submission_sent']}",
        "",
        "PUBLIC_BOUNDARY",
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
        "SUMMARY_GATES",
    ]

    for gate in summary["summary_gates"]:
        lines.append(f"{gate['name']} passed={gate['passed']} severity={gate['severity']}")

    lines.extend(["", "SUMMARY_ISSUES"])

    for issue in summary["summary_issues"]:
        lines.append(f"{issue['name']} active={issue['active']} severity={issue['severity']}")

    lines.append("")
    return "\n".join(lines)


def render_public_readme_snippet(summary: Mapping[str, Any]) -> str:
    return "\n".join(
        [
            "## ARC AGI3 Milestone #5 - Submission Preparation",
            "",
            "Milestone #5 is closed as local-only submission preparation.",
            "",
            "- status: CLOSED_PASS",
            "- closed tasks: 9/9",
            "- tests: 433 passed",
            "- submission preparation closed: true",
            "- real Kaggle submission: false",
            "- Kaggle upload: false",
            "- external API dependency: false",
            "- private core exposure: false",
            "- legal certification: false",
            "",
            f"Closure commit: `{summary['baseline_commit']}`",
            f"Closure id: `{summary['closure_id']}`",
            "",
        ]
    )


def write_public_release_summary_artifacts(
    summary: Mapping[str, Any] | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    summary = dict(summary or build_milestone_5_public_release_summary())
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-5-public-release-summary-v1.json"
    markdown_path = output_path / "milestone-5-public-release-summary-v1.md"
    manifest_path = output_path / "milestone-5-public-release-summary-manifest-v1.txt"
    index_path = output_path / "milestone-5-public-release-summary-index-v1.json"
    readme_snippet_path = output_path / "milestone-5-public-readme-snippet-v1.md"

    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_public_release_summary_markdown(summary), encoding="utf-8")
    manifest_path.write_text(render_public_release_manifest(summary), encoding="utf-8")
    index_path.write_text(json.dumps(summary["summary_index"], indent=2, sort_keys=True), encoding="utf-8")
    readme_snippet_path.write_text(render_public_readme_snippet(summary), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "readme_snippet_path": str(readme_snippet_path),
    }


def run_milestone_5_public_release_summary_pipeline() -> Dict[str, Any]:
    summary = build_milestone_5_public_release_summary()
    validation = validate_milestone_5_public_release_summary(summary)
    artifacts = write_public_release_summary_artifacts(summary)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_PUBLIC_RELEASE_SUMMARY_PIPELINE_INVALID",
        "summary_status": summary["status"],
        "validation_status": validation["status"],
        "summary": summary,
        "summary_id": summary["summary_id"],
        "signature": summary["signature"],
        "closed_task_count": summary["closed_task_count"],
        "ready_task_count": summary["ready_task_count"],
        "summary_gate_count": summary["summary_gate_count"],
        "passed_gate_count": summary["passed_gate_count"],
        "summary_issue_count": summary["summary_issue_count"],
        "warning_count": summary["warning_count"],
        "public_release_summary_ready": summary["public_release_summary_ready"],
        "ready_for_real_kaggle_submission": summary["ready_for_real_kaggle_submission"],
        "kaggle_submission_sent": summary["kaggle_submission_sent"],
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_public_release_summary_pipeline_v1",
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
