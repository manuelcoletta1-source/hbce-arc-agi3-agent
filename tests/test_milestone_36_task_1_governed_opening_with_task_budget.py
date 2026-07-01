from hbce_arc_agi3.milestone_36_governed_opening import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_36_governed_opening,
    validate_milestone_36_governed_opening_report,
    write_milestone_34_task_1_artifacts,
)

def test_task_1_identity_is_stable():
    report = run_milestone_36_governed_opening()
    assert report["task_id"] == TASK_ID
    assert report["milestone_id"] == "MILESTONE_36"

def test_task_1_objective_selection_is_pending_task_2():
    report = run_milestone_36_governed_opening()
    assert report["objective_selection_status"] == "PENDING_TASK_2_SCOPE_LOCK"
    assert report["next_stage"] == NEXT_STAGE

def test_task_1_doc_contains_required_markers():
    write_milestone_34_task_1_artifacts()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_36_TASK_1_OPENING_STATUS=READY" in text
    assert "MILESTONE_36_TASK_1_TASK_BUDGET_MAX=8" in text
    assert "MILESTONE_36_TASK_1_NEXT_STAGE=MILESTONE_36_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1" in text
    assert validate_milestone_36_governed_opening_report(run_milestone_36_governed_opening())
