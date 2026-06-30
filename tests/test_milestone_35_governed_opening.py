from hbce_arc_agi3.milestone_35_governed_opening import (
    DOC_PATH,
    NEXT_STAGE,
    TASK_ID,
    run_milestone_35_governed_opening,
    validate_milestone_35_governed_opening_report,
    write_milestone_34_task_1_artifacts,
)

def test_milestone_34_opening_identity_and_source_closure():
    report = run_milestone_35_governed_opening()
    assert report["task_id"] == TASK_ID
    assert report["source_closure_status"] == "CLOSED"
    assert report["source_closure_passed"] is True
    assert report["opening_status"] == "READY"

def test_milestone_34_task_budget_and_next_stage():
    report = run_milestone_35_governed_opening()
    assert report["task_budget_max"] == 8
    assert report["current_task_number"] == 1
    assert report["next_stage"] == NEXT_STAGE

def test_milestone_34_opening_case_accounting():
    report = run_milestone_35_governed_opening()
    assert report["opening_case_count"] == 8
    assert report["pass_count"] == 8
    assert report["fail_count"] == 0
    assert report["opening_passed"] is True
    assert validate_milestone_35_governed_opening_report(report)

def test_milestone_34_validation_rejects_budget_drift():
    report = run_milestone_35_governed_opening()
    report["task_budget_max"] = 9
    assert not validate_milestone_35_governed_opening_report(report)

def test_milestone_34_task_1_artifacts_and_doc_are_written():
    artifacts = write_milestone_34_task_1_artifacts()
    assert len([key for key in artifacts if key != "doc"]) == 5
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "MILESTONE_35_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in text
    assert "MILESTONE_35_TASK_1_OPENING_STATUS=READY" in text
    assert f"MILESTONE_35_TASK_1_NEXT_STAGE={NEXT_STAGE}" in text
