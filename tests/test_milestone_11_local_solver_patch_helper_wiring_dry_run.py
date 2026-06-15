from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_wiring_dry_run import (
    EXPECTED_ADAPTER_COUNT,
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_DRY_RUN_FAILURE_COUNT,
    EXPECTED_DRY_RUN_OUTPUT_COUNT,
    EXPECTED_DRY_RUN_PASS_COUNT,
    EXPECTED_LAYER_COUNT,
    EXPECTED_RECORD_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_diagnostic_records,
    build_dry_run_bundle,
    build_dry_run_decision,
    build_dry_run_scorecard,
    build_milestone_11_local_solver_patch_helper_wiring_dry_run,
    build_task_12_source_summary,
    build_task_13_checks,
    evaluate_all_task_13_cases,
    evaluate_task_13_case,
    render_task_13_manifest,
    render_task_13_markdown,
    run_milestone_11_local_solver_patch_helper_wiring_dry_run_pipeline,
    validate_milestone_11_local_solver_patch_helper_wiring_dry_run,
    write_task_13_artifacts,
)


def test_task_13_source_summary_reads_task_12():
    source = build_task_12_source_summary()
    assert source["task_12_present"] is True
    assert source["task_12_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY"
    assert source["task_12_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-PLAN-")
    assert source["task_12_ready"] is True
    assert source["wiring_plan_ready"] is True
    assert source["wiring_performed"] is False
    assert source["next_stage_authorized_scope"] == "LOCAL_WIRING_DRY_RUN_ONLY"
    assert source["runtime_solver_modified"] is False
    assert source["ranker_runtime_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False


def test_diagnostic_records_ready():
    records = build_diagnostic_records()
    assert len(records) == EXPECTED_RECORD_COUNT
    assert all("fixture_id" in item for item in records)
    assert all("episode_id" in item for item in records)


def test_dry_run_bundle_ready():
    bundle = build_dry_run_bundle()
    assert bundle["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert bundle["record_count"] == EXPECTED_RECORD_COUNT
    assert len(bundle["layer_summary"]) == EXPECTED_LAYER_COUNT
    assert bundle["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert bundle["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert bundle["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT
    assert bundle["wiring_dry_run"] is True
    assert bundle["wiring_performed"] is False
    assert bundle["runtime_solver_modified"] is False
    assert bundle["ranker_runtime_modified"] is False


def test_dry_run_layers_pass():
    summary = build_dry_run_bundle()["layer_summary"]
    assert len(summary) == EXPECTED_LAYER_COUNT
    assert all(item["output_count"] == 6 for item in summary)
    assert all(item["pass_count"] == 6 for item in summary)
    assert all(item["failure_count"] == 0 for item in summary)
    assert all(item["dry_run_passed"] is True for item in summary)


def test_dry_run_decision_is_conservative():
    decision = build_dry_run_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["dry_run_ready"] is True
    assert decision["dry_run_passed"] is True
    assert decision["wiring_dry_run"] is True
    assert decision["wiring_performed"] is False
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_13_checks_all_pass():
    checks = build_task_13_checks()
    assert all(checks.values())


def test_each_task_13_case_passes():
    case_ids = [
        "m11_task13_source_task12_ready_v1",
        "m11_task13_records_ready_v1",
        "m11_task13_wiring_module_ready_v1",
        "m11_task13_adapter_outputs_ready_v1",
        "m11_task13_all_layers_pass_v1",
        "m11_task13_dry_run_output_count_v1",
        "m11_task13_no_runtime_mutation_v1",
        "m11_task13_score_submission_boundary_v1",
        "m11_task13_fail_closed_boundary_v1",
        "m11_task13_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_13_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_13_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_13_case("missing_task_13_case")


def test_all_task_13_cases_pass():
    results = evaluate_all_task_13_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_dry_run_scorecard_passes():
    scorecard = build_dry_run_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_13_record_ready():
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_13_ready"] is True
    assert record["dry_run_ready"] is True
    assert record["dry_run_passed"] is True
    assert record["wiring_dry_run"] is True
    assert record["wiring_performed"] is False
    assert record["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert record["layer_count"] == EXPECTED_LAYER_COUNT
    assert record["diagnostic_record_count"] == EXPECTED_RECORD_COUNT
    assert record["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert record["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert record["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["dry_run_check_count"] == EXPECTED_CHECK_COUNT
    assert record["dry_run_case_count"] == EXPECTED_CASE_COUNT
    assert record["dry_run_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["dry_run_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["dry_run_gate_count"]
    assert record["dry_run_issue_count"] == 0


def test_task_13_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    assert record["official_score_claim_allowed"] is False
    assert record["competitive_score_claim_allowed"] is False
    assert record["public_score_claim_allowed"] is False
    assert record["private_score_claim_allowed"] is False
    assert record["real_public_score_claimed"] is False
    assert record["private_score_claimed"] is False
    assert record["real_benchmark_score"] is None
    assert record["real_submission_candidate_created"] is False
    assert record["submission_json_created"] is False
    assert record["upload_package_created"] is False
    assert record["real_submission_decision"] == "NOT_AUTHORIZED"
    assert record["real_submission_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["fail_closed_active"] is True


def test_task_13_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_dry_run(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_wiring_dry_run_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_13_ready"] is True
    assert payload["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert payload["dry_run_failure_count"] == 0


def test_task_13_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    markdown = render_task_13_markdown(record)
    manifest = render_task_13_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_13_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_13_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_DRY_RUN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_WIRING_DRY_RUN=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_WIRING_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "DRY_RUN_LAYER_SUMMARY" in manifest
    assert "DRY_RUN_CASE_RESULTS" in manifest


def test_task_13_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_wiring_dry_run()
    paths = write_task_13_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["bundle_path"]).exists()
    assert Path(paths["outputs_path"]).exists()
    assert Path(paths["layer_summary_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_13_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "DRY_RUN_ONLY_NO_RUNTIME_SOLVER_MUTATION_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_13_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_wiring_dry_run()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
