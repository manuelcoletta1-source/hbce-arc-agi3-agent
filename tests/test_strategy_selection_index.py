import json
from pathlib import Path

import pytest

from hbce_arc_agi3.multi_task_outcome_aggregator import aggregate_multi_task_outcomes
from hbce_arc_agi3.strategy_selection_index import (
    build_strategy_selection_index,
    generate_and_validate_strategy_selection_index,
    render_strategy_selection_index_markdown,
    validate_strategy_selection_index,
    write_strategy_selection_index_artifacts,
)


def test_strategy_selection_index_builds_default_index():
    index = build_strategy_selection_index()
    validation = validate_strategy_selection_index(index)

    assert index.status == "STRATEGY_SELECTION_INDEX_READY"
    assert index.index_status == "STRATEGY_SELECTION_INDEX_VALID"
    assert index.candidate_count == 3
    assert index.selected_strategy_id == "STRATEGY-IDENTITY-BASELINE-v1"
    assert index.selected_strategy_name == "identity_baseline_v1"
    assert index.selected_score == 0.916667
    assert index.selected_quality_band == "STRONG"
    assert validation["status"] == "STRATEGY_SELECTION_INDEX_VALID"


def test_strategy_selection_index_pipeline_wrapper():
    result = generate_and_validate_strategy_selection_index()

    assert result["status"] == "STRATEGY_SELECTION_INDEX_PIPELINE_READY"
    assert result["strategy_selection_index"]["status"] == "STRATEGY_SELECTION_INDEX_READY"
    assert result["validation"]["status"] == "STRATEGY_SELECTION_INDEX_VALID"
    assert result["metadata"]["external_api_dependency"] is False


def test_strategy_selection_index_is_deterministic():
    first = build_strategy_selection_index()
    second = build_strategy_selection_index()

    assert first.to_dict() == second.to_dict()
    assert first.index_id == second.index_id
    assert first.signature == second.signature


def test_strategy_selection_index_accepts_aggregate_payload_dict():
    aggregate = aggregate_multi_task_outcomes().to_dict()
    index = build_strategy_selection_index(aggregate)

    assert index.aggregate_id == aggregate["aggregate_id"]
    assert index.batch_id == aggregate["batch_id"]
    assert index.registry_id == aggregate["registry_id"]


def test_strategy_selection_index_rejects_invalid_aggregate_payload():
    with pytest.raises(ValueError, match="MULTI_TASK_OUTCOME_AGGREGATE_VALID"):
        build_strategy_selection_index({"status": "BROKEN", "metadata": {}, "outcome_records": []})


def test_strategy_selection_index_candidates_are_ranked():
    index = build_strategy_selection_index()
    ranks = [candidate["rank"] for candidate in index.candidates]

    assert ranks == [1, 2, 3]
    assert index.candidates[0]["selected"] is True
    assert index.candidates[0]["strategy_id"] == index.selected_strategy_id


def test_strategy_selection_index_markdown_contains_boundary():
    index = build_strategy_selection_index()
    markdown = render_strategy_selection_index_markdown(index)

    assert "# ARC-AGI-3 Strategy Selection Index v1" in markdown
    assert "public_safe=true" in markdown
    assert "external_api_dependency=false" in markdown
    assert "kaggle_submission_sent=false" in markdown
    assert index.signature in markdown


def test_strategy_selection_index_writes_artifacts(tmp_path: Path):
    index = build_strategy_selection_index()
    artifacts = write_strategy_selection_index_artifacts(index, output_dir=tmp_path / "strategy")

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["candidate_count"] == 3
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Strategy Selection Index v1")


def test_strategy_selection_index_validation_rejects_broken_contract():
    validation = validate_strategy_selection_index(
        {
            "status": "BROKEN",
            "metadata": {},
            "candidates": [],
        }
    )

    assert validation["status"] == "STRATEGY_SELECTION_INDEX_INVALID"
    assert validation["valid"] is False


def test_strategy_selection_index_has_public_boundary_metadata():
    index = build_strategy_selection_index()

    assert index.metadata["public_safe"] is True
    assert index.metadata["deterministic"] is True
    assert index.metadata["external_api_dependency"] is False
    assert index.metadata["executes_dataset_code"] is False
    assert index.metadata["contains_api_keys"] is False
    assert index.metadata["private_core_exposure"] is False
    assert index.metadata["uses_multi_task_outcome_aggregator"] is True
