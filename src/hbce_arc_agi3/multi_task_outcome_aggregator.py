"""Multi-Task Outcome Aggregator v1 for HBCE ARC-AGI-3 public baseline.

This module aggregates public batch benchmark task records into a deterministic
multi-task outcome summary.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
"""

from __future__ import annotations

import copy
import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.batch_benchmark_runner import (
    BatchBenchmarkRun,
    run_batch_benchmark,
    validate_batch_benchmark_run,
)


@dataclass(frozen=True)
class MultiTaskOutcomeRecord:
    status: str
    task_id: str
    sample_id: str
    sample_name: str
    exact_match: bool
    verified: bool
    cell_accuracy: float
    mismatch_count: int
    outcome_status: str
    quality_band: str
    calibrated_score: float
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class MultiTaskOutcomeAggregate:
    status: str
    aggregate_status: str
    aggregate_id: str
    batch_id: str
    registry_id: str
    task_count: int
    matched_count: int
    partial_count: int
    failed_count: int
    unverified_count: int
    average_cell_accuracy: float
    average_calibrated_score: float
    exact_match_rate: float
    aggregate_quality_band: str
    aggregate_verdict: str
    outcome_records: List[Dict[str, Any]]
    outcome_ids: List[str]
    outcome_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _quality_band(score: float) -> str:
    if score >= 1.0:
        return "PERFECT"
    if score >= 0.9:
        return "STRONG"
    if score >= 0.75:
        return "GOOD"
    if score >= 0.5:
        return "PARTIAL"
    return "WEAK"


def _aggregate_verdict(quality_band: str, *, failed_count: int, unverified_count: int) -> str:
    if unverified_count > 0:
        return "OUTCOME_AGGREGATE_UNVERIFIED"
    if failed_count > 0 and quality_band in {"WEAK", "PARTIAL"}:
        return "OUTCOME_AGGREGATE_NEEDS_REVIEW"
    if quality_band in {"PERFECT", "STRONG"}:
        return "OUTCOME_AGGREGATE_STRONG"
    if quality_band == "GOOD":
        return "OUTCOME_AGGREGATE_GOOD"
    return "OUTCOME_AGGREGATE_PARTIAL"


def _outcome_status(record: Dict[str, Any]) -> str:
    if record.get("verified") is not True:
        return "OUTCOME_UNVERIFIED"
    if record.get("exact_match") is True:
        return "OUTCOME_MATCH"

    cell_accuracy = record.get("cell_accuracy")
    if isinstance(cell_accuracy, (int, float)) and float(cell_accuracy) > 0:
        return "OUTCOME_PARTIAL"

    return "OUTCOME_FAIL"


