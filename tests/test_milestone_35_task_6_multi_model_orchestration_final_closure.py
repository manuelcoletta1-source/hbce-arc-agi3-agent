from hbce_arc_agi3.milestone_35_multi_model_orchestration_final_closure import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_35_multi_model_orchestration_final_closure,
    validate_milestone_35_multi_model_orchestration_final_closure_report,
    write_milestone_35_task_6_artifacts,
)


def test_task_6_identity_and_source_integration_are_stable():
    report = run_milestone_35_multi_model_orchestration_final_closure()
    assert report["task_id"] == TASK_ID
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True


def test_task_6_boundary_parts_are_closed():
    report = run_milestone_35_multi_model_orchestration_final_closure()
    assert report["multi_model_orchestration_boundary"] is True
    assert report["replayable_event_trace_required"] is True
    assert report["local_evaluation_record_required"] is True
    assert report["regression_snapshot_required"] is True
    assert report["audit_artifact_required"] is True


def test_task_6_pass_fail_accounting_is_closed():
    report = run_milestone_35_multi_model_orchestration_final_closure()
    assert report["closure_case_count"] == 16
    assert report["pass_count"] == 16
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True
    assert report["closure_status"] == "CLOSED"


def test_task_6_next_stage_points_to_milestone_35_opening():
    report = run_milestone_35_multi_model_orchestration_final_closure()
    assert report["next_stage"] == NEXT_STAGE
    assert "MILESTONE_36_TASK_1" in report["next_stage"]
    assert "GOVERNED_OPENING" in report["next_stage"]


def test_task_6_doc_contains_required_markers():
    write_milestone_35_task_6_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_35_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_MULTI_MODEL_ORCHESTRATION_BOUNDARY_FINAL_CLOSURE_READY=true" in text
    assert "MILESTONE_35_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_35_TASK_6_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_35_TASK_6_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_35_multi_model_orchestration_final_closure_report(
        run_milestone_35_multi_model_orchestration_final_closure()
    )
