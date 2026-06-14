from pathlib import Path

from hbce_arc_agi3.milestone_4_solver_engine_closure import (
    CLOSURE_STATUS,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_4_solver_engine_closure,
    render_milestone_4_solver_engine_closure_markdown,
    run_milestone_4_solver_engine_closure_pipeline,
    validate_milestone_4_solver_engine_closure,
    write_milestone_4_solver_engine_closure_artifacts,
)


def test_milestone_4_solver_engine_closure_ready():
    closure = build_milestone_4_solver_engine_closure()

    assert closure.status == CLOSURE_STATUS
    assert closure.closed_task_count == 9
    assert closure.final_test_count_before_closure == 337
    assert closure.ready_for_next_phase is True
    assert closure.kaggle_submission_sent is False
    assert closure.solver_engine_result["expanded_best_candidate_match_rate"] == 1.0
    assert closure.solver_engine_result["failure_loop_improvement_item_count"] == 0
    assert closure.solver_engine_result["failure_loop_next_solver_target"] == "none"


def test_milestone_4_solver_engine_closure_validation_passes():
    closure = build_milestone_4_solver_engine_closure()
    validation = validate_milestone_4_solver_engine_closure(closure)

    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_milestone_4_solver_engine_closure_pipeline_ready():
    payload = run_milestone_4_solver_engine_closure_pipeline()

    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closed_task_count"] == 9
    assert payload["final_test_count_before_closure"] == 337
    assert payload["ready_for_next_phase"] is True
    assert payload["kaggle_submission_sent"] is False


def test_milestone_4_solver_engine_closure_markdown_contains_markers():
    closure = build_milestone_4_solver_engine_closure()
    markdown = render_milestone_4_solver_engine_closure_markdown(closure)

    assert "ARC_AGI3_MILESTONE_4_SOLVER_ENGINE_CLOSURE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_4_TASKS_CLOSED=9" in markdown
    assert "ARC_AGI3_MILESTONE_4_FINAL_TESTS_PASS=337" in markdown
    assert "ARC_AGI3_MILESTONE_4_READY_FOR_NEXT_PHASE=true" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_milestone_4_solver_engine_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_4_solver_engine_closure()
    paths = write_milestone_4_solver_engine_closure_artifacts(
        closure,
        output_dir=str(tmp_path),
    )

    json_path = Path(paths["json_path"])
    markdown_path = Path(paths["markdown_path"])

    assert json_path.exists()
    assert markdown_path.exists()
    assert "MILESTONE_4_SOLVER_ENGINE_CLOSURE_READY" in json_path.read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_4_SOLVER_ENGINE_CLOSURE_V1_READY=true" in markdown_path.read_text(encoding="utf-8")
