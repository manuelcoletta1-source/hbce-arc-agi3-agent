from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_wiring_plan import (
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_REQUIRED_TEST_COUNT,
    EXPECTED_STOP_CONDITION_COUNT,
    EXPECTED_WIRING_GATE_COUNT,
    EXPECTED_WIRING_STEP_COUNT,
    EXPECTED_WIRING_TARGET_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_adapter_plan,
    build_milestone_11_local_solver_patch_helper_wiring_plan,
    build_required_tests,
    build_stop_conditions,
    build_task_11_source_summary,
    build_task_12_checks,
    build_wiring_decision,
    build_wiring_gate_plan,
    build_wiring_scorecard,
    build_wiring_steps,
    build_wiring_targets,
    evaluate_all_task_12_cases,
    evaluate_task_12_case,
    render_task_12_manifest,
    render_task_12_markdown,
    run_milestone_11_local_solver_patch_helper_wiring_plan_pipeline,
    validate_milestone_11_local_solver_patch_helper_wiring_plan,
    write_task_12_artifacts,
)


def test_task_12_source_summary_reads_task_11():
    source = build_task_11_source_summary()
    assert source["task_11_present"] is True
    assert source["task_11_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_PROBE_RUN_V1_READY"
    assert source["task_11_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-PROBE-RUN-")
    assert source["task_11_ready"] is True
    assert source["helper_probe_run_passed"] is True
    assert source["helper_runtime_wiring_performed"] is False
    assert source["probe_result_count"] == 30
    assert source["probe_pass_count"] == 30
    assert source["probe_failure_count"] == 0
    assert source["runtime_solver_modified"] is False
    assert source["ranker_runtime_modified"] is False
    assert source["external_solver_dependency"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_wiring_targets_cover_all_layers():
    targets = build_wiring_targets()
    assert len(targets) == EXPECTED_WIRING_TARGET_COUNT
    assert {item["target_layer"] for item in targets} == {
        "world_model",
        "goal_inference",
        "planner",
        "verifier",
        "action_policy",
    }
    assert all(item["planned_module"] == "src/hbce_arc_agi3/local_solver_patch_helper_wiring.py" for item in targets)
    assert all(item["helper_function"] for item in targets)
    assert all(item["adapter_name"] for item in targets)
    assert all(item["runtime_solver_patch_allowed"] is False for item in targets)
    assert all(item["score_claim_allowed"] is False for item in targets)


def test_adapter_plan_is_fail_closed():
    adapters = build_adapter_plan()
    assert len(adapters) == EXPECTED_WIRING_TARGET_COUNT
    assert all(item["input_contract"] == "diagnostic_record_sequence" for item in adapters)
    assert all(item["output_contract"] == "diagnostic_hint_sequence" for item in adapters)
    assert all(item["fail_closed_on_missing_input"] is True for item in adapters)
    assert all(item["fail_closed_on_invalid_hint"] is True for item in adapters)
    assert all(item["runtime_side_effect_allowed"] is False for item in adapters)


def test_wiring_steps_are_plan_only():
    steps = build_wiring_steps()
    assert len(steps) == EXPECTED_WIRING_STEP_COUNT
    assert steps[0]["allowed_now"] is True
    assert all(item["modifies_runtime_solver"] is False for item in steps)
    assert all(item["modifies_ranker_runtime"] is False for item in steps)
    assert all(item["score_claim_allowed"] is False for item in steps)
    assert steps[-1]["step_id"] == "step_08_authorize_next_dry_run_v1"


def test_wiring_gate_plan_ready():
    gates = build_wiring_gate_plan()
    assert len(gates) == EXPECTED_WIRING_GATE_COUNT
    assert all(item["required"] is True for item in gates)
    assert all(item["passed"] is True for item in gates)
    assert all(item["failure_action"] == "STOP_WIRING_PLAN" for item in gates)


def test_stop_conditions_ready_and_inactive():
    stops = build_stop_conditions()
    assert len(stops) == EXPECTED_STOP_CONDITION_COUNT
    assert all(item["severity"] == "BLOCKING" for item in stops)
    assert all(item["active"] is False for item in stops)
    assert all(item["action"] == "STOP_AND_REVIEW" for item in stops)


def test_required_tests_declared():
    tests = build_required_tests()
    assert len(tests) == EXPECTED_REQUIRED_TEST_COUNT
    assert all(item["required"] is True for item in tests)
    assert all(item["local_only"] is True for item in tests)
    assert all(item["external_api_dependency"] is False for item in tests)
    assert all(item["score_claim_allowed"] is False for item in tests)


def test_wiring_decision_is_conservative():
    decision = build_wiring_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["wiring_plan_ready"] is True
    assert decision["wiring_performed"] is False
    assert decision["next_stage_authorized_scope"] == "LOCAL_WIRING_DRY_RUN_ONLY"
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_12_checks_all_pass():
    checks = build_task_12_checks()
    assert all(checks.values())


def test_each_task_12_case_passes():
    case_ids = [
        "m11_task12_source_task11_ready_v1",
        "m11_task12_probe_pass_required_v1",
        "m11_task12_wiring_targets_ready_v1",
        "m11_task12_adapter_plan_ready_v1",
        "m11_task12_step_plan_ready_v1",
        "m11_task12_gate_plan_ready_v1",
        "m11_task12_stop_conditions_ready_v1",
        "m11_task12_required_tests_ready_v1",
        "m11_task12_score_submission_boundary_v1",
        "m11_task12_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_12_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_12_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_12_case("missing_task_12_case")


def test_all_task_12_cases_pass():
    results = evaluate_all_task_12_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_wiring_scorecard_passes():
    scorecard = build_wiring_scorecard()
    assert len(scorecard) == 10
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_12_record_ready():
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_12_ready"] is True
    assert record["wiring_plan_ready"] is True
    assert record["wiring_performed"] is False
    assert record["next_stage_authorized_scope"] == "LOCAL_WIRING_DRY_RUN_ONLY"
    assert record["wiring_target_count"] == EXPECTED_WIRING_TARGET_COUNT
    assert record["adapter_plan_count"] == EXPECTED_WIRING_TARGET_COUNT
    assert record["wiring_step_count"] == EXPECTED_WIRING_STEP_COUNT
    assert record["wiring_gate_count"] == EXPECTED_WIRING_GATE_COUNT
    assert record["stop_condition_count"] == EXPECTED_STOP_CONDITION_COUNT
    assert record["required_test_count"] == EXPECTED_REQUIRED_TEST_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["wiring_check_count"] == EXPECTED_CHECK_COUNT
    assert record["wiring_case_count"] == EXPECTED_CASE_COUNT
    assert record["wiring_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["wiring_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["wiring_internal_gate_count"]
    assert record["wiring_issue_count"] == 0


def test_task_12_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
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


def test_task_12_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_plan(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_wiring_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_12_ready"] is True
    assert payload["wiring_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert payload["wiring_case_failure_count"] == 0


def test_task_12_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
    markdown = render_task_12_markdown(record)
    manifest = render_task_12_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_12_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_12_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_WIRING_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_NEXT_STAGE_AUTHORIZED_SCOPE=LOCAL_WIRING_DRY_RUN_ONLY" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "WIRING_TARGETS" in manifest
    assert "WIRING_CASE_RESULTS" in manifest


def test_task_12_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_wiring_plan()
    paths = write_task_12_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["targets_path"]).exists()
    assert Path(paths["adapters_path"]).exists()
    assert Path(paths["steps_path"]).exists()
    assert Path(paths["gates_path"]).exists()
    assert Path(paths["stops_path"]).exists()
    assert Path(paths["tests_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_PLAN_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_12_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "LOCAL_WIRING_DRY_RUN_ONLY" in Path(paths["decision_path"]).read_text(encoding="utf-8")


def test_task_12_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_wiring_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
