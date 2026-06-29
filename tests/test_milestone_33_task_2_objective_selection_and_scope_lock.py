from hbce_arc_agi3.milestone_33_objective_scope_lock import (
    DOC_PATH,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    TASK_ID,
    run_milestone_33_objective_scope_lock,
    validate_milestone_33_objective_scope_lock_report,
    write_milestone_33_task_2_artifacts,
)


def test_task_2_identity_markers_are_stable():
    report = run_milestone_33_objective_scope_lock()

    assert report["task_id"] == TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID


def test_task_2_source_task_1_dependency_is_valid():
    report = run_milestone_33_objective_scope_lock()

    assert report["source_opening_status"] == "READY"
    assert report["source_opening_passed"] is True


def test_task_2_pass_fail_accounting_is_closed():
    report = run_milestone_33_objective_scope_lock()

    assert report["scope_lock_case_count"] == 12
    assert report["pass_count"] == 12
    assert report["fail_count"] == 0
    assert report["scope_lock_passed"] is True


def test_task_2_next_stage_points_to_task_3_implementation():
    report = run_milestone_33_objective_scope_lock()

    assert report["next_stage"] == NEXT_STAGE
    assert "TASK_3" in report["next_stage"]
    assert "IMPLEMENTATION" in report["next_stage"]


def test_task_2_doc_contains_required_markers():
    write_milestone_33_task_2_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")

    assert "MILESTONE_33_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in text
    assert "MILESTONE_33_TASK_2_SCOPE_LOCK_STATUS=LOCKED" in text
    assert "MILESTONE_33_TASK_2_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_33_TASK_2_KAGGLE_SCORE_CLAIM=false" in text
    assert validate_milestone_33_objective_scope_lock_report(run_milestone_33_objective_scope_lock())
