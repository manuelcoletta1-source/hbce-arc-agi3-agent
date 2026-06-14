from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_solver_patch_implementation import (
    EXPECTED_IMPLEMENTATION_CASE_COUNT,
    EXPECTED_IMPLEMENTATION_CHECK_COUNT,
    EXPECTED_IMPLEMENTATION_FAILURE_COUNT,
    EXPECTED_IMPLEMENTATION_FUNCTION_COUNT,
    EXPECTED_IMPLEMENTATION_PASS_COUNT,
    EXPECTED_PATCH_TARGET_COUNT,
    IMPLEMENTATION_MODE,
    IMPLEMENTATION_SCOPE,
    IMPLEMENTATION_STATUS,
    IMPLEMENTATION_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_10_solver_patch_implementation,
    build_solver_patch_function_samples,
    build_solver_patch_implementation_catalog,
    build_solver_patch_implementation_checks,
    build_solver_patch_implementation_source_summary,
    build_solver_patch_implementation_state,
    build_trace_generalization_fields,
    compute_color_remap_stability_score,
    evaluate_all_solver_patch_implementation_cases,
    evaluate_solver_patch_implementation_case,
    extract_object_boundary_signature,
    rank_candidates_by_patch_evidence,
    rank_symmetry_axis_candidates,
    render_solver_patch_implementation_manifest,
    render_solver_patch_implementation_markdown,
    run_milestone_10_solver_patch_implementation_pipeline,
    score_composition_order,
    validate_milestone_10_solver_patch_implementation,
    write_solver_patch_implementation_artifacts,
)


