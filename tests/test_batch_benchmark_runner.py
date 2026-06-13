import json
from pathlib import Path

import pytest

from hbce_arc_agi3.batch_benchmark_runner import (
    build_batch_benchmark_task_record,
    generate_and_validate_batch_benchmark_run,
    render_batch_benchmark_markdown,
    run_batch_benchmark,
    validate_batch_benchmark_run,
    write_batch_benchmark_artifacts,
)
from hbce_arc_agi3.dataset_sample_registry import generate_dataset_sample_registry


def test_batch_benchmark_task_record_builds_identity_prediction():
    registry = generate_dataset_sample_registry()
    sample = registry.samples[0]
    record = build_batch_benchmark_task_record(sample)

    assert record.status == "BATCH_BENCHMARK_TASK_READY"
    assert record.task_id.startswith("BATCH-TASK-")
    assert record.runner_strategy == "identity_baseline_v1"
    assert record.prediction == sample["input_grid"]
    assert record.verified is True
    assert record.metadata["uses_dataset_sample_registry"] is True


def test_batch_benchmark_run_generates_default_batch():
    batch_run = run_batch_benchmark()
    validation = validate_batch_benchmark_run(batch_run)

    assert batch_run.status == "BATCH_BENCHMARK_RUN_READY"
    assert batch_run.batch_status == "BATCH_BENCHMARK_RUN_VALID"
    assert batch_run.task_count == 3
    assert batch_run.matched_count == 2
    assert batch_run.mismatched_count == 1
    assert validation["status"] == "BATCH_BENCHMARK_RUN_VALID"


def test_batch_benchmark_pipeline_wrapper():
    result = generate_and_validate_batch_benchmark_run()

    assert result["status"] == "BATCH_BENCHMARK_PIPELINE_READY"
    assert result["batch_benchmark_run"]["status"] == "BATCH_BENCHMARK_RUN_READY"
    assert result["validation"]["status"] == "BATCH_BENCHMARK_RUN_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_batch_benchmark_run_is_deterministic():
    first = run_batch_benchmark()
    second = run_batch_benchmark()

    assert first.to_dict() == second.to_dict()
    assert first.batch_id == second.batch_id
    assert first.signature == second.signature


def test_batch_benchmark_accepts_registry_payload_dict():
    registry = generate_dataset_sample_registry().to_dict()
    batch_run = run_batch_benchmark(registry)

    assert batch_run.registry_id == registry["registry_id"]
    assert batch_run.task_count == registry["sample_count"]


def test_batch_benchmark_rejects_invalid_registry_payload():
    with pytest.raises(ValueError, match="DATASET_SAMPLE_REGISTRY_VALID"):
        run_batch_benchmark({"status": "BROKEN", "metadata": {}, "samples": []})


def test_batch_benchmark_rejects_unsupported_strategy():
    registry = generate_dataset_sample_registry()
    with pytest.raises(ValueError, match="Unsupported"):
        run_batch_benchmark(registry, runner_strategy="private_strategy")


def test_batch_benchmark_markdown_contains_boundary():
    batch_run = run_batch_benchmark()
    markdown = render_batch_benchmark_markdown(batch_run)

    assert "# ARC-AGI-3 Batch Benchmark Runner v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert batch_run.signature in markdown


def test_batch_benchmark_writes_artifacts(tmp_path: Path):
    batch_run = run_batch_benchmark()
    artifacts = write_batch_benchmark_artifacts(batch_run, output_dir=tmp_path / "batch")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["task_count"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Batch Benchmark Runner v1")


def test_batch_benchmark_validation_rejects_broken_contract():
    validation = validate_batch_benchmark_run(
        {
            "status": "BROKEN",
            "metadata": {},
            "task_records": [],
        }
    )

    assert validation["status"] == "BATCH_BENCHMARK_RUN_INVALID"
    assert validation["valid"] is False
