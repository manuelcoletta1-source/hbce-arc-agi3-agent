from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_public_game_failure_taxonomy import (
    EXPECTED_NEXT_ACTION_COUNT,
    EXPECTED_TAXONOMY_CASE_COUNT,
    EXPECTED_TAXONOMY_CHECK_COUNT,
    EXPECTED_TAXONOMY_CLASS_COUNT,
    EXPECTED_TAXONOMY_FAILURE_COUNT,
    EXPECTED_TAXONOMY_PASS_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_failure_taxonomy_interpretation,
    build_milestone_11_public_game_failure_taxonomy,
    build_next_action_plan,
    build_public_game_failure_taxonomy,
    build_task_2_source_summary,
    build_task_3_checks,
    build_taxonomy_scorecard,
    evaluate_all_task_3_cases,
    evaluate_task_3_case,
    render_task_3_manifest,
    render_task_3_markdown,
    run_milestone_11_public_game_failure_taxonomy_pipeline,
    validate_milestone_11_public_game_failure_taxonomy,
    write_task_3_artifacts,
)


def test_task_3_source_summary_reads_task_2():
    summary = build_task_2_source_summary()
    assert summary["task_2_present"] is True
    assert summary["task_2_status"] == "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY"
    assert summary["task_2_id"].startswith("MILESTONE-11-PUBLIC-GAME-INVENTORY-BASELINE-RUN-")
    assert summary["task_2_ready"] is True
    assert summary["total_file_count"] == 0
    assert summary["compatible_fixture_count"] == 0
    assert summary["has_local_public_fixtures"] is False
    assert summary["baseline_execution_performed"] is False
    assert summary["baseline_execution_mode"] == "NO_LOCAL_PUBLIC_FIXTURES"
    assert summary["baseline_status"] == "BASELINE_NOT_EXECUTED_NO_LOCAL_PUBLIC_FIXTURES"
    assert summary["real_public_score_claimed"] is False
    assert summary["private_score_claimed"] is False
    assert summary["real_benchmark_score"] is None
    assert summary["real_submission_allowed"] is False
    assert summary["kaggle_submission_sent"] is False
    assert summary["fail_closed_active"] is True


def test_failure_taxonomy_classes_are_active_constraints():
    taxonomy = build_public_game_failure_taxonomy()
    assert len(taxonomy) == EXPECTED_TAXONOMY_CLASS_COUNT
    assert all(item["active"] is True for item in taxonomy)
    ids = {item["taxonomy_id"] for item in taxonomy}
    assert "dataset_missing_v1" in ids
    assert "fixture_missing_v1" in ids
    assert "baseline_not_executed_v1" in ids
    assert "score_not_claimed_v1" in ids
    assert "solver_not_measured_v1" in ids
    assert "submission_still_blocked_v1" in ids
    assert "next_action_required_v1" in ids


