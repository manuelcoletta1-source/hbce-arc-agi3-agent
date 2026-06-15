from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_public_game_benchmark_solver_improvement import (
    EXPECTED_BENCHMARK_AXIS_COUNT,
    EXPECTED_CANDIDATE_PACKAGE_ID,
    EXPECTED_MILESTONE_CASE_COUNT,
    EXPECTED_MILESTONE_CHECK_COUNT,
    EXPECTED_MILESTONE_FAILURE_COUNT,
    EXPECTED_MILESTONE_PASS_COUNT,
    EXPECTED_REBUILT_CANDIDATE_ID,
    EXPECTED_REBUILT_CANDIDATE_REVIEW_ID,
    EXPECTED_SELECTED_CANDIDATE_ID,
    EXPECTED_SOLVER_TARGET_COUNT,
    MILESTONE_MODE,
    MILESTONE_SCOPE,
    MILESTONE_VERDICT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    VALIDATION_STATUS,
    build_m10_closure_source_summary,
    build_milestone_11_checks,
    build_milestone_11_public_game_benchmark_solver_improvement,
    build_milestone_11_scorecard,
    build_public_game_benchmark_policy,
    build_solver_improvement_backlog,
    detect_local_public_game_paths,
    evaluate_all_milestone_11_cases,
    evaluate_milestone_11_case,
    render_milestone_11_manifest,
    render_milestone_11_markdown,
    run_milestone_11_public_game_benchmark_solver_improvement_pipeline,
    validate_milestone_11_public_game_benchmark_solver_improvement,
    write_milestone_11_artifacts,
)


