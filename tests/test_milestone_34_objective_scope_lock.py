from hbce_arc_agi3.milestone_34_objective_scope_lock import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    run_milestone_34_objective_scope_lock,
    validate_milestone_34_objective_scope_lock_report,
    write_milestone_34_task_2_artifacts,
)

def test_milestone_34_objective_candidate_selected_and_locked():
    report = run_milestone_34_objective_scope_lock()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["scope_lock_status"] == "LOCKED"

def test_milestone_34_replay_harness_boundary_invariants():
    report = run_milestone_34_objective_scope_lock()
    assert report["replay_evaluation_harness_boundary"] is True
    assert report["replayable_event_trace_required"] is True
    assert report["local_evaluation_record_required"] is True
    assert report["regression_snapshot_required"] is True
    assert report["audit_artifact_required"] is True
    assert report["technical_evaluation_only"] is True
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["official_benchmark_certification"] is False

def test_milestone_34_scope_lock_case_accounting():
    report = run_milestone_34_objective_scope_lock()
    assert report["scope_lock_case_count"] == 12
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["scope_lock_passed"] is True
    assert validate_milestone_34_objective_scope_lock_report(report)

def test_milestone_34_validation_rejects_kaggle_claim_drift():
    report = run_milestone_34_objective_scope_lock()
    report["kaggle_score_claim"] = True
    assert not validate_milestone_34_objective_scope_lock_report(report)

def test_milestone_34_task_2_artifacts_and_doc_are_written():
    artifacts = write_milestone_34_task_2_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_34_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_34_TASK_2_SCOPE_LOCK_STATUS=LOCKED" in text
    assert "MILESTONE_34_TASK_2_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_34_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text
