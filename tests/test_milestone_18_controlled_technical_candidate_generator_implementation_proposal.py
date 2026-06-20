from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_decision_gate_review import (
    build_candidate_generator_implementation_decision_gate_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_proposal import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_proposal,
    build_proposal_items,
    write_artifacts,
)


def test_task_10_proposal_is_ready_valid_and_proposal_only() -> None:
    data = build_candidate_generator_implementation_proposal()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["implementation_proposal_ready"] is True
    assert data["implementation_proposal_created"] is True
    assert data["implementation_proposal_review_required"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["implementation_authorization_scope"] == "PROPOSAL_ONLY_NO_CODE_NO_RUNTIME"
    assert data["blocking_issue_count"] == 0


def test_task_10_preserves_task_9_baseline() -> None:
    source = build_candidate_generator_implementation_decision_gate_review()
    data = build_candidate_generator_implementation_proposal()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "51a7e3b"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "3C632A7BAA041134"
    assert data["source_decision_gate_review_signature"] == source["signature"] == "3C632A7BAA041134"
    assert data["source_decision_gate_review_validation"].endswith("_VALID")
    assert "PROPOSAL_STAGE_ALLOWED" in data["source_decision_gate_review_verdict"]
    assert data["next_stage"] == NEXT_STAGE


def test_task_10_creates_six_proposal_items_without_code_authorization() -> None:
    source = build_candidate_generator_implementation_decision_gate_review()
    proposal_items = build_proposal_items(source)

    assert len(proposal_items) == 6
    assert {item.source_improvement_item for item in proposal_items} == {
        "M18-CGIM-1",
        "M18-CGIM-2",
        "M18-CGIM-3",
        "M18-CGIM-4",
        "M18-CGIM-5",
        "M18-CGIM-6",
    }
    assert all(item.proposal_kind == "CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY" for item in proposal_items)
    assert all(item.implementation_scope == "PROPOSAL_ONLY_NO_CODE_NO_RUNTIME" for item in proposal_items)
    assert all(item.proposal_review_required for item in proposal_items)
    assert all(len(item.deterministic_constraints) >= 3 for item in proposal_items)
    assert all(len(item.test_expectations) >= 3 for item in proposal_items)
    assert all(len(item.guardrails) >= 3 for item in proposal_items)
    assert not any(item.implementation_code_authorized for item in proposal_items)
    assert not any(item.runtime_execution_authorized for item in proposal_items)
    assert not any(item.real_submission_authorized for item in proposal_items)


def test_task_10_boundary_keeps_runtime_code_and_submission_blocked() -> None:
    controls = build_boundary_controls()

    assert controls["implementation_proposal_only"] is True
    assert controls["implementation_proposal_created"] is True
    assert controls["implementation_proposal_review_required"] is True
    assert controls["implementation_proposal_ready"] is True
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


def test_task_10_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_proposal()

    assert data["acceptance_gate_count"] > 50
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_10_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_proposal()
    second = build_candidate_generator_implementation_proposal()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["implementation_proposal_id"].endswith(first["signature"])


def test_task_10_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-10"
    docs_path = tmp_path / "docs" / "task-10.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "implementation_proposal_only=true" in manifest
    assert "implementation_proposal_review_required=true" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Proposal v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
