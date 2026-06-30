from hbce_arc_agi3.milestone_34_replay_evaluation_harness_validation import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_milestone_34_replay_evaluation_harness_validation_cases,
    run_milestone_34_replay_evaluation_harness_validation,
    validate_milestone_34_replay_evaluation_harness_validation_report,
    write_milestone_34_task_4_artifacts,
)


def test_validation_identity_matches_scope_and_source():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["source_implementation_status"] == "READY"
    assert report["source_implementation_passed"] is True


def test_validation_cases_all_pass():
    cases = build_milestone_34_replay_evaluation_harness_validation_cases()
    assert len(cases) == 17
    assert all(case["passed"] is True for case in cases)


def test_validation_preserves_replay_evidence_ids():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["replay_id"]
    assert report["local_evaluation_id"]
    assert report["regression_snapshot_id"]
    assert report["audit_id"]


def test_validation_denies_claims_and_side_effects():
    report = run_milestone_34_replay_evaluation_harness_validation()
    assert report["technical_evaluation_only"] is True
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["official_benchmark_certification"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_validation_rejects_kaggle_claim_drift():
    report = run_milestone_34_replay_evaluation_harness_validation()
    report["kaggle_score_claim"] = True
    assert not validate_milestone_34_replay_evaluation_harness_validation_report(report)


def test_validation_artifacts_and_doc_are_written():
    artifacts = write_milestone_34_task_4_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_34_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_34_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_34_TASK_4_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_34_TASK_4_NEXT_STAGE={NEXT_STAGE}" in text
