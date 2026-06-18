from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_operator_approval_gate import (
    GATE_STATUS,
    GATE_VERDICT,
    NEXT_STAGE,
    TASK_VALID,
    build_milestone_14_task_8_operator_approval_gate_record,
    validate_milestone_14_task_8_operator_approval_gate_record,
    write_milestone_14_task_8_operator_approval_gate_artifacts,
)


def test_task_8_operator_approval_gate_record_is_valid() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_8_operator_approval_gate_record(record)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_8_gate_is_closed_without_operator_approval() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.gate_verdict == GATE_VERDICT
    assert record.gate_status == GATE_STATUS
    assert record.operator_approval_gate_performed is True
    assert record.operator_approval_gate_open is False
    assert record.operator_approval_gate_closed is True
    assert record.operator_approval_required is True
    assert record.operator_approval_received is False


def test_task_8_implementation_is_not_authorized() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.implementation_authorized is False
    assert record.implementation_blocked is True
    assert record.implementation_block_reason == "OPERATOR_APPROVAL_GATE_CLOSED"
    assert record.source_implementation_authorized is False
    assert record.source_implementation_blocked is True
    assert record.source_implementation_block_reason == "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED"


def test_task_8_source_decision_is_valid() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.source_decision_loaded is True
    assert record.source_decision_valid is True
    assert record.source_decision_signature != "NO_SOURCE_DECISION_SIGNATURE"
    assert record.source_decision_baseline_commit != "NO_SOURCE_DECISION_BASELINE"
    assert record.implementation_review_decision_performed is True


def test_task_8_gate_counts_are_clean() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.approval_requirement_count == 7
    assert record.approval_requirement_pass_count == 7
    assert record.approval_requirement_failure_count == 0
    assert record.gate_check_count == 16
    assert record.gate_check_pass_count == 16
    assert record.gate_check_failure_count == 0
    assert record.blocking_issue_count == 0
    assert record.issue_count == 0


def test_task_8_next_stage_is_authorization_review() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.next_stage == NEXT_STAGE


def test_task_8_runtime_and_submission_are_blocked() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.gate_only is True
    assert record.decision_only is True
    assert record.review_only is True
    assert record.dry_run_only is True
    assert record.runtime_activation_performed is False
    assert record.runtime_execution_performed is False
    assert record.runtime_solver_modified is False
    assert record.ranker_runtime_modified is False
    assert record.candidate_generator_modified is False
    assert record.implementation_performed is False
    assert record.real_submission_allowed is False
    assert record.ready_for_real_kaggle_submission is False


def test_task_8_kaggle_boundary_is_closed() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.kaggle_authentication_allowed is False
    assert record.kaggle_authentication_performed is False
    assert record.kaggle_upload_allowed is False
    assert record.kaggle_upload_performed is False
    assert record.kaggle_submission_sent is False
    assert record.kaggle_score_semantics == "NOT_A_KAGGLE_SCORE"


def test_task_8_public_boundary_is_safe() -> None:
    record = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert record.local_only is True
    assert record.deterministic is True
    assert record.public_safe is True
    assert record.external_api_dependency is False
    assert record.internet_during_eval is False
    assert record.private_core_exposure is False
    assert record.legal_certification is False
    assert record.public_overfit_allowed is False
    assert record.public_overfit_guard_required is True


def test_task_8_writes_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "artifacts"
    doc_path = tmp_path / "doc.md"

    record, validation, paths = write_milestone_14_task_8_operator_approval_gate_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert record.operator_approval_gate_closed is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads((output_dir / "milestone-14-local-solver-controlled-runtime-integration-operator-approval-gate-v1.json").read_text())
    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["gate_verdict"] == GATE_VERDICT


def test_task_8_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")
    second = build_milestone_14_task_8_operator_approval_gate_record(baseline_commit="TESTBASE")

    assert first.signature == second.signature
