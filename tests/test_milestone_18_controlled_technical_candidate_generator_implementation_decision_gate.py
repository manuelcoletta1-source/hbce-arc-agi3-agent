from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_authorization_gate_review import (
    build_candidate_generator_implementation_authorization_gate_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_decision_gate import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_decision_gate,
    build_decision_items,
    write_artifacts,
)


def test_task_8_decision_gate_is_ready_valid_and_proposal_review_only() -> None:
    data = build_candidate_generator_implementation_decision_gate()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["decision_gate_ready"] is True
    assert data["decision_gate_created"] is True
    assert data["decision_gate_locked"] is True
    assert data["decision_gate_review_required"] is True
    assert data["decision_gate_passed"] is False
    assert data["decision_gate_value"] == "ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY"
    assert data["implementation_proposal_review_allowed_next"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_8_preserves_task_7_baseline() -> None:
    source = build_candidate_generator_implementation_authorization_gate_review()
    data = build_candidate_generator_implementation_decision_gate()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "2f58bdb"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "929FA73D0F5361FB"
    assert data["source_gate_review_signature"] == source["signature"] == "929FA73D0F5361FB"
    assert data["source_gate_review_validation"].endswith("_VALID")
    assert "PENDING_DECISION" in data["source_gate_review_verdict"]
    assert data["next_stage"] == NEXT_STAGE


def test_task_8_creates_six_decision_items_without_code_authorization() -> None:
    source = build_candidate_generator_implementation_authorization_gate_review()
    decision_items = build_decision_items(source)

    assert len(decision_items) == 6
    assert {item.source_improvement_item for item in decision_items} == {
        "M18-CGIM-1",
        "M18-CGIM-2",
        "M18-CGIM-3",
        "M18-CGIM-4",
        "M18-CGIM-5",
        "M18-CGIM-6",
    }
    assert all(
        item.decision_value == "ALLOW_NEXT_CONTROLLED_IMPLEMENTATION_PROPOSAL_REVIEW_ONLY"
        for item in decision_items
    )
    assert all(
        item.decision_effect == "NEXT_STAGE_REVIEW_REQUIRED_NO_CODE_IMPLEMENTATION"
        for item in decision_items
    )
    assert all(item.review_required_before_effective_authorization for item in decision_items)
    assert not any(item.implementation_code_authorized for item in decision_items)
    assert not any(item.runtime_execution_authorized for item in decision_items)
    assert not any(item.real_submission_authorized for item in decision_items)


def test_task_8_boundary_blocks_code_runtime_and_submission() -> None:
    controls = build_boundary_controls()

    assert controls["decision_gate_only"] is True
    assert controls["decision_gate_created"] is True
    assert controls["decision_gate_review_required"] is True
    assert controls["decision_gate_passed"] is False
    assert controls["decision_gate_locked"] is True
    assert controls["decision_gate_allows_next_proposal_review_only"] is True
    assert controls["implementation_proposal_review_allowed_next"] is True
    assert controls["implementation_code_authorization_granted"] is False
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
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_required"] is True
    assert controls["fail_closed_active"] is True
    assert controls["local_only"] is True
    assert controls["deterministic"] is True
    assert controls["public_safe"] is True


def test_task_8_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_decision_gate()

    assert data["acceptance_gate_count"] > 55
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_8_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_decision_gate()
    second = build_candidate_generator_implementation_decision_gate()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["decision_gate_id"].endswith(first["signature"])


def test_task_8_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-8"
    docs_path = tmp_path / "docs" / "task-8.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "decision_gate_only=true" in manifest
    assert "implementation_proposal_review_allowed_next=true" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Decision Gate v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
