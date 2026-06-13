"""Dataset Sample Registry v1 for HBCE ARC-AGI-3 public baseline.

This module creates a deterministic public-safe registry for ARC-style sample
tasks used by the Milestone #3 multi-task benchmark pipeline.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


Grid = List[List[int]]


DEFAULT_SAMPLE_TASKS: List[Dict[str, Any]] = [
    {
        "name": "identity-single-object",
        "split": "public-smoke",
        "input_grid": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        "expected_output": [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        "tags": ["identity", "object-preservation", "smoke"],
    },
    {
        "name": "preserve-non-background",
        "split": "public-smoke",
        "input_grid": [[0, 2, 0], [0, 2, 0], [0, 0, 0]],
        "expected_output": [[0, 2, 0], [0, 2, 0], [0, 0, 0]],
        "tags": ["preserve-structure", "vertical-object", "smoke"],
    },
    {
        "name": "partial-transform-reference",
        "split": "public-smoke",
        "input_grid": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
        "tags": ["partial", "score-calibration", "smoke"],
    },
]


@dataclass(frozen=True)
class DatasetSampleRecord:
    status: str
    sample_id: str
    name: str
    split: str
    input_shape: List[int]
    expected_shape: List[int]
    input_grid: Grid
    expected_output: Grid
    tags: List[str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DatasetSampleRegistry:
    status: str
    registry_status: str
    registry_id: str
    sample_count: int
    samples: List[Dict[str, Any]]
    sample_ids: List[str]
    sample_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _coerce_int_grid(value: Any, *, field_name: str) -> Grid:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{field_name} must be a non-empty grid")

    width: Optional[int] = None
    grid: Grid = []

    for row in value:
        if not isinstance(row, list) or not row:
            raise ValueError(f"{field_name} rows must be non-empty lists")

        if width is None:
            width = len(row)
        elif len(row) != width:
            raise ValueError(f"{field_name} must be rectangular")

        coerced_row: List[int] = []
        for cell in row:
            if not isinstance(cell, int):
                raise ValueError(f"{field_name} cells must be integers")
            if cell < 0 or cell > 9:
                raise ValueError(f"{field_name} cells must be ARC color integers between 0 and 9")
            coerced_row.append(cell)

        grid.append(coerced_row)

    return grid


def _shape(grid: Grid) -> List[int]:
    return [len(grid), len(grid[0]) if grid else 0]


def _sample_id_for(name: str, input_grid: Grid, expected_output: Grid) -> str:
    signature = _stable_signature(
        {
            "name": name,
            "input_grid": input_grid,
            "expected_output": expected_output,
        }
    )
    return f"SAMPLE-{signature[:12]}"


def build_dataset_sample_record(payload: Dict[str, Any]) -> DatasetSampleRecord:
    """Build one deterministic sample registry record."""

    if not isinstance(payload, dict):
        raise ValueError("Sample payload must be a dictionary")

    name = str(payload.get("name") or "").strip()
    if not name:
        raise ValueError("Sample payload requires a name")

    split = str(payload.get("split") or "public-smoke").strip()
    input_grid = _coerce_int_grid(payload.get("input_grid"), field_name="input_grid")
    expected_output = _coerce_int_grid(payload.get("expected_output"), field_name="expected_output")

    tags_raw = payload.get("tags", [])
    if not isinstance(tags_raw, list):
        raise ValueError("tags must be a list")

    tags = sorted(str(tag).strip() for tag in tags_raw if str(tag).strip())
    sample_id = str(payload.get("sample_id") or _sample_id_for(name, input_grid, expected_output))

    signature_basis = {
        "sample_id": sample_id,
        "name": name,
        "split": split,
        "input_shape": _shape(input_grid),
        "expected_shape": _shape(expected_output),
        "input_grid": input_grid,
        "expected_output": expected_output,
        "tags": tags,
    }
    signature = _stable_signature(signature_basis)

    return DatasetSampleRecord(
        status="DATASET_SAMPLE_RECORD_READY",
        sample_id=sample_id,
        name=name,
        split=split,
        input_shape=_shape(input_grid),
        expected_shape=_shape(expected_output),
        input_grid=input_grid,
        expected_output=expected_output,
        tags=tags,
        signature=signature,
        metadata={
            "source": "dataset_sample_registry_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    )


def generate_dataset_sample_registry(
    samples: Optional[Iterable[Dict[str, Any]]] = None,
) -> DatasetSampleRegistry:
    """Generate a deterministic public sample registry."""

    source_samples = list(samples) if samples is not None else list(DEFAULT_SAMPLE_TASKS)
    records = [build_dataset_sample_record(sample) for sample in source_samples]

    records_sorted = sorted(records, key=lambda item: item.sample_id)
    sample_dicts = [record.to_dict() for record in records_sorted]
    sample_ids = [record.sample_id for record in records_sorted]
    sample_signatures = {record.sample_id: record.signature for record in records_sorted}

    registry_signature_basis = {
        "sample_ids": sample_ids,
        "sample_signatures": sample_signatures,
        "sample_count": len(records_sorted),
        "source": "dataset_sample_registry_v1",
    }
    signature = _stable_signature(registry_signature_basis)
    registry_id = f"DATASET-SAMPLE-REGISTRY-{signature[:12]}"

    return DatasetSampleRegistry(
        status="DATASET_SAMPLE_REGISTRY_READY",
        registry_status="DATASET_SAMPLE_REGISTRY_VALID",
        registry_id=registry_id,
        sample_count=len(records_sorted),
        samples=sample_dicts,
        sample_ids=sample_ids,
        sample_signatures=sample_signatures,
        signature=signature,
        metadata={
            "source": "dataset_sample_registry_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "milestone": "Milestone #3",
            "task": "Task 1",
        },
    )


def render_dataset_sample_registry_markdown(registry: DatasetSampleRegistry | Dict[str, Any]) -> str:
    data = registry.to_dict() if isinstance(registry, DatasetSampleRegistry) else dict(registry)

    lines = [
        "# ARC-AGI-3 Dataset Sample Registry v1",
        "",
        f"Status: {data['status']}",
        f"Registry status: {data['registry_status']}",
        f"Registry ID: {data['registry_id']}",
        f"Sample count: {data['sample_count']}",
        "",
        "## Samples",
        "",
    ]

    for sample in data.get("samples", []):
        lines.extend(
            [
                f"### {sample['sample_id']}",
                "",
                f"- Name: {sample['name']}",
                f"- Split: {sample['split']}",
                f"- Input shape: {sample['input_shape']}",
                f"- Expected shape: {sample['expected_shape']}",
                f"- Signature: {sample['signature']}",
                f"- Tags: {', '.join(sample.get('tags', []))}",
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
            f"Registry signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_dataset_sample_registry(registry: DatasetSampleRegistry | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Dataset Sample Registry v1 public contract."""

    data = registry.to_dict() if isinstance(registry, DatasetSampleRegistry) else dict(registry)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    samples = data.get("samples") if isinstance(data.get("samples"), list) else []

    sample_checks = []
    for sample in samples:
        sample_metadata = sample.get("metadata") if isinstance(sample.get("metadata"), dict) else {}
        sample_checks.append(
            isinstance(sample.get("sample_id"), str)
            and sample.get("status") == "DATASET_SAMPLE_RECORD_READY"
            and isinstance(sample.get("input_grid"), list)
            and isinstance(sample.get("expected_output"), list)
            and isinstance(sample.get("signature"), str)
            and sample_metadata.get("public_safe") is True
            and sample_metadata.get("deterministic") is True
            and sample_metadata.get("external_api_dependency") is False
            and sample_metadata.get("executes_dataset_code") is False
            and sample_metadata.get("contains_api_keys") is False
        )

    checks = {
        "status_ready": data.get("status") == "DATASET_SAMPLE_REGISTRY_READY",
        "registry_status_valid": data.get("registry_status") == "DATASET_SAMPLE_REGISTRY_VALID",
        "registry_id_present": bool(data.get("registry_id")),
        "sample_count_positive": isinstance(data.get("sample_count"), int) and data.get("sample_count") > 0,
        "sample_count_matches": data.get("sample_count") == len(samples),
        "sample_ids_list": isinstance(data.get("sample_ids"), list),
        "sample_signatures_dict": isinstance(data.get("sample_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_samples_valid": bool(sample_checks) and all(sample_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
    }

    valid = all(checks.values())

    return {
        "status": "DATASET_SAMPLE_REGISTRY_VALID" if valid else "DATASET_SAMPLE_REGISTRY_INVALID",
        "valid": valid,
        "checks": checks,
        "registry_id": data.get("registry_id"),
        "sample_count": data.get("sample_count"),
        "signature": data.get("signature"),
        "metadata": {
            "source": "dataset_sample_registry_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_dataset_sample_registry(
    samples: Optional[Iterable[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    registry = generate_dataset_sample_registry(samples)
    validation = validate_dataset_sample_registry(registry)

    return {
        "status": "DATASET_SAMPLE_REGISTRY_PIPELINE_READY",
        "dataset_sample_registry": registry.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "dataset_sample_registry_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    }


def write_dataset_sample_registry_artifacts(
    registry: DatasetSampleRegistry | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/dataset-sample-registry",
) -> Dict[str, str]:
    data = registry.to_dict() if isinstance(registry, DatasetSampleRegistry) else dict(registry)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "dataset-sample-registry.json"
    markdown_path = output_path / "dataset-sample-registry.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_dataset_sample_registry_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
