from pathlib import Path

from hbce_arc_agi3.milestone_12_submission_readiness_gate import (
    NEXT_STAGE,
    READINESS_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_readiness_package,
    build_submission_readiness_gate_record,
    validate_submission_readiness_gate_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "guard_case_count": 6,
        "guard_pass_count": 6,
        "public_overfit_violation_count": 0,
        "boundary_violation_count": 0,
        "forbidden_field_hit_count": 0,
        "forbidden_text_hit_count": 0,
        "score_claim_violation_count": 0,
        "submission_violation_count": 0,
    }


def test_submission_readiness_gate_record_is_valid():
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["readiness_verdict"] == READINESS_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["submission_readiness_gate_ready"] is True
    assert record["submission_readiness_gate_valid"] is True
    assert record["submission_readiness_gate_passed"] is True
    assert record["required_source_artifact_count"] == 4
    assert record["required_source_artifact_present_count"] == 4
    assert record["required_source_artifact_parseable_count"] == 4
    assert record["source_guard_case_count"] == 6
    assert record["source_guard_pass_count"] == 6
    assert record["source_public_overfit_violation_count"] == 0
    assert record["source_boundary_violation_count"] == 0
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["manual_upload_allowed"] is False
    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_submission_readiness_gate_record(record) == []


def test_readiness_package_summarizes_source_record():
    package = build_readiness_package(_sample_source_record())

    assert package["required_source_artifact_count"] == 4
    assert package["source_guard_case_count"] == 6
    assert package["source_guard_pass_count"] == 6
    assert package["source_public_overfit_violation_count"] == 0
    assert package["source_boundary_violation_count"] == 0
    assert package["measurement_target_count"] == 10


def test_submission_readiness_gate_blocks_real_submission():
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_submission_readiness_gate_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_submission_readiness_gate_blocks_ready_for_real_kaggle_submission():
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")
    record["ready_for_real_kaggle_submission"] = True

    issues = validate_submission_readiness_gate_record(record)

    assert "ready_for_real_kaggle_submission_NOT_FALSE" in issues


def test_submission_readiness_gate_requires_operator_approval_but_not_received():
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")

    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False


def test_submission_readiness_gate_fails_if_guard_violation_count_mutated():
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")
    record["source_public_overfit_violation_count"] = 1

    issues = validate_submission_readiness_gate_record(record)

    assert "SOURCE_PUBLIC_OVERFIT_VIOLATION_COUNT_MISMATCH" in issues


def test_submission_readiness_gate_artifacts_are_written(tmp_path: Path):
    record = build_submission_readiness_gate_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-submission-readiness-gate-v1.json" in written_files
    assert "milestone-12-submission-readiness-gate-index-v1.json" in written_files
    assert "milestone-12-submission-readiness-gate-manifest-v1.txt" in written_files
    assert "milestone-12-submission-readiness-gate-v1.md" in written_files
