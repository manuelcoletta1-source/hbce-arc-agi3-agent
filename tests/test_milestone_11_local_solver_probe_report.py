from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_probe_report import (
    EXPECTED_LAYER_REPORT_COUNT,
    EXPECTED_PATCH_BACKLOG_COUNT,
    EXPECTED_PROBE_PASS_COUNT,
    EXPECTED_PROBE_RESULT_COUNT,
    EXPECTED_REPORT_CASE_COUNT,
    EXPECTED_REPORT_CHECK_COUNT,
    EXPECTED_REPORT_FAILURE_COUNT,
    EXPECTED_REPORT_PASS_COUNT,
    EXPECTED_REPORT_SECTION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_coverage_matrix,
    build_limits_and_non_claims,
    build_milestone_11_local_solver_probe_report,
    build_report_decision,
    build_report_scorecard,
    build_report_sections,
    build_solver_patch_backlog,
    build_task_6_source_summary,
    build_task_7_checks,
    evaluate_all_task_7_cases,
    evaluate_task_7_case,
    render_task_7_manifest,
    render_task_7_markdown,
    run_milestone_11_local_solver_probe_report_pipeline,
    validate_milestone_11_local_solver_probe_report,
    write_task_7_artifacts,
)


def test_task_7_source_summary_reads_task_6():
    source = build_task_6_source_summary()
    assert source["task_6_present"] is True
    assert source["task_6_status"] == "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_READY"
    assert source["task_6_id"].startswith("MILESTONE-11-SOLVER-PROBE-INTEGRATION-")
    assert source["task_6_ready"] is True
    assert source["solver_probe_integration_created"] is True
    assert source["probe_result_count"] == 30
    assert source["probe_pass_count"] == 30
    assert source["probe_failure_count"] == 0
    assert source["diagnostic_only"] is True
    assert source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert source["runtime_solver_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_coverage_matrix_reports_all_layers():
    matrix = build_coverage_matrix()
    assert len(matrix) == EXPECTED_LAYER_REPORT_COUNT
    assert all(row["coverage"] == "COVERED_PASS" for row in matrix)
    layers = {row["layer"] for row in matrix}
    assert {"world_model", "goal_inference", "planner", "verifier", "action_policy"}.issubset(layers)
    assert all(row["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for row in matrix)


def test_limits_and_non_claims_are_blocking_where_required():
    limits = build_limits_and_non_claims()
    assert len(limits) == 5
    blocking_ids = {item["limit_id"] for item in limits if item["severity"] == "BLOCKING"}
    assert "not_official_kaggle_score_v1" in blocking_ids
    assert "no_real_submission_artifact_v1" in blocking_ids
    assert "competitive_claim_not_allowed_v1" in blocking_ids


def test_solver_patch_backlog_is_ready_and_non_scoring():
    backlog = build_solver_patch_backlog()
    assert len(backlog) == EXPECTED_PATCH_BACKLOG_COUNT
    assert all(item["priority"] == "P0" for item in backlog)
    assert all(item["status"] == "PLANNED" for item in backlog)
    assert all(item["score_claim_allowed"] is False for item in backlog)
    targets = {item["target_layer"] for item in backlog}
    assert {"world_model", "goal_inference", "planner", "verifier", "action_policy"}.issubset(targets)


def test_report_decision_is_conservative():
    decision = build_report_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["probe_results_interpreted"] is True
    assert decision["coverage_status"] == "LOCAL_DIAGNOSTIC_COVERAGE_PASS"
    assert decision["competitive_score_claim_allowed"] is False
    assert decision["official_score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_report_sections_exist():
    sections = build_report_sections()
    assert "executive_summary" in sections
    assert "measured_layers" in sections
    assert "coverage_matrix" in sections
    assert "diagnostic_interpretation" in sections
    assert "limits_and_non_claims" in sections
    assert "solver_patch_backlog" in sections
    assert "boundary_control" in sections
    assert "report_decision" in sections
    assert sections["executive_summary"]["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert sections["executive_summary"]["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert sections["boundary_control"]["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"


def test_task_7_checks_all_pass():
    checks = build_task_7_checks()
    assert all(checks.values())


def test_each_task_7_case_passes():
    case_ids = [
        "m11_task7_source_task6_ready_v1",
        "m11_task7_report_sections_ready_v1",
        "m11_task7_coverage_matrix_ready_v1",
        "m11_task7_limits_ready_v1",
        "m11_task7_patch_backlog_ready_v1",
        "m11_task7_report_decision_ready_v1",
        "m11_task7_score_boundary_preserved_v1",
        "m11_task7_submission_boundary_preserved_v1",
        "m11_task7_next_stage_valid_v1",
        "m11_task7_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_7_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_7_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_7_case("missing_task_7_case")


def test_all_task_7_cases_pass():
    results = evaluate_all_task_7_cases()
    assert len(results) == EXPECTED_REPORT_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_report_scorecard_passes():
    scorecard = build_report_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_7_record_ready():
    record = build_milestone_11_local_solver_probe_report()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_7_ready"] is True
    assert record["report_created"] is True
    assert record["report_section_count"] == EXPECTED_REPORT_SECTION_COUNT
    assert record["coverage_layer_count"] == EXPECTED_LAYER_REPORT_COUNT
    assert record["limits_count"] == 5
    assert record["patch_backlog_count"] == EXPECTED_PATCH_BACKLOG_COUNT
    assert record["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert record["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert record["probe_failure_count"] == 0
    assert record["diagnostic_only"] is True
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["report_check_count"] == EXPECTED_REPORT_CHECK_COUNT
    assert record["report_case_count"] == EXPECTED_REPORT_CASE_COUNT
    assert record["report_case_pass_count"] == EXPECTED_REPORT_PASS_COUNT
    assert record["report_case_failure_count"] == EXPECTED_REPORT_FAILURE_COUNT
    assert record["passed_gate_count"] == record["report_gate_count"]
    assert record["report_issue_count"] == 0


def test_task_7_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_probe_report()
    assert record["official_score_claim_allowed"] is False
    assert record["synthetic_fixture_score_claim_allowed"] is False
    assert record["public_score_claim_allowed"] is False
    assert record["private_score_claim_allowed"] is False
    assert record["competitive_score_claim_allowed"] is False
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
    assert record["fail_closed_active"] is True


def test_task_7_does_not_modify_runtime_solver_or_require_external_dependency():
    record = build_milestone_11_local_solver_probe_report()
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False


def test_task_7_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_probe_report()
    validation = validate_milestone_11_local_solver_probe_report(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_probe_report_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_7_ready"] is True
    assert payload["report_case_pass_count"] == EXPECTED_REPORT_PASS_COUNT
    assert payload["report_case_failure_count"] == 0


def test_task_7_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_probe_report()
    markdown = render_task_7_markdown(record)
    manifest = render_task_7_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_7_LOCAL_SOLVER_PROBE_REPORT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_7_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_KAGGLE_SCORE_SEMANTICS=NOT_A_KAGGLE_SCORE" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "COVERAGE_MATRIX" in manifest
    assert "SOLVER_PATCH_BACKLOG" in manifest
    assert "REPORT_CASE_RESULTS" in manifest


def test_task_7_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_probe_report()
    paths = write_task_7_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["coverage_path"]).exists()
    assert Path(paths["limits_path"]).exists()
    assert Path(paths["backlog_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_7_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "NOT_A_KAGGLE_SCORE" in Path(paths["index_path"]).read_text(encoding="utf-8")
    assert "patch_world_model_state_tracking_v1" in Path(paths["backlog_path"]).read_text(encoding="utf-8")


def test_task_7_metadata_safe():
    metadata = build_milestone_11_local_solver_probe_report()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_7_index_is_conservative():
    index = build_milestone_11_local_solver_probe_report()["report_index"]
    assert index["report_created"] is True
    assert index["coverage_layer_count"] == EXPECTED_LAYER_REPORT_COUNT
    assert index["patch_backlog_count"] == EXPECTED_PATCH_BACKLOG_COUNT
    assert index["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert index["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert index["probe_failure_count"] == 0
    assert index["diagnostic_only"] is True
    assert index["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert index["official_score_claim_allowed"] is False
    assert index["real_public_score_claimed"] is False
    assert index["private_score_claimed"] is False
    assert index["real_benchmark_score"] is None
    assert index["runtime_solver_modified"] is False
    assert index["external_solver_dependency"] is False
    assert index["fail_closed_active"] is True
