from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_review_decision import (
    DECISION_STATUS,
    DECISION_VERDICT,
    NEXT_STAGE,
    TASK_VALID,
    build_milestone_14_task_7_review_decision_record,
    validate_milestone_14_task_7_review_decision_record,
    write_milestone_14_task_7_review_decision_artifacts,
)


def test_task_7_review_decision_record_is_valid() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_7_review_decision_record(record)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_7_decision_blocks_implementation_without_operator_approval() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.decision_verdict == DECISION_VERDICT
    assert record.decision_status == DECISION_STATUS
    assert record.implementation_review_decision_performed is True
    assert record.implementation_authorized is False
    assert record.implementation_blocked is True
    assert record.implementation_block_reason == "EXPLICIT_OPERATOR_APPROVAL_NOT_RECEIVED"


def test_task_7_source_review_is_valid() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.source_review_loaded is True
    assert record.source_review_valid is True
    assert record.source_review_signature != "NO_SOURCE_REVIEW_SIGNATURE"
    assert record.source_review_baseline_commit != "NO_SOURCE_REVIEW_BASELINE"
    assert record.dry_run_review_passed is True
    assert record.ready_for_review_decision is True


def test_task_7_next_stage_is_operator_approval_gate() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.next_stage == NEXT_STAGE
    assert record.operator_approval_gate_required_next is True
    assert record.operator_approval_required is True
    assert record.operator_approval_received is False


def test_task_7_decision_gate_counts_are_clean() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.decision_gate_count == 20
    assert record.decision_gate_pass_count == 20
    assert record.decision_gate_failure_count == 0
    assert record.decision_finding_count == 4
    assert record.blocking_issue_count == 0
    assert record.issue_count == 0


def test_task_7_runtime_and_submission_are_blocked() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.review_only is True
    assert record.decision_only is True
    assert record.dry_run_only is True
    assert record.runtime_activation_performed is False
    assert record.runtime_execution_performed is False
    assert record.runtime_solver_modified is False
    assert record.ranker_runtime_modified is False
    assert record.candidate_generator_modified is False
    assert record.implementation_performed is False
    assert record.real_submission_allowed is False
    assert record.ready_for_real_kaggle_submission is False


def test_task_7_kaggle_boundary_is_closed() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.kaggle_authentication_allowed is False
    assert record.kaggle_authentication_performed is False
    assert record.kaggle_upload_allowed is False
    assert record.kaggle_upload_performed is False
    assert record.kaggle_submission_sent is False
    assert record.kaggle_score_semantics == "NOT_A_KAGGLE_SCORE"


def test_task_7_public_boundary_is_safe() -> None:
    record = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert record.local_only is True
    assert record.deterministic is True
    assert record.public_safe is True
    assert record.external_api_dependency is False
    assert record.internet_during_eval is False
    assert record.private_core_exposure is False
    assert record.legal_certification is False
    assert record.public_overfit_allowed is False
    assert record.public_overfit_guard_required is True


def test_task_7_writes_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "artifacts"
    doc_path = tmp_path / "doc.md"

    record, validation, paths = write_milestone_14_task_7_review_decision_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert record.implementation_blocked is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads((output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-review-decision-v1.json").read_text())
    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["decision_verdict"] == DECISION_VERDICT


def test_task_7_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")
    second = build_milestone_14_task_7_review_decision_record(baseline_commit="TESTBASE")

    assert first.signature == second.signature
