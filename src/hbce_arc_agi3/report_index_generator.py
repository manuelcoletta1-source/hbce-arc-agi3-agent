"""Report Index Generator v1 for HBCE ARC-AGI-3 public baseline.

This module builds a deterministic public index of Milestone #3 reports and
artifacts generated so far.

It does not execute dataset code.
It does not call external APIs.
It does not read credentials.
It does not submit to Kaggle.
It does not expose private HBCE/JOKER-C2 runtime code.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.batch_benchmark_runner import run_batch_benchmark
from hbce_arc_agi3.failure_taxonomy import build_failure_taxonomy_report
from hbce_arc_agi3.multi_task_outcome_aggregator import aggregate_multi_task_outcomes
from hbce_arc_agi3.strategy_selection_index import build_strategy_selection_index


@dataclass(frozen=True)
class ReportIndexEntry:
    status: str
    report_key: str
    report_title: str
    report_type: str
    milestone: str
    task: str
    module_name: str
    primary_path: str
    artifact_paths: List[str]
    ready_marker: str
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
class ReportIndex:
    status: str
    index_status: str
    report_index_id: str
    milestone: str
    indexed_report_count: int
    indexed_artifact_count: int
    ready_report_count: int
    source_chain_ids: Dict[str, str]
    report_entries: List[Dict[str, Any]]
    report_keys: List[str]
    report_signatures: Dict[str, str]
    signature: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _stable_signature(payload: Dict[str, Any]) -> str:
    serial = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return sha256(serial).hexdigest()[:16].upper()


def _path_exists(path: str) -> bool:
    return Path(path).exists()


def _build_entry(
    *,
    report_key: str,
    report_title: str,
    report_type: str,
    task: str,
    module_name: str,
    primary_path: str,
    artifact_paths: List[str],
    ready_marker: str,
) -> ReportIndexEntry:
    public_safe = True
    deterministic = True
    external_api_dependency = False
    kaggle_submission_sent = False
    private_core_exposure = False

    signature_basis = {
        "report_key": report_key,
        "report_title": report_title,
        "report_type": report_type,
        "task": task,
        "module_name": module_name,
        "primary_path": primary_path,
        "artifact_paths": artifact_paths,
        "ready_marker": ready_marker,
        "public_safe": public_safe,
        "deterministic": deterministic,
        "external_api_dependency": external_api_dependency,
        "kaggle_submission_sent": kaggle_submission_sent,
        "private_core_exposure": private_core_exposure,
    }
    signature = _stable_signature(signature_basis)

    return ReportIndexEntry(
        status="REPORT_INDEX_ENTRY_READY",
        report_key=report_key,
        report_title=report_title,
        report_type=report_type,
        milestone="Milestone #3",
        task=task,
        module_name=module_name,
        primary_path=primary_path,
        artifact_paths=artifact_paths,
        ready_marker=ready_marker,
        public_safe=public_safe,
        deterministic=deterministic,
        external_api_dependency=external_api_dependency,
        kaggle_submission_sent=kaggle_submission_sent,
        private_core_exposure=private_core_exposure,
        signature=signature,
        metadata={
            "source": "report_index_generator_v1",
            "primary_path_exists": _path_exists(primary_path),
            "artifact_paths_exist": {path: _path_exists(path) for path in artifact_paths},
            "public_safe": public_safe,
            "deterministic": deterministic,
            "external_api_dependency": external_api_dependency,
            "kaggle_submission_sent": kaggle_submission_sent,
            "private_core_exposure": private_core_exposure,
        },
    )


def _default_report_entries() -> List[ReportIndexEntry]:
    return [
        _build_entry(
            report_key="dataset_sample_registry_v1",
            report_title="Dataset Sample Registry v1",
            report_type="public_registry_report",
            task="Task 1",
            module_name="dataset_sample_registry",
            primary_path="docs/dataset-sample-registry-v1.md",
            artifact_paths=[
                "examples/milestone-3/dataset-sample-registry/dataset-sample-registry.json",
                "examples/milestone-3/dataset-sample-registry/dataset-sample-registry.md",
            ],
            ready_marker="ARC_AGI3_DATASET_SAMPLE_REGISTRY_V1_READY=true",
        ),
        _build_entry(
            report_key="batch_benchmark_runner_v1",
            report_title="Batch Benchmark Runner v1",
            report_type="public_benchmark_report",
            task="Task 2",
            module_name="batch_benchmark_runner",
            primary_path="docs/batch-benchmark-runner-v1.md",
            artifact_paths=[
                "examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.json",
                "examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.md",
            ],
            ready_marker="ARC_AGI3_BATCH_BENCHMARK_RUNNER_V1_READY=true",
        ),
        _build_entry(
            report_key="multi_task_outcome_aggregator_v1",
            report_title="Multi-Task Outcome Aggregator v1",
            report_type="public_outcome_aggregate_report",
            task="Task 3",
            module_name="multi_task_outcome_aggregator",
            primary_path="docs/multi-task-outcome-aggregator-v1.md",
            artifact_paths=[
                "examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.json",
                "examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.md",
            ],
            ready_marker="ARC_AGI3_MULTI_TASK_OUTCOME_AGGREGATOR_V1_READY=true",
        ),
        _build_entry(
            report_key="strategy_selection_index_v1",
            report_title="Strategy Selection Index v1",
            report_type="public_strategy_selection_report",
            task="Task 4",
            module_name="strategy_selection_index",
            primary_path="docs/strategy-selection-index-v1.md",
            artifact_paths=[
                "examples/milestone-3/strategy-selection-index/strategy-selection-index.json",
                "examples/milestone-3/strategy-selection-index/strategy-selection-index.md",
            ],
            ready_marker="ARC_AGI3_STRATEGY_SELECTION_INDEX_V1_READY=true",
        ),
        _build_entry(
            report_key="failure_taxonomy_v1",
            report_title="Failure Taxonomy v1",
            report_type="public_failure_taxonomy_report",
            task="Task 5",
            module_name="failure_taxonomy",
            primary_path="docs/failure-taxonomy-v1.md",
            artifact_paths=[
                "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.json",
                "examples/milestone-3/failure-taxonomy/failure-taxonomy-report.md",
            ],
            ready_marker="ARC_AGI3_FAILURE_TAXONOMY_V1_READY=true",
        ),
    ]


def _source_chain_ids() -> Dict[str, str]:
    batch = run_batch_benchmark()
    batch_data = batch.to_dict() if hasattr(batch, "to_dict") else dict(batch)

    aggregate = aggregate_multi_task_outcomes()
    strategy_index = build_strategy_selection_index(aggregate)
    taxonomy = build_failure_taxonomy_report(aggregate, strategy_index)

    return {
        "dataset_sample_registry_id": str(batch_data.get("registry_id")),
        "batch_id": str(batch_data.get("batch_id")),
        "multi_task_outcome_aggregate_id": aggregate.aggregate_id,
        "strategy_selection_index_id": strategy_index.index_id,
        "failure_taxonomy_report_id": taxonomy.taxonomy_report_id,
        "selected_strategy_id": strategy_index.selected_strategy_id,
        "selected_strategy_name": strategy_index.selected_strategy_name,
        "primary_failure_class": taxonomy.primary_failure_class,
        "severity_band": taxonomy.severity_band,
    }


def build_report_index(entries: Optional[List[ReportIndexEntry | Dict[str, Any]]] = None) -> ReportIndex:
    """Build deterministic public report index for Milestone #3."""

    if entries is None:
        entry_objects = _default_report_entries()
    else:
        entry_objects = []
        for entry in entries:
            if isinstance(entry, ReportIndexEntry):
                entry_objects.append(entry)
            elif isinstance(entry, dict):
                entry_objects.append(ReportIndexEntry(**entry))
            else:
                raise ValueError("Report index entries must be ReportIndexEntry or dictionary")

    if not entry_objects:
        raise ValueError("Report index requires at least one entry")

    entries_sorted = sorted(entry_objects, key=lambda item: item.report_key)
    entry_dicts = [entry.to_dict() for entry in entries_sorted]
    report_keys = [entry.report_key for entry in entries_sorted]
    report_signatures = {entry.report_key: entry.signature for entry in entries_sorted}
    indexed_artifact_count = sum(1 + len(entry.artifact_paths) for entry in entries_sorted)
    ready_report_count = sum(1 for entry in entries_sorted if entry.status == "REPORT_INDEX_ENTRY_READY")
    source_chain_ids = _source_chain_ids()

    signature_basis = {
        "milestone": "Milestone #3",
        "report_keys": report_keys,
        "report_signatures": report_signatures,
        "indexed_report_count": len(entries_sorted),
        "indexed_artifact_count": indexed_artifact_count,
        "source_chain_ids": source_chain_ids,
    }
    signature = _stable_signature(signature_basis)
    report_index_id = f"REPORT-INDEX-{signature[:12]}"

    return ReportIndex(
        status="REPORT_INDEX_GENERATOR_READY",
        index_status="REPORT_INDEX_VALID",
        report_index_id=report_index_id,
        milestone="Milestone #3",
        indexed_report_count=len(entries_sorted),
        indexed_artifact_count=indexed_artifact_count,
        ready_report_count=ready_report_count,
        source_chain_ids=source_chain_ids,
        report_entries=entry_dicts,
        report_keys=report_keys,
        report_signatures=report_signatures,
        signature=signature,
        metadata={
            "source": "report_index_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
            "milestone": "Milestone #3",
            "task": "Task 6",
        },
    )


