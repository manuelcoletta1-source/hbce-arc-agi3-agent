from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_solver_patch_plan import (
    EXPECTED_PATCH_STEP_COUNT,
    EXPECTED_PATCH_TARGET_COUNT,
    EXPECTED_PLAN_CASE_COUNT,
    EXPECTED_PLAN_CHECK_COUNT,
    EXPECTED_PLAN_FAILURE_COUNT,
    EXPECTED_PLAN_PASS_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    PLAN_MODE,
    PLAN_SCOPE,
    PLAN_STATUS,
    PLAN_VERDICT,
    VALIDATION_STATUS,
    build_milestone_10_solver_patch_plan,
    build_solver_patch_plan_checks,
    build_solver_patch_plan_source_summary,
    build_solver_patch_plan_state,
    build_solver_patch_steps,
    evaluate_all_solver_patch_plan_cases,
    evaluate_solver_patch_plan_case,
    render_solver_patch_plan_manifest,
    render_solver_patch_plan_markdown,
    run_milestone_10_solver_patch_plan_pipeline,
    validate_milestone_10_solver_patch_plan,
    write_solver_patch_plan_artifacts,
)


def test_patch_plan_source_summary_reads_audit():
    summary = build_solver_patch_plan_source_summary()
    assert summary["audit_present"] is True
    assert summary["audit_status"] == "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY"
    assert summary["audit_id"].startswith("MILESTONE-10-ERROR-AUDIT-")
    assert summary["audit_ready"] is True
    assert summary["audit_locked"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_3_SOLVER_PATCH_PLAN_V1"
    assert summary["error_pattern_count"] == 6
    assert summary["solver_target_count"] == 6
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True
    assert Path(summary["candidate_source_path"]).exists()
    assert summary["candidate_id"].startswith("MILESTONE-8-SUBMISSION-REFRESH-")


def test_patch_steps_are_complete_and_local_only():
    steps = build_solver_patch_steps()
    assert len(steps) == EXPECTED_PATCH_STEP_COUNT
    assert len({step["source_pattern_id"] for step in steps}) == EXPECTED_PATCH_TARGET_COUNT
    assert all(step["source_pattern_present"] is True for step in steps)
    assert all(step["local_only"] is True for step in steps)
    assert all(step["requires_external_api"] is False for step in steps)
    assert all(step["requires_kaggle_upload"] is False for step in steps)
    assert all(step["creates_submission_candidate"] is False for step in steps)
    assert all(step["runtime_modification_allowed_now"] is False for step in steps)
    assert all(step["ready_for_implementation"] is True for step in steps)


def test_patch_plan_state_blocks_runtime_modification_now():
    state = build_solver_patch_plan_state()
    assert state["solver_patch_plan_required"] is True
    assert state["solver_patch_plan_created"] is True
    assert state["solver_patch_plan_ready"] is True
    assert state["solver_patch_plan_locked"] is True
    assert state["plan_mode"] == PLAN_MODE
    assert state["plan_scope"] == PLAN_SCOPE
    assert state["plan_verdict"] == PLAN_VERDICT
    assert state["runtime_modification_allowed_now"] is False
    assert state["submission_candidate_created"] is False
    assert state["implementation_required_next"] is True
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_patch_plan_checks_all_pass():
    checks = build_solver_patch_plan_checks()
    assert all(checks.values())


def test_each_patch_plan_case_passes():
    case_ids = [
        "m10_patch_plan_audit_source_ready_v1",
        "m10_patch_plan_patch_targets_complete_v1",
        "m10_patch_plan_color_remap_patch_v1",
        "m10_patch_plan_object_boundary_patch_v1",
        "m10_patch_plan_symmetry_patch_v1",
        "m10_patch_plan_composition_patch_v1",
        "m10_patch_plan_ranker_patch_v1",
        "m10_patch_plan_traceability_patch_v1",
        "m10_patch_plan_fail_closed_preserved_v1",
        "m10_patch_plan_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_solver_patch_plan_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_patch_plan_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_solver_patch_plan_case("missing_patch_plan_case")


def test_all_patch_plan_cases_pass():
    results = evaluate_all_solver_patch_plan_cases()
    assert len(results) == EXPECTED_PLAN_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_solver_patch_plan_record_ready():
    plan = build_milestone_10_solver_patch_plan()
    assert plan["status"] == PLAN_STATUS
    assert plan["plan_mode"] == PLAN_MODE
    assert plan["plan_scope"] == PLAN_SCOPE
    assert plan["plan_verdict"] == PLAN_VERDICT
    assert plan["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert plan["plan_ready"] is True
    assert plan["plan_locked"] is True
    assert plan["solver_patch_plan_created"] is True
    assert plan["solver_patch_plan_ready"] is True
    assert plan["solver_patch_plan_locked"] is True
    assert plan["patch_target_count"] == EXPECTED_PATCH_TARGET_COUNT
    assert plan["patch_step_count"] == EXPECTED_PATCH_STEP_COUNT
    assert plan["plan_check_count"] == EXPECTED_PLAN_CHECK_COUNT
    assert plan["plan_case_count"] == EXPECTED_PLAN_CASE_COUNT
    assert plan["plan_pass_count"] == EXPECTED_PLAN_PASS_COUNT
    assert plan["plan_failure_count"] == EXPECTED_PLAN_FAILURE_COUNT
    assert plan["passed_gate_count"] == plan["plan_gate_count"]
    assert plan["plan_issue_count"] == 0


def test_patch_plan_audit_source_is_hashed():
    source = build_milestone_10_solver_patch_plan()["audit_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_LOCAL_ERROR_PATTERN_AUDIT_V1_READY"
    assert source["audit_id"].startswith("MILESTONE-10-ERROR-AUDIT-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_patch_plan_keeps_real_submission_blocked():
    plan = build_milestone_10_solver_patch_plan()
    assert plan["runtime_modification_allowed_now"] is False
    assert plan["submission_candidate_created"] is False
    assert plan["implementation_required_next"] is True
    assert plan["real_submission_decision"] == "NOT_AUTHORIZED"
    assert plan["real_submission_allowed"] is False
    assert plan["manual_upload_allowed"] is False
    assert plan["kaggle_authentication_allowed"] is False
    assert plan["kaggle_submission_sent"] is False
    assert plan["fail_closed_required"] is True
    assert plan["fail_closed_active"] is True


def test_patch_plan_validation_and_pipeline_pass():
    plan = build_milestone_10_solver_patch_plan()
    validation = validate_milestone_10_solver_patch_plan(plan)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_solver_patch_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["plan_status"] == PLAN_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["plan_ready"] is True
    assert payload["plan_pass_count"] == 10
    assert payload["plan_failure_count"] == 0


def test_patch_plan_markdown_and_manifest_contain_markers():
    plan = build_milestone_10_solver_patch_plan()
    markdown = render_solver_patch_plan_markdown(plan)
    manifest = render_solver_patch_plan_manifest(plan)
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_PATCH_TARGET_COUNT=6" in markdown
    assert "ARC_AGI3_MILESTONE_10_RUNTIME_MODIFICATION_ALLOWED_NOW=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "PATCH_STEPS" in manifest
    assert "PLAN_RESULTS" in manifest
    assert "m10_patch_plan_patch_targets_complete_v1" in manifest


def test_patch_plan_writes_artifacts(tmp_path: Path):
    plan = build_milestone_10_solver_patch_plan()
    paths = write_solver_patch_plan_artifacts(plan, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_10_SOLVER_PATCH_PLAN_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_SOLVER_PATCH_PLAN_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "SOLVER_PATCH_PLAN_READY_FOR_LOCAL_IMPLEMENTATION" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_patch_plan_metadata_safe():
    metadata = build_milestone_10_solver_patch_plan()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_patch_plan_index_is_conservative():
    index = build_milestone_10_solver_patch_plan()["plan_index"]
    assert index["plan_ready"] is True
    assert index["solver_patch_plan_created"] is True
    assert index["solver_patch_plan_ready"] is True
    assert index["patch_target_count"] == EXPECTED_PATCH_TARGET_COUNT
    assert index["patch_step_count"] == EXPECTED_PATCH_STEP_COUNT
    assert index["runtime_modification_allowed_now"] is False
    assert index["submission_candidate_created"] is False
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_4_SOLVER_PATCH_IMPLEMENTATION_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["manual_upload_allowed"] is False
    assert index["kaggle_authentication_allowed"] is False
    assert index["kaggle_submission_sent"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
