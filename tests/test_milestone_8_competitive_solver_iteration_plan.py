from pathlib import Path

from hbce_arc_agi3.milestone_8_competitive_solver_iteration_plan import (
    BASELINE_COMMIT,
    EXPECTED_AUDIT_GATE_COUNT,
    EXPECTED_AUDIT_ISSUE_COUNT,
    EXPECTED_BENCHMARK_TARGET_COUNT,
    EXPECTED_CONTROL_COUNT,
    EXPECTED_ITERATION_FAMILY_COUNT,
    EXPECTED_PLAN_SECTION_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SOLVER_ITERATION_COUNT,
    EXPECTED_TASK_QUEUE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    PLAN_GATES,
    PLAN_ISSUES,
    PLAN_MODE,
    PLAN_SCOPE,
    PLAN_STATUS,
    PLAN_VERDICT,
    VALIDATION_STATUS,
    build_milestone_8_competitive_solver_iteration_plan,
    render_competitive_solver_iteration_plan_manifest,
    render_competitive_solver_iteration_plan_markdown,
    run_milestone_8_competitive_solver_iteration_plan_pipeline,
    validate_milestone_8_competitive_solver_iteration_plan,
    write_competitive_solver_iteration_plan_artifacts,
)


def test_milestone_8_plan_ready():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    assert plan["status"] == PLAN_STATUS
    assert plan["baseline_commit"] == BASELINE_COMMIT
    assert plan["plan_mode"] == PLAN_MODE
    assert plan["plan_scope"] == PLAN_SCOPE
    assert plan["plan_verdict"] == PLAN_VERDICT
    assert plan["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert plan["audit_gate_count"] == EXPECTED_AUDIT_GATE_COUNT
    assert plan["audit_issue_count"] == EXPECTED_AUDIT_ISSUE_COUNT
    assert plan["audit_real_submission_readiness"] == "BLOCKED"
    assert plan["audit_real_submission_decision"] == "NOT_READY"
    assert plan["iteration_family_count"] == EXPECTED_ITERATION_FAMILY_COUNT
    assert plan["solver_iteration_count"] == EXPECTED_SOLVER_ITERATION_COUNT
    assert plan["benchmark_target_count"] == EXPECTED_BENCHMARK_TARGET_COUNT
    assert plan["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert plan["control_count"] == EXPECTED_CONTROL_COUNT
    assert plan["plan_section_count"] == EXPECTED_PLAN_SECTION_COUNT
    assert plan["task_queue_count"] == EXPECTED_TASK_QUEUE_COUNT
    assert plan["plan_gate_count"] == len(PLAN_GATES)
    assert plan["passed_gate_count"] == len(PLAN_GATES)
    assert plan["plan_issue_count"] == 0
    assert plan["plan_ready"] is True


def test_milestone_8_keeps_submission_blocked():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    assert plan["runtime_solver_iteration_required"] is True
    assert plan["real_submission_created"] is False
    assert plan["real_submission_allowed"] is False
    assert plan["ready_for_real_kaggle_submission"] is False
    assert plan["kaggle_submission_sent"] is False
    assert plan["upload_performed"] is False
    assert plan["kaggle_authentication_performed"] is False
    assert plan["score_claim_absent"] is True
    assert plan["public_leaderboard_claim_absent"] is True


def test_iteration_families_are_p0_and_ready():
    families = build_milestone_8_competitive_solver_iteration_plan()["iteration_families"]
    assert len(families) == EXPECTED_ITERATION_FAMILY_COUNT
    assert {item["source_family"] for item in families} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }
    assert all(item["priority"] == "P0" for item in families)
    assert all(item["ready_for_kernel_v2"] is True for item in families)


def test_solver_iterations_are_runtime_targets():
    iterations = build_milestone_8_competitive_solver_iteration_plan()["solver_iterations"]
    assert len(iterations) == EXPECTED_SOLVER_ITERATION_COUNT
    assert all(item["runtime_solver_target"] is True for item in iterations)
    assert {item["family"] for item in iterations} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_benchmark_targets_and_guards_present():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    assert len(plan["benchmark_targets"]) == EXPECTED_BENCHMARK_TARGET_COUNT
    assert len(plan["regression_guards"]) == EXPECTED_REGRESSION_GUARD_COUNT
    assert "benchmark_cross_family_ranker_signal_v2" in plan["benchmark_targets"]
    assert "guard_no_real_submission_side_effect_v2" in plan["regression_guards"]


def test_task_queue_points_to_kernel_v2():
    queue = build_milestone_8_competitive_solver_iteration_plan()["task_queue"]
    assert len(queue) == EXPECTED_TASK_QUEUE_COUNT
    assert queue[0]["task"] == "Milestone #8 Task 2"
    assert queue[0]["name"] == "Competitive Solver Kernel v2"
    assert all(item["commit_expected"] is True for item in queue)


def test_final_audit_source_is_present_and_hashed():
    source = build_milestone_8_competitive_solver_iteration_plan()["final_audit_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_7_FINAL_COMPETITIVE_READINESS_AUDIT_READY"
    assert source["audit_id"].startswith("MILESTONE-7-FINAL-READINESS-AUDIT-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_plan_record_is_conservative():
    record = build_milestone_8_competitive_solver_iteration_plan()["plan_record"]
    assert record["plan_ready"] is True
    assert record["plan_locked"] is True
    assert record["audit_real_submission_readiness"] == "BLOCKED"
    assert record["audit_real_submission_decision"] == "NOT_READY"
    assert record["runtime_solver_iteration_required"] is True
    assert record["real_submission_created"] is False
    assert record["real_submission_allowed"] is False
    assert record["upload_performed"] is False
    assert record["kaggle_authentication_performed"] is False
    assert record["external_api_dependency"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_plan_gates_pass():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    assert [item["name"] for item in plan["plan_gates"]] == list(PLAN_GATES)
    assert all(item["passed"] is True for item in plan["plan_gates"])
    assert all(item["severity"] == "PASS" for item in plan["plan_gates"])


def test_plan_issues_inactive():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    assert [item["name"] for item in plan["plan_issues"]] == list(PLAN_ISSUES)
    assert all(item["active"] is False for item in plan["plan_issues"])


def test_plan_boundary_intact():
    boundary = build_milestone_8_competitive_solver_iteration_plan()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_plan_validation_passes():
    plan = build_milestone_8_competitive_solver_iteration_plan()
    validation = validate_milestone_8_competitive_solver_iteration_plan(plan)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_plan_pipeline_ready():
    payload = run_milestone_8_competitive_solver_iteration_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["plan_status"] == PLAN_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["plan_mode"] == PLAN_MODE
    assert payload["plan_verdict"] == PLAN_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["iteration_family_count"] == EXPECTED_ITERATION_FAMILY_COUNT
    assert payload["solver_iteration_count"] == EXPECTED_SOLVER_ITERATION_COUNT
    assert payload["plan_gate_count"] == len(PLAN_GATES)
    assert payload["passed_gate_count"] == len(PLAN_GATES)
    assert payload["plan_issue_count"] == 0
    assert payload["runtime_solver_iteration_required"] is True
    assert payload["kaggle_submission_sent"] is False


def test_plan_markdown_contains_markers():
    markdown = render_competitive_solver_iteration_plan_markdown(
        build_milestone_8_competitive_solver_iteration_plan()
    )
    assert "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_PLAN_MODE=COMPETITIVE_SOLVER_ITERATION_PLAN_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_8_RUNTIME_SOLVER_ITERATION_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_2_COMPETITIVE_SOLVER_KERNEL_V2" in markdown
    assert "ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_plan_manifest_contains_families_iterations_and_queue():
    manifest = render_competitive_solver_iteration_plan_manifest(
        build_milestone_8_competitive_solver_iteration_plan()
    )
    assert "ARC AGI3 MILESTONE 8 COMPETITIVE SOLVER ITERATION PLAN MANIFEST v2" in manifest
    assert "plan_mode=COMPETITIVE_SOLVER_ITERATION_PLAN_ONLY_NO_UPLOAD" in manifest
    assert "ITERATION_FAMILIES" in manifest
    assert "SOLVER_ITERATIONS" in manifest
    assert "TASK_QUEUE" in manifest
    assert "milestone_8_cross_family_composition_solver_v2" in manifest
    assert "solver_v2_cross_family_ranker_signal" in manifest
    assert "Milestone #8 Task 2 name=Competitive Solver Kernel v2" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_plan_writes_artifacts(tmp_path: Path):
    plan = build_milestone_8_competitive_solver_iteration_plan()
    paths = write_competitive_solver_iteration_plan_artifacts(plan, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_8_COMPETITIVE_SOLVER_ITERATION_PLAN_V2_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "COMPETITIVE_SOLVER_ITERATION_PLAN_READY_FOR_SOLVER_KERNEL_V2" in Path(paths["index_path"]).read_text(encoding="utf-8")
