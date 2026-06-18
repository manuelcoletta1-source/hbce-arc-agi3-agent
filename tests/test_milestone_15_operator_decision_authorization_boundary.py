from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_operator_decision_authorization_boundary import (
    BLOCK_REASON,
    BOUNDARY_DECISION,
    BOUNDARY_VERDICT,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    TASK_VALID,
    build_milestone_15_task_3_authorization_boundary,
    validate_milestone_15_task_3_authorization_boundary,
    write_milestone_15_task_3_authorization_boundary_artifacts,
)


def test_task_3_authorization_boundary_is_valid() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_3_authorization_boundary(boundary)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_3_formalizes_pending_decision_not_authorization() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.boundary_verdict == BOUNDARY_VERDICT
    assert boundary.boundary_decision == BOUNDARY_DECISION
    assert boundary.block_reason == BLOCK_REASON
    assert boundary.pending_decision_is_authorization is False


def test_task_3_chain_is_correct() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.previous_stage == PREVIOUS_STAGE
    assert boundary.next_stage == NEXT_STAGE
    assert boundary.source_task_2_final_baseline_commit == "7cd11c0"
    assert boundary.source_task_2_final_signature == "92DD45142240063F"
    assert boundary.source_task_1_final_baseline_commit == "ed48f9c"
    assert boundary.source_task_1_final_signature == "22CAADB16533FB69"


def test_task_3_operator_decision_is_pending_only() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.operator_decision_required is True
    assert boundary.operator_decision_received is False
    assert boundary.operator_decision_recorded is False
    assert boundary.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_3_requires_explicit_authorization() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.explicit_authorization_required is True
    assert boundary.explicit_authorization_received is False
    assert boundary.operator_decision_authorizes_implementation is False
    assert boundary.no_implicit_authorization is True


def test_task_3_no_implementation_authorization_exists() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.implementation_authorized is False
    assert boundary.implementation_blocked is True
    assert boundary.runtime_activation_authorized is False
    assert boundary.runtime_activation_performed is False
    assert boundary.runtime_execution_performed is False
    assert boundary.implementation_performed is False


def test_task_3_runtime_modules_remain_unmodified() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.runtime_solver_modified is False
    assert boundary.ranker_runtime_modified is False
    assert boundary.candidate_generator_modified is False


def test_task_3_no_real_submission_path_is_open() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.real_evaluation_performed is False
    assert boundary.real_submission_allowed is False
    assert boundary.ready_for_real_kaggle_submission is False
    assert boundary.manual_upload_allowed is False
    assert boundary.kaggle_authentication_allowed is False
    assert boundary.kaggle_authentication_performed is False
    assert boundary.kaggle_upload_allowed is False
    assert boundary.kaggle_upload_performed is False
    assert boundary.kaggle_submission_sent is False


def test_task_3_public_boundary_is_preserved() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.external_api_dependency is False
    assert boundary.internet_during_eval is False
    assert boundary.private_core_exposure is False
    assert boundary.legal_certification is False
    assert boundary.official_score_claim_allowed is False
    assert boundary.competitive_score_claim_allowed is False
    assert boundary.public_overfit_allowed is False
    assert boundary.public_overfit_guard_required is True


def test_task_3_fail_closed_boundary_is_active() -> None:
    boundary = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert boundary.fail_closed_required is True
    assert boundary.fail_closed_active is True
    assert boundary.authorization_boundary_failure_count == 0
    assert boundary.authorization_boundary_check_count == len(boundary.authorization_boundary_checks)
    assert boundary.authorization_boundary_check_count == 12


def test_task_3_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")
    second = build_milestone_15_task_3_authorization_boundary(baseline_commit="TESTBASE")

    assert first.signature == second.signature


def test_task_3_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task3"
    doc_path = tmp_path / "m15_task3.md"

    boundary, validation, paths = write_milestone_15_task_3_authorization_boundary_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert boundary.authorization_boundary_created is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-operator-decision-authorization-boundary-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["boundary_decision"] == BOUNDARY_DECISION
    assert payload["record"]["pending_decision_is_authorization"] is False
    assert payload["record"]["implementation_authorized"] is False
