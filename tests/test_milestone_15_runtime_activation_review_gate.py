from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_runtime_activation_review_gate import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    REVIEW_GATE_DECISION,
    REVIEW_GATE_VERDICT,
    TASK_VALID,
    build_milestone_15_task_5_runtime_activation_review_gate,
    validate_milestone_15_task_5_runtime_activation_review_gate,
    write_milestone_15_task_5_runtime_activation_review_gate_artifacts,
)


def test_task_5_runtime_activation_review_gate_is_valid() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_5_runtime_activation_review_gate(gate)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_5_reviews_task_4_block() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.review_gate_verdict == REVIEW_GATE_VERDICT
    assert gate.review_gate_decision == REVIEW_GATE_DECISION
    assert gate.block_reason == BLOCK_REASON
    assert gate.task_4_boundary_confirmed is True


def test_task_5_chain_is_correct() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.previous_stage == PREVIOUS_STAGE
    assert gate.next_stage == NEXT_STAGE
    assert gate.source_task_4_final_baseline_commit == "2e7e02c"
    assert gate.source_task_4_final_signature == "3DA3C07D68125962"
    assert gate.source_task_3_final_baseline_commit == "756df18"
    assert gate.source_task_3_final_signature == "3FF1874D0CEBB5C2"


def test_task_5_operator_decision_still_pending() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.operator_decision_required is True
    assert gate.operator_decision_received is False
    assert gate.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_5_no_explicit_authorization_received() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.explicit_operator_authorization_required is True
    assert gate.explicit_operator_authorization_received is False
    assert gate.no_implicit_authorization is True


def test_task_5_runtime_activation_stays_blocked() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.runtime_activation_authorization_required is True
    assert gate.runtime_activation_authorization_received is False
    assert gate.runtime_activation_authorized is False
    assert gate.runtime_activation_blocked is True
    assert gate.runtime_activation_performed is False


def test_task_5_runtime_execution_stays_blocked() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.runtime_execution_allowed is False
    assert gate.runtime_execution_performed is False


def test_task_5_no_implementation_authorization_exists() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.implementation_authorized is False
    assert gate.implementation_blocked is True
    assert gate.implementation_performed is False


def test_task_5_runtime_modules_remain_unmodified() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.runtime_solver_modified is False
    assert gate.ranker_runtime_modified is False
    assert gate.candidate_generator_modified is False


def test_task_5_no_real_submission_path_is_open() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.real_evaluation_performed is False
    assert gate.real_submission_allowed is False
    assert gate.ready_for_real_kaggle_submission is False
    assert gate.manual_upload_allowed is False
    assert gate.kaggle_authentication_allowed is False
    assert gate.kaggle_authentication_performed is False
    assert gate.kaggle_upload_allowed is False
    assert gate.kaggle_upload_performed is False
    assert gate.kaggle_submission_sent is False


def test_task_5_public_boundary_is_preserved() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.external_api_dependency is False
    assert gate.internet_during_eval is False
    assert gate.private_core_exposure is False
    assert gate.legal_certification is False
    assert gate.official_score_claim_allowed is False
    assert gate.competitive_score_claim_allowed is False
    assert gate.public_overfit_allowed is False
    assert gate.public_overfit_guard_required is True


def test_task_5_fail_closed_review_gate_is_active() -> None:
    gate = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert gate.fail_closed_required is True
    assert gate.fail_closed_active is True
    assert gate.runtime_activation_review_failure_count == 0
    assert gate.runtime_activation_review_check_count == len(gate.runtime_activation_review_checks)
    assert gate.runtime_activation_review_check_count == 14


def test_task_5_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")
    second = build_milestone_15_task_5_runtime_activation_review_gate(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_5_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task5"
    doc_path = tmp_path / "m15_task5.md"

    gate, validation, paths = write_milestone_15_task_5_runtime_activation_review_gate_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert gate.runtime_activation_review_gate_created is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-runtime-activation-review-gate-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["review_gate_decision"] == REVIEW_GATE_DECISION
    assert payload["record"]["runtime_activation_authorized"] is False
    assert payload["record"]["runtime_activation_performed"] is False
