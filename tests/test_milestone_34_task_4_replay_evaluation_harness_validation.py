from hbce_arc_agi3.milestone_34_replay_evaluation_harness_validation import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_34_replay_evaluation_harness_validation,
    validate_milestone_34_replay_evaluation_harness_validation_report,
    write_milestone_34_task_4_artifacts,
)


def test_task_4_identity_and_source_implementation_are_stable():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["task_id"] == TASK_ID
    assert report["source_implementation_status"] == "READY"
    assert report["source_implementation_passed"] is True


def test_task_4_boundary_parts_are_validated():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["replay_evaluation_harness_boundary"] is True
    assert report["replayable_event_trace_required"] is True
    assert report["local_evaluation_record_required"] is True
    assert report["regression_snapshot_required"] is True
    assert report["audit_artifact_required"] is True


def test_task_4_pass_fail_accounting_is_closed():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["validation_case_count"] == 17
    assert report["pass_count"] == 17
    assert report["fail_count"] == 0
    assert report["validation_passed"] is True


def test_task_4_next_stage_points_to_regression_integration():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["next_stage"] == NEXT_STAGE
    assert "TASK_5" in report["next_stage"]
    assert "REGRESSION_INTEGRATION" in report["next_stage"]


def test_task_4_doc_contains_required_markers():
    write_milestone_34_task_4_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_34_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_REPLAY_EVALUATION_HARNESS_BOUNDARY_VALIDATION_READY=true" in text
    assert "MILESTONE_34_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_34_TASK_4_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_34_TASK_4_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_34_replay_evaluation_harness_validation_report(
        run_milestone_34_replay_evaluation_harness_validation()
    )
