from pathlib import Path

from hbce_arc_agi3.milestone_7_baseline_solver_failure_taxonomy import (
    BASELINE_COMMIT,
    EXPECTED_FAILURE_CLASS_COUNT,
    EXPECTED_TARGET_TASK_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    TAXONOMY_GATES,
    TAXONOMY_ISSUES,
    TAXONOMY_MODE,
    TAXONOMY_SCOPE,
    TAXONOMY_STATUS,
    TAXONOMY_VERDICT,
    VALIDATION_STATUS,
    build_milestone_7_baseline_solver_failure_taxonomy,
    render_baseline_solver_failure_taxonomy_manifest,
    render_baseline_solver_failure_taxonomy_markdown,
    run_milestone_7_baseline_solver_failure_taxonomy_pipeline,
    validate_milestone_7_baseline_solver_failure_taxonomy,
    write_baseline_solver_failure_taxonomy_artifacts,
)


def test_baseline_solver_failure_taxonomy_ready():
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    assert taxonomy["status"] == TAXONOMY_STATUS
    assert taxonomy["baseline_commit"] == BASELINE_COMMIT
    assert taxonomy["taxonomy_mode"] == TAXONOMY_MODE
    assert taxonomy["taxonomy_scope"] == TAXONOMY_SCOPE
    assert taxonomy["taxonomy_verdict"] == TAXONOMY_VERDICT
    assert taxonomy["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert taxonomy["failure_class_count"] == EXPECTED_FAILURE_CLASS_COUNT
    assert taxonomy["open_failure_count"] == EXPECTED_FAILURE_CLASS_COUNT
    assert taxonomy["closed_failure_count"] == 0
    assert taxonomy["priority_p0_count"] >= 4
    assert taxonomy["target_task_count"] == EXPECTED_TARGET_TASK_COUNT
    assert taxonomy["taxonomy_gate_count"] == len(TAXONOMY_GATES)
    assert taxonomy["passed_gate_count"] == len(TAXONOMY_GATES)
    assert taxonomy["taxonomy_issue_count"] == 0
    assert taxonomy["taxonomy_ready"] is True
    assert taxonomy["taxonomy_locked"] is True


def test_taxonomy_keeps_real_submission_blocked():
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    assert taxonomy["solver_improvement_required"] is True
    assert taxonomy["competitive_claim_absent"] is True
    assert taxonomy["manual_submission_allowed"] is False
    assert taxonomy["manual_upload_performed"] is False
    assert taxonomy["real_submission_allowed"] is False
    assert taxonomy["ready_for_real_kaggle_submission"] is False
    assert taxonomy["real_submission_created"] is False
    assert taxonomy["kaggle_submission_sent"] is False
    assert taxonomy["upload_performed"] is False
    assert taxonomy["kaggle_authentication_performed"] is False


def test_failure_classes_are_open_actionable_and_measurable():
    failure_classes = build_milestone_7_baseline_solver_failure_taxonomy()["failure_classes"]
    assert len(failure_classes) == EXPECTED_FAILURE_CLASS_COUNT
    assert all(item["open"] is True for item in failure_classes)
    assert all(item["closed"] is False for item in failure_classes)
    assert all(bool(item["family"]) for item in failure_classes)
    assert all(bool(item["symptom"]) for item in failure_classes)
    assert all(bool(item["probable_cause"]) for item in failure_classes)
    assert all(bool(item["target_task"]) for item in failure_classes)
    assert all(bool(item["improvement_target"]) for item in failure_classes)
    assert all(bool(item["measurement"]) for item in failure_classes)


def test_failure_classes_cover_required_families():
    failure_classes = build_milestone_7_baseline_solver_failure_taxonomy()["failure_classes"]
    families = {item["family"] for item in failure_classes}
    assert "color_mapping" in families
    assert "object_model" in families
    assert "shape_symmetry" in families
    assert "candidate_generation" in families
    assert "candidate_ranking" in families
    assert "regression_safety" in families
    assert "competitive_readiness" in families


def test_failure_classes_route_to_expected_tasks():
    failure_classes = build_milestone_7_baseline_solver_failure_taxonomy()["failure_classes"]
    targets = {item["target_task"] for item in failure_classes}
    assert "Task 3 Task-Family Solver Expansion v1" in targets
    assert "Task 4 Candidate Generator Improvement v1" in targets
    assert "Task 5 Ranker Evidence Upgrade v1" in targets
    assert "Task 6 Regression Benchmark v1" in targets


def test_plan_source_is_ready_and_hashed():
    source = build_milestone_7_baseline_solver_failure_taxonomy()["milestone_7_plan_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-COMPETITIVE-SOLVER-PLAN-")


def test_taxonomy_record_is_conservative():
    record = build_milestone_7_baseline_solver_failure_taxonomy()["taxonomy_record"]
    assert record["taxonomy_ready"] is True
    assert record["taxonomy_locked"] is True
    assert record["milestone_7_open"] is True
    assert record["plan_solver_improvement_required"] is True
    assert record["failure_class_count"] == EXPECTED_FAILURE_CLASS_COUNT
    assert record["closed_failure_count"] == 0
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_taxonomy_gates_pass():
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    assert [item["name"] for item in taxonomy["taxonomy_gates"]] == list(TAXONOMY_GATES)
    assert all(item["passed"] is True for item in taxonomy["taxonomy_gates"])
    assert all(item["severity"] == "PASS" for item in taxonomy["taxonomy_gates"])


def test_taxonomy_issues_inactive():
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    assert [item["name"] for item in taxonomy["taxonomy_issues"]] == list(TAXONOMY_ISSUES)
    assert all(item["active"] is False for item in taxonomy["taxonomy_issues"])


def test_taxonomy_boundary_intact():
    boundary = build_milestone_7_baseline_solver_failure_taxonomy()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_taxonomy_validation_passes():
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    validation = validate_milestone_7_baseline_solver_failure_taxonomy(taxonomy)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_taxonomy_pipeline_ready():
    payload = run_milestone_7_baseline_solver_failure_taxonomy_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["taxonomy_status"] == TAXONOMY_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["taxonomy_mode"] == TAXONOMY_MODE
    assert payload["taxonomy_verdict"] == TAXONOMY_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["failure_class_count"] == EXPECTED_FAILURE_CLASS_COUNT
    assert payload["open_failure_count"] == EXPECTED_FAILURE_CLASS_COUNT
    assert payload["closed_failure_count"] == 0
    assert payload["taxonomy_gate_count"] == len(TAXONOMY_GATES)
    assert payload["passed_gate_count"] == len(TAXONOMY_GATES)
    assert payload["taxonomy_issue_count"] == 0
    assert payload["taxonomy_ready"] is True
    assert payload["kaggle_submission_sent"] is False


def test_taxonomy_markdown_contains_markers():
    markdown = render_baseline_solver_failure_taxonomy_markdown(
        build_milestone_7_baseline_solver_failure_taxonomy()
    )
    assert "ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_TAXONOMY_MODE=BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_FAILURE_CLASS_COUNT=7" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_taxonomy_manifest_contains_failure_classes():
    manifest = render_baseline_solver_failure_taxonomy_manifest(
        build_milestone_7_baseline_solver_failure_taxonomy()
    )
    assert "ARC AGI3 MILESTONE 7 BASELINE SOLVER FAILURE TAXONOMY MANIFEST v1" in manifest
    assert "taxonomy_mode=BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD" in manifest
    assert "taxonomy_ready=True" in manifest
    assert "FAILURE_CLASSES" in manifest
    assert "color_transform_undercoverage" in manifest
    assert "object_segmentation_undercoverage" in manifest
    assert "spatial_symmetry_undercoverage" in manifest
    assert "candidate_generator_low_diversity" in manifest
    assert "ranker_evidence_weakness" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_taxonomy_writes_artifacts(tmp_path: Path):
    taxonomy = build_milestone_7_baseline_solver_failure_taxonomy()
    paths = write_baseline_solver_failure_taxonomy_artifacts(taxonomy, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "BASELINE_FAILURE_TAXONOMY_READY_SOLVER_IMPROVEMENT_REQUIRED" in Path(paths["index_path"]).read_text(encoding="utf-8")
