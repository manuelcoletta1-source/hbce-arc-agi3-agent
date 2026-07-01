from hbce_arc_agi3.milestone_36_runtime_model_routing_final_closure import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_milestone_36_runtime_model_routing_final_closure_cases,
    run_milestone_36_runtime_model_routing_final_closure,
    validate_milestone_36_runtime_model_routing_final_closure_report,
    write_milestone_36_task_6_artifacts,
)


def test_final_closure_identity_matches_scope_and_integration():
    report = run_milestone_36_runtime_model_routing_final_closure()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["source_integration_status"] == "VALID"
    assert report["source_integration_passed"] is True


def test_final_closure_cases_all_pass():
    cases = build_milestone_36_runtime_model_routing_final_closure_cases()
    assert len(cases) == 16
    assert all(case["passed"] is True for case in cases)


def test_final_closure_preserves_regression_evidence():
    report = run_milestone_36_runtime_model_routing_final_closure()
    assert report["regression_event_count"] == 4
    assert report["regression_event_trace_fingerprint"]
    assert report["replay_id"]
    assert report["local_evaluation_id"]
    assert report["regression_snapshot_id"]
    assert report["audit_id"]


def test_final_closure_denies_claims_and_side_effects():
    report = run_milestone_36_runtime_model_routing_final_closure()
    assert report["technical_evaluation_only"] is True
    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["official_benchmark_certification"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_final_closure_rejects_kaggle_claim_drift():
    report = run_milestone_36_runtime_model_routing_final_closure()
    report["kaggle_score_claim"] = True
    assert not validate_milestone_36_runtime_model_routing_final_closure_report(report)


def test_final_closure_artifacts_and_doc_are_written():
    artifacts = write_milestone_36_task_6_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_36_TASK_6_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_36_TASK_6_CLOSURE_STATUS=CLOSED" in text
    assert "MILESTONE_36_TASK_6_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_36_TASK_6_NEXT_STAGE={NEXT_STAGE}" in text
