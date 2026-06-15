from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run import (
    EXPECTED_BOUNDARY_ASSERTION_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_CONTRACT_VALIDATION_COUNT,
    EXPECTED_DRY_RUN_CASE_COUNT,
    EXPECTED_DRY_RUN_CASE_FAILURE_COUNT,
    EXPECTED_DRY_RUN_CASE_PASS_COUNT,
    EXPECTED_IMPORT_SIMULATION_COUNT,
    EXPECTED_REGRESSION_SIMULATION_COUNT,
    EXPECTED_REVIEW_GATE_CONFIRMATION_COUNT,
    EXPECTED_ROLLBACK_READINESS_COUNT,
    EXPECTED_STEP_SIMULATION_COUNT,
    EXPECTED_TARGET_SIMULATION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_contract_dry_run_validations,
    build_import_surface_dry_run_simulations,
    build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run,
    build_operator_review_gate_confirmations,
    build_regression_dry_run_simulations,
    build_rollback_dry_run_readiness,
    build_runtime_dry_run_boundary_assertions,
    build_runtime_wiring_dry_run_decision,
    build_runtime_wiring_dry_run_scorecard,
    build_step_dry_run_simulations,
    build_target_dry_run_simulations,
    build_task_20_source_summary,
    build_task_21_checks,
    evaluate_all_task_21_cases,
    evaluate_task_21_case,
    render_task_21_manifest,
    render_task_21_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run,
    write_task_21_artifacts,
)


def test_task_21_source_summary_reads_task_20():
    source = build_task_20_source_summary()
    assert source["task_20_present"] is True
    assert source["task_20_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_READY"
    assert source["task_20_id"].startswith(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-PLAN-"
    )
    assert source["task_20_ready"] is True
    assert source["runtime_wiring_plan_ready"] is True
    assert source["runtime_wiring_plan_passed"] is True
    assert source["runtime_wiring_dry_run_authorized"] is True
    assert source["controlled_runtime_wiring_authorized"] is False
    assert source["runtime_solver_patch_allowed"] is False
    assert source["ranker_runtime_patch_allowed"] is False


def test_target_dry_run_simulations_do_not_mutate_runtime():
    simulations = build_target_dry_run_simulations()
    assert len(simulations) == EXPECTED_TARGET_SIMULATION_COUNT
    assert all(item["simulation_status"] == "SIMULATION_PASS" for item in simulations)
    assert all(item["runtime_solver_patch_applied"] is False for item in simulations)
    assert all(item["ranker_runtime_patch_applied"] is False for item in simulations)
    assert all(item["runtime_wiring_performed"] is False for item in simulations)
    assert all(item["runtime_solver_modified"] is False for item in simulations)


def test_import_surface_dry_run_not_applied():
    simulations = build_import_surface_dry_run_simulations()
    assert len(simulations) == EXPECTED_IMPORT_SIMULATION_COUNT
    assert all(item["simulation_status"] == "IMPORT_SIMULATION_PASS" for item in simulations)
    assert all(item["import_checked"] is True for item in simulations)
    assert all(item["import_applied"] is False for item in simulations)
    assert all(item["requires_review"] is True for item in simulations)


def test_contract_validations_pass():
    validations = build_contract_dry_run_validations()
    assert len(validations) == EXPECTED_CONTRACT_VALIDATION_COUNT
    assert all(item["validation_status"] == "CONTRACT_DRY_RUN_PASS" for item in validations)
    assert all(item["passed"] is True for item in validations)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in validations)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in validations)


def test_step_simulations_are_not_executed_for_real():
    steps = build_step_dry_run_simulations()
    assert len(steps) == EXPECTED_STEP_SIMULATION_COUNT
    assert all(item["simulation_status"] == "STEP_DRY_RUN_PASS" for item in steps)
    assert all(item["executed_for_real"] is False for item in steps)
    assert all(item["runtime_solver_modified"] is False for item in steps)
    assert all(item["ranker_runtime_modified"] is False for item in steps)


def test_regression_rollback_and_review_gates_pass():
    regressions = build_regression_dry_run_simulations()
    rollbacks = build_rollback_dry_run_readiness()
    review_gates = build_operator_review_gate_confirmations()
    assert len(regressions) == EXPECTED_REGRESSION_SIMULATION_COUNT
    assert len(rollbacks) == EXPECTED_ROLLBACK_READINESS_COUNT
    assert len(review_gates) == EXPECTED_REVIEW_GATE_CONFIRMATION_COUNT
    assert all(item["passed"] is True for item in regressions)
    assert all(item["local_only"] is True for item in regressions)
    assert all(item["external_api_dependency"] is False for item in regressions)
    assert all(item["ready"] is True for item in rollbacks)
    assert all(item["confirmed"] is True for item in review_gates)


