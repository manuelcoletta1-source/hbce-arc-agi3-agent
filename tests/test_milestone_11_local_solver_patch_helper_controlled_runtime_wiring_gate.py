from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate import (
    EXPECTED_CHECK_COUNT,
    EXPECTED_RUNTIME_AUTHORIZATION_ITEM_COUNT,
    EXPECTED_RUNTIME_DENIAL_ITEM_COUNT,
    EXPECTED_RUNTIME_GATE_CASE_COUNT,
    EXPECTED_RUNTIME_GATE_CASE_FAILURE_COUNT,
    EXPECTED_RUNTIME_GATE_CASE_PASS_COUNT,
    EXPECTED_RUNTIME_GATE_RULE_COUNT,
    EXPECTED_RUNTIME_STOP_CONDITION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate,
    build_runtime_gate_authorizations,
    build_runtime_gate_decision,
    build_runtime_gate_denials,
    build_runtime_gate_rules,
    build_runtime_gate_scorecard,
    build_runtime_gate_stop_conditions,
    build_task_18_source_summary,
    build_task_19_checks,
    evaluate_all_task_19_cases,
    evaluate_task_19_case,
    render_task_19_manifest,
    render_task_19_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate,
    write_task_19_artifacts,
)


def test_task_19_source_summary_reads_task_18():
    source = build_task_18_source_summary()
    assert source["task_18_present"] is True
    assert source["task_18_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_READY"
    assert source["task_18_id"].startswith(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-REVIEW-"
    )
    assert source["task_18_ready"] is True
    assert source["implementation_review_ready"] is True
    assert source["implementation_review_passed"] is True
    assert source["controlled_runtime_wiring_gate_recommended"] is True
    assert source["controlled_runtime_wiring_authorized"] is False
    assert source["runtime_solver_patch_allowed"] is False
    assert source["ranker_runtime_patch_allowed"] is False


def test_runtime_gate_rules_pass():
    rules = build_runtime_gate_rules()
    assert len(rules) == EXPECTED_RUNTIME_GATE_RULE_COUNT
    assert all(item["required"] is True for item in rules)
    assert all(item["passed"] is True for item in rules)
    assert all(item["allows_runtime_mutation"] is False for item in rules)
    assert all(item["failure_action"] == "STOP_CONTROLLED_RUNTIME_WIRING_GATE" for item in rules)


def test_runtime_gate_authorizations_are_plan_only():
    authorizations = build_runtime_gate_authorizations()
    assert len(authorizations) == EXPECTED_RUNTIME_AUTHORIZATION_ITEM_COUNT
    assert all(item["authorized"] is True for item in authorizations)
    assert all(item["scope"] == "PLAN_ONLY" for item in authorizations)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in authorizations)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in authorizations)
    assert all(item["score_claim_allowed"] is False for item in authorizations)
    assert all(item["submission_allowed"] is False for item in authorizations)


def test_runtime_gate_denials_active():
    denials = build_runtime_gate_denials()
    assert len(denials) == EXPECTED_RUNTIME_DENIAL_ITEM_COUNT
    assert all(item["denied"] is True for item in denials)
    assert all(item["failure_action"] == "STOP_AND_REVIEW" for item in denials)


def test_runtime_gate_stop_conditions_inactive():
    stops = build_runtime_gate_stop_conditions()
    assert len(stops) == EXPECTED_RUNTIME_STOP_CONDITION_COUNT
    assert all(item["active"] is False for item in stops)
    assert all(item["severity"] == "BLOCKING" for item in stops)


def test_runtime_gate_decision_authorizes_plan_only():
    decision = build_runtime_gate_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["controlled_runtime_wiring_gate_ready"] is True
    assert decision["controlled_runtime_wiring_gate_passed"] is True
    assert decision["controlled_runtime_wiring_plan_authorized"] is True
    assert decision["controlled_runtime_wiring_authorized"] is False
    assert decision["runtime_solver_patch_allowed"] is False
    assert decision["ranker_runtime_patch_allowed"] is False
    assert decision["runtime_solver_patch_applied"] is False
    assert decision["ranker_runtime_patch_applied"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_19_checks_all_pass():
    checks = build_task_19_checks()
    assert all(checks.values())


def test_each_task_19_case_passes():
    case_ids = [
        "m11_task19_source_task18_ready_v1",
        "m11_task19_review_passed_v1",
        "m11_task19_recommendation_present_v1",
        "m11_task19_gate_rules_v1",
        "m11_task19_authorizations_v1",
        "m11_task19_denials_v1",
        "m11_task19_stop_conditions_v1",
        "m11_task19_boundary_v1",
        "m11_task19_score_submission_blocked_v1",
        "m11_task19_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_19_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_19_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_19_case("missing_task_19_case")


def test_all_task_19_cases_pass():
    results = evaluate_all_task_19_cases()
    assert len(results) == EXPECTED_RUNTIME_GATE_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_runtime_gate_scorecard_passes():
    scorecard = build_runtime_gate_scorecard()
    assert len(scorecard) == 19
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_19_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_19_ready"] is True
    assert record["controlled_runtime_wiring_gate_ready"] is True
    assert record["controlled_runtime_wiring_gate_passed"] is True
    assert record["controlled_runtime_wiring_plan_authorized"] is True
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["runtime_solver_patch_applied"] is False
    assert record["ranker_runtime_patch_applied"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["runtime_gate_rule_count"] == EXPECTED_RUNTIME_GATE_RULE_COUNT
    assert record["runtime_authorization_item_count"] == EXPECTED_RUNTIME_AUTHORIZATION_ITEM_COUNT
    assert record["runtime_denial_item_count"] == EXPECTED_RUNTIME_DENIAL_ITEM_COUNT
    assert record["runtime_stop_condition_count"] == EXPECTED_RUNTIME_STOP_CONDITION_COUNT
    assert record["runtime_gate_check_count"] == EXPECTED_CHECK_COUNT
    assert record["runtime_gate_case_count"] == EXPECTED_RUNTIME_GATE_CASE_COUNT
    assert record["runtime_gate_case_pass_count"] == EXPECTED_RUNTIME_GATE_CASE_PASS_COUNT
    assert record["runtime_gate_case_failure_count"] == EXPECTED_RUNTIME_GATE_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["runtime_gate_gate_count"]
    assert record["runtime_gate_issue_count"] == 0


def test_task_19_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()
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


def test_task_19_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_19_ready"] is True
    assert payload["controlled_runtime_wiring_gate_passed"] is True
    assert payload["controlled_runtime_wiring_plan_authorized"] is True
    assert payload["controlled_runtime_wiring_authorized"] is False


def test_task_19_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()
    markdown = render_task_19_markdown(record)
    manifest = render_task_19_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_19_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_19_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_GATE_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_PLAN_AUTHORIZED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "CONTROLLED_RUNTIME_WIRING_GATE_RULES" in manifest
    assert "CONTROLLED_RUNTIME_WIRING_GATE_CASE_RESULTS" in manifest


def test_task_19_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()
    paths = write_task_19_artifacts(record, output_dir=str(tmp_path))
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
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_GATE_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_19_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "CONTROLLED_RUNTIME_WIRING_GATE_ONLY_NEXT_PLAN_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_19_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_runtime_wiring_gate()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
