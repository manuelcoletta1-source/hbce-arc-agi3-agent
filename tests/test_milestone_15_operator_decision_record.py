from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_operator_decision_record import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    RECORD_DECISION,
    RECORD_VERDICT,
    TASK_VALID,
    build_milestone_15_task_2_operator_decision_record,
    validate_milestone_15_task_2_operator_decision_record,
    write_milestone_15_task_2_operator_decision_record_artifacts,
)


def test_task_2_operator_decision_record_is_valid() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_2_operator_decision_record(record)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_2_records_pending_operator_decision_only() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.record_verdict == RECORD_VERDICT
    assert record.record_decision == RECORD_DECISION
    assert record.block_reason == BLOCK_REASON
    assert record.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_2_chain_is_correct() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.previous_stage == PREVIOUS_STAGE
    assert record.next_stage == NEXT_STAGE
    assert record.source_task_1_final_baseline_commit == "ed48f9c"
    assert record.source_task_1_final_signature == "22CAADB16533FB69"


def test_task_2_decision_not_received_and_not_recorded() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.operator_decision_required is True
    assert record.operator_decision_received is False
    assert record.operator_decision_recorded is False
    assert record.operator_decision_authorizes_implementation is False


def test_task_2_no_implementation_authorization_exists() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.implementation_authorized is False
    assert record.implementation_blocked is True
    assert record.runtime_activation_authorized is False
    assert record.runtime_activation_performed is False
    assert record.runtime_execution_performed is False
    assert record.implementation_performed is False


def test_task_2_runtime_modules_remain_unmodified() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.runtime_solver_modified is False
    assert record.ranker_runtime_modified is False
    assert record.candidate_generator_modified is False


def test_task_2_no_real_submission_path_is_open() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.real_evaluation_performed is False
    assert record.real_submission_allowed is False
    assert record.ready_for_real_kaggle_submission is False
    assert record.manual_upload_allowed is False
    assert record.kaggle_authentication_allowed is False
    assert record.kaggle_authentication_performed is False
    assert record.kaggle_upload_allowed is False
    assert record.kaggle_upload_performed is False
    assert record.kaggle_submission_sent is False


def test_task_2_public_boundary_is_preserved() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.external_api_dependency is False
    assert record.internet_during_eval is False
    assert record.private_core_exposure is False
    assert record.legal_certification is False
    assert record.official_score_claim_allowed is False
    assert record.competitive_score_claim_allowed is False
    assert record.public_overfit_allowed is False
    assert record.public_overfit_guard_required is True


def test_task_2_fail_closed_boundary_is_active() -> None:
    record = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert record.fail_closed_required is True
    assert record.fail_closed_active is True
    assert record.decision_record_failure_count == 0
    assert record.decision_record_check_count == len(record.decision_record_checks)
    assert record.decision_record_check_count == 10


def test_task_2_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")
    second = build_milestone_15_task_2_operator_decision_record(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_2_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task2"
    doc_path = tmp_path / "m15_task2.md"

    record, validation, paths = write_milestone_15_task_2_operator_decision_record_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert record.operator_decision_record_created is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-operator-decision-record-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["record_decision"] == RECORD_DECISION
    assert payload["record"]["operator_decision_received"] is False
    assert payload["record"]["implementation_authorized"] is False
