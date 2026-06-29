from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_regression_integration import (
    DOC_PATH,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    run_milestone_33_boundary_regression_integration,
    validate_milestone_33_boundary_regression_integration_report,
    write_milestone_33_task_5_artifacts,
)


def test_milestone_33_regression_integration_identity_matches_validation():
    report = run_milestone_33_boundary_regression_integration()

    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["integration_status"] == "VALID"


def test_milestone_33_regression_source_validation_is_valid():
    report = run_milestone_33_boundary_regression_integration()

    assert report["source_validation_status"] == "VALID"
    assert report["source_validation_passed"] is True
    assert report["source_validation_report"]["_validation_report_valid"] is True


def test_milestone_33_regression_snapshot_is_stable():
    report = run_milestone_33_boundary_regression_integration()
    snapshot = report["regression_snapshot"]

    assert snapshot["event_count"] == 4
    assert snapshot["event_trace_fingerprint"]
    assert snapshot["action_ids"] == ["ACTION-001", "ACTION-002", "ACTION-003", "ACTION-004"]
    assert snapshot["observation_ids"] == ["OBSERVATION-001", "OBSERVATION-002", "OBSERVATION-003", "OBSERVATION-004"]
    assert snapshot["planning_step_ids"] == ["PLAN-001", "PLAN-002", "PLAN-003", "PLAN-004"]


def test_milestone_33_regression_denies_side_effects_and_claims():
    report = run_milestone_33_boundary_regression_integration()

    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_milestone_33_regression_case_accounting_is_closed():
    report = run_milestone_33_boundary_regression_integration()

    assert report["integration_case_count"] == 20
    assert report["pass_count"] == 20
    assert report["fail_count"] == 0
    assert report["integration_passed"] is True
    assert validate_milestone_33_boundary_regression_integration_report(report)


def test_milestone_33_regression_rejects_legal_certification_drift():
    report = run_milestone_33_boundary_regression_integration()
    report["legal_certification"] = True

    assert not validate_milestone_33_boundary_regression_integration_report(report)


def test_milestone_33_task_5_artifacts_and_doc_are_written():
    artifacts = write_milestone_33_task_5_artifacts()

    assert len([key for key in artifacts if key != "doc"]) == GENERATED_ARTIFACT_COUNT
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_33_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_33_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_33_TASK_5_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_33_TASK_5_NEXT_STAGE={NEXT_STAGE}" in text
