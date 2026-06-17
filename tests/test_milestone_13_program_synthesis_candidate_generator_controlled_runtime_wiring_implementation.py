from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_implementation import (
    NEXT_STAGE,
    TASK_NAME,
    build_controlled_runtime_wiring_implementation_record,
    validate_controlled_runtime_wiring_implementation_record,
    write_artifacts,
)
from hbce_arc_agi3.program_synthesis_candidate_fixture_bridge import build_candidate_fixture_matrix
from hbce_arc_agi3.program_synthesis_candidate_generator_runtime_adapter import (
    normalize_generated_candidate,
    normalize_generated_candidates,
)
from hbce_arc_agi3.solver_runtime_candidate_generation_hook import (
    build_controlled_candidate_generation_hook_payload,
)


def test_normalize_generated_candidate_is_deterministic_and_inactive():
    candidate = {"family": "color_mapping", "operation": "map", "program": ["a", "b"], "confidence": 1.7}

    first = normalize_generated_candidate(candidate, index=0)
    second = normalize_generated_candidate(candidate, index=0)

    assert first == second
    assert first.confidence == 1.0
    assert first.runtime_activation_allowed is False
    assert first.candidate_id.startswith("RUNTIME-CANDIDATE-")


def test_normalize_generated_candidates_sorts_output():
    candidates = [
        {"family": "z_family", "operation": "op_z", "confidence": 0.1},
        {"family": "a_family", "operation": "op_a", "confidence": 0.2},
    ]

    normalized = normalize_generated_candidates(candidates)

    assert [item["family"] for item in normalized] == ["a_family", "z_family"]


def test_fixture_bridge_builds_diagnostic_matrix_without_execution():
    candidates = normalize_generated_candidates(
        [
            {"family": "color", "operation": "map"},
            {"family": "object", "operation": "move"},
        ]
    )
    fixtures = [
        {"fixture_id": "FIXTURE-1", "family": "color"},
        {"fixture_id": "FIXTURE-2", "family": "object"},
    ]

    matrix = build_candidate_fixture_matrix(candidates, fixtures)

    assert len(matrix) == 4
    assert all(row["diagnostic_only"] is True for row in matrix)
    assert all(row["runtime_execution_performed"] is False for row in matrix)
    assert all(row["real_evaluation_performed"] is False for row in matrix)


def test_controlled_hook_payload_is_local_only_and_blocked():
    payload = build_controlled_candidate_generation_hook_payload(
        [{"family": "color", "operation": "map"}],
        [{"fixture_id": "FIXTURE-1", "family": "color"}],
    )

    assert payload["runtime_candidate_count"] == 1
    assert payload["candidate_fixture_matrix_count"] == 1
    assert payload["controlled_implementation_performed"] is True
    assert payload["runtime_activation_performed"] is False
    assert payload["runtime_execution_performed"] is False
    assert payload["real_evaluation_performed"] is False
    assert payload["kaggle_submission_sent"] is False
    assert payload["private_core_exposure"] is False
    assert payload["legal_certification"] is False


def test_task14_controlled_runtime_wiring_implementation_record_is_valid():
    record = build_controlled_runtime_wiring_implementation_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_review_passed"] is True
    assert record["controlled_implementation_performed"] is True
    assert record["controlled_runtime_adapter_created"] is True
    assert record["controlled_solver_hook_created"] is True
    assert record["controlled_fixture_bridge_created"] is True
    assert record["runtime_candidate_count"] == 4
    assert record["candidate_fixture_matrix_count"] == 12
    assert record["runtime_activation_performed"] is False
    assert record["runtime_execution_performed"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_controlled_runtime_wiring_implementation_record(record) == []


def test_task14_validation_fails_if_runtime_execution_is_performed():
    record = build_controlled_runtime_wiring_implementation_record(baseline_commit="TEST-COMMIT")
    record["runtime_execution_performed"] = True

    issues = validate_controlled_runtime_wiring_implementation_record(record)

    assert "runtime_execution_performed_NOT_FALSE" in issues


def test_task14_validation_fails_if_submission_is_sent():
    record = build_controlled_runtime_wiring_implementation_record(baseline_commit="TEST-COMMIT")
    record["kaggle_submission_sent"] = True

    issues = validate_controlled_runtime_wiring_implementation_record(record)

    assert "kaggle_submission_sent_NOT_FALSE" in issues


def test_task14_artifacts_are_written(tmp_path: Path):
    record = build_controlled_runtime_wiring_implementation_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-v1.md" in written_files
