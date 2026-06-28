from pathlib import Path
import json

from hbce_arc_agi3.milestone_30_identity_boundary_fail_closed_regression_integration import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    INTEGRATION_CASE_COUNT,
    NEXT_STAGE,
    REGRESSION_INTEGRATION_REVISION,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_validation_snapshot,
    run_identity_boundary_fail_closed_regression_integration,
    task_5_signature,
    validate_identity_boundary_regression_integration_report,
    validate_validation_snapshot,
    write_task_5_artifacts,
)


def test_milestone_30_identity_boundary_regression_validation_snapshot_is_valid():
    snapshot = build_validation_snapshot()

    assert validate_validation_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["source_implementation_status"] == "READY"
    assert snapshot["source_implementation_complete"] is True
    assert snapshot["source_runtime_cases_valid"] is True
    assert snapshot["source_private_core_access_allowed_without_verified_manuel"] is False
    assert snapshot["source_unverified_manuel_assumption_allowed"] is False
    assert snapshot["source_external_command_authority_allowed"] is False
    assert snapshot["validation_status"] == "VALID"
    assert snapshot["validation_case_count"] == 9
    assert snapshot["pass_count"] == 9
    assert snapshot["fail_count"] == 0
    assert snapshot["stable_validation"] is True


def test_milestone_30_identity_boundary_regression_integration_report_is_valid():
    report = run_identity_boundary_fail_closed_regression_integration()

    assert validate_identity_boundary_regression_integration_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["regression_integration_revision"] == REGRESSION_INTEGRATION_REVISION
    assert report["task_5_signature"] == task_5_signature()
    assert report["source_validation_status"] == "VALID"
    assert report["source_validation_passed"] is True
    assert report["source_private_core_access_allowed_without_verified_manuel"] is False
    assert report["source_unverified_manuel_assumption_allowed"] is False
    assert report["source_external_command_authority_allowed"] is False
    assert report["integration_status"] == "VALID"
    assert report["integration_case_count"] == INTEGRATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_30_identity_boundary_regression_cases_cover_required_surface():
    report = run_identity_boundary_fail_closed_regression_integration()
    case_ids = {case["case_id"] for case in report["integration_cases"]}

    assert case_ids == {
        "TASK_4_VALIDATION_REPORT_VALID",
        "TASK_4_VALIDATION_RUNTIME_STABILITY_VALID",
        "TASK_4_VALIDATION_ARTIFACT_SET_PRESENT",
        "TASK_4_VALIDATION_MANIFEST_CONSISTENCY_VALID",
        "TASK_4_VALIDATION_CASE_SET_VALID",
        "IDENTITY_BOUNDARY_DIRECT_REGRESSION_PROBES_VALID",
        "TASK_3_SOURCE_IMPLEMENTATION_REMAINS_VALID",
        "TASK_2_SCOPE_LOCK_GUARDRAILS_REMAIN_VALID",
        "TASK_5_TRANSITION_AND_BUDGET_VALID",
    }
    assert all(case["passed"] is True for case in report["integration_cases"])
    assert all(case["failure_reason"] == "NONE" for case in report["integration_cases"])


def test_milestone_30_identity_boundary_regression_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_5_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_5_signature"] == task_5_signature()
    assert artifacts["manifest"]["integration_status"] == "VALID"
    assert artifacts["manifest"]["integration_passed"] is True
    assert artifacts["manifest"]["integration_case_count"] == INTEGRATION_CASE_COUNT
    assert artifacts["manifest"]["pass_count"] == REQUIRED_PASS_COUNT
    assert artifacts["manifest"]["fail_count"] == REQUIRED_FAIL_COUNT
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-5-regression-integration-report.json"
    markdown_path = Path(tmp_path) / "task-5-regression-integration-report.md"
    cases_path = Path(tmp_path) / "task-5-regression-integration-cases.json"
    manifest_path = Path(tmp_path) / "task-5-manifest.json"
    index_path = Path(tmp_path) / "task-5-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_identity_boundary_regression_integration_report(report)
    assert "MILESTONE_30_TASK_5_IDENTITY_BOUNDARY_FAIL_CLOSED_REGRESSION_INTEGRATION_READY=true" in index_path.read_text(encoding="utf-8")
