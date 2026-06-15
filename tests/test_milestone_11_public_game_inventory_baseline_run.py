from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_public_game_inventory_baseline_run import (
    EXPECTED_CANDIDATE_PACKAGE_ID,
    EXPECTED_INVENTORY_CASE_COUNT,
    EXPECTED_INVENTORY_CHECK_COUNT,
    EXPECTED_INVENTORY_FAILURE_COUNT,
    EXPECTED_INVENTORY_PASS_COUNT,
    EXPECTED_REBUILT_CANDIDATE_ID,
    EXPECTED_SELECTED_CANDIDATE_ID,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_inventory_scorecard,
    build_m11_opening_source_summary,
    build_milestone_11_public_game_inventory_baseline_run,
    build_public_game_inventory,
    build_safe_baseline_record,
    build_task_2_checks,
    evaluate_all_task_2_cases,
    evaluate_task_2_case,
    render_task_2_manifest,
    render_task_2_markdown,
    run_milestone_11_public_game_inventory_baseline_run_pipeline,
    validate_milestone_11_public_game_inventory_baseline_run,
    write_task_2_artifacts,
)


def test_task_2_source_summary_reads_milestone_11_opening():
    summary = build_m11_opening_source_summary()
    assert summary["m11_opening_present"] is True
    assert summary["m11_opening_status"] == "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY"
    assert summary["m11_opening_id"].startswith("MILESTONE-11-PUBLIC-GAME-BENCHMARK-SOLVER-IMPROVEMENT-")
    assert summary["m11_opening_ready"] is True
    assert summary["next_stage"] == "MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_AND_BASELINE_RUN_V1"
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert summary["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert summary["real_public_score_claimed"] is False
    assert summary["private_score_claimed"] is False
    assert summary["real_submission_allowed"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["kaggle_submission_sent"] is False
    assert summary["fail_closed_active"] is True


def test_public_game_inventory_is_safe_and_deterministic():
    inventory = build_public_game_inventory()
    assert inventory["inventory_created"] is True
    assert inventory["inventory_scan_completed"] is True
    assert inventory["compatible_fixture_detection_completed"] is True
    assert inventory["candidate_path_count"] > 0
    assert isinstance(inventory["path_records"], list)
    assert isinstance(inventory["compatible_fixtures"], list)
    assert inventory["compatible_fixture_count"] == len(inventory["compatible_fixtures"])


def test_safe_baseline_record_never_claims_score():
    baseline = build_safe_baseline_record()
    assert baseline["baseline_policy_created"] is True
    assert baseline["baseline_attempt_recorded"] is True
    assert baseline["baseline_result_recorded"] is True
    assert baseline["real_public_score_claimed"] is False
    assert baseline["private_score_claimed"] is False
    assert baseline["real_benchmark_score"] is None
    assert baseline["score_boundary"] == "NO_SCORE_CLAIM_WITHOUT_OFFICIAL_VALIDATION"
    if baseline["compatible_fixture_count"] > 0:
        assert baseline["baseline_execution_performed"] is True
        assert baseline["baseline_execution_mode"] == "DRY_RUN_STRUCTURE_ONLY"
    else:
        assert baseline["baseline_execution_performed"] is False
        assert baseline["baseline_execution_mode"] == "NO_LOCAL_PUBLIC_FIXTURES"


def test_task_2_checks_all_pass():
    checks = build_task_2_checks()
    assert all(checks.values())


def test_each_task_2_case_passes():
    case_ids = [
        "m11_task2_source_opening_ready_v1",
        "m11_task2_candidate_identity_loaded_v1",
        "m11_task2_public_game_paths_scanned_v1",
        "m11_task2_compatible_fixture_detection_v1",
        "m11_task2_baseline_policy_ready_v1",
        "m11_task2_safe_baseline_record_ready_v1",
        "m11_task2_no_score_claim_without_valid_run_v1",
        "m11_task2_real_submission_blocked_v1",
        "m11_task2_next_stage_valid_v1",
        "m11_task2_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_2_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_2_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_2_case("missing_task_2_case")


def test_all_task_2_cases_pass():
    results = evaluate_all_task_2_cases()
    assert len(results) == EXPECTED_INVENTORY_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_inventory_scorecard_passes():
    scorecard = build_inventory_scorecard()
    assert len(scorecard) == 9
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_2_record_ready():
    record = build_milestone_11_public_game_inventory_baseline_run()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_2_ready"] is True
    assert record["inventory_created"] is True
    assert record["inventory_scan_completed"] is True
    assert record["compatible_fixture_detection_completed"] is True
    assert record["baseline_policy_created"] is True
    assert record["baseline_attempt_recorded"] is True
    assert record["baseline_result_recorded"] is True
    assert record["inventory_check_count"] == EXPECTED_INVENTORY_CHECK_COUNT
    assert record["inventory_case_count"] == EXPECTED_INVENTORY_CASE_COUNT
    assert record["inventory_pass_count"] == EXPECTED_INVENTORY_PASS_COUNT
    assert record["inventory_failure_count"] == EXPECTED_INVENTORY_FAILURE_COUNT
    assert record["passed_gate_count"] == record["inventory_gate_count"]
    assert record["inventory_issue_count"] == 0


def test_task_2_keeps_submission_and_score_blocked():
    record = build_milestone_11_public_game_inventory_baseline_run()
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


def test_task_2_validation_and_pipeline_pass():
    record = build_milestone_11_public_game_inventory_baseline_run()
    validation = validate_milestone_11_public_game_inventory_baseline_run(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_public_game_inventory_baseline_run_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_2_ready"] is True
    assert payload["inventory_pass_count"] == 10
    assert payload["inventory_failure_count"] == 0


def test_task_2_markdown_and_manifest_contain_markers():
    record = build_milestone_11_public_game_inventory_baseline_run()
    markdown = render_task_2_markdown(record)
    manifest = render_task_2_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_2_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_INVENTORY_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PUBLIC_GAME_PATH_RECORDS" in manifest
    assert "INVENTORY_VALIDATION_RESULTS" in manifest


def test_task_2_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_public_game_inventory_baseline_run()
    paths = write_task_2_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["inventory_path"]).exists()
    assert Path(paths["baseline_path"]).exists()
    assert "MILESTONE_11_PUBLIC_GAME_INVENTORY_BASELINE_RUN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_2_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "PUBLIC_GAME_INVENTORY_BASELINE_RUN_READY_FOR_FAILURE_TAXONOMY" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_task_2_metadata_safe():
    metadata = build_milestone_11_public_game_inventory_baseline_run()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_2_index_is_conservative():
    index = build_milestone_11_public_game_inventory_baseline_run()["inventory_index"]
    assert index["inventory_created"] is True
    assert index["inventory_scan_completed"] is True
    assert index["baseline_status"] in {
        "BASELINE_DRY_RUN_RECORDED",
        "BASELINE_NOT_EXECUTED_NO_LOCAL_PUBLIC_FIXTURES",
    }
    assert index["real_public_score_claimed"] is False
    assert index["private_score_claimed"] is False
    assert index["real_benchmark_score"] is None
    assert index["real_submission_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_active"] is True
