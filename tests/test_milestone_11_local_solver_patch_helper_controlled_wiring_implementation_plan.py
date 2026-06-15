from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan import (
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_CONTRACT_COUNT,
    EXPECTED_IMPLEMENTATION_STEP_COUNT,
    EXPECTED_REGRESSION_TEST_COUNT,
    EXPECTED_REVIEW_GATE_COUNT,
    EXPECTED_ROLLBACK_ITEM_COUNT,
    EXPECTED_TARGET_MODULE_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_contracts,
    build_implementation_plan_scorecard,
    build_implementation_steps,
    build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan,
    build_plan_decision,
    build_regression_tests,
    build_review_gates,
    build_rollback_items,
    build_target_module_proposals,
    build_task_15_source_summary,
    build_task_16_checks,
    evaluate_all_task_16_cases,
    evaluate_task_16_case,
    render_task_16_manifest,
    render_task_16_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan,
    write_task_16_artifacts,
)


def test_task_16_source_summary_reads_task_15():
    source = build_task_15_source_summary()
    assert source["task_15_present"] is True
    assert source["task_15_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY"
    assert source["task_15_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-GATE-")
    assert source["task_15_ready"] is True
    assert source["controlled_gate_ready"] is True
    assert source["controlled_gate_passed"] is True
    assert source["controlled_gate_status"] == "CONTROLLED_GATE_PASS"
    assert source["implementation_plan_authorized"] is True
    assert source["controlled_runtime_wiring_authorized"] is False
    assert source["runtime_wiring_performed"] is False


def test_target_module_proposals_are_plan_only():
    targets = build_target_module_proposals()
    assert len(targets) == EXPECTED_TARGET_MODULE_COUNT
    assert all(item["implementation_phase"] == "IMPLEMENTATION_PLAN_ONLY" for item in targets)
    assert all(item["runtime_solver_patch_allowed"] is False for item in targets)
    assert all(item["ranker_runtime_patch_allowed"] is False for item in targets)
    assert all(item["score_claim_allowed"] is False for item in targets)
    assert all(item["submission_allowed"] is False for item in targets)


def test_implementation_steps_are_guarded():
    steps = build_implementation_steps()
    assert len(steps) == EXPECTED_IMPLEMENTATION_STEP_COUNT
    assert all(item["allowed_now"] is True for item in steps)
    assert all(item["runtime_solver_modification_allowed"] is False for item in steps)
    assert all(item["ranker_runtime_modification_allowed"] is False for item in steps)
    assert all(item["score_claim_allowed"] is False for item in steps)
    assert all(item["submission_allowed"] is False for item in steps)


def test_contracts_all_pass():
    contracts = build_contracts()
    assert len(contracts) == EXPECTED_CONTRACT_COUNT
    assert all(item["required"] is True for item in contracts)
    assert all(item["passed"] is True for item in contracts)
    assert all(item["runtime_solver_modification_allowed"] is False for item in contracts)


def test_regression_tests_are_local_only():
    tests = build_regression_tests()
    assert len(tests) == EXPECTED_REGRESSION_TEST_COUNT
    assert all(item["required"] is True for item in tests)
    assert all(item["local_only"] is True for item in tests)
    assert all(item["external_api_dependency"] is False for item in tests)
    assert all(item["score_claim_allowed"] is False for item in tests)


def test_rollback_and_review_gates_ready():
    rollback = build_rollback_items()
    gates = build_review_gates()
    assert len(rollback) == EXPECTED_ROLLBACK_ITEM_COUNT
    assert len(gates) == EXPECTED_REVIEW_GATE_COUNT
    assert all(item["ready"] is True for item in rollback)
    assert all(item["passed"] is True for item in gates)


def test_plan_decision_authorizes_dry_run_only():
    decision = build_plan_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["implementation_plan_ready"] is True
    assert decision["implementation_plan_passed"] is True
    assert decision["implementation_dry_run_authorized"] is True
    assert decision["runtime_solver_patch_allowed"] is False
    assert decision["ranker_runtime_patch_allowed"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_16_checks_all_pass():
    checks = build_task_16_checks()
    assert all(checks.values())


def test_each_task_16_case_passes():
    case_ids = [
        "m11_task16_source_task15_ready_v1",
        "m11_task16_gate_passed_v1",
        "m11_task16_implementation_plan_authorized_v1",
        "m11_task16_target_modules_v1",
        "m11_task16_steps_contracts_tests_v1",
        "m11_task16_rollback_review_v1",
        "m11_task16_runtime_boundary_v1",
        "m11_task16_score_boundary_v1",
        "m11_task16_submission_boundary_v1",
        "m11_task16_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_16_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_16_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_16_case("missing_task_16_case")


def test_all_task_16_cases_pass():
    results = evaluate_all_task_16_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_implementation_plan_scorecard_passes():
    scorecard = build_implementation_plan_scorecard()
    assert len(scorecard) == 16
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_16_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_16_ready"] is True
    assert record["implementation_plan_ready"] is True
    assert record["implementation_plan_passed"] is True
    assert record["implementation_dry_run_authorized"] is True
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["target_module_count"] == EXPECTED_TARGET_MODULE_COUNT
    assert record["implementation_step_count"] == EXPECTED_IMPLEMENTATION_STEP_COUNT
    assert record["contract_count"] == EXPECTED_CONTRACT_COUNT
    assert record["regression_test_count"] == EXPECTED_REGRESSION_TEST_COUNT
    assert record["rollback_item_count"] == EXPECTED_ROLLBACK_ITEM_COUNT
    assert record["review_gate_count"] == EXPECTED_REVIEW_GATE_COUNT
    assert record["plan_check_count"] == EXPECTED_CHECK_COUNT
    assert record["plan_case_count"] == EXPECTED_CASE_COUNT
    assert record["plan_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["plan_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["implementation_plan_gate_count"]
    assert record["implementation_plan_issue_count"] == 0


def test_task_16_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
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


def test_task_16_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_16_ready"] is True
    assert payload["implementation_plan_passed"] is True
    assert payload["implementation_dry_run_authorized"] is True
    assert payload["runtime_solver_patch_allowed"] is False


def test_task_16_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
    markdown = render_task_16_markdown(record)
    manifest = render_task_16_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_16_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_16_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_PLAN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_DRY_RUN_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "IMPLEMENTATION_TARGETS" in manifest
    assert "IMPLEMENTATION_PLAN_CASE_RESULTS" in manifest


def test_task_16_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()
    paths = write_task_16_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["targets_path"]).exists()
    assert Path(paths["steps_path"]).exists()
    assert Path(paths["contracts_path"]).exists()
    assert Path(paths["tests_path"]).exists()
    assert Path(paths["rollback_path"]).exists()
    assert Path(paths["gates_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_16_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "IMPLEMENTATION_PLAN_ONLY_NEXT_DRY_RUN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_16_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
