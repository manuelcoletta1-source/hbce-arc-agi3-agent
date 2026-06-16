from pathlib import Path

from hbce_arc_agi3.milestone_12_competitive_solver_runtime_strategy_gate import (
    CHOSEN_STRATEGY,
    COMPETITIVE_GOAL,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_strategy_gate_record,
    validate_strategy_gate_record,
    write_artifacts,
)


def test_strategy_gate_record_is_valid():
    record = build_strategy_gate_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_12_status"] == "OPENED_CANONICALLY"
    assert record["milestone_12_opened_canonically"] is True
    assert record["competitive_goal"] == COMPETITIVE_GOAL
    assert record["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["strategy_summary"]["milestone_12_status"] == "OPENED_CANONICALLY"
    assert record["strategy_summary"]["competitive_goal"] == COMPETITIVE_GOAL
    assert record["strategy_summary"]["chosen_strategy"] == CHOSEN_STRATEGY
    assert record["source_milestone_11_status_closed"] is True
    assert record["source_milestone_11_final_closure_complete"] is True
    assert record["source_milestone_11_final_closure_passed"] is True
    assert record["source_milestone_11_closure_ok"] is True
    assert record["workstream_count"] == 8
    assert record["p0_workstream_count"] == 5
    assert record["measurement_target_count"] == 10
    assert record["public_overfit_allowed"] is False
    assert record["public_overfit_guard_required"] is True
    assert record["external_api_dependency"] is False
    assert record["internet_during_eval"] is False
    assert record["open_source_prize_eligibility_required"] is True
    assert record["real_submission_allowed"] is False
    assert record["manual_upload_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["kaggle_authentication_performed"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["gate_count"] >= 30
    assert record["issue_count"] == 0
    assert validate_strategy_gate_record(record) == []


def test_strategy_gate_fails_if_external_api_dependency_is_enabled():
    record = build_strategy_gate_record(baseline_commit="TEST-COMMIT")
    record["external_api_dependency"] = True

    issues = validate_strategy_gate_record(record)

    assert "external_api_dependency_NOT_FALSE" in issues


def test_strategy_gate_fails_if_submission_is_allowed():
    record = build_strategy_gate_record(baseline_commit="TEST-COMMIT")
    record["real_submission_allowed"] = True

    issues = validate_strategy_gate_record(record)

    assert "real_submission_allowed_NOT_FALSE" in issues


def test_strategy_gate_fails_if_public_overfit_is_allowed():
    record = build_strategy_gate_record(baseline_commit="TEST-COMMIT")
    record["public_overfit_allowed"] = True

    issues = validate_strategy_gate_record(record)

    assert "public_overfit_allowed_NOT_FALSE" in issues


def test_strategy_gate_artifacts_are_written(tmp_path: Path):
    record = build_strategy_gate_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-12-competitive-solver-runtime-strategy-gate-v1.json" in written_files
    assert "milestone-12-competitive-solver-runtime-strategy-gate-index-v1.json" in written_files
    assert "milestone-12-competitive-solver-runtime-strategy-gate-manifest-v1.txt" in written_files
    assert "milestone-12-competitive-solver-runtime-strategy-gate-v1.md" in written_files
