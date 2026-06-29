from hbce_arc_agi3.milestone_33_arc_agi3_interactive_runtime_planning_trace_boundary_validation import (
    DOC_PATH,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SELECTED_OBJECTIVE_ID,
    SCOPE_LOCK_ID,
    run_milestone_33_boundary_validation,
    validate_milestone_33_boundary_validation_report,
    write_milestone_33_task_4_artifacts,
)


def test_milestone_33_validation_identity_matches_implementation():
    report = run_milestone_33_boundary_validation()

    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_status"] == "VALID"


def test_milestone_33_validation_source_implementation_is_valid():
    report = run_milestone_33_boundary_validation()

    assert report["source_implementation_status"] == "READY"
    assert report["source_implementation_passed"] is True
    assert report["source_implementation_report"]["_implementation_report_valid"] is True


def test_milestone_33_validation_runtime_boundaries_remain_denied():
    report = run_milestone_33_boundary_validation()

    assert report["legal_certification"] is False
    assert report["kaggle_score_claim"] is False
    assert report["network_access_allowed"] is False
    assert report["shell_execution_allowed"] is False
    assert report["repository_mutation_allowed"] is False


def test_milestone_33_validation_case_accounting_is_closed():
    report = run_milestone_33_boundary_validation()

    assert report["validation_case_count"] == 16
    assert report["pass_count"] == 16
    assert report["fail_count"] == 0
    assert report["validation_passed"] is True
    assert validate_milestone_33_boundary_validation_report(report)


def test_milestone_33_validation_rejects_kaggle_claim_drift():
    report = run_milestone_33_boundary_validation()
    report["kaggle_score_claim"] = True

    assert not validate_milestone_33_boundary_validation_report(report)


def test_milestone_33_task_4_artifacts_and_doc_are_written():
    artifacts = write_milestone_33_task_4_artifacts()

    assert len([key for key in artifacts if key != "doc"]) == GENERATED_ARTIFACT_COUNT
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    assert f"MILESTONE_33_TASK_4_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}" in text
    assert "MILESTONE_33_TASK_4_VALIDATION_STATUS=VALID" in text
    assert "MILESTONE_33_TASK_4_KAGGLE_SCORE_CLAIM=false" in text
    assert f"MILESTONE_33_TASK_4_NEXT_STAGE={NEXT_STAGE}" in text
