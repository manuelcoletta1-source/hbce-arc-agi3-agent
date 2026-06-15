from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_solver_probe_integration import (
    EXPECTED_PROBE_CASE_COUNT,
    EXPECTED_PROBE_CHECK_COUNT,
    EXPECTED_PROBE_COMPONENT_COUNT,
    EXPECTED_PROBE_FAILURE_COUNT,
    EXPECTED_PROBE_PASS_COUNT,
    EXPECTED_PROBE_RESULT_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_milestone_11_solver_probe_integration,
    build_probe_layer_report,
    build_probe_scorecard,
    build_probe_summary,
    build_solver_probe_contract,
    build_solver_probe_results,
    build_task_5_source_summary,
    build_task_6_checks,
    evaluate_all_task_6_cases,
    evaluate_probe_component,
    evaluate_task_6_case,
    render_task_6_manifest,
    render_task_6_markdown,
    run_milestone_11_solver_probe_integration_pipeline,
    validate_milestone_11_solver_probe_integration,
    write_task_6_artifacts,
)


def test_task_6_source_summary_reads_task_5():
    source = build_task_5_source_summary()
    assert source["task_5_present"] is True
    assert source["task_5_status"] == "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY"
    assert source["task_5_id"].startswith("MILESTONE-11-LOCAL-DIAGNOSTIC-FIXTURE-HARNESS-")
    assert source["task_5_ready"] is True
    assert source["fixture_schema_created"] is True
    assert source["fixture_count"] == 6
    assert source["episode_count"] == 6
    assert source["trace_record_count"] == 6
    assert source["diagnostic_result_guard_active"] is True
    assert source["diagnostic_only"] is True
    assert source["diagnostic_result_guard"]["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert source["real_public_score_claimed"] is False
    assert source["private_score_claimed"] is False
    assert source["real_benchmark_score"] is None
    assert source["real_submission_allowed"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_solver_probe_contract_is_safe():
    contract = build_solver_probe_contract()
    assert contract["contract_id"] == "M11-TASK6-SOLVER-PROBE-CONTRACT-v1"
    assert len(contract["probe_components"]) == EXPECTED_PROBE_COMPONENT_COUNT
    assert contract["diagnostic_only"] is True
    assert contract["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert contract["official_score_claim_allowed"] is False
    assert contract["synthetic_fixture_score_claim_allowed"] is False
    assert contract["public_score_claim_allowed"] is False
    assert contract["private_score_claim_allowed"] is False
    assert contract["runtime_solver_modified"] is False
    assert contract["ranker_runtime_modified"] is False
    assert contract["external_solver_dependency"] is False


def test_probe_results_created_for_all_episodes_and_components():
    results = build_solver_probe_results()
    assert len(results) == EXPECTED_PROBE_RESULT_COUNT
    assert all(result["diagnostic_only"] is True for result in results)
    assert all(result["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for result in results)
    assert all(result["score_claim_allowed"] is False for result in results)
    assert all(result["official_score_claim_allowed"] is False for result in results)
    assert all(result["diagnostic_probe_passed"] is True for result in results)
    assert all(result["diagnostic_probe_score"] == 100 for result in results)


def test_evaluate_probe_component_unknown_probe_fails_closed():
    source = build_task_5_source_summary()
    episode = source["episode_results"][0]
    result = evaluate_probe_component(
        episode,
        {"probe_id": "unknown_probe_v1", "target_layer": "unknown", "purpose": "fail closed"},
    )
    assert result["diagnostic_probe_passed"] is False
    assert result["diagnostic_probe_score"] == 0
    assert result["diagnostic_only"] is True
    assert result["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"


def test_probe_summary_counts_pass():
    summary = build_probe_summary()
    assert summary["probe_component_count"] == EXPECTED_PROBE_COMPONENT_COUNT
    assert summary["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert summary["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert summary["probe_failure_count"] == EXPECTED_PROBE_FAILURE_COUNT
    assert summary["diagnostic_only"] is True
    assert summary["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert summary["official_score_claim_allowed"] is False


def test_probe_layer_report_counts_pass():
    report = build_probe_layer_report()
    assert len(report) == EXPECTED_PROBE_COMPONENT_COUNT
    assert all(row["result_count"] == 6 for row in report)
    assert all(row["pass_count"] == 6 for row in report)
    assert all(row["failure_count"] == 0 for row in report)
    assert all(row["diagnostic_only"] is True for row in report)
    assert all(row["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for row in report)
    layers = {row["target_layer"] for row in report}
    assert "world_model" in layers
    assert "goal_inference" in layers
    assert "planner" in layers
    assert "verifier" in layers
    assert "action_policy" in layers


def test_task_6_checks_all_pass():
    checks = build_task_6_checks()
    assert all(checks.values())


def test_each_task_6_case_passes():
    case_ids = [
        "m11_task6_source_task5_ready_v1",
        "m11_task6_probe_components_ready_v1",
        "m11_task6_probe_results_ready_v1",
        "m11_task6_world_model_probe_ready_v1",
        "m11_task6_goal_inference_probe_ready_v1",
        "m11_task6_planner_probe_ready_v1",
        "m11_task6_transition_verifier_probe_ready_v1",
        "m11_task6_action_policy_probe_ready_v1",
        "m11_task6_score_and_submission_boundary_v1",
        "m11_task6_next_stage_valid_v1",
        "m11_task6_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_6_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_6_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_6_case("missing_task_6_case")


def test_all_task_6_cases_pass():
    results = evaluate_all_task_6_cases()
    assert len(results) == EXPECTED_PROBE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_probe_scorecard_passes():
    scorecard = build_probe_scorecard()
    assert len(scorecard) == 11
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_6_record_ready():
    record = build_milestone_11_solver_probe_integration()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_6_ready"] is True
    assert record["solver_probe_contract_created"] is True
    assert record["solver_probe_integration_created"] is True
    assert record["probe_component_count"] == EXPECTED_PROBE_COMPONENT_COUNT
    assert record["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert record["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert record["probe_failure_count"] == EXPECTED_PROBE_FAILURE_COUNT
    assert record["layer_report_count"] == EXPECTED_PROBE_COMPONENT_COUNT
    assert record["local_solver_diagnostic_measured"] is True
    assert record["diagnostic_only"] is True
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["probe_check_count"] == EXPECTED_PROBE_CHECK_COUNT
    assert record["probe_case_count"] == EXPECTED_PROBE_CASE_COUNT
    assert record["probe_case_pass_count"] == EXPECTED_PROBE_CASE_COUNT
    assert record["probe_case_failure_count"] == 0
    assert record["passed_gate_count"] == record["probe_gate_count"]
    assert record["probe_issue_count"] == 0


def test_task_6_keeps_score_and_submission_blocked():
    record = build_milestone_11_solver_probe_integration()
    assert record["official_score_claim_allowed"] is False
    assert record["synthetic_fixture_score_claim_allowed"] is False
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
    assert record["manual_upload_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["fail_closed_required"] is True
    assert record["fail_closed_active"] is True


def test_task_6_does_not_modify_runtime_solver_or_require_external_dependency():
    record = build_milestone_11_solver_probe_integration()
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False


def test_task_6_validation_and_pipeline_pass():
    record = build_milestone_11_solver_probe_integration()
    validation = validate_milestone_11_solver_probe_integration(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_solver_probe_integration_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_6_ready"] is True
    assert payload["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert payload["probe_failure_count"] == 0


def test_task_6_markdown_and_manifest_contain_markers():
    record = build_milestone_11_solver_probe_integration()
    markdown = render_task_6_markdown(record)
    manifest = render_task_6_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_6_SOLVER_PROBE_INTEGRATION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_6_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_SOLVER_PROBE_INTEGRATION_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_KAGGLE_SCORE_SEMANTICS=NOT_A_KAGGLE_SCORE" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PROBE_COMPONENTS" in manifest
    assert "PROBE_LAYER_REPORT" in manifest
    assert "PROBE_CASE_RESULTS" in manifest


def test_task_6_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_solver_probe_integration()
    paths = write_task_6_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["contract_path"]).exists()
    assert Path(paths["components_path"]).exists()
    assert Path(paths["results_path"]).exists()
    assert Path(paths["layer_report_path"]).exists()
    assert Path(paths["summary_path"]).exists()
    assert "MILESTONE_11_SOLVER_PROBE_INTEGRATION_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_6_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "NOT_A_KAGGLE_SCORE" in Path(paths["contract_path"]).read_text(encoding="utf-8")
    assert "world_model_probe_v1" in Path(paths["components_path"]).read_text(encoding="utf-8")


def test_task_6_metadata_safe():
    metadata = build_milestone_11_solver_probe_integration()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_6_index_is_conservative():
    index = build_milestone_11_solver_probe_integration()["probe_index"]
    assert index["solver_probe_contract_created"] is True
    assert index["solver_probe_integration_created"] is True
    assert index["probe_component_count"] == EXPECTED_PROBE_COMPONENT_COUNT
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