def test_boundary_assertions_pass():
    assertions = build_runtime_dry_run_boundary_assertions()
    assert len(assertions) == EXPECTED_BOUNDARY_ASSERTION_COUNT
    assert all(item["passed"] is True for item in assertions)
    assert all(item["severity"] == "PASS" for item in assertions)


def test_runtime_wiring_dry_run_decision_authorizes_review_only():
    decision = build_runtime_wiring_dry_run_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["runtime_wiring_dry_run_ready"] is True
    assert decision["runtime_wiring_dry_run_passed"] is True
    assert decision["runtime_wiring_review_authorized"] is True
    assert decision["controlled_runtime_wiring_authorized"] is False
    assert decision["runtime_solver_patch_allowed"] is False
    assert decision["ranker_runtime_patch_allowed"] is False
    assert decision["runtime_solver_patch_applied"] is False
    assert decision["ranker_runtime_patch_applied"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_21_checks_all_pass():
    checks = build_task_21_checks()
    assert all(checks.values())


def test_each_task_21_case_passes():
    case_ids = [
        "m11_task21_source_task20_ready_v1",
        "m11_task21_plan_passed_v1",
        "m11_task21_target_simulations_v1",
        "m11_task21_import_simulations_v1",
        "m11_task21_contract_validations_v1",
        "m11_task21_step_simulations_v1",
        "m11_task21_regression_simulations_v1",
        "m11_task21_rollback_readiness_v1",
        "m11_task21_boundary_v1",
        "m11_task21_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_21_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_21_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_21_case("missing_task_21_case")


def test_all_task_21_cases_pass():
    results = evaluate_all_task_21_cases()
    assert len(results) == EXPECTED_DRY_RUN_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_runtime_wiring_dry_run_scorecard_passes():
    scorecard = build_runtime_wiring_dry_run_scorecard()
    assert len(scorecard) == 23
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_21_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_21_ready"] is True
    assert record["runtime_wiring_dry_run_ready"] is True
    assert record["runtime_wiring_dry_run_passed"] is True
    assert record["runtime_wiring_review_authorized"] is True
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["ranker_runtime_patch_applied"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["target_simulation_count"] == EXPECTED_TARGET_SIMULATION_COUNT
    assert record["import_simulation_count"] == EXPECTED_IMPORT_SIMULATION_COUNT
    assert record["contract_validation_count"] == EXPECTED_CONTRACT_VALIDATION_COUNT
    assert record["step_simulation_count"] == EXPECTED_STEP_SIMULATION_COUNT
    assert record["regression_simulation_count"] == EXPECTED_REGRESSION_SIMULATION_COUNT
    assert record["rollback_readiness_count"] == EXPECTED_ROLLBACK_READINESS_COUNT
    assert record["review_gate_confirmation_count"] == EXPECTED_REVIEW_GATE_CONFIRMATION_COUNT
    assert record["boundary_assertion_count"] == EXPECTED_BOUNDARY_ASSERTION_COUNT
    assert record["runtime_wiring_dry_run_check_count"] == EXPECTED_CHECK_COUNT
    assert record["runtime_wiring_dry_run_case_count"] == EXPECTED_DRY_RUN_CASE_COUNT
    assert record["runtime_wiring_dry_run_case_pass_count"] == EXPECTED_DRY_RUN_CASE_PASS_COUNT
    assert record["runtime_wiring_dry_run_case_failure_count"] == EXPECTED_DRY_RUN_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["runtime_wiring_dry_run_gate_count"]
    assert record["runtime_wiring_dry_run_issue_count"] == 0


def test_task_21_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()
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


def test_task_21_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_21_ready"] is True
    assert payload["runtime_wiring_dry_run_passed"] is True
    assert payload["runtime_wiring_review_authorized"] is True
    assert payload["controlled_runtime_wiring_authorized"] is False


def test_task_21_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()
    markdown = render_task_21_markdown(record)
    manifest = render_task_21_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_21_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_21_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_DRY_RUN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_REVIEW_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CONTROLLED_RUNTIME_WIRING_DRY_RUN_TARGET_SIMULATIONS" in manifest
    assert "CONTROLLED_RUNTIME_WIRING_DRY_RUN_CASE_RESULTS" in manifest


def test_task_21_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()
    paths = write_task_21_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["targets_path"]).exists()
    assert Path(paths["imports_path"]).exists()
    assert Path(paths["contracts_path"]).exists()
    assert Path(paths["steps_path"]).exists()
    assert Path(paths["regressions_path"]).exists()
    assert Path(paths["rollback_path"]).exists()
    assert Path(paths["review_gates_path"]).exists()
    assert Path(paths["boundary_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_DRY_RUN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_21_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "CONTROLLED_RUNTIME_WIRING_DRY_RUN_ONLY_NEXT_REVIEW_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_21_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_dry_run()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
