from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_implementation_review import (
    NEXT_STAGE,
    TASK_NAME,
    build_controlled_runtime_wiring_implementation_review_record,
    review_fixture_bridge_behavior,
    review_implemented_file_presence,
    review_runtime_candidate_adapter_behavior,
    review_solver_hook_behavior,
    validate_controlled_runtime_wiring_implementation_review_record,
    write_artifacts,
)


def test_task15_review_record_is_valid():
    record = build_controlled_runtime_wiring_implementation_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_implementation_passed"] is True
    assert record["implementation_review_passed"] is True
    assert record["ready_for_local_diagnostic_evaluation"] is True
    assert record["implemented_file_count"] == 3
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_controlled_runtime_wiring_implementation_review_record(record) == []


def test_file_presence_review_passes():
    review = review_implemented_file_presence()

    assert review["implemented_file_count"] == 3
    assert review["present_file_count"] == 3
    assert review["all_implemented_files_present"] is True


def test_runtime_candidate_adapter_review_passes():
    review = review_runtime_candidate_adapter_behavior()

    assert review["runtime_candidate_count"] == 4
    assert review["runtime_candidate_ids_unique"] is True
    assert review["all_runtime_activation_blocked"] is True
    assert review["all_candidate_ids_runtime_prefixed"] is True


def test_fixture_bridge_review_passes():
    review = review_fixture_bridge_behavior()

    assert review["candidate_fixture_matrix_count"] == 12
    assert review["all_rows_diagnostic_only"] is True
    assert review["all_rows_runtime_execution_false"] is True
    assert review["all_rows_real_evaluation_false"] is True


def test_solver_hook_review_passes_with_boundaries():
    review = review_solver_hook_behavior()

    assert review["runtime_candidate_count"] == 4
    assert review["candidate_fixture_matrix_count"] == 12
    assert review["controlled_implementation_performed"] is True
    assert review["runtime_activation_performed"] is False
    assert review["runtime_execution_performed"] is False
    assert review["real_evaluation_performed"] is False
    assert review["real_submission_allowed"] is False
    assert review["kaggle_authentication_performed"] is False
    assert review["kaggle_upload_performed"] is False
    assert review["kaggle_submission_sent"] is False
    assert review["private_core_exposure"] is False
    assert review["legal_certification"] is False


def test_task15_validation_fails_if_runtime_execution_performed():
    record = build_controlled_runtime_wiring_implementation_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_controlled_runtime_wiring_implementation_review_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_task15_validation_fails_if_kaggle_submission_sent():
    record = build_controlled_runtime_wiring_implementation_review_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_controlled_runtime_wiring_implementation_review_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_task15_artifacts_are_written(tmp_path: Path):
    record = build_controlled_runtime_wiring_implementation_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-review-v1.md" in written_files
