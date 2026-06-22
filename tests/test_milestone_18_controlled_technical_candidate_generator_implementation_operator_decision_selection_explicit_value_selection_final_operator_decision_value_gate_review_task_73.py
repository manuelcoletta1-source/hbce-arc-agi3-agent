from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_value_gate import (
    allowed_operator_decision_values,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_task_72 import (
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review_task_73 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review,
    build_final_operator_decision_value_gate_review_items,
    write_artifacts,
)


def test_task_73_ready_valid_passed() -> None:
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["final_operator_decision_value_gate_review_ready"] is True
    assert data["final_operator_decision_value_gate_review_passed"] is True
    assert data["final_operator_decision_value_gate_confirmed"] is True
    assert data["milestone_18_closure_required"] is True
    assert data["milestone_18_closure_allowed_next"] is True
    assert data["selected_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["selected_operator_decision_value_validated"] is False
    assert data["final_operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["final_operator_decision_value_selected"] is False
    assert data["final_operator_decision_value_validated"] is False
    assert data["final_operator_decision_value_gate_authorized"] is False
    assert data["final_operator_decision_value_gate_decision_selected"] is False
    assert data["operator_decision_selection_authorization_received"] is False
    assert data["operator_decision_selection_authorized"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_73_preserves_task_72_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate()
    data = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "9da5ad7"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "14C24698D4231248"
    assert (
        data["source_final_operator_decision_value_gate_signature"]
        == source["signature"]
        == PREVIOUS_SIGNATURE
    )
    assert source["final_operator_decision_value_gate_created"] is True
    assert source["final_operator_decision_value_gate_review_required"] is True
    assert source["final_operator_decision_value_gate_passed"] is False


def test_task_73_review_items_pending_closure_no_code() -> None:
    source = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate()
    items = build_final_operator_decision_value_gate_review_items(source)

    assert len(items) == 6
    assert all(
        item["review_decision"]
        == "CONFIRMED_FINAL_OPERATOR_DECISION_VALUE_GATE_PENDING_MILESTONE_18_CLOSURE"
        for item in items
    )
    assert all(item["allowed_operator_decision_values_confirmed"] == allowed_operator_decision_values() for item in items)
    assert all(item["selected_operator_decision_value_confirmed"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["selected_operator_decision_value_validated_confirmed"] for item in items)
    assert all(item["final_operator_decision_value_confirmed"] == "PENDING_EXPLICIT_OPERATOR_DECISION" for item in items)
    assert not any(item["final_operator_decision_value_selected_confirmed"] for item in items)
    assert not any(item["final_operator_decision_value_validated_confirmed"] for item in items)
    assert all(item["final_operator_decision_value_gate_created_confirmed"] is True for item in items)
    assert all(item["final_operator_decision_value_gate_review_required_confirmed"] is True for item in items)
    assert not any(item["final_operator_decision_value_gate_authorized_confirmed"] for item in items)
    assert not any(item["final_operator_decision_value_gate_decision_selected_confirmed"] for item in items)
    assert all(item["milestone_18_closure_required"] is True for item in items)
    assert all(item["milestone_18_closure_allowed_next"] is True for item in items)
    assert not any(item["operator_decision_selection_authorization_received_confirmed"] for item in items)
    assert not any(item["operator_decision_selection_authorized_confirmed"] for item in items)
    assert not any(item["explicit_operator_authorization_received_confirmed"] for item in items)
    assert not any(item["implementation_code_authorized"] for item in items)
    assert not any(item["runtime_execution_authorized"] for item in items)
    assert not any(item["real_submission_authorized"] for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_73_boundary_blocks_code_runtime_submission() -> None:
    controls = build_boundary_controls()

    assert controls["final_operator_decision_value_gate_review_only"] is True
    assert controls["final_operator_decision_value_gate_confirmed"] is True
    assert controls["final_operator_decision_value_gate_review_passed"] is True
    assert controls["milestone_18_closure_required"] is True
    assert controls["milestone_18_closure_created"] is False
    assert controls["milestone_18_closure_allowed_next"] is True
    assert controls["final_operator_decision_value_gate_authorized"] is False
    assert controls["final_operator_decision_value_gate_decision_selected"] is False
    assert controls["final_operator_decision_value_pending"] is True
    assert controls["final_operator_decision_value_selected"] is False
    assert controls["final_operator_decision_value_validated"] is False
    assert controls["operator_decision_selection_authorization_received"] is False
    assert controls["operator_decision_selection_authorized"] is False
    assert controls["explicit_operator_authorization_received"] is False
    assert controls["implementation_code_authorized"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["runtime_execution_allowed"] is False
    assert controls["real_submission_allowed"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["private_core_exposure"] is False
    assert controls["legal_certification"] is False
    assert controls["fail_closed_active"] is True


def test_task_73_acceptance_and_signature() -> None:
    first = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()
    second = build_candidate_generator_implementation_operator_decision_selection_explicit_value_selection_final_operator_decision_value_gate_review()

    assert first["acceptance_gate_count"] > 155
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []
    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["final_operator_decision_value_gate_review_id"].endswith(first["signature"])


def test_task_73_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "task-73",
        docs_path=tmp_path / "docs" / "task-73.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "final_operator_decision_value_gate_review_ready=true" in manifest
    assert "final_operator_decision_value_gate_review_passed=true" in manifest
    assert "final_operator_decision_value_gate_confirmed=true" in manifest
    assert "milestone_18_closure_required=true" in manifest
    assert "milestone_18_closure_allowed_next=true" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "selected_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "final_operator_decision_value_selected=false" in manifest
    assert "final_operator_decision_value_validated=false" in manifest
    assert "final_operator_decision_value_gate_authorized=false" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Selection Explicit Value Selection Final Operator Decision Value Gate Review v1" in markdown
