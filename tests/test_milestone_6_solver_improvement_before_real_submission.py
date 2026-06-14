from pathlib import Path

from hbce_arc_agi3.milestone_6_solver_improvement_before_real_submission import (
    BASELINE_COMMIT,
    EXPECTED_IMPROVEMENT_TARGET_COUNT,
    IMPROVEMENT_GATES,
    IMPROVEMENT_ISSUES,
    IMPROVEMENT_MODE,
    IMPROVEMENT_SCOPE,
    IMPROVEMENT_STATUS,
    IMPROVEMENT_VERDICT,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_solver_improvement_before_real_submission,
    render_solver_improvement_before_real_submission_manifest,
    render_solver_improvement_before_real_submission_markdown,
    run_milestone_6_solver_improvement_before_real_submission_pipeline,
    validate_milestone_6_solver_improvement_before_real_submission,
    write_solver_improvement_before_real_submission_artifacts,
)


def test_solver_improvement_before_real_submission_ready():
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    assert improvement["status"] == IMPROVEMENT_STATUS
    assert improvement["baseline_commit"] == BASELINE_COMMIT
    assert improvement["improvement_mode"] == IMPROVEMENT_MODE
    assert improvement["improvement_scope"] == IMPROVEMENT_SCOPE
    assert improvement["improvement_verdict"] == IMPROVEMENT_VERDICT
    assert improvement["improvement_target_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert improvement["required_target_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert improvement["priority_p0_count"] >= 2
    assert improvement["measurement_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert improvement["improvement_gate_count"] == len(IMPROVEMENT_GATES)
    assert improvement["passed_gate_count"] == len(IMPROVEMENT_GATES)
    assert improvement["improvement_issue_count"] == 0
    assert improvement["improvement_ready"] is True
    assert improvement["improvement_locked"] is True


def test_solver_improvement_keeps_submission_blocked():
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    assert improvement["solver_improvement_required"] is True
    assert improvement["solver_improvement_started"] is True
    assert improvement["solver_improvement_completed"] is False
    assert improvement["competitive_claim_absent"] is True
    assert improvement["manual_upload_required"] is True
    assert improvement["manual_execution_performed"] is False
    assert improvement["real_submission_allowed"] is False
    assert improvement["ready_for_real_kaggle_submission"] is False
    assert improvement["real_submission_created"] is False
    assert improvement["kaggle_submission_sent"] is False
    assert improvement["upload_performed"] is False
    assert improvement["kaggle_authentication_performed"] is False


def test_improvement_targets_are_required_and_measurable():
    targets = build_milestone_6_solver_improvement_before_real_submission()["improvement_targets"]
    assert len(targets) == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert all(item["required_before_submission"] is True for item in targets)
    assert all(bool(item["target"]) for item in targets)
    assert all(bool(item["priority"]) for item in targets)
    assert all(bool(item["reason"]) for item in targets)
    assert all(bool(item["measurement"]) for item in targets)
    assert sum(1 for item in targets if item["priority"] == "P0") >= 2


def test_final_audit_source_is_ready_and_hashed():
    source = build_milestone_6_solver_improvement_before_real_submission()["final_audit_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-6-SUBMISSION-CANDIDATE-AUDIT-")


def test_improvement_record_is_conservative():
    record = build_milestone_6_solver_improvement_before_real_submission()["improvement_record"]
    assert record["improvement_ready"] is True
    assert record["improvement_locked"] is True
    assert record["final_audit_ready"] is True
    assert record["final_audit_locked"] is True
    assert record["final_audit_solver_improvement_required"] is True
    assert record["solver_improvement_required"] is True
    assert record["solver_improvement_started"] is True
    assert record["solver_improvement_completed"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_improvement_gates_pass():
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    assert [item["name"] for item in improvement["improvement_gates"]] == list(IMPROVEMENT_GATES)
    assert all(item["passed"] is True for item in improvement["improvement_gates"])
    assert all(item["severity"] == "PASS" for item in improvement["improvement_gates"])


def test_improvement_issues_inactive():
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    assert [item["name"] for item in improvement["improvement_issues"]] == list(IMPROVEMENT_ISSUES)
    assert all(item["active"] is False for item in improvement["improvement_issues"])


def test_improvement_boundary_intact():
    boundary = build_milestone_6_solver_improvement_before_real_submission()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_improvement_validation_passes():
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    validation = validate_milestone_6_solver_improvement_before_real_submission(improvement)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_improvement_pipeline_ready():
    payload = run_milestone_6_solver_improvement_before_real_submission_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["improvement_status"] == IMPROVEMENT_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["improvement_mode"] == IMPROVEMENT_MODE
    assert payload["improvement_verdict"] == IMPROVEMENT_VERDICT
    assert payload["improvement_target_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert payload["required_target_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert payload["measurement_count"] == EXPECTED_IMPROVEMENT_TARGET_COUNT
    assert payload["improvement_gate_count"] == len(IMPROVEMENT_GATES)
    assert payload["passed_gate_count"] == len(IMPROVEMENT_GATES)
    assert payload["improvement_issue_count"] == 0
    assert payload["solver_improvement_completed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_improvement_markdown_contains_markers():
    markdown = render_solver_improvement_before_real_submission_markdown(
        build_milestone_6_solver_improvement_before_real_submission()
    )
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_IMPROVEMENT_MODE=SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_COMPLETED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_improvement_manifest_contains_targets_and_boundary():
    manifest = render_solver_improvement_before_real_submission_manifest(
        build_milestone_6_solver_improvement_before_real_submission()
    )
    assert "ARC AGI3 MILESTONE 6 SOLVER IMPROVEMENT BEFORE REAL SUBMISSION MANIFEST v1" in manifest
    assert "improvement_mode=SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_ONLY_NO_UPLOAD" in manifest
    assert "improvement_ready=True" in manifest
    assert "solver_improvement_required=True" in manifest
    assert "solver_improvement_completed=False" in manifest
    assert "IMPROVEMENT_TARGETS" in manifest
    assert "solver_candidate_quality" in manifest
    assert "candidate_ranker_discrimination" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_improvement_writes_artifacts(tmp_path: Path):
    improvement = build_milestone_6_solver_improvement_before_real_submission()
    paths = write_solver_improvement_before_real_submission_artifacts(improvement, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_BEFORE_REAL_SUBMISSION_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "SOLVER_IMPROVEMENT_REQUIRED_REAL_SUBMISSION_REMAINS_BLOCKED" in Path(paths["index_path"]).read_text(encoding="utf-8")
