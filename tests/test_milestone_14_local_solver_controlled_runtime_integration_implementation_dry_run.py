from __future__ import annotations

import json

from hbce_arc_agi3.milestone_14_local_solver_controlled_runtime_integration_implementation_dry_run import (
    DRY_RUN_VERDICT,
    NEXT_STAGE,
    TASK_MODE,
    TASK_VALID,
    build_milestone_14_task_5_dry_run_record,
    validate_milestone_14_task_5_dry_run_record,
    write_milestone_14_task_5_dry_run_artifacts,
)


def test_task_5_dry_run_record_is_valid() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")
    validation = validate_milestone_14_task_5_dry_run_record(record)

    assert validation.valid is True
    assert validation.status == TASK_VALID
    assert validation.issue_count == 0


def test_task_5_dry_run_verdict_and_next_stage() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert record.task_mode == TASK_MODE
    assert record.dry_run_verdict == DRY_RUN_VERDICT
    assert record.next_stage == NEXT_STAGE
    assert record.implementation_dry_run_performed is True
    assert record.dry_run_projection_created is True


def test_task_5_counts_match_contract() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert record.target_module_count == 5
    assert record.implementation_step_count == 10
    assert record.integration_contract_count == 8
    assert record.regression_test_count == 8
    assert record.rollback_item_count == 5
    assert record.dry_run_check_count == 24
    assert record.dry_run_failure_count == 0
    assert record.dry_run_pass_count == 24


def test_task_5_runtime_and_submission_are_blocked() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert record.runtime_activation_performed is False
    assert record.runtime_execution_performed is False
    assert record.runtime_solver_modified is False
    assert record.ranker_runtime_modified is False
    assert record.candidate_generator_modified is False
    assert record.implementation_performed is False
    assert record.real_evaluation_performed is False
    assert record.real_submission_allowed is False
    assert record.ready_for_real_kaggle_submission is False


def test_task_5_kaggle_boundary_is_closed() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert record.kaggle_authentication_allowed is False
    assert record.kaggle_authentication_performed is False
    assert record.kaggle_upload_allowed is False
    assert record.kaggle_upload_performed is False
    assert record.kaggle_submission_sent is False
    assert record.kaggle_score_semantics == "NOT_A_KAGGLE_SCORE"


def test_task_5_public_boundary_is_safe() -> None:
    record = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert record.local_only is True
    assert record.deterministic is True
    assert record.public_safe is True
    assert record.external_api_dependency is False
    assert record.internet_during_eval is False
    assert record.private_core_exposure is False
    assert record.legal_certification is False
    assert record.public_overfit_allowed is False
    assert record.public_overfit_guard_required is True


def test_task_5_writes_artifacts(tmp_path) -> None:
    output_dir = tmp_path / "artifacts"
    doc_path = tmp_path / "doc.md"

    record, validation, paths = write_milestone_14_task_5_dry_run_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert record.implementation_dry_run_performed is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads((output_dir / "milestone-14-local-solver-controlled-runtime-integration-implementation-dry-run-v1.json").read_text())
    assert payload["validation"]["status"] == TASK_VALID
    assert payload["record"]["dry_run_verdict"] == DRY_RUN_VERDICT


def test_task_5_signature_is_deterministic_for_same_baseline() -> None:
    first = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")
    second = build_milestone_14_task_5_dry_run_record(baseline_commit="TESTBASE")

    assert first.signature == second.signature
