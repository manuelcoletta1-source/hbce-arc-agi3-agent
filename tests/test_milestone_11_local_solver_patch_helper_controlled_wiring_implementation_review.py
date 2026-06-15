from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review import (
    EXPECTED_ACCEPTANCE_ITEM_COUNT,
    EXPECTED_REVIEW_CASE_COUNT,
    EXPECTED_REVIEW_CASE_FAILURE_COUNT,
    EXPECTED_REVIEW_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_REVIEW_CRITERION_COUNT,
    EXPECTED_REVIEW_FINDING_COUNT,
    EXPECTED_STOP_CONDITION_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_acceptance_items,
    build_implementation_review_scorecard,
    build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review,
    build_review_criteria,
    build_review_decision,
    build_review_findings,
    build_stop_conditions,
    build_task_17_source_summary,
    build_task_18_checks,
    evaluate_all_task_18_cases,
    evaluate_task_18_case,
    render_task_18_manifest,
    render_task_18_markdown,
    run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review_pipeline,
    validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review,
    write_task_18_artifacts,
)


def test_task_18_source_summary_reads_task_17():
    source = build_task_17_source_summary()
    assert source["task_17_present"] is True
    assert source["task_17_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_DRY_RUN_V1_READY"
    assert source["task_17_id"].startswith(
        "MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-CONTROLLED-WIRING-IMPLEMENTATION-DRY-RUN-"
    )
    assert source["task_17_ready"] is True
    assert source["implementation_dry_run_ready"] is True
    assert source["implementation_dry_run_passed"] is True
    assert source["implementation_review_authorized"] is True
    assert source["runtime_solver_patch_applied"] is False
    assert source["ranker_runtime_patch_applied"] is False
    assert source["runtime_wiring_performed"] is False


def test_review_findings_pass():
    findings = build_review_findings()
    assert len(findings) == EXPECTED_REVIEW_FINDING_COUNT
    assert all(item["passed"] is True for item in findings)
    assert all(item["severity"] == "PASS" for item in findings)
    assert all(item["recommendation"] == "ALLOW_CONTROLLED_RUNTIME_WIRING_GATE_REVIEW" for item in findings)


def test_review_criteria_pass():
    criteria = build_review_criteria()
    assert len(criteria) == EXPECTED_REVIEW_CRITERION_COUNT
    assert all(item["required"] is True for item in criteria)
    assert all(item["passed"] is True for item in criteria)
    assert all(item["failure_action"] == "STOP_IMPLEMENTATION_REVIEW" for item in criteria)


def test_acceptance_items_are_review_only():
    items = build_acceptance_items()
    assert len(items) == EXPECTED_ACCEPTANCE_ITEM_COUNT
    assert all(item["accepted"] is True for item in items)
    assert all(item["scope"] == "REVIEW_ACCEPTANCE_ONLY" for item in items)
    assert all(item["runtime_solver_mutation_allowed"] is False for item in items)
    assert all(item["ranker_runtime_mutation_allowed"] is False for item in items)
    assert all(item["score_claim_allowed"] is False for item in items)
    assert all(item["submission_allowed"] is False for item in items)


def test_stop_conditions_inactive():
    stops = build_stop_conditions()
    assert len(stops) == EXPECTED_STOP_CONDITION_COUNT
    assert all(item["active"] is False for item in stops)
    assert all(item["severity"] == "BLOCKING" for item in stops)


def test_review_decision_recommends_gate_only():
    decision = build_review_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["implementation_review_ready"] is True
    assert decision["implementation_review_passed"] is True
    assert decision["controlled_runtime_wiring_gate_recommended"] is True
    assert decision["controlled_runtime_wiring_authorized"] is False
    assert decision["runtime_solver_patch_allowed"] is False
    assert decision["ranker_runtime_patch_allowed"] is False
    assert decision["runtime_wiring_performed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_18_checks_all_pass():
    checks = build_task_18_checks()
    assert all(checks.values())


def test_each_task_18_case_passes():
    case_ids = [
        "m11_task18_source_task17_ready_v1",
        "m11_task18_dry_run_passed_v1",
        "m11_task18_operations_reviewed_v1",
        "m11_task18_contracts_reviewed_v1",
        "m11_task18_regression_reviewed_v1",
        "m11_task18_rollback_reviewed_v1",
        "m11_task18_boundary_reviewed_v1",
        "m11_task18_score_submission_blocked_v1",
        "m11_task18_fail_closed_v1",
        "m11_task18_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_18_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_18_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_18_case("missing_task_18_case")


def test_all_task_18_cases_pass():
    results = evaluate_all_task_18_cases()
    assert len(results) == EXPECTED_REVIEW_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_implementation_review_scorecard_passes():
    scorecard = build_implementation_review_scorecard()
    assert len(scorecard) == 18
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_18_record_ready():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_18_ready"] is True
    assert record["implementation_review_ready"] is True
    assert record["implementation_review_passed"] is True
    assert record["controlled_runtime_wiring_gate_recommended"] is True
    assert record["controlled_runtime_wiring_authorized"] is False
    assert record["runtime_solver_patch_allowed"] is False
    assert record["ranker_runtime_patch_allowed"] is False
    assert record["runtime_wiring_performed"] is False
    assert record["review_finding_count"] == EXPECTED_REVIEW_FINDING_COUNT
    assert record["review_criterion_count"] == EXPECTED_REVIEW_CRITERION_COUNT
    assert record["acceptance_item_count"] == EXPECTED_ACCEPTANCE_ITEM_COUNT
    assert record["stop_condition_count"] == EXPECTED_STOP_CONDITION_COUNT
    assert record["review_check_count"] == EXPECTED_CHECK_COUNT
    assert record["review_case_count"] == EXPECTED_REVIEW_CASE_COUNT
    assert record["review_case_pass_count"] == EXPECTED_REVIEW_CASE_PASS_COUNT
    assert record["review_case_failure_count"] == EXPECTED_REVIEW_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["implementation_review_gate_count"]
    assert record["implementation_review_issue_count"] == 0


def test_task_18_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
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


def test_task_18_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
    validation = validate_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_18_ready"] is True
    assert payload["implementation_review_passed"] is True
    assert payload["controlled_runtime_wiring_gate_recommended"] is True
    assert payload["controlled_runtime_wiring_authorized"] is False


def test_task_18_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
    markdown = render_task_18_markdown(record)
    manifest = render_task_18_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_18_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_18_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_IMPLEMENTATION_REVIEW_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_GATE_RECOMMENDED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_RUNTIME_WIRING_AUTHORIZED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "IMPLEMENTATION_REVIEW_FINDINGS" in manifest
    assert "IMPLEMENTATION_REVIEW_CASE_RESULTS" in manifest


def test_task_18_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()
    paths = write_task_18_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["findings_path"]).exists()
    assert Path(paths["criteria_path"]).exists()
    assert Path(paths["acceptance_path"]).exists()
    assert Path(paths["stops_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_WIRING_IMPLEMENTATION_REVIEW_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_18_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "IMPLEMENTATION_REVIEW_ONLY_NEXT_CONTROLLED_RUNTIME_WIRING_GATE_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_18_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_controlled_wiring_implementation_review()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
