from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_final_closure import (
    BLOCK_REASON,
    FINAL_DECISION,
    FINAL_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    SOURCE_AUTHORIZATION_STAGE,
    SOURCE_OPERATOR_GATE_STAGE,
    SOURCE_QIV_STAGE,
    TASK_VALID,
    build_milestone_14_task_11_final_closure,
    validate_milestone_14_task_11_final_closure,
    write_milestone_14_task_11_final_closure_artifacts,
)


def test_task_11_final_closure_is_valid() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_11_final_closure(closure)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_11_closes_milestone_14_without_runtime_activation() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.final_verdict == FINAL_VERDICT
    assert closure.final_decision == FINAL_DECISION
    assert closure.block_reason == BLOCK_REASON
    assert closure.milestone_14_closed is True
    assert closure.milestone_14_closed_without_runtime_activation is True
    assert closure.runtime_activation_performed is False


def test_task_11_chain_references_task_8_qiv_task_9_task_10() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.previous_stage == PREVIOUS_STAGE
    assert closure.source_operator_gate_stage == SOURCE_OPERATOR_GATE_STAGE
    assert closure.source_qiv_stage == SOURCE_QIV_STAGE
    assert closure.source_authorization_stage == SOURCE_AUTHORIZATION_STAGE
    assert closure.next_stage == NEXT_STAGE
    assert "TASK_10" in closure.previous_stage
    assert "TASK_8" in closure.source_operator_gate_stage
    assert "QIV" in closure.source_qiv_stage
    assert "TASK_9" in closure.source_authorization_stage


def test_task_11_operator_gate_and_authorization_are_closed() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.operator_approval_required is True
    assert closure.operator_approval_received is False
    assert closure.operator_gate_closed is True
    assert closure.authorization_review_denied is True
    assert closure.implementation_authorized is False
    assert closure.implementation_blocked is True


def test_task_11_qiv_is_valid_but_non_authorizing() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.qiv_constraint_link_valid is True
    assert closure.qiv_authorizes_implementation is False
    assert closure.qiv_overrides_operator_gate is False


def test_task_11_no_runtime_or_solver_modification() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.runtime_execution_performed is False
    assert closure.runtime_solver_modified is False
    assert closure.ranker_runtime_modified is False
    assert closure.candidate_generator_modified is False
    assert closure.implementation_performed is False


def test_task_11_no_real_submission_path() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.real_submission_allowed is False
    assert closure.ready_for_real_kaggle_submission is False
    assert closure.manual_upload_allowed is False
    assert closure.kaggle_authentication_allowed is False
    assert closure.kaggle_authentication_performed is False
    assert closure.kaggle_upload_allowed is False
    assert closure.kaggle_upload_performed is False
    assert closure.kaggle_submission_sent is False


def test_task_11_public_boundary() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.external_api_dependency is False
    assert closure.internet_during_eval is False
    assert closure.private_core_exposure is False
    assert closure.legal_certification is False
    assert closure.official_score_claim_allowed is False
    assert closure.competitive_score_claim_allowed is False
    assert closure.public_overfit_allowed is False
    assert closure.public_overfit_guard_required is True


def test_task_11_fail_closed_boundary() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.fail_closed_required is True
    assert closure.fail_closed_active is True
    assert closure.final_closure_gate_failure_count == 0
    assert closure.final_closure_gate_count == len(closure.final_closure_gates)
    assert closure.final_closure_gate_count == 9


def test_task_11_ready_for_milestone_15_decision() -> None:
    closure = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert closure.ready_for_milestone_15_decision is True
    assert closure.next_stage == "MILESTONE_15_PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_11_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")
    second = build_milestone_14_task_11_final_closure(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_11_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "task11"
    doc_path = tmp_path / "task11.md"

    closure, validation, paths = write_milestone_14_task_11_final_closure_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert closure.milestone_14_closed is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-14-local-solver-controlled-runtime-integration-final-closure-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["final_decision"] == FINAL_DECISION
    assert payload["record"]["runtime_activation_performed"] is False
