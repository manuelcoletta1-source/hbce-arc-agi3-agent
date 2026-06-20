from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map_review import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_improvement_map_review,
    build_review_items,
    write_artifacts,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map import (
    build_candidate_generator_improvement_map,
)


def test_task_5_review_is_ready_valid_and_passed() -> None:
    data = build_candidate_generator_improvement_map_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["review_ready"] is True
    assert data["review_locked"] is True
    assert data["review_passed"] is True
    assert data["review_only"] is True
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_5_preserves_task_4_baseline() -> None:
    source = build_candidate_generator_improvement_map()
    data = build_candidate_generator_improvement_map_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "d5fb1e7"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "D52615F216F01836"
    assert data["source_map_signature"] == source["signature"] == "D52615F216F01836"
    assert data["source_map_validation"].endswith("_VALID")
    assert data["next_stage"] == NEXT_STAGE


def test_task_5_review_items_confirm_all_task_4_items() -> None:
    source = build_candidate_generator_improvement_map()
    review_items = build_review_items(source)

    assert len(review_items) == 6
    assert {item.source_item_id for item in review_items} == {
        "M18-CGIM-1",
        "M18-CGIM-2",
        "M18-CGIM-3",
        "M18-CGIM-4",
        "M18-CGIM-5",
        "M18-CGIM-6",
    }
    assert all(item.review_decision == "CONFIRMED_NO_IMPLEMENTATION" for item in review_items)
    assert not any(item.blocking_issue for item in review_items)
    assert not any(item.implementation_authorized for item in review_items)
    assert not any(item.runtime_execution_authorized for item in review_items)


def test_task_5_boundary_blocks_runtime_submission_and_implementation() -> None:
    controls = build_boundary_controls()

    assert controls["review_only"] is True
    assert controls["planning_only"] is True
    assert controls["source_map_confirmed"] is True
    assert controls["source_map_reopened"] is False
    assert controls["implementation_authorization_granted"] is False
    assert controls["implementation_authorized"] is False
    assert controls["implementation_blocked"] is True
    assert controls["implementation_performed"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["candidate_generator_wiring_authorized"] is False
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


def test_task_5_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_improvement_map_review()

    assert data["acceptance_gate_count"] > 40
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_5_signature_is_deterministic() -> None:
    first = build_candidate_generator_improvement_map_review()
    second = build_candidate_generator_improvement_map_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["review_id"].endswith(first["signature"])


def test_task_5_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-5"
    docs_path = tmp_path / "docs" / "task-5.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "review_only=true" in manifest
    assert "implementation_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Improvement Map Review v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
