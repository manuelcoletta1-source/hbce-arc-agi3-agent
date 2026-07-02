from hbce_arc_agi3.milestone_38_kaggle_competitive_agent_productization_regression_integration import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_regression_event_trace,
    run_milestone_38_kaggle_competitive_agent_productization_regression_integration,
    validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report,
    write_milestone_38_task_5_artifacts,
)


def test_regression_integration_identity_matches_scope_and_validation():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["source_validation_status"] == "VALID"
    assert report["source_validation_passed"] is True


def test_regression_event_trace_is_bound():
    events = build_regression_event_trace()
    assert len(events) == 4
    assert {event["event_type"] for event in events} == {
        "source-validation-bound",
        "replay-record-bound",
        "regression-snapshot-bound",
        "audit-artifact-bound",
    }


def test_regression_integration_denies_claims_and_side_effects():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["technical_evaluation_only"] is True
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["official_benchmark_certification"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_regression_integration_case_accounting():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    assert report["integration_case_count"] == 20
    assert report["pass_count"] == 20
    assert report["fail_count"] == 0
    assert report["integration_passed"] is True
    assert validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report(report)


def test_regression_integration_rejects_official_benchmark_claim_drift():
    report = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    report["official_benchmark_certification"] = True
    assert not validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report(report)


def test_regression_integration_artifacts_and_doc_are_written():
    artifacts = write_milestone_38_task_5_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_38_TASK_5_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_38_TASK_5_INTEGRATION_STATUS=VALID" in text
    assert "MILESTONE_38_TASK_5_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_38_TASK_5_NEXT_STAGE={NEXT_STAGE}" in text
