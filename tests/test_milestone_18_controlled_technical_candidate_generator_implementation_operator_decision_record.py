from __future__ import annotations

import json

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_gate_review import (
    build_candidate_generator_implementation_operator_decision_gate_review,
)
from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_implementation_operator_decision_record import (
    NEXT_STAGE,
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_candidate_generator_implementation_operator_decision_record,
    build_operator_decision_record_items,
    write_artifacts,
)


def test_task_18_operator_decision_record_is_ready_valid_and_created() -> None:
    data = build_candidate_generator_implementation_operator_decision_record()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["operator_decision_record_ready"] is True
    assert data["operator_decision_record_created"] is True
    assert data["operator_decision_record_locked"] is True
    assert data["operator_decision_record_open"] is False
    assert data["operator_decision_record_review_required"] is True
    assert data["operator_decision_record_passed"] is False
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


def test_task_18_preserves_task_17_baseline() -> None:
    source = build_candidate_generator_implementation_operator_decision_gate_review()
    data = build_candidate_generator_implementation_operator_decision_record()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "dcc5195"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "B6562BE15E923085"
    assert (
        data["source_operator_decision_gate_review_signature"]
        == source["signature"]
        == "B6562BE15E923085"
    )
    assert data["source_operator_decision_gate_review_validation"].endswith("_VALID")
    assert "OPERATOR_DECISION_RECORD_REQUIRED_NO_CODE" in data[
        "source_operator_decision_gate_review_verdict"
    ]
    assert data["next_stage"] == NEXT_STAGE


def test_task_18_creates_six_pending_operator_decision_record_items() -> None:
    source = build_candidate_generator_implementation_operator_decision_gate_review()
    record_items = build_operator_decision_record_items(source)

    assert len(record_items) == 6
    assert {item.source_operator_decision_gate_item for item in record_items} == {
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-1",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-2",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-3",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-4",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-5",
        "M18-CG-IMPL-OPERATOR-DECISION-GATE-6",
    }
    assert all(
        item.record_status
        == "OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION"
        for item in record_items
    )
    assert all(
        item.operator_decision_value == "PENDING_EXPLICIT_OPERATOR_DECISION"
        for item in record_items
    )
    assert not any(item.operator_decision_value_selected for item in record_items)
    assert not any(item.operator_decision_received for item in record_items)
    assert not any(item.explicit_operator_authorization_received for item in record_items)
    assert all(item.operator_decision_record_review_required for item in record_items)
    assert all(item.implementation_authorization_candidate_confirmed for item in record_items)
    assert not any(item.implementation_code_authorized for item in record_items)
    assert not any(item.runtime_execution_authorized for item in record_items)
    assert not any(item.real_submission_authorized for item in record_items)
    assert not any(item.blocking_issue for item in record_items)


def test_task_18_boundary_blocks_code_runtime_submission_and_decision_value() -> None:
    controls = build_boundary_controls()

    assert controls["operator_decision_record_only"] is True
    assert controls["operator_decision_record_created"] is True
    assert controls["operator_decision_record_review_required"] is True
    assert controls["operator_decision_record_locked"] is True
    assert controls["operator_decision_record_open"] is False
    assert controls["operator_decision_record_passed"] is False
    assert controls["operator_decision_record_allows_next_review_only"] is True
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


def test_task_18_acceptance_gates_have_no_failures() -> None:
    data = build_candidate_generator_implementation_operator_decision_record()

    assert data["acceptance_gate_count"] > 80
    assert data["acceptance_gate_failure_count"] == 0
    assert data["acceptance_gate_failures"] == []
    assert all(gate["passed"] is True for gate in data["acceptance_gates"])


def test_task_18_signature_is_deterministic() -> None:
    first = build_candidate_generator_implementation_operator_decision_record()
    second = build_candidate_generator_implementation_operator_decision_record()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["operator_decision_record_id"].endswith(first["signature"])


def test_task_18_artifacts_are_written(tmp_path) -> None:
    artifact_dir = tmp_path / "examples" / "task-18"
    docs_path = tmp_path / "docs" / "task-18.md"

    paths = write_artifacts(artifact_dir=artifact_dir, docs_path=docs_path)

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    index = json.loads(paths["index"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    markdown = paths["markdown"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert index["signature"] == data["signature"]
    assert "operator_decision_record_only=true" in manifest
    assert "operator_decision_record_created=true" in manifest
    assert "operator_decision_required=true" in manifest
    assert "operator_decision_received=false" in manifest
    assert "operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "operator_decision_value_selected=false" in manifest
    assert "implementation_code_authorized=false" in manifest
    assert "real_submission_allowed=false" in manifest
    assert "Controlled Technical Candidate Generator Implementation Operator Decision Record v1" in markdown
    assert docs_path.read_text(encoding="utf-8") == markdown
