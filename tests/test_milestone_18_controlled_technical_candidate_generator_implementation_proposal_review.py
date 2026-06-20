from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal import (
    build_candidate_generator_implementation_proposal,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal_review import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_proposal_review,
    build_proposal_review_items,
    write_artifacts,
)


def test_task_11_proposal_review_is_ready_valid_and_passed() -> None:
    data = build_candidate_generator_implementation_proposal_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["implementation_proposal_review_ready"] is True
    assert data["implementation_proposal_review_passed"] is True
    assert data["implementation_proposal_confirmed"] is True
    assert data["authorization_review_gate_required"] is True
    assert data["authorization_review_gate_allowed_next"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_11_preserves_task_10_baseline() -> None:
    source = build_candidate_generator_implementation_proposal()
    data = build_candidate_generator_implementation_proposal_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "b805b16"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "A2BE24B5965B838E"
    assert data["source_proposal_signature"] == source["signature"] == "A2BE24B5965B838E"
    assert data["source_proposal_validation"].endswith("_VALID")
    assert "NO_CODE_NO_RUNTIME" in data["source_proposal_verdict"]
    assert data["next_stage"] == NEXT_STAGE


def test_task_11_reviews_six_proposal_items_without_code_authorization() -> None:
    source = build_candidate_generator_implementation_proposal()
    review_items = build_proposal_review_items(source)

    assert len(review_items) == 6
    assert {item.source_proposal_id for item in review_items} == {
        "M18-CG-IMPL-PROPOSAL-1",
        "M18-CG-IMPL-PROPOSAL-2",
        "M18-CG-IMPL-PROPOSAL-3",
        "M18-CG-IMPL-PROPOSAL-4",
        "M18-CG-IMPL-PROPOSAL-5",
        "M18-CG-IMPL-PROPOSAL-6",
    }
    assert all(
        item.review_decision == "CONFIRMED_PROPOSAL_VALID_PENDING_AUTHORIZATION_REVIEW_GATE"
        for item in review_items
    )
    assert all(item.proposal_accepted_for_next_gate for item in review_items)
    assert all(item.authorization_review_gate_required for item in review_items)
    assert not any(item.implementation_code_authorized for item in review_items)
    assert not any(item.runtime_execution_authorized for item in review_items)
    assert not any(item.real_submission_authorized for item in review_items)
    assert not any(item.blocking_issue for item in review_items)


def test_task_11_boundary_allows_only_next_authorization_review_gate() -> None:
    controls = build_boundary_controls()

    assert controls["implementation_proposal_review_only"] is True
    assert controls["implementation_proposal_confirmed"] is True
    assert controls["implementation_proposal_review_passed"] is True
    assert controls["authorization_review_gate_required"] is True
    assert controls["authorization_review_gate_created"] is False
    assert controls["authorization_review_gate_allowed_next"] is True
    assert controls["implementation_code_authorization_granted"] is False
    assert controls["implementation_code_authorized"] is False
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
    assert controls["submission_artifact_created"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_required"] is True
    assert controls["fail_closed_active"] is True
    assert controls["local_only"] is True
    assert controls["deterministic"] is True
    assert controls["public_safe"] is True


def test_task_11_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_proposal_review()

    assert data["acceptance_gate_count"] > 55
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_11_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_proposal_review()
    second = build_candidate_generator_implementation_proposal_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["implementation_proposal_review_id"].endswith(first["signature"])


def test_task_11_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-11"
    docs_path = tmp_path / "docs" / "task-11.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "implementation_proposal_review_only=true" in manifest
    assert "authorization_review_gate_required=true" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Proposal Review v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
