from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_final_closure import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_33_boundary_final_closure,
    validate_milestone_33_boundary_final_closure_report,
    write_milestone_33_task_6_artifacts,
)

def test_task_6_identity_and_source_regression_are_stable():
    report = run_milestone_33_boundary_final_closure()
    assert report["task_id"] == TASK_ID
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True

def test_task_6_closes_with_required_counts():
    report = run_milestone_33_boundary_final_closure()
    assert report["closure_case_count"] == 16
    assert report["pass_count"] == 16
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True

def test_task_6_next_stage_points_to_milestone_34_opening():
    report = run_milestone_33_boundary_final_closure()
    assert report["next_stage"] == NEXT_STAGE
    assert "MILESTONE_34_TASK_1" in report["next_stage"]

def test_task_6_doc_contains_required_markers():
    write_milestone_33_task_6_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_33_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_33_TASK_6_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_33_TASK_6_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_33_boundary_final_closure_report(run_milestone_33_boundary_final_closure())
