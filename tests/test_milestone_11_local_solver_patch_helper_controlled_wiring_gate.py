from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_wiring_gate import (
    EXPECTED_ADAPTER_COUNT,
    EXPECTED_AUTHORIZATION_ITEM_COUNT,
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_DENIAL_ITEM_COUNT,
    EXPECTED_DRY_RUN_FAILURE_COUNT,
    EXPECTED_DRY_RUN_OUTPUT_COUNT,
    EXPECTED_DRY_RUN_PASS_COUNT,
    EXPECTED_GATE_RULE_COUNT,
    EXPECTED_LAYER_COUNT,
    EXPECTED_STOP_CONDITION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_authorization_items,
    build_controlled_gate_scorecard,
    build_denial_items,
    build_gate_decision,
    build_gate_rules,
    build_milestone_11_local_solver_patch_helper_controlled_wiring_gate,
    build_stop_conditions,
    build_task_14_source_summary,
    build_task_15_checks,
    evaluate_all_task_15_cases,
    evaluate_task_15_case,
    render_task_15_manifest,
    render_task_15_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_wiring_gate_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_wiring_gate,
    write_task_15_artifacts,
)


def test_task_15_source_summary_reads_task_14():
    source = build_task_14_source_summary()
    assert source["task_14_present"] is True
    assert source["task_14_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY"
    assert source["task_14_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-REVIEW-")
    assert source["task_14_ready"] is True
    assert source["review_ready"] is True
    assert source["review_passed"] is True
    assert source["dry_run_accepted"] is True
    assert source["controlled_gate_recommended"] is True
    assert source["runtime_wiring_performed"] is False
    assert source["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert source["layer_count"] == EXPECTED_LAYER_COUNT
    assert source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert source["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert source["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT


def test_gate_rules_all_pass_and_block_runtime_mutation():
    rules = build_gate_rules()
    assert len(rules) == EXPECTED_GATE_RULE_COUNT
    assert all(item["required"] is True for item in rules)
    assert all(item["passed"] is True for item in rules)
    assert all(item["failure_action"] == "STOP_CONTROLLED_GATE" for item in rules)
    assert all(item["allows_runtime_mutation"] is False for item in rules)


def test_authorization_items_are_plan_only():
    items = build_authorization_items()
    assert len(items) == EXPECTED_AUTHORIZATION_ITEM_COUNT
    assert all(item["authorized"] is True for item in items)
    assert all(item["scope"] == "PLAN_OR_REVIEW_ONLY" for item in items)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in items)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in items)
    assert all(item["score_claim_allowed"] is False for item in items)
    assert all(item["submission_allowed"] is False for item in items)


def test_denial_items_block_runtime_score_submission():
    items = build_denial_items()
    assert len(items) == EXPECTED_DENIAL_ITEM_COUNT
    assert all(item["denied"] is True for item in items)
    assert all(item["failure_action"] == "STOP_AND_REVIEW" for item in items)


def test_stop_conditions_are_inactive_but_blocking():
    stops = build_stop_conditions()
    assert len(stops) == EXPECTED_STOP_CONDITION_COUNT
    assert all(item["active"] is False for item in stops)
    assert all(item["severity"] == "BLOCKING" for item in stops)
    assert all(item["action"] == "STOP_CONTROLLED_GATE" for item in stops)


def test_gate_decision_is_conservative():
    decision = build_gate_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["controlled_gate_ready"] is True
    assert decision["controlled_gate_passed"] is True
    assert decision["controlled_gate_status"] == "CONTROLLED_GATE_PASS"
    assert decision["implementation_plan_authorized"] is True
    assert decision["controlled_runtime_wiring_authorized"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_15_checks_all_pass():
    checks = build_task_15_checks()
    assert all(checks.values())


def test_each_task_15_case_passes():
    case_ids = [
        "m11_task15_source_task14_ready_v1",
        "m11_task15_review_passed_v1",
        "m11_task15_dry_run_accepted_v1",
        "m11_task15_gate_recommendation_v1",
        "m11_task15_artifact_counts_v1",
        "m11_task15_runtime_boundary_v1",
        "m11_task15_score_boundary_v1",
        "m11_task15_submission_boundary_v1",
        "m11_task15_fail_closed_boundary_v1",
        "m11_task15_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_15_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_15_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_15_case("missing_task_15_case")


def test_all_task_15_cases_pass():
    results = evaluate_all_task_15_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_controlled_gate_scorecard_passes():
    scorecard = build_controlled_gate_scorecard()
    assert len(scorecard) == 15
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_15_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_15_ready"] is True
    assert record["controlled_gate_ready"] is True
    assert record["controlled_gate_passed"] is True
    assert record["controlled_gate_status"] == "CONTROLLED_GATE_PASS"
    assert record["implementation_plan_authorized"] is True
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["gate_rule_count"] == EXPECTED_GATE_RULE_COUNT
    assert record["authorization_item_count"] == EXPECTED_AUTHORIZATION_ITEM_COUNT
    assert record["denial_item_count"] == EXPECTED_DENIAL_ITEM_COUNT
    assert record["stop_condition_count"] == EXPECTED_STOP_CONDITION_COUNT
    assert record["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert record["layer_count"] == EXPECTED_LAYER_COUNT
    assert record["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert record["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert record["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["gate_check_count"] == EXPECTED_CHECK_COUNT
    assert record["gate_case_count"] == EXPECTED_CASE_COUNT
    assert record["gate_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["gate_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["controlled_gate_gate_count"]
    assert record["controlled_gate_issue_count"] == 0


def test_task_15_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
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


def test_task_15_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_gate(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_wiring_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_15_ready"] is True
    assert payload["controlled_gate_passed"] is True
    assert payload["implementation_plan_authorized"] is True
    assert payload["controlled_runtime_wiring_authorized"] is False


def test_task_15_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
    markdown = render_task_15_markdown(record)
    manifest = render_task_15_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_15_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_15_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_PLAN_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CONTROLLED_GATE_RULES" in manifest
    assert "CONTROLLED_GATE_CASE_RESULTS" in manifest


def test_task_15_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()
    paths = write_task_15_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["rules_path"]).exists()
    assert Path(paths["authorization_path"]).exists()
    assert Path(paths["denials_path"]).exists()
    assert Path(paths["stops_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_GATE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_15_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "CONTROLLED_GATE_ONLY_IMPLEMENTATION_PLAN_NEXT_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_15_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_wiring_gate()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
