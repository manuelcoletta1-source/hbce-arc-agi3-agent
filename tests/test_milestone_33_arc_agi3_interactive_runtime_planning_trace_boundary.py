from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary import (
    DOC_PATH,
    GENERATED_ARTIFACT_COUNT,
    KAGGLE_SCORE_CLAIM,
    LEGAL_CERTIFICATION,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_sample_interactive_runtime_episode,
    run_milestone_33_boundary_implementation,
    validate_interactive_runtime_episode,
    validate_milestone_33_boundary_implementation_report,
    write_milestone_33_task_3_artifacts,
)


def test_milestone_33_boundary_identity_matches_scope_lock():
    report = run_milestone_33_boundary_implementation()

    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["implementation_status"] == "READY"


def test_milestone_33_sample_episode_has_required_trace_parts():
    episode = build_sample_interactive_runtime_episode()

    assert validate_interactive_runtime_episode(episode)
    assert episode["event_count"] == 4
    for event in episode["events"]:
        assert event["action_id"]
        assert event["observation_id"]
        assert event["planning_step_id"]
        assert event["goal_hypothesis"]
        assert event["memory_state_digest"]


def test_milestone_33_boundary_denies_unsafe_runtime_claims():
    report = run_milestone_33_boundary_implementation()
    episode = report["sample_episode"]

    assert report["technical_trace_artifact_only"] is True
    assert report["legal_certification"] is LEGAL_CERTIFICATION is False
    assert report["kaggle_score_claim"] is KAGGLE_SCORE_CLAIM is False
    assert episode["network_access_allowed"] is False
    assert episode["shell_execution_allowed"] is False
    assert episode["repository_mutation_allowed"] is False


def test_milestone_33_boundary_report_validates():
    report = run_milestone_33_boundary_implementation()

    assert report["implementation_case_count"] == 14
    assert report["pass_count"] == 14
    assert report["fail_count"] == 0
    assert report["implementation_passed"] is True
    assert validate_milestone_33_boundary_implementation_report(report)


def test_milestone_33_validation_rejects_kaggle_score_claim_drift():
    report = run_milestone_33_boundary_implementation()
    report["kaggle_score_claim"] = True

    assert not validate_milestone_33_boundary_implementation_report(report)


def test_milestone_33_task_3_artifacts_and_doc_are_written():
    artifacts = write_milestone_33_task_3_artifacts()

    assert len([key for key in artifacts if key != "doc"]) == GENERATED_ARTIFACT_COUNT
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_33_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_33_TASK_3_IMPLEMENTATION_STATUS=READY" in text
    assert "MILESTONE_33_TASK_3_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_33_TASK_3_NEXT_STAGE={NEXT_STAGE}" in text
