import json
from pathlib import Path

import pytest

from hbce_arc_agi3.batch_benchmark_runner import run_batch_benchmark
from hbce_arc_agi3.multi_task_outcome_aggregator import (
    aggregate_multi_task_outcomes,
    build_multi_task_outcome_record,
    generate_and_validate_multi_task_outcome_aggregate,
    render_multi_task_outcome_markdown,
    validate_multi_task_outcome_aggregate,
    write_multi_task_outcome_artifacts,
)


def test_multi_task_outcome_record_builds_from_batch_record():
    batch_run = run_batch_benchmark()
    task_record = batch_run.task_records[0]
    outcome = build_multi_task_outcome_record(task_record)

    assert outcome.status == "MULTI_TASK_OUTCOME_RECORD_READY"
    assert outcome.task_id == task_record["task_id"]
    assert outcome.sample_id == task_record["sample_id"]
    assert outcome.outcome_status in {"OUTCOME_MATCH", "OUTCOME_PARTIAL"}
    assert outcome.metadata["uses_batch_benchmark_runner"] is True


def test_multi_task_outcome_aggregate_default_batch():
    aggregate = aggregate_multi_task_outcomes()
    validation = validate_multi_task_outcome_aggregate(aggregate)

    assert aggregate.status == "MULTI_TASK_OUTCOME_AGGREGATOR_READY"
    assert aggregate.aggregate_status == "MULTI_TASK_OUTCOME_AGGREGATE_VALID"
    assert aggregate.task_count == 3
    assert aggregate.matched_count == 2
    assert aggregate.partial_count == 1
    assert aggregate.failed_count == 0
    assert aggregate.unverified_count == 0
    assert aggregate.average_calibrated_score == 0.916667
    assert aggregate.aggregate_quality_band == "STRONG"
    assert validation["status"] == "MULTI_TASK_OUTCOME_AGGREGATE_VALID"


def test_multi_task_outcome_pipeline_wrapper():
    result = generate_and_validate_multi_task_outcome_aggregate()

    assert result["status"] == "MULTI_TASK_OUTCOME_AGGREGATOR_PIPELINE_READY"
    assert result["multi_task_outcome_aggregate"]["status"] == "MULTI_TASK_OUTCOME_AGGREGATOR_READY"
    assert result["validation"]["status"] == "MULTI_TASK_OUTCOME_AGGREGATE_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_multi_task_outcome_aggregate_is_deterministic():
    first = aggregate_multi_task_outcomes()
    second = aggregate_multi_task_outcomes()

    assert first.to_dict() == second.to_dict()
    assert first.aggregate_id == second.aggregate_id
    assert first.signature == second.signature


def test_multi_task_outcome_accepts_batch_payload_dict():
    batch_run = run_batch_benchmark().to_dict()
    aggregate = aggregate_multi_task_outcomes(batch_run)

    assert aggregate.batch_id == batch_run["batch_id"]
    assert aggregate.registry_id == batch_run["registry_id"]
    assert aggregate.task_count == batch_run["task_count"]


def test_multi_task_outcome_rejects_invalid_batch_payload():
    with pytest.raises(ValueError, match="BATCH_BENCHMARK_RUN_VALID"):
        aggregate_multi_task_outcomes({"status": "BROKEN", "metadata": {}, "task_records": []})


def test_multi_task_outcome_rejects_invalid_task_record():
    with pytest.raises(ValueError, match="task_id"):
        build_multi_task_outcome_record({"sample_id": "SAMPLE-X", "sample_name": "broken"})


def test_multi_task_outcome_markdown_contains_boundary():
    aggregate = aggregate_multi_task_outcomes()
    markdown = render_multi_task_outcome_markdown(aggregate)

    assert "# ARC-AGI-3 Multi-Task Outcome Aggregator v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert aggregate.signature in markdown


def test_multi_task_outcome_writes_artifacts(tmp_path: Path):
    aggregate = aggregate_multi_task_outcomes()
    artifacts = write_multi_task_outcome_artifacts(aggregate, output_dir=tmp_path / "aggregate")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["task_count"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Multi-Task Outcome Aggregator v1")


def test_multi_task_outcome_validation_rejects_broken_contract():
    validation = validate_multi_task_outcome_aggregate(
        {
            "status": "BROKEN",
            "metadata": {},
            "outcome_records": [],
        }
    )

    assert validation["status"] == "MULTI_TASK_OUTCOME_AGGREGATE_INVALID"
    assert validation["valid"] is False
