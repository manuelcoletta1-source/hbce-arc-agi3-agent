from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_11_local_diagnostic_fixture_harness import (
    EXPECTED_EPISODE_COUNT,
    EXPECTED_FIXTURE_COUNT,
    EXPECTED_HARNESS_CASE_COUNT,
    EXPECTED_HARNESS_CHECK_COUNT,
    EXPECTED_HARNESS_FAILURE_COUNT,
    EXPECTED_HARNESS_PASS_COUNT,
    EXPECTED_TRACE_RECORD_COUNT,
    NEXT_STAGE,
    PIPELINE_STATUS,
    STATUS,
    TASK_MODE,
    TASK_SCOPE,
    TASK_VERDICT,
    VALIDATION_STATUS,
    build_diagnostic_result_guard,
    build_fixture_schema,
    build_harness_scorecard,
    build_local_diagnostic_fixtures,
    build_milestone_11_local_diagnostic_fixture_harness,
    build_task_4_source_summary,
    build_task_5_checks,
    build_trace_records,
    evaluate_all_task_5_cases,
    evaluate_task_5_case,
    render_task_5_manifest,
    render_task_5_markdown,
    run_fixture_episode,
    run_local_diagnostic_fixture_harness,
    run_milestone_11_local_diagnostic_fixture_harness_pipeline,
    validate_fixture,
    validate_milestone_11_local_diagnostic_fixture_harness,
    write_task_5_artifacts,
)


def test_task_5_source_summary_reads_task_4():
    source = build_task_4_source_summary()
    assert source["task_4_present"] is True
    assert source["task_4_status"] == "MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY"
    assert source["task_4_id"].startswith("MILESTONE-11-LOCAL-FIXTURE-HARNESS-PLAN-")
    assert source["task_4_ready"] is True
    assert source["harness_plan_created"] is True
    assert source["diagnostic_only"] is True
    assert source["official_score_claim_allowed"] is False
    assert source["synthetic_fixture_score_claim_allowed"] is False
    assert source["real_public_score_claimed"] is False
    assert source["private_score_claimed"] is False
    assert source["real_benchmark_score"] is None
    assert source["real_submission_allowed"] is False
    assert source["kaggle_submission_sent"] is False
    assert source["fail_closed_active"] is True


