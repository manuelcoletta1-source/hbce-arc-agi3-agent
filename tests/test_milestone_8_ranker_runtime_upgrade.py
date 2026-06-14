from pathlib import Path

import pytest

from hbce_arc_agi3.milestone_8_candidate_generator_runtime_upgrade import (
    generate_runtime_upgraded_candidates,
)
from hbce_arc_agi3.milestone_8_ranker_runtime_upgrade import (
    EXPECTED_BOUNDARY_CONTROL_COUNT,
    EXPECTED_FAMILY_COUNT,
    EXPECTED_RANKER_CASE_COUNT,
    EXPECTED_RANKER_FAILURE_COUNT,
    EXPECTED_RANKER_OPERATION_COUNT,
    EXPECTED_RANKER_PASS_COUNT,
    EXPECTED_RANKER_POLICY_COUNT,
    EXPECTED_REGRESSION_GUARD_COUNT,
    EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT,
    NEXT_ALLOWED_STAGE,
    PIPELINE_STATUS,
    RANKER_GATES,
    RANKER_ISSUES,
    RANKER_MODE,
    RANKER_SCOPE,
    RANKER_STATUS,
    RANKER_VERDICT,
    VALIDATION_STATUS,
    build_milestone_8_ranker_runtime_upgrade,
    evaluate_all_ranker_runtime_cases,
    evaluate_ranker_runtime_case,
    rank_runtime_candidates,
    render_ranker_runtime_upgrade_manifest,
    render_ranker_runtime_upgrade_markdown,
    run_milestone_8_ranker_runtime_upgrade_pipeline,
    score_runtime_candidate,
    validate_milestone_8_ranker_runtime_upgrade,
    write_ranker_runtime_upgrade_artifacts,
)


def _candidates():
    return generate_runtime_upgraded_candidates([[0, 1, 0], [0, 1, 0], [0, 0, 0]])


def test_score_runtime_candidate_applies_family_hint():
    candidate = next(item for item in _candidates() if item["family"] == "object_model")
    without_hint = score_runtime_candidate(candidate)
    with_hint = score_runtime_candidate(candidate, task_family_hint="object_model")
    assert with_hint > without_hint


def test_ranker_color_hint_prioritizes_color_family():
    ranked = rank_runtime_candidates(_candidates(), task_family_hint="color_mapping")
    assert ranked[0]["family"] == "color_mapping"
    assert ranked[0]["ranker_policy_applied"] is True


def test_ranker_object_hint_prioritizes_object_family():
    ranked = rank_runtime_candidates(_candidates(), task_family_hint="object_model")
    assert ranked[0]["family"] == "object_model"
    assert ranked[0]["ranker_policy_applied"] is True


def test_ranker_shape_hint_prioritizes_shape_family():
    ranked = rank_runtime_candidates(_candidates(), task_family_hint="shape_symmetry")
    assert ranked[0]["family"] == "shape_symmetry"
    assert ranked[0]["ranker_policy_applied"] is True


def test_ranker_no_hint_orders_by_ranker_score():
    ranked = rank_runtime_candidates(_candidates())
    scores = [candidate["ranker_score"] for candidate in ranked]
    assert scores == sorted(scores, reverse=True)
    assert all(candidate["ranker_family_hint"] == "none" for candidate in ranked)


def test_ranker_deduplicates_by_signature():
    candidates = _candidates()
    ranked = rank_runtime_candidates(tuple(candidates) + tuple(candidates[:2]))
    signatures = [candidate["signature"] for candidate in ranked]
    assert len(signatures) == len(set(signatures))
    assert len(ranked) == len(rank_runtime_candidates(candidates))


def test_ranker_order_is_deterministic():
    first = rank_runtime_candidates(_candidates(), task_family_hint="object_model")
    second = rank_runtime_candidates(_candidates(), task_family_hint="object_model")
    assert first == second


def test_ranker_assigns_complete_fields():
    ranked = rank_runtime_candidates(_candidates())
    required = {
        "candidate_id",
        "family",
        "operation",
        "signature",
        "ranker_score",
        "ranker_rank",
        "ranker_family_hint",
        "ranker_ready",
        "ranker_runtime_upgrade",
    }
    assert all(required.issubset(set(candidate)) for candidate in ranked)
    assert [candidate["ranker_rank"] for candidate in ranked] == list(range(1, len(ranked) + 1))


def test_each_ranker_runtime_case_passes():
    case_ids = [
        "ranker_runtime_color_hint_top_candidate_v2",
        "ranker_runtime_object_hint_top_candidate_v2",
        "ranker_runtime_shape_hint_top_candidate_v2",
        "ranker_runtime_no_hint_score_order_v2",
        "ranker_runtime_deduplicate_candidates_v2",
        "ranker_runtime_deterministic_order_v2",
        "ranker_runtime_rank_fields_complete_v2",
        "ranker_runtime_boundary_guard_v2",
    ]
    for case_id in case_ids:
        result = evaluate_ranker_runtime_case(case_id)
        assert result["passed"] is True
        assert result["actual_status"] == "PASS"
        assert result["evidence_score"] == 100


def test_unknown_ranker_runtime_case_fails_closed():
    with pytest.raises(ValueError):
        evaluate_ranker_runtime_case("missing_ranker_case")


def test_all_ranker_runtime_cases_pass_and_cover_families():
    results = evaluate_all_ranker_runtime_cases()
    assert len(results) == EXPECTED_RANKER_CASE_COUNT
    assert all(result["passed"] is True for result in results)
    assert {result["family"] for result in results} == {
        "color_mapping",
        "object_model",
        "shape_symmetry",
        "cross_family_composition",
    }


