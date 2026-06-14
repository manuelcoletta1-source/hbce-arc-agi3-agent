from pathlib import Path

from hbce_arc_agi3.milestone_7_regression_benchmark import (
    BASELINE_COMMIT,
    BENCHMARK_GATES,
    BENCHMARK_ISSUES,
    BENCHMARK_MODE,
    BENCHMARK_SCOPE,
    BENCHMARK_STATUS,
    BENCHMARK_VERDICT,
    EXPECTED_BENCHMARK_CASE_COUNT,
    EXPECTED_EVIDENCE_CHECK_COUNT,
    EXPECTED_FAILURE_COUNT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_MEASUREMENT_COUNT,
    EXPECTED_PASS_COUNT,
    EXPECTED_RANKER_PROFILE_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_7_regression_benchmark,
    render_regression_benchmark_manifest,
    render_regression_benchmark_markdown,
    run_milestone_7_regression_benchmark_pipeline,
    validate_milestone_7_regression_benchmark,
    write_regression_benchmark_artifacts,
)


def test_regression_benchmark_ready():
    benchmark = build_milestone_7_regression_benchmark()
    assert benchmark["status"] == BENCHMARK_STATUS
    assert benchmark["baseline_commit"] == BASELINE_COMMIT
    assert benchmark["benchmark_mode"] == BENCHMARK_MODE
    assert benchmark["benchmark_scope"] == BENCHMARK_SCOPE
    assert benchmark["benchmark_verdict"] == BENCHMARK_VERDICT
    assert benchmark["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert benchmark["ranker_profile_count"] == EXPECTED_RANKER_PROFILE_COUNT
    assert benchmark["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert benchmark["family_count"] == EXPECTED_FAMILY_COUNT
    assert benchmark["evidence_check_count"] == EXPECTED_EVIDENCE_CHECK_COUNT
    assert benchmark["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert benchmark["measurement_count"] == EXPECTED_MEASUREMENT_COUNT
    assert benchmark["pass_count"] == EXPECTED_PASS_COUNT
    assert benchmark["failure_count"] == EXPECTED_FAILURE_COUNT
    assert benchmark["benchmark_gate_count"] == len(BENCHMARK_GATES)
    assert benchmark["passed_gate_count"] == len(BENCHMARK_GATES)
    assert benchmark["benchmark_issue_count"] == 0
    assert benchmark["benchmark_ready"] is True


def test_benchmark_keeps_real_submission_blocked():
    benchmark = build_milestone_7_regression_benchmark()
    assert benchmark["solver_improvement_required"] is True
    assert benchmark["competitive_claim_absent"] is True
    assert benchmark["manual_submission_allowed"] is False
    assert benchmark["manual_upload_performed"] is False
    assert benchmark["real_submission_allowed"] is False
    assert benchmark["ready_for_real_kaggle_submission"] is False
    assert benchmark["real_submission_created"] is False
    assert benchmark["kaggle_submission_sent"] is False
    assert benchmark["upload_performed"] is False
    assert benchmark["kaggle_authentication_performed"] is False


def test_benchmark_cases_cover_required_families():
    cases = build_milestone_7_regression_benchmark()["benchmark_cases"]
    families = {item["family"] for item in cases}
    assert families == {"color_mapping", "object_model", "shape_symmetry"}
    source_rankers = {item["source_ranker_profile_id"] for item in cases}
    assert source_rankers == {
        "ranker_evidence_color_mapping_v1",
        "ranker_evidence_object_model_v1",
        "ranker_evidence_shape_symmetry_v1",
    }


def test_benchmark_cases_are_deterministic_local_and_passed():
    cases = build_milestone_7_regression_benchmark()["benchmark_cases"]
    assert all(item["priority"] == "P0" for item in cases)
    assert all(item["deterministic"] is True for item in cases)
    assert all(item["local_only"] is True for item in cases)
    assert all(item["dry_run_only"] is True for item in cases)
    assert all(item["benchmark_passed"] is True for item in cases)
    assert all(item["competitive_score_claim"] is False for item in cases)
    assert all(item["ready_for_task_7"] is True for item in cases)


def test_benchmark_cases_are_actionable_and_measurable():
    cases = build_milestone_7_regression_benchmark()["benchmark_cases"]
    assert all(bool(item["case_type"]) for item in cases)
    assert all(bool(item["purpose"]) for item in cases)
    assert all(bool(item["measurement"]) for item in cases)
    assert all(len(item["evidence_checks"]) > 0 for item in cases)
    assert all(len(item["regression_guards"]) > 0 for item in cases)
    assert sum(len(item["evidence_checks"]) for item in cases) == EXPECTED_EVIDENCE_CHECK_COUNT
    assert sum(len(item["regression_guards"]) for item in cases) == EXPECTED_REGRESSION_GUARD_COUNT


def test_ranker_source_is_ready_and_hashed():
    source = build_milestone_7_regression_benchmark()["milestone_7_ranker_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-RANKER-EVIDENCE-")


def test_benchmark_record_is_conservative():
    record = build_milestone_7_regression_benchmark()["benchmark_record"]
    assert record["benchmark_ready"] is True
    assert record["benchmark_locked"] is True
    assert record["ranker_ready"] is True
    assert record["ranker_evidence_profiles_ready"] is True
    assert record["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["benchmark_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_benchmark_gates_pass():
    benchmark = build_milestone_7_regression_benchmark()
    assert [item["name"] for item in benchmark["benchmark_gates"]] == list(BENCHMARK_GATES)
    assert all(item["passed"] is True for item in benchmark["benchmark_gates"])
    assert all(item["severity"] == "PASS" for item in benchmark["benchmark_gates"])


def test_benchmark_issues_inactive():
    benchmark = build_milestone_7_regression_benchmark()
    assert [item["name"] for item in benchmark["benchmark_issues"]] == list(BENCHMARK_ISSUES)
    assert all(item["active"] is False for item in benchmark["benchmark_issues"])


def test_benchmark_boundary_intact():
    boundary = build_milestone_7_regression_benchmark()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_benchmark_validation_passes():
    benchmark = build_milestone_7_regression_benchmark()
    validation = validate_milestone_7_regression_benchmark(benchmark)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_benchmark_pipeline_ready():
    payload = run_milestone_7_regression_benchmark_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["benchmark_status"] == BENCHMARK_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["benchmark_mode"] == BENCHMARK_MODE
    assert payload["benchmark_verdict"] == BENCHMARK_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["ranker_profile_count"] == EXPECTED_RANKER_PROFILE_COUNT
    assert payload["benchmark_case_count"] == EXPECTED_BENCHMARK_CASE_COUNT
    assert payload["benchmark_gate_count"] == len(BENCHMARK_GATES)
    assert payload["passed_gate_count"] == len(BENCHMARK_GATES)
    assert payload["benchmark_issue_count"] == 0
    assert payload["benchmark_ready"] is True
    assert payload["runtime_solver_modified"] is False
    assert payload["benchmark_runtime_modified"] is False
    assert payload["kaggle_submission_sent"] is False


def test_benchmark_markdown_contains_markers():
    markdown = render_regression_benchmark_markdown(
        build_milestone_7_regression_benchmark()
    )
    assert "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_BENCHMARK_MODE=REGRESSION_BENCHMARK_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_BENCHMARK_CASE_COUNT=6" in markdown
    assert "ARC_AGI3_MILESTONE_7_EVIDENCE_CHECK_COUNT=24" in markdown
    assert "ARC_AGI3_MILESTONE_7_FAILURE_COUNT=0" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_benchmark_manifest_contains_cases():
    manifest = render_regression_benchmark_manifest(
        build_milestone_7_regression_benchmark()
    )
    assert "ARC AGI3 MILESTONE 7 REGRESSION BENCHMARK MANIFEST v1" in manifest
    assert "benchmark_mode=REGRESSION_BENCHMARK_ONLY_NO_UPLOAD" in manifest
    assert "benchmark_ready=True" in manifest
    assert "BENCHMARK_CASES" in manifest
    assert "regression_color_palette_stability_v1" in manifest
    assert "regression_object_component_count_v1" in manifest
    assert "regression_shape_axis_symmetry_v1" in manifest
    assert "benchmark_passed=True" in manifest
    assert "ready_for_task_7=True" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_benchmark_writes_artifacts(tmp_path: Path):
    benchmark = build_milestone_7_regression_benchmark()
    paths = write_regression_benchmark_artifacts(benchmark, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_REGRESSION_BENCHMARK_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "REGRESSION_BENCHMARK_READY_FOR_LOCAL_SCORE_IMPROVEMENT_REPORT" in Path(paths["index_path"]).read_text(encoding="utf-8")
