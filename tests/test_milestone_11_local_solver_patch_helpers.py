from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helpers import (
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_HELPER_COUNT,
    EXPECTED_HINT_COUNT_PER_LAYER,
    EXPECTED_RECORD_COUNT,
    EXPECTED_TOTAL_HINT_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_diagnostic_records,
    build_helper_layer_summary,
    build_helper_outputs,
    build_helper_scorecard,
    build_milestone_11_local_solver_patch_helpers,
    build_task_9_source_summary,
    build_task_10_checks,
    build_task_10_decision,
    evaluate_all_task_10_cases,
    evaluate_task_10_case,
    render_task_10_manifest,
    render_task_10_markdown,
    run_milestone_11_local_solver_patch_helpers_pipeline,
    validate_milestone_11_local_solver_patch_helpers,
    write_task_10_artifacts,
)


def test_task_10_source_summary_reads_task_9():
    source = build_task_9_source_summary()
    assert source["task_9_present"] is True
    assert source["task_9_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY"
    assert source["task_9_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-IMPLEMENTATION-PLAN-")
    assert source["task_9_ready"] is True
    assert source["implementation_plan_ready"] is True
    assert source["next_stage_authorized_scope"] == "PATCH_HELPERS_ONLY"
    assert source["runtime_solver_modified"] is False
    assert source["ranker_runtime_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_diagnostic_records_load_from_task5():
    records = build_diagnostic_records()
    assert len(records) == EXPECTED_RECORD_COUNT
    assert all("fixture_id" in item for item in records)
    assert all("episode_id" in item for item in records)


def test_helper_outputs_have_all_layers():
    outputs = build_helper_outputs()
    assert outputs["bundle"]["status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_READY"
    assert len(outputs["world_model_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER
    assert len(outputs["goal_inference_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER
    assert len(outputs["planner_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER
    assert len(outputs["transition_verifier_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER
    assert len(outputs["action_policy_hints"]) == EXPECTED_HINT_COUNT_PER_LAYER


def test_helper_layer_summary_ready():
    summary = build_helper_layer_summary()
    assert len(summary) == EXPECTED_HELPER_COUNT
    assert all(item["hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER for item in summary)
    assert all(item["diagnostic_only"] is True for item in summary)
    assert all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in summary)
    assert all(item["score_claim_allowed"] is False for item in summary)


def test_task_10_decision_is_conservative():
    decision = build_task_10_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["helper_implementation_ready"] is True
    assert decision["helper_scope"] == "PATCH_HELPERS_ONLY"
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_10_checks_all_pass():
    checks = build_task_10_checks()
    assert all(checks.values())


def test_each_task_10_case_passes():
    case_ids = [
        "m11_task10_source_task9_ready_v1",
        "m11_task10_helper_module_ready_v1",
        "m11_task10_world_model_hints_ready_v1",
        "m11_task10_goal_inference_hints_ready_v1",
        "m11_task10_planner_hints_ready_v1",
        "m11_task10_verifier_hints_ready_v1",
        "m11_task10_action_policy_hints_ready_v1",
        "m11_task10_score_submission_boundary_v1",
        "m11_task10_next_stage_valid_v1",
        "m11_task10_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_10_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_10_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_10_case("missing_task_10_case")


def test_all_task_10_cases_pass():
    results = evaluate_all_task_10_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_helper_scorecard_passes():
    scorecard = build_helper_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_10_record_ready():
    record = build_milestone_11_local_solver_patch_helpers()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_10_ready"] is True
    assert record["helper_implementation_ready"] is True
    assert record["helper_count"] == EXPECTED_HELPER_COUNT
    assert record["diagnostic_record_count"] == EXPECTED_RECORD_COUNT
    assert record["total_hint_count"] == EXPECTED_TOTAL_HINT_COUNT
    assert record["world_model_hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER
    assert record["goal_inference_hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER
    assert record["planner_hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER
    assert record["transition_verifier_hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER
    assert record["action_policy_hint_count"] == EXPECTED_HINT_COUNT_PER_LAYER
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["helper_check_count"] == EXPECTED_CHECK_COUNT
    assert record["helper_case_count"] == EXPECTED_CASE_COUNT
    assert record["helper_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["helper_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["helper_gate_count"]
    assert record["helper_issue_count"] == 0


def test_task_10_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helpers()
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


def test_task_10_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helpers()
    validation = validate_milestone_11_local_solver_patch_helpers(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helpers_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_10_ready"] is True
    assert payload["helper_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert payload["helper_case_failure_count"] == 0


def test_task_10_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helpers()
    markdown = render_task_10_markdown(record)
    manifest = render_task_10_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_10_LOCAL_SOLVER_PATCH_HELPERS_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_10_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "HELPER_LAYER_SUMMARY" in manifest
    assert "HELPER_CASE_RESULTS" in manifest


def test_task_10_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helpers()
    paths = write_task_10_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["bundle_path"]).exists()
    assert Path(paths["layer_summary_path"]).exists()
    assert Path(paths["world_model_path"]).exists()
    assert Path(paths["goal_inference_path"]).exists()
    assert Path(paths["planner_path"]).exists()
    assert Path(paths["verifier_path"]).exists()
    assert Path(paths["action_policy_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPERS_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_10_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "PATCH_HELPERS_ONLY" in Path(paths["decision_path"]).read_text(encoding="utf-8")


def test_task_10_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helpers()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
