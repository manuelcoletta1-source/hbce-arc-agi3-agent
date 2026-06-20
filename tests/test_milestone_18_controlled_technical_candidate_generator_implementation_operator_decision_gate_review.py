from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_gate import (
    build_candidate_generator_implementation_operator_decision_gate,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_gate_review import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_gate_review,
    build_operator_decision_gate_review_items,
    write_artifacts,
)


def test_task_17_operator_decision_gate_review_is_ready_valid_and_passed() -> None:
    data = build_candidate_generator_implementation_operator_decision_gate_review()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["operator_decision_gate_review_ready"] is True
    assert data["operator_decision_gate_review_passed"] is True
    assert data["operator_decision_gate_confirmed"] is True
    assert data["operator_decision_record_required"] is True
    assert data["operator_decision_record_allowed_next"] is True
    assert data["operator_decision_required"] is True
    assert data["operator_decision_received"] is False
    assert data["operator_decision_value"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert data["operator_decision_value_selected"] is False
    assert data["operator_authorization_received"] is False
    assert data["explicit_operator_authorization_received"] is False
    assert data["implementation_authorization_candidate_confirmed"] is True
    assert data["implementation_code_authorized"] is False
    assert data["implementation_allowed_now"] is False
    assert data["blocking_issue_count"] == 0


def test_task_17_preserves_task_16_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_gate()
    data = build_candidate_generator_implementation_operator_decision_gate_review()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "95fe0bf"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "61BE6CF6078C8065"
    assert (
        data["source_operator_decision_gate_signature"]
        == source["signature"]
        == "61BE6CF6078C8065"
    )
    assert data["source_operator_decision_gate_validation"].endswith("_VALID")
    assert "PENDING_EXPLICIT_OPERATOR_DECISION_NO_CODE" in data[
        "source_operator_decision_gate_verdict"
    ]
    assert data["next_stage"] == NEXT_STAGE


def test_task_17_reviews_six_operator_decision_gate_items_without_decision() -> None:
    source = build_candidate_generator_implementation_operator_decision_gate()
    review_items = build_operator_decision_gate_review_items(source)

    assert len(review_items) == 6
    assert {item.source_operator_decision_gate_item for item in review_items} == {
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-1",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-2",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-3",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-4",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-5",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-6",
    }
    assert all(
        item.review_decision
        == "CONFIRMED_OPERATOR_DECISION_GATE_PENDING_OPERATOR_DECISION_RECORD"
        for item in review_items
    )
    assert all(item.operator_decision_record_required for item in review_items)
    assert all(item.operator_decision_record_allowed_next for item in review_items)
    assert all(item.operator_decision_required_confirmed for item in review_items)
    assert all(item.operator_decision_received_confirmed_false for item in review_items)
    assert all(item.operator_decision_value_pending_confirmed for item in review_items)
    assert all(item.explicit_operator_authorization_received_confirmed_false for item in review_items)
    assert all(item.implementation_authorization_candidate_confirmed for item in review_items)
    assert not any(item.implementation_code_authorized for item in review_items)
    assert not any(item.runtime_execution_authorized for item in review_items)
    assert not any(item.real_submission_authorized for item in review_items)
    assert not any(item.blocking_issue for item in review_items)


def test_task_17_boundary_allows_only_next_operator_decision_record() -> None:
    controls = build_boundary_controls()

    assert controls["operator_decision_gate_review_only"] is True
    assert controls["operator_decision_gate_confirmed"] is True
    assert controls["operator_decision_gate_review_passed"] is True
    assert controls["operator_decision_record_required"] is True
    assert controls["operator_decision_record_created"] is False
    assert controls["operator_decision_record_allowed_next"] is True
    assert controls["operator_decision_required"] is True
    assert controls["operator_decision_received"] is False
    assert controls["operator_decision_value_selected"] is False
    assert controls["operator_authorization_required"] is True
    assert controls["operator_authorization_received"] is False
    assert controls["explicit_operator_authorization_received"] is False
    assert controls["implementation_authorization_candidate_confirmed"] is True
    assert controls["implementation_authorization_granted"] is False
    assert controls["implementation_code_authorization_granted"] is False
    assert controls["implementation_code_authorized"] is False
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


def test_task_17_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_operator_decision_gate_review()

    assert data["acceptance_gate_count"] > 80
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_17_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_operator_decision_gate_review()
    second = build_candidate_generator_implementation_operator_decision_gate_review()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["operator_decision_gate_review_id"].endswith(first["signature"])


def test_task_17_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-17"
    docs_path = tmp_path / "docs" / "task-17.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "operator_decision_gate_review_only=true" in manifest
    assert "operator_decision_record_required=true" in manifest
    assert "operator_decision_required=true" in manifest
    assert "operator_decision_received=false" in manifest
    assert "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Gate Review v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
