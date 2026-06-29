from hbce_arc_agi3.milestone_32_hbce_ipr_runtime_api_boundary import (
    BOUNDARY_MODE_ID,
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    IMPLEMENTATION_CASE_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_SCOPE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_operational_identity_proof_layer,
    run_milestone_32_boundary_implementation,
    task_3_signature,
    validate_milestone_32_boundary_implementation_report,
    validate_operational_identity_proof_layer,
    write_task_3_artifacts,
)


def test_milestone_32_boundary_implementation_report_is_valid():
    report = run_milestone_32_boundary_implementation()

    assert validate_milestone_32_boundary_implementation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_scope_task_id"] == SOURCE_SCOPE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["boundary_mode_id"] == BOUNDARY_MODE_ID
    assert report["task_3_signature"] == task_3_signature()
    assert report["implementation_status"] == "READY"
    assert report["implementation_case_count"] == IMPLEMENTATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["implementation_passed"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_operational_identity_proof_layer_accepts_complete_links():
    layer = build_operational_identity_proof_layer(
        operational_subject_id="SUBJECT",
        governed_session_id="SESSION",
        event_trace_id="EVT",
        technical_proof_receipt_id="OPC",
        audit_record_id="AUDIT",
        model_usage_record_id="USAGE",
    )

    assert validate_operational_identity_proof_layer(layer)
    assert layer["proof_layer_status"] == "READY"
    assert layer["missing_required_links"] == []


def test_operational_identity_proof_layer_blocks_missing_required_link():
    layer = build_operational_identity_proof_layer(
        operational_subject_id="SUBJECT",
        governed_session_id="",
        event_trace_id="EVT",
        technical_proof_receipt_id="OPC",
        audit_record_id="AUDIT",
        model_usage_record_id="USAGE",
    )

    assert not validate_operational_identity_proof_layer(layer)
    assert layer["proof_layer_status"] == "BLOCKED"
    assert "governed_session" in layer["missing_required_links"]


def test_boundary_flags_are_fail_closed():
    report = run_milestone_32_boundary_implementation()
    layer = report["sample_proof_layer"]

    assert layer["opc_technical_proof_receipt_only"] is True
    assert layer["legal_certification"] is False
    assert layer["ipr_card_internal_operational_identity_certificate"] is True
    assert layer["ipr_card_official_public_identity_document"] is False
    assert layer["explicit_legal_boundary_required"] is True


def test_milestone_32_boundary_implementation_cases_are_all_passed():
    report = run_milestone_32_boundary_implementation()

    assert len(report["implementation_cases"]) == IMPLEMENTATION_CASE_COUNT
    assert all(case["passed"] is True for case in report["implementation_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["implementation_cases"])


def test_milestone_32_boundary_implementation_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_3_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_scope_task_id"] == SOURCE_SCOPE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["boundary_mode_id"] == BOUNDARY_MODE_ID
    assert artifacts["manifest"]["task_3_signature"] == task_3_signature()
    assert artifacts["manifest"]["implementation_status"] == "READY"
    assert artifacts["manifest"]["implementation_passed"] is True
    assert artifacts["manifest"]["implementation_case_count"] == IMPLEMENTATION_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE


def test_milestone_32_boundary_implementation_rejects_mutated_report():
    report = run_milestone_32_boundary_implementation()
    report["legal_certification"] = True

    assert not validate_milestone_32_boundary_implementation_report(report)
