from pathlib import Path
import json

from hbce_arc_agi3.milestone_30_governed_opening import (
    CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT,
    NEXT_STAGE,
    OPENING_REVISION,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    SOURCE_MILESTONE_ID,
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


def test_milestone_30_source_closure_snapshot_is_valid():
    snapshot = build_source_closure_snapshot()

    assert validate_source_closure_snapshot(snapshot)
    assert snapshot["source_task_id"] == SOURCE_TASK_ID
    assert snapshot["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert snapshot["source_closure_status"] == "CLOSED"
    assert snapshot["source_technical_status"] == "PASS"
    assert snapshot["source_milestone_closed"] is True
    assert snapshot["source_ready_for_next_milestone"] is True
    assert snapshot["source_next_stage"] == TASK_ID
    assert snapshot["stable_source_closure"] is True


def test_milestone_30_governed_opening_report_is_valid():
    report = build_governed_opening_report()

    assert validate_governed_opening_report(report)
    assert report["task_id"] == TASK_ID
    assert report["source_task_id"] == SOURCE_TASK_ID
    assert report["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert report["opening_revision"] == OPENING_REVISION
    assert report["task_1_signature"] == task_1_signature()
    assert report["opening_status"] == "OPEN"
    assert report["technical_status"] == "PASS"
    assert report["process_status"] == "GOVERNED_OPENING_WITH_TASK_BUDGET_MAX_8"
    assert report["source_dependency_valid"] is True
    assert report["task_budget_max"] == TASK_BUDGET_MAX
    assert report["current_task_number"] == CURRENT_TASK_NUMBER
    assert report["implementation_started"] is False
    assert report["implementation_allowed_at_task_1"] is False
    assert report["objective_selection_required_next"] is True
    assert report["scope_lock_required_next"] is True
    assert report["proposed_operator_seed"]["seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert report["proposed_operator_seed"]["status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert report["generated_artifact_count"] == GENERATED_ARTIFACT_COUNT
    assert report["next_stage"] == NEXT_STAGE


def test_milestone_30_governed_opening_operator_seed_is_candidate_only():
    report = build_governed_opening_report()
    seed = report["proposed_operator_seed"]

    assert seed["seed_id"] == "JOKER_C2_IDENTITY_BOUNDARY_AND_FAIL_CLOSED_PUBLIC_MODE"
    assert seed["status"] == "CANDIDATE_ONLY_NOT_LOCKED"
    assert seed["scope_lock_required_before_implementation"] is True
    assert seed["private_core_access_without_verified_manuel"] is False
    assert seed["external_command_authority_without_authorization"] is False
    assert seed["fail_closed_rules"]["missing_identity"] == "RESTRICT"
    assert seed["fail_closed_rules"]["missing_authorization"] == "REFUSE"
    assert seed["fail_closed_rules"]["private_core_forcing_attempt"] == "BLOCK"


def test_milestone_30_governed_opening_artifact_writer_generates_valid_artifacts(tmp_path):
    artifacts = write_task_1_artifacts(tmp_path)

    assert artifacts["manifest"]["task_id"] == TASK_ID
    assert artifacts["manifest"]["source_task_id"] == SOURCE_TASK_ID
    assert artifacts["manifest"]["source_milestone_id"] == SOURCE_MILESTONE_ID
    assert artifacts["manifest"]["opening_revision"] == OPENING_REVISION
    assert artifacts["manifest"]["task_1_signature"] == task_1_signature()
    assert artifacts["manifest"]["opening_status"] == "OPEN"
    assert artifacts["manifest"]["technical_status"] == "PASS"
    assert artifacts["manifest"]["source_dependency_valid"] is True
    assert artifacts["manifest"]["implementation_started"] is False
    assert artifacts["manifest"]["implementation_allowed_at_task_1"] is False
    assert artifacts["manifest"]["objective_selection_required_next"] is True
    assert artifacts["manifest"]["scope_lock_required_next"] is True
    assert artifacts["manifest"]["proposed_operator_seed_id"] == PROPOSED_OPERATOR_SEED_ID
    assert artifacts["manifest"]["proposed_operator_seed_status"] == PROPOSED_OPERATOR_SEED_STATUS
    assert artifacts["manifest"]["generated_artifact_count"] == 5
    assert artifacts["manifest"]["next_stage"] == NEXT_STAGE

    report_path = Path(tmp_path) / "task-1-governed-opening.json"
    markdown_path = Path(tmp_path) / "task-1-governed-opening.md"
    seed_path = Path(tmp_path) / "task-1-operator-seed.json"
    manifest_path = Path(tmp_path) / "task-1-manifest.json"
    index_path = Path(tmp_path) / "task-1-index.txt"

    assert report_path.exists()
    assert markdown_path.exists()
    assert seed_path.exists()
    assert manifest_path.exists()
    assert index_path.exists()

    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert validate_governed_opening_report(report)
    assert "MILESTONE_30_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_READY=true" in index_path.read_text(encoding="utf-8")
