from hbce_arc_agi3.milestone_38_kaggle_competitive_agent_productization import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_replay_evaluation_record,
    run_milestone_38_kaggle_competitive_agent_productization_implementation,
    validate_milestone_38_kaggle_competitive_agent_productization_report,
    validate_replay_evaluation_record,
    write_milestone_38_task_3_artifacts,
)


def test_replay_harness_identity_matches_scope():
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_status"] == "READY"


def test_replay_evaluation_record_validates():
    record = build_replay_evaluation_record()
    assert validate_replay_evaluation_record(record)
    assert record["local_evaluation_record"]["evaluation_status"] == "READY"
    assert record["regression_snapshot"]["source_runtime_event_count"] == 4
    assert record["audit_artifact"]["audit_id"]


def test_replay_harness_denies_claims_and_side_effects():
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    assert report["technical_evaluation_only"] is True
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["official_benchmark_certification"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_replay_harness_case_accounting():
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    assert report["implementation_case_count"] == 14
    assert report["pass_count"] == 14
    assert report["fail_count"] == 0
    assert report["implementation_passed"] is True
    assert validate_milestone_38_kaggle_competitive_agent_productization_report(report)


def test_replay_harness_rejects_kaggle_claim_drift():
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    report["kaggle_score_claim"] = True
    assert not validate_milestone_38_kaggle_competitive_agent_productization_report(report)


def test_task_3_artifacts_and_doc_are_written():
    artifacts = write_milestone_38_task_3_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_38_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_38_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_38_TASK_3_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_38_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text
