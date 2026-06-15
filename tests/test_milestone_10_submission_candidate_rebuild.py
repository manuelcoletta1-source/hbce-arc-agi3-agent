from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_10_submission_candidate_rebuild import (
    EXPECTED_CANDIDATE_PACKAGE_ID,
    EXPECTED_REBUILD_CASE_COUNT,
    EXPECTED_REBUILD_CHECK_COUNT,
    EXPECTED_REBUILD_COMPONENT_COUNT,
    EXPECTED_REBUILD_FAILURE_COUNT,
    EXPECTED_REBUILD_PASS_COUNT,
    EXPECTED_SELECTED_CANDIDATE_ID,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    REBUILD_MODE,
    REBUILD_SCOPE,
    REBUILD_STATUS,
    REBUILD_VERDICT,
    VALIDATION_STATUS,
    build_milestone_10_submission_candidate_rebuild,
    build_rebuild_component_catalog,
    build_rebuild_state,
    build_rebuild_trace,
    build_rebuilt_candidate_payload,
    build_submission_candidate_rebuild_checks,
    build_submission_candidate_rebuild_source_summary,
    evaluate_all_submission_candidate_rebuild_cases,
    evaluate_submission_candidate_rebuild_case,
    render_submission_candidate_rebuild_manifest,
    render_submission_candidate_rebuild_markdown,
    run_milestone_10_submission_candidate_rebuild_pipeline,
    validate_milestone_10_submission_candidate_rebuild,
    write_submission_candidate_rebuild_artifacts,
)


