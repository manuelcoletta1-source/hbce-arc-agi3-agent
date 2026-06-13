"""Local Submission Candidate Builder v1 for HBCE ARC-AGI-3 public baseline.

This module builds a deterministic local-only submission candidate package from
the public Milestone #3 chain.

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

from hbce_arc_agi3.batch_benchmark_runner import run_batch_benchmark, validate_batch_benchmark_run
from hbce_arc_agi3.failure_taxonomy import build_failure_taxonomy_report, validate_failure_taxonomy_report
from hbce_arc_agi3.multi_task_outcome_aggregator import (
    aggregate_multi_task_outcomes,
    validate_multi_task_outcome_aggregate,
)
from hbce_arc_agi3.report_index_generator import ReportIndex, build_report_index, validate_report_index
from hbce_arc_agi3.strategy_selection_index import build_strategy_selection_index, validate_strategy_selection_index


@dataclass(frozen=True)
class LocalSubmissionCandidateTask:
    status: str
    task_id: str
    sample_id: str
    sample_name: str
    selected_strategy_id: str
    selected_strategy_name: str
    outcome_status: str
    failure_class: str
    severity: str
    eligible_for_submission: bool
    local_output_status: str
    local_prediction_ref: str
    remediation_required: bool
    evidence: Dict[str, Any]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LocalSubmissionCandidatePackage:
    status: str
    candidate_status: str
    candidate_id: str
    report_index_id: str
    batch_id: str
    registry_id: str
    aggregate_id: str
    strategy_index_id: str
    failure_taxonomy_report_id: str
    selected_strategy_id: str
    selected_strategy_name: str
    submission_mode: str
    task_count: int
    eligible_task_count: int
    blocked_task_count: int
    remediation_required_count: int
    ready_for_public_readiness_audit: bool
    ready_for_kaggle_submission: bool
    kaggle_submission_sent: bool
    local_candidate_tasks: List[Dict[str, Any]]
    local_submission_payload: Dict[str, Any]
    candidate_task_ids: List[str]
    candidate_task_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_report_index(report_index: Optional[ReportIndex | Dict[str, Any]]) -> Dict[str, Any]:
    if report_index is None:
        return build_report_index().to_dict()

    if isinstance(report_index, ReportIndex):
        return report_index.to_dict()

    if isinstance(report_index, dict):
        return copy.deepcopy(report_index)

    raise ValueError("Local submission candidate requires a ReportIndex or dictionary")


def _build_failure_entry_map(taxonomy_report: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    entries = taxonomy_report.get("taxonomy_entries")
    if not isinstance(entries, list):
        raise ValueError("Local submission candidate requires taxonomy_entries list")

    return {
        str(entry.get("task_id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("task_id")
    }


def _local_output_status(outcome_status: str, failure_class: str, severity: str) -> str:
    if outcome_status == "OUTCOME_MATCH" and failure_class == "NO_FAILURE_EXACT_MATCH":
        return "LOCAL_TASK_OUTPUT_ACCEPTED_BASELINE"

    if outcome_status == "OUTCOME_PARTIAL":
        return "LOCAL_TASK_OUTPUT_PARTIAL_REPAIR_REQUIRED"

    if outcome_status == "OUTCOME_UNVERIFIED":
        return "LOCAL_TASK_OUTPUT_BLOCKED_UNVERIFIED"

    if severity == "HIGH":
        return "LOCAL_TASK_OUTPUT_BLOCKED_HIGH_SEVERITY"

    return "LOCAL_TASK_OUTPUT_BLOCKED_REVIEW_REQUIRED"


def build_local_submission_candidate_task(
    outcome_record: Dict[str, Any],
    taxonomy_entry: Dict[str, Any],
    *,
    selected_strategy_id: str,
    selected_strategy_name: str,
) -> LocalSubmissionCandidateTask:
    """Build one local-only candidate task entry."""

    if not isinstance(outcome_record, dict):
        raise ValueError("Local submission candidate outcome record must be a dictionary")

    if not isinstance(taxonomy_entry, dict):
        raise ValueError("Local submission candidate taxonomy entry must be a dictionary")

    task_id = str(outcome_record.get("task_id") or "").strip()
    sample_id = str(outcome_record.get("sample_id") or "").strip()
    sample_name = str(outcome_record.get("sample_name") or "").strip()
    outcome_status = str(outcome_record.get("outcome_status") or "").strip()
    failure_class = str(taxonomy_entry.get("failure_class") or "").strip()
    severity = str(taxonomy_entry.get("severity") or "").strip()

    if not task_id:
        raise ValueError("Local submission candidate task requires task_id")
    if not sample_id:
        raise ValueError("Local submission candidate task requires sample_id")
    if not sample_name:
        raise ValueError("Local submission candidate task requires sample_name")
    if not outcome_status:
        raise ValueError("Local submission candidate task requires outcome_status")
    if not failure_class:
        raise ValueError("Local submission candidate task requires failure_class")
    if not severity:
        raise ValueError("Local submission candidate task requires severity")

    eligible_for_submission = (
        outcome_status == "OUTCOME_MATCH"
        and failure_class == "NO_FAILURE_EXACT_MATCH"
        and taxonomy_entry.get("is_failure") is False
        and severity == "NONE"
    )
    remediation_required = not eligible_for_submission
    local_output_status = _local_output_status(outcome_status, failure_class, severity)

    prediction_basis = {
        "task_id": task_id,
        "sample_id": sample_id,
        "selected_strategy_id": selected_strategy_id,
        "outcome_status": outcome_status,
        "failure_class": failure_class,
        "severity": severity,
        "eligible_for_submission": eligible_for_submission,
    }
    prediction_ref = f"LOCAL-PREDICTION-{_stable_signature(prediction_basis)[:12]}"

    signature_basis = {
        **prediction_basis,
        "sample_name": sample_name,
        "selected_strategy_name": selected_strategy_name,
        "local_output_status": local_output_status,
        "local_prediction_ref": prediction_ref,
        "remediation_required": remediation_required,
    }
    signature = _stable_signature(signature_basis)

    return LocalSubmissionCandidateTask(
        status="LOCAL_SUBMISSION_CANDIDATE_TASK_READY",
        task_id=task_id,
        sample_id=sample_id,
        sample_name=sample_name,
        selected_strategy_id=selected_strategy_id,
        selected_strategy_name=selected_strategy_name,
        outcome_status=outcome_status,
        failure_class=failure_class,
        severity=severity,
        eligible_for_submission=eligible_for_submission,
        local_output_status=local_output_status,
        local_prediction_ref=prediction_ref,
        remediation_required=remediation_required,
        evidence={
            "outcome_signature": outcome_record.get("signature"),
            "taxonomy_signature": taxonomy_entry.get("signature"),
            "taxonomy_id": taxonomy_entry.get("taxonomy_id"),
            "cell_accuracy": outcome_record.get("cell_accuracy"),
            "mismatch_count": outcome_record.get("mismatch_count"),
            "remediation_hint": taxonomy_entry.get("remediation_hint"),
        },
        signature=signature,
        metadata={
            "source": "local_submission_candidate_builder_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    )


def build_local_submission_candidate_package(
    report_index: Optional[ReportIndex | Dict[str, Any]] = None,
) -> LocalSubmissionCandidatePackage:
    """Build deterministic local-only submission candidate package."""

    report_index_data = _coerce_report_index(report_index)
    report_validation = validate_report_index(report_index_data)

    if report_validation["status"] != "REPORT_INDEX_VALID":
        raise ValueError("Local submission candidate requires a valid REPORT_INDEX_VALID payload")

    batch = run_batch_benchmark()
    batch_data = batch.to_dict() if hasattr(batch, "to_dict") else dict(batch)
    batch_validation = validate_batch_benchmark_run(batch_data)

    if batch_validation["status"] != "BATCH_BENCHMARK_RUN_VALID":
        raise ValueError("Local submission candidate requires a valid BATCH_BENCHMARK_RUN_VALID payload")

    aggregate = aggregate_multi_task_outcomes(batch_data)
    aggregate_validation = validate_multi_task_outcome_aggregate(aggregate)

    if aggregate_validation["status"] != "MULTI_TASK_OUTCOME_AGGREGATE_VALID":
        raise ValueError("Local submission candidate requires a valid MULTI_TASK_OUTCOME_AGGREGATE_VALID payload")

    strategy_index = build_strategy_selection_index(aggregate)
    strategy_validation = validate_strategy_selection_index(strategy_index)

    if strategy_validation["status"] != "STRATEGY_SELECTION_INDEX_VALID":
        raise ValueError("Local submission candidate requires a valid STRATEGY_SELECTION_INDEX_VALID payload")

    taxonomy = build_failure_taxonomy_report(aggregate, strategy_index)
    taxonomy_validation = validate_failure_taxonomy_report(taxonomy)

    if taxonomy_validation["status"] != "FAILURE_TAXONOMY_VALID":
        raise ValueError("Local submission candidate requires a valid FAILURE_TAXONOMY_VALID payload")

    taxonomy_data = taxonomy.to_dict()
    taxonomy_by_task_id = _build_failure_entry_map(taxonomy_data)

    candidate_tasks = []
    for outcome_record in aggregate.outcome_records:
        task_id = str(outcome_record.get("task_id"))
        taxonomy_entry = taxonomy_by_task_id.get(task_id)
        if taxonomy_entry is None:
            raise ValueError(f"Missing taxonomy entry for task_id={task_id}")

        candidate_tasks.append(
            build_local_submission_candidate_task(
                outcome_record,
                taxonomy_entry,
                selected_strategy_id=strategy_index.selected_strategy_id,
                selected_strategy_name=strategy_index.selected_strategy_name,
            )
        )

    candidate_tasks_sorted = sorted(candidate_tasks, key=lambda item: item.task_id)
    candidate_task_dicts = [item.to_dict() for item in candidate_tasks_sorted]

    eligible_task_count = sum(1 for item in candidate_tasks_sorted if item.eligible_for_submission)
    blocked_task_count = sum(1 for item in candidate_tasks_sorted if not item.eligible_for_submission)
    remediation_required_count = sum(1 for item in candidate_tasks_sorted if item.remediation_required)

    local_submission_payload = {
        "submission_mode": "LOCAL_DRY_RUN_ONLY",
        "kaggle_submission_sent": False,
        "ready_for_kaggle_submission": False,
        "selected_strategy_id": strategy_index.selected_strategy_id,
        "selected_strategy_name": strategy_index.selected_strategy_name,
        "tasks": {
            item.sample_id: {
                "task_id": item.task_id,
                "sample_name": item.sample_name,
                "local_prediction_ref": item.local_prediction_ref,
                "local_output_status": item.local_output_status,
                "eligible_for_submission": item.eligible_for_submission,
                "remediation_required": item.remediation_required,
            }
            for item in candidate_tasks_sorted
        },
    }

    candidate_task_ids = [item.task_id for item in candidate_tasks_sorted]
    candidate_task_signatures = {item.task_id: item.signature for item in candidate_tasks_sorted}

    ready_for_kaggle_submission = False
    ready_for_public_readiness_audit = True

    signature_basis = {
        "report_index_id": report_index_data.get("report_index_id"),
        "batch_id": batch_data.get("batch_id"),
        "registry_id": batch_data.get("registry_id"),
        "aggregate_id": aggregate.aggregate_id,
        "strategy_index_id": strategy_index.index_id,
        "failure_taxonomy_report_id": taxonomy.taxonomy_report_id,
        "selected_strategy_id": strategy_index.selected_strategy_id,
        "task_count": len(candidate_tasks_sorted),
        "eligible_task_count": eligible_task_count,
        "blocked_task_count": blocked_task_count,
        "remediation_required_count": remediation_required_count,
        "candidate_task_ids": candidate_task_ids,
        "candidate_task_signatures": candidate_task_signatures,
        "ready_for_kaggle_submission": ready_for_kaggle_submission,
        "kaggle_submission_sent": False,
    }
    signature = _stable_signature(signature_basis)
    candidate_id = f"LOCAL-SUBMISSION-CANDIDATE-{signature[:12]}"

    return LocalSubmissionCandidatePackage(
        status="LOCAL_SUBMISSION_CANDIDATE_BUILDER_READY",
        candidate_status="LOCAL_SUBMISSION_CANDIDATE_VALID",
        candidate_id=candidate_id,
        report_index_id=str(report_index_data.get("report_index_id")),
        batch_id=str(batch_data.get("batch_id")),
        registry_id=str(batch_data.get("registry_id")),
        aggregate_id=aggregate.aggregate_id,
        strategy_index_id=strategy_index.index_id,
        failure_taxonomy_report_id=taxonomy.taxonomy_report_id,
        selected_strategy_id=strategy_index.selected_strategy_id,
        selected_strategy_name=strategy_index.selected_strategy_name,
        submission_mode="LOCAL_DRY_RUN_ONLY",
        task_count=len(candidate_tasks_sorted),
        eligible_task_count=eligible_task_count,
        blocked_task_count=blocked_task_count,
        remediation_required_count=remediation_required_count,
        ready_for_public_readiness_audit=ready_for_public_readiness_audit,
        ready_for_kaggle_submission=ready_for_kaggle_submission,
        kaggle_submission_sent=False,
        local_candidate_tasks=candidate_task_dicts,
        local_submission_payload=local_submission_payload,
        candidate_task_ids=candidate_task_ids,
        candidate_task_signatures=candidate_task_signatures,
        signature=signature,
        metadata={
            "source": "local_submission_candidate_builder_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 7",
        },
    )


def render_local_submission_candidate_markdown(
    package: LocalSubmissionCandidatePackage | Dict[str, Any],
) -> str:
    data = package.to_dict() if isinstance(package, LocalSubmissionCandidatePackage) else dict(package)

    lines = [
        "# ARC-AGI-3 Local Submission Candidate Builder v1",
        "",
        f"Status: {data['status']}",
        f"Candidate status: {data['candidate_status']}",
        f"Candidate ID: {data['candidate_id']}",
        f"Report index ID: {data['report_index_id']}",
        f"Batch ID: {data['batch_id']}",
        f"Registry ID: {data['registry_id']}",
        f"Aggregate ID: {data['aggregate_id']}",
        f"Strategy index ID: {data['strategy_index_id']}",
        f"Failure taxonomy report ID: {data['failure_taxonomy_report_id']}",
        f"Selected strategy: {data['selected_strategy_name']}",
        f"Submission mode: {data['submission_mode']}",
        f"Task count: {data['task_count']}",
        f"Eligible task count: {data['eligible_task_count']}",
        f"Blocked task count: {data['blocked_task_count']}",
        f"Remediation required count: {data['remediation_required_count']}",
        f"Ready for public readiness audit: {str(data['ready_for_public_readiness_audit']).lower()}",
        f"Ready for Kaggle submission: {str(data['ready_for_kaggle_submission']).lower()}",
        f"Kaggle submission sent: {str(data['kaggle_submission_sent']).lower()}",
        "",
        "## Candidate tasks",
        "",
    ]

    for task in data.get("local_candidate_tasks", []):
        lines.extend(
            [
                f"### {task['task_id']}",
                "",
                f"- Sample ID: {task['sample_id']}",
                f"- Sample name: {task['sample_name']}",
                f"- Outcome status: {task['outcome_status']}",
                f"- Failure class: {task['failure_class']}",
                f"- Severity: {task['severity']}",
                f"- Eligible for submission: {str(task['eligible_for_submission']).lower()}",
                f"- Local output status: {task['local_output_status']}",
                f"- Local prediction ref: {task['local_prediction_ref']}",
                f"- Remediation required: {str(task['remediation_required']).lower()}",
                f"- Signature: {task['signature']}",
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
            f"Candidate signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_local_submission_candidate_package(
    package: LocalSubmissionCandidatePackage | Dict[str, Any],
) -> Dict[str, Any]:
    """Validate Local Submission Candidate Builder v1 public contract."""

    data = package.to_dict() if isinstance(package, LocalSubmissionCandidatePackage) else dict(package)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    tasks = data.get("local_candidate_tasks") if isinstance(data.get("local_candidate_tasks"), list) else []
    payload = data.get("local_submission_payload") if isinstance(data.get("local_submission_payload"), dict) else {}

    task_checks = []
    for task in tasks:
        task_metadata = task.get("metadata") if isinstance(task.get("metadata"), dict) else {}
        task_checks.append(
            task.get("status") == "LOCAL_SUBMISSION_CANDIDATE_TASK_READY"
            and isinstance(task.get("task_id"), str)
            and isinstance(task.get("sample_id"), str)
            and isinstance(task.get("sample_name"), str)
            and task.get("outcome_status")
            in {"OUTCOME_MATCH", "OUTCOME_PARTIAL", "OUTCOME_FAIL", "OUTCOME_UNVERIFIED"}
            and isinstance(task.get("failure_class"), str)
            and task.get("severity") in {"NONE", "LOW", "MEDIUM", "HIGH"}
            and isinstance(task.get("eligible_for_submission"), bool)
            and isinstance(task.get("local_output_status"), str)
            and isinstance(task.get("local_prediction_ref"), str)
            and isinstance(task.get("remediation_required"), bool)
            and isinstance(task.get("signature"), str)
            and task_metadata.get("public_safe") is True
            and task_metadata.get("deterministic") is True
            and task_metadata.get("local_only") is True
            and task_metadata.get("dry_run_only") is True
            and task_metadata.get("external_api_dependency") is False
            and task_metadata.get("executes_dataset_code") is False
            and task_metadata.get("contains_api_keys") is False
            and task_metadata.get("kaggle_submission_sent") is False
            and task_metadata.get("private_core_exposure") is False
        )

    eligible_task_count = data.get("eligible_task_count")
    blocked_task_count = data.get("blocked_task_count")
    remediation_required_count = data.get("remediation_required_count")
    task_count = data.get("task_count")

    checks = {
        "status_ready": data.get("status") == "LOCAL_SUBMISSION_CANDIDATE_BUILDER_READY",
        "candidate_status_valid": data.get("candidate_status") == "LOCAL_SUBMISSION_CANDIDATE_VALID",
        "candidate_id_present": bool(data.get("candidate_id")),
        "report_index_id_present": bool(data.get("report_index_id")),
        "batch_id_present": bool(data.get("batch_id")),
        "registry_id_present": bool(data.get("registry_id")),
        "aggregate_id_present": bool(data.get("aggregate_id")),
        "strategy_index_id_present": bool(data.get("strategy_index_id")),
        "failure_taxonomy_report_id_present": bool(data.get("failure_taxonomy_report_id")),
        "selected_strategy_present": bool(data.get("selected_strategy_id"))
        and bool(data.get("selected_strategy_name")),
        "submission_mode_local": data.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "task_count_positive": isinstance(task_count, int) and task_count > 0,
        "task_count_matches": task_count == len(tasks),
        "eligible_blocked_sum_matches": isinstance(eligible_task_count, int)
        and isinstance(blocked_task_count, int)
        and isinstance(task_count, int)
        and eligible_task_count + blocked_task_count == task_count,
        "remediation_required_count_valid": isinstance(remediation_required_count, int)
        and remediation_required_count == blocked_task_count,
        "ready_for_public_readiness_audit_true": data.get("ready_for_public_readiness_audit") is True,
        "ready_for_kaggle_submission_false": data.get("ready_for_kaggle_submission") is False,
        "kaggle_submission_sent_false": data.get("kaggle_submission_sent") is False,
        "local_submission_payload_present": payload.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "payload_kaggle_submission_sent_false": payload.get("kaggle_submission_sent") is False,
        "payload_ready_for_kaggle_submission_false": payload.get("ready_for_kaggle_submission") is False,
        "candidate_task_ids_list": isinstance(data.get("candidate_task_ids"), list),
        "candidate_task_signatures_dict": isinstance(data.get("candidate_task_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_tasks_valid": bool(task_checks) and all(task_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "metadata_local_only": metadata.get("local_only") is True,
        "metadata_dry_run_only": metadata.get("dry_run_only") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_report_index_generator": metadata.get("uses_report_index_generator") is True,
        "uses_failure_taxonomy": metadata.get("uses_failure_taxonomy") is True,
        "uses_strategy_selection_index": metadata.get("uses_strategy_selection_index") is True,
        "uses_multi_task_outcome_aggregator": metadata.get("uses_multi_task_outcome_aggregator") is True,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "LOCAL_SUBMISSION_CANDIDATE_VALID"
        if valid
        else "LOCAL_SUBMISSION_CANDIDATE_INVALID",
        "valid": valid,
        "checks": checks,
        "candidate_id": data.get("candidate_id"),
        "task_count": data.get("task_count"),
        "eligible_task_count": data.get("eligible_task_count"),
        "blocked_task_count": data.get("blocked_task_count"),
        "remediation_required_count": data.get("remediation_required_count"),
        "selected_strategy_id": data.get("selected_strategy_id"),
        "submission_mode": data.get("submission_mode"),
        "ready_for_public_readiness_audit": data.get("ready_for_public_readiness_audit"),
        "ready_for_kaggle_submission": data.get("ready_for_kaggle_submission"),
        "kaggle_submission_sent": data.get("kaggle_submission_sent"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "local_submission_candidate_builder_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_local_submission_candidate_package() -> Dict[str, Any]:
    package = build_local_submission_candidate_package()
    validation = validate_local_submission_candidate_package(package)

    return {
        "status": "LOCAL_SUBMISSION_CANDIDATE_PIPELINE_READY",
        "local_submission_candidate": package.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "local_submission_candidate_builder_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_report_index_generator": True,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_local_submission_candidate_artifacts(
    package: LocalSubmissionCandidatePackage | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/local-submission-candidate-builder",
) -> Dict[str, str]:
    data = package.to_dict() if isinstance(package, LocalSubmissionCandidatePackage) else dict(package)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "local-submission-candidate.json"
    markdown_path = output_path / "local-submission-candidate.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_local_submission_candidate_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
