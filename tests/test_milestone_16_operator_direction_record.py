from __future__ import annotations

import json

from hbce_arc_agi3.milestone_16_operator_direction_record import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    RECORD_DECISION,
    RECORD_VERDICT,
    TASK_VALID,
    build_milestone_16_task_2_operator_direction_record,
    validate_milestone_16_task_2_operator_direction_record,
    write_milestone_16_task_2_operator_direction_record_artifacts,
)


def test_task_2_operator_direction_record_is_valid() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")
    validation = validate_milestone_16_task_2_operator_direction_record(record)

    assert validation["valid"] is True
    assert validation["status"] == TASK_VALID
    assert validation["issue_count"] == 0


def test_task_2_records_pending_direction() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["operator_direction_record_created"] is True
    assert record["operator_direction_required"] is True
    assert record["operator_direction_received"] is False
    assert record["operator_direction_value"] == "PENDING_EXPLICIT_OPERATOR_DIRECTION"


def test_task_2_chain_from_task_1_is_correct() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["previous_stage"] == PREVIOUS_STAGE
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_task_1_final_baseline_commit"] == "6393a02"
    assert record["source_task_1_final_signature"] == "CC061B8120F619BA"


def test_task_2_record_decision_is_no_runtime_action() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["record_verdict"] == RECORD_VERDICT
    assert record["record_decision"] == RECORD_DECISION
    assert record["block_reason"] == BLOCK_REASON


def test_task_2_operator_authorization_not_received() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["operator_decision_required"] is True
    assert record["operator_decision_received"] is False
    assert record["explicit_operator_authorization_required"] is True
    assert record["explicit_operator_authorization_received"] is False


def test_task_2_no_implementation_is_authorized() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["implementation_authorization_granted"] is False
    assert record["implementation_authorized"] is False
    assert record["implementation_blocked"] is True
    assert record["implementation_performed"] is False
    assert record["implementation_patch_created"] is False
    assert record["implementation_patch_applied"] is False


def test_task_2_no_runtime_modification_is_allowed() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["runtime_solver_patch_allowed"] is False
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["candidate_generator_patch_allowed"] is False
    assert record["candidate_generator_modified"] is False


def test_task_2_no_runtime_wiring_activation_execution() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["runtime_wiring_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_activation_authorized"] is False
    assert record["runtime_activation_blocked"] is True
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_allowed"] is False
    assert record["runtime_execution_performed"] is False


def test_task_2_no_real_submission_path_is_open() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["real_evaluation_allowed"] is False
    assert record["real_evaluation_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["ready_for_real_kaggle_submission"] is False
    assert record["manual_upload_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_upload_allowed"] is False
    assert record["kaggle_submission_sent"] is False


def test_task_2_public_boundary_is_preserved() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["external_api_dependency"] is False
    assert record["internet_during_eval"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert record["official_score_claim_allowed"] is False
    assert record["competitive_score_claim_allowed"] is False
    assert record["public_overfit_allowed"] is False
    assert record["public_overfit_guard_required"] is True


def test_task_2_fail_closed_record_is_active() -> None:
    record = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert record["fail_closed_required"] is True
    assert record["fail_closed_active"] is True
    assert record["milestone_16_operator_direction_record_failure_count"] == 0
    assert record["milestone_16_operator_direction_record_check_count"] == len(record["milestone_16_operator_direction_record_checks"])
    assert record["milestone_16_operator_direction_record_check_count"] == 31


def test_task_2_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")
    second = build_milestone_16_task_2_operator_direction_record(baseline_commit="TESTBASE")

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16


def test_task_2_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m16_task2"
    doc_path = tmp_path / "m16_task2.md"

    record, validation, paths = write_milestone_16_task_2_operator_direction_record_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation["valid"] is True
    assert record["operator_direction_record_created"] is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-16-operator-direction-record-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["record_decision"] == RECORD_DECISION
    assert payload["record"]["operator_direction_received"] is False
    assert payload["record"]["implementation_authorized"] is False
    assert payload["record"]["runtime_activation_performed"] is False
