"""Milestone #3 Dry-Run Release Package v1 for HBCE ARC-AGI-3 public baseline.

This module builds a deterministic local-only dry-run release package manifest
from the Milestone #3 public chain.

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

from hbce_arc_agi3.public_readiness_audit import (
    PublicReadinessAuditReport,
    build_public_readiness_audit_report,
    validate_public_readiness_audit_report,
)


@dataclass(frozen=True)
class DryRunReleaseArtifact:
    status: str
    artifact_key: str
    artifact_title: str
    artifact_category: str
    path: str
    required: bool
    present: bool
    size_bytes: int
    sha256: str
    included_in_package: bool
    public_safe: bool
    deterministic: bool
    external_api_dependency: bool
    kaggle_submission_sent: bool
    private_core_exposure: bool
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Milestone3DryRunReleasePackage:
    status: str
    package_status: str
    package_id: str
    milestone: str
    release_mode: str
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
    source_artifact_count: int
    present_source_artifact_count: int
    missing_source_artifact_count: int
    generated_package_artifact_count: int
    total_package_artifact_count: int
    blocking_issue_count: int
    warning_count: int
    ready_for_milestone_3_closure: bool
    ready_for_kaggle_submission: bool
    kaggle_submission_sent: bool
    artifact_manifest: List[Dict[str, Any]]
    missing_artifact_keys: List[str]
    artifact_signatures: Dict[str, str]
    source_chain_ids: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _file_sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return sha256(path.read_bytes()).hexdigest()


def _file_size(path: Path) -> int:
    if not path.exists() or not path.is_file():
        return 0
    return path.stat().st_size


def _coerce_audit(
    audit_report: Optional[PublicReadinessAuditReport | Dict[str, Any]],
) -> Dict[str, Any]:
    if audit_report is None:
        return build_public_readiness_audit_report().to_dict()

    if isinstance(audit_report, PublicReadinessAuditReport):
        return audit_report.to_dict()

    if isinstance(audit_report, dict):
        return copy.deepcopy(audit_report)

    raise ValueError("Dry-run release package requires a PublicReadinessAuditReport or dictionary")


def _source_artifact_specs() -> List[Dict[str, str]]:
    return [
        {
            "artifact_key": "dataset_sample_registry_doc",
            "artifact_title": "Dataset Sample Registry documentation",
            "artifact_category": "documentation",
            "path": "docs/dataset-sample-registry-v1.md",
        },
        {
            "artifact_key": "dataset_sample_registry_json",
            "artifact_title": "Dataset Sample Registry JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/dataset-sample-registry/dataset-sample-registry.json",
        },
        {
            "artifact_key": "dataset_sample_registry_md",
            "artifact_title": "Dataset Sample Registry Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/dataset-sample-registry/dataset-sample-registry.md",
        },
        {
            "artifact_key": "batch_benchmark_runner_doc",
            "artifact_title": "Batch Benchmark Runner documentation",
            "artifact_category": "documentation",
            "path": "docs/batch-benchmark-runner-v1.md",
        },
        {
            "artifact_key": "batch_benchmark_run_json",
            "artifact_title": "Batch Benchmark Run JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.json",
        },
        {
            "artifact_key": "batch_benchmark_run_md",
            "artifact_title": "Batch Benchmark Run Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.md",
        },
        {
            "artifact_key": "multi_task_outcome_aggregator_doc",
            "artifact_title": "Multi-Task Outcome Aggregator documentation",
            "artifact_category": "documentation",
            "path": "docs/multi-task-outcome-aggregator-v1.md",
        },
        {
            "artifact_key": "multi_task_outcome_aggregate_json",
            "artifact_title": "Multi-Task Outcome Aggregate JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.json",
        },
        {
            "artifact_key": "multi_task_outcome_aggregate_md",
            "artifact_title": "Multi-Task Outcome Aggregate Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.md",
        },
        {
            "artifact_key": "strategy_selection_index_doc",
            "artifact_title": "Strategy Selection Index documentation",
            "artifact_category": "documentation",
            "path": "docs/strategy-selection-index-v1.md",
        },
        {
            "artifact_key": "strategy_selection_index_json",
            "artifact_title": "Strategy Selection Index JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/strategy-selection-index/strategy-selection-index.json",
        },
        {
            "artifact_key": "strategy_selection_index_md",
            "artifact_title": "Strategy Selection Index Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/strategy-selection-index/strategy-selection-index.md",
        },
        {
            "artifact_key": "failure_taxonomy_doc",
            "artifact_title": "Failure Taxonomy documentation",
            "artifact_category": "documentation",
            "path": "docs/failure-taxonomy-v1.md",
        },
        {
            "artifact_key": "failure_taxonomy_json",
            "artifact_title": "Failure Taxonomy JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.json",
        },
        {
            "artifact_key": "failure_taxonomy_md",
            "artifact_title": "Failure Taxonomy Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.md",
        },
        {
            "artifact_key": "report_index_generator_doc",
            "artifact_title": "Report Index Generator documentation",
            "artifact_category": "documentation",
            "path": "docs/report-index-generator-v1.md",
        },
        {
            "artifact_key": "report_index_json",
            "artifact_title": "Report Index JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/report-index-generator/report-index.json",
        },
        {
            "artifact_key": "report_index_md",
            "artifact_title": "Report Index Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/report-index-generator/report-index.md",
        },
        {
            "artifact_key": "local_submission_candidate_doc",
            "artifact_title": "Local Submission Candidate Builder documentation",
            "artifact_category": "documentation",
            "path": "docs/local-submission-candidate-builder-v1.md",
        },
        {
            "artifact_key": "local_submission_candidate_json",
            "artifact_title": "Local Submission Candidate JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/local-submission-candidate-builder/local-submission-candidate.json",
        },
        {
            "artifact_key": "local_submission_candidate_md",
            "artifact_title": "Local Submission Candidate Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/local-submission-candidate-builder/local-submission-candidate.md",
        },
        {
            "artifact_key": "public_readiness_audit_doc",
            "artifact_title": "Public Readiness Audit documentation",
            "artifact_category": "documentation",
            "path": "docs/public-readiness-audit-v1.md",
        },
        {
            "artifact_key": "public_readiness_audit_json",
            "artifact_title": "Public Readiness Audit JSON",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/public-readiness-audit/public-readiness-audit.json",
        },
        {
            "artifact_key": "public_readiness_audit_md",
            "artifact_title": "Public Readiness Audit Markdown",
            "artifact_category": "public_artifact",
            "path": "examples/milestone-3/public-readiness-audit/public-readiness-audit.md",
        },
    ]


def _build_release_artifact(spec: Dict[str, str]) -> DryRunReleaseArtifact:
    artifact_path = Path(spec["path"])
    present = artifact_path.exists() and artifact_path.is_file()
    file_hash = _file_sha256(artifact_path)
    size_bytes = _file_size(artifact_path)

    basis = {
        "artifact_key": spec["artifact_key"],
        "artifact_title": spec["artifact_title"],
        "artifact_category": spec["artifact_category"],
        "path": spec["path"],
        "present": present,
        "size_bytes": size_bytes,
        "sha256": file_hash,
    }
    signature = _stable_signature(basis)

    return DryRunReleaseArtifact(
        status="DRY_RUN_RELEASE_ARTIFACT_READY" if present else "DRY_RUN_RELEASE_ARTIFACT_MISSING",
        artifact_key=spec["artifact_key"],
        artifact_title=spec["artifact_title"],
        artifact_category=spec["artifact_category"],
        path=spec["path"],
        required=True,
        present=present,
        size_bytes=size_bytes,
        sha256=file_hash,
        included_in_package=present,
        public_safe=True,
        deterministic=True,
        external_api_dependency=False,
        kaggle_submission_sent=False,
        private_core_exposure=False,
        signature=signature,
        metadata={
            "source": "milestone_3_dry_run_release_package_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def build_milestone_3_dry_run_release_package(
    audit_report: Optional[PublicReadinessAuditReport | Dict[str, Any]] = None,
) -> Milestone3DryRunReleasePackage:
    """Build deterministic Milestone #3 dry-run release package."""

    audit_data = _coerce_audit(audit_report)
    audit_validation = validate_public_readiness_audit_report(audit_data)

    if audit_validation["status"] != "PUBLIC_READINESS_AUDIT_VALID":
        raise ValueError("Dry-run release package requires a valid PUBLIC_READINESS_AUDIT_VALID payload")

    artifacts = [_build_release_artifact(spec) for spec in _source_artifact_specs()]
    artifacts_sorted = sorted(artifacts, key=lambda item: item.artifact_key)
    artifact_dicts = [artifact.to_dict() for artifact in artifacts_sorted]

    source_artifact_count = len(artifacts_sorted)
    present_source_artifact_count = sum(1 for artifact in artifacts_sorted if artifact.present)
    missing_artifact_keys = [
        artifact.artifact_key for artifact in artifacts_sorted if not artifact.present
    ]
    missing_source_artifact_count = len(missing_artifact_keys)
    generated_package_artifact_count = 2
    total_package_artifact_count = source_artifact_count + generated_package_artifact_count

    ready_for_milestone_3_closure = (
        audit_data.get("audit_status") == "PUBLIC_READINESS_AUDIT_PASS"
        and audit_data.get("ready_for_release_package") is True
        and missing_source_artifact_count == 0
        and audit_data.get("ready_for_kaggle_submission") is False
        and audit_data.get("kaggle_submission_sent") is False
    )

    ready_for_kaggle_submission = False
    kaggle_submission_sent = False

    source_chain_ids = {
        "audit_id": str(audit_data.get("audit_id")),
        "candidate_id": str(audit_data.get("candidate_id")),
        "report_index_id": str(audit_data.get("report_index_id")),
        "batch_id": str(audit_data.get("batch_id")),
        "registry_id": str(audit_data.get("registry_id")),
        "aggregate_id": str(audit_data.get("aggregate_id")),
        "strategy_index_id": str(audit_data.get("strategy_index_id")),
        "failure_taxonomy_report_id": str(audit_data.get("failure_taxonomy_report_id")),
        "selected_strategy_id": str(audit_data.get("selected_strategy_id")),
    }

    artifact_signatures = {
        artifact.artifact_key: artifact.signature for artifact in artifacts_sorted
    }

    signature_basis = {
        "milestone": "Milestone #3",
        "release_mode": "MILESTONE_3_LOCAL_DRY_RUN_RELEASE_PACKAGE_ONLY",
        "source_artifact_count": source_artifact_count,
        "present_source_artifact_count": present_source_artifact_count,
        "missing_source_artifact_count": missing_source_artifact_count,
        "generated_package_artifact_count": generated_package_artifact_count,
        "total_package_artifact_count": total_package_artifact_count,
        "source_chain_ids": source_chain_ids,
        "artifact_signatures": artifact_signatures,
        "ready_for_milestone_3_closure": ready_for_milestone_3_closure,
        "ready_for_kaggle_submission": ready_for_kaggle_submission,
        "kaggle_submission_sent": kaggle_submission_sent,
    }
    signature = _stable_signature(signature_basis)
    package_id = f"MILESTONE-3-DRY-RUN-RELEASE-PACKAGE-{signature[:12]}"

    return Milestone3DryRunReleasePackage(
        status="MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_READY",
        package_status="MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"
        if ready_for_milestone_3_closure
        else "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_INVALID",
        package_id=package_id,
        milestone="Milestone #3",
        release_mode="MILESTONE_3_LOCAL_DRY_RUN_RELEASE_PACKAGE_ONLY",
        audit_id=source_chain_ids["audit_id"],
        candidate_id=source_chain_ids["candidate_id"],
        report_index_id=source_chain_ids["report_index_id"],
        batch_id=source_chain_ids["batch_id"],
        registry_id=source_chain_ids["registry_id"],
        aggregate_id=source_chain_ids["aggregate_id"],
        strategy_index_id=source_chain_ids["strategy_index_id"],
        failure_taxonomy_report_id=source_chain_ids["failure_taxonomy_report_id"],
        selected_strategy_id=source_chain_ids["selected_strategy_id"],
        submission_mode=str(audit_data.get("submission_mode")),
        source_artifact_count=source_artifact_count,
        present_source_artifact_count=present_source_artifact_count,
        missing_source_artifact_count=missing_source_artifact_count,
        generated_package_artifact_count=generated_package_artifact_count,
        total_package_artifact_count=total_package_artifact_count,
        blocking_issue_count=int(audit_data.get("blocking_issue_count")),
        warning_count=int(audit_data.get("warning_count")),
        ready_for_milestone_3_closure=ready_for_milestone_3_closure,
        ready_for_kaggle_submission=ready_for_kaggle_submission,
        kaggle_submission_sent=kaggle_submission_sent,
        artifact_manifest=artifact_dicts,
        missing_artifact_keys=missing_artifact_keys,
        artifact_signatures=artifact_signatures,
        source_chain_ids=source_chain_ids,
        signature=signature,
        metadata={
            "source": "milestone_3_dry_run_release_package_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_public_readiness_audit": True,
            "uses_local_submission_candidate_builder": True,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 9",
        },
    )