def render_report_index_markdown(index: ReportIndex | Dict[str, Any]) -> str:
    data = index.to_dict() if isinstance(index, ReportIndex) else dict(index)

    lines = [
        "# ARC-AGI-3 Report Index Generator v1",
        "",
        f"Status: {data['status']}",
        f"Index status: {data['index_status']}",
        f"Report index ID: {data['report_index_id']}",
        f"Milestone: {data['milestone']}",
        f"Indexed report count: {data['indexed_report_count']}",
        f"Indexed artifact count: {data['indexed_artifact_count']}",
        f"Ready report count: {data['ready_report_count']}",
        "",
        "## Source chain",
        "",
    ]

    for key, value in data.get("source_chain_ids", {}).items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Indexed reports", ""])

    for entry in data.get("report_entries", []):
        lines.extend(
            [
                f"### {entry['report_title']}",
                "",
                f"- Key: {entry['report_key']}",
                f"- Type: {entry['report_type']}",
                f"- Task: {entry['task']}",
                f"- Module: {entry['module_name']}",
                f"- Primary path: `{entry['primary_path']}`",
                f"- Ready marker: `{entry['ready_marker']}`",
                f"- Signature: {entry['signature']}",
                "",
                "Artifacts:",
                "",
            ]
        )
        for artifact_path in entry.get("artifact_paths", []):
            lines.append(f"- `{artifact_path}`")
        lines.append("")

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
            f"Report index signature: {data['signature']}",
            "",
        ]
    )

    return "\n".join(lines)


