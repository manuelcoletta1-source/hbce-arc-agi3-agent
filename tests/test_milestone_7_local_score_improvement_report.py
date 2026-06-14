from pathlib import Path

from hbce_arc_agi3.milestone_7_local_score_improvement_report import (
    BASELINE_COMMIT,
    EXPECTED_BENCHMARK_CASE_COUNT,
    EXPECTED_BLOCKING_CONTROL_COUNT,
    EXPECTED_FAMILY_REPORT_COUNT,
    EXPECTED_IMPROVEMENT_SIGNAL_COUNT,
    EXPECTED_LOCAL_MEASUREMENT_COUNT,
    EXPECTED_REGRESSION_FAILURE_COUNT,
    EXPECTED_REGRESSION_PASS_COUNT,
    EXPECTED_REPORT_SECTION_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REPORT_GATES,
    REPORT_ISSUES,
    REPORT_MODE,
    REPORT_SCOPE,
    REPORT_STATUS,
    REPORT_VERDICT,
    VALIDATION_STATUS,
    build_milestone_7_local_score_improvement_report,
    render_local_score_improvement_report_manifest,
    render_local_score_improvement_report_markdown,
    run_milestone_7_local_score_improvement_report_pipeline,
    validate_milestone_7_local_score_improvement_report,
    write_local_score_improvement_report_artifacts,
)


