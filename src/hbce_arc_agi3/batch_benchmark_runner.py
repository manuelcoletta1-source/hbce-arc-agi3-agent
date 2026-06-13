"""Batch Benchmark Runner v1 for HBCE ARC-AGI-3 public baseline.

This module runs a deterministic public-safe batch benchmark over the
Dataset Sample Registry v1 records.

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
from typing import Any, Dict, Iterable, List, Optional

from hbce_arc_agi3.dataset_sample_registry import (
    DatasetSampleRegistry,
    generate_dataset_sample_registry,
    validate_dataset_sample_registry,
)


Grid = List[List[int]]


@dataclass(frozen=True)
class BatchBenchmarkTaskRecord:
    status: str
    task_id: str
    sample_id: str
    sample_name: str
    runner_strategy: str
    input_shape: List[int]
    expected_shape: List[int]
    predicted_shape: List[int]
    prediction: Grid
    expected_output: Grid
    exact_match: bool
    cell_accuracy: float
    mismatch_count: int
    verified: bool
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BatchBenchmarkRun:
    status: str
    batch_status: str
    batch_id: str
    registry_id: str
    runner_strategy: str
    task_count: int
    matched_count: int
    mismatched_count: int
    verified_count: int
    average_cell_accuracy: float
    task_records: List[Dict[str, Any]]
    task_ids: List[str]
    task_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _shape(grid: Grid) -> List[int]:
    if not grid:
        return [0, 0]
    return [len(grid), len(grid[0])]


def _copy_grid(grid: Grid) -> Grid:
    return [list(row) for row in grid]


def _identity_baseline_prediction(input_grid: Grid) -> Grid:
    """Public deterministic baseline strategy.

    The first Milestone #3 runner intentionally uses a simple identity baseline:
    prediction equals input grid. Later tasks can rank richer strategies without
    exposing private logic.
    """

    return _copy_grid(input_grid)


def _cell_accuracy(prediction: Grid, expected_output: Grid) -> Dict[str, Any]:
    if _shape(prediction) != _shape(expected_output):
        return {
            "cell_accuracy": 0.0,
            "mismatch_count": max(
                sum(len(row) for row in prediction),
                sum(len(row) for row in expected_output),
            ),
        }

    total = 0
    mismatches = 0

    for predicted_row, expected_row in zip(prediction, expected_output):
        for predicted_cell, expected_cell in zip(predicted_row, expected_row):
            total += 1
            if predicted_cell != expected_cell:
                mismatches += 1

    if total == 0:
        return {"cell_accuracy": 0.0, "mismatch_count": 0}

    return {
        "cell_accuracy": round((total - mismatches) / total, 6),
        "mismatch_count": mismatches,
    }


def _task_id_for(sample_id: str, runner_strategy: str) -> str:
    signature = _stable_signature(
        {
            "sample_id": sample_id,
            "runner_strategy": runner_strategy,
        }
    )
    return f"BATCH-TASK-{signature[:12]}"


def build_batch_benchmark_task_record(
    sample: Dict[str, Any],
    *,
    runner_strategy: str = "identity_baseline_v1",
) -> BatchBenchmarkTaskRecord:
    """Build one deterministic batch benchmark task record."""

    if not isinstance(sample, dict):
        raise ValueError("Batch benchmark sample must be a dictionary")

    sample_id = str(sample.get("sample_id") or "").strip()
    sample_name = str(sample.get("name") or "").strip()
    input_grid = sample.get("input_grid")
    expected_output = sample.get("expected_output")

    if not sample_id:
        raise ValueError("Batch benchmark sample requires sample_id")
    if not sample_name:
        raise ValueError("Batch benchmark sample requires name")
    if not isinstance(input_grid, list) or not isinstance(expected_output, list):
        raise ValueError("Batch benchmark sample requires input_grid and expected_output")

    if runner_strategy != "identity_baseline_v1":
        raise ValueError("Unsupported public batch runner strategy")

    prediction = _identity_baseline_prediction(input_grid)
    exact_match = prediction == expected_output
    accuracy = _cell_accuracy(prediction, expected_output)
    task_id = _task_id_for(sample_id, runner_strategy)

    signature_basis = {
        "task_id": task_id,
        "sample_id": sample_id,
        "runner_strategy": runner_strategy,
        "prediction": prediction,
        "expected_output": expected_output,
        "exact_match": exact_match,
        "cell_accuracy": accuracy["cell_accuracy"],
        "mismatch_count": accuracy["mismatch_count"],
    }
    signature = _stable_signature(signature_basis)

    return BatchBenchmarkTaskRecord(
        status="BATCH_BENCHMARK_TASK_READY",
        task_id=task_id,
        sample_id=sample_id,
        sample_name=sample_name,
        runner_strategy=runner_strategy,
        input_shape=_shape(input_grid),
        expected_shape=_shape(expected_output),
        predicted_shape=_shape(prediction),
        prediction=prediction,
        expected_output=_copy_grid(expected_output),
        exact_match=exact_match,
        cell_accuracy=accuracy["cell_accuracy"],
        mismatch_count=accuracy["mismatch_count"],
        verified=True,
        signature=signature,
        metadata={
            "source": "batch_benchmark_runner_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_dataset_sample_registry": True,
        },
    )


def _coerce_registry(registry: Optional[DatasetSampleRegistry | Dict[str, Any]]) -> Dict[str, Any]:
    if registry is None:
        return generate_dataset_sample_registry().to_dict()

    if isinstance(registry, DatasetSampleRegistry):
        return registry.to_dict()

    if isinstance(registry, dict):
        return copy.deepcopy(registry)

    raise ValueError("Batch benchmark runner requires a DatasetSampleRegistry or dictionary")


def run_batch_benchmark(
    registry: Optional[DatasetSampleRegistry | Dict[str, Any]] = None,
    *,
    runner_strategy: str = "identity_baseline_v1",
) -> BatchBenchmarkRun:
    """Run deterministic batch benchmark over registry samples."""

    registry_data = _coerce_registry(registry)
    registry_validation = validate_dataset_sample_registry(registry_data)

    if registry_validation["status"] != "DATASET_SAMPLE_REGISTRY_VALID":
        raise ValueError("Batch benchmark runner requires a valid DATASET_SAMPLE_REGISTRY_VALID payload")

    samples = registry_data.get("samples")
    if not isinstance(samples, list) or not samples:
        raise ValueError("Batch benchmark runner requires non-empty registry samples")

    task_records = [
        build_batch_benchmark_task_record(sample, runner_strategy=runner_strategy)
        for sample in samples
    ]
    task_records_sorted = sorted(task_records, key=lambda item: item.task_id)
    task_dicts = [record.to_dict() for record in task_records_sorted]

    task_count = len(task_records_sorted)
    matched_count = sum(1 for record in task_records_sorted if record.exact_match)
    mismatched_count = task_count - matched_count
    verified_count = sum(1 for record in task_records_sorted if record.verified)

    average_cell_accuracy = (
        round(sum(record.cell_accuracy for record in task_records_sorted) / task_count, 6)
        if task_count
        else 0.0
    )

    task_ids = [record.task_id for record in task_records_sorted]
    task_signatures = {record.task_id: record.signature for record in task_records_sorted}

    signature_basis = {
        "registry_id": registry_data.get("registry_id"),
        "runner_strategy": runner_strategy,
        "task_ids": task_ids,
        "task_signatures": task_signatures,
        "task_count": task_count,
        "matched_count": matched_count,
        "mismatched_count": mismatched_count,
        "average_cell_accuracy": average_cell_accuracy,
    }
    signature = _stable_signature(signature_basis)
    batch_id = f"BATCH-BENCHMARK-{signature[:12]}"

    return BatchBenchmarkRun(
        status="BATCH_BENCHMARK_RUN_READY",
        batch_status="BATCH_BENCHMARK_RUN_VALID",
        batch_id=batch_id,
        registry_id=str(registry_data.get("registry_id")),
        runner_strategy=runner_strategy,
        task_count=task_count,
        matched_count=matched_count,
        mismatched_count=mismatched_count,
        verified_count=verified_count,
        average_cell_accuracy=average_cell_accuracy,
        task_records=task_dicts,
        task_ids=task_ids,
        task_signatures=task_signatures,
        signature=signature,
        metadata={
            "source": "batch_benchmark_runner_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 2",
        },
    )


def render_batch_benchmark_markdown(batch_run: BatchBenchmarkRun | Dict[str, Any]) -> str:
    data = batch_run.to_dict() if isinstance(batch_run, BatchBenchmarkRun) else dict(batch_run)

    lines = [
        "# ARC-AGI-3 Batch Benchmark Runner v1",
        "",
        f"Status: {data['status']}",
        f"Batch status: {data['batch_status']}",
        f"Batch ID: {data['batch_id']}",
        f"Registry ID: {data['registry_id']}",
        f"Runner strategy: {data['runner_strategy']}",
        f"Task count: {data['task_count']}",
        f"Matched count: {data['matched_count']}",
        f"Mismatched count: {data['mismatched_count']}",
        f"Verified count: {data['verified_count']}",
        f"Average cell accuracy: {data['average_cell_accuracy']}",
        "",
        "## Task records",
        "",
    ]

    for record in data.get("task_records", []):
        lines.extend(
            [
                f"### {record['task_id']}",
                "",
                f"- Sample ID: {record['sample_id']}",
                f"- Sample name: {record['sample_name']}",
                f"- Exact match: {str(record['exact_match']).lower()}",
                f"- Cell accuracy: {record['cell_accuracy']}",
                f"- Mismatch count: {record['mismatch_count']}",
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
            f"Batch signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_batch_benchmark_run(batch_run: BatchBenchmarkRun | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Batch Benchmark Runner v1 public contract."""

    data = batch_run.to_dict() if isinstance(batch_run, BatchBenchmarkRun) else dict(batch_run)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    task_records = data.get("task_records") if isinstance(data.get("task_records"), list) else []

    task_checks = []
    for record in task_records:
        record_metadata = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
        task_checks.append(
            record.get("status") == "BATCH_BENCHMARK_TASK_READY"
            and isinstance(record.get("task_id"), str)
            and isinstance(record.get("sample_id"), str)
            and isinstance(record.get("prediction"), list)
            and isinstance(record.get("expected_output"), list)
            and isinstance(record.get("cell_accuracy"), float)
            and isinstance(record.get("mismatch_count"), int)
            and record.get("verified") is True
            and isinstance(record.get("signature"), str)
            and record_metadata.get("public_safe") is True
            and record_metadata.get("deterministic") is True
            and record_metadata.get("external_api_dependency") is False
            and record_metadata.get("executes_dataset_code") is False
            and record_metadata.get("contains_api_keys") is False
        )

    task_count_value = data.get("task_count")
    matched_count_value = data.get("matched_count")
    mismatched_count_value = data.get("mismatched_count")
    verified_count_value = data.get("verified_count")

    matched_plus_mismatched_matches = (
        isinstance(task_count_value, int)
        and isinstance(matched_count_value, int)
        and isinstance(mismatched_count_value, int)
        and task_count_value == matched_count_value + mismatched_count_value
    )

    checks = {
        "status_ready": data.get("status") == "BATCH_BENCHMARK_RUN_READY",
        "batch_status_valid": data.get("batch_status") == "BATCH_BENCHMARK_RUN_VALID",
        "batch_id_present": bool(data.get("batch_id")),
        "registry_id_present": bool(data.get("registry_id")),
        "runner_strategy_valid": data.get("runner_strategy") == "identity_baseline_v1",
        "task_count_positive": isinstance(task_count_value, int) and task_count_value > 0,
        "task_count_matches": task_count_value == len(task_records),
        "matched_plus_mismatched_matches": matched_plus_mismatched_matches,
        "verified_count_matches": verified_count_value == len(task_records),
        "average_cell_accuracy_number": isinstance(data.get("average_cell_accuracy"), float),
        "task_ids_list": isinstance(data.get("task_ids"), list),
        "task_signatures_dict": isinstance(data.get("task_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_task_records_valid": bool(task_checks) and all(task_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "BATCH_BENCHMARK_RUN_VALID" if valid else "BATCH_BENCHMARK_RUN_INVALID",
        "valid": valid,
        "checks": checks,
        "batch_id": data.get("batch_id"),
        "registry_id": data.get("registry_id"),
        "task_count": data.get("task_count"),
        "matched_count": data.get("matched_count"),
        "mismatched_count": data.get("mismatched_count"),
        "average_cell_accuracy": data.get("average_cell_accuracy"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "batch_benchmark_runner_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_batch_benchmark_run(
    registry: Optional[DatasetSampleRegistry | Dict[str, Any]] = None,
) -> Dict[str, Any]:
    batch_run = run_batch_benchmark(registry)
    validation = validate_batch_benchmark_run(batch_run)

    return {
        "status": "BATCH_BENCHMARK_PIPELINE_READY",
        "batch_benchmark_run": batch_run.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "batch_benchmark_runner_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_dataset_sample_registry": True,
        },
    }


def write_batch_benchmark_artifacts(
    batch_run: BatchBenchmarkRun | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/batch-benchmark-runner",
) -> Dict[str, str]:
    data = batch_run.to_dict() if isinstance(batch_run, BatchBenchmarkRun) else dict(batch_run)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "batch-benchmark-run.json"
    markdown_path = output_path / "batch-benchmark-run.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_batch_benchmark_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
