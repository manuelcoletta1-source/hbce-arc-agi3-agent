import json
from pathlib import Path

import pytest

from hbce_arc_agi3.report_index_generator import (
    ReportIndexEntry,
    build_report_index,
    generate_and_validate_report_index,
    render_report_index_markdown,
    validate_report_index,
    write_report_index_artifacts,
)


def test_report_index_builds_default_index():
    index = build_report_index()
    validation = validate_report_index(index)

    assert index.status == "REPORT_INDEX_GENERATOR_READY"
    assert index.index_status == "REPORT_INDEX_VALID"
    assert index.indexed_report_count == 5
    assert index.ready_report_count == 5
    assert index.indexed_artifact_count == 15
    assert validation["status"] == "REPORT_INDEX_VALID"


def test_report_index_pipeline_wrapper():
    result = generate_and_validate_report_index()

    assert result["status"] == "REPORT_INDEX_GENERATOR_PIPELINE_READY"
    assert result["report_index"]["status"] == "REPORT_INDEX_GENERATOR_READY"
    assert result["validation"]["status"] == "REPORT_INDEX_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_report_index_source_chain_contains_expected_ids():
    index = build_report_index()
    source_chain = index.source_chain_ids

    assert source_chain["dataset_sample_registry_id"].startswith("DATASET-SAMPLE-REGISTRY-")
    assert source_chain["batch_id"].startswith("BATCH-BENCHMARK-")
    assert source_chain["multi_task_outcome_aggregate_id"].startswith("MULTI-TASK-OUTCOME-")
    assert source_chain["strategy_selection_index_id"].startswith("STRATEGY-SELECTION-INDEX-")
    assert source_chain["failure_taxonomy_report_id"].startswith("FAILURE-TAXONOMY-REPORT-")
    assert source_chain["selected_strategy_id"] == "STRATEGY-IDENTITY-BASELINE-v1"
    assert source_chain["primary_failure_class"] == "PARTIAL_TRANSFORM_REFERENCE_MISMATCH"


def test_report_index_is_deterministic():
    first = build_report_index()
    second = build_report_index()

    assert first.to_dict() == second.to_dict()
    assert first.report_index_id == second.report_index_id
    assert first.signature == second.signature


def test_report_index_entries_are_public_safe():
    index = build_report_index()

    assert all(entry["status"] == "REPORT_INDEX_ENTRY_READY" for entry in index.report_entries)
    assert all(entry["public_safe"] is True for entry in index.report_entries)
    assert all(entry["external_api_dependency"] is False for entry in index.report_entries)
    assert all(entry["kaggle_submission_sent"] is False for entry in index.report_entries)
    assert all(entry["private_core_exposure"] is False for entry in index.report_entries)


def test_report_index_rejects_empty_entries():
    with pytest.raises(ValueError, match="at least one entry"):
        build_report_index([])


def test_report_index_accepts_custom_entry_dict():
    entry = ReportIndexEntry(
        status="REPORT_INDEX_ENTRY_READY",
        report_key="custom_report",
        report_title="Custom Report",
        report_type="public_custom_report",
        milestone="Milestone #3",
        task="Task X",
        module_name="custom_module",
        primary_path="docs/custom.md",
        artifact_paths=["examples/custom.json"],
        ready_marker="CUSTOM_READY=true",
        public_safe=True,
        deterministic=True,
        external_api_dependency=False,
        kaggle_submission_sent=False,
        private_core_exposure=False,
        signature="CUSTOMSIGNATURE",
        metadata={
            "source": "report_index_generator_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
        },
    ).to_dict()

    index = build_report_index([entry])

    assert index.indexed_report_count == 1
    assert index.report_entries[0]["report_key"] == "custom_report"


def test_report_index_markdown_contains_boundary():
    index = build_report_index()
    markdown = render_report_index_markdown(index)

    assert "# ARC-AGI-3 Report Index Generator v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert index.signature in markdown


def test_report_index_writes_artifacts(tmp_path: Path):
    index = build_report_index()
    artifacts = write_report_index_artifacts(index, output_dir=tmp_path / "report-index")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["indexed_report_count"] == 5
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Report Index Generator v1")


def test_report_index_validation_rejects_broken_contract():
    validation = validate_report_index(
        {
            "status": "BROKEN",
            "metadata": {},
            "report_entries": [],
        }
    )

    assert validation["status"] == "REPORT_INDEX_INVALID"
    assert validation["valid"] is False
