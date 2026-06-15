from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_solver_patch_helper_wiring_review import (
    EXPECTED_ADAPTER_COUNT,
    EXPECTED_CASE_COUNT,
    EXPECTED_CASE_FAILURE_COUNT,
    EXPECTED_CASE_PASS_COUNT,
    EXPECTED_CHECK_COUNT,
    EXPECTED_DRY_RUN_FAILURE_COUNT,
    EXPECTED_DRY_RUN_OUTPUT_COUNT,
    EXPECTED_DRY_RUN_PASS_COUNT,
    EXPECTED_LAYER_COUNT,
    EXPECTED_REVIEW_CRITERION_COUNT,
    EXPECTED_REVIEW_FINDING_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_milestone_11_local_solver_patch_helper_wiring_review,
    build_review_criteria,
    build_review_decision,
    build_review_findings,
    build_review_scorecard,
    build_task_13_source_summary,
    build_task_14_checks,
    evaluate_all_task_14_cases,
    evaluate_task_14_case,
    render_task_14_manifest,
    render_task_14_markdown,
    run_milestone_11_local_solver_patch_helper_wiring_review_pipeline,
    validate_milestone_11_local_solver_patch_helper_wiring_review,
    write_task_14_artifacts,
)


def test_task_14_source_summary_reads_task_13():
    source = build_task_13_source_summary()
    assert source["task_13_present"] is True
    assert source["task_13_status"] == "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_DRY_RUN_V1_READY"
    assert source["task_13_id"].startswith("MILESTONE-11-LOCAL-SOLVER-PATCH-HELPER-WIRING-DRY-RUN-")
    assert source["task_13_ready"] is True
    assert source["dry_run_ready"] is True
    assert source["dry_run_passed"] is True
    assert source["wiring_dry_run"] is True
    assert source["wiring_performed"] is False
    assert source["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert source["layer_count"] == EXPECTED_LAYER_COUNT
    assert source["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert source["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert source["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT


def test_review_findings_all_pass():
    findings = build_review_findings()
    assert len(findings) == EXPECTED_REVIEW_FINDING_COUNT
    assert all(item["passed"] is True for item in findings)
    assert all(item["severity"] == "PASS" for item in findings)


def test_review_criteria_all_pass():
    criteria = build_review_criteria()
    assert len(criteria) == EXPECTED_REVIEW_CRITERION_COUNT
    assert all(item["required"] is True for item in criteria)
    assert all(item["passed"] is True for item in criteria)
    assert all(item["failure_action"] == "STOP_REVIEW_AND_REPAIR" for item in criteria)


def test_review_decision_conservative():
    decision = build_review_decision()
    assert decision["verdict"] == TASK_VERDICT
    assert decision["review_ready"] is True
    assert decision["review_passed"] is True
    assert decision["dry_run_accepted"] is True
    assert decision["controlled_gate_recommended"] is True
    assert decision["runtime_wiring_performed"] is False
    assert decision["runtime_solver_modification_allowed"] is False
    assert decision["ranker_runtime_modification_allowed"] is False
    assert decision["score_claim_allowed"] is False
    assert decision["real_submission_allowed"] is False
    assert decision["next_stage"] == NEXT_STAGE


def test_task_14_checks_all_pass():
    checks = build_task_14_checks()
    assert all(checks.values())


def test_each_task_14_case_passes():
    case_ids = [
        "m11_task14_source_task13_ready_v1",
        "m11_task14_dry_run_passed_v1",
        "m11_task14_adapter_layer_counts_v1",
        "m11_task14_output_integrity_v1",
        "m11_task14_runtime_boundary_v1",
        "m11_task14_score_boundary_v1",
        "m11_task14_submission_boundary_v1",
        "m11_task14_fail_closed_boundary_v1",
        "m11_task14_review_decision_v1",
        "m11_task14_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_14_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_14_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_14_case("missing_task_14_case")


def test_all_task_14_cases_pass():
    results = evaluate_all_task_14_cases()
    assert len(results) == EXPECTED_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_review_scorecard_passes():
    scorecard = build_review_scorecard()
    assert len(scorecard) == EXPECTED_REVIEW_CRITERION_COUNT
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_14_record_ready():
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_14_ready"] is True
    assert record["review_ready"] is True
    assert record["review_passed"] is True
    assert record["dry_run_accepted"] is True
    assert record["controlled_gate_recommended"] is True
    assert record["runtime_wiring_performed"] is False
    assert record["review_finding_count"] == EXPECTED_REVIEW_FINDING_COUNT
    assert record["review_criterion_count"] == EXPECTED_REVIEW_CRITERION_COUNT
    assert record["adapter_count"] == EXPECTED_ADAPTER_COUNT
    assert record["layer_count"] == EXPECTED_LAYER_COUNT
    assert record["dry_run_output_count"] == EXPECTED_DRY_RUN_OUTPUT_COUNT
    assert record["dry_run_pass_count"] == EXPECTED_DRY_RUN_PASS_COUNT
    assert record["dry_run_failure_count"] == EXPECTED_DRY_RUN_FAILURE_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["external_solver_dependency"] is False
    assert record["review_check_count"] == EXPECTED_CHECK_COUNT
    assert record["review_case_count"] == EXPECTED_CASE_COUNT
    assert record["review_case_pass_count"] == EXPECTED_CASE_PASS_COUNT
    assert record["review_case_failure_count"] == EXPECTED_CASE_FAILURE_COUNT
    assert record["passed_gate_count"] == record["review_gate_count"]
    assert record["review_issue_count"] == 0


def test_task_14_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
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


def test_task_14_validation_and_pipeline_pass():
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
    validation = validate_milestone_11_local_solver_patch_helper_wiring_review(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_solver_patch_helper_wiring_review_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_14_ready"] is True
    assert payload["review_passed"] is True
    assert payload["controlled_gate_recommended"] is True


def test_task_14_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
    markdown = render_task_14_markdown(record)
    manifest = render_task_14_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_14_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_14_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_REVIEW_PASSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_CONTROLLED_GATE_RECOMMENDED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_WIRING_PERFORMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_EXTERNAL_SOLVER_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REVIEW_FINDINGS" in manifest
    assert "REVIEW_CASE_RESULTS" in manifest


def test_task_14_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_solver_patch_helper_wiring_review()
    paths = write_task_14_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["findings_path"]).exists()
    assert Path(paths["criteria_path"]).exists()
    assert Path(paths["decision_path"]).exists()
    assert Path(paths["scorecard_path"]).exists()
    assert "MILESTONE_11_LOCAL_SOLVER_PATCH_HELPER_WIRING_REVIEW_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_14_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "REVIEW_ONLY_CONTROLLED_GATE_NEXT_NO_RUNTIME_WIRING_NO_SCORE_NO_SUBMISSION" in Path(
        paths["decision_path"]
    ).read_text(encoding="utf-8")


def test_task_14_metadata_safe():
    metadata = build_milestone_11_local_solver_patch_helper_wiring_review()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
