from pathlib import Path

from hbce_arc_agi3.milestone_6_real_submission_readiness_closure import (
    BASELINE_COMMIT,
    CLOSURE_GATES,
    CLOSURE_ISSUES,
    CLOSURE_MODE,
    CLOSURE_SCOPE,
    CLOSURE_STATUS,
    CLOSURE_VERDICT,
    EXPECTED_CLOSED_TASK_COUNT,
    EXPECTED_CLOSURE_SOURCE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_6_real_submission_readiness_closure,
    render_real_submission_readiness_closure_manifest,
    render_real_submission_readiness_closure_markdown,
    run_milestone_6_real_submission_readiness_closure_pipeline,
    validate_milestone_6_real_submission_readiness_closure,
    write_real_submission_readiness_closure_artifacts,
)


def test_real_submission_readiness_closure_ready():
    closure = build_milestone_6_real_submission_readiness_closure()
    assert closure["status"] == CLOSURE_STATUS
    assert closure["baseline_commit"] == BASELINE_COMMIT
    assert closure["closure_mode"] == CLOSURE_MODE
    assert closure["closure_scope"] == CLOSURE_SCOPE
    assert closure["closure_verdict"] == CLOSURE_VERDICT
    assert closure["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert closure["closure_source_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert closure["ready_source_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert closure["source_hash_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert closure["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert closure["closure_gate_count"] == len(CLOSURE_GATES)
    assert closure["passed_gate_count"] == len(CLOSURE_GATES)
    assert closure["closure_issue_count"] == 0
    assert closure["closure_ready"] is True
    assert closure["closure_locked"] is True
    assert closure["milestone_closed"] is True


def test_closure_blocks_real_submission():
    closure = build_milestone_6_real_submission_readiness_closure()
    assert closure["package_prepared"] is True
    assert closure["package_frozen"] is True
    assert closure["integrity_verified"] is True
    assert closure["final_audit_passed"] is True
    assert closure["solver_improvement_required"] is True
    assert closure["solver_improvement_started"] is True
    assert closure["solver_improvement_completed"] is False
    assert closure["competitive_claim_absent"] is True
    assert closure["manual_upload_required"] is True
    assert closure["manual_execution_performed"] is False
    assert closure["real_submission_allowed"] is False
    assert closure["ready_for_real_kaggle_submission"] is False
    assert closure["real_submission_created"] is False
    assert closure["kaggle_submission_sent"] is False
    assert closure["upload_performed"] is False
    assert closure["kaggle_authentication_performed"] is False


def test_closure_sources_are_ready_and_hashed():
    sources = build_milestone_6_real_submission_readiness_closure()["closure_sources"]
    assert len(sources) == EXPECTED_CLOSURE_SOURCE_COUNT
    assert all(item["present"] is True for item in sources)
    assert all(item["ready"] is True for item in sources)
    assert all(item["sha256"] != "MISSING_HASH" for item in sources)
    assert all(item["sha256_16"] != "MISSING_HASH" for item in sources)


def test_closure_record_is_conservative():
    record = build_milestone_6_real_submission_readiness_closure()["closure_record"]
    assert record["closure_ready"] is True
    assert record["closure_locked"] is True
    assert record["milestone_closed"] is True
    assert record["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert record["package_prepared"] is True
    assert record["package_frozen"] is True
    assert record["integrity_verified"] is True
    assert record["final_audit_passed"] is True
    assert record["solver_improvement_required"] is True
    assert record["solver_improvement_started"] is True
    assert record["solver_improvement_completed"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_closure_gates_pass():
    closure = build_milestone_6_real_submission_readiness_closure()
    assert [item["name"] for item in closure["closure_gates"]] == list(CLOSURE_GATES)
    assert all(item["passed"] is True for item in closure["closure_gates"])
    assert all(item["severity"] == "PASS" for item in closure["closure_gates"])


def test_closure_issues_inactive():
    closure = build_milestone_6_real_submission_readiness_closure()
    assert [item["name"] for item in closure["closure_issues"]] == list(CLOSURE_ISSUES)
    assert all(item["active"] is False for item in closure["closure_issues"])


def test_closure_boundary_intact():
    boundary = build_milestone_6_real_submission_readiness_closure()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_closure_validation_passes():
    closure = build_milestone_6_real_submission_readiness_closure()
    validation = validate_milestone_6_real_submission_readiness_closure(closure)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_closure_pipeline_ready():
    payload = run_milestone_6_real_submission_readiness_closure_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["closure_status"] == CLOSURE_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["closure_mode"] == CLOSURE_MODE
    assert payload["closure_verdict"] == CLOSURE_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["closure_source_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert payload["ready_source_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert payload["source_hash_count"] == EXPECTED_CLOSURE_SOURCE_COUNT
    assert payload["closed_task_count"] == EXPECTED_CLOSED_TASK_COUNT
    assert payload["closure_gate_count"] == len(CLOSURE_GATES)
    assert payload["passed_gate_count"] == len(CLOSURE_GATES)
    assert payload["closure_issue_count"] == 0
    assert payload["closure_ready"] is True
    assert payload["milestone_closed"] is True
    assert payload["solver_improvement_completed"] is False
    assert payload["kaggle_submission_sent"] is False


def test_closure_markdown_contains_markers():
    markdown = render_real_submission_readiness_closure_markdown(
        build_milestone_6_real_submission_readiness_closure()
    )
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_CLOSURE_MODE=REAL_SUBMISSION_READINESS_CLOSURE_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_6_CLOSED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_CLOSED_TASK_COUNT=10" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_REQUIRED=true" in markdown
    assert "ARC_AGI3_MILESTONE_6_SOLVER_IMPROVEMENT_COMPLETED=false" in markdown
    assert "ARC_AGI3_MILESTONE_6_NEXT_STAGE=OPEN_MILESTONE_7_COMPETITIVE_SOLVER_IMPROVEMENT" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_closure_manifest_contains_sources_and_boundary():
    manifest = render_real_submission_readiness_closure_manifest(
        build_milestone_6_real_submission_readiness_closure()
    )
    assert "ARC AGI3 MILESTONE 6 REAL SUBMISSION READINESS CLOSURE MANIFEST v1" in manifest
    assert "closure_mode=REAL_SUBMISSION_READINESS_CLOSURE_ONLY_NO_UPLOAD" in manifest
    assert "closure_ready=True" in manifest
    assert "milestone_closed=True" in manifest
    assert "closed_task_count=10" in manifest
    assert "solver_improvement_required=True" in manifest
    assert "solver_improvement_completed=False" in manifest
    assert "CLOSURE_SOURCES" in manifest
    assert "solver_improvement_before_real_submission" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_closure_writes_artifacts(tmp_path: Path):
    closure = build_milestone_6_real_submission_readiness_closure()
    paths = write_real_submission_readiness_closure_artifacts(closure, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_6_REAL_SUBMISSION_READINESS_CLOSURE_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "MILESTONE_6_CLOSED_REAL_SUBMISSION_NOT_READY_SOLVER_IMPROVEMENT_REQUIRED" in Path(paths["index_path"]).read_text(encoding="utf-8")