def test_implementation_source_summary_reads_patch_plan():
    summary = build_solver_patch_implementation_source_summary()
    assert summary["plan_present"] is True
    assert summary["plan_status"] == "MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY"
    assert summary["plan_id"].startswith("MILESTONE-10-SOLVER-PATCH-PLAN-")
    assert summary["plan_ready"] is True
    assert summary["plan_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_4_SOLVER_PATCH_IMPLEMENTATION_V1"
    assert summary["patch_target_count"] == 6
    assert summary["patch_step_count"] == 6
    assert summary["implementation_required_next"] is True
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")


def test_implementation_catalog_is_complete_and_local_only():
    catalog = build_solver_patch_implementation_catalog()
    assert len(catalog) == EXPECTED_IMPLEMENTATION_FUNCTION_COUNT
    assert len({item["source_patch_id"] for item in catalog}) == EXPECTED_PATCH_TARGET_COUNT
    assert all(item["source_patch_present"] is True for item in catalog)
    assert all(item["implemented"] is True for item in catalog)
    assert all(item["local_only"] is True for item in catalog)
    assert all(item["requires_external_api"] is False for item in catalog)
    assert all(item["requires_kaggle_upload"] is False for item in catalog)
    assert all(item["creates_submission_candidate"] is False for item in catalog)
    assert all(item["runtime_integration_performed"] is False for item in catalog)
    assert all(item["ready_for_benchmark_refresh"] is True for item in catalog)


def test_patch_helper_functions_behave_deterministically():
    color = compute_color_remap_stability_score({1: 2, 3: 4}, unseen_color_count=1)
    assert color["score"] == 93
    assert color["stable"] is True

    boundary = extract_object_boundary_signature([[0, 0, 0], [0, 8, 8], [0, 0, 8]])
    assert boundary["bbox"] == {"min_row": 1, "max_row": 2, "min_col": 1, "max_col": 2}
    assert boundary["nonzero_count"] == 3

    symmetry = rank_symmetry_axis_candidates(
        [
            {"axis": "horizontal", "score": 90, "evidence_count": 2, "penalty": 1},
            {"axis": "vertical", "score": 90, "evidence_count": 3, "penalty": 1},
        ]
    )
    assert symmetry["best_axis"] == "vertical"

    composition = score_composition_order(["color_mapping", "object_model", "shape_symmetry"])
    assert composition["stable_order"] is True

    ranked = rank_candidates_by_patch_evidence(
        [
            {"candidate_id": "b", "score_hint": 0.9, "confidence": 0.7, "family_evidence": 2, "complexity": 3},
            {"candidate_id": "a", "score_hint": 0.9, "confidence": 0.8, "family_evidence": 2, "complexity": 3},
        ]
    )
    assert ranked["best_candidate_id"] == "a"

    trace = build_trace_generalization_fields(
        task_id="task-x",
        family="color_mapping",
        assumptions=("zero background", "foreground remap"),
    )
    assert trace["trace_ready"] is True
    assert trace["assumption_count"] == 2
    assert len(trace["generalization_trace_hash"]) == 64


def test_implementation_state_keeps_runtime_and_submission_blocked():
    state = build_solver_patch_implementation_state()
    assert state["solver_patch_implementation_required"] is True
    assert state["solver_patch_implementation_created"] is True
    assert state["solver_patch_implementation_ready"] is True
    assert state["solver_patch_implementation_locked"] is True
    assert state["implementation_mode"] == IMPLEMENTATION_MODE
    assert state["implementation_scope"] == IMPLEMENTATION_SCOPE
    assert state["implementation_verdict"] == IMPLEMENTATION_VERDICT
    assert state["runtime_helper_functions_created"] is True
    assert state["runtime_integration_performed"] is False
    assert state["solver_runtime_modified"] is False
    assert state["submission_candidate_created"] is False
    assert state["benchmark_required_next"] is True
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_implementation_samples_are_ready():
    samples = build_solver_patch_function_samples()
    assert samples["color_remap_sample"]["stable"] is True
    assert samples["object_boundary_sample"]["nonzero_count"] == 3
    assert samples["symmetry_axis_sample"]["best_axis"] == "vertical"
    assert samples["composition_order_sample"]["stable_order"] is True
    assert samples["ranker_sample"]["best_candidate_id"] == "candidate_a"
    assert samples["trace_sample"]["trace_ready"] is True


def test_solver_patch_implementation_checks_all_pass():
    checks = build_solver_patch_implementation_checks()
    assert all(checks.values())


def test_each_solver_patch_implementation_case_passes():
    case_ids = [
        "m10_patch_impl_plan_source_ready_v1",
        "m10_patch_impl_catalog_complete_v1",
        "m10_patch_impl_color_remap_ready_v1",
        "m10_patch_impl_object_boundary_ready_v1",
        "m10_patch_impl_symmetry_tiebreak_ready_v1",
        "m10_patch_impl_composition_scoring_ready_v1",
        "m10_patch_impl_ranker_tiebreak_ready_v1",
        "m10_patch_impl_trace_fields_ready_v1",
        "m10_patch_impl_fail_closed_preserved_v1",
        "m10_patch_impl_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_solver_patch_implementation_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_solver_patch_implementation_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_solver_patch_implementation_case("missing_solver_patch_implementation_case")


def test_all_solver_patch_implementation_cases_pass():
    results = evaluate_all_solver_patch_implementation_cases()
    assert len(results) == EXPECTED_IMPLEMENTATION_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_solver_patch_implementation_record_ready():
    implementation = build_milestone_10_solver_patch_implementation()
    assert implementation["status"] == IMPLEMENTATION_STATUS
    assert implementation["implementation_mode"] == IMPLEMENTATION_MODE
    assert implementation["implementation_scope"] == IMPLEMENTATION_SCOPE
    assert implementation["implementation_verdict"] == IMPLEMENTATION_VERDICT
    assert implementation["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert implementation["implementation_ready"] is True
    assert implementation["implementation_locked"] is True
    assert implementation["solver_patch_implementation_created"] is True
    assert implementation["solver_patch_implementation_ready"] is True
    assert implementation["solver_patch_implementation_locked"] is True
    assert implementation["implementation_function_count"] == EXPECTED_IMPLEMENTATION_FUNCTION_COUNT
    assert implementation["patch_target_count"] == EXPECTED_PATCH_TARGET_COUNT
    assert implementation["implementation_check_count"] == EXPECTED_IMPLEMENTATION_CHECK_COUNT
    assert implementation["implementation_case_count"] == EXPECTED_IMPLEMENTATION_CASE_COUNT
    assert implementation["implementation_pass_count"] == EXPECTED_IMPLEMENTATION_PASS_COUNT
    assert implementation["implementation_failure_count"] == EXPECTED_IMPLEMENTATION_FAILURE_COUNT
    assert implementation["passed_gate_count"] == implementation["implementation_gate_count"]
    assert implementation["implementation_issue_count"] == 0


def test_solver_patch_plan_source_is_hashed():
    source = build_milestone_10_solver_patch_implementation()["plan_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY"
    assert source["plan_id"].startswith("MILESTONE-10-SOLVER-PATCH-PLAN-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_solver_patch_implementation_keeps_submission_blocked():
    implementation = build_milestone_10_solver_patch_implementation()
    assert implementation["runtime_helper_functions_created"] is True
    assert implementation["runtime_integration_performed"] is False
    assert implementation["solver_runtime_modified"] is False
    assert implementation["submission_candidate_created"] is False
    assert implementation["benchmark_required_next"] is True
    assert implementation["real_submission_decision"] == "NOT_AUTHORIZED"
    assert implementation["real_submission_allowed"] is False
    assert implementation["manual_upload_allowed"] is False
    assert implementation["kaggle_authentication_allowed"] is False
    assert implementation["kaggle_submission_sent"] is False
    assert implementation["fail_closed_required"] is True
    assert implementation["fail_closed_active"] is True


def test_solver_patch_implementation_validation_and_pipeline_pass():
    implementation = build_milestone_10_solver_patch_implementation()
    validation = validate_milestone_10_solver_patch_implementation(implementation)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_solver_patch_implementation_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["implementation_status"] == IMPLEMENTATION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["implementation_ready"] is True
    assert payload["implementation_pass_count"] == 10
    assert payload["implementation_failure_count"] == 0


def test_solver_patch_implementation_markdown_and_manifest_contain_markers():
    implementation = build_milestone_10_solver_patch_implementation()
    markdown = render_solver_patch_implementation_markdown(implementation)
    manifest = render_solver_patch_implementation_manifest(implementation)
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_IMPLEMENTATION_FUNCTION_COUNT=6" in markdown
    assert "ARC_AGI3_MILESTONE_10_RUNTIME_HELPER_FUNCTIONS_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SOLVER_RUNTIME_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_BENCHMARK_REQUIRED_NEXT=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "IMPLEMENTATION_CATALOG" in manifest
    assert "IMPLEMENTATION_RESULTS" in manifest
    assert "m10_patch_impl_catalog_complete_v1" in manifest


def test_solver_patch_implementation_writes_artifacts(tmp_path: Path):
    implementation = build_milestone_10_solver_patch_implementation()
    paths = write_solver_patch_implementation_artifacts(implementation, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_IMPLEMENTATION_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "SOLVER_PATCH_IMPLEMENTATION_READY_FOR_LOCAL_BENCHMARK_REFRESH" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_solver_patch_implementation_metadata_safe():
    metadata = build_milestone_10_solver_patch_implementation()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_solver_patch_implementation_index_is_conservative():
    index = build_milestone_10_solver_patch_implementation()["implementation_index"]
    assert index["implementation_ready"] is True
    assert index["solver_patch_implementation_created"] is True
    assert index["solver_patch_implementation_ready"] is True
    assert index["implementation_function_count"] == EXPECTED_IMPLEMENTATION_FUNCTION_COUNT
    assert index["patch_target_count"] == EXPECTED_PATCH_TARGET_COUNT
    assert index["runtime_helper_functions_created"] is True
    assert index["runtime_integration_performed"] is False
    assert index["solver_runtime_modified"] is False
    assert index["submission_candidate_created"] is False
    assert index["benchmark_required_next"] is True
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_5_BENCHMARK_REFRESH_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
