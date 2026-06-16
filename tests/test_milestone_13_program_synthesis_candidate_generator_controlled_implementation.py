from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_implementation import (
    NEXT_STAGE,
    TASK_NAME,
    TASK_VERDICT,
    IMPLEMENTATION_VERDICT,
    build_candidate_evidence_pack,
    build_controlled_candidate_generator_implementation,
    build_controlled_candidate_generator_record,
    generate_controlled_candidate_programs,
    validate_controlled_candidate_generator_record,
    write_artifacts,
)


def test_controlled_candidate_generator_record_is_valid():
    record = build_controlled_candidate_generator_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["implementation_verdict"] == IMPLEMENTATION_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_plan_ready"] is True
    assert record["source_plan_shape_ok"] is True
    assert record["controlled_candidate_generator_implementation_ready"] is True
    assert record["controlled_candidate_generator_implementation_valid"] is True
    assert record["candidate_template_count"] == 12
    assert record["candidate_family_count"] == 7
    assert record["parameter_binding_field_count"] == 8
    assert record["implementation_component_count"] == 6
    assert record["generated_candidate_count"] == 12
    assert record["max_program_depth"] == 2
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_controlled_candidate_generator_record(record) == []


def test_generate_controlled_candidate_programs_is_deterministic():
    first = generate_controlled_candidate_programs()
    second = generate_controlled_candidate_programs()

    assert first == second
    assert len(first) == 12
    assert len({candidate["candidate_id"] for candidate in first}) == 12


def test_generated_candidates_preserve_boundary():
    candidates = generate_controlled_candidate_programs()

    assert all(candidate["program_depth"] <= 3 for candidate in candidates)
    assert all(candidate["deterministic"] is True for candidate in candidates)
    assert all(candidate["local_only"] is True for candidate in candidates)
    assert all(candidate["public_safe"] is True for candidate in candidates)
    assert all(candidate["runtime_wiring_required"] is False for candidate in candidates)
    assert all(candidate["runtime_solver_patch"] is False for candidate in candidates)
    assert all(candidate["candidate_generator_runtime_wiring"] is False for candidate in candidates)
    assert all(candidate["real_submission_candidate"] is False for candidate in candidates)
    assert all(candidate["kaggle_submission_payload"] is False for candidate in candidates)


def test_candidate_evidence_pack_is_complete():
    candidates = generate_controlled_candidate_programs()
    evidence = build_candidate_evidence_pack(candidates)

    assert evidence["candidate_count"] == 12
    assert evidence["candidate_family_count"] == 7
    assert evidence["max_program_depth"] == 2
    assert evidence["unique_candidate_ids"] is True
    assert evidence["all_candidates_deterministic"] is True
    assert evidence["all_runtime_wiring_blocked"] is True
    assert evidence["all_real_submission_blocked"] is True


def test_controlled_implementation_has_expected_shape():
    implementation = build_controlled_candidate_generator_implementation(source_record={})

    assert implementation["candidate_template_count"] == 12
    assert implementation["candidate_family_count"] == 7
    assert implementation["parameter_binding_field_count"] == 8
    assert implementation["implementation_component_count"] == 6
    assert implementation["generated_candidate_count"] == 12
    assert implementation["max_program_depth"] == 2
    assert implementation["candidate_generator_wiring_authorized"] is False
    assert implementation["runtime_wiring_authorized"] is False
    assert implementation["recommended_next_stage"] == NEXT_STAGE


def test_controlled_candidate_generator_fails_if_runtime_wiring_mutated():
    record = build_controlled_candidate_generator_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_controlled_candidate_generator_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_controlled_candidate_generator_fails_if_candidate_count_mutated():
    record = build_controlled_candidate_generator_record(baseline_commit="TEST-COMMIT")
    record["generated_candidate_count"] = 11

    issues = validate_controlled_candidate_generator_record(record)

    assert "GENERATED_CANDIDATE_COUNT_MISMATCH" in issues


def test_controlled_candidate_generator_artifacts_are_written(tmp_path: Path):
    record = build_controlled_candidate_generator_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-implementation-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-implementation-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-implementation-v1.md" in written_files
