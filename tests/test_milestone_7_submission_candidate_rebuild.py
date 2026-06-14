from pathlib import Path

from hbce_arc_agi3.milestone_7_submission_candidate_rebuild import (
    BASELINE_COMMIT,
    EXPECTED_AUDIT_CHAIN_COUNT,
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_CANDIDATE_FILE_COUNT,
    EXPECTED_FAMILY_REPORT_COUNT,
    EXPECTED_LOCAL_MEASUREMENT_COUNT,
    EXPECTED_READINESS_CHECK_COUNT,
    EXPECTED_REBUILD_COMPONENT_COUNT,
    EXPECTED_REGRESSION_FAILURE_COUNT,
    EXPECTED_REGRESSION_PASS_COUNT,
    EXPECTED_SOURCE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REBUILD_GATES,
    REBUILD_ISSUES,
    REBUILD_MODE,
    REBUILD_SCOPE,
    REBUILD_STATUS,
    REBUILD_VERDICT,
    VALIDATION_STATUS,
    build_milestone_7_submission_candidate_rebuild,
    render_submission_candidate_rebuild_manifest,
    render_submission_candidate_rebuild_markdown,
    run_milestone_7_submission_candidate_rebuild_pipeline,
    validate_milestone_7_submission_candidate_rebuild,
    write_submission_candidate_rebuild_artifacts,
)


