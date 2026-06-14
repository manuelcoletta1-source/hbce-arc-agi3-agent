from pathlib import Path

from hbce_arc_agi3.milestone_7_ranker_evidence_upgrade import (
    BASELINE_COMMIT,
    EXPECTED_AGGREGATE_MAX_SCORE,
    EXPECTED_CALIBRATION_RULE_COUNT,
    EXPECTED_EVIDENCE_CHANNEL_COUNT,
    EXPECTED_PROFILE_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SCORING_RULE_COUNT,
    EXPECTED_SOURCE_GENERATOR_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    RANKER_GATES,
    RANKER_ISSUES,
    RANKER_MODE,
    RANKER_SCOPE,
    RANKER_STATUS,
    RANKER_VERDICT,
    VALIDATION_STATUS,
    build_milestone_7_ranker_evidence_upgrade,
    render_ranker_evidence_upgrade_manifest,
    render_ranker_evidence_upgrade_markdown,
    run_milestone_7_ranker_evidence_upgrade_pipeline,
    validate_milestone_7_ranker_evidence_upgrade,
    write_ranker_evidence_upgrade_artifacts,
)


def test_ranker_evidence_upgrade_ready():
    ranker = build_milestone_7_ranker_evidence_upgrade()
    assert ranker["status"] == RANKER_STATUS
    assert ranker["baseline_commit"] == BASELINE_COMMIT
    assert ranker["ranker_mode"] == RANKER_MODE
    assert ranker["ranker_scope"] == RANKER_SCOPE
    assert ranker["ranker_verdict"] == RANKER_VERDICT
    assert ranker["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert ranker["profile_count"] == EXPECTED_PROFILE_COUNT
    assert ranker["source_generator_count"] == EXPECTED_SOURCE_GENERATOR_COUNT
    assert ranker["evidence_channel_count"] == EXPECTED_EVIDENCE_CHANNEL_COUNT
    assert ranker["scoring_rule_count"] == EXPECTED_SCORING_RULE_COUNT
    assert ranker["calibration_rule_count"] == EXPECTED_CALIBRATION_RULE_COUNT
    assert ranker["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert ranker["aggregate_max_score"] == EXPECTED_AGGREGATE_MAX_SCORE
    assert ranker["ranker_gate_count"] == len(RANKER_GATES)
    assert ranker["passed_gate_count"] == len(RANKER_GATES)
    assert ranker["ranker_issue_count"] == 0
    assert ranker["ranker_ready"] is True


def test_ranker_keeps_real_submission_blocked():
    ranker = build_milestone_7_ranker_evidence_upgrade()
    assert ranker["solver_improvement_required"] is True
    assert ranker["competitive_claim_absent"] is True
    assert ranker["manual_submission_allowed"] is False
    assert ranker["manual_upload_performed"] is False
    assert ranker["real_submission_allowed"] is False
    assert ranker["ready_for_real_kaggle_submission"] is False
    assert ranker["real_submission_created"] is False
    assert ranker["kaggle_submission_sent"] is False
    assert ranker["upload_performed"] is False
    assert ranker["kaggle_authentication_performed"] is False


def test_ranker_profiles_cover_required_families():
    profiles = build_milestone_7_ranker_evidence_upgrade()["ranker_profiles"]
    families = {item["family"] for item in profiles}
    assert families == {"color_mapping", "object_model", "shape_symmetry"}
    source_generators = {item["source_generator_profile_id"] for item in profiles}
    assert source_generators == {
        "candidate_generator_color_mapping_v1",
        "candidate_generator_object_model_v1",
        "candidate_generator_shape_symmetry_v1",
    }


def test_ranker_profiles_are_deterministic_and_bounded():
    profiles = build_milestone_7_ranker_evidence_upgrade()["ranker_profiles"]
    assert all(item["priority"] == "P0" for item in profiles)
    assert all(item["ranker_runtime_modified"] is False for item in profiles)
    assert all(item["ready_for_task_6"] is True for item in profiles)
    assert all(item["max_profile_score"] == 100 for item in profiles)
    assert sum(item["max_profile_score"] for item in profiles) == EXPECTED_AGGREGATE_MAX_SCORE


def test_ranker_profiles_are_actionable_and_measurable():
    profiles = build_milestone_7_ranker_evidence_upgrade()["ranker_profiles"]
    assert all(bool(item["source_branch"]) for item in profiles)
    assert all(bool(item["tie_breaker"]) for item in profiles)
    assert all(len(item["evidence_channels"]) > 0 for item in profiles)
    assert all(len(item["scoring_rules"]) > 0 for item in profiles)
    assert all(len(item["calibration_rules"]) > 0 for item in profiles)
    assert all(len(item["regression_guards"]) > 0 for item in profiles)
    assert sum(len(item["evidence_channels"]) for item in profiles) == EXPECTED_EVIDENCE_CHANNEL_COUNT
    assert sum(len(item["scoring_rules"]) for item in profiles) == EXPECTED_SCORING_RULE_COUNT
    assert sum(len(item["calibration_rules"]) for item in profiles) == EXPECTED_CALIBRATION_RULE_COUNT
    assert sum(len(item["regression_guards"]) for item in profiles) == EXPECTED_REGRESSION_GUARD_COUNT


def test_generator_source_is_ready_and_hashed():
    source = build_milestone_7_ranker_evidence_upgrade()["milestone_7_generator_source"]
    assert source["present"] is True
    assert source["ready"] is True
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"
    assert source["artifact_id"].startswith("MILESTONE-7-CANDIDATE-GENERATOR-")


def test_ranker_record_is_conservative():
    record = build_milestone_7_ranker_evidence_upgrade()["ranker_record"]
    assert record["ranker_ready"] is True
    assert record["ranker_locked"] is True
    assert record["generator_ready"] is True
    assert record["candidate_generator_profiles_ready"] is True
    assert record["evidence_channel_count"] == EXPECTED_EVIDENCE_CHANNEL_COUNT
    assert record["runtime_solver_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["external_api_dependency"] is False
    assert record["contains_api_keys"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False


def test_ranker_gates_pass():
    ranker = build_milestone_7_ranker_evidence_upgrade()
    assert [item["name"] for item in ranker["ranker_gates"]] == list(RANKER_GATES)
    assert all(item["passed"] is True for item in ranker["ranker_gates"])
    assert all(item["severity"] == "PASS" for item in ranker["ranker_gates"])


def test_ranker_issues_inactive():
    ranker = build_milestone_7_ranker_evidence_upgrade()
    assert [item["name"] for item in ranker["ranker_issues"]] == list(RANKER_ISSUES)
    assert all(item["active"] is False for item in ranker["ranker_issues"])


def test_ranker_boundary_intact():
    boundary = build_milestone_7_ranker_evidence_upgrade()["boundary"]
    assert boundary["public_safe"] is True
    assert boundary["deterministic"] is True
    assert boundary["local_only"] is True
    assert boundary["dry_run_only"] is True
    assert boundary["external_api_dependency"] is False
    assert boundary["contains_api_keys"] is False
    assert boundary["kaggle_submission_sent"] is False
    assert boundary["private_core_exposure"] is False
    assert boundary["legal_certification"] is False


def test_ranker_validation_passes():
    ranker = build_milestone_7_ranker_evidence_upgrade()
    validation = validate_milestone_7_ranker_evidence_upgrade(ranker)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())


def test_ranker_pipeline_ready():
    payload = run_milestone_7_ranker_evidence_upgrade_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["ranker_status"] == RANKER_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["ranker_mode"] == RANKER_MODE
    assert payload["ranker_verdict"] == RANKER_VERDICT
    assert payload["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert payload["profile_count"] == EXPECTED_PROFILE_COUNT
    assert payload["evidence_channel_count"] == EXPECTED_EVIDENCE_CHANNEL_COUNT
    assert payload["ranker_gate_count"] == len(RANKER_GATES)
    assert payload["passed_gate_count"] == len(RANKER_GATES)
    assert payload["ranker_issue_count"] == 0
    assert payload["ranker_ready"] is True
    assert payload["runtime_solver_modified"] is False
    assert payload["ranker_runtime_modified"] is False
    assert payload["kaggle_submission_sent"] is False


def test_ranker_markdown_contains_markers():
    markdown = render_ranker_evidence_upgrade_markdown(
        build_milestone_7_ranker_evidence_upgrade()
    )
    assert "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_7_RANKER_MODE=RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD" in markdown
    assert "ARC_AGI3_MILESTONE_7_EVIDENCE_CHANNEL_COUNT=12" in markdown
    assert "ARC_AGI3_MILESTONE_7_SCORING_RULE_COUNT=12" in markdown
    assert "ARC_AGI3_MILESTONE_7_AGGREGATE_MAX_SCORE=300" in markdown
    assert "ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_6_REGRESSION_BENCHMARK" in markdown
    assert "ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false" in markdown
    assert "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown


def test_ranker_manifest_contains_profiles():
    manifest = render_ranker_evidence_upgrade_manifest(
        build_milestone_7_ranker_evidence_upgrade()
    )
    assert "ARC AGI3 MILESTONE 7 RANKER EVIDENCE UPGRADE MANIFEST v1" in manifest
    assert "ranker_mode=RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD" in manifest
    assert "ranker_ready=True" in manifest
    assert "RANKER_PROFILES" in manifest
    assert "ranker_evidence_color_mapping_v1" in manifest
    assert "ranker_evidence_object_model_v1" in manifest
    assert "ranker_evidence_shape_symmetry_v1" in manifest
    assert "ranker_runtime_modified=False" in manifest
    assert "ready_for_task_6=True" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "upload_performed=False" in manifest


def test_ranker_writes_artifacts(tmp_path: Path):
    ranker = build_milestone_7_ranker_evidence_upgrade()
    paths = write_ranker_evidence_upgrade_artifacts(ranker, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_7_RANKER_EVIDENCE_UPGRADE_READY" in Path(paths["json_path"]).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_V1_READY=true" in Path(paths["markdown_path"]).read_text(encoding="utf-8")
    assert "RANKER_EVIDENCE_UPGRADE_READY_FOR_REGRESSION_BENCHMARK" in Path(paths["index_path"]).read_text(encoding="utf-8")
