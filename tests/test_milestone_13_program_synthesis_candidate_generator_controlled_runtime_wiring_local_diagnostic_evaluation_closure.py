from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_local_diagnostic_evaluation_closure import (
    CLOSURE_VERDICT,
    NEXT_STAGE,
    TASK_NAME,
    build_closure_gate_map,
    build_local_diagnostic_evaluation_closure_record,
    review_source_review_artifact,
    validate_local_diagnostic_evaluation_closure_record,
    write_artifacts,
)


def test_source_review_artifact_passes():
    review = review_source_review_artifact()

    assert review["source_review_artifact_present"] is True
    assert review["source_review_artifact_parseable"] is True
    assert review["source_review_passed"] is True


def test_closure_gate_map_passes():
    source = review_source_review_artifact()["source_record"]
    gates = build_closure_gate_map(source)

    assert len(gates) == 36
    assert all(gates.values())


def test_task18_closure_record_is_valid():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["closure_verdict"] == CLOSURE_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["local_diagnostic_evaluation_closed"] is True
    assert record["ready_for_milestone_closure_review"] is True
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["diagnostic_case_count"] == 12
    assert record["diagnostic_pass_count"] == 12
    assert record["diagnostic_failure_count"] == 0
    assert record["diagnostic_average_score"] == 0.6875
    assert record["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_local_diagnostic_evaluation_closure_record(record) == []


def test_task18_validation_fails_if_not_closed():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    record["local_diagnostic_evaluation_closed"] = False

    issues = validate_local_diagnostic_evaluation_closure_record(record)

    assert "local_diagnostic_evaluation_closed_NOT_TRUE" in issues


def test_task18_validation_fails_if_runtime_execution_performed():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_local_diagnostic_evaluation_closure_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_task18_validation_fails_if_kaggle_upload_performed():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    record["kaggle_upload_performed"] = True

    issues = validate_local_diagnostic_evaluation_closure_record(record)

    assert "kaggle_upload_performed_NOT_FALSE" in issues


def test_task18_validation_fails_if_score_is_changed():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    record["diagnostic_average_score"] = 0.1

    issues = validate_local_diagnostic_evaluation_closure_record(record)

    assert "DIAGNOSTIC_AVERAGE_SCORE_MISMATCH" in issues


def test_task18_validation_fails_if_kaggle_score_semantics_removed():
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    record["kaggle_score_semantics"] = "KAGGLE_SCORE"

    issues = validate_local_diagnostic_evaluation_closure_record(record)

    assert "KAGGLE_SCORE_SEMANTICS_MISMATCH" in issues


def test_task18_artifacts_are_written(tmp_path: Path):
    record = build_local_diagnostic_evaluation_closure_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-local-diagnostic-evaluation-closure-v1.md" in written_files
