from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run import (
    EXPECTED_BOUNDARY_ASSERTION_COUNT,
    EXPECTED_CONTRACT_VALIDATION_COUNT,
    EXPECTED_DRY_RUN_CASE_COUNT,
    EXPECTED_DRY_RUN_CASE_FAILURE_COUNT,
    EXPECTED_DRY_RUN_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_REGRESSION_SIMULATION_COUNT,
    EXPECTED_ROLLBACK_SIMULATION_COUNT,
    EXPECTED_SIMULATED_OPERATION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_boundary_assertions,
    build_contract_validation_results,
    build_dry_run_decision,
    build_implementation_dry_run_scorecard,
    build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run,
    build_regression_simulation_results,
    build_rollback_simulation_results,
    build_simulated_wiring_operations,
    build_task_16_source_summary,
    build_task_17_checks,
    evaluate_all_task_17_cases,
    evaluate_task_17_case,
    render_task_17_manifest,
    render_task_17_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run,
    write_task_17_artifacts,
)


def test_task_17_source_summary_reads_task_16():
    source = build_task_16_source_summary()
    assert source["task_16_present"] is True
    assert source["task_16_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_PLAN_V1_READY"
    assert source["task_16_id"].startswith(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-PLAN-"
    )
    assert source["task_16_ready"] is True
    assert source["implementation_plan_ready"] is True
    assert source["implementation_plan_passed"] is True
    assert source["implementation_dry_run_authorized"] is True
    assert source["runtime_solver_patch_allowed"] is False
    assert source["ranker_runtime_patch_allowed"] is False
    assert source["runtime_wiring_performed"] is False


def test_simulated_wiring_operations_pass_without_runtime_patch():
    operations = build_simulated_wiring_operations()
    assert len(operations) == EXPECTED_SIMULATED_OPERATION_COUNT
    assert all(item["operation_status"] == "SIMULATION_PASS" for item in operations)
    assert all(item["operation_type"] == "CONTROLLED_IMPLEMENTATION_DRY_RUN" for item in operations)
    assert all(item["runtime_solver_patch_applied"] is False for item in operations)
    assert all(item["ranker_runtime_patch_applied"] is False for item in operations)
    assert all(item["runtime_solver_modified"] is False for item in operations)
    assert all(item["ranker_runtime_modified"] is False for item in operations)
    assert all(item["score_claim_allowed"] is False for item in operations)
    assert all(item["submission_allowed"] is False for item in operations)


def test_contract_validations_pass():
    validations = build_contract_validation_results()
    assert len(validations) == EXPECTED_CONTRACT_VALIDATION_COUNT
    assert all(item["validation_status"] == "CONTRACT_VALIDATION_PASS" for item in validations)
    assert all(item["passed"] is True for item in validations)
    assert all(item["runtime_solver_modification_allowed"] is False for item in validations)


def test_regression_simulations_are_not_real_execution():
    simulations = build_regression_simulation_results()
    assert len(simulations) == EXPECTED_REGRESSION_SIMULATION_COUNT
    assert all(item["simulation_status"] == "REGRESSION_SIMULATION_PASS" for item in simulations)
    assert all(item["passed"] is True for item in simulations)
    assert all(item["executed_for_real"] is False for item in simulations)
    assert all(item["local_only"] is True for item in simulations)
    assert all(item["external_api_dependency"] is False for item in simulations)


def test_rollback_simulations_ready():
    rollbacks = build_rollback_simulation_results()
    assert len(rollbacks) == EXPECTED_ROLLBACK_SIMULATION_COUNT
    assert all(item["simulation_status"] == "ROLLBACK_READY" for item in rollbacks)
    assert all(item["ready"] is True for item in rollbacks)
    assert all(item["executed_for_real"] is False for item in rollbacks)


def test_boundary_assertions_pass():
    assertions = build_boundary_assertions()
    assert len(assertions) == EXPECTED_BOUNDARY_ASSERTION_COUNT
    assert all(item["passed"] is True for item in assertions)
    assert all(item["severity"] == "PASS" for item in assertions)


def test_dry_run_decision_authorizes_review_only():
    decision = build_dry_run_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["implementation_dry_run_ready"] is True
    assert decision["implementation_dry_run_passed"] is True
    assert decision["implementation_review_authorized"] is True
    assert decision["runtime_solver_patch_applied"] is False
    assert decision["ranker_runtime_patch_applied"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_17_checks_all_pass():
    checks = build_task_17_checks()
    assert all(checks.values())


def test_each_task_17_case_passes():
    case_ids = [
        "m11_task17_source_task16_ready_v1",
        "m11_task17_plan_passed_v1",
        "m11_task17_targets_simulated_v1",
        "m11_task17_contracts_validated_v1",
        "m11_task17_regression_simulated_v1",
        "m11_task17_rollback_simulated_v1",
        "m11_task17_runtime_boundary_v1",
        "m11_task17_score_boundary_v1",
        "m11_task17_submission_boundary_v1",
        "m11_task17_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_17_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_17_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_17_case("missing_task_17_case")


def test_all_task_17_cases_pass():
    results = evaluate_all_task_17_cases()
    assert len(results) == EXPECTED_DRY_RUN_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_implementation_dry_run_scorecard_passes():
    scorecard = build_implementation_dry_run_scorecard()
    assert len(scorecard) == 17
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_17_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_17_ready"] is True
    assert record["implementation_dry_run_ready"] is True
    assert record["implementation_dry_run_passed"] is True
    assert record["implementation_review_authorized"] is True
    assert record["runtime_solver_patch_applied"] is False
    assert record["ranker_runtime_patch_applied"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["simulated_operation_count"] == EXPECTED_SIMULATED_OPERATION_COUNT
    assert record["contract_validation_count"] == EXPECTED_CONTRACT_VALIDATION_COUNT
    assert record["regression_simulation_count"] == EXPECTED_REGRESSION_SIMULATION_COUNT
    assert record["rollback_simulation_count"] == EXPECTED_ROLLBACK_SIMULATION_COUNT
    assert record["boundary_assertion_count"] == EXPECTED_BOUNDARY_ASSERTION_COUNT
    assert record["dry_run_check_count"] == EXPECTED_CHECK_COUNT
    assert record["dry_run_case_count"] == EXPECTED_DRY_RUN_CASE_COUNT
    assert record["dry_run_case_pass_count"] == EXPECTED_DRY_RUN_CASE_PASS_COUNT
    assert record["dry_run_case_failure_count"] == EXPECTED_DRY_RUN_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["implementation_dry_run_gate_count"]
    assert record["implementation_dry_run_issue_count"] == 0


def test_task_17_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()
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


def test_task_17_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_17_ready"] is True
    assert payload["implementation_dry_run_passed"] is True
    assert payload["implementation_review_authorized"] is True
    assert payload["runtime_solver_patch_applied"] is False


def test_task_17_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()
    markdown = render_task_17_markdown(record)
    manifest = render_task_17_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_17_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_17_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_DRY_RUN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_REVIEW_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_PATCH_APPLIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RANKER_RUNTIME_PATCH_APPLIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "IMPLEMENTATION_DRY_RUN_OPERATIONS" in manifest
    assert "IMPLEMENTATION_DRY_RUN_CASE_RESULTS" in manifest


def test_task_17_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()
    paths = write_task_17_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["operations_path"]).exists()
    assert Path(paths["contracts_path"]).exists()
    assert Path(paths["regressions_path"]).exists()
    assert Path(paths["rollback_path"]).exists()
    assert Path(paths["boundary_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_17_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "IMPLEMENTATION_DRY_RUN_ONLY_NEXT_REVIEW_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_17_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_dry_run()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
