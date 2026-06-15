from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_probe_run import (
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_HINT_COUNT_PER_LAYER,
    EXPECTED_LAYER_COUNT,
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
    build_helper_probe_decision,
    build_helper_probe_layer_summary,
    build_helper_probe_results,
    build_helper_probe_scorecard,
    build_milestone_11_local_solver_patch_helper_probe_run,
    build_task_10_source_summary,
    build_task_11_checks,
    evaluate_all_task_11_cases,
    evaluate_task_11_case,
    render_task_11_manifest,
    render_task_11_markdown,
    run_milestone_11_local_solver_patch_helper_probe_run_pipeline,
    validate_milestone_11_local_solver_patch_helper_probe_run,
    write_task_11_artifacts,
)


def test_task_11_source_summary_reads_task_10():
    source = build_task_10_source_summary()
    assert source["task_10_present"] is True
    assert source["task_10_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_READY"
    assert source["task_10_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPERS-")
    assert source["task_10_ready"] is True
    assert source["helper_implementation_ready"] is True
    assert source["helper_count"] == EXPECTED_LAYER_COUNT
    assert source["total_hint_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert source["runtime_solver_modified"] is False
    assert source["ranker_runtime_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_helper_probe_results_ready():
    results = build_helper_probe_results()
    assert len(results) == EXPECTED_PROBE_RESULT_COUNT
    assert all(item["passed"] is True for item in results)
    assert all(item["evidence_score"] == 100 for item in results)
    assert all(item["diagnostic_only"] is True for item in results)
    assert all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in results)
    assert all(item["score_claim_allowed"] is False for item in results)
    assert all(item["submission_artifact_allowed"] is False for item in results)
    assert all(item["runtime_solver_modified"] is False for item in results)
    assert all(item["ranker_runtime_modified"] is False for item in results)


def test_helper_probe_layer_summary_passes():
    summary = build_helper_probe_layer_summary()
    assert len(summary) == EXPECTED_LAYER_COUNT
    assert all(item["probe_result_count"] == EXPECTED_HINT_COUNT_PER_LAYER for item in summary)
    assert all(item["probe_pass_count"] == EXPECTED_HINT_COUNT_PER_LAYER for item in summary)
    assert all(item["probe_failure_count"] == 0 for item in summary)
    assert all(item["layer_probe_passed"] is True for item in summary)
    assert {item["target_layer"] for item in summary} == {
        "world_model",
        "goal_inference",
        "planner",
        "verifier",
        "action_policy",
    }


def test_helper_probe_decision_is_conservative():
    decision = build_helper_probe_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["helper_probe_run_ready"] is True
    assert decision["helper_probe_run_passed"] is True
    assert decision["helper_runtime_wiring_performed"] is False
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_11_checks_all_pass():
    checks = build_task_11_checks()
    assert all(checks.values())


def test_each_task_11_case_passes():
    case_ids = [
        "m11_task11_source_task10_ready_v1",
        "m11_task11_probe_inputs_ready_v1",
        "m11_task11_probe_results_ready_v1",
        "m11_task11_world_model_probe_pass_v1",
        "m11_task11_goal_inference_probe_pass_v1",
        "m11_task11_planner_probe_pass_v1",
        "m11_task11_verifier_probe_pass_v1",
        "m11_task11_action_policy_probe_pass_v1",
        "m11_task11_score_submission_boundary_v1",
        "m11_task11_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_11_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_11_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_11_case("missing_task_11_case")


def test_all_task_11_cases_pass():
    results = evaluate_all_task_11_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_helper_probe_scorecard_passes():
    scorecard = build_helper_probe_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_11_record_ready():
    record = build_milestone_11_local_solver_patch_helper_probe_run()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_11_ready"] is True
    assert record["helper_probe_run_ready"] is True
    assert record["helper_probe_run_passed"] is True
    assert record["helper_runtime_wiring_performed"] is False
    assert record["layer_count"] == EXPECTED_LAYER_COUNT
    assert record["probe_result_count"] == EXPECTED_PROBE_RESULT_COUNT
    assert record["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert record["probe_failure_count"] == EXPECTED_PROBE_FAILURE_COUNT
    assert record["world_model_probe_passed"] is True
    assert record["goal_inference_probe_passed"] is True
    assert record["planner_probe_passed"] is True
    assert record["verifier_probe_passed"] is True
    assert record["action_policy_probe_passed"] is True
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["helper_probe_check_count"] == EXPECTED_CHECK_COUNT
    assert record["helper_probe_case_count"] == EXPECTED_CASE_COUNT
    assert record["helper_probe_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["helper_probe_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["helper_probe_gate_count"]
    assert record["helper_probe_issue_count"] == 0


def test_task_11_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_probe_run()
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


def test_task_11_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_probe_run()
    validation = validate_milestone_11_local_solver_patch_helper_probe_run(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_probe_run_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_11_ready"] is True
    assert payload["probe_pass_count"] == EXPECTED_PROBE_PASS_COUNT
    assert payload["probe_failure_count"] == 0


def test_task_11_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_probe_run()
    markdown = render_task_11_markdown(record)
    manifest = render_task_11_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_11_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_HELPER_PROBE_RUN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_HELPER_RUNTIME_WIRING_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "HELPER_PROBE_LAYER_SUMMARY" in manifest
    assert "HELPER_PROBE_CASE_RESULTS" in manifest


def test_task_11_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_probe_run()
    paths = write_task_11_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["results_path"]).exists()
    assert Path(paths["layer_summary_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_11_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "PROBE_RUN_ONLY_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(paths["decision_path"]).read_text(
        encoding="utf-8"
    )


def test_task_11_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_probe_run()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
