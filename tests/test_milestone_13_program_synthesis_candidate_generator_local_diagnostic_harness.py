from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_local_diagnostic_harness import (
    DIAGNOSTIC_FIXTURES,
    HARNESS_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    build_candidate_fixture_matrix,
    build_diagnostic_harness_report,
    build_fixture_features,
    build_local_diagnostic_harness_record,
    validate_local_diagnostic_harness_record,
    write_artifacts,
)


def _candidate(index: int, family: str):
    return {
        "candidate_id": f"CAND-{index:02d}",
        "candidate_signature": f"SIG-{index:02d}",
        "family": family,
        "deterministic": True,
        "local_only": True,
        "public_safe": True,
        "bounded": True,
        "runtime_wiring_required": False,
        "real_submission_candidate": False,
    }


def _sample_candidates():
    return [
        _candidate(1, "primitive_sequence_candidates"),
        _candidate(2, "object_transform_candidates"),
        _candidate(3, "color_rule_candidates"),
        _candidate(4, "symmetry_completion_candidates"),
        _candidate(5, "crop_pad_resize_candidates"),
        _candidate(6, "relation_graph_candidates"),
        _candidate(7, "composite_program_candidates"),
        _candidate(8, "primitive_sequence_candidates"),
        _candidate(9, "object_transform_candidates"),
        _candidate(10, "color_rule_candidates"),
        _candidate(11, "symmetry_completion_candidates"),
        _candidate(12, "composite_program_candidates"),
    ]


def test_local_diagnostic_harness_record_is_valid():
    record = build_local_diagnostic_harness_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["harness_verdict"] == HARNESS_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_review_passed"] is True
    assert record["source_implementation_passed"] is True
    assert record["local_diagnostic_harness_ready"] is True
    assert record["local_diagnostic_harness_valid"] is True
    assert record["local_diagnostic_harness_passed"] is True
    assert record["candidate_count"] == 12
    assert record["candidate_family_count"] == 7
    assert record["diagnostic_fixture_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 4
    assert record["blocking_issue_count"] == 0
    assert record["runtime_execution_performed"] is False
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_local_diagnostic_harness_record(record) == []


def test_fixture_features_are_public_safe_and_deterministic():
    fixture = DIAGNOSTIC_FIXTURES[0]
    features = build_fixture_features(fixture)

    assert features["fixture_id"] == "DIAG-FIXTURE-001"
    assert features["height"] == 2
    assert features["width"] == 2
    assert features["cell_count"] == 4
    assert features["public_safe"] is True


def test_candidate_fixture_matrix_matches_required_families():
    matrix = build_candidate_fixture_matrix(_sample_candidates(), DIAGNOSTIC_FIXTURES)

    assert len(matrix) == 4
    assert all(row["observation_passed"] is True for row in matrix)
    assert all(row["matching_candidate_count"] > 0 for row in matrix)
    assert all(row["runtime_execution_performed"] is False for row in matrix)
    assert all(row["real_evaluation_performed"] is False for row in matrix)


def test_diagnostic_harness_report_passes_for_good_records():
    review_record = {
        "implementation_review_passed": True,
        "local_diagnostic_harness_authorized": True,
    }
    implementation_record = {
        "controlled_candidate_generator_implementation_passed": True,
        "generated_candidates": _sample_candidates(),
    }

    report = build_diagnostic_harness_report(review_record, implementation_record)

    assert report["harness_passed"] is True
    assert report["candidate_count"] == 12
    assert report["diagnostic_fixture_count"] == 4
    assert report["candidate_fixture_matrix_count"] == 4
    assert report["blocking_issue_count"] == 0
    assert report["recommended_next_stage"] == NEXT_STAGE


def test_diagnostic_harness_report_fails_if_family_missing():
    candidates = [candidate for candidate in _sample_candidates() if candidate["family"] != "color_rule_candidates"]
    review_record = {
        "implementation_review_passed": True,
        "local_diagnostic_harness_authorized": True,
    }
    implementation_record = {
        "controlled_candidate_generator_implementation_passed": True,
        "generated_candidates": candidates,
    }

    report = build_diagnostic_harness_report(review_record, implementation_record)

    assert report["harness_passed"] is False
    assert "candidate_count_12" in report["blocking_issues"]
    assert "all_fixture_observations_passed" in report["blocking_issues"]


def test_local_diagnostic_harness_fails_if_runtime_wiring_mutated():
    record = build_local_diagnostic_harness_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_local_diagnostic_harness_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_local_diagnostic_harness_artifacts_are_written(tmp_path: Path):
    record = build_local_diagnostic_harness_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-local-diagnostic-harness-v1.md" in written_files
