from pathlib import Path

from hbce_arc_agi3.milestone_7_candidate_generator_improvement import (
    BASELINE_COMMIT,
    EXPECTED_DETERMINISTIC_RULE_COUNT,
    EXPECTED_EVIDENCE_FIELD_COUNT,
    EXPECTED_MAX_CANDIDATE_COUNT,
    EXPECTED_PROFILE_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SOURCE_FAMILY_COUNT,
    EXPECTED_TEMPLATE_COUNT,
    GENERATOR_GATES,
    GENERATOR_ISSUES,
    GENERATOR_MODE,
    GENERATOR_SCOPE,
    GENERATOR_STATUS,
    GENERATOR_VERDICT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    VALIDATION_STATUS,
    build_milestone_7_candidate_generator_improvement,
    render_candidate_generator_improvement_manifest,
    render_candidate_generator_improvement_markdown,
    run_milestone_7_candidate_generator_improvement_pipeline,
    validate_milestone_7_candidate_generator_improvement,
    write_candidate_generator_improvement_artifacts,
)


def test_candidate_generator_improvement_ready():
    generator = build_milestone_7_candidate_generator_improvement()
    assert generator["status"] == GENERATOR_STATUS
    assert generator["baseline_commit"] == BASELINE_COMMIT
    assert generator["generator_mode"] == GENERATOR_MODE
    assert generator["generator_scope"] == GENERATOR_SCOPE
    assert generator["generator_verdict"] == GENERATOR_VERDICT
    assert generator["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert generator["profile_count"] == EXPECTED_PROFILE_COUNT
    assert generator["source_family_count"] == EXPECTED_SOURCE_FAMILY_COUNT
    assert generator["template_count"] == EXPECTED_TEMPLATE_COUNT
    assert generator["evidence_field_count"] == EXPECTED_EVIDENCE_FIELD_COUNT
    assert generator["deterministic_rule_count"] == EXPECTED_DETERMINISTIC_RULE_COUNT
    assert generator["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert generator["max_candidate_count"] == EXPECTED_MAX_CANDIDATE_COUNT
    assert generator["generator_gate_count"] == len(GENERATOR_GATES)
    assert generator["passed_gate_count"] == len(GENERATOR_GATES)
    assert generator["generator_issue_count"] == 0
    assert generator["generator_ready"] is True


def test_generator_keeps_real_submission_blocked():
    generator = build_milestone_7_candidate_generator_improvement()
    assert generator["solver_improvement_required"] is True
    assert generator["competitive_claim_absent"] is True
    assert generator["manual_submission_allowed"] is False
    assert generator["manual_upload_performed"] is False
    assert generator["real_submission_allowed"] is False
    assert generator["ready_for_real_kaggle_submission"] is False
    assert generator["real_submission_created"] is False
    assert generator["kaggle_submission_sent"] is False
    assert generator["upload_performed"] is False
    assert generator["kaggle_authentication_performed"] is False


def test_generator_profiles_cover_required_families():
    profiles = build_milestone_7_candidate_generator_improvement()["generator_profiles"]
    families = {item["family"] for item in profiles}
    assert families == {"color_mapping", "object_model", "shape_symmetry"}
    source_families = {item["source_family_id"] for item in profiles}
    assert source_families == {
        "color_mapping_family_v1",
        "object_model_family_v1",
        "shape_symmetry_family_v1",
    }


def test_generator_profiles_are_deterministic_and_bounded():
    profiles = build_milestone_7_candidate_generator_improvement()["generator_profiles"]
    assert all(item["priority"] == "P0" for item in profiles)
    assert all(item["random_search_allowed"] is False for item in profiles)
    assert all(item["unbounded_search_allowed"] is False for item in profiles)
    assert all(0 < item["max_candidate_count"] <= 8 for item in profiles)
    assert sum(item["max_candidate_count"] for item in profiles) == EXPECTED_MAX_CANDIDATE_COUNT


def test_generator_profiles_are_actionable_and_measurable():
    profiles = build_milestone_7_candidate_generator_improvement()["generator_profiles"]
    assert all(bool(item["generator_branch"]) for item in profiles)
    assert all(len(item["candidate_templates"]) > 0 for item in profiles)
    assert all(len(item["evidence_fields"]) > 0 for item in profiles)
    assert all(len(item["deterministic_rules"]) > 0 for item in profiles)
    assert all(len(item["regression_guards"]) > 0 for item in profiles)
    assert sum(len(item["candidate_templates"]) for item in profiles) == EXPECTED_TEMPLATE_COUNT
    assert sum(len(item["evidence_fields"]) for item in profiles) == EXPECTED_EVIDENCE_FIELD_COUNT
    assert sum(len(item["deterministic_rules"]) for item in profiles) == EXPECTED_DETERMINISTIC_RULE_COUNT
    assert sum(len(item["regression_guards"]) for item in profiles) == EXPECTED_REGRESSION_GUARD_COUNT


def test_expansion_source_is_ready_and_hashed():
    source = build_milestone_7_candidate_generator_improvement()["milestone_7_expansion_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-TASK-FAMILY-EXPANSION-")


def test_generator_record_is_conservative():
    record = build_milestone_7_candidate_generator_improvement()["generator_record"]
    assert record["generator_ready"] is True
    assert record["generator_locked"] is True
    assert record["expansion_ready"] is True
    assert record["solver_family_registry_ready"] is True
    assert record["template_count"] == EXPECTED_TEMPLATE_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_generator_gates_pass():
    generator = build_milestone_7_candidate_generator_improvement()
    assert [item["name"] for item in generator["generator_gates"]] == list(GENERATOR_GATES)
    assert all(item["passed"] is True for item in generator["generator_gates"])
    assert all(item["severity"] == "PASS" for item in generator["generator_gates"])


def test_generator_issues_inactive():
    generator = build_milestone_7_candidate_generator_improvement()
    assert [item["name"] for item in generator["generator_issues"]] == list(GENERATOR_ISSUES)
    assert all(item["active"] is False for item in generator["generator_issues"])


def test_generator_boundary_intact():
    boundary = build_milestone_7_candidate_generator_improvement()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_generator_validation_passes():
    generator = build_milestone_7_candidate_generator_improvement()
    validation = validate_milestone_7_candidate_generator_improvement(generator)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_generator_pipeline_ready():
    payload = run_milestone_7_candidate_generator_improvement_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["generator_status"] == GENERATOR_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["generator_mode"] == GENERATOR_MODE
    assert payload["generator_verdict"] == GENERATOR_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["profile_count"] == EXPECTED_PROFILE_COUNT
    assert payload["template_count"] == EXPECTED_TEMPLATE_COUNT
    assert payload["generator_gate_count"] == len(GENERATOR_GATES)
    assert payload["passed_gate_count"] == len(GENERATOR_GATES)
    assert payload["generator_issue_count"] == 0
    assert payload["generator_ready"] is True
    assert payload["runtime_solver_modified"] is False
    assert payload["kaggle_submission_sent"] is False


def test_generator_markdown_contains_markers():
    markdown = render_candidate_generator_improvement_markdown(
        build_milestone_7_candidate_generator_improvement()
    )
    assert "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_GENERATOR_MODE=CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_TEMPLATE_COUNT=12" in markdown
    assert "ARC_AGI3_MILESTONE_7_EVIDENCE_FIELD_COUNT=15" in markdown
    assert "ARC_AGI3_MILESTONE_7_MAX_CANDIDATE_COUNT=24" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_generator_manifest_contains_profiles():
    manifest = render_candidate_generator_improvement_manifest(
        build_milestone_7_candidate_generator_improvement()
    )
    assert "ARC AGI3 MILESTONE 7 CANDIDATE GENERATOR IMPROVEMENT MANIFEST v1" in manifest
    assert "generator_mode=CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD" in manifest
    assert "generator_ready=True" in manifest
    assert "GENERATOR_PROFILES" in manifest
    assert "candidate_generator_color_mapping_v1" in manifest
    assert "candidate_generator_object_model_v1" in manifest
    assert "candidate_generator_shape_symmetry_v1" in manifest
    assert "random_search_allowed=False" in manifest
    assert "unbounded_search_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_generator_writes_artifacts(tmp_path: Path):
    generator = build_milestone_7_candidate_generator_improvement()
    paths = write_candidate_generator_improvement_artifacts(generator, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "CANDIDATE_GENERATOR_IMPROVEMENT_READY_FOR_RANKER_EVIDENCE_UPGRADE" in Path(paths["index_path"]).read_text(encoding="utf-8")
