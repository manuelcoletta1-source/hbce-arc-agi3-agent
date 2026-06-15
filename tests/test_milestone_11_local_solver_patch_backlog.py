from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_backlog import (
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_GATE_COUNT,
    EXPECTED_PATCH_COUNT,
    EXPECTED_REQUIRED_TEST_COUNT,
    EXPECTED_RISK_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_backlog_scorecard,
    build_milestone_11_local_solver_patch_backlog,
    build_patch_backlog_decision,
    build_patch_candidates,
    build_patch_execution_gates,
    build_patch_risk_register,
    build_required_test_plan,
    build_task_7_source_summary,
    build_task_8_checks,
    evaluate_all_task_8_cases,
    evaluate_task_8_case,
    render_task_8_manifest,
    render_task_8_markdown,
    run_milestone_11_local_solver_patch_backlog_pipeline,
    validate_milestone_11_local_solver_patch_backlog,
    write_task_8_artifacts,
)


def test_task_8_source_summary_reads_task_7():
    source = build_task_7_source_summary()
    assert source["task_7_present"] is True
    assert source["task_7_status"] == "MILESTONE_11_LOCAL_SOLVER_PROBE_REPORT_V1_READY"
    assert source["task_7_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PROBE-REPORT-")
    assert source["task_7_ready"] is True
    assert source["report_created"] is True
    assert source["patch_backlog_count"] == EXPECTED_PATCH_COUNT
    assert source["diagnostic_only"] is True
    assert source["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert source["runtime_solver_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_patch_candidates_are_executable_backlog_only():
    candidates = build_patch_candidates()
    assert len(candidates) == EXPECTED_PATCH_COUNT
    assert all(item["priority"] == "P0" for item in candidates)
    assert all(item["file_target"] == "src/hbce_arc_agi3/solver_patch_helpers.py" for item in candidates)
    assert all(item["function_target"] for item in candidates)
    assert all(item["test_target"] for item in candidates)
    assert all(item["patch_status"] == "READY_FOR_IMPLEMENTATION_PLAN" for item in candidates)
    assert all(item["implementation_allowed_now"] is False for item in candidates)
    assert all(item["runtime_solver_patch_applied"] is False for item in candidates)
    assert all(item["score_claim_allowed"] is False for item in candidates)


def test_required_test_plan_is_ready():
    tests = build_required_test_plan()
    assert len(tests) == EXPECTED_REQUIRED_TEST_COUNT
    assert all(item["required"] is True for item in tests)
    assert all(item["local_only"] is True for item in tests)
    assert all(item["external_api_dependency"] is False for item in tests)
    assert all(item["score_claim_allowed"] is False for item in tests)
    assert any("tests/test_solver_patch_helpers.py" in item["command"] for item in tests)
    assert any(item["command"].endswith("pytest") for item in tests)


def test_patch_risk_register_is_ready():
    risks = build_patch_risk_register()
    assert len(risks) == EXPECTED_RISK_COUNT
    assert all(item["active"] is True for item in risks)
    assert all(item["blocking_without_tests"] is True for item in risks)
    assert {item["target_layer"] for item in risks} == {
        "world_model",
        "goal_inference",
        "planner",
        "verifier",
        "action_policy",
    }


def test_patch_execution_gates_are_ready_but_do_not_apply_patch():
    gates = build_patch_execution_gates()
    assert len(gates) == EXPECTED_GATE_COUNT
    assert all(item["passed"] is True for item in gates)
    assert all(item["diagnostic_only"] is True for item in gates)


def test_backlog_decision_blocks_implementation_now():
    decision = build_patch_backlog_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["patch_backlog_ready"] is True
    assert decision["patch_implementation_allowed_now"] is False
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_8_checks_all_pass():
    checks = build_task_8_checks()
    assert all(checks.values())


def test_each_task_8_case_passes():
    case_ids = [
        "m11_task8_source_task7_ready_v1",
        "m11_task8_patch_candidates_ready_v1",
        "m11_task8_file_targets_ready_v1",
        "m11_task8_function_targets_ready_v1",
        "m11_task8_required_tests_ready_v1",
        "m11_task8_risk_register_ready_v1",
        "m11_task8_patch_execution_gate_ready_v1",
        "m11_task8_score_submission_boundary_v1",
        "m11_task8_next_stage_valid_v1",
        "m11_task8_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_8_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_8_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_8_case("missing_task_8_case")


def test_all_task_8_cases_pass():
    results = evaluate_all_task_8_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_backlog_scorecard_passes():
    scorecard = build_backlog_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_8_record_ready():
    record = build_milestone_11_local_solver_patch_backlog()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_8_ready"] is True
    assert record["patch_backlog_ready"] is True
    assert record["patch_candidate_count"] == EXPECTED_PATCH_COUNT
    assert record["required_test_count"] == EXPECTED_REQUIRED_TEST_COUNT
    assert record["risk_count"] == EXPECTED_RISK_COUNT
    assert record["execution_gate_count"] == EXPECTED_GATE_COUNT
    assert record["patch_implementation_allowed_now"] is False
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["diagnostic_only"] is True
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["backlog_check_count"] == EXPECTED_CHECK_COUNT
    assert record["backlog_case_count"] == EXPECTED_CASE_COUNT
    assert record["backlog_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["backlog_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["backlog_gate_count"]
    assert record["backlog_issue_count"] == 0


def test_task_8_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_backlog()
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


def test_task_8_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_backlog()
    validation = validate_milestone_11_local_solver_patch_backlog(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_backlog_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_8_ready"] is True
    assert payload["backlog_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert payload["backlog_case_failure_count"] == 0


def test_task_8_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_backlog()
    markdown = render_task_8_markdown(record)
    manifest = render_task_8_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_8_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_8_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_PATCH_IMPLEMENTATION_ALLOWED_NOW=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PATCH_CANDIDATES" in manifest
    assert "REQUIRED_TEST_PLAN" in manifest
    assert "BACKLOG_CASE_RESULTS" in manifest


def test_task_8_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_backlog()
    paths = write_task_8_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["candidates_path"]).exists()
    assert Path(paths["tests_path"]).exists()
    assert Path(paths["risks_path"]).exists()
    assert Path(paths["gates_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_8_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "patch_world_model_state_tracking_v1" in Path(paths["candidates_path"]).read_text(
        encoding="utf-8"
    )
    assert "BACKLOG_ONLY_NO_RUNTIME_PATCH_NO_SCORE_NO_SUBMISSION" in Path(paths["decision_path"]).read_text(
        encoding="utf-8"
    )


def test_task_8_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_backlog()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_8_index_is_conservative():
    index = build_milestone_11_local_solver_patch_backlog()["backlog_index"]
    assert index["patch_backlog_ready"] is True
    assert index["patch_candidate_count"] == EXPECTED_PATCH_COUNT
    assert index["required_test_count"] == EXPECTED_REQUIRED_TEST_COUNT
    assert index["risk_count"] == EXPECTED_RISK_COUNT
    assert index["execution_gate_count"] == EXPECTED_GATE_COUNT
    assert index["patch_implementation_allowed_now"] is False
    assert index["runtime_solver_modified"] is False
    assert index["external_solver_dependency"] is False
    assert index["diagnostic_only"] is True
    assert index["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert index["official_score_claim_allowed"] is False
    assert index["real_submission_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_active"] is True