def test_local_score_report_ready():
    report = build_milestone_7_local_score_improvement_report()
    assert report["status"] == REPORT_STATUS
    assert report["baseline_commit"] == BASELINE_COMMIT
    assert report["report_mode"] == REPORT_MODE
    assert report["report_scope"] == REPORT_SCOPE
    assert report["report_verdict"] == REPORT_VERDICT
    assert report["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert report["family_report_count"] == EXPECTED_FAMILY_REPORT_COUNT
    assert report["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert report["local_measurement_count"] == EXPECTED_LOCAL_MEASUREMENT_COUNT
    assert report["improvement_signal_count"] == EXPECTED_IMPROVEMENT_SIGNAL_COUNT
    assert report["blocking_control_count"] == EXPECTED_BLOCKING_CONTROL_COUNT
    assert report["report_section_count"] == EXPECTED_REPORT_SECTION_COUNT
    assert report["regression_pass_count"] == EXPECTED_REGRESSION_PASS_COUNT
    assert report["regression_failure_count"] == EXPECTED_REGRESSION_FAILURE_COUNT
    assert report["report_gate_count"] == len(REPORT_GATES)
    assert report["passed_gate_count"] == len(REPORT_GATES)
    assert report["report_issue_count"] == 0
    assert report["report_ready"] is True


def test_report_keeps_real_submission_blocked():
    report = build_milestone_7_local_score_improvement_report()
    assert report["solver_improvement_required"] is True
    assert report["competitive_claim_absent"] is True
    assert report["manual_submission_allowed"] is False
    assert report["manual_upload_performed"] is False
    assert report["real_submission_allowed"] is False
    assert report["ready_for_real_kaggle_submission"] is False
    assert report["real_submission_created"] is False
    assert report["kaggle_submission_sent"] is False
    assert report["upload_performed"] is False
    assert report["kaggle_authentication_performed"] is False


def test_family_reports_cover_required_families():
    reports = build_milestone_7_local_score_improvement_report()["family_reports"]
    families = {item["family"] for item in reports}
    assert families == {"color_mapping", "object_model", "shape_symmetry"}
    assert all(item["priority"] == "P0" for item in reports)
    assert all(item["ready_for_task_8"] is True for item in reports)


def test_family_reports_have_no_score_claims():
    reports = build_milestone_7_local_score_improvement_report()["family_reports"]
    assert all(item["local_score_delta_claim"] == "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM" for item in reports)
    assert all(item["competitive_score_claim"] is False for item in reports)
    assert all(item["public_leaderboard_claim"] is False for item in reports)


def test_family_reports_are_actionable_and_measurable():
    reports = build_milestone_7_local_score_improvement_report()["family_reports"]
    assert all(bool(item["measurement_summary"]) for item in reports)
    assert all(len(item["source_cases"]) == 2 for item in reports)
    assert all(len(item["local_improvement_signals"]) == 3 for item in reports)
    assert sum(len(item["local_improvement_signals"]) for item in reports) == EXPECTED_IMPROVEMENT_SIGNAL_COUNT


def test_local_measurements_are_passed_and_non_competitive():
    measurements = build_milestone_7_local_score_improvement_report()["local_measurements"]
    assert len(measurements) == EXPECTED_LOCAL_MEASUREMENT_COUNT
    assert all(item["result"] == "PASS" for item in measurements)
    assert all(item["numeric_score_claim"] is False for item in measurements)
    assert {item["family"] for item in measurements} == {"color_mapping", "object_model", "shape_symmetry"}


def test_benchmark_source_is_ready_and_hashed():
    source = build_milestone_7_local_score_improvement_report()["milestone_7_benchmark_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-REGRESSION-BENCHMARK-")


def test_report_record_is_conservative():
    record = build_milestone_7_local_score_improvement_report()["report_record"]
    assert record["report_ready"] is True
    assert record["report_locked"] is True
    assert record["benchmark_ready"] is True
    assert record["regression_benchmark_records_ready"] is True
    assert record["local_score_claim_absent"] is True
    assert record["competitive_score_claim_absent"] is True
    assert record["public_leaderboard_claim_absent"] is True
    assert record["runtime_solver_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_report_gates_pass():
    report = build_milestone_7_local_score_improvement_report()
    assert [item["name"] for item in report["report_gates"]] == list(REPORT_GATES)
    assert all(item["passed"] is True for item in report["report_gates"])
    assert all(item["severity"] == "PASS" for item in report["report_gates"])


def test_report_issues_inactive():
    report = build_milestone_7_local_score_improvement_report()
    assert [item["name"] for item in report["report_issues"]] == list(REPORT_ISSUES)
    assert all(item["active"] is False for item in report["report_issues"])


def test_report_boundary_intact():
    boundary = build_milestone_7_local_score_improvement_report()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_report_validation_passes():
    report = build_milestone_7_local_score_improvement_report()
    validation = validate_milestone_7_local_score_improvement_report(report)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_report_pipeline_ready():
    payload = run_milestone_7_local_score_improvement_report_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["report_status"] == REPORT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["report_mode"] == REPORT_MODE
    assert payload["report_verdict"] == REPORT_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["family_report_count"] == EXPECTED_FAMILY_REPORT_COUNT
    assert payload["local_measurement_count"] == EXPECTED_LOCAL_MEASUREMENT_COUNT
    assert payload["report_gate_count"] == len(REPORT_GATES)
    assert payload["passed_gate_count"] == len(REPORT_GATES)
    assert payload["report_issue_count"] == 0
    assert payload["report_ready"] is True
    assert payload["local_score_claim_absent"] is True
    assert payload["kaggle_submission_sent"] is False


def test_report_markdown_contains_markers():
    markdown = render_local_score_improvement_report_markdown(
        build_milestone_7_local_score_improvement_report()
    )
    assert "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_REPORT_MODE=LOCAL_SCORE_IMPROVEMENT_REPORT_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_CLAIM_ABSENT=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_COMPETITIVE_SCORE_CLAIM_ABSENT=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_PUBLIC_LEADERBOARD_CLAIM_ABSENT=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_8_SUBMISSION_CANDIDATE_REBUILD" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_report_manifest_contains_reports_and_measurements():
    manifest = render_local_score_improvement_report_manifest(
        build_milestone_7_local_score_improvement_report()
    )
    assert "ARC AGI3 MILESTONE 7 LOCAL SCORE IMPROVEMENT REPORT MANIFEST v1" in manifest
    assert "report_mode=LOCAL_SCORE_IMPROVEMENT_REPORT_ONLY_NO_UPLOAD" in manifest
    assert "report_ready=True" in manifest
    assert "FAMILY_REPORTS" in manifest
    assert "LOCAL_MEASUREMENTS" in manifest
    assert "local_score_report_color_mapping_v1" in manifest
    assert "local_score_report_object_model_v1" in manifest
    assert "local_score_report_shape_symmetry_v1" in manifest
    assert "NO_NUMERIC_COMPETITIVE_SCORE_CLAIM" in manifest
    assert "numeric_score_claim=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_report_writes_artifacts(tmp_path: Path):
    report = build_milestone_7_local_score_improvement_report()
    paths = write_local_score_improvement_report_artifacts(report, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_LOCAL_SCORE_IMPROVEMENT_REPORT_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "LOCAL_SCORE_IMPROVEMENT_REPORT_READY_FOR_SUBMISSION_CANDIDATE_REBUILD" in Path(paths["index_path"]).read_text(encoding="utf-8")
