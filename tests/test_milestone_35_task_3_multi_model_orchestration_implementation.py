from hbce_arc_agi3.milestone_35_multi_model_orchestration import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_35_multi_model_orchestration_implementation,
    validate_milestone_35_multi_model_orchestration_report,
    write_milestone_35_task_3_artifacts,
)


def test_task_3_identity_and_source_scope_are_stable():
    report = run_milestone_35_multi_model_orchestration_implementation()
    assert report["task_id"] == TASK_ID
    assert report["source_scope_status"] == "LOCKED"
    assert report["source_scope_passed"] is True


def test_task_3_boundary_parts_are_implemented():
    report = run_milestone_35_multi_model_orchestration_implementation()
    assert report["multi_model_orchestration_boundary"] is True
    assert report["replayable_event_trace_required"] is True
    assert report["local_evaluation_record_required"] is True
    assert report["regression_snapshot_required"] is True
    assert report["audit_artifact_required"] is True


def test_task_3_pass_fail_accounting_is_closed():
    report = run_milestone_35_multi_model_orchestration_implementation()
    assert report["implementation_case_count"] == 14
    assert report["pass_count"] == 14
    assert report["fail_count"] == 0
    assert report["implementation_passed"] is True


def test_task_3_next_stage_points_to_validation():
    report = run_milestone_35_multi_model_orchestration_implementation()
    assert report["next_stage"] == NEXT_STAGE
    assert "TASK_4" in report["next_stage"]
    assert "VALIDATION" in report["next_stage"]


def test_task_3_doc_contains_required_markers():
    write_milestone_35_task_3_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_35_TASK_3_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_MULTI_MODEL_ORCHESTRATION_BOUNDARY_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_35_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_35_TASK_3_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_35_TASK_3_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_35_multi_model_orchestration_report(
        run_milestone_35_multi_model_orchestration_implementation()
    )
