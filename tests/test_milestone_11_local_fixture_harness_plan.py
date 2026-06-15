from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_fixture_harness_plan import (
    EXPECTED_BOUNDARY_RULE_COUNT,
    EXPECTED_FIXTURE_CLASS_COUNT,
    EXPECTED_HARNESS_CASE_COUNT,
    EXPECTED_HARNESS_CHECK_COUNT,
    EXPECTED_HARNESS_COMPONENT_COUNT,
    EXPECTED_HARNESS_FAILURE_COUNT,
    EXPECTED_HARNESS_PASS_COUNT,
    EXPECTED_MEASUREMENT_AXIS_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_harness_scorecard,
    build_local_fixture_harness_plan,
    build_milestone_11_local_fixture_harness_plan,
    build_task_3_source_summary,
    build_task_4_checks,
    build_task_4_next_action_plan,
    evaluate_all_task_4_cases,
    evaluate_task_4_case,
    render_task_4_manifest,
    render_task_4_markdown,
    run_milestone_11_local_fixture_harness_plan_pipeline,
    validate_milestone_11_local_fixture_harness_plan,
    write_task_4_artifacts,
)


def test_task_4_source_summary_reads_task_3():
    source = build_task_3_source_summary()
    assert source["task_3_present"] is True
    assert source["task_3_status"] == "MILESTONE_11_PUBLIC_GAME_FAILURE_TAXONOMY_V1_READY"
    assert source["task_3_id"].startswith("MILESTONE-11-PUBLIC-GAME-FAILURE-TAXONOMY-")
    assert source["task_3_ready"] is True
    assert source["primary_condition"] == "NO_LOCAL_PUBLIC_FIXTURES"
    assert source["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert source["solver_failure_detected"] is False
    assert source["solver_not_measured"] is True
    assert source["real_public_score_claimed"] is False
    assert source["private_score_claimed"] is False
    assert source["real_benchmark_score"] is None
    assert source["real_submission_allowed"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_local_fixture_harness_plan_is_diagnostic_only():
    plan = build_local_fixture_harness_plan()
    assert plan["harness_plan_id"] == "M11-TASK4-LOCAL-FIXTURE-HARNESS-PLAN-v1"
    assert plan["diagnostic_only"] is True
    assert plan["fixture_generation_performed"] is False
    assert plan["fixture_generation_deferred_to"] == NEXT_STAGE
    assert plan["synthetic_fixture_allowed"] is True
    assert plan["synthetic_fixture_score_claim_allowed"] is False
    assert plan["official_score_claim_allowed"] is False
    assert plan["result_label"] == "LOCAL_DIAGNOSTIC_ONLY_NOT_KAGGLE_SCORE"
    assert len(plan["harness_components"]) == EXPECTED_HARNESS_COMPONENT_COUNT
    assert len(plan["fixture_classes"]) == EXPECTED_FIXTURE_CLASS_COUNT
    assert len(plan["measurement_axes"]) == EXPECTED_MEASUREMENT_AXIS_COUNT
    assert len(plan["boundary_rules"]) == EXPECTED_BOUNDARY_RULE_COUNT


def test_task_4_next_action_plan_is_safe():
    actions = build_task_4_next_action_plan()
    assert len(actions) == 4
    assert all(action["status"] == "PLANNED" for action in actions)
    assert all(action["requires_real_submission"] is False for action in actions)
    assert all(action["score_claim_allowed"] is False for action in actions)


def test_task_4_checks_all_pass():
    checks = build_task_4_checks()
    assert all(checks.values())


def test_each_task_4_case_passes():
    case_ids = [
        "m11_task4_source_task3_ready_v1",
        "m11_task4_measurement_constraint_loaded_v1",
        "m11_task4_harness_components_ready_v1",
        "m11_task4_fixture_classes_ready_v1",
        "m11_task4_measurement_axes_ready_v1",
        "m11_task4_boundary_rules_ready_v1",
        "m11_task4_diagnostic_only_enforced_v1",
        "m11_task4_real_submission_blocked_v1",
        "m11_task4_next_stage_valid_v1",
        "m11_task4_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_4_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_4_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_4_case("missing_task_4_case")


def test_all_task_4_cases_pass():
    results = evaluate_all_task_4_cases()
    assert len(results) == EXPECTED_HARNESS_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_harness_scorecard_passes():
    scorecard = build_harness_scorecard()
    assert len(scorecard) == 9
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_4_record_ready():
    record = build_milestone_11_local_fixture_harness_plan()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_4_ready"] is True
    assert record["harness_plan_created"] is True
    assert record["harness_component_count"] == EXPECTED_HARNESS_COMPONENT_COUNT
    assert record["fixture_class_count"] == EXPECTED_FIXTURE_CLASS_COUNT
    assert record["measurement_axis_count"] == EXPECTED_MEASUREMENT_AXIS_COUNT
    assert record["boundary_rule_count"] == EXPECTED_BOUNDARY_RULE_COUNT
    assert record["diagnostic_only"] is True
    assert record["fixture_generation_performed"] is False
    assert record["fixture_generation_deferred_to"] == NEXT_STAGE
    assert record["official_score_claim_allowed"] is False
    assert record["synthetic_fixture_score_claim_allowed"] is False
    assert record["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert record["solver_failure_detected"] is False
    assert record["solver_not_measured"] is True
    assert record["harness_check_count"] == EXPECTED_HARNESS_CHECK_COUNT
    assert record["harness_case_count"] == EXPECTED_HARNESS_CASE_COUNT
    assert record["harness_pass_count"] == EXPECTED_HARNESS_PASS_COUNT
    assert record["harness_failure_count"] == EXPECTED_HARNESS_FAILURE_COUNT
    assert record["passed_gate_count"] == record["harness_gate_count"]
    assert record["harness_issue_count"] == 0


def test_task_4_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_fixture_harness_plan()
    assert record["real_public_score_claimed"] is False
    assert record["private_score_claimed"] is False
    assert record["real_benchmark_score"] is None
    assert record["real_submission_candidate_created"] is False
    assert record["submission_json_created"] is False
    assert record["upload_package_created"] is False
    assert record["real_submission_decision"] == "NOT_AUTHORIZED"
    assert record["real_submission_allowed"] is False
    assert record["manual_upload_allowed"] is False
    assert record["kaggle_authentication_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["fail_closed_required"] is True
    assert record["fail_closed_active"] is True


def test_task_4_validation_and_pipeline_pass():
    record = build_milestone_11_local_fixture_harness_plan()
    validation = validate_milestone_11_local_fixture_harness_plan(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_fixture_harness_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_4_ready"] is True
    assert payload["harness_pass_count"] == 10
    assert payload["harness_failure_count"] == 0


def test_task_4_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_fixture_harness_plan()
    markdown = render_task_4_markdown(record)
    manifest = render_task_4_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_4_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "HARNESS_COMPONENTS" in manifest
    assert "FIXTURE_CLASSES" in manifest
    assert "MEASUREMENT_AXES" in manifest
    assert "BOUNDARY_RULES" in manifest
    assert "HARNESS_VALIDATION_RESULTS" in manifest


def test_task_4_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_fixture_harness_plan()
    paths = write_task_4_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["components_path"]).exists()
    assert Path(paths["fixture_classes_path"]).exists()
    assert Path(paths["boundary_rules_path"]).exists()
    assert Path(paths["next_actions_path"]).exists()
    assert "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_11_TASK_4_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "diagnostic_only" in Path(paths["index_path"]).read_text(encoding="utf-8")


def test_task_4_metadata_safe():
    metadata = build_milestone_11_local_fixture_harness_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_4_index_is_conservative():
    index = build_milestone_11_local_fixture_harness_plan()["harness_index"]
    assert index["primary_classification"] == "MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE"
    assert index["harness_component_count"] == EXPECTED_HARNESS_COMPONENT_COUNT
    assert index["fixture_class_count"] == EXPECTED_FIXTURE_CLASS_COUNT
    assert index["measurement_axis_count"] == EXPECTED_MEASUREMENT_AXIS_COUNT
    assert index["boundary_rule_count"] == EXPECTED_BOUNDARY_RULE_COUNT
    assert index["diagnostic_only"] is True
    assert index["fixture_generation_performed"] is False
    assert index["official_score_claim_allowed"] is False
    assert index["real_public_score_claimed"] is False
    assert index["private_score_claimed"] is False
    assert index["real_benchmark_score"] is None
    assert index["real_submission_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_active"] is True
