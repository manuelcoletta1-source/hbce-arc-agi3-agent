from pathlib import Path

from hbce_arc_agi3.milestone_13_real_evaluation_boundary_gate import (
    BOUNDARY_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_boundary_policy,
    build_real_evaluation_boundary_gate_record,
    validate_real_evaluation_boundary_gate_record,
    write_artifacts,
)


def _sample_source_record():
    return {
        "milestone_12_status": "CLOSED",
        "closure_verdict": "MILESTONE_12_CLOSED_LOCAL_COMPETITIVE_SOLVER_READY_REAL_SUBMISSION_BLOCKED",
        "next_stage": "MILESTONE_13_NOT_OPENED_CANONICALLY",
        "milestone_13_opened": False,
        "milestone_13_opening_allowed": False,
    }


def test_real_evaluation_boundary_gate_record_is_valid():
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["boundary_verdict"] == BOUNDARY_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_13_status"] == "OPENED_CANONICALLY"
    assert record["milestone_13_opened"] is True
    assert record["milestone_13_opened_canonically"] is True
    assert record["source_milestone_12_closed"] is True
    assert record["source_closure_passed"] is True
    assert record["source_milestone_13_not_opened"] is True
    assert record["real_evaluation_boundary_gate_ready"] is True
    assert record["real_evaluation_boundary_gate_passed"] is True
    assert record["real_evaluation_prep_allowed"] is True
    assert record["local_solver_improvement_allowed"] is True
    assert record["solver_capability_gap_audit_allowed"] is True
    assert record["real_kaggle_evaluation_allowed"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["issue_count"] == 0
    assert validate_real_evaluation_boundary_gate_record(record) == []


def test_boundary_policy_allows_local_work_and_blocks_submission():
    policy = build_boundary_policy(_sample_source_record())

    assert policy["real_evaluation_prep_allowed"] is True
    assert policy["local_solver_improvement_allowed"] is True
    assert policy["local_diagnostic_eval_allowed"] is True
    assert policy["real_kaggle_evaluation_allowed"] is False
    assert policy["kaggle_authentication_allowed"] is False
    assert policy["kaggle_upload_allowed"] is False
    assert policy["real_submission_allowed"] is False
    assert policy["manual_upload_allowed"] is False
    assert policy["official_score_claim_allowed"] is False
    assert policy["competitive_score_claim_allowed"] is False
    assert policy["measurement_target_count"] == 10


def test_real_evaluation_boundary_blocks_kaggle_authentication():
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")
    record["kaggle_authentication_allowed"] = True

    issues = validate_real_evaluation_boundary_gate_record(record)

    assert "kaggle_authentication_allowed_NOT_FALSE" in issues


def test_real_evaluation_boundary_blocks_real_submission():
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_real_evaluation_boundary_gate_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_real_evaluation_boundary_requires_operator_approval_but_not_received():
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")

    assert record["operator_approval_required"] is True
    assert record["operator_approval_received"] is False


def test_real_evaluation_boundary_fails_if_milestone_13_not_opened():
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")
    record["milestone_13_opened"] = False

    issues = validate_real_evaluation_boundary_gate_record(record)

    assert "milestone_13_opened_NOT_TRUE" in issues


def test_real_evaluation_boundary_artifacts_are_written(tmp_path: Path):
    record = build_real_evaluation_boundary_gate_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-real-evaluation-boundary-gate-v1.json" in written_files
    assert "milestone-13-real-evaluation-boundary-gate-index-v1.json" in written_files
    assert "milestone-13-real-evaluation-boundary-gate-manifest-v1.txt" in written_files
    assert "milestone-13-real-evaluation-boundary-gate-v1.md" in written_files
