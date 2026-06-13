"""Public Readiness Audit v1 for HBCE ARC-AGI-3 public baseline.

This module audits the Milestone #3 public chain before any public release or
submission step.

It does not submit to Kaggle.
It does not call external APIs.
It does not read credentials.
It does not execute dataset code.
It does not expose private HBCE/JOKER-C2 runtime code.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.local_submission_candidate_builder import (
    LocalSubmissionCandidatePackage,
    build_local_submission_candidate_package,
    validate_local_submission_candidate_package,
)


@dataclass(frozen=True)
class PublicReadinessAuditCheck:
    status: str
    check_id: str
    check_name: str
    category: str
    passed: bool
    severity: str
    evidence: Dict[str, Any]
    remediation_hint: str
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicReadinessAuditReport:
    status: str
    audit_status: str
    audit_id: str
    candidate_id: str
    report_index_id: str
    batch_id: str
    registry_id: str
    aggregate_id: str
    strategy_index_id: str
    failure_taxonomy_report_id: str
    selected_strategy_id: str
    submission_mode: str
    total_checks: int
    passed_checks: int
    failed_checks: int
    blocking_issue_count: int
    warning_count: int
    ready_for_release_package: bool
    ready_for_kaggle_submission: bool
    kaggle_submission_sent: bool
    audit_checks: List[Dict[str, Any]]
    failed_check_ids: List[str]
    warning_check_ids: List[str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_candidate(
    candidate: Optional[LocalSubmissionCandidatePackage | Dict[str, Any]],
) -> Dict[str, Any]:
    if candidate is None:
        return build_local_submission_candidate_package().to_dict()

    if isinstance(candidate, LocalSubmissionCandidatePackage):
        return candidate.to_dict()

    if isinstance(candidate, dict):
        return copy.deepcopy(candidate)

    raise ValueError("Public readiness audit requires a LocalSubmissionCandidatePackage or dictionary")


def _artifact_exists(path: str) -> bool:
    return Path(path).exists()


def _make_check(
    *,
    check_name: str,
    category: str,
    passed: bool,
    severity: str,
    evidence: Dict[str, Any],
    remediation_hint: str,
) -> PublicReadinessAuditCheck:
    check_basis = {
        "check_name": check_name,
        "category": category,
        "passed": passed,
        "severity": severity,
        "evidence": evidence,
        "remediation_hint": remediation_hint,
    }
    signature = _stable_signature(check_basis)
    check_id = f"PUBLIC-READINESS-CHECK-{signature[:12]}"

    return PublicReadinessAuditCheck(
        status="PUBLIC_READINESS_AUDIT_CHECK_READY",
        check_id=check_id,
        check_name=check_name,
        category=category,
        passed=passed,
        severity=severity,
        evidence=evidence,
        remediation_hint=remediation_hint,
        signature=signature,
        metadata={
            "source": "public_readiness_audit_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def _build_audit_checks(candidate: Dict[str, Any]) -> List[PublicReadinessAuditCheck]:
    metadata = candidate.get("metadata") if isinstance(candidate.get("metadata"), dict) else {}
    local_payload = (
        candidate.get("local_submission_payload")
        if isinstance(candidate.get("local_submission_payload"), dict)
        else {}
    )

    expected_artifacts = {
        "local_submission_candidate_json": "examples/milestone-3/local-submission-candidate-builder/local-submission-candidate.json",
        "local_submission_candidate_md": "examples/milestone-3/local-submission-candidate-builder/local-submission-candidate.md",
        "report_index_json": "examples/milestone-3/report-index-generator/report-index.json",
        "report_index_md": "examples/milestone-3/report-index-generator/report-index.md",
        "failure_taxonomy_json": "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.json",
        "failure_taxonomy_md": "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.md",
    }
    artifact_status = {key: _artifact_exists(path) for key, path in expected_artifacts.items()}

    checks = [
        _make_check(
            check_name="candidate_contract_valid",
            category="contract",
            passed=validate_local_submission_candidate_package(candidate)["status"]
            == "LOCAL_SUBMISSION_CANDIDATE_VALID",
            severity="BLOCKER",
            evidence={
                "candidate_status": candidate.get("candidate_status"),
                "candidate_id": candidate.get("candidate_id"),
            },
            remediation_hint="Regenerate the local submission candidate package before public audit.",
        ),
        _make_check(
            check_name="local_dry_run_only",
            category="submission_boundary",
            passed=candidate.get("submission_mode") == "LOCAL_DRY_RUN_ONLY"
            and local_payload.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
            severity="BLOCKER",
            evidence={
                "candidate_submission_mode": candidate.get("submission_mode"),
                "payload_submission_mode": local_payload.get("submission_mode"),
            },
            remediation_hint="Force submission mode to LOCAL_DRY_RUN_ONLY before any public release package.",
        ),
        _make_check(
            check_name="kaggle_submission_not_sent",
            category="submission_boundary",
            passed=candidate.get("kaggle_submission_sent") is False
            and local_payload.get("kaggle_submission_sent") is False,
            severity="BLOCKER",
            evidence={
                "candidate_kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
                "payload_kaggle_submission_sent": local_payload.get("kaggle_submission_sent"),
            },
            remediation_hint="Block audit if any Kaggle submission flag is true.",
        ),
        _make_check(
            check_name="not_ready_for_kaggle_submission",
            category="submission_boundary",
            passed=candidate.get("ready_for_kaggle_submission") is False
            and local_payload.get("ready_for_kaggle_submission") is False,
            severity="BLOCKER",
            evidence={
                "candidate_ready_for_kaggle_submission": candidate.get("ready_for_kaggle_submission"),
                "payload_ready_for_kaggle_submission": local_payload.get("ready_for_kaggle_submission"),
            },
            remediation_hint="Keep Kaggle readiness false until public readiness and release package gates pass.",
        ),
        _make_check(
            check_name="public_readiness_audit_enabled",
            category="readiness",
            passed=candidate.get("ready_for_public_readiness_audit") is True,
            severity="BLOCKER",
            evidence={
                "ready_for_public_readiness_audit": candidate.get("ready_for_public_readiness_audit"),
            },
            remediation_hint="Rebuild candidate package with ready_for_public_readiness_audit=true.",
        ),
        _make_check(
            check_name="public_safety_metadata",
            category="metadata_boundary",
            passed=metadata.get("public_safe") is True
            and metadata.get("deterministic") is True
            and metadata.get("private_core_exposure") is False,
            severity="BLOCKER",
            evidence={
                "public_safe": metadata.get("public_safe"),
                "deterministic": metadata.get("deterministic"),
                "private_core_exposure": metadata.get("private_core_exposure"),
            },
            remediation_hint="Fix candidate metadata before public packaging.",
        ),
        _make_check(
            check_name="no_external_dependency_or_credentials",
            category="metadata_boundary",
            passed=metadata.get("external_api_dependency") is False
            and metadata.get("contains_api_keys") is False
            and metadata.get("executes_dataset_code") is False,
            severity="BLOCKER",
            evidence={
                "external_api_dependency": metadata.get("external_api_dependency"),
                "contains_api_keys": metadata.get("contains_api_keys"),
                "executes_dataset_code": metadata.get("executes_dataset_code"),
            },
            remediation_hint="Remove external API, key, or executable dataset dependency before audit passes.",
        ),
        _make_check(
            check_name="artifact_presence",
            category="artifact_boundary",
            passed=all(artifact_status.values()),
            severity="BLOCKER",
            evidence={
                "artifact_status": artifact_status,
                "expected_artifacts": expected_artifacts,
            },
            remediation_hint="Regenerate missing public artifacts before release packaging.",
        ),
        _make_check(
            check_name="blocked_task_count_tracked",
            category="quality_gate",
            passed=isinstance(candidate.get("blocked_task_count"), int)
            and candidate.get("blocked_task_count") >= 0
            and isinstance(candidate.get("remediation_required_count"), int)
            and candidate.get("remediation_required_count") == candidate.get("blocked_task_count"),
            severity="WARNING",
            evidence={
                "blocked_task_count": candidate.get("blocked_task_count"),
                "remediation_required_count": candidate.get("remediation_required_count"),
            },
            remediation_hint="Align blocked task and remediation counts before advancing readiness.",
        ),
        _make_check(
            check_name="release_package_ready_not_submission_ready",
            category="release_boundary",
            passed=candidate.get("ready_for_public_readiness_audit") is True
            and candidate.get("ready_for_kaggle_submission") is False,
            severity="WARNING",
            evidence={
                "ready_for_public_readiness_audit": candidate.get("ready_for_public_readiness_audit"),
                "ready_for_kaggle_submission": candidate.get("ready_for_kaggle_submission"),
            },
            remediation_hint="Proceed only to dry-run release package, not Kaggle submission.",
        ),
    ]

    return checks


def build_public_readiness_audit_report(
    candidate: Optional[LocalSubmissionCandidatePackage | Dict[str, Any]] = None,
) -> PublicReadinessAuditReport:
    """Build deterministic public readiness audit report."""

    candidate_data = _coerce_candidate(candidate)
    candidate_validation = validate_local_submission_candidate_package(candidate_data)

    required_candidate_fields = {
        "candidate_id",
        "report_index_id",
        "batch_id",
        "registry_id",
        "aggregate_id",
        "strategy_index_id",
        "failure_taxonomy_report_id",
        "selected_strategy_id",
        "selected_strategy_name",
        "submission_mode",
        "task_count",
        "eligible_task_count",
        "blocked_task_count",
        "remediation_required_count",
        "ready_for_public_readiness_audit",
        "ready_for_kaggle_submission",
        "kaggle_submission_sent",
        "local_candidate_tasks",
        "local_submission_payload",
        "metadata",
    }
    missing_required_candidate_fields = [
        field for field in sorted(required_candidate_fields) if field not in candidate_data
    ]

    if candidate_validation["status"] != "LOCAL_SUBMISSION_CANDIDATE_VALID" and missing_required_candidate_fields:
        raise ValueError("Public readiness audit requires a valid LOCAL_SUBMISSION_CANDIDATE_VALID payload")

    checks = _build_audit_checks(candidate_data)
    checks_sorted = sorted(checks, key=lambda item: item.check_name)
    check_dicts = [item.to_dict() for item in checks_sorted]

    failed_checks = [item for item in checks_sorted if item.passed is False]
    blocker_failures = [
        item for item in failed_checks if item.severity == "BLOCKER"
    ]
    warning_failures = [
        item for item in failed_checks if item.severity == "WARNING"
    ]

    failed_check_ids = [item.check_id for item in failed_checks]
    warning_check_ids = [
        item.check_id
        for item in checks_sorted
        if item.severity == "WARNING"
    ]

    blocking_issue_count = len(blocker_failures)
    failed_checks_count = len(failed_checks)
    warning_count = len(warning_failures)

    ready_for_release_package = blocking_issue_count == 0
    ready_for_kaggle_submission = False
    kaggle_submission_sent = False

    signature_basis = {
        "candidate_id": candidate_data.get("candidate_id"),
        "total_checks": len(checks_sorted),
        "passed_checks": len(checks_sorted) - failed_checks_count,
        "failed_checks": failed_checks_count,
        "blocking_issue_count": blocking_issue_count,
        "warning_count": warning_count,
        "failed_check_ids": failed_check_ids,
        "ready_for_release_package": ready_for_release_package,
        "ready_for_kaggle_submission": ready_for_kaggle_submission,
        "kaggle_submission_sent": kaggle_submission_sent,
    }
    signature = _stable_signature(signature_basis)
    audit_id = f"PUBLIC-READINESS-AUDIT-{signature[:12]}"

    return PublicReadinessAuditReport(
        status="PUBLIC_READINESS_AUDIT_READY",
        audit_status="PUBLIC_READINESS_AUDIT_PASS" if ready_for_release_package else "PUBLIC_READINESS_AUDIT_FAIL",
        audit_id=audit_id,
        candidate_id=str(candidate_data.get("candidate_id")),
        report_index_id=str(candidate_data.get("report_index_id")),
        batch_id=str(candidate_data.get("batch_id")),
        registry_id=str(candidate_data.get("registry_id")),
        aggregate_id=str(candidate_data.get("aggregate_id")),
        strategy_index_id=str(candidate_data.get("strategy_index_id")),
        failure_taxonomy_report_id=str(candidate_data.get("failure_taxonomy_report_id")),
        selected_strategy_id=str(candidate_data.get("selected_strategy_id")),
        submission_mode=str(candidate_data.get("submission_mode")),
        total_checks=len(checks_sorted),
        passed_checks=len(checks_sorted) - failed_checks_count,
        failed_checks=failed_checks_count,
        blocking_issue_count=blocking_issue_count,
        warning_count=warning_count,
        ready_for_release_package=ready_for_release_package,
        ready_for_kaggle_submission=ready_for_kaggle_submission,
        kaggle_submission_sent=kaggle_submission_sent,
        audit_checks=check_dicts,
        failed_check_ids=failed_check_ids,
        warning_check_ids=warning_check_ids,
        signature=signature,
        metadata={
            "source": "public_readiness_audit_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_local_submission_candidate_builder": True,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 8",
        },
    )


def render_public_readiness_audit_markdown(report: PublicReadinessAuditReport | Dict[str, Any]) -> str:
    data = report.to_dict() if isinstance(report, PublicReadinessAuditReport) else dict(report)

    lines = [
        "# ARC-AGI-3 Public Readiness Audit v1",
        "",
        f"Status: {data['status']}",
        f"Audit status: {data['audit_status']}",
        f"Audit ID: {data['audit_id']}",
        f"Candidate ID: {data['candidate_id']}",
        f"Report index ID: {data['report_index_id']}",
        f"Submission mode: {data['submission_mode']}",
        f"Total checks: {data['total_checks']}",
        f"Passed checks: {data['passed_checks']}",
        f"Failed checks: {data['failed_checks']}",
        f"Blocking issues: {data['blocking_issue_count']}",
        f"Warnings: {data['warning_count']}",
        f"Ready for release package: {str(data['ready_for_release_package']).lower()}",
        f"Ready for Kaggle submission: {str(data['ready_for_kaggle_submission']).lower()}",
        f"Kaggle submission sent: {str(data['kaggle_submission_sent']).lower()}",
        "",
        "## Audit checks",
        "",
    ]

    for check in data.get("audit_checks", []):
        lines.extend(
            [
                f"### {check['check_name']}",
                "",
                f"- Check ID: {check['check_id']}",
                f"- Category: {check['category']}",
                f"- Passed: {str(check['passed']).lower()}",
                f"- Severity: {check['severity']}",
                f"- Remediation: {check['remediation_hint']}",
                f"- Signature: {check['signature']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary",
            "",
            "- local_only=true",
            "- dry_run_only=true",
            "- public_safe=true",
            "- deterministic=true",
            "- external_api_dependency=false",
            "- executes_dataset_code=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
            f"Audit signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_public_readiness_audit_report(
    report: PublicReadinessAuditReport | Dict[str, Any],
) -> Dict[str, Any]:
    """Validate Public Readiness Audit v1 contract."""

    data = report.to_dict() if isinstance(report, PublicReadinessAuditReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    checks_list = data.get("audit_checks") if isinstance(data.get("audit_checks"), list) else []

    check_checks = []
    for check in checks_list:
        check_metadata = check.get("metadata") if isinstance(check.get("metadata"), dict) else {}
        check_checks.append(
            check.get("status") == "PUBLIC_READINESS_AUDIT_CHECK_READY"
            and isinstance(check.get("check_id"), str)
            and isinstance(check.get("check_name"), str)
            and isinstance(check.get("category"), str)
            and isinstance(check.get("passed"), bool)
            and check.get("severity") in {"BLOCKER", "WARNING"}
            and isinstance(check.get("evidence"), dict)
            and isinstance(check.get("remediation_hint"), str)
            and isinstance(check.get("signature"), str)
            and check_metadata.get("public_safe") is True
            and check_metadata.get("deterministic") is True
            and check_metadata.get("external_api_dependency") is False
            and check_metadata.get("executes_dataset_code") is False
            and check_metadata.get("contains_api_keys") is False
            and check_metadata.get("kaggle_submission_sent") is False
            and check_metadata.get("private_core_exposure") is False
        )

    total_checks = data.get("total_checks")
    passed_checks = data.get("passed_checks")
    failed_checks = data.get("failed_checks")
    blocking_issue_count = data.get("blocking_issue_count")

    checks = {
        "status_ready": data.get("status") == "PUBLIC_READINESS_AUDIT_READY",
        "audit_status_pass": data.get("audit_status") == "PUBLIC_READINESS_AUDIT_PASS",
        "audit_id_present": bool(data.get("audit_id")),
        "candidate_id_present": bool(data.get("candidate_id")),
        "report_index_id_present": bool(data.get("report_index_id")),
        "submission_mode_local": data.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "total_checks_positive": isinstance(total_checks, int) and total_checks > 0,
        "total_checks_matches": total_checks == len(checks_list),
        "pass_fail_sum_matches": isinstance(passed_checks, int)
        and isinstance(failed_checks, int)
        and isinstance(total_checks, int)
        and passed_checks + failed_checks == total_checks,
        "blocking_issue_count_zero": blocking_issue_count == 0,
        "ready_for_release_package_true": data.get("ready_for_release_package") is True,
        "ready_for_kaggle_submission_false": data.get("ready_for_kaggle_submission") is False,
        "kaggle_submission_sent_false": data.get("kaggle_submission_sent") is False,
        "failed_check_ids_list": isinstance(data.get("failed_check_ids"), list),
        "warning_check_ids_list": isinstance(data.get("warning_check_ids"), list),
        "signature_present": bool(data.get("signature")),
        "all_checks_valid": bool(check_checks) and all(check_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_local_submission_candidate_builder": metadata.get("uses_local_submission_candidate_builder") is True,
        "uses_report_index_generator": metadata.get("uses_report_index_generator") is True,
        "uses_failure_taxonomy": metadata.get("uses_failure_taxonomy") is True,
        "uses_strategy_selection_index": metadata.get("uses_strategy_selection_index") is True,
        "uses_multi_task_outcome_aggregator": metadata.get("uses_multi_task_outcome_aggregator") is True,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "PUBLIC_READINESS_AUDIT_VALID" if valid else "PUBLIC_READINESS_AUDIT_INVALID",
        "valid": valid,
        "checks": checks,
        "audit_id": data.get("audit_id"),
        "candidate_id": data.get("candidate_id"),
        "total_checks": data.get("total_checks"),
        "passed_checks": data.get("passed_checks"),
        "failed_checks": data.get("failed_checks"),
        "blocking_issue_count": data.get("blocking_issue_count"),
        "warning_count": data.get("warning_count"),
        "ready_for_release_package": data.get("ready_for_release_package"),
        "ready_for_kaggle_submission": data.get("ready_for_kaggle_submission"),
        "kaggle_submission_sent": data.get("kaggle_submission_sent"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "public_readiness_audit_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_public_readiness_audit_report() -> Dict[str, Any]:
    report = build_public_readiness_audit_report()
    validation = validate_public_readiness_audit_report(report)

    return {
        "status": "PUBLIC_READINESS_AUDIT_PIPELINE_READY",
        "public_readiness_audit": report.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "public_readiness_audit_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_local_submission_candidate_builder": True,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_public_readiness_audit_artifacts(
    report: PublicReadinessAuditReport | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/public-readiness-audit",
) -> Dict[str, str]:
    data = report.to_dict() if isinstance(report, PublicReadinessAuditReport) else dict(report)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "public-readiness-audit.json"
    markdown_path = output_path / "public-readiness-audit.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_public_readiness_audit_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
