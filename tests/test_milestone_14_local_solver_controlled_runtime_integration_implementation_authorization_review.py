from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_authorization_review import (
    AUTHORIZATION_STATUS,
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    QIV_STAGE,
    REVIEW_VERDICT,
    TASK_VALID,
    build_milestone_14_task_9_authorization_review,
    validate_milestone_14_task_9_authorization_review,
    write_milestone_14_task_9_authorization_review_artifacts,
)


def test_task_9_authorization_review_is_valid() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_9_authorization_review(review)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_9_denies_implementation_authorization() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.review_verdict == REVIEW_VERDICT
    assert review.authorization_status == AUTHORIZATION_STATUS
    assert review.block_reason == BLOCK_REASON
    assert review.implementation_authorized is False
    assert review.implementation_blocked is True


def test_task_9_operator_gate_remains_closed() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.operator_approval_required is True
    assert review.operator_approval_received is False
    assert review.operator_approval_gate_closed is True


def test_task_9_qiv_is_constraint_not_authorization() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.qiv_constraint_link_present is True
    assert review.qiv_authorizes_implementation is False
    assert review.qiv_overrides_operator_gate is False


def test_task_9_chain_after_task_8_and_qiv_before_task_10() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.previous_stage == PREVIOUS_STAGE
    assert review.qiv_stage == QIV_STAGE
    assert review.next_stage == NEXT_STAGE
    assert "TASK_8" in review.previous_stage
    assert "QIV" in review.qiv_stage
    assert "TASK_10" in review.next_stage


def test_task_9_no_runtime_or_solver_modification() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.runtime_activation_performed is False
    assert review.runtime_execution_performed is False
    assert review.runtime_solver_modified is False
    assert review.ranker_runtime_modified is False
    assert review.candidate_generator_modified is False
    assert review.implementation_performed is False


def test_task_9_no_kaggle_submission_path() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.real_submission_allowed is False
    assert review.ready_for_real_kaggle_submission is False
    assert review.manual_upload_allowed is False
    assert review.kaggle_authentication_allowed is False
    assert review.kaggle_authentication_performed is False
    assert review.kaggle_upload_allowed is False
    assert review.kaggle_upload_performed is False
    assert review.kaggle_submission_sent is False


def test_task_9_public_safety_boundary() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.external_api_dependency is False
    assert review.internet_during_eval is False
    assert review.private_core_exposure is False
    assert review.legal_certification is False
    assert review.official_score_claim_allowed is False
    assert review.competitive_score_claim_allowed is False
    assert review.public_overfit_allowed is False
    assert review.public_overfit_guard_required is True


def test_task_9_fail_closed_boundary() -> None:
    review = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert review.fail_closed_required is True
    assert review.fail_closed_active is True
    assert review.review_gate_failure_count == 0
    assert review.review_gate_count == len(review.review_gates)


def test_task_9_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")
    second = build_milestone_14_task_9_authorization_review(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_9_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "task9"
    doc_path = tmp_path / "task9.md"

    review, validation, paths = write_milestone_14_task_9_authorization_review_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert review.implementation_authorized is False
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-authorization-review-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["authorization_status"] == AUTHORIZATION_STATUS
    assert payload["record"]["qiv_authorizes_implementation"] is False
