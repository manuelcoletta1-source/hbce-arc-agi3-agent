from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_authorization_gate import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_authorization_gate,
    build_gate_conditions,
    write_artifacts,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map_review import (
    build_candidate_generator_improvement_map_review,
)


def test_task_6_authorization_gate_is_ready_valid_and_closed() -> None:
    data = build_candidate_generator_implementation_authorization_gate()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["authorization_gate_ready"] is True
    assert data["authorization_gate_created"] is True
    assert data["authorization_gate_locked"] is True
    assert data["authorization_gate_open"] is False
    assert data["authorization_gate_review_required"] is True
    assert data["authorization_gate_passed"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_6_preserves_task_5_baseline() -> None:
    source = build_candidate_generator_improvement_map_review()
    data = build_candidate_generator_implementation_authorization_gate()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "1af8533"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "9EADD41F6C2BD263"
    assert data["source_review_signature"] == source["signature"] == "9EADD41F6C2BD263"
    assert data["source_review_validation"].endswith("_VALID")
    assert data["source_review_verdict"].endswith("_PASS_NO_IMPLEMENTATION")
    assert data["next_stage"] == NEXT_STAGE


def test_task_6_creates_six_gate_conditions_without_authorization() -> None:
    source = build_candidate_generator_improvement_map_review()
    conditions = build_gate_conditions(source)

    assert len(conditions) == 6
    assert {condition.source_improvement_item for condition in conditions} == {
        "M18-CGIM-1",
        "M18-CGIM-2",
        "M18-CGIM-3",
        "M18-CGIM-4",
        "M18-CGIM-5",
        "M18-CGIM-6",
    }
    assert all(condition.gate_decision == "GATE_CREATED_PENDING_REVIEW" for condition in conditions)
    assert all(condition.authorization_effect == "NO_IMPLEMENTATION_AUTHORIZATION_GRANTED" for condition in conditions)
    assert all(condition.review_required_before_authorization for condition in conditions)
    assert not any(condition.implementation_authorized for condition in conditions)
    assert not any(condition.runtime_execution_authorized for condition in conditions)
    assert not any(condition.blocking_issue for condition in conditions)


def test_task_6_boundary_blocks_implementation_runtime_and_submission() -> None:
    controls = build_boundary_controls()

    assert controls["authorization_gate_only"] is True
    assert controls["authorization_gate_created"] is True
    assert controls["authorization_gate_review_required"] is True
    assert controls["authorization_gate_open"] is False
    assert controls["authorization_gate_locked"] is True
    assert controls["authorization_gate_passed"] is False
    assert controls["operator_authorization_required"] is True
    assert controls["operator_authorization_received"] is False
    assert controls["implementation_authorization_granted"] is False
    assert controls["implementation_authorized"] is False
    assert controls["implementation_blocked"] is True
    assert controls["implementation_performed"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["candidate_generator_runtime_patch_allowed"] is False
    assert controls["solver_runtime_modified"] is False
    assert controls["ranker_runtime_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_evaluation_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["manual_upload_allowed"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_required"] is True
    assert controls["fail_closed_active"] is True
    assert controls["local_only"] is True
    assert controls["deterministic"] is True
    assert controls["public_safe"] is True


def test_task_6_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_authorization_gate()

    assert data["acceptance_gate_count"] > 50
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_6_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_authorization_gate()
    second = build_candidate_generator_implementation_authorization_gate()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["authorization_gate_id"].endswith(first["signature"])


def test_task_6_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-6"
    docs_path = tmp_path / "docs" / "task-6.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "authorization_gate_only=true" in manifest
    assert "authorization_gate_open=false" in manifest
    assert "implementation_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Authorization Gate v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
