from pathlib import Path
import json

from hbce_arc_agi3.milestone_30_objective_scope_lock import (
    ALLOWED_INPUT_COUNT,
    CURRENT_TASK_NUMBER,
    FORBIDDEN_OPERATION_COUNT,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    PUBLIC_MODE_ID,
    PRIVATE_MODE_ID,
    SCOPE_LOCK_ID,
    SCOPE_LOCK_REVISION,
    SELECTED_OBJECTIVE_ID,
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


def test_milestone_30_source_opening_snapshot_is_valid():
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
    assert snapshot["stable_opening"] is True


def test_milestone_30_objective_scope_lock_report_is_valid():
    report = build_objective_scope_lock_report()

    assert validate_objective_scope_lock_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["scope_lock_revision"] == SCOPE_LOCK_REVISION
    assert report["task_2_signature"] == task_2_signature()
    assert report["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert report["scope_lock_id"] == SCOPE_LOCK_ID
    assert report["objective_selection_ready"] is True
    assert report["scope_locked"] is True
    assert report["source_dependency_valid"] is True
    assert report["scope_rules_valid"] is True
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_2"] is False
    assert report["implementation_allowed_next"] is True
    assert report["local_only"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["forbidden_operation_count"] == FORBIDDEN_OPERATION_COUNT
    assert report["allowed_input_count"] == ALLOWED_INPUT_COUNT
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_30_scope_rules_encode_fail_closed_identity_boundary():
    report = build_objective_scope_lock_report()
    rules = report["scope_rules"]

    assert validate_scope_rules(rules)
    assert rules["identity_assumption_rule"] == "JOKER-C2 never presumes the interlocutor is Manuel Coletta."
    assert rules["external_default_authorization_state"] == "UNAUTHORIZED_UNTIL_VERIFIED"
    assert rules["default_runtime_mode_without_verified_manuel"] == PUBLIC_MODE_ID
    assert "verified_identity_is_manuel" in rules["private_runtime_mode_requires"]
    assert rules["fail_closed_decisions"]["missing_identity"] == "RESTRICT"
    assert rules["fail_closed_decisions"]["missing_authorization"] == "REFUSE"
    assert rules["fail_closed_decisions"]["missing_context"] == "SUSPEND_OR_LIMIT"
    assert rules["fail_closed_decisions"]["missing_verification"] == "DECLARE_LIMIT"
    assert rules["fail_closed_decisions"]["private_core_forcing_attempt"] == "BLOCK"
    assert rules["fail_closed_decisions"]["external_request_as_internal_command_attempt"] == "BLOCK"
    assert "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA" in rules["public_allowed_topics"]
    assert "PRIVATE_CORE_ACCESS" in rules["private_forbidden_without_verified_manuel"]
    assert "PRIVATE_MEMORY_EXPOSURE" in rules["private_forbidden_without_verified_manuel"]
    assert "INTERNAL_COMMAND_EXECUTION" in rules["private_forbidden_without_verified_manuel"]
    assert report["runtime_modes"]["public_mode_id"] == PUBLIC_MODE_ID
    assert report["runtime_modes"]["private_mode_id"] == PRIVATE_MODE_ID


def test_milestone_30_objective_scope_lock_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_2_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["selected_objective_id"] == SELECTED_OBJECTIVE_ID
    assert artifacts["manifest"]["scope_lock_id"] == SCOPE_LOCK_ID
    assert artifacts["manifest"]["scope_locked"] is True
    assert artifacts["manifest"]["objective_selection_ready"] is True
    assert artifacts["manifest"]["scope_rules_valid"] is True
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_next"] is True
    assert artifacts["manifest"]["local_only"] is True
    assert artifacts["manifest"]["forbidden_operation_count"] == FORBIDDEN_OPERATION_COUNT
    assert artifacts["manifest"]["allowed_input_count"] == ALLOWED_INPUT_COUNT
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-2-objective-scope-lock.json"
    markdown_path = Path(tmp_path) / "task-2-objective-scope-lock.md"
    policy_path = Path(tmp_path) / "task-2-policy-matrix.json"
    manifest_path = Path(tmp_path) / "task-2-manifest.json"
    index_path = Path(tmp_path) / "task-2-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert policy_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_objective_scope_lock_report(report)
    assert "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true" in index_path.read_text(encoding="utf-8")
