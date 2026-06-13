import json
from pathlib import Path

import pytest

from hbce_arc_agi3.strategy_interface_v2 import (
    IdentityBaselineStrategyV2,
    StrategyExample,
    StrategyInput,
    StrategyRegistryV2,
    build_strategy_interface_v2_smoke_input,
    grid_shape,
    grid_signature,
    normalize_grid,
    render_strategy_interface_v2_markdown,
    run_strategy_interface_v2_pipeline,
    validate_strategy_descriptor,
    validate_strategy_interface_v2_pipeline,
    validate_strategy_result,
    write_strategy_interface_v2_artifacts,
)


def test_normalize_grid_accepts_rectangular_int_grid():
    assert normalize_grid([[1, 2], [3, 4]]) == ((1, 2), (3, 4))


def test_normalize_grid_rejects_empty_grid():
    with pytest.raises(ValueError, match="must not be empty"):
        normalize_grid([])


def test_normalize_grid_rejects_ragged_grid():
    with pytest.raises(ValueError, match="rectangular"):
        normalize_grid([[1, 2], [3]])


def test_normalize_grid_rejects_non_color_value():
    with pytest.raises(ValueError, match="between 0 and 9"):
        normalize_grid([[10]])


def test_grid_shape_and_signature_are_deterministic():
    grid = [[1, 0], [0, 1]]

    assert grid_shape(grid) == {"height": 2, "width": 2, "cell_count": 4}
    assert grid_signature(grid) == grid_signature(grid)


def test_strategy_input_builds_normalized_contract():
    strategy_input = build_strategy_interface_v2_smoke_input()

    assert strategy_input.task_id == "MILESTONE-4-TASK-1-SMOKE"
    assert len(strategy_input.train_pairs) == 1
    assert strategy_input.metadata["score_oriented"] is True
    assert strategy_input.metadata["prize_oriented_solver_target"] is True
    assert strategy_input.metadata["kaggle_submission_sent"] is False


def test_strategy_example_to_dict_contains_shapes():
    example = StrategyExample.build([[1]], [[2]])

    payload = example.to_dict()

    assert payload["input_shape"]["cell_count"] == 1
    assert payload["output_shape"]["cell_count"] == 1
    assert payload["input_signature"]
    assert payload["output_signature"]


def test_identity_baseline_strategy_descriptor_is_valid():
    strategy = IdentityBaselineStrategyV2()
    validation = validate_strategy_descriptor(strategy.descriptor)

    assert validation["status"] == "STRATEGY_DESCRIPTOR_VALID"
    assert validation["valid"] is True
    assert validation["strategy_id"] == "STRATEGY-IDENTITY-BASELINE-v2"


def test_identity_baseline_returns_test_input_candidate():
    strategy_input = build_strategy_interface_v2_smoke_input()
    result = IdentityBaselineStrategyV2().solve(strategy_input)

    assert result.status == "STRATEGY_RESULT_READY"
    assert result.strategy_id == "STRATEGY-IDENTITY-BASELINE-v2"
    assert result.candidate_grid == strategy_input.test_input
    assert result.metadata["candidate_policy"] == "RETURN_TEST_INPUT_UNCHANGED"


def test_identity_baseline_result_is_valid():
    strategy_input = build_strategy_interface_v2_smoke_input()
    result = IdentityBaselineStrategyV2().solve(strategy_input)
    validation = validate_strategy_result(result, expected_task_id=strategy_input.task_id)

    assert validation["status"] == "STRATEGY_RESULT_VALID"
    assert validation["valid"] is True


def test_strategy_registry_default_selects_identity_baseline():
    strategy_input = build_strategy_interface_v2_smoke_input()
    registry = StrategyRegistryV2.build_default()

    result = registry.select_best(strategy_input)

    assert len(registry.descriptors()) == 1
    assert result.strategy_id == "STRATEGY-IDENTITY-BASELINE-v2"


def test_strategy_registry_rejects_duplicate_strategy_id():
    registry = StrategyRegistryV2.build_default()

    with pytest.raises(ValueError, match="duplicate strategy_id"):
        registry.register(IdentityBaselineStrategyV2())


def test_strategy_interface_pipeline_is_valid():
    payload = run_strategy_interface_v2_pipeline()
    validation = validate_strategy_interface_v2_pipeline(payload)

    assert payload["status"] == "STRATEGY_INTERFACE_V2_PIPELINE_READY"
    assert payload["interface_status"] == "STRATEGY_INTERFACE_V2_READY"
    assert payload["validation_status"] == "STRATEGY_INTERFACE_V2_VALID"
    assert validation["status"] == "STRATEGY_INTERFACE_V2_VALID"
    assert payload["strategy_count"] == 1
    assert payload["candidate_count"] == 1
    assert payload["best_strategy_id"] == "STRATEGY-IDENTITY-BASELINE-v2"


def test_strategy_interface_pipeline_is_deterministic():
    first = run_strategy_interface_v2_pipeline()
    second = run_strategy_interface_v2_pipeline()

    assert first == second
    assert first["signature"] == second["signature"]


def test_strategy_interface_pipeline_boundary_metadata():
    payload = run_strategy_interface_v2_pipeline()
    metadata = payload["metadata"]

    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["score_oriented"] is True
    assert metadata["prize_oriented_solver_target"] is True
    assert metadata["result_required"] is True
    assert metadata["score_improvement_required"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False


def test_strategy_interface_pipeline_validation_rejects_broken_payload():
    validation = validate_strategy_interface_v2_pipeline(
        {
            "status": "BROKEN",
            "metadata": {},
        }
    )

    assert validation["status"] == "STRATEGY_INTERFACE_V2_INVALID"
    assert validation["valid"] is False


def test_strategy_interface_markdown_contains_boundary():
    payload = run_strategy_interface_v2_pipeline()
    markdown = render_strategy_interface_v2_markdown(payload)

    assert "# ARC-AGI-3 Milestone #4 Task 1" in markdown
    assert "score_oriented=true" in markdown
    assert "prize_oriented_solver_target=true" in markdown
    assert "kaggle_submission_sent=false" in markdown


def test_strategy_interface_writes_artifacts(tmp_path: Path):
    payload = run_strategy_interface_v2_pipeline()
    artifacts = write_strategy_interface_v2_artifacts(payload, output_dir=str(tmp_path / "strategy"))

    json_path = Path(artifacts["json_path"])
    markdown_path = Path(artifacts["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["validation_status"] == "STRATEGY_INTERFACE_V2_VALID"
    assert markdown_path.read_text(encoding="utf-8").startswith("# ARC-AGI-3 Milestone #4 Task 1")


def test_strategy_input_mapping_train_pairs_supported():
    strategy_input = StrategyInput.build(
        task_id="MAPPING-PAIR-SMOKE",
        train_pairs=[
            {
                "input": [[1, 1], [0, 0]],
                "output": [[2, 2], [0, 0]],
            }
        ],
        test_input=[[1, 0], [0, 1]],
    )

    assert strategy_input.task_id == "MAPPING-PAIR-SMOKE"
    assert len(strategy_input.train_pairs) == 1