def test_fixture_schema_is_public_safe_and_diagnostic_only():
    schema = build_fixture_schema()
    assert schema["schema_id"] == "M11-TASK5-LOCAL-DIAGNOSTIC-FIXTURE-SCHEMA-v1"
    assert schema["diagnostic_only_required"] is True
    assert schema["score_claim_allowed_required_value"] is False
    assert schema["external_api_dependency"] is False
    assert schema["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert "fixture_id" in schema["required_fields"]
    assert "diagnostic_only" in schema["required_fields"]
    assert "score_claim_allowed" in schema["required_fields"]


def test_local_diagnostic_fixtures_validate():
    fixtures = build_local_diagnostic_fixtures()
    assert len(fixtures) == EXPECTED_FIXTURE_COUNT
    assert all(validate_fixture(fixture) for fixture in fixtures)
    assert all(fixture["diagnostic_only"] is True for fixture in fixtures)
    assert all(fixture["score_claim_allowed"] is False for fixture in fixtures)


def test_fixture_episode_runner_is_deterministic():
    fixture = build_local_diagnostic_fixtures()[0]
    first = run_fixture_episode(fixture)
    second = run_fixture_episode(fixture)
    assert first == second
    assert first["episode_id"].startswith("EP-")
    assert first["diagnostic_only"] is True
    assert first["score_claim_allowed"] is False
    assert first["official_score_claim_allowed"] is False
    assert first["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"


def test_local_diagnostic_fixture_harness_runs_all_episodes():
    episodes = run_local_diagnostic_fixture_harness()
    assert len(episodes) == EXPECTED_EPISODE_COUNT
    assert all(episode["diagnostic_only"] is True for episode in episodes)
    assert all(episode["score_claim_allowed"] is False for episode in episodes)
    assert all(episode["official_score_claim_allowed"] is False for episode in episodes)
    assert all(episode["step_count"] >= 1 for episode in episodes)


def test_trace_records_are_diagnostic_only():
    traces = build_trace_records()
    assert len(traces) == EXPECTED_TRACE_RECORD_COUNT
    assert all(trace["diagnostic_only"] is True for trace in traces)
    assert all(trace["score_claim_allowed"] is False for trace in traces)
    assert all(trace["official_score_claim_allowed"] is False for trace in traces)
    assert all(trace["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for trace in traces)
    assert all(trace["trace_hash_16"] for trace in traces)


def test_diagnostic_result_guard_blocks_score_and_submission():
    guard = build_diagnostic_result_guard()
    assert guard["diagnostic_only"] is True
    assert guard["official_score_claim_allowed"] is False
    assert guard["synthetic_fixture_score_claim_allowed"] is False
    assert guard["public_score_claim_allowed"] is False
    assert guard["private_score_claim_allowed"] is False
    assert guard["submission_candidate_creation_allowed"] is False
    assert guard["submission_json_creation_allowed"] is False
    assert guard["upload_package_creation_allowed"] is False
    assert guard["kaggle_authentication_allowed"] is False
    assert guard["kaggle_submission_allowed"] is False
    assert guard["fail_closed_on_missing_label"] is True


def test_task_5_checks_all_pass():
    checks = build_task_5_checks()
    assert all(checks.values())


def test_each_task_5_case_passes():
    case_ids = [
        "m11_task5_source_task4_ready_v1",
        "m11_task5_fixture_schema_ready_v1",
        "m11_task5_minimal_fixtures_ready_v1",
        "m11_task5_episode_runner_ready_v1",
        "m11_task5_trace_records_ready_v1",
        "m11_task5_diagnostic_result_guard_ready_v1",
        "m11_task5_score_boundary_preserved_v1",
        "m11_task5_real_submission_blocked_v1",
        "m11_task5_next_stage_valid_v1",
        "m11_task5_metadata_safe_v1",
    ]
    for case_id in case_ids:
        result = evaluate_task_5_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_task_5_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_task_5_case("missing_task_5_case")


def test_all_task_5_cases_pass():
    results = evaluate_all_task_5_cases()
    assert len(results) == EXPECTED_HARNESS_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_harness_scorecard_passes():
    scorecard = build_harness_scorecard()
    assert len(scorecard) == 9
    assert all(item["passed"] is True for item in scorecard)
    assert all(item["score"] == 100 for item in scorecard)
    assert all(item["severity"] == "PASS" for item in scorecard)


def test_task_5_record_ready():
    record = build_milestone_11_local_diagnostic_fixture_harness()
    assert record["status"] == STATUS
    assert record["task_mode"] == TASK_MODE
    assert record["task_scope"] == TASK_SCOPE
    assert record["task_verdict"] == TASK_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["task_5_ready"] is True
    assert record["fixture_schema_created"] is True
    assert record["fixture_count"] == EXPECTED_FIXTURE_COUNT
    assert record["valid_fixture_count"] == EXPECTED_FIXTURE_COUNT
    assert record["episode_runner_created"] is True
    assert record["episode_count"] == EXPECTED_EPISODE_COUNT
    assert record["trace_record_count"] == EXPECTED_TRACE_RECORD_COUNT
    assert record["diagnostic_result_guard_active"] is True
    assert record["diagnostic_only"] is True
    assert record["official_score_claim_allowed"] is False
    assert record["synthetic_fixture_score_claim_allowed"] is False
    assert record["harness_check_count"] == EXPECTED_HARNESS_CHECK_COUNT
    assert record["harness_case_count"] == EXPECTED_HARNESS_CASE_COUNT
    assert record["harness_pass_count"] == EXPECTED_HARNESS_PASS_COUNT
    assert record["harness_failure_count"] == EXPECTED_HARNESS_FAILURE_COUNT
    assert record["passed_gate_count"] == record["harness_gate_count"]
    assert record["harness_issue_count"] == 0


def test_task_5_keeps_score_and_submission_blocked():
    record = build_milestone_11_local_diagnostic_fixture_harness()
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


def test_task_5_validation_and_pipeline_pass():
    record = build_milestone_11_local_diagnostic_fixture_harness()
    validation = validate_milestone_11_local_diagnostic_fixture_harness(record)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_11_local_diagnostic_fixture_harness_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["task_status"] == STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["task_5_ready"] is True
    assert payload["harness_pass_count"] == 10
    assert payload["harness_failure_count"] == 0


def test_task_5_markdown_and_manifest_contain_markers():
    record = build_milestone_11_local_diagnostic_fixture_harness()
    markdown = render_task_5_markdown(record)
    manifest = render_task_5_manifest(record)
    assert "ARC_AGI3_MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_TASK_5_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_FIXTURE_SCHEMA_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_DIAGNOSTIC_RESULT_GUARD_ACTIVE=true" in markdown
    assert "ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false" in markdown
    assert "ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "FIXTURE_SCHEMA" in manifest
    assert "LOCAL_DIAGNOSTIC_FIXTURES" in manifest
    assert "EPISODE_RESULTS" in manifest
    assert "TRACE_RECORDS" in manifest
    assert "HARNESS_VALIDATION_RESULTS" in manifest


def test_task_5_writes_artifacts(tmp_path: Path):
    record = build_milestone_11_local_diagnostic_fixture_harness()
    paths = write_task_5_artifacts(record, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["schema_path"]).exists()
    assert Path(paths["fixtures_path"]).exists()
    assert Path(paths["episodes_path"]).exists()
    assert Path(paths["traces_path"]).exists()
    assert Path(paths["guard_path"]).exists()
    assert "MILESTONE_11_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_11_TASK_5_READY=true" in Path(paths["markdown_path"]).read_text(
        encoding="utf-8"
    )
    assert "NOT_A_KAGGLE_SCORE" in Path(paths["guard_path"]).read_text(encoding="utf-8")


def test_task_5_metadata_safe():
    metadata = build_milestone_11_local_diagnostic_fixture_harness()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_task_5_index_is_conservative():
    index = build_milestone_11_local_diagnostic_fixture_harness()["harness_index"]
    assert index["fixture_schema_created"] is True
    assert index["fixture_count"] == EXPECTED_FIXTURE_COUNT
    assert index["episode_count"] == EXPECTED_EPISODE_COUNT
    assert index["trace_record_count"] == EXPECTED_TRACE_RECORD_COUNT
    assert index["diagnostic_result_guard_active"] is True
    assert index["diagnostic_only"] is True
    assert index["official_score_claim_allowed"] is False
    assert index["synthetic_fixture_score_claim_allowed"] is False
    assert index["real_public_score_claimed"] is False
    assert index["private_score_claimed"] is False
    assert index["real_benchmark_score"] is None
    assert index["real_submission_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_active"] is True