def test_ranker_record_ready():
    ranker = build_milestone_8_ranker_runtime_upgrade()
    assert ranker["status"] == RANKER_STATUS
    assert ranker["ranker_mode"] == RANKER_MODE
    assert ranker["ranker_scope"] == RANKER_SCOPE
    assert ranker["ranker_verdict"] == RANKER_VERDICT
    assert ranker["next_allowed_stage"] == NEXT_ALLOWED_STAGE
    assert ranker["family_count"] == EXPECTED_FAMILY_COUNT
    assert ranker["ranker_policy_count"] == EXPECTED_RANKER_POLICY_COUNT
    assert ranker["ranker_operation_count"] == EXPECTED_RANKER_OPERATION_COUNT
    assert ranker["ranker_case_count"] == EXPECTED_RANKER_CASE_COUNT
    assert ranker["ranker_pass_count"] == EXPECTED_RANKER_PASS_COUNT
    assert ranker["ranker_failure_count"] == EXPECTED_RANKER_FAILURE_COUNT
    assert ranker["sample_ranked_candidate_count"] == EXPECTED_SAMPLE_RANKED_CANDIDATE_COUNT
    assert ranker["regression_guard_count"] == EXPECTED_REGRESSION_GUARD_COUNT
    assert ranker["boundary_control_count"] == EXPECTED_BOUNDARY_CONTROL_COUNT
    assert ranker["passed_gate_count"] == len(RANKER_GATES)
    assert ranker["ranker_issue_count"] == 0
    assert ranker["ranker_ready"] is True


def test_runtime_source_is_present_and_hashed():
    source = build_milestone_8_ranker_runtime_upgrade()["runtime_source"]
    assert source["present"] is True
    assert source["status"] == "MILESTONE_8_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2_READY"
    assert source["runtime_id"].startswith("MILESTONE-8-CANDIDATE-RUNTIME-")
    assert source["sha256"] != "MISSING_HASH"
    assert source["sha256_16"] != "MISSING_HASH"


def test_ranker_keeps_submission_blocked():
    ranker = build_milestone_8_ranker_runtime_upgrade()
    assert ranker["real_submission_created"] is False
    assert ranker["real_submission_allowed"] is False
    assert ranker["ready_for_real_kaggle_submission"] is False
    assert ranker["kaggle_submission_sent"] is False
    assert ranker["upload_performed"] is False
    assert ranker["kaggle_authentication_performed"] is False
    assert ranker["score_claim_absent"] is True
    assert ranker["public_leaderboard_claim_absent"] is True


def test_ranker_gates_and_issues_are_clean():
    ranker = build_milestone_8_ranker_runtime_upgrade()
    assert [item["name"] for item in ranker["ranker_gates"]] == list(RANKER_GATES)
    assert [item["name"] for item in ranker["ranker_issues"]] == list(RANKER_ISSUES)
    assert all(item["passed"] is True for item in ranker["ranker_gates"])
    assert all(item["active"] is False for item in ranker["ranker_issues"])


def test_ranker_validation_and_pipeline_pass():
    ranker = build_milestone_8_ranker_runtime_upgrade()
    validation = validate_milestone_8_ranker_runtime_upgrade(ranker)
    assert validation["status"] == VALIDATION_STATUS
    assert validation["valid"] is True
    assert all(validation["checks"].values())

    payload = run_milestone_8_ranker_runtime_upgrade_pipeline()
    assert payload["status"] == PIPELINE_STATUS
    assert payload["ranker_status"] == RANKER_STATUS
    assert payload["validation_status"] == VALIDATION_STATUS
    assert payload["ranker_ready"] is True
    assert payload["ranker_pass_count"] == 8
    assert payload["ranker_failure_count"] == 0


def test_ranker_markdown_and_manifest_contain_markers():
    ranker = build_milestone_8_ranker_runtime_upgrade()
    markdown = render_ranker_runtime_upgrade_markdown(ranker)
    manifest = render_ranker_runtime_upgrade_manifest(ranker)
    assert "ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_VALID=true" in markdown
    assert "ARC_AGI3_MILESTONE_8_RANKER_PASS_COUNT=8" in markdown
    assert "ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2" in markdown
    assert "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false" in markdown
    assert "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false" in markdown
    assert "ARC_AGI3_LEGAL_CERTIFICATION=false" in markdown
    assert "RANKER_RESULTS" in manifest
    assert "SAMPLE_RANKED_CANDIDATES" in manifest
    assert "ranker_runtime_object_hint_top_candidate_v2" in manifest
    assert "ranker_runtime_boundary_guard_v2" in manifest


def test_ranker_writes_artifacts(tmp_path: Path):
    ranker = build_milestone_8_ranker_runtime_upgrade()
    paths = write_ranker_runtime_upgrade_artifacts(ranker, output_dir=str(tmp_path))
    assert Path(paths["json_path"]).exists()
    assert Path(paths["markdown_path"]).exists()
    assert Path(paths["manifest_path"]).exists()
    assert Path(paths["index_path"]).exists()
    assert "MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY" in Path(paths["json_path"]).read_text(
        encoding="utf-8"
    )
    assert "ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY=true" in Path(
        paths["markdown_path"]
    ).read_text(encoding="utf-8")
    assert "RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK" in Path(
        paths["index_path"]
    ).read_text(encoding="utf-8")


def test_ranker_metadata_safe():
    metadata = build_milestone_8_ranker_runtime_upgrade()["metadata"]
    assert metadata["public_safe"] is True
    assert metadata["deterministic"] is True
    assert metadata["local_only"] is True
    assert metadata["dry_run_only"] is True
    assert metadata["external_api_dependency"] is False
    assert metadata["contains_api_keys"] is False
    assert metadata["kaggle_submission_sent"] is False
    assert metadata["private_core_exposure"] is False
    assert metadata["legal_certification"] is False
