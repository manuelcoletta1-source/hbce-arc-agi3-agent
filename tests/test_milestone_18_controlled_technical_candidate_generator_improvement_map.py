from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_improvement_items,
    build_candidate_generator_improvement_map,
    write_artifacts,
)


def test_task_4_map_is_ready_and_valid() -> None:
    data = build_candidate_generator_improvement_map()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["candidate_generator_improvement_map_ready"] is True
    assert data["candidate_generator_improvement_map_locked"] is True
    assert data["candidate_generator_improvement_map_review_required"] is True
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_4_preserves_previous_task_3_baseline() -> None:
    data = build_candidate_generator_improvement_map()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "ff72908"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "38A0F948AFF91AC9"
    assert data["next_stage"] == NEXT_STAGE
    assert data["implementation_authorization_scope"] == "NOT_GRANTED"


def test_task_4_has_six_controlled_improvement_items() -> None:
    items = build_candidate_generator_improvement_items()

    assert len(items) == 6
    assert {item.source_limitation_id for item in items} == {
        "M18-LIM-1",
        "M18-LIM-2",
        "M18-LIM-3",
        "M18-LIM-4",
        "M18-LIM-5",
        "M18-LIM-6",
    }
    assert all(item.review_required_before_implementation for item in items)
    assert not any(item.implementation_authorized for item in items)
    assert all(item.blocked_actions for item in items)


def test_task_4_boundary_blocks_runtime_submission_and_implementation() -> None:
    controls = build_boundary_controls()

    assert controls["planning_only"] is True
    assert controls["implementation_authorization_granted"] is False
    assert controls["implementation_authorized"] is False
    assert controls["implementation_blocked"] is True
    assert controls["implementation_performed"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["solver_runtime_modified"] is False
    assert controls["ranker_runtime_modified"] is False
    assert controls["runtime_execution_allowed"] is False
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


def test_task_4_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_improvement_map()

    assert data["acceptance_gate_count"] > 30
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_4_signature_is_deterministic() -> None:
    first = build_candidate_generator_improvement_map()
    second = build_candidate_generator_improvement_map()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["map_id"].endswith(first["signature"])


def test_task_4_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-4"
    docs_path = tmp_path / "docs" / "task-4.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "implementation_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Improvement Map v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