def build_multi_task_outcome_record(task_record: Dict[str, Any]) -> MultiTaskOutcomeRecord:
    """Build one deterministic outcome record from a batch task record."""

    if not isinstance(task_record, dict):
        raise ValueError("Outcome aggregator task record must be a dictionary")

    task_id = str(task_record.get("task_id") or "").strip()
    sample_id = str(task_record.get("sample_id") or "").strip()
    sample_name = str(task_record.get("sample_name") or "").strip()

    if not task_id:
        raise ValueError("Outcome aggregator task record requires task_id")
    if not sample_id:
        raise ValueError("Outcome aggregator task record requires sample_id")
    if not sample_name:
        raise ValueError("Outcome aggregator task record requires sample_name")

    cell_accuracy_raw = task_record.get("cell_accuracy")
    mismatch_count_raw = task_record.get("mismatch_count")

    if not isinstance(cell_accuracy_raw, (int, float)):
        raise ValueError("Outcome aggregator task record requires numeric cell_accuracy")
    if not isinstance(mismatch_count_raw, int):
        raise ValueError("Outcome aggregator task record requires integer mismatch_count")

    cell_accuracy = round(float(cell_accuracy_raw), 6)
    mismatch_count = int(mismatch_count_raw)
    exact_match = task_record.get("exact_match") is True
    verified = task_record.get("verified") is True
    outcome_status = _outcome_status(task_record)
    quality_band = _quality_band(cell_accuracy)
    calibrated_score = cell_accuracy

    signature_basis = {
        "task_id": task_id,
        "sample_id": sample_id,
        "sample_name": sample_name,
        "exact_match": exact_match,
        "verified": verified,
        "cell_accuracy": cell_accuracy,
        "mismatch_count": mismatch_count,
        "outcome_status": outcome_status,
        "quality_band": quality_band,
        "calibrated_score": calibrated_score,
    }
    signature = _stable_signature(signature_basis)

    return MultiTaskOutcomeRecord(
        status="MULTI_TASK_OUTCOME_RECORD_READY",
        task_id=task_id,
        sample_id=sample_id,
        sample_name=sample_name,
        exact_match=exact_match,
        verified=verified,
        cell_accuracy=cell_accuracy,
        mismatch_count=mismatch_count,
        outcome_status=outcome_status,
        quality_band=quality_band,
        calibrated_score=calibrated_score,
        signature=signature,
        metadata={
            "source": "multi_task_outcome_aggregator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    )


def _coerce_batch_run(batch_run: Optional[BatchBenchmarkRun | Dict[str, Any]]) -> Dict[str, Any]:
    if batch_run is None:
        return run_batch_benchmark().to_dict()

    if isinstance(batch_run, BatchBenchmarkRun):
        return batch_run.to_dict()

    if isinstance(batch_run, dict):
        return copy.deepcopy(batch_run)

    raise ValueError("Multi-task outcome aggregator requires a BatchBenchmarkRun or dictionary")


def aggregate_multi_task_outcomes(
    batch_run: Optional[BatchBenchmarkRun | Dict[str, Any]] = None,
) -> MultiTaskOutcomeAggregate:
    """Aggregate deterministic public batch benchmark outcomes."""

    batch_data = _coerce_batch_run(batch_run)
    batch_validation = validate_batch_benchmark_run(batch_data)

    if batch_validation["status"] != "BATCH_BENCHMARK_RUN_VALID":
        raise ValueError("Multi-task outcome aggregator requires a valid BATCH_BENCHMARK_RUN_VALID payload")

    task_records = batch_data.get("task_records")
    if not isinstance(task_records, list) or not task_records:
        raise ValueError("Multi-task outcome aggregator requires non-empty task_records")

    outcome_records = [build_multi_task_outcome_record(record) for record in task_records]
    outcome_records_sorted = sorted(outcome_records, key=lambda item: item.task_id)
    outcome_dicts = [record.to_dict() for record in outcome_records_sorted]

    task_count = len(outcome_records_sorted)
    matched_count = sum(1 for record in outcome_records_sorted if record.outcome_status == "OUTCOME_MATCH")
    partial_count = sum(1 for record in outcome_records_sorted if record.outcome_status == "OUTCOME_PARTIAL")
    failed_count = sum(1 for record in outcome_records_sorted if record.outcome_status == "OUTCOME_FAIL")
    unverified_count = sum(1 for record in outcome_records_sorted if record.outcome_status == "OUTCOME_UNVERIFIED")

    average_cell_accuracy = (
        round(sum(record.cell_accuracy for record in outcome_records_sorted) / task_count, 6)
        if task_count
        else 0.0
    )
    average_calibrated_score = (
        round(sum(record.calibrated_score for record in outcome_records_sorted) / task_count, 6)
        if task_count
        else 0.0
    )
    exact_match_rate = round(matched_count / task_count, 6) if task_count else 0.0
    aggregate_quality_band = _quality_band(average_calibrated_score)
    aggregate_verdict = _aggregate_verdict(
        aggregate_quality_band,
        failed_count=failed_count,
        unverified_count=unverified_count,
    )

    outcome_ids = [record.task_id for record in outcome_records_sorted]
    outcome_signatures = {record.task_id: record.signature for record in outcome_records_sorted}

    signature_basis = {
        "batch_id": batch_data.get("batch_id"),
        "registry_id": batch_data.get("registry_id"),
        "task_count": task_count,
        "matched_count": matched_count,
        "partial_count": partial_count,
        "failed_count": failed_count,
        "unverified_count": unverified_count,
        "average_cell_accuracy": average_cell_accuracy,
        "average_calibrated_score": average_calibrated_score,
        "exact_match_rate": exact_match_rate,
        "aggregate_quality_band": aggregate_quality_band,
        "aggregate_verdict": aggregate_verdict,
        "outcome_ids": outcome_ids,
        "outcome_signatures": outcome_signatures,
    }
    signature = _stable_signature(signature_basis)
    aggregate_id = f"MULTI-TASK-OUTCOME-{signature[:12]}"

    return MultiTaskOutcomeAggregate(
        status="MULTI_TASK_OUTCOME_AGGREGATOR_READY",
        aggregate_status="MULTI_TASK_OUTCOME_AGGREGATE_VALID",
        aggregate_id=aggregate_id,
        batch_id=str(batch_data.get("batch_id")),
        registry_id=str(batch_data.get("registry_id")),
        task_count=task_count,
        matched_count=matched_count,
        partial_count=partial_count,
        failed_count=failed_count,
        unverified_count=unverified_count,
        average_cell_accuracy=average_cell_accuracy,
        average_calibrated_score=average_calibrated_score,
        exact_match_rate=exact_match_rate,
        aggregate_quality_band=aggregate_quality_band,
        aggregate_verdict=aggregate_verdict,
        outcome_records=outcome_dicts,
        outcome_ids=outcome_ids,
        outcome_signatures=outcome_signatures,
        signature=signature,
        metadata={
            "source": "multi_task_outcome_aggregator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 3",
        },
    )


def render_multi_task_outcome_markdown(
    aggregate: MultiTaskOutcomeAggregate | Dict[str, Any],
) -> str:
    data = aggregate.to_dict() if isinstance(aggregate, MultiTaskOutcomeAggregate) else dict(aggregate)

    lines = [
        "# ARC-AGI-3 Multi-Task Outcome Aggregator v1",
        "",
        f"Status: {data['status']}",
        f"Aggregate status: {data['aggregate_status']}",
        f"Aggregate ID: {data['aggregate_id']}",
        f"Batch ID: {data['batch_id']}",
        f"Registry ID: {data['registry_id']}",
        f"Task count: {data['task_count']}",
        f"Matched count: {data['matched_count']}",
        f"Partial count: {data['partial_count']}",
        f"Failed count: {data['failed_count']}",
        f"Unverified count: {data['unverified_count']}",
        f"Average cell accuracy: {data['average_cell_accuracy']}",
        f"Average calibrated score: {data['average_calibrated_score']}",
        f"Exact match rate: {data['exact_match_rate']}",
        f"Aggregate quality band: {data['aggregate_quality_band']}",
        f"Aggregate verdict: {data['aggregate_verdict']}",
        "",
        "## Outcome records",
        "",
    ]

    for record in data.get("outcome_records", []):
        lines.extend(
            [
                f"### {record['task_id']}",
                "",
                f"- Sample ID: {record['sample_id']}",
                f"- Sample name: {record['sample_name']}",
                f"- Outcome status: {record['outcome_status']}",
                f"- Quality band: {record['quality_band']}",
                f"- Cell accuracy: {record['cell_accuracy']}",
                f"- Calibrated score: {record['calibrated_score']}",
                f"- Signature: {record['signature']}",
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
            f"Aggregate signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_multi_task_outcome_aggregate(
    aggregate: MultiTaskOutcomeAggregate | Dict[str, Any],
) -> Dict[str, Any]:
    """Validate Multi-Task Outcome Aggregator v1 public contract."""

    data = aggregate.to_dict() if isinstance(aggregate, MultiTaskOutcomeAggregate) else dict(aggregate)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    outcome_records = data.get("outcome_records") if isinstance(data.get("outcome_records"), list) else []

    task_count_value = data.get("task_count")
    matched_count_value = data.get("matched_count")
    partial_count_value = data.get("partial_count")
    failed_count_value = data.get("failed_count")
    unverified_count_value = data.get("unverified_count")

    count_sum_matches = (
        isinstance(task_count_value, int)
        and isinstance(matched_count_value, int)
        and isinstance(partial_count_value, int)
        and isinstance(failed_count_value, int)
        and isinstance(unverified_count_value, int)
        and task_count_value
        == matched_count_value + partial_count_value + failed_count_value + unverified_count_value
    )

    record_checks = []
    for record in outcome_records:
        record_metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
        record_checks.append(
            record.get("status") == "MULTI_TASK_OUTCOME_RECORD_READY"
            and isinstance(record.get("task_id"), str)
            and isinstance(record.get("sample_id"), str)
            and record.get("outcome_status")
            in {"OUTCOME_MATCH", "OUTCOME_PARTIAL", "OUTCOME_FAIL", "OUTCOME_UNVERIFIED"}
            and record.get("quality_band") in {"PERFECT", "STRONG", "GOOD", "PARTIAL", "WEAK"}
            and isinstance(record.get("cell_accuracy"), float)
            and isinstance(record.get("calibrated_score"), float)
            and isinstance(record.get("mismatch_count"), int)
            and isinstance(record.get("signature"), str)
            and record_metadata.get("public_safe") is True
            and record_metadata.get("deterministic") is True
            and record_metadata.get("external_api_dependency") is False
            and record_metadata.get("executes_dataset_code") is False
            and record_metadata.get("contains_api_keys") is False
        )

    checks = {
        "status_ready": data.get("status") == "MULTI_TASK_OUTCOME_AGGREGATOR_READY",
        "aggregate_status_valid": data.get("aggregate_status") == "MULTI_TASK_OUTCOME_AGGREGATE_VALID",
        "aggregate_id_present": bool(data.get("aggregate_id")),
        "batch_id_present": bool(data.get("batch_id")),
        "registry_id_present": bool(data.get("registry_id")),
        "task_count_positive": isinstance(task_count_value, int) and task_count_value > 0,
        "task_count_matches_records": task_count_value == len(outcome_records),
        "count_sum_matches": count_sum_matches,
        "average_cell_accuracy_number": isinstance(data.get("average_cell_accuracy"), float),
        "average_calibrated_score_number": isinstance(data.get("average_calibrated_score"), float),
        "exact_match_rate_number": isinstance(data.get("exact_match_rate"), float),
        "aggregate_quality_band_valid": data.get("aggregate_quality_band")
        in {"PERFECT", "STRONG", "GOOD", "PARTIAL", "WEAK"},
        "aggregate_verdict_present": isinstance(data.get("aggregate_verdict"), str)
        and bool(data.get("aggregate_verdict")),
        "outcome_ids_list": isinstance(data.get("outcome_ids"), list),
        "outcome_signatures_dict": isinstance(data.get("outcome_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_outcome_records_valid": bool(record_checks) and all(record_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "MULTI_TASK_OUTCOME_AGGREGATE_VALID"
        if valid
        else "MULTI_TASK_OUTCOME_AGGREGATE_INVALID",
        "valid": valid,
        "checks": checks,
        "aggregate_id": data.get("aggregate_id"),
        "batch_id": data.get("batch_id"),
        "registry_id": data.get("registry_id"),
        "task_count": data.get("task_count"),
        "matched_count": data.get("matched_count"),
        "partial_count": data.get("partial_count"),
        "failed_count": data.get("failed_count"),
        "unverified_count": data.get("unverified_count"),
        "average_calibrated_score": data.get("average_calibrated_score"),
        "aggregate_quality_band": data.get("aggregate_quality_band"),
        "aggregate_verdict": data.get("aggregate_verdict"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "multi_task_outcome_aggregator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_multi_task_outcome_aggregate(
    batch_run: Optional[BatchBenchmarkRun | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    aggregate = aggregate_multi_task_outcomes(batch_run)
    validation = validate_multi_task_outcome_aggregate(aggregate)

    return {
        "status": "MULTI_TASK_OUTCOME_AGGREGATOR_PIPELINE_READY",
        "multi_task_outcome_aggregate": aggregate.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "multi_task_outcome_aggregator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_multi_task_outcome_artifacts(
    aggregate: MultiTaskOutcomeAggregate | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/multi-task-outcome-aggregator",
) -> Dict[str, str]:
    data = aggregate.to_dict() if isinstance(aggregate, MultiTaskOutcomeAggregate) else dict(aggregate)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "multi-task-outcome-aggregate.json"
    markdown_path = output_path / "multi-task-outcome-aggregate.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_multi_task_outcome_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
