from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_closure_review import (
    BLOCK_REASON,
    CLOSURE_DECISION,
    CLOSURE_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    SOURCE_OPERATOR_GATE_STAGE,
    SOURCE_QIV_STAGE,
    TASK_VALID,
    build_milestone_14_task_10_closure_review,
    validate_milestone_14_task_10_closure_review,
    write_milestone_14_task_10_closure_review_artifacts,
)


def test_task_10_closure_review_is_valid() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_10_closure_review(review)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_10_closes_review_chain_without_implementation() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.closure_verdict == CLOSURE_VERDICT
    assert review.closure_decision == CLOSURE_DECISION
    assert review.block_reason == BLOCK_REASON
    assert review.review_chain_closed is True
    assert review.ready_for_final_closure is True
    assert review.implementation_authorized is False
    assert review.implementation_blocked is True


def test_task_10_chain_references_task_8_qiv_and_task_9() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.previous_stage == PREVIOUS_STAGE
    assert review.source_operator_gate_stage == SOURCE_OPERATOR_GATE_STAGE
    assert review.source_qiv_stage == SOURCE_QIV_STAGE
    assert review.next_stage == NEXT_STAGE
    assert "TASK_9" in review.previous_stage
    assert "TASK_8" in review.source_operator_gate_stage
    assert "QIV" in review.source_qiv_stage


def test_task_10_operator_approval_still_missing() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.operator_approval_required is True
    assert review.operator_approval_received is False
    assert review.operator_gate_closed is True


def test_task_10_qiv_is_valid_but_non_authorizing() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.qiv_constraint_link_valid is True
    assert review.qiv_authorizes_implementation is False
    assert review.qiv_overrides_operator_gate is False


def test_task_10_authorization_review_denied() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.authorization_review_denied is True
    assert review.source_authorization_review_final_baseline_commit == "9a092a5"
    assert review.source_authorization_review_final_signature == "D6D132659FF2406B"


def test_task_10_no_runtime_or_solver_modification() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.runtime_activation_performed is False
    assert review.runtime_execution_performed is False
    assert review.runtime_solver_modified is False
    assert review.ranker_runtime_modified is False
    assert review.candidate_generator_modified is False
    assert review.implementation_performed is False


def test_task_10_no_kaggle_path() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.real_submission_allowed is False
    assert review.ready_for_real_kaggle_submission is False
    assert review.manual_upload_allowed is False
    assert review.kaggle_authentication_allowed is False
    assert review.kaggle_authentication_performed is False
    assert review.kaggle_upload_allowed is False
    assert review.kaggle_upload_performed is False
    assert review.kaggle_submission_sent is False


def test_task_10_public_boundary() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.external_api_dependency is False
    assert review.internet_during_eval is False
    assert review.private_core_exposure is False
    assert review.legal_certification is False
    assert review.official_score_claim_allowed is False
    assert review.competitive_score_claim_allowed is False
    assert review.public_overfit_allowed is False
    assert review.public_overfit_guard_required is True


def test_task_10_fail_closed_boundary() -> None:
    review = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert review.fail_closed_required is True
    assert review.fail_closed_active is True
    assert review.closure_gate_failure_count == 0
    assert review.closure_gate_count == len(review.closure_gates)
    assert review.closure_gate_count == 8


def test_task_10_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")
    second = build_milestone_14_task_10_closure_review(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_10_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "task10"
    doc_path = tmp_path / "task10.md"

    review, validation, paths = write_milestone_14_task_10_closure_review_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert review.review_chain_closed is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-14-local-solver-controlled-runtime-integration-closure-review-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["closure_decision"] == CLOSURE_DECISION
    assert payload["record"]["implementation_authorized"] is False