def test_failure_taxonomy_interpretation_is_not_solver_failure():
    interpretation = build_failure_taxonomy_interpretation()
    assert interpretation["primary_condition"] == "NO_LOCAL_PUBLIC_FIXTURES"
    assert interpretation["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert interpretation["solver_failure_detected"] is False
    assert interpretation["dataset_constraint_detected"] is True
    assert interpretation["fixture_constraint_detected"] is True
    assert interpretation["baseline_constraint_detected"] is True
    assert interpretation["score_boundary_preserved"] is True
    assert interpretation["solver_not_measured"] is True
    assert interpretation["submission_boundary_preserved"] is True
    assert interpretation["next_action_required"] is True
    assert interpretation["safe_next_stage"] == NEXT_STAGE


def test_next_action_plan_is_safe():
    actions = build_next_action_plan()
    assert len(actions) == EXPECTED_NEXT_ACTION_COUNT
    assert all(action["implementation_required"] is True for action in actions)
    assert all(action["requires_external_api"] is False for action in actions)
    assert all(action["requires_secret"] is False for action in actions)
    assert all(action["requires_real_submission"] is False for action in actions)
    assert all(action["score_claim_allowed"] is False for action in actions)


def test_task_3_checks_all_pass():
    checks = build_task_3_checks()
    assert all(checks.values())


def test_each_task_3_case_passes():
    case_ids = [
        "m11_task3_source_task2_ready_v1",
        "m11_task3_no_local_public_fixtures_classified_v1",
        "m11_task3_baseline_not_executed_classified_v1",
        "m11_task3_score_boundary_classified_v1",
        "m11_task3_solver_not_measured_classified_v1",
        "m11_task3_submission_boundary_classified_v1",
        "m11_task3_next_actions_ready_v1",
        "m11_task3_taxonomy_not_solver_failure_v1",
        "m11_task3_next_stage_valid_v1",
        "m11_task3_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_3_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_3_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_3_case("missing_task_3_case")


def test_all_task_3_cases_pass():
    results = evaluate_all_task_3_cases()
    assert len(results) == EXPECTED_TAXONOMY_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_taxonomy_scorecard_passes():
    scorecard = build_taxonomy_scorecard()
    assert len(scorecard) == 9
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_3_record_ready():
    record = build_milestone_11_public_game_failure_taxonomy()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_3_ready"] is True
    assert record["taxonomy_created"] is True
    assert record["taxonomy_validated"] is True
    assert record["taxonomy_class_count"] == EXPECTED_TAXONOMY_CLASS_COUNT
    assert record["active_taxonomy_class_count"] == EXPECTED_TAXONOMY_CLASS_COUNT
    assert record["next_action_count"] == EXPECTED_NEXT_ACTION_COUNT
    assert record["primary_condition"] == "NO_LOCAL_PUBLIC_FIXTURES"
    assert record["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert record["solver_failure_detected"] is False
    assert record["solver_not_measured"] is True
    assert record["failure_is_constraint_not_solver_failure"] is True
    assert record["taxonomy_check_count"] == EXPECTED_TAXONOMY_CHECK_COUNT
    assert record["taxonomy_case_count"] == EXPECTED_TAXONOMY_CASE_COUNT
    assert record["taxonomy_pass_count"] == EXPECTED_TAXONOMY_PASS_COUNT
    assert record["taxonomy_failure_count"] == EXPECTED_TAXONOMY_FAILURE_COUNT
    assert record["passed_gate_count"] == record["taxonomy_gate_count"]
    assert record["taxonomy_issue_count"] == 0


def test_task_3_keeps_score_and_submission_blocked():
    record = build_milestone_11_public_game_failure_taxonomy()
    assert record["real_public_score_claimed"] is False
    assert record["private_score_claimed"] is False
    assert record["real_benchmark_score"] is None
    assert record["real_submission_candidate_created"] is False
    assert record["submission_json_created"] is False
    assert record["upload_package_created"] is False
    assert record["real_submission_decision"] == "NOT_AUTHORIZED"
    assert record["real_submission_allowed"] is False
    assert record["manual_upload_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["fail_closed_required"] is True
    assert record["fail_closed_active"] is True


def test_task_3_validation_and_pipeline_pass():
    record = build_milestone_11_public_game_failure_taxonomy()
    validation = validate_milestone_11_public_game_failure_taxonomy(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_public_game_failure_taxonomy_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_3_ready"] is True
    assert payload["taxonomy_pass_count"] == 10
    assert payload["taxonomy_failure_count"] == 0


def test_task_3_markdown_and_manifest_contain_markers():
    record = build_milestone_11_public_game_failure_taxonomy()
    markdown = render_task_3_markdown(record)
    manifest = render_task_3_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_3_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_3_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_PRIMARY_CONDITION=NO_LOCAL_PUBLIC_FIXTURES" in markdown
    assert "ARC_AGI3_MILESTONE_11_PRIMARY_CLASSIFICATION=MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE" in markdown
    assert "ARC_AGI3_MILESTONE_11_SOLVER_FAILURE_DETECTED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_SOLVER_NOT_MEASURED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "FAILURE_TAXONOMY" in manifest
    assert "NEXT_ACTION_PLAN" in manifest
    assert "TAXONOMY_VALIDATION_RESULTS" in manifest


def test_task_3_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_public_game_failure_taxonomy()
    paths = write_task_3_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["taxonomy_path"]).exists()
    assert Path(paths["next_actions_path"]).exists()
    assert Path(paths["interpretation_path"]).exists()
    assert "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_3_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE" in Path(paths["interpretation_path"]).read_text(
        encoding="utf-8"
    )


def test_task_3_metadata_safe():
    metadata = build_milestone_11_public_game_failure_taxonomy()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_3_index_is_conservative():
    index = build_milestone_11_public_game_failure_taxonomy()["taxonomy_index"]
    assert index["primary_condition"] == "NO_LOCAL_PUBLIC_FIXTURES"
    assert index["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert index["solver_failure_detected"] is False
    assert index["solver_not_measured"] is True
    assert index["taxonomy_class_count"] == EXPECTED_TAXONOMY_CLASS_COUNT
    assert index["next_action_count"] == EXPECTED_NEXT_ACTION_COUNT
    assert index["real_public_score_claimed"] is False
    assert index["private_score_claimed"] is False
    assert index["real_benchmark_score"] is None
    assert index["real_submission_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_active"] is True