def validate_report_index(index: ReportIndex | Dict[str, Any]) -> Dict[str, Any]:
    """Validate Report Index Generator v1 public contract."""

    data = index.to_dict() if isinstance(index, ReportIndex) else dict(index)
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    entries = data.get("report_entries") if isinstance(data.get("report_entries"), list) else []
    source_chain_ids = data.get("source_chain_ids") if isinstance(data.get("source_chain_ids"), dict) else {}

    entry_checks = []
    for entry in entries:
        entry_metadata = entry.get("metadata") if isinstance(entry.get("metadata"), dict) else {}
        artifact_paths = entry.get("artifact_paths") if isinstance(entry.get("artifact_paths"), list) else []
        entry_checks.append(
            entry.get("status") == "REPORT_INDEX_ENTRY_READY"
            and isinstance(entry.get("report_key"), str)
            and isinstance(entry.get("report_title"), str)
            and isinstance(entry.get("report_type"), str)
            and isinstance(entry.get("task"), str)
            and isinstance(entry.get("module_name"), str)
            and isinstance(entry.get("primary_path"), str)
            and bool(artifact_paths)
            and isinstance(entry.get("ready_marker"), str)
            and entry.get("public_safe") is True
            and entry.get("deterministic") is True
            and entry.get("external_api_dependency") is False
            and entry.get("kaggle_submission_sent") is False
            and entry.get("private_core_exposure") is False
            and isinstance(entry.get("signature"), str)
            and entry_metadata.get("public_safe") is True
            and entry_metadata.get("deterministic") is True
            and entry_metadata.get("external_api_dependency") is False
            and entry_metadata.get("kaggle_submission_sent") is False
            and entry_metadata.get("private_core_exposure") is False
        )

    required_source_keys = {
        "dataset_sample_registry_id",
        "batch_id",
        "multi_task_outcome_aggregate_id",
        "strategy_selection_index_id",
        "failure_taxonomy_report_id",
        "selected_strategy_id",
        "selected_strategy_name",
        "primary_failure_class",
        "severity_band",
    }

    checks = {
        "status_ready": data.get("status") == "REPORT_INDEX_GENERATOR_READY",
        "index_status_valid": data.get("index_status") == "REPORT_INDEX_VALID",
        "report_index_id_present": bool(data.get("report_index_id")),
        "milestone_matches": data.get("milestone") == "Milestone #3",
        "indexed_report_count_positive": isinstance(data.get("indexed_report_count"), int)
        and data.get("indexed_report_count") > 0,
        "indexed_report_count_matches": data.get("indexed_report_count") == len(entries),
        "ready_report_count_matches": data.get("ready_report_count") == len(entries),
        "indexed_artifact_count_valid": isinstance(data.get("indexed_artifact_count"), int)
        and data.get("indexed_artifact_count") >= len(entries),
        "source_chain_ids_complete": required_source_keys.issubset(set(source_chain_ids.keys())),
        "report_keys_list": isinstance(data.get("report_keys"), list),
        "report_signatures_dict": isinstance(data.get("report_signatures"), dict),
        "signature_present": bool(data.get("signature")),
        "all_entries_valid": bool(entry_checks) and all(entry_checks),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
        "kaggle_submission_sent_false": metadata.get("kaggle_submission_sent") is False,
        "private_core_exposure_false": metadata.get("private_core_exposure") is False,
        "uses_failure_taxonomy": metadata.get("uses_failure_taxonomy") is True,
        "uses_strategy_selection_index": metadata.get("uses_strategy_selection_index") is True,
        "uses_multi_task_outcome_aggregator": metadata.get("uses_multi_task_outcome_aggregator") is True,
        "uses_batch_benchmark_runner": metadata.get("uses_batch_benchmark_runner") is True,
        "uses_dataset_sample_registry": metadata.get("uses_dataset_sample_registry") is True,
    }

    valid = all(checks.values())

    return {
        "status": "REPORT_INDEX_VALID" if valid else "REPORT_INDEX_INVALID",
        "valid": valid,
        "checks": checks,
        "report_index_id": data.get("report_index_id"),
        "indexed_report_count": data.get("indexed_report_count"),
        "indexed_artifact_count": data.get("indexed_artifact_count"),
        "ready_report_count": data.get("ready_report_count"),
        "source_chain_ids": source_chain_ids,
        "signature": data.get("signature"),
        "metadata": {
            "source": "report_index_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def generate_and_validate_report_index() -> Dict[str, Any]:
    index = build_report_index()
    validation = validate_report_index(index)

    return {
        "status": "REPORT_INDEX_GENERATOR_PIPELINE_READY",
        "report_index": index.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "report_index_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "uses_failure_taxonomy": True,
            "uses_strategy_selection_index": True,
            "uses_multi_task_outcome_aggregator": True,
            "uses_batch_benchmark_runner": True,
            "uses_dataset_sample_registry": True,
        },
    }


def write_report_index_artifacts(
    index: ReportIndex | Dict[str, Any],
    *,
    output_dir: str | Path = "examples/milestone-3/report-index-generator",
) -> Dict[str, str]:
    data = index.to_dict() if isinstance(index, ReportIndex) else dict(index)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "report-index.json"
    markdown_path = output_path / "report-index.md"

    json_path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_report_index_markdown(data), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }
