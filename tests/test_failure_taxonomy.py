import json
from pathlib import Path

import pytest

from hbce_arc_agi3.failure_taxonomy import (
    build_failure_taxonomy_entry,
    build_failure_taxonomy_report,
    generate_and_validate_failure_taxonomy_report,
    render_failure_taxonomy_markdown,
    validate_failure_taxonomy_report,
    write_failure_taxonomy_artifacts,
)
from hbce_arc_agi3.multi_task_outcome_aggregator import aggregate_multi_task_outcomes
from hbce_arc_agi3.strategy_selection_index import build_strategy_selection_index


def test_failure_taxonomy_entry_classifies_exact_match():
    aggregate = aggregate_multi_task_outcomes()
    exact_record = next(record for record in aggregate.outcome_records if record["outcome_status"] == "OUTCOME_MATCH")
    entry = build_failure_taxonomy_entry(exact_record)

    assert entry.status == "FAILURE_TAXONOMY_ENTRY_READY"
    assert entry.failure_class == "NO_FAILURE_EXACT_MATCH"
    assert entry.severity == "NONE"
    assert entry.is_failure is False
    assert entry.is_partial is False


def test_failure_taxonomy_entry_classifies_partial_mismatch():
    aggregate = aggregate_multi_task_outcomes()
    partial_record = next(record for record in aggregate.outcome_records if record["outcome_status"] == "OUTCOME_PARTIAL")
    entry = build_failure_taxonomy_entry(partial_record)

    assert entry.failure_class == "PARTIAL_TRANSFORM_REFERENCE_MISMATCH"
    assert entry.severity == "LOW"
    assert entry.is_failure is False
    assert entry.is_partial is True
    assert "repair strategy" in entry.remediation_hint


def test_failure_taxonomy_report_default_pipeline():
    report = build_failure_taxonomy_report()
    validation = validate_failure_taxonomy_report(report)

    assert report.status == "FAILURE_TAXONOMY_READY"
    assert report.taxonomy_status == "FAILURE_TAXONOMY_VALID"
    assert report.total_outcomes == 3
    assert report.exact_match_count == 2
    assert report.partial_count == 1
    assert report.failure_count == 0
    assert report.unverified_count == 0
    assert report.primary_failure_class == "PARTIAL_TRANSFORM_REFERENCE_MISMATCH"
    assert report.severity_band == "LOW"
    assert validation["status"] == "FAILURE_TAXONOMY_VALID"


def test_failure_taxonomy_pipeline_wrapper():
    result = generate_and_validate_failure_taxonomy_report()

    assert result["status"] == "FAILURE_TAXONOMY_PIPELINE_READY"
    assert result["failure_taxonomy_report"]["status"] == "FAILURE_TAXONOMY_READY"
    assert result["validation"]["status"] == "FAILURE_TAXONOMY_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_failure_taxonomy_is_deterministic():
    first = build_failure_taxonomy_report()
    second = build_failure_taxonomy_report()

    assert first.to_dict() == second.to_dict()
    assert first.taxonomy_report_id == second.taxonomy_report_id
    assert first.signature == second.signature


def test_failure_taxonomy_accepts_payload_dicts():
    aggregate = aggregate_multi_task_outcomes().to_dict()
    strategy_index = build_strategy_selection_index(aggregate).to_dict()
    report = build_failure_taxonomy_report(aggregate, strategy_index)

    assert report.aggregate_id == aggregate["aggregate_id"]
    assert report.index_id == strategy_index["index_id"]
    assert report.registry_id == aggregate["registry_id"]


def test_failure_taxonomy_rejects_invalid_aggregate_payload():
    with pytest.raises(ValueError, match="MULTI_TASK_OUTCOME_AGGREGATE_VALID"):
        build_failure_taxonomy_report({"status": "BROKEN", "metadata": {}, "outcome_records": []})


def test_failure_taxonomy_rejects_invalid_strategy_index_payload():
    aggregate = aggregate_multi_task_outcomes().to_dict()
    with pytest.raises(ValueError, match="STRATEGY_SELECTION_INDEX_VALID"):
        build_failure_taxonomy_report(aggregate, {"status": "BROKEN", "metadata": {}, "candidates": []})


def test_failure_taxonomy_markdown_contains_boundary():
    report = build_failure_taxonomy_report()
    markdown = render_failure_taxonomy_markdown(report)

    assert "# ARC-AGI-3 Failure Taxonomy v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert report.signature in markdown


def test_failure_taxonomy_writes_artifacts(tmp_path: Path):
    report = build_failure_taxonomy_report()
    artifacts = write_failure_taxonomy_artifacts(report, output_dir=tmp_path / "failure")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["total_outcomes"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Failure Taxonomy v1")


def test_failure_taxonomy_validation_rejects_broken_contract():
    validation = validate_failure_taxonomy_report(
        {
            "status": "BROKEN",
            "metadata": {},
            "taxonomy_entries": [],
        }
    )

    assert validation["status"] == "FAILURE_TAXONOMY_INVALID"
    assert validation["valid"] is False
