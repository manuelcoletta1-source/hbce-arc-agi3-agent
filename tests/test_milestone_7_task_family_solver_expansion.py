from pathlib import Path

from hbce_arc_agi3.milestone_7_task_family_solver_expansion import (
    BASELINE_COMMIT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SOURCE_FAILURE_COUNT,
    EXPECTED_STRATEGY_COUNT,
    EXPANSION_GATES,
    EXPANSION_ISSUES,
    EXPANSION_MODE,
    EXPANSION_SCOPE,
    EXPANSION_STATUS,
    EXPANSION_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_7_task_family_solver_expansion,
    render_task_family_solver_expansion_manifest,
    render_task_family_solver_expansion_markdown,
    run_milestone_7_task_family_solver_expansion_pipeline,
    validate_milestone_7_task_family_solver_expansion,
    write_task_family_solver_expansion_artifacts,
)


def test_task_family_solver_expansion_ready():
    expansion = build_milestone_7_task_family_solver_expansion()
    assert expansion["status"] == EXPANSION_STATUS
    assert expansion["baseline_commit"] == BASELINE_COMMIT
    assert expansion["expansion_mode"] == EXPANSION_MODE
    assert expansion["expansion_scope"] == EXPANSION_SCOPE
    assert expansion["expansion_verdict"] == EXPANSION_VERDICT
    assert expansion["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert expansion["family_count"] == EXPECTED_FAMILY_COUNT
    assert expansion["source_failure_count"] == EXPECTED_SOURCE_FAILURE_COUNT
    assert expansion["strategy_count"] == EXPECTED_STRATEGY_COUNT
    assert expansion["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert expansion["expansion_gate_count"] == len(EXPANSION_GATES)
    assert expansion["passed_gate_count"] == len(EXPANSION_GATES)
    assert expansion["expansion_issue_count"] == 0
    assert expansion["expansion_ready"] is True
    assert expansion["expansion_locked"] is True


def test_expansion_keeps_real_submission_blocked():
    expansion = build_milestone_7_task_family_solver_expansion()
    assert expansion["solver_improvement_required"] is True
    assert expansion["competitive_claim_absent"] is True
    assert expansion["manual_submission_allowed"] is False
    assert expansion["manual_upload_performed"] is False
    assert expansion["real_submission_allowed"] is False
    assert expansion["ready_for_real_kaggle_submission"] is False
    assert expansion["real_submission_created"] is False
    assert expansion["kaggle_submission_sent"] is False
    assert expansion["upload_performed"] is False
    assert expansion["kaggle_authentication_performed"] is False


def test_family_expansions_cover_required_families():
    families = build_milestone_7_task_family_solver_expansion()["family_expansions"]
    family_names = {item["family"] for item in families}
    assert family_names == {"color_mapping", "object_model", "shape_symmetry"}
    source_failures = {item["source_failure_class"] for item in families}
    assert "color_transform_undercoverage" in source_failures
    assert "object_segmentation_undercoverage" in source_failures
    assert "spatial_symmetry_undercoverage" in source_failures


def test_family_expansions_are_registry_only_and_task_4_ready():
    families = build_milestone_7_task_family_solver_expansion()["family_expansions"]
    assert all(item["implemented_as_registry"] is True for item in families)
    assert all(item["runtime_solver_modified"] is False for item in families)
    assert all(item["ready_for_task_4"] is True for item in families)
    assert all(bool(item["solver_branch"]) for item in families)
    assert all(bool(item["output_candidate_type"]) for item in families)


def test_family_expansions_are_actionable_and_measurable():
    families = build_milestone_7_task_family_solver_expansion()["family_expansions"]
    assert all(bool(item["purpose"]) for item in families)
    assert all(bool(item["measurement"]) for item in families)
    assert all(len(item["strategies"]) > 0 for item in families)
    assert all(len(item["inputs_required"]) > 0 for item in families)
    assert all(len(item["regression_guards"]) > 0 for item in families)
    assert sum(len(item["strategies"]) for item in families) == EXPECTED_STRATEGY_COUNT
    assert sum(len(item["regression_guards"]) for item in families) == EXPECTED_REGRESSION_GUARD_COUNT


def test_taxonomy_source_is_ready_and_hashed():
    source = build_milestone_7_task_family_solver_expansion()["milestone_7_taxonomy_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-FAILURE-TAXONOMY-")


def test_expansion_record_is_conservative():
    record = build_milestone_7_task_family_solver_expansion()["expansion_record"]
    assert record["expansion_ready"] is True
    assert record["expansion_locked"] is True
    assert record["taxonomy_ready"] is True
    assert record["taxonomy_solver_improvement_required"] is True
    assert record["family_count"] == EXPECTED_FAMILY_COUNT
    assert record["strategy_count"] == EXPECTED_STRATEGY_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_expansion_gates_pass():
    expansion = build_milestone_7_task_family_solver_expansion()
    assert [item["name"] for item in expansion["expansion_gates"]] == list(EXPANSION_GATES)
    assert all(item["passed"] is True for item in expansion["expansion_gates"])
    assert all(item["severity"] == "PASS" for item in expansion["expansion_gates"])


def test_expansion_issues_inactive():
    expansion = build_milestone_7_task_family_solver_expansion()
    assert [item["name"] for item in expansion["expansion_issues"]] == list(EXPANSION_ISSUES)
    assert all(item["active"] is False for item in expansion["expansion_issues"])


def test_expansion_boundary_intact():
    boundary = build_milestone_7_task_family_solver_expansion()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_expansion_validation_passes():
    expansion = build_milestone_7_task_family_solver_expansion()
    validation = validate_milestone_7_task_family_solver_expansion(expansion)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_expansion_pipeline_ready():
    payload = run_milestone_7_task_family_solver_expansion_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["expansion_status"] == EXPANSION_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["expansion_mode"] == EXPANSION_MODE
    assert payload["expansion_verdict"] == EXPANSION_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["family_count"] == EXPECTED_FAMILY_COUNT
    assert payload["strategy_count"] == EXPECTED_STRATEGY_COUNT
    assert payload["expansion_gate_count"] == len(EXPANSION_GATES)
    assert payload["passed_gate_count"] == len(EXPANSION_GATES)
    assert payload["expansion_issue_count"] == 0
    assert payload["expansion_ready"] is True
    assert payload["runtime_solver_modified"] is False
    assert payload["kaggle_submission_sent"] is False


def test_expansion_markdown_contains_markers():
    markdown = render_task_family_solver_expansion_markdown(
        build_milestone_7_task_family_solver_expansion()
    )
    assert "ARC_AGI3_MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_EXPANSION_MODE=TASK_FAMILY_SOLVER_EXPANSION_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_FAMILY_COUNT=3" in markdown
    assert "ARC_AGI3_MILESTONE_7_STRATEGY_COUNT=10" in markdown
    assert "ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_expansion_manifest_contains_families():
    manifest = render_task_family_solver_expansion_manifest(
        build_milestone_7_task_family_solver_expansion()
    )
    assert "ARC AGI3 MILESTONE 7 TASK-FAMILY SOLVER EXPANSION MANIFEST v1" in manifest
    assert "expansion_mode=TASK_FAMILY_SOLVER_EXPANSION_ONLY_NO_UPLOAD" in manifest
    assert "expansion_ready=True" in manifest
    assert "FAMILY_EXPANSIONS" in manifest
    assert "color_mapping_family_v1" in manifest
    assert "object_model_family_v1" in manifest
    assert "shape_symmetry_family_v1" in manifest
    assert "runtime_solver_modified=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_expansion_writes_artifacts(tmp_path: Path):
    expansion = build_milestone_7_task_family_solver_expansion()
    paths = write_task_family_solver_expansion_artifacts(expansion, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_TASK_FAMILY_SOLVER_EXPANSION_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "TASK_FAMILY_SOLVER_EXPANSION_READY_FOR_CANDIDATE_GENERATOR_IMPROVEMENT" in Path(paths["index_path"]).read_text(encoding="utf-8")
