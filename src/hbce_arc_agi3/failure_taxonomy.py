"""Failure Taxonomy v1 for HBCE ARC-AGI-3 public baseline.

This module classifies deterministic public benchmark outcomes into a stable
failure taxonomy.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
It does not expose private HBCE/JOKER-C2 strategy logic.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.multi_task_outcome_aggregator import (
    MultiTaskOutcomeAggregate,
    aggregate_multi_task_outcomes,
    validate_multi_task_outcome_aggregate,
)
from hbce_arc_agi3.strategy_selection_index import (
    StrategySelectionIndex,
    build_strategy_selection_index,
    validate_strategy_selection_index,
)


@dataclass(frozen=True)
class FailureTaxonomyEntry:
    status: str
    taxonomy_id: str
    task_id: str
    sample_id: str
    sample_name: str
    outcome_status: str
    exact_match: bool
    cell_accuracy: float
    mismatch_count: int
    failure_class: str
    severity: str
    is_failure: bool
    is_partial: bool
    remediation_hint: str
    evidence: Dict[str, Any]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FailureTaxonomyReport:
    status: str
    taxonomy_status: str
    taxonomy_report_id: str
    index_id: str
    aggregate_id: str
    batch_id: str
    registry_id: str
    selected_strategy_id: str
    selected_strategy_name: str
    total_outcomes: int
    exact_match_count: int
    partial_count: int
    failure_count: int
    unverified_count: int
    taxonomy_entry_count: int
    primary_failure_class: str
    severity_band: str
    taxonomy_entries: List[Dict[str, Any]]
    taxonomy_ids: List[str]
    taxonomy_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_aggregate(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]],
) -> Dict[str, Any]:
    if aggregate is None:
        return aggregate_multi_task_outcomes().to_dict()

    if isinstance(aggregate, MultiTaskOutcomeAggregate):
        return aggregate.to_dict()

    if isinstance(aggregate, dict):
        return copy.deepcopy(aggregate)

    raise ValueError("Failure taxonomy requires a MultiTaskOutcomeAggregate or dictionary")


def _coerce_strategy_index(
    strategy_index: Optional[StrategySelectionIndex | Dict[str, Any]],
    aggregate_data: Dict[str, Any],
) -> Dict[str, Any]:
    if strategy_index is None:
        return build_strategy_selection_index(aggregate_data).to_dict()

    if isinstance(strategy_index, StrategySelectionIndex):
        return strategy_index.to_dict()

    if isinstance(strategy_index, dict):
        return copy.deepcopy(strategy_index)

    raise ValueError("Failure taxonomy requires a StrategySelectionIndex or dictionary")


def _classify_failure(record: Dict[str, Any]) -> Dict[str, str | bool]:
    outcome_status = str(record.get("outcome_status") or "")
    exact_match = record.get("exact_match") is True
    cell_accuracy = float(record.get("cell_accuracy") or 0.0)
    mismatch_count = int(record.get("mismatch_count") or 0)

    if outcome_status == "OUTCOME_UNVERIFIED":
        return {
            "failure_class": "UNVERIFIED_OUTCOME",
            "severity": "HIGH",
            "is_failure": True,
            "is_partial": False,
            "remediation_hint": "Re-run verification before using this outcome for ranking.",
        }

    if exact_match and outcome_status == "OUTCOME_MATCH":
        return {
            "failure_class": "NO_FAILURE_EXACT_MATCH",
            "severity": "NONE",
            "is_failure": False,
            "is_partial": False,
            "remediation_hint": "No remediation required for exact public benchmark match.",
        }

    if outcome_status == "OUTCOME_PARTIAL" or (0.0 < cell_accuracy < 1.0):
        severity = "LOW" if cell_accuracy >= 0.75 and mismatch_count <= 1 else "MEDIUM"
        return {
            "failure_class": "PARTIAL_TRANSFORM_REFERENCE_MISMATCH",
            "severity": severity,
            "is_failure": False,
            "is_partial": True,
            "remediation_hint": "Inspect transformation reference and add targeted repair strategy before release candidate selection.",
        }

    if outcome_status == "OUTCOME_FAIL" or cell_accuracy <= 0.0:
        return {
            "failure_class": "HARD_FAILURE_ZERO_OR_INVALID_ACCURACY",
            "severity": "HIGH",
            "is_failure": True,
            "is_partial": False,
            "remediation_hint": "Block release candidate until task-level prediction path is repaired.",
        }

    return {
        "failure_class": "UNKNOWN_OUTCOME_CLASS",
        "severity": "MEDIUM",
        "is_failure": True,
        "is_partial": False,
        "remediation_hint": "Inspect outcome payload contract and normalize status mapping.",
    }


def _severity_rank(severity: str) -> int:
    return {
        "NONE": 0,
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
    }.get(severity, 2)


def _severity_band(entries: List[FailureTaxonomyEntry]) -> str:
    if not entries:
        return "NONE"

    highest = max(_severity_rank(entry.severity) for entry in entries)
    if highest >= 3:
        return "HIGH"
    if highest == 2:
        return "MEDIUM"
    if highest == 1:
        return "LOW"
    return "NONE"


def _primary_failure_class(entries: List[FailureTaxonomyEntry]) -> str:
    non_exact = [
        entry.failure_class
        for entry in entries
        if entry.failure_class != "NO_FAILURE_EXACT_MATCH"
    ]

    if not non_exact:
        return "NO_FAILURE_EXACT_MATCH"

    counts: Dict[str, int] = {}
    for item in non_exact:
        counts[item] = counts.get(item, 0) + 1

    return sorted(counts.items(), key=lambda pair: (-pair[1], pair[0]))[0][0]


def build_failure_taxonomy_entry(record: Dict[str, Any]) -> FailureTaxonomyEntry:
    """Build one deterministic failure taxonomy entry from an outcome record."""

    if not isinstance(record, dict):
        raise ValueError("Failure taxonomy record must be a dictionary")

    task_id = str(record.get("task_id") or "").strip()
    sample_id = str(record.get("sample_id") or "").strip()
    sample_name = str(record.get("sample_name") or "").strip()
    outcome_status = str(record.get("outcome_status") or "").strip()

    if not task_id:
        raise ValueError("Failure taxonomy record requires task_id")
    if not sample_id:
        raise ValueError("Failure taxonomy record requires sample_id")
    if not sample_name:
        raise ValueError("Failure taxonomy record requires sample_name")
    if not outcome_status:
        raise ValueError("Failure taxonomy record requires outcome_status")

    cell_accuracy_raw = record.get("cell_accuracy")
    mismatch_count_raw = record.get("mismatch_count")

    if not isinstance(cell_accuracy_raw, (int, float)):
        raise ValueError("Failure taxonomy record requires numeric cell_accuracy")
    if not isinstance(mismatch_count_raw, int):
        raise ValueError("Failure taxonomy record requires integer mismatch_count")

    exact_match = record.get("exact_match") is True
    cell_accuracy = round(float(cell_accuracy_raw), 6)
    mismatch_count = int(mismatch_count_raw)
    classification = _classify_failure(record)

    taxonomy_basis = {
        "task_id": task_id,
        "sample_id": sample_id,
        "outcome_status": outcome_status,
        "exact_match": exact_match,
        "cell_accuracy": cell_accuracy,
        "mismatch_count": mismatch_count,
        "failure_class": classification["failure_class"],
        "severity": classification["severity"],
    }
    signature = _stable_signature(taxonomy_basis)
    taxonomy_id = f"FAILURE-TAXONOMY-{signature[:12]}"

    return FailureTaxonomyEntry(
        status="FAILURE_TAXONOMY_ENTRY_READY",
        taxonomy_id=taxonomy_id,
        task_id=task_id,
        sample_id=sample_id,
        sample_name=sample_name,
        outcome_status=outcome_status,
        exact_match=exact_match,
        cell_accuracy=cell_accuracy,
        mismatch_count=mismatch_count,
        failure_class=str(classification["failure_class"]),
        severity=str(classification["severity"]),
        is_failure=bool(classification["is_failure"]),
        is_partial=bool(classification["is_partial"]),
        remediation_hint=str(classification["remediation_hint"]),
        evidence={
            "task_id": task_id,
            "sample_id": sample_id,
            "sample_name": sample_name,
            "outcome_status": outcome_status,
            "exact_match": exact_match,
            "cell_accuracy": cell_accuracy,
            "mismatch_count": mismatch_count,
            "source_signature": record.get("signature"),
        },
        signature=signature,
        metadata={
            "source": "failure_taxonomy_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    )


def build_failure_taxonomy_report(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]] = None,
    strategy_index: Optional[StrategySelectionIndex | Dict[str, Any]] = None,
) -> FailureTaxonomyReport:
    """Build deterministic public failure taxonomy report."""

    aggregate_data = _coerce_aggregate(aggregate)
    aggregate_validation = validate_multi_task_outcome_aggregate(aggregate_data)

    if aggregate_validation["status"] != "MULTI_TASK_OUTCOME_AGGREGATE_VALID":
        raise ValueError("Failure taxonomy requires a valid MULTI_TASK_OUTCOME_AGGREGATE_VALID payload")

    index_data = _coerce_strategy_index(strategy_index, aggregate_data)
    index_validation = validate_strategy_selection_index(index_data)

    if index_validation["status"] != "STRATEGY_SELECTION_INDEX_VALID":
        raise ValueError("Failure taxonomy requires a valid STRATEGY_SELECTION_INDEX_VALID payload")

    outcome_records = aggregate_data.get("outcome_records")
    if not isinstance(outcome_records, list) or not outcome_records:
        raise ValueError("Failure taxonomy requires non-empty outcome_records")

    entries = [build_failure_taxonomy_entry(record) for record in outcome_records]
    entries_sorted = sorted(entries, key=lambda item: item.taxonomy_id)
    entry_dicts = [entry.to_dict() for entry in entries_sorted]

    exact_match_count = sum(1 for entry in entries_sorted if entry.failure_class == "NO_FAILURE_EXACT_MATCH")
    partial_count = sum(1 for entry in entries_sorted if entry.is_partial)
    failure_count = sum(1 for entry in entries_sorted if entry.is_failure)
    unverified_count = sum(1 for entry in entries_sorted if entry.failure_class == "UNVERIFIED_OUTCOME")

    taxonomy_ids = [entry.taxonomy_id for entry in entries_sorted]
    taxonomy_signatures = {entry.taxonomy_id: entry.signature for entry in entries_sorted}
    primary_failure_class = _primary_failure_class(entries_sorted)
    severity_band = _severity_band(entries_sorted)

    signature_basis = {
        "index_id": index_data.get("index_id"),
        "aggregate_id": aggregate_data.get("aggregate_id"),
        "batch_id": aggregate_data.get("batch_id"),
        "registry_id": aggregate_data.get("registry_id"),
        "selected_strategy_id": index_data.get("selected_strategy_id"),
        "taxonomy_ids": taxonomy_ids,
        "taxonomy_signatures": taxonomy_signatures,
        "exact_match_count": exact_match_count,
        "partial_count": partial_count,
        "failure_count": failure_count,
        "unverified_count": unverified_count,
        "primary_failure_class": primary_failure_class,
        "severity_band": severity_band,
    }
    signature = _stable_signature(signature_basis)
    taxonomy_report_id = f"FAILURE-TAXONOMY-REPORT-{signature[:12]}"

    return FailureTaxonomyReport(
        status="FAILURE_TAXONOMY_READY",
        taxonomy_status="FAILURE_TAXONOMY_VALID",
        taxonomy_report_id=taxonomy_report_id,
        index_id=str(index_data.get("index_id")),
        aggregate_id=str(aggregate_data.get("aggregate_id")),
        batch_id=str(aggregate_data.get("batch_id")),
        registry_id=str(aggregate_data.get("registry_id")),
        selected_strategy_id=str(index_data.get("selected_strategy_id")),
        selected_strategy_name=str(index_data.get("selected_strategy_name")),
        total_outcomes=len(entries_sorted),
        exact_match_count=exact_match_count,
        partial_count=partial_count,
        failure_count=failure_count,
        unverified_count=unverified_count,
        taxonomy_entry_count=len(entries_sorted),
        primary_failure_class=primary_failure_class,
        severity_band=severity_band,
        taxonomy_entries=entry_dicts,
        taxonomy_ids=taxonomy_ids,
        taxonomy_signatures=taxonomy_signatures,
        signature=signature,
        metadata={
            "source": "failure_taxonomy_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 5",
        },
    )


def render_failure_taxonomy_markdown(report: FailureTaxonomyReport | Dict[str, Any]) -> str:
    data = report.to_dict() if isinstance(report, FailureTaxonomyReport) else dict(report)

    lines = [
        "# ARC-AGI-3 Failure Taxonomy v1",
        "",
        f"Status: {data['status']}",
        f"Taxonomy status: {data['taxonomy_status']}",
        f"Taxonomy report ID: {data['taxonomy_report_id']}",
        f"Strategy index ID: {data['index_id']}",
        f"Aggregate ID: {data['aggregate_id']}",
        f"Batch ID: {data['batch_id']}",
        f"Registry ID: {data['registry_id']}",
        f"Selected strategy: {data['selected_strategy_name']}",
        f"Total outcomes: {data['total_outcomes']}",
        f"Exact match count: {data['exact_match_count']}",
        f"Partial count: {data['partial_count']}",
        f"Failure count: {data['failure_count']}",
        f"Unverified count: {data['unverified_count']}",
        f"Primary failure class: {data['primary_failure_class']}",
        f"Severity band: {data['severity_band']}",
        "",
        "## Taxonomy entries",
        "",
    ]

    for entry in data.get("taxonomy_entries", []):
        lines.extend(
            [
                f"### {entry['taxonomy_id']}",
                "",
                f"- Task ID: {entry['task_id']}",
                f"- Sample ID: {entry['sample_id']}",
                f"- Sample name: {entry['sample_name']}",
                f"- Outcome status: {entry['outcome_status']}",
                f"- Failure class: {entry['failure_class']}",
                f"- Severity: {entry['severity']}",
                f"- Partial: {str(entry['is_partial']).lower()}",
                f"- Failure: {str(entry['is_failure']).lower()}",
                f"- Remediation hint: {entry['remediation_hint']}",
                f"- Signature: {entry['signature']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- external_api_dependency=false",
            "- executes_dataset_code=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "",
            f"Taxonomy signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_failure_taxonomy_report(report: FailureTaxonomyReport | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Failure Taxonomy v1 public contract."""

    data = report.to_dict() if isinstance(report, FailureTaxonomyReport) else dict(report)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    entries = data.get("taxonomy_entries") if isinstance(data.get("taxonomy_entries"), list) else []

    exact_match_count = data.get("exact_match_count")
    partial_count = data.get("partial_count")
    failure_count = data.get("failure_count")
    unverified_count = data.get("unverified_count")
    total_outcomes = data.get("total_outcomes")

    counts_are_ints = all(
        isinstance(value, int)
        for value in [
            exact_match_count,
            partial_count,
            failure_count,
            unverified_count,
            total_outcomes,
        ]
    )

    entry_checks = []
    for entry in entries:
        entry_metadata = entry.get("metadata") if isinstance(entry.get("metadata"), dict) else {}
        entry_checks.append(
            entry.get("status") == "FAILURE_TAXONOMY_ENTRY_READY"
            and isinstance(entry.get("taxonomy_id"), str)
            and isinstance(entry.get("task_id"), str)
            and isinstance(entry.get("sample_id"), str)
            and entry.get("outcome_status")
            in {"OUTCOME_MATCH", "OUTCOME_PARTIAL", "OUTCOME_FAIL", "OUTCOME_UNVERIFIED"}
            and entry.get("failure_class")
            in {
                "NO_FAILURE_EXACT_MATCH",
                "PARTIAL_TRANSFORM_REFERENCE_MISMATCH",
                "HARD_FAILURE_ZERO_OR_INVALID_ACCURACY",
                "UNVERIFIED_OUTCOME",
                "UNKNOWN_OUTCOME_CLASS",
            }
            and entry.get("severity") in {"NONE", "LOW", "MEDIUM", "HIGH"}
            and isinstance(entry.get("is_failure"), bool)
            and isinstance(entry.get("is_partial"), bool)
            and isinstance(entry.get("cell_accuracy"), float)
            and isinstance(entry.get("mismatch_count"), int)
            and isinstance(entry.get("remediation_hint"), str)
            and isinstance(entry.get("signature"), str)
            and entry_metadata.get("public_safe") is True
            and entry_metadata.get("deterministic") is True
            and entry_metadata.get("external_api_dependency") is False
            and entry_metadata.get("executes_dataset_code") is False
            and entry_metadata.get("contains_api_keys") is False
            and entry_metadata.get("private_core_exposure") is False
        )

    checks = {
        "status_ready": data.get("status") == "FAILURE_TAXONOMY_READY",
        "taxonomy_status_valid": data.get("taxonomy_status") == "FAILURE_TAXONOMY_VALID",
        "taxonomy_report_id_present": bool(data.get("taxonomy_report_id")),
        "index_id_present": bool(data.get("index_id")),
        "aggregate_id_present": bool(data.get("aggregate_id")),
        "batch_id_present": bool(data.get("batch_id")),
        "registry_id_present": bool(data.get("registry_id")),
        "selected_strategy_present": bool(data.get("selected_strategy_id"))
        and bool(data.get("selected_strategy_name")),
        "total_outcomes_positive": isinstance(total_outcomes, int) and total_outcomes > 0,
        "taxonomy_entry_count_matches": data.get("taxonomy_entry_count") == len(entries),
        "total_outcomes_matches_entries": total_outcomes == len(entries),
        "counts_are_ints": counts_are_ints,
        "primary_failure_class_present": isinstance(data.get("primary_failure_class"), str)
        and bool(data.get("primary_failure_class")),
        "severity_band_valid": data.get("severity_band") in {"NONE", "LOW", "MEDIUM", "HIGH"},
        "taxonomy_ids_list": isinstance(data.get("taxonomy_ids"), list),
        "taxonomy_signatures_dict": isinstance(data.get("taxonomy_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_entries_valid": bool(entry_checks) and all(entry_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_strategy_selection_index": metadata.get("uses_strategy_selection_index") is True,
        "uses_multi_task_outcome_aggregator": metadata.get("uses_multi_task_outcome_aggregator") is True,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "FAILURE_TAXONOMY_VALID" if valid else "FAILURE_TAXONOMY_INVALID",
        "valid": valid,
        "checks": checks,
        "taxonomy_report_id": data.get("taxonomy_report_id"),
        "index_id": data.get("index_id"),
        "aggregate_id": data.get("aggregate_id"),
        "batch_id": data.get("batch_id"),
        "registry_id": data.get("registry_id"),
        "total_outcomes": data.get("total_outcomes"),
        "exact_match_count": data.get("exact_match_count"),
        "partial_count": data.get("partial_count"),
        "failure_count": data.get("failure_count"),
        "unverified_count": data.get("unverified_count"),
        "primary_failure_class": data.get("primary_failure_class"),
        "severity_band": data.get("severity_band"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "failure_taxonomy_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_failure_taxonomy_report(
    aggregate: Optional[MultiTaskOutcomeAggregate | Dict[str, Any]] = None,
    strategy_index: Optional[StrategySelectionIndex | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    report = build_failure_taxonomy_report(aggregate, strategy_index)
    validation = validate_failure_taxonomy_report(report)

    return {
        "status": "FAILURE_TAXONOMY_PIPELINE_READY",
        "failure_taxonomy_report": report.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "failure_taxonomy_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_failure_taxonomy_artifacts(
    report: FailureTaxonomyReport | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/failure-taxonomy",
) -> Dict[str, str]:
    data = report.to_dict() if isinstance(report, FailureTaxonomyReport) else dict(report)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "failure-taxonomy-report.json"
    markdown_path = output_path / "failure-taxonomy-report.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_failure_taxonomy_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
