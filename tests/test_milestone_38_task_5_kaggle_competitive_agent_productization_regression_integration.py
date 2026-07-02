from hbce_arc_agi3.milestone_38_kaggle_competitive_agent_productization_regression_integration import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_38_kaggle_competitive_agent_productization_regression_integration,
    validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report,
    write_milestone_38_task_5_artifacts,
)


def test_task_5_identity_and_source_validation_are_stable():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["task_id"] == TASK_ID
    assert report["source_validation_status"] == "VALID"
    assert report["source_validation_passed"] is True


def test_task_5_regression_integration_parts_are_bound():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["kaggle_competitive_agent_productization_boundary"] is True
    assert report["replayable_event_trace_required"] is True
    assert report["local_evaluation_record_required"] is True
    assert report["regression_snapshot_required"] is True
    assert report["audit_artifact_required"] is True
    assert report["regression_event_count"] == 4


def test_task_5_pass_fail_accounting_is_closed():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["integration_case_count"] == 20
    assert report["pass_count"] == 20
    assert report["fail_count"] == 0
    assert report["integration_passed"] is True


def test_task_5_next_stage_points_to_final_closure():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["next_stage"] == NEXT_STAGE
    assert "TASK_6" in report["next_stage"]
    assert "FINAL_CLOSURE" in report["next_stage"]


def test_task_5_doc_contains_required_markers():
    write_milestone_38_task_5_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_38_TASK_5_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_REGRESSION_INTEGRATION_READY=true" in text
    assert "MILESTONE_38_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_38_TASK_5_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_38_TASK_5_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report(
        run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    )
