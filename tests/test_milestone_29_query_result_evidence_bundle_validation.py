from pathlib import Path
import json

from hbce_arc_agi3.milestone_29_query_result_evidence_bundle_validation import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    REQUIRED_FAIL_COUNT,
    REQUIRED_PASS_COUNT,
    SCOPE_LOCK_ID,
    SELECTED_OBJECTIVE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    VALIDATION_CASE_COUNT,
    VALIDATION_REVISION,
    build_bundle_snapshot,
    run_query_result_evidence_bundle_validation,
    task_4_signature,
    validate_bundle_snapshot,
    validate_validation_report,
    write_task_4_artifacts,
)


def test_milestone_29_evidence_bundle_validation_snapshot_is_stable():
    snapshot = build_bundle_snapshot()

    assert validate_bundle_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["scope_lock_id"] == SCOPE_LOCK_ID
    assert snapshot["implementation_status"] == "READY"
    assert snapshot["implementation_complete"] is True
    assert snapshot["scope_lock_valid"] is True
    assert snapshot["source_chain_valid"] is True
    assert snapshot["evidence_valid"] is True
    assert snapshot["stable_bundle"] is True


def test_milestone_29_evidence_bundle_validation_report_is_valid():
    report = run_query_result_evidence_bundle_validation()

    assert validate_validation_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["validation_revision"] == VALIDATION_REVISION
    assert report["task_4_signature"] == task_4_signature()
    assert report["source_implementation_status"] == "READY"
    assert report["source_scope_lock_valid"] is True
    assert report["source_chain_valid"] is True
    assert report["source_evidence_valid"] is True
    assert report["validation_status"] == "VALID"
    assert report["validation_case_count"] == VALIDATION_CASE_COUNT
    assert report["pass_count"] == REQUIRED_PASS_COUNT
    assert report["fail_count"] == REQUIRED_FAIL_COUNT
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_29_evidence_bundle_validation_cases_cover_bundle_surface():
    report = run_query_result_evidence_bundle_validation()
    case_ids = {case["case_id"] for case in report["case_results"]}

    assert case_ids == {
        "TASK_3_EVIDENCE_BUNDLE_REPORT_VALID",
        "TASK_3_EVIDENCE_BUNDLE_RUNTIME_STABILITY_VALID",
        "TASK_3_EVIDENCE_BUNDLE_ARTIFACT_SET_PRESENT",
        "TASK_3_EVIDENCE_BUNDLE_MANIFEST_CONSISTENCY_VALID",
        "TASK_3_EVIDENCE_BUNDLE_INDEX_MARKERS_VALID",
        "TASK_3_EVIDENCE_INDEX_CONSISTENCY_VALID",
        "TASK_3_EVIDENCE_DIGESTS_VALID",
        "TASK_3_SOURCE_CHAIN_STATUS_VALID",
    }
    assert all(case["passed"] is True for case in report["case_results"])
    assert all(case["failure_reason"] == "NONE" for case in report["case_results"])


def test_milestone_29_evidence_bundle_validation_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_4_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["task_4_signature"] == task_4_signature()
    assert artifacts["manifest"]["validation_status"] == "VALID"
    assert artifacts["manifest"]["validation_passed"] is True
    assert artifacts["manifest"]["pass_count"] == 8
    assert artifacts["manifest"]["fail_count"] == 0
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-4-validation-report.json"
    markdown_path = Path(tmp_path) / "task-4-validation-report.md"
    cases_path = Path(tmp_path) / "task-4-validation-cases.json"
    manifest_path = Path(tmp_path) / "task-4-manifest.json"
    index_path = Path(tmp_path) / "task-4-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert cases_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_validation_report(report)
    assert "MILESTONE_29_TASK_4_QUERY_RESULT_EVIDENCE_BUNDLE_VALIDATION_READY=true" in index_path.read_text(encoding="utf-8")
