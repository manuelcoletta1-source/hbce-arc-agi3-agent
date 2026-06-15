from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan import (
    EXPECTED_CHECK_COUNT,
    EXPECTED_IMPORT_SURFACE_COUNT,
    EXPECTED_OPERATOR_REVIEW_GATE_COUNT,
    EXPECTED_PLAN_CASE_COUNT,
    EXPECTED_PLAN_CASE_FAILURE_COUNT,
    EXPECTED_PLAN_CASE_PASS_COUNT,
    EXPECTED_PREFLIGHT_CONTRACT_COUNT,
    EXPECTED_RUNTIME_REGRESSION_TEST_COUNT,
    EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT,
    EXPECTED_RUNTIME_WIRING_STEP_COUNT,
    EXPECTED_RUNTIME_WIRING_TARGET_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_import_surface_plan,
    build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan,
    build_operator_review_gates,
    build_preflight_contracts,
    build_runtime_regression_plan,
    build_runtime_rollback_plan,
    build_runtime_wiring_plan_decision,
    build_runtime_wiring_plan_scorecard,
    build_runtime_wiring_steps,
    build_runtime_wiring_targets,
    build_task_19_source_summary,
    build_task_20_checks,
    evaluate_all_task_20_cases,
    evaluate_task_20_case,
    render_task_20_manifest,
    render_task_20_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan,
    write_task_20_artifacts,
)


def test_task_20_source_summary_reads_task_19():
    source = build_task_19_source_summary()
    assert source["task_19_present"] is True
    assert source["task_19_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1_READY"
    assert source["task_19_id"].startswith(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-RUNTIME-WIRING-GATE-"
    )
    assert source["task_19_ready"] is True
    assert source["controlled_runtime_wiring_gate_ready"] is True
    assert source["controlled_runtime_wiring_gate_passed"] is True
    assert source["controlled_runtime_wiring_plan_authorized"] is True
    assert source["controlled_runtime_wiring_authorized"] is False
    assert source["runtime_solver_patch_allowed"] is False
    assert source["ranker_runtime_patch_allowed"] is False


def test_runtime_wiring_targets_are_plan_only():
    targets = build_runtime_wiring_targets()
    assert len(targets) == EXPECTED_RUNTIME_WIRING_TARGET_COUNT
    assert all(item["planned"] is True for item in targets)
    assert all(item["plan_only"] is True for item in targets)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in targets)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in targets)


def test_import_surface_plan_is_not_applied():
    surfaces = build_import_surface_plan()
    assert len(surfaces) == EXPECTED_IMPORT_SURFACE_COUNT
    assert all(item["plan_only"] is True for item in surfaces)
    assert all(item["import_allowed_now"] is False for item in surfaces)
    assert all(item["requires_dry_run"] is True for item in surfaces)
    assert all(item["requires_review"] is True for item in surfaces)


def test_preflight_contracts_pass():
    contracts = build_preflight_contracts()
    assert len(contracts) == EXPECTED_PREFLIGHT_CONTRACT_COUNT
    assert all(item["required"] is True for item in contracts)
    assert all(item["passed"] is True for item in contracts)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in contracts)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in contracts)


def test_runtime_wiring_steps_are_plan_only():
    steps = build_runtime_wiring_steps()
    assert len(steps) == EXPECTED_RUNTIME_WIRING_STEP_COUNT
    assert all(item["planned"] is True for item in steps)
    assert all(item["plan_only"] is True for item in steps)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in steps)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in steps)


def test_regression_and_rollback_plan_are_local_only():
    regressions = build_runtime_regression_plan()
    rollbacks = build_runtime_rollback_plan()
    assert len(regressions) == EXPECTED_RUNTIME_REGRESSION_TEST_COUNT
    assert len(rollbacks) == EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT
    assert all(item["local_only"] is True for item in regressions)
    assert all(item["executed_now"] is False for item in regressions)
    assert all(item["external_api_dependency"] is False for item in regressions)
    assert all(item["required"] is True for item in rollbacks)
    assert all(item["ready"] is True for item in rollbacks)
    assert all(item["executed_now"] is False for item in rollbacks)


def test_operator_review_gates_required():
    gates = build_operator_review_gates()
    assert len(gates) == EXPECTED_OPERATOR_REVIEW_GATE_COUNT
    assert all(item["required"] is True for item in gates)
    assert all(item["passed"] is True for item in gates)
    assert all(item["manual_runtime_mutation_allowed"] is False for item in gates)