def test_m11_source_summary_reads_milestone_10_closure():
    summary = build_m10_closure_source_summary()
    assert summary["m10_closure_present"] is True
    assert summary["m10_closure_status"] == "MILESTONE_10_SUBMISSION_PREPARATION_CLOSURE_V1_READY"
    assert summary["m10_closure_id"].startswith("MILESTONE-10-SUBMISSION-PREPARATION-CLOSURE-")
    assert summary["m10_closure_ready"] is True
    assert summary["m10_closure_created"] is True
    assert summary["m10_closure_passed"] is True
    assert summary["m10_closed"] is True
    assert summary["local_package_prepared"] is True
    assert summary["local_package_frozen"] is True
    assert summary["integrity_verified"] is True
    assert summary["final_audit_passed"] is True
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert summary["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert summary["rebuilt_candidate_review_id"] == EXPECTED_REBUILT_CANDIDATE_REVIEW_ID
    assert summary["real_submission_allowed"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["kaggle_submission_sent"] is False
    assert summary["fail_closed_active"] is True


def test_detect_local_public_game_paths_is_safe():
    records = detect_local_public_game_paths()
    assert len(records) > 0
    assert all("path" in item for item in records)
    assert all("exists" in item for item in records)
    assert all("file_count" in item for item in records)


def test_public_game_benchmark_policy_does_not_claim_score():
    policy = build_public_game_benchmark_policy()
    assert policy["public_game_inventory_created"] is True
    assert policy["public_game_dataset_required_now"] is False
    assert policy["public_game_benchmark_execution_allowed"] is True
    assert policy["public_game_benchmark_execution_performed"] is False
    assert policy["real_public_score_claimed"] is False
    assert policy["private_score_claimed"] is False
    assert policy["kaggle_submission_required_now"] is False
    assert policy["boundary"] == "NO_SCORE_CLAIM_WITHOUT_LOCAL_PUBLIC_RUN"


def test_solver_improvement_backlog_is_complete_and_safe():
    backlog = build_solver_improvement_backlog()
    assert len(backlog) == EXPECTED_SOLVER_TARGET_COUNT
    assert all(item["implementation_required"] is True for item in backlog)
    assert all(item["public_safe"] is True for item in backlog)
    assert all(item["requires_external_api"] is False for item in backlog)
    assert all(item["requires_secret"] is False for item in backlog)
    assert all(item["requires_real_submission"] is False for item in backlog)


def test_milestone_11_checks_all_pass():
    checks = build_milestone_11_checks()
    assert all(checks.values())


def test_each_milestone_11_case_passes():
    case_ids = [
        "m11_public_game_benchmark_source_closure_ready_v1",
        "m11_public_game_benchmark_candidate_identity_loaded_v1",
        "m11_public_game_benchmark_axes_ready_v1",
        "m11_solver_improvement_targets_ready_v1",
        "m11_public_game_inventory_policy_ready_v1",
        "m11_no_score_claimed_without_public_run_v1",
        "m11_real_submission_blocked_v1",
        "m11_fail_closed_preserved_v1",
        "m11_next_stage_valid_v1",
        "m11_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_milestone_11_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_milestone_11_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_milestone_11_case("missing_milestone_11_case")


def test_all_milestone_11_cases_pass():
    results = evaluate_all_milestone_11_cases()
    assert len(results) == EXPECTED_MILESTONE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_milestone_11_scorecard_passes():
    scorecard = build_milestone_11_scorecard()
    assert len(scorecard) == 8
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_milestone_11_record_ready():
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    assert record["status"] == STATUS
    assert record["milestone_mode"] == MILESTONE_MODE
    assert record["milestone_scope"] == MILESTONE_SCOPE
    assert record["milestone_verdict"] == MILESTONE_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["milestone_11_ready"] is True
    assert record["benchmark_axis_count"] == EXPECTED_BENCHMARK_AXIS_COUNT
    assert record["solver_improvement_target_count"] == EXPECTED_SOLVER_TARGET_COUNT
    assert record["milestone_check_count"] == EXPECTED_MILESTONE_CHECK_COUNT
    assert record["milestone_case_count"] == EXPECTED_MILESTONE_CASE_COUNT
    assert record["milestone_pass_count"] == EXPECTED_MILESTONE_PASS_COUNT
    assert record["milestone_failure_count"] == EXPECTED_MILESTONE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["milestone_gate_count"]
    assert record["milestone_issue_count"] == 0


def test_milestone_11_keeps_submission_blocked():
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    assert record["public_game_benchmark_execution_performed"] is False
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


def test_milestone_11_validation_and_pipeline_pass():
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    validation = validate_milestone_11_public_game_benchmark_solver_improvement(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_public_game_benchmark_solver_improvement_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["milestone_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["milestone_11_ready"] is True
    assert payload["milestone_pass_count"] == 10
    assert payload["milestone_failure_count"] == 0


def test_milestone_11_markdown_and_manifest_contain_markers():
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    markdown = render_milestone_11_markdown(record)
    manifest = render_milestone_11_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "BENCHMARK_AXES" in manifest
    assert "SOLVER_IMPROVEMENT_BACKLOG" in manifest
    assert "MILESTONE_11_VALIDATION_RESULTS" in manifest


def test_milestone_11_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_public_game_benchmark_solver_improvement()
    paths = write_milestone_11_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["backlog_path"]).exists()
    assert "MILESTONE_11_PUBLIC_GAME_BENCHMARK_SOLVER_IMPROVEMENT_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "MILESTONE_11_READY_FOR_PUBLIC_GAME_BENCHMARK_AND_SOLVER_PATCH_CYCLE" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_milestone_11_metadata_safe():
    metadata = build_milestone_11_public_game_benchmark_solver_improvement()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_milestone_11_index_is_conservative():
    index = build_milestone_11_public_game_benchmark_solver_improvement()["milestone_index"]
    assert index["milestone_11_ready"] is True
    assert index["public_game_inventory_created"] is True
    assert index["public_game_benchmark_execution_performed"] is False
    assert index["real_public_score_claimed"] is False
    assert index["solver_improvement_target_count"] == EXPECTED_SOLVER_TARGET_COUNT
    assert index["benchmark_axis_count"] == EXPECTED_BENCHMARK_AXIS_COUNT
    assert index["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert index["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert index["rebuilt_candidate_id"] == EXPECTED_REBUILT_CANDIDATE_ID
    assert index["next_stage"] == NEXT_STAGE
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_active"] is True
