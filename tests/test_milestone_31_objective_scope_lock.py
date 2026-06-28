from pathlib import Path
import json

from hbce_arc_agi3.milestone_31_objective_scope_lock import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
    SELECTED_OBJECTIVE_STATUS,
    SESSION_GATE_MODE_ID,
    SOURCE_TASK_ID,
    TASK_BUDGET_MAX,
    TASK_ID,
    build_objective_scope_lock_report,
    build_source_opening_snapshot,
    task_2_signature,
    validate_objective_scope_lock_report,
    validate_scope_rules,
    validate_source_opening_snapshot,
    write_task_2_artifacts,
)


def test_milestone_31_objective_scope_lock_source_opening_snapshot_is_valid():
    snapshot = build_source_opening_snapshot()

    assert validate_source_opening_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["opening_status"] == "OPEN"
    assert snapshot["technical_status"] == "PASS"
    assert snapshot["source_dependency_valid"] is True
    assert snapshot["implementation_started"] is False
    assert snapshot["implementation_allowed_at_task_1"] is False
    assert snapshot["objective_selection_required_next"] is True
    assert snapshot["scope_lock_required_next"] is True
    assert snapshot["proposed_operator_seed_id"] == SELECTED_OBJECTIVE_ID
    assert snapshot["proposed_operator_seed_status"] == "CANDIDATE_ONLY_NOT_LOCKED"
    assert snapshot["seed_candidate_only"] is True
    assert snapshot["seed_selected"] is False
    assert snapshot["seed_scope_locked"] is False
    assert snapshot["stable_opening"] is True


def test_milestone_31_objective_scope_lock_report_is_valid():
    report = build_objective_scope_lock_report()

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["scope_lock_revision"] == SCOPE_LOCK_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["source_dependency_valid"] is True
    assert report["objective_selection_ready"] is True
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["selected_objective_status"] == SELECTED_OBJECTIVE_STATUS
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["scope_locked"] is True
    assert report["scope_rules_valid"] is True
    assert validate_scope_rules(report["scope_rules"])
    assert report["runtime_modes"]["session_gate_mode_id"] == SESSION_GATE_MODE_ID
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_2"] is False
    assert report["implementation_allowed_next"] is True
    assert report["local_only"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_31_scope_lock_forbids_unverified_or_unauthorized_session_gate():
    report = build_objective_scope_lock_report()

    assert report["private_core_access_without_verified_manuel_allowed"] is False
    assert report["unverified_manuel_assumption_allowed"] is False
    assert report["external_command_authority_allowed"] is False
    assert report["session_authorization_without_valid_authorization_allowed"] is False
    assert report["session_authorization_without_context_allowed"] is False
    assert report["session_authorization_without_verification_allowed"] is False
    assert all(value is False for value in report["scope_rules"]["forbidden_operations"].values())
    assert "verified_identity_is_manuel" in report["scope_rules"]["required_session_gate_inputs"]
    assert "authorization_valid" in report["scope_rules"]["required_session_gate_inputs"]
    assert "context_sufficient" in report["scope_rules"]["required_session_gate_inputs"]
    assert "verification_available" in report["scope_rules"]["required_session_gate_inputs"]


def test_milestone_31_objective_scope_lock_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_2_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["selected_objective_status"] == SELECTED_OBJECTIVE_STATUS
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["scope_locked"] is True
    assert artifacts["manifest"]["scope_rules_valid"] is True
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_at_task_2"] is False
    assert artifacts["manifest"]["implementation_allowed_next"] is True
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-2-objective-scope-lock.json"
    markdown_path = Path(tmp_path) / "task-2-objective-scope-lock.md"
    matrix_path = Path(tmp_path) / "task-2-policy-matrix.json"
    manifest_path = Path(tmp_path) / "task-2-manifest.json"
    index_path = Path(tmp_path) / "task-2-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert matrix_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_objective_scope_lock_report(report)
    assert "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index_path.read_text(encoding="utf-8")
