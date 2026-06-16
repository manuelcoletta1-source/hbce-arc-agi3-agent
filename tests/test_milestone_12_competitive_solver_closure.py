from pathlib import Path

from hbce_arc_agi3.milestone_12_competitive_solver_closure import (
    CLOSURE_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_closure_package,
    build_competitive_solver_closure_record,
    validate_competitive_solver_closure_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "submission_readiness_gate_ready": True,
        "submission_readiness_gate_passed": True,
        "readiness_verdict": "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED",
        "required_source_artifact_count": 4,
        "required_source_artifact_present_count": 4,
        "source_guard_case_count": 6,
        "source_guard_pass_count": 6,
        "source_public_overfit_violation_count": 0,
        "source_boundary_violation_count": 0,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "manual_upload_allowed": False,
        "operator_approval_required": True,
        "operator_approval_received": False,
    }


def test_competitive_solver_closure_record_is_valid():
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["closure_verdict"] == CLOSURE_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_12_status"] == "CLOSED"
    assert record["milestone_12_closure_ready"] is True
    assert record["milestone_12_closure_valid"] is True
    assert record["milestone_12_closure_passed"] is True
    assert record["required_chain_artifact_count"] == 12
    assert record["required_chain_artifact_present_count"] == 12
    assert record["required_chain_artifact_parseable_count"] == 12
    assert record["source_readiness_verdict"] == "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED"
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["manual_upload_allowed"] is False
    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False
    assert record["milestone_13_opened"] is False
    assert record["milestone_13_opening_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_competitive_solver_closure_record(record) == []


def test_closure_package_summarizes_source_record():
    package = build_closure_package(_sample_source_record())

    assert package["required_chain_artifact_count"] == 12
    assert package["source_submission_readiness_gate_passed"] is True
    assert package["source_readiness_verdict"] == "LOCAL_READINESS_PACKAGE_READY_REAL_SUBMISSION_BLOCKED"
    assert package["source_real_submission_allowed"] is False
    assert package["source_ready_for_real_kaggle_submission"] is False
    assert package["source_operator_approval_required"] is True
    assert package["source_operator_approval_received"] is False
    assert package["measurement_target_count"] == 10


def test_competitive_solver_closure_blocks_real_submission():
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_competitive_solver_closure_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_competitive_solver_closure_blocks_milestone_13_auto_opening():
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")
    record["milestone_13_opened"] = True

    issues = validate_competitive_solver_closure_record(record)

    assert "milestone_13_opened_NOT_FALSE" in issues


def test_competitive_solver_closure_requires_operator_approval_but_not_received():
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")

    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False


def test_competitive_solver_closure_fails_if_chain_count_mutated():
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")
    record["required_chain_artifact_present_count"] = 11

    issues = validate_competitive_solver_closure_record(record)

    assert "REQUIRED_CHAIN_ARTIFACT_PRESENT_COUNT_MISMATCH" in issues


def test_competitive_solver_closure_artifacts_are_written(tmp_path: Path):
    record = build_competitive_solver_closure_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-competitive-solver-closure-v1.json" in written_files
    assert "milestone-12-competitive-solver-closure-index-v1.json" in written_files
    assert "milestone-12-competitive-solver-closure-manifest-v1.txt" in written_files
    assert "milestone-12-competitive-solver-closure-v1.md" in written_files
