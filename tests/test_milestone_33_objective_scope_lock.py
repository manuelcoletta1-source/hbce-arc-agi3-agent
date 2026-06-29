from hbce_arc_agi3.milestone_33_objective_scope_lock import (
    DOC_PATH,
    GENERATED_ARTIFACT_COUNT,
    LEGAL_CERTIFICATION,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    build_milestone_33_objective_scope_lock_cases,
    run_milestone_33_objective_scope_lock,
    validate_milestone_33_objective_scope_lock_report,
    write_milestone_33_task_2_artifacts,
)


def test_milestone_33_objective_candidate_is_selected_and_locked():
    report = run_milestone_33_objective_scope_lock()

    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["selected_objective_status"] == "SELECTED_AND_SCOPE_LOCKED"
    assert report["scope_lock_status"] == "LOCKED"


def test_milestone_33_arc_agi3_interactive_runtime_boundary_invariants_hold():
    report = run_milestone_33_objective_scope_lock()

    assert report["arc_agi3_interactive_runtime_boundary"] is True
    assert report["planning_trace_required"] is True
    assert report["action_observation_event_trace_required"] is True
    assert report["goal_inference_boundary_required"] is True
    assert report["memory_state_boundary_required"] is True
    assert report["technical_trace_artifact_only"] is True
    assert report["legal_certification"] is LEGAL_CERTIFICATION is False
    assert report["kaggle_score_claim"] is False


def test_milestone_33_scope_lock_cases_all_pass():
    report = run_milestone_33_objective_scope_lock()
    cases = build_milestone_33_objective_scope_lock_cases(report)

    assert len(cases) == report["scope_lock_case_count"]
    assert all(case["passed"] for case in cases)
    assert report["pass_count"] == len(cases)
    assert report["fail_count"] == 0
    assert report["scope_lock_passed"] is True


def test_milestone_33_scope_lock_report_validates():
    report = run_milestone_33_objective_scope_lock()

    assert validate_milestone_33_objective_scope_lock_report(report)


def test_milestone_33_scope_lock_validation_rejects_legal_certification_drift():
    report = run_milestone_33_objective_scope_lock()
    report["legal_certification"] = True

    assert not validate_milestone_33_objective_scope_lock_report(report)


def test_milestone_33_task_2_artifacts_and_doc_are_written():
    artifacts = write_milestone_33_task_2_artifacts()

    assert len([key for key in artifacts if key != "doc"]) == GENERATED_ARTIFACT_COUNT
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_33_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_33_TASK_2_SCOPE_LOCK_STATUS=LOCKED" in text
    assert f"MILESTONE_33_TASK_2_NEXT_STAGE={NEXT_STAGE}" in text
