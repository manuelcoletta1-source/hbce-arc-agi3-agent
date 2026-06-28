from pathlib import Path
import json

from hbce_arc_agi3.milestone_31_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE,
    OPENING_REVISION,
    PROCESS_STATUS,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_governed_opening_report,
    build_source_closure_snapshot,
    task_1_signature,
    validate_governed_opening_report,
    validate_source_closure_snapshot,
    write_task_1_artifacts,
)


def test_milestone_31_governed_opening_source_closure_snapshot_is_valid():
    snapshot = build_source_closure_snapshot()

    assert validate_source_closure_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["source_closure_status"] == "CLOSED"
    assert snapshot["source_technical_status"] == "PASS"
    assert snapshot["source_milestone_closed"] is True
    assert snapshot["source_ready_for_next_milestone"] is True
    assert snapshot["source_private_core_access_allowed_without_verified_manuel"] is False
    assert snapshot["source_unverified_manuel_assumption_allowed"] is False
    assert snapshot["source_external_command_authority_allowed"] is False
    assert snapshot["source_task_budget_max"] == 8
    assert snapshot["source_final_task_number"] == 6
    assert snapshot["source_task_7_unused"] is True
    assert snapshot["source_task_8_unused"] is True
    assert snapshot["stable_closure"] is True


def test_milestone_31_governed_opening_report_is_valid():
    report = build_governed_opening_report()

    assert validate_governed_opening_report(report)
    assert report["milestone_id"] == MILESTONE_ID
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == PROCESS_STATUS
    assert report["source_dependency_valid"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["proposed_operator_seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert report["proposed_operator_seed_status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert report["guardrails_carried_forward"]["fail_closed_default"] is True
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_31_governed_opening_seed_is_candidate_only():
    report = build_governed_opening_report()

    assert report["proposed_operator_seed_id"] == "JOKER_C2_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE"
    assert report["proposed_operator_seed_status"] == "CANDIDATE_ONLY_NOT_LOCKED"
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["guardrails_carried_forward"]["candidate_seed_not_locked"] is True
    assert report["guardrails_carried_forward"]["implementation_not_started"] is True


def test_milestone_31_governed_opening_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_1_artifacts(tmp_path)

    assert artifacts["manifest"]["milestone_id"] == MILESTONE_ID
    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["opening_status"] == "OPEN"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["source_dependency_valid"] is True
    assert artifacts["manifest"]["task_budget_max"] == 8
    assert artifacts["manifest"]["current_task_number"] == 1
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE
    assert artifacts["seed_candidate"]["candidate_only"] is True
    assert artifacts["seed_candidate"]["selected"] is False
    assert artifacts["seed_candidate"]["scope_locked"] is False
    assert artifacts["seed_candidate"]["implementation_started"] is False

    report_path = Path(tmp_path) / "task-1-governed-opening.json"
    markdown_path = Path(tmp_path) / "task-1-governed-opening.md"
    seed_path = Path(tmp_path) / "task-1-proposed-operator-seed.json"
    manifest_path = Path(tmp_path) / "task-1-manifest.json"
    index_path = Path(tmp_path) / "task-1-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert seed_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_governed_opening_report(report)
    assert "MILESTONE_31_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index_path.read_text(encoding="utf-8")
