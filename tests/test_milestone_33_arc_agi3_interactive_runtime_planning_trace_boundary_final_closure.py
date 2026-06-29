from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_final_closure import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    run_milestone_33_boundary_final_closure,
    validate_milestone_33_boundary_final_closure_report,
    write_milestone_33_task_6_artifacts,
)

def test_milestone_33_final_closure_identity_matches_scope():
    report = run_milestone_33_boundary_final_closure()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["closure_status"] == "CLOSED"

def test_milestone_33_final_closure_source_integration_is_valid():
    report = run_milestone_33_boundary_final_closure()
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True
    assert report["source_integration_report"]["_integration_report_valid"] is True

def test_milestone_33_final_closure_preserves_regression_and_claim_denial():
    report = run_milestone_33_boundary_final_closure()
    assert report["regression_event_count"] == 4
    assert report["regression_event_trace_fingerprint"]
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False

def test_milestone_33_final_closure_case_accounting_is_closed():
    report = run_milestone_33_boundary_final_closure()
    assert report["closure_case_count"] == 16
    assert report["pass_count"] == 16
    assert report["fail_count"] == 0
    assert report["closure_passed"] is True
    assert validate_milestone_33_boundary_final_closure_report(report)

def test_milestone_33_final_closure_rejects_claim_drift():
    report = run_milestone_33_boundary_final_closure()
    report["kaggle_score_claim"] = True
    assert not validate_milestone_33_boundary_final_closure_report(report)

def test_milestone_33_task_6_artifacts_and_doc_are_written():
    artifacts = write_milestone_33_task_6_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_33_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_PLANNING_TRACE_BOUNDARY_FINAL_CLOSURE_READY=true" in text
    assert "MILESTONE_33_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_33_TASK_6_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_33_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text
