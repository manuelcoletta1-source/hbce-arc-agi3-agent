from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_implementation_plan import (
    EXPECTED_AUTHORIZATION_CRITERION_COUNT,
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_IMPLEMENTATION_STEP_COUNT,
    EXPECTED_PATCH_COUNT,
    EXPECTED_REQUIRED_TEST_COUNT,
    EXPECTED_STOP_CONDITION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_authorization_criteria,
    build_implementation_decision,
    build_implementation_plan_scorecard,
    build_implementation_sequence,
    build_milestone_11_local_solver_patch_implementation_plan,
    build_patch_order,
    build_preflight_plan,
    build_stop_conditions,
    build_task_8_source_summary,
    build_task_9_checks,
    build_test_gate_plan,
    evaluate_all_task_9_cases,
    evaluate_task_9_case,
    render_task_9_manifest,
    render_task_9_markdown,
    run_milestone_11_local_solver_patch_implementation_plan_pipeline,
    validate_milestone_11_local_solver_patch_implementation_plan,
    write_task_9_artifacts,
)


def test_task_9_source_summary_reads_task_8():
    source = build_task_8_source_summary()
    assert source["task_8_present"] is True
    assert source["task_8_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_BACKLOG_V1_READY"
    assert source["task_8_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-BACKLOG-")
    assert source["task_8_ready"] is True
    assert source["patch_backlog_ready"] is True
    assert source["patch_candidate_count"] == EXPECTED_PATCH_COUNT
    assert source["required_test_count"] == EXPECTED_REQUIRED_TEST_COUNT
    assert source["patch_implementation_allowed_now"] is False
    assert source["runtime_solver_modified"] is False
    assert source["ranker_runtime_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_preflight_plan_is_ready():
    preflight = build_preflight_plan()
    assert len(preflight) == 3
    assert all(item["required"] is True for item in preflight)
    assert all(item["failure_action"] == "STOP_IMPLEMENTATION" for item in preflight)
    assert any(item["command"] == "git status -sb" for item in preflight)
    assert any(item["command"].endswith("pytest") for item in preflight)


def test_patch_order_preserves_task_8_patch_candidates():
    order = build_patch_order()
    assert len(order) == EXPECTED_PATCH_COUNT
    assert all(item["file_target"] == "src/hbce_arc_agi3/solver_patch_helpers.py" for item in order)
    assert all(item["function_target"] for item in order)
    assert all(item["test_target"] for item in order)
    assert all(item["implementation_phase"] == "PLANNED_NOT_APPLIED" for item in order)
    assert all(item["implementation_allowed_now"] is False for item in order)
    assert all(item["score_claim_allowed"] is False for item in order)


def test_implementation_sequence_is_plan_only():
    sequence = build_implementation_sequence()
    assert len(sequence) == EXPECTED_IMPLEMENTATION_STEP_COUNT
    assert sequence[0]["allowed_now"] is True
    assert all(step["modifies_runtime_solver"] is False for step in sequence)
    assert sequence[-1]["step_id"] == "step_07_authorize_next_stage_v1"


def test_test_gate_plan_preserves_required_tests():
    gates = build_test_gate_plan()
    assert len(gates) == EXPECTED_REQUIRED_TEST_COUNT
    assert all(item["required"] is True for item in gates)
    assert all(item["must_pass_before_next_stage"] is True for item in gates)
    assert all(item["external_api_dependency"] is False for item in gates)
    assert all(item["score_claim_allowed"] is False for item in gates)


def test_authorization_criteria_ready():
    criteria = build_authorization_criteria()
    assert len(criteria) == EXPECTED_AUTHORIZATION_CRITERION_COUNT
    assert all(item["required"] is True for item in criteria)
    assert all(item["passed"] is True for item in criteria)
    assert all(item["authorization_scope"] == "NEXT_STAGE_ONLY" for item in criteria)


def test_stop_conditions_ready_and_inactive():
    stops = build_stop_conditions()
    assert len(stops) == EXPECTED_STOP_CONDITION_COUNT
    assert all(item["severity"] == "BLOCKING" for item in stops)
    assert all(item["active"] is False for item in stops)
    assert all(item["action"] == "STOP_AND_REVIEW" for item in stops)


def test_implementation_decision_is_conservative():
    decision = build_implementation_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["implementation_plan_ready"] is True
    assert decision["implementation_allowed_now"] is False
    assert decision["next_stage_authorized_scope"] == "PATCH_HELPERS_ONLY"
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_9_checks_all_pass():
    checks = build_task_9_checks()
    assert all(checks.values())


def test_each_task_9_case_passes():
    case_ids = [
        "m11_task9_source_task8_ready_v1",
        "m11_task9_implementation_sequence_ready_v1",
        "m11_task9_preflight_ready_v1",
        "m11_task9_patch_order_ready_v1",
        "m11_task9_required_tests_ready_v1",
        "m11_task9_authorization_criteria_ready_v1",
        "m11_task9_stop_conditions_ready_v1",
        "m11_task9_score_submission_boundary_v1",
        "m11_task9_next_stage_valid_v1",
        "m11_task9_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_9_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_9_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_9_case("missing_task_9_case")


def test_all_task_9_cases_pass():
    results = evaluate_all_task_9_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_implementation_plan_scorecard_passes():
    scorecard = build_implementation_plan_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_9_record_ready():
    record = build_milestone_11_local_solver_patch_implementation_plan()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_9_ready"] is True
    assert record["implementation_plan_ready"] is True
    assert record["implementation_step_count"] == EXPECTED_IMPLEMENTATION_STEP_COUNT
    assert record["preflight_step_count"] == 3
    assert record["patch_order_count"] == EXPECTED_PATCH_COUNT
    assert record["required_test_gate_count"] == EXPECTED_REQUIRED_TEST_COUNT
    assert record["authorization_criterion_count"] == EXPECTED_AUTHORIZATION_CRITERION_COUNT
    assert record["stop_condition_count"] == EXPECTED_STOP_CONDITION_COUNT
    assert record["implementation_allowed_now"] is False
    assert record["next_stage_authorized_scope"] == "PATCH_HELPERS_ONLY"
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["implementation_plan_check_count"] == EXPECTED_CHECK_COUNT
    assert record["implementation_plan_case_count"] == EXPECTED_CASE_COUNT
    assert record["implementation_plan_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["implementation_plan_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["implementation_plan_gate_count"]
    assert record["implementation_plan_issue_count"] == 0


def test_task_9_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_implementation_plan()
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


def test_task_9_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_implementation_plan()
    validation = validate_milestone_11_local_solver_patch_implementation_plan(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_implementation_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_9_ready"] is True
    assert payload["implementation_plan_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert payload["implementation_plan_case_failure_count"] == 0


def test_task_9_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_implementation_plan()
    markdown = render_task_9_markdown(record)
    manifest = render_task_9_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_9_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_9_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_ALLOWED_NOW=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_NEXT_STAGE_AUTHORIZED_SCOPE=PATCH_HELPERS_ONLY" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PREFLIGHT_PLAN" in manifest
    assert "PATCH_ORDER" in manifest
    assert "IMPLEMENTATION_SEQUENCE" in manifest
    assert "IMPLEMENTATION_PLAN_CASE_RESULTS" in manifest


def test_task_9_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_implementation_plan()
    paths = write_task_9_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["preflight_path"]).exists()
    assert Path(paths["order_path"]).exists()
    assert Path(paths["sequence_path"]).exists()
    assert Path(paths["test_gates_path"]).exists()
    assert Path(paths["authorization_path"]).exists()
    assert Path(paths["stop_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_IMPLEMENTATION_PLAN_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_9_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "PATCH_HELPERS_ONLY" in Path(paths["decision_path"]).read_text(encoding="utf-8")


def test_task_9_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_implementation_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
