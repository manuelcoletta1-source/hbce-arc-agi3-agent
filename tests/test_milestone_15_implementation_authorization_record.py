from __future__ import annotations

import json

from hbce_arc_agi3.milestone_15_implementation_authorization_record import (
    BLOCK_REASON,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    RECORD_DECISION,
    RECORD_VERDICT,
    TASK_VALID,
    build_milestone_15_task_8_implementation_authorization_record,
    validate_milestone_15_task_8_implementation_authorization_record,
    write_milestone_15_task_8_implementation_authorization_record_artifacts,
)


def test_task_8_authorization_record_is_valid() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")
    validation = validate_milestone_15_task_8_implementation_authorization_record(record)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_8_records_task_7_decision_gate() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.task_7_decision_gate_confirmed is True
    assert record.source_task_7_final_baseline_commit == "73a7fbd"
    assert record.source_task_7_final_signature == "B2CDE3D0D82C2DD6"


def test_task_8_chain_is_correct() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.previous_stage == PREVIOUS_STAGE
    assert record.next_stage == NEXT_STAGE
    assert record.source_task_6_final_baseline_commit == "c70df02"
    assert record.source_task_6_final_signature == "D93E57F44AAF8A8E"


def test_task_8_record_decision_is_no_authorization_granted() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.record_verdict == RECORD_VERDICT
    assert record.record_decision == RECORD_DECISION
    assert record.block_reason == BLOCK_REASON


def test_task_8_operator_decision_still_pending() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.operator_decision_required is True
    assert record.operator_decision_received is False
    assert record.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"


def test_task_8_explicit_authorization_not_received() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.explicit_operator_authorization_required is True
    assert record.explicit_operator_authorization_received is False
    assert record.explicit_operator_authorization_value == "NO_EXPLICIT_OPERATOR_AUTHORIZATION_RECEIVED"


def test_task_8_implementation_authorization_record_is_negative() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.implementation_authorization_record_required is True
    assert record.implementation_authorization_recorded is True
    assert record.implementation_authorization_record_value == "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED"
    assert record.implementation_authorization_granted is False
    assert record.implementation_authorization_recorded_as_granted is False


def test_task_8_implementation_remains_blocked() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.implementation_authorized is False
    assert record.implementation_blocked is True
    assert record.implementation_performed is False
    assert record.implementation_patch_created is False
    assert record.implementation_patch_applied is False


def test_task_8_runtime_patch_and_wiring_are_not_allowed() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.runtime_solver_patch_allowed is False
    assert record.runtime_solver_modified is False
    assert record.ranker_runtime_patch_allowed is False
    assert record.ranker_runtime_modified is False
    assert record.candidate_generator_patch_allowed is False
    assert record.candidate_generator_modified is False
    assert record.runtime_wiring_allowed is False
    assert record.runtime_wiring_performed is False


def test_task_8_runtime_activation_and_execution_stay_blocked() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.runtime_activation_authorized is False
    assert record.runtime_activation_blocked is True
    assert record.runtime_activation_performed is False
    assert record.runtime_execution_allowed is False
    assert record.runtime_execution_performed is False


def test_task_8_no_real_submission_path_is_open() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.real_evaluation_performed is False
    assert record.real_submission_allowed is False
    assert record.ready_for_real_kaggle_submission is False
    assert record.manual_upload_allowed is False
    assert record.kaggle_authentication_allowed is False
    assert record.kaggle_authentication_performed is False
    assert record.kaggle_upload_allowed is False
    assert record.kaggle_upload_performed is False
    assert record.kaggle_submission_sent is False


def test_task_8_public_boundary_is_preserved() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.external_api_dependency is False
    assert record.internet_during_eval is False
    assert record.private_core_exposure is False
    assert record.legal_certification is False
    assert record.official_score_claim_allowed is False
    assert record.competitive_score_claim_allowed is False
    assert record.public_overfit_allowed is False
    assert record.public_overfit_guard_required is True


def test_task_8_fail_closed_record_is_active() -> None:
    record = build_milestone_15_task_8_implementation_authorization_record(baseline_commit="TESTBASE")

    assert record.fail_closed_required is True
    assert record.fail_closed_active is True
    assert record.implementation_authorization_record_failure_count == 0
    assert record.implementation_authorization_record_check_count == len(record.implementation_authorization_record_checks)
    assert record.implementation_authorization_record_check_count == 22


def test_task_8_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "m15_task8"
    doc_path = tmp_path / "m15_task8.md"

    record, validation, paths = write_milestone_15_task_8_implementation_authorization_record_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert record.implementation_authorization_record_created is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads(
        (output_dir / "milestone-15-implementation-authorization-record-v1.json").read_text()
    )

    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["record_decision"] == RECORD_DECISION
    assert payload["record"]["implementation_authorization_record_value"] == "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED"
    assert payload["record"]["implementation_authorization_recorded_as_granted"] is False
    assert payload["record"]["implementation_authorized"] is False