def test_runtime_wiring_plan_decision_authorizes_dry_run_only():
    decision = build_runtime_wiring_plan_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["runtime_wiring_plan_ready"] is True
    assert decision["runtime_wiring_plan_passed"] is True
    assert decision["runtime_wiring_dry_run_authorized"] is True
    assert decision["controlled_runtime_wiring_authorized"] is False
    assert decision["runtime_solver_patch_allowed"] is False
    assert decision["ranker_runtime_patch_allowed"] is False
    assert decision["runtime_solver_patch_applied"] is False
    assert decision["ranker_runtime_patch_applied"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_20_checks_all_pass():
    checks = build_task_20_checks()
    assert all(checks.values())


def test_each_task_20_case_passes():
    case_ids = [
        "m11_task20_source_task19_ready_v1",
        "m11_task20_gate_passed_v1",
        "m11_task20_targets_planned_v1",
        "m11_task20_import_surface_planned_v1",
        "m11_task20_contracts_planned_v1",
        "m11_task20_steps_planned_v1",
        "m11_task20_regression_planned_v1",
        "m11_task20_rollback_planned_v1",
        "m11_task20_boundary_v1",
        "m11_task20_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_20_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_20_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_20_case("missing_task_20_case")


def test_all_task_20_cases_pass():
    results = evaluate_all_task_20_cases()
    assert len(results) == EXPECTED_PLAN_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_runtime_wiring_plan_scorecard_passes():
    scorecard = build_runtime_wiring_plan_scorecard()
    assert len(scorecard) == 21
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_20_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_20_ready"] is True
    assert record["runtime_wiring_plan_ready"] is True
    assert record["runtime_wiring_plan_passed"] is True
    assert record["runtime_wiring_dry_run_authorized"] is True
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["ranker_runtime_patch_applied"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_wiring_target_count"] == EXPECTED_RUNTIME_WIRING_TARGET_COUNT
    assert record["import_surface_count"] == EXPECTED_IMPORT_SURFACE_COUNT
    assert record["preflight_contract_count"] == EXPECTED_PREFLIGHT_CONTRACT_COUNT
    assert record["runtime_wiring_step_count"] == EXPECTED_RUNTIME_WIRING_STEP_COUNT
    assert record["runtime_regression_test_count"] == EXPECTED_RUNTIME_REGRESSION_TEST_COUNT
    assert record["runtime_rollback_item_count"] == EXPECTED_RUNTIME_ROLLBACK_ITEM_COUNT
    assert record["operator_review_gate_count"] == EXPECTED_OPERATOR_REVIEW_GATE_COUNT
    assert record["runtime_wiring_plan_check_count"] == EXPECTED_CHECK_COUNT
    assert record["runtime_wiring_plan_case_count"] == EXPECTED_PLAN_CASE_COUNT
    assert record["runtime_wiring_plan_case_pass_count"] == EXPECTED_PLAN_CASE_PASS_COUNT
    assert record["runtime_wiring_plan_case_failure_count"] == EXPECTED_PLAN_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["runtime_wiring_plan_gate_count"]
    assert record["runtime_wiring_plan_issue_count"] == 0


def test_task_20_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
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


def test_task_20_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_20_ready"] is True
    assert payload["runtime_wiring_plan_passed"] is True
    assert payload["runtime_wiring_dry_run_authorized"] is True
    assert payload["controlled_runtime_wiring_authorized"] is False


def test_task_20_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
    markdown = render_task_20_markdown(record)
    manifest = render_task_20_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_20_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_20_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PLAN_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_DRY_RUN_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CONTROLLED_RUNTIME_WIRING_PLAN_TARGETS" in manifest
    assert "CONTROLLED_RUNTIME_WIRING_PLAN_CASE_RESULTS" in manifest


def test_task_20_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()
    paths = write_task_20_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["targets_path"]).exists()
    assert Path(paths["import_surface_path"]).exists()
    assert Path(paths["contracts_path"]).exists()
    assert Path(paths["steps_path"]).exists()
    assert Path(paths["regressions_path"]).exists()
    assert Path(paths["rollback_path"]).exists()
    assert Path(paths["review_gates_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_PLAN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_20_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "CONTROLLED_RUNTIME_WIRING_PLAN_ONLY_NEXT_DRY_RUN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_20_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
