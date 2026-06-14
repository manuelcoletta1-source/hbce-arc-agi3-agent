from pathlib import Path

from hbce_arc_agi3.milestone_7_competitive_solver_improvement_plan import (
    BASELINE_COMMIT,
    EXPECTED_TASK_COUNT,
    EXPECTED_WORKSTREAM_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    PLAN_GATES,
    PLAN_ISSUES,
    PLAN_MODE,
    PLAN_SCOPE,
    PLAN_STATUS,
    PLAN_VERDICT,
    VALIDATION_STATUS,
    build_milestone_7_competitive_solver_improvement_plan,
    render_competitive_solver_improvement_plan_manifest,
    render_competitive_solver_improvement_plan_markdown,
    run_milestone_7_competitive_solver_improvement_plan_pipeline,
    validate_milestone_7_competitive_solver_improvement_plan,
    write_competitive_solver_improvement_plan_artifacts,
)


def test_competitive_solver_improvement_plan_ready():
    plan = build_milestone_7_competitive_solver_improvement_plan()
    assert plan["status"] == PLAN_STATUS
    assert plan["baseline_commit"] == BASELINE_COMMIT
    assert plan["plan_mode"] == PLAN_MODE
    assert plan["plan_scope"] == PLAN_SCOPE
    assert plan["plan_verdict"] == PLAN_VERDICT
    assert plan["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert plan["workstream_count"] == EXPECTED_WORKSTREAM_COUNT
    assert plan["required_workstream_count"] == EXPECTED_WORKSTREAM_COUNT
    assert plan["priority_p0_count"] >= 3
    assert plan["measurement_count"] == EXPECTED_WORKSTREAM_COUNT
    assert plan["task_count"] == EXPECTED_TASK_COUNT
    assert plan["plan_gate_count"] == len(PLAN_GATES)
    assert plan["passed_gate_count"] == len(PLAN_GATES)
    assert plan["plan_issue_count"] == 0
    assert plan["plan_ready"] is True
    assert plan["plan_locked"] is True
    assert plan["milestone_7_open"] is True


def test_plan_keeps_real_submission_blocked():
    plan = build_milestone_7_competitive_solver_improvement_plan()
    assert plan["solver_improvement_required"] is True
    assert plan["competitive_claim_absent"] is True
    assert plan["manual_submission_allowed"] is False
    assert plan["manual_upload_performed"] is False
    assert plan["real_submission_allowed"] is False
    assert plan["ready_for_real_kaggle_submission"] is False
    assert plan["real_submission_created"] is False
    assert plan["kaggle_submission_sent"] is False
    assert plan["upload_performed"] is False
    assert plan["kaggle_authentication_performed"] is False


def test_workstreams_are_required_and_measurable():
    workstreams = build_milestone_7_competitive_solver_improvement_plan()["workstreams"]
    assert len(workstreams) == EXPECTED_WORKSTREAM_COUNT
    assert all(item["required"] is True for item in workstreams)
    assert all(bool(item["name"]) for item in workstreams)
    assert all(bool(item["priority"]) for item in workstreams)
    assert all(bool(item["goal"]) for item in workstreams)
    assert all(bool(item["measurement"]) for item in workstreams)
    assert sum(1 for item in workstreams if item["priority"] == "P0") >= 3


def test_milestone_7_tasks_are_ordered():
    tasks = build_milestone_7_competitive_solver_improvement_plan()["milestone_7_tasks"]
    assert len(tasks) == EXPECTED_TASK_COUNT
    assert [item["task"] for item in tasks] == list(range(1, EXPECTED_TASK_COUNT + 1))
    assert tasks[0]["status"] == "CURRENT_TASK_READY"
    assert all(bool(item["name"]) for item in tasks)
    assert all(bool(item["output"]) for item in tasks)


def test_milestone_6_closure_source_is_ready_and_hashed():
    source = build_milestone_7_competitive_solver_improvement_plan()["milestone_6_closure_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-6-READINESS-CLOSURE-")


def test_plan_record_is_conservative():
    record = build_milestone_7_competitive_solver_improvement_plan()["plan_record"]
    assert record["plan_ready"] is True
    assert record["plan_locked"] is True
    assert record["milestone_7_open"] is True
    assert record["milestone_6_closed"] is True
    assert record["milestone_6_solver_improvement_required"] is True
    assert record["milestone_6_solver_improvement_completed"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_plan_gates_pass():
    plan = build_milestone_7_competitive_solver_improvement_plan()
    assert [item["name"] for item in plan["plan_gates"]] == list(PLAN_GATES)
    assert all(item["passed"] is True for item in plan["plan_gates"])
    assert all(item["severity"] == "PASS" for item in plan["plan_gates"])


def test_plan_issues_inactive():
    plan = build_milestone_7_competitive_solver_improvement_plan()
    assert [item["name"] for item in plan["plan_issues"]] == list(PLAN_ISSUES)
    assert all(item["active"] is False for item in plan["plan_issues"])


def test_plan_boundary_intact():
    boundary = build_milestone_7_competitive_solver_improvement_plan()["boundary"]
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
    plan = build_milestone_7_competitive_solver_improvement_plan()
    validation = validate_milestone_7_competitive_solver_improvement_plan(plan)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_plan_pipeline_ready():
    payload = run_milestone_7_competitive_solver_improvement_plan_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["plan_status"] == PLAN_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["plan_mode"] == PLAN_MODE
    assert payload["plan_verdict"] == PLAN_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["workstream_count"] == EXPECTED_WORKSTREAM_COUNT
    assert payload["task_count"] == EXPECTED_TASK_COUNT
    assert payload["plan_gate_count"] == len(PLAN_GATES)
    assert payload["passed_gate_count"] == len(PLAN_GATES)
    assert payload["plan_issue_count"] == 0
    assert payload["plan_ready"] is True
    assert payload["milestone_7_open"] is True
    assert payload["kaggle_submission_sent"] is False


def test_plan_markdown_contains_markers():
    markdown = render_competitive_solver_improvement_plan_markdown(
        build_milestone_7_competitive_solver_improvement_plan()
    )
    assert "ARC_AGI3_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_PLAN_MODE=COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_OPEN=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_TASK_COUNT=10" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_2_BASELINE_SOLVER_FAILURE_TAXONOMY" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_plan_manifest_contains_workstreams_and_tasks():
    manifest = render_competitive_solver_improvement_plan_manifest(
        build_milestone_7_competitive_solver_improvement_plan()
    )
    assert "ARC AGI3 MILESTONE 7 COMPETITIVE SOLVER IMPROVEMENT PLAN MANIFEST v1" in manifest
    assert "plan_mode=COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_ONLY_NO_UPLOAD" in manifest
    assert "plan_ready=True" in manifest
    assert "milestone_7_open=True" in manifest
    assert "WORKSTREAMS" in manifest
    assert "TASKS" in manifest
    assert "baseline_failure_taxonomy" in manifest
    assert "candidate_generator_improvement" in manifest
    assert "Task 2 Baseline Solver Failure Taxonomy v1" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_plan_writes_artifacts(tmp_path: Path):
    plan = build_milestone_7_competitive_solver_improvement_plan()
    paths = write_competitive_solver_improvement_plan_artifacts(plan, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT_PLAN_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "MILESTONE_7_OPEN_COMPETITIVE_SOLVER_IMPROVEMENT_REQUIRED" in Path(paths["index_path"]).read_text(encoding="utf-8")
