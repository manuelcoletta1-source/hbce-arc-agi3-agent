from pathlib import Path

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run_review import (
    NEXT_STAGE,
    SOURCE_TASK,
    TASK_NAME,
    TASK_VERDICT,
    build_dry_run_review_record,
    validate_dry_run_review_record,
    write_artifacts,
)


def test_dry_run_review_record_is_valid():
    record = build_dry_run_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["source_task"] == SOURCE_TASK
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["dry_run_review_ready"] is True
    assert record["dry_run_review_valid"] is True
    assert record["dry_run_review_passed"] is True
    assert record["source_dry_run_valid"] is True
    assert record["source_dry_run_completed"] is True
    assert record["controlled_runtime_wiring_execution_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 25
    assert record["issue_count"] == 0
    assert validate_dry_run_review_record(record) == []


def test_dry_run_review_fails_closed_when_runtime_wiring_is_marked_real():
    record = build_dry_run_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_performed"] = True

    issues = validate_dry_run_review_record(record)

    assert "runtime_wiring_performed_NOT_FALSE" in issues


def test_dry_run_review_fails_closed_when_review_finding_fails():
    record = build_dry_run_review_record(baseline_commit="TEST-COMMIT")
    record["review_findings"][0]["status"] = False

    issues = validate_dry_run_review_record(record)

    assert "REVIEW_FINDING_FAILED" in issues


def test_dry_run_review_artifacts_are_written(tmp_path: Path):
    record = build_dry_run_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-dry-run-review-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-dry-run-review-index-v1.json" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-dry-run-review-manifest-v1.txt" in written_files
    assert "milestone-11-local-solver-patch-helper-controlled-runtime-wiring-dry-run-review-v1.md" in written_files