def render_milestone_3_dry_run_release_package_markdown(
    package: Milestone3DryRunReleasePackage | Dict[str, Any],
) -> str:
    data = package.to_dict() if isinstance(package, Milestone3DryRunReleasePackage) else dict(package)

    lines = [
        "# ARC-AGI-3 Milestone #3 Dry-Run Release Package v1",
        "",
        f"Status: {data['status']}",
        f"Package status: {data['package_status']}",
        f"Package ID: {data['package_id']}",
        f"Milestone: {data['milestone']}",
        f"Release mode: {data['release_mode']}",
        f"Audit ID: {data['audit_id']}",
        f"Candidate ID: {data['candidate_id']}",
        f"Report index ID: {data['report_index_id']}",
        f"Submission mode: {data['submission_mode']}",
        f"Source artifact count: {data['source_artifact_count']}",
        f"Present source artifact count: {data['present_source_artifact_count']}",
        f"Missing source artifact count: {data['missing_source_artifact_count']}",
        f"Generated package artifact count: {data['generated_package_artifact_count']}",
        f"Total package artifact count: {data['total_package_artifact_count']}",
        f"Blocking issues: {data['blocking_issue_count']}",
        f"Warnings: {data['warning_count']}",
        f"Ready for Milestone #3 closure: {str(data['ready_for_milestone_3_closure']).lower()}",
        f"Ready for Kaggle submission: {str(data['ready_for_kaggle_submission']).lower()}",
        f"Kaggle submission sent: {str(data['kaggle_submission_sent']).lower()}",
        "",
        "## Artifact manifest",
        "",
    ]

    for artifact in data.get("artifact_manifest", []):
        lines.extend(
            [
                f"### {artifact['artifact_key']}",
                "",
                f"- Title: {artifact['artifact_title']}",
                f"- Category: {artifact['artifact_category']}",
                f"- Path: `{artifact['path']}`",
                f"- Present: {str(artifact['present']).lower()}",
                f"- Size bytes: {artifact['size_bytes']}",
                f"- SHA-256: `{artifact['sha256']}`",
                f"- Signature: {artifact['signature']}",
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
            f"Package signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_milestone_3_dry_run_release_package(
    package: Milestone3DryRunReleasePackage | Dict[str, Any],
) -> Dict[str, Any]:
    """Validate Milestone #3 Dry-Run Release Package v1 contract."""

    data = package.to_dict() if isinstance(package, Milestone3DryRunReleasePackage) else dict(package)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    artifacts = data.get("artifact_manifest") if isinstance(data.get("artifact_manifest"), list) else []

    artifact_checks = []
    for artifact in artifacts:
        artifact_metadata = artifact.get("metadata") if isinstance(artifact.get("metadata"), dict) else {}
        artifact_checks.append(
            artifact.get("status") == "DRY_RUN_RELEASE_ARTIFACT_READY"
            and isinstance(artifact.get("artifact_key"), str)
            and isinstance(artifact.get("artifact_title"), str)
            and isinstance(artifact.get("artifact_category"), str)
            and isinstance(artifact.get("path"), str)
            and artifact.get("required") is True
            and artifact.get("present") is True
            and isinstance(artifact.get("size_bytes"), int)
            and artifact.get("size_bytes") > 0
            and isinstance(artifact.get("sha256"), str)
            and len(artifact.get("sha256")) == 64
            and artifact.get("included_in_package") is True
            and artifact.get("public_safe") is True
            and artifact.get("deterministic") is True
            and artifact.get("external_api_dependency") is False
            and artifact.get("kaggle_submission_sent") is False
            and artifact.get("private_core_exposure") is False
            and isinstance(artifact.get("signature"), str)
            and artifact_metadata.get("public_safe") is True
            and artifact_metadata.get("deterministic") is True
            and artifact_metadata.get("local_only") is True
            and artifact_metadata.get("dry_run_only") is True
            and artifact_metadata.get("external_api_dependency") is False
            and artifact_metadata.get("executes_dataset_code") is False
            and artifact_metadata.get("contains_api_keys") is False
            and artifact_metadata.get("kaggle_submission_sent") is False
            and artifact_metadata.get("private_core_exposure") is False
        )

    source_artifact_count = data.get("source_artifact_count")
    present_source_artifact_count = data.get("present_source_artifact_count")
    missing_source_artifact_count = data.get("missing_source_artifact_count")
    generated_package_artifact_count = data.get("generated_package_artifact_count")
    total_package_artifact_count = data.get("total_package_artifact_count")

    checks = {
        "status_ready": data.get("status") == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_READY",
        "package_status_valid": data.get("package_status") == "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID",
        "package_id_present": bool(data.get("package_id")),
        "milestone_matches": data.get("milestone") == "Milestone #3",
        "release_mode_local_dry_run": data.get("release_mode")
        == "MILESTONE_3_LOCAL_DRY_RUN_RELEASE_PACKAGE_ONLY",
        "audit_id_present": bool(data.get("audit_id")),
        "candidate_id_present": bool(data.get("candidate_id")),
        "report_index_id_present": bool(data.get("report_index_id")),
        "submission_mode_local": data.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "source_artifact_count_matches": source_artifact_count == len(artifacts),
        "present_source_artifact_count_matches": present_source_artifact_count == len(artifacts),
        "missing_source_artifact_count_zero": missing_source_artifact_count == 0,
        "generated_package_artifact_count_two": generated_package_artifact_count == 2,
        "total_package_artifact_count_matches": isinstance(total_package_artifact_count, int)
        and isinstance(source_artifact_count, int)
        and isinstance(generated_package_artifact_count, int)
        and total_package_artifact_count == source_artifact_count + generated_package_artifact_count,
        "blocking_issue_count_zero": data.get("blocking_issue_count") == 0,
        "ready_for_milestone_3_closure_true": data.get("ready_for_milestone_3_closure") is True,
        "ready_for_kaggle_submission_false": data.get("ready_for_kaggle_submission") is False,
        "kaggle_submission_sent_false": data.get("kaggle_submission_sent") is False,
        "artifact_manifest_non_empty": bool(artifacts),
        "missing_artifact_keys_empty": data.get("missing_artifact_keys") == [],
        "artifact_signatures_dict": isinstance(data.get("artifact_signatures"), dict),
        "source_chain_ids_dict": isinstance(data.get("source_chain_ids"), dict),
        "signature_present": bool(data.get("signature")),
        "all_artifacts_valid": bool(artifact_checks) and all(artifact_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_public_readiness_audit": metadata.get("uses_public_readiness_audit") is True,
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
        "status": "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_VALID"
        if valid
        else "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_INVALID",
        "valid": valid,
        "checks": checks,
        "package_id": data.get("package_id"),
        "source_artifact_count": data.get("source_artifact_count"),
        "present_source_artifact_count": data.get("present_source_artifact_count"),
        "missing_source_artifact_count": data.get("missing_source_artifact_count"),
        "generated_package_artifact_count": data.get("generated_package_artifact_count"),
        "total_package_artifact_count": data.get("total_package_artifact_count"),
        "ready_for_milestone_3_closure": data.get("ready_for_milestone_3_closure"),
        "ready_for_kaggle_submission": data.get("ready_for_kaggle_submission"),
        "kaggle_submission_sent": data.get("kaggle_submission_sent"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "milestone_3_dry_run_release_package_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_milestone_3_dry_run_release_package() -> Dict[str, Any]:
    package = build_milestone_3_dry_run_release_package()
    validation = validate_milestone_3_dry_run_release_package(package)

    return {
        "status": "MILESTONE_3_DRY_RUN_RELEASE_PACKAGE_PIPELINE_READY",
        "dry_run_release_package": package.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "milestone_3_dry_run_release_package_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_public_readiness_audit": True,
            "uses_local_submission_candidate_builder": True,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_milestone_3_dry_run_release_package_artifacts(
    package: Milestone3DryRunReleasePackage | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/dry-run-release-package",
) -> Dict[str, str]:
    data = package.to_dict() if isinstance(package, Milestone3DryRunReleasePackage) else dict(package)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "milestone-3-dry-run-release-package.json"
    markdown_path = output_path / "milestone-3-dry-run-release-package.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_milestone_3_dry_run_release_package_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
