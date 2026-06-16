from pathlib import Path

from hbce_arc_agi3.milestone_13_solver_capability_gap_audit import (
    AUDIT_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_gap_audit_package,
    build_solver_capability_gap_audit_record,
    validate_solver_capability_gap_audit_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "boundary_verdict": "MILESTONE_13_OPENED_CANONICALLY_REAL_EVALUATION_PREP_ALLOWED_REAL_SUBMISSION_BLOCKED",
        "milestone_13_status": "OPENED_CANONICALLY",
        "next_stage": "MILESTONE_13_TASK_2_SOLVER_CAPABILITY_GAP_AUDIT_V1",
        "real_evaluation_prep_allowed": True,
        "local_solver_improvement_allowed": True,
        "solver_capability_gap_audit_allowed": True,
        "real_submission_allowed": False,
        "kaggle_authentication_allowed": False,
    }


def test_solver_capability_gap_audit_record_is_valid():
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["audit_verdict"] == AUDIT_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_boundary_passed"] is True
    assert record["solver_capability_gap_audit_ready"] is True
    assert record["solver_capability_gap_audit_valid"] is True
    assert record["solver_capability_gap_audit_passed"] is True
    assert record["capability_area_count"] == 12
    assert record["gap_count"] == 6
    assert record["high_priority_gap_count"] == 5
    assert record["priority_plan_step_count"] == 6
    assert record["top_priority"] == "TRANSFORMATION_PRIMITIVE_EXPANSION"
    assert record["real_evaluation_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_solver_capability_gap_audit_record(record) == []


def test_gap_audit_package_has_expected_gap_shape():
    package = build_gap_audit_package(_sample_source_record())

    assert package["capability_area_count"] == 12
    assert package["gap_count"] == 6
    assert package["high_priority_gap_count"] == 5
    assert package["priority_plan_step_count"] == 6
    assert package["measurement_target_count"] == 10
    assert package["priority_plan"][0] == "TRANSFORMATION_PRIMITIVE_EXPANSION"


def test_solver_capability_gap_audit_blocks_real_evaluation():
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")
    record["real_evaluation_performed"] = True

    issues = validate_solver_capability_gap_audit_record(record)

    assert "real_evaluation_performed_NOT_FALSE" in issues


def test_solver_capability_gap_audit_blocks_kaggle_authentication():
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")
    record["kaggle_authentication_allowed"] = True

    issues = validate_solver_capability_gap_audit_record(record)

    assert "kaggle_authentication_allowed_NOT_FALSE" in issues


def test_solver_capability_gap_audit_blocks_real_submission():
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_solver_capability_gap_audit_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_solver_capability_gap_audit_fails_if_gap_count_mutated():
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")
    record["gap_count"] = 5

    issues = validate_solver_capability_gap_audit_record(record)

    assert "GAP_COUNT_MISMATCH" in issues


def test_solver_capability_gap_audit_artifacts_are_written(tmp_path: Path):
    record = build_solver_capability_gap_audit_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-solver-capability-gap-audit-v1.json" in written_files
    assert "milestone-13-solver-capability-gap-audit-index-v1.json" in written_files
    assert "milestone-13-solver-capability-gap-audit-manifest-v1.txt" in written_files
    assert "milestone-13-solver-capability-gap-audit-v1.md" in written_files