def test_submission_candidate_rebuild_ready():
    candidate = build_milestone_7_submission_candidate_rebuild()
    assert candidate["status"] == REBUILD_STATUS
    assert candidate["baseline_commit"] == BASELINE_COMMIT
    assert candidate["rebuild_mode"] == REBUILD_MODE
    assert candidate["rebuild_scope"] == REBUILD_SCOPE
    assert candidate["rebuild_verdict"] == REBUILD_VERDICT
    assert candidate["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert candidate["source_count"] == EXPECTED_SOURCE_COUNT
    assert candidate["rebuild_component_count"] == EXPECTED_REBUILD_COMPONENT_COUNT
    assert candidate["candidate_file_count"] == EXPECTED_CANDIDATE_FILE_COUNT
    assert candidate["readiness_check_count"] == EXPECTED_READINESS_CHECK_COUNT
    assert candidate["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert candidate["audit_chain_count"] == EXPECTED_AUDIT_CHAIN_COUNT
    assert candidate["family_report_count"] == EXPECTED_FAMILY_REPORT_COUNT
    assert candidate["local_measurement_count"] == EXPECTED_LOCAL_MEASUREMENT_COUNT
    assert candidate["regression_pass_count"] == EXPECTED_REGRESSION_PASS_COUNT
    assert candidate["regression_failure_count"] == EXPECTED_REGRESSION_FAILURE_COUNT
    assert candidate["rebuild_gate_count"] == len(REBUILD_GATES)
    assert candidate["passed_gate_count"] == len(REBUILD_GATES)
    assert candidate["rebuild_issue_count"] == 0
    assert candidate["rebuild_ready"] is True


def test_rebuild_keeps_real_submission_blocked():
    candidate = build_milestone_7_submission_candidate_rebuild()
    assert candidate["local_submission_candidate_created"] is True
    assert candidate["real_submission_created"] is False
    assert candidate["real_submission_allowed"] is False
    assert candidate["ready_for_real_kaggle_submission"] is False
    assert candidate["kaggle_submission_sent"] is False
    assert candidate["upload_performed"] is False
    assert candidate["kaggle_authentication_performed"] is False
    assert candidate["manual_submission_allowed"] is False
    assert candidate["manual_upload_performed"] is False


def test_source_artifacts_are_present_hashed_and_status_valid():
    sources = build_milestone_7_submission_candidate_rebuild()["source_artifacts"]
    assert len(sources) == EXPECTED_SOURCE_COUNT
    assert all(item["present"] is True for item in sources)
    assert all(item["status_valid"] is True for item in sources)
    assert all(item["sha256"] != "MISSING_HASH" for item in sources)
    assert all(item["sha256_16"] != "MISSING_HASH" for item in sources)


def test_rebuild_components_are_ready_and_not_runtime_modified():
    components = build_milestone_7_submission_candidate_rebuild()["rebuild_components"]
    assert len(components) == EXPECTED_REBUILD_COMPONENT_COUNT
    assert all(item["ready"] is True for item in components)
    assert all(item["runtime_modified"] is False for item in components)


def test_candidate_files_are_required():
    files = build_milestone_7_submission_candidate_rebuild()["candidate_files"]
    assert len(files) == EXPECTED_CANDIDATE_FILE_COUNT
    assert all(item["required"] is True for item in files)
    assert {item["filename"] for item in files} == {
        "milestone-7-submission-candidate-rebuild-v1.json",
        "milestone-7-submission-candidate-rebuild-v1.md",
        "milestone-7-submission-candidate-rebuild-manifest-v1.txt",
        "milestone-7-submission-candidate-rebuild-index-v1.json",
    }


def test_readiness_boundary_and_audit_chain_counts():
    candidate = build_milestone_7_submission_candidate_rebuild()
    assert len(candidate["readiness_checks"]) == EXPECTED_READINESS_CHECK_COUNT
    assert len(candidate["boundary_controls"]) == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert len(candidate["audit_chain"]) == EXPECTED_AUDIT_CHAIN_COUNT
    assert candidate["audit_chain"][-1]["commit"] == "bc41cd1"


def test_candidate_record_is_conservative():
    record = build_milestone_7_submission_candidate_rebuild()["rebuild_record"]
    assert record["rebuild_ready"] is True
    assert record["rebuild_locked"] is True
    assert record["local_submission_candidate_created"] is True
    assert record["real_submission_created"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["upload_performed"] is False
    assert record["kaggle_authentication_performed"] is False
    assert record["final_competitive_readiness_audit_required"] is True
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_rebuild_gates_pass():
    candidate = build_milestone_7_submission_candidate_rebuild()
    assert [item["name"] for item in candidate["rebuild_gates"]] == list(REBUILD_GATES)
    assert all(item["passed"] is True for item in candidate["rebuild_gates"])
    assert all(item["severity"] == "PASS" for item in candidate["rebuild_gates"])


def test_rebuild_issues_inactive():
    candidate = build_milestone_7_submission_candidate_rebuild()
    assert [item["name"] for item in candidate["rebuild_issues"]] == list(REBUILD_ISSUES)
    assert all(item["active"] is False for item in candidate["rebuild_issues"])


def test_rebuild_boundary_intact():
    boundary = build_milestone_7_submission_candidate_rebuild()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_rebuild_validation_passes():
    candidate = build_milestone_7_submission_candidate_rebuild()
    validation = validate_milestone_7_submission_candidate_rebuild(candidate)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_rebuild_pipeline_ready():
    payload = run_milestone_7_submission_candidate_rebuild_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["candidate_status"] == REBUILD_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["rebuild_mode"] == REBUILD_MODE
    assert payload["rebuild_verdict"] == REBUILD_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["source_count"] == EXPECTED_SOURCE_COUNT
    assert payload["candidate_file_count"] == EXPECTED_CANDIDATE_FILE_COUNT
    assert payload["rebuild_gate_count"] == len(REBUILD_GATES)
    assert payload["passed_gate_count"] == len(REBUILD_GATES)
    assert payload["rebuild_issue_count"] == 0
    assert payload["rebuild_ready"] is True
    assert payload["real_submission_created"] is False
    assert payload["kaggle_submission_sent"] is False


def test_rebuild_markdown_contains_markers():
    markdown = render_submission_candidate_rebuild_markdown(
        build_milestone_7_submission_candidate_rebuild()
    )
    assert "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_REBUILD_MODE=SUBMISSION_CANDIDATE_REBUILD_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_LOCAL_SUBMISSION_CANDIDATE_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_7_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_9_FINAL_COMPETITIVE_READINESS_AUDIT" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_rebuild_manifest_contains_sources_and_audit_chain():
    manifest = render_submission_candidate_rebuild_manifest(
        build_milestone_7_submission_candidate_rebuild()
    )
    assert "ARC AGI3 MILESTONE 7 SUBMISSION CANDIDATE REBUILD MANIFEST v1" in manifest
    assert "rebuild_mode=SUBMISSION_CANDIDATE_REBUILD_ONLY_NO_UPLOAD" in manifest
    assert "rebuild_ready=True" in manifest
    assert "SOURCE_ARTIFACTS" in manifest
    assert "AUDIT_CHAIN" in manifest
    assert "task_7_local_score_improvement_report" in manifest
    assert "commit=bc41cd1" in manifest
    assert "real_submission_created=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_rebuild_writes_artifacts(tmp_path: Path):
    candidate = build_milestone_7_submission_candidate_rebuild()
    paths = write_submission_candidate_rebuild_artifacts(candidate, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_SUBMISSION_CANDIDATE_REBUILD_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "SUBMISSION_CANDIDATE_REBUILD_READY_FOR_FINAL_COMPETITIVE_READINESS_AUDIT" in Path(paths["index_path"]).read_text(encoding="utf-8")


def test_rebuild_metadata_safe():
    metadata = build_milestone_7_submission_candidate_rebuild()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