def test_submission_candidate_rebuild_source_summary_reads_gate():
    summary = build_submission_candidate_rebuild_source_summary()
    assert summary["rebuild_gate_present"] is True
    assert summary["gate_status"] == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY"
    assert summary["rebuild_gate_id"].startswith("MILESTONE-10-REBUILD-GATE-")
    assert summary["rebuild_gate_ready"] is True
    assert summary["rebuild_gate_locked"] is True
    assert summary["rebuild_gate_passed"] is True
    assert summary["next_allowed_stage"] == "MILESTONE_10_TASK_8_SUBMISSION_CANDIDATE_REBUILD_V1"
    assert summary["local_candidate_rebuild_allowed"] is True
    assert summary["submission_candidate_rebuild_required_next"] is True
    assert summary["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert summary["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert summary["real_submission_candidate_created"] is False
    assert summary["submission_json_created"] is False
    assert summary["upload_package_created"] is False
    assert summary["real_submission_decision"] == "NOT_AUTHORIZED"
    assert summary["real_submission_allowed"] is False
    assert summary["fail_closed_active"] is True


def test_rebuild_component_catalog_is_safe_and_complete():
    components = build_rebuild_component_catalog()
    assert len(components) == EXPECTED_REBUILD_COMPONENT_COUNT
    assert all(component["required"] is True for component in components)
    assert all(component["ready"] is True for component in components)
    assert all(component["local_only"] is True for component in components)
    assert all(component["deterministic"] is True for component in components)
    assert all(component["requires_external_api"] is False for component in components)
    assert all(component["requires_kaggle_upload"] is False for component in components)
    assert all(component["creates_real_submission"] is False for component in components)
    assert all(component["creates_submission_json"] is False for component in components)
    assert all(component["creates_upload_package"] is False for component in components)


def test_rebuilt_candidate_payload_created_but_not_real_submission():
    payload = build_rebuilt_candidate_payload()
    assert payload["rebuilt_candidate_id"].startswith("MILESTONE-10-REBUILT-CANDIDATE-")
    assert payload["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert payload["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert payload["payload_kind"] == "LOCAL_REBUILT_CANDIDATE_PACKAGE"
    assert payload["local_candidate_package_rebuilt"] is True
    assert payload["rebuilt_candidate_payload_created"] is True
    assert payload["real_submission_candidate_created"] is False
    assert payload["submission_json_created"] is False
    assert payload["upload_package_created"] is False
    assert payload["ready_for_review"] is True


def test_rebuild_state_is_conservative():
    state = build_rebuild_state()
    assert state["submission_candidate_rebuild_required"] is True
    assert state["submission_candidate_rebuild_created"] is True
    assert state["submission_candidate_rebuild_ready"] is True
    assert state["submission_candidate_rebuild_locked"] is True
    assert state["rebuild_mode"] == REBUILD_MODE
    assert state["rebuild_scope"] == REBUILD_SCOPE
    assert state["rebuild_verdict"] == REBUILD_VERDICT
    assert state["local_candidate_package_rebuilt"] is True
    assert state["rebuilt_candidate_payload_created"] is True
    assert state["real_submission_candidate_created"] is False
    assert state["submission_json_created"] is False
    assert state["upload_package_created"] is False
    assert state["rebuilt_candidate_review_required_next"] is True
    assert state["real_submission_allowed"] is False
    assert state["fail_closed_active"] is True


def test_rebuild_trace_is_ready():
    trace = build_rebuild_trace()
    assert trace["trace_ready"] is True
    assert len(trace["trace_hash"]) == 64
    assert trace["trace_hash_16"]
    assert trace["boundary"] == "LOCAL_ONLY_NO_SUBMISSION"


def test_submission_candidate_rebuild_checks_all_pass():
    checks = build_submission_candidate_rebuild_checks()
    assert all(checks.values())


def test_each_submission_candidate_rebuild_case_passes():
    case_ids = [
        "m10_candidate_rebuild_gate_source_ready_v1",
        "m10_candidate_rebuild_selected_candidate_valid_v1",
        "m10_candidate_rebuild_package_rebuilt_v1",
        "m10_candidate_rebuild_components_ready_v1",
        "m10_candidate_rebuild_trace_ready_v1",
        "m10_candidate_rebuild_review_handoff_ready_v1",
        "m10_candidate_rebuild_no_submission_json_v1",
        "m10_candidate_rebuild_real_submission_blocked_v1",
        "m10_candidate_rebuild_fail_closed_preserved_v1",
        "m10_candidate_rebuild_next_stage_valid_v1",
    ]
    for case_id in case_ids:
        result = evaluate_submission_candidate_rebuild_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_submission_candidate_rebuild_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_submission_candidate_rebuild_case("missing_submission_candidate_rebuild_case")


def test_all_submission_candidate_rebuild_cases_pass():
    results = evaluate_all_submission_candidate_rebuild_cases()
    assert len(results) == EXPECTED_REBUILD_CASE_COUNT
    assert all(result["passed"] is True for result in results)


def test_submission_candidate_rebuild_record_ready():
    rebuild = build_milestone_10_submission_candidate_rebuild()
    assert rebuild["status"] == REBUILD_STATUS
    assert rebuild["rebuild_mode"] == REBUILD_MODE
    assert rebuild["rebuild_scope"] == REBUILD_SCOPE
    assert rebuild["rebuild_verdict"] == REBUILD_VERDICT
    assert rebuild["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert rebuild["submission_candidate_rebuild_ready"] is True
    assert rebuild["submission_candidate_rebuild_locked"] is True
    assert rebuild["submission_candidate_rebuild_created"] is True
    assert rebuild["local_candidate_package_rebuilt"] is True
    assert rebuild["rebuilt_candidate_payload_created"] is True
    assert rebuild["rebuilt_candidate_manifest_created"] is True
    assert rebuild["rebuilt_candidate_index_created"] is True
    assert rebuild["rebuilt_candidate_trace_created"] is True
    assert rebuild["review_handoff_created"] is True
    assert rebuild["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert rebuild["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert rebuild["rebuild_component_count"] == EXPECTED_REBUILD_COMPONENT_COUNT
    assert rebuild["rebuild_check_count"] == EXPECTED_REBUILD_CHECK_COUNT
    assert rebuild["rebuild_case_count"] == EXPECTED_REBUILD_CASE_COUNT
    assert rebuild["rebuild_pass_count"] == EXPECTED_REBUILD_PASS_COUNT
    assert rebuild["rebuild_failure_count"] == EXPECTED_REBUILD_FAILURE_COUNT
    assert rebuild["passed_gate_count"] == rebuild["rebuild_gate_count"]
    assert rebuild["rebuild_issue_count"] == 0


def test_rebuild_gate_source_is_hashed():
    source = build_milestone_10_submission_candidate_rebuild()["rebuild_gate_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_GATE_V1_READY"
    assert source["rebuild_gate_id"].startswith("MILESTONE-10-REBUILD-GATE-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_submission_candidate_rebuild_keeps_submission_blocked():
    rebuild = build_milestone_10_submission_candidate_rebuild()
    assert rebuild["local_candidate_package_rebuilt"] is True
    assert rebuild["rebuilt_candidate_review_required_next"] is True
    assert rebuild["real_submission_candidate_created"] is False
    assert rebuild["submission_json_created"] is False
    assert rebuild["upload_package_created"] is False
    assert rebuild["real_submission_decision"] == "NOT_AUTHORIZED"
    assert rebuild["real_submission_allowed"] is False
    assert rebuild["manual_upload_allowed"] is False
    assert rebuild["kaggle_authentication_allowed"] is False
    assert rebuild["kaggle_submission_sent"] is False
    assert rebuild["fail_closed_required"] is True
    assert rebuild["fail_closed_active"] is True


def test_submission_candidate_rebuild_validation_and_pipeline_pass():
    rebuild = build_milestone_10_submission_candidate_rebuild()
    validation = validate_milestone_10_submission_candidate_rebuild(rebuild)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_10_submission_candidate_rebuild_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["rebuild_status"] == REBUILD_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["submission_candidate_rebuild_ready"] is True
    assert payload["rebuild_pass_count"] == 10
    assert payload["rebuild_failure_count"] == 0


def test_submission_candidate_rebuild_markdown_and_manifest_contain_markers():
    rebuild = build_milestone_10_submission_candidate_rebuild()
    markdown = render_submission_candidate_rebuild_markdown(rebuild)
    manifest = render_submission_candidate_rebuild_manifest(rebuild)
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_LOCAL_CANDIDATE_PACKAGE_REBUILT=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REBUILT_CANDIDATE_PAYLOAD_CREATED=true" in markdown
    assert "ARC_AGI3_MILESTONE_10_REAL_SUBMISSION_CANDIDATE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_JSON_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_UPLOAD_PACKAGE_CREATED=false" in markdown
    assert "ARC_AGI3_MILESTONE_10_FAIL_CLOSED_ACTIVE=true" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "REBUILD_COMPONENTS" in manifest
    assert "REBUILD_VALIDATION_RESULTS" in manifest
    assert "m10_candidate_rebuild_package_rebuilt_v1" in manifest


def test_submission_candidate_rebuild_writes_artifacts(tmp_path: Path):
    rebuild = build_milestone_10_submission_candidate_rebuild()
    paths = write_submission_candidate_rebuild_artifacts(rebuild, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert Path(paths["payload_path"]).exists()
    assert "MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_V1_READY" in Path(
        paths["json_path"]
    ).read_text(encoding="utf-8")
    assert "ARC_AGI3_MILESTONE_10_SUBMISSION_CANDIDATE_REBUILD_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "SUBMISSION_CANDIDATE_REBUILD_READY_FOR_REBUILT_CANDIDATE_REVIEW_REAL_SUBMISSION_BLOCKED" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_submission_candidate_rebuild_metadata_safe():
    metadata = build_milestone_10_submission_candidate_rebuild()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False


def test_submission_candidate_rebuild_index_is_conservative():
    index = build_milestone_10_submission_candidate_rebuild()["rebuild_index"]
    assert index["submission_candidate_rebuild_ready"] is True
    assert index["submission_candidate_rebuild_created"] is True
    assert index["local_candidate_package_rebuilt"] is True
    assert index["rebuilt_candidate_payload_created"] is True
    assert index["selected_candidate_id"] == EXPECTED_SELECTED_CANDIDATE_ID
    assert index["candidate_package_id"] == EXPECTED_CANDIDATE_PACKAGE_ID
    assert index["rebuild_component_count"] == EXPECTED_REBUILD_COMPONENT_COUNT
    assert index["real_submission_candidate_created"] is False
    assert index["submission_json_created"] is False
    assert index["upload_package_created"] is False
    assert index["rebuilt_candidate_review_required_next"] is True
    assert index["next_allowed_stage"] == "MILESTONE_10_TASK_9_REBUILT_CANDIDATE_REVIEW_V1"
    assert index["real_submission_decision"] == "NOT_AUTHORIZED"
    assert index["real_submission_allowed"] is False
    assert index["fail_closed_required"] is True
    assert index["fail_closed_active"] is True
