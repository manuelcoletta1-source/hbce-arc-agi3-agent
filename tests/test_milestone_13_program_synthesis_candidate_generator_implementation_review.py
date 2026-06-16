from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_implementation_review import (
    NEXT_STAGE,
    REVIEW_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_implementation_review_record,
    build_review_report,
    review_generated_candidates,
    validate_implementation_review_record,
    write_artifacts,
)


def _candidate(index: int, family: str):
    return {
        "candidate_id": f"CAND-{index:02d}",
        "candidate_signature": f"SIG-{index:02d}",
        "family": family,
        "program_depth": 2,
        "deterministic": True,
        "local_only": True,
        "public_safe": True,
        "bounded": True,
        "runtime_wiring_required": False,
        "runtime_solver_patch": False,
        "candidate_generator_runtime_wiring": False,
        "ranker_runtime_wiring": False,
        "real_submission_candidate": False,
        "kaggle_submission_payload": False,
    }


def _sample_candidates():
    families = [
        "primitive_sequence_candidates",
        "object_transform_candidates",
        "color_rule_candidates",
        "symmetry_completion_candidates",
        "crop_pad_resize_candidates",
        "relation_graph_candidates",
        "composite_program_candidates",
        "primitive_sequence_candidates",
        "object_transform_candidates",
        "color_rule_candidates",
        "symmetry_completion_candidates",
        "composite_program_candidates",
    ]
    return [_candidate(index + 1, family) for index, family in enumerate(families)]


def test_implementation_review_record_is_valid():
    record = build_implementation_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["review_verdict"] == REVIEW_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_ready"] is True
    assert record["source_shape_ok"] is True
    assert record["implementation_review_ready"] is True
    assert record["implementation_review_valid"] is True
    assert record["implementation_review_passed"] is True
    assert record["candidate_count"] == 12
    assert record["candidate_family_count"] == 7
    assert record["max_program_depth"] == 2
    assert record["blocking_issue_count"] == 0
    assert record["local_diagnostic_harness_authorized"] is True
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_implementation_review_record(record) == []


def test_review_generated_candidates_detects_good_candidate_set():
    review = review_generated_candidates(_sample_candidates())

    assert review["candidate_count"] == 12
    assert review["unique_candidate_ids"] is True
    assert review["unique_candidate_signatures"] is True
    assert review["candidate_family_count"] == 7
    assert review["missing_families"] == []
    assert review["unexpected_families"] == []
    assert review["max_program_depth"] == 2
    assert review["all_runtime_wiring_blocked"] is True
    assert review["all_real_submission_blocked"] is True


def test_review_report_passes_for_good_source_record():
    source_record = {
        "revision": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1",
        "task_verdict": "MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_READY",
        "implementation_verdict": "PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_READY_FOR_REVIEW",
        "next_stage": "MILESTONE_13_TASK_7_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_IMPLEMENTATION_REVIEW_V1",
        "generated_candidates": _sample_candidates(),
        "candidate_evidence_pack": {
            "candidate_count": 12,
            "max_program_depth": 2,
            "all_runtime_wiring_blocked": True,
            "all_real_submission_blocked": True,
        },
    }

    report = build_review_report(source_record)

    assert report["review_passed"] is True
    assert report["blocking_issue_count"] == 0
    assert report["recommended_next_stage"] == NEXT_STAGE


def test_review_report_fails_for_duplicate_candidate_ids():
    candidates = _sample_candidates()
    candidates[1]["candidate_id"] = candidates[0]["candidate_id"]
    source_record = {
        "generated_candidates": candidates,
        "candidate_evidence_pack": {
            "candidate_count": 12,
            "max_program_depth": 2,
            "all_runtime_wiring_blocked": True,
            "all_real_submission_blocked": True,
        },
    }

    report = build_review_report(source_record)

    assert report["review_passed"] is False
    assert "candidate_ids_unique" in report["blocking_issues"]


def test_implementation_review_fails_if_runtime_wiring_mutated():
    record = build_implementation_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_implementation_review_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_implementation_review_fails_if_candidate_count_mutated():
    record = build_implementation_review_record(baseline_commit="TEST-COMMIT")
    record["candidate_count"] = 11

    issues = validate_implementation_review_record(record)

    assert "CANDIDATE_COUNT_MISMATCH" in issues


def test_implementation_review_artifacts_are_written(tmp_path: Path):
    record = build_implementation_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-implementation-review-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-implementation-review-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-implementation-review-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-implementation-review-v1.md" in written_files
