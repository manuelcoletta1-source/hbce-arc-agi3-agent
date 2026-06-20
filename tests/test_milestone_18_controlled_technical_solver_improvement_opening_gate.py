from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_18_controlled_technical_solver_improvement_opening_gate as m


def test_identity_and_source_binding() -> None:
    status = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["pipeline_ready_marker"] == m.PIPELINE_READY_MARKER
    assert status["opening_gate_marker"] == m.OPENING_GATE_MARKER
    assert status["milestone_18_name"] == "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
    assert status["source_milestone_17_terminal_stop_commit"] == "bd94b8a"
    assert status["source_milestone_17_terminal_stop_signature"] == "B0355A824F6C64C7"
    assert status["source_milestone_17_terminal_stage"] == m.SOURCE_MILESTONE_17_TERMINAL_STAGE
    assert status["previous_stage"] == "OPERATOR_DIRECTION_REQUIRED_BEFORE_MILESTONE_18"
    assert status["next_stage"] == "MILESTONE_18_TASK_2_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_V1"


def test_opening_scope_verdict_and_decision() -> None:
    status = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()

    assert status["opening_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_ONLY"
    assert status["milestone_18_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["runtime_authorization_scope"] == "NOT_GRANTED"
    assert status["submission_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.OPENING_GATE_VERDICT
    assert status["decision"] == "OPEN_MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert status["opening_gate_reason"] == m.OPENING_GATE_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()
    status_b = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert all(ch in "0123456789ABCDEF" for ch in status_a["signature"])


def test_opening_flags_and_objectives() -> None:
    status = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()
    objectives = status["technical_solver_improvement_objectives"]

    assert status["operator_direction_received"] is True
    assert status["operator_direction_value"] == "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
    assert status["milestone_17_stopped"] is True
    assert status["milestone_18_opening_allowed"] is True
    assert status["milestone_18_opened"] is True
    assert status["controlled_technical_solver_improvement_opening_gate_ready"] is True
    assert status["controlled_technical_solver_improvement_opening_gate_passed"] is True
    assert status["controlled_technical_solver_improvement_opening_gate_locked"] is True
    assert status["objective_count"] == 5
    assert len(objectives) == 5
    assert objectives[0]["objective_id"] == "M18-OBJ-1"
    assert objectives[0]["status"] == "NEXT_TASK"
    for objective in objectives:
        assert objective["implementation_authorized"] == "false"


def test_implementation_runtime_submission_and_boundary_are_blocked() -> None:
    status = m.build_milestone_18_controlled_technical_solver_improvement_opening_gate()

    assert status["implementation_authorization_granted"] is False
    assert status["implementation_authorized"] is False
    assert status["implementation_blocked"] is True
    assert status["implementation_performed"] is False
    assert status["runtime_solver_patch_allowed"] is False
    assert status["runtime_solver_modified"] is False
    assert status["candidate_generator_patch_allowed"] is False
    assert status["candidate_generator_modified"] is False
    assert status["ranker_patch_allowed"] is False
    assert status["ranker_modified"] is False
    assert status["runtime_wiring_allowed"] is False
    assert status["runtime_wiring_performed"] is False
    assert status["runtime_activation_authorized"] is False
    assert status["runtime_activation_performed"] is False
    assert status["runtime_execution_allowed"] is False
    assert status["runtime_execution_performed"] is False
    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["upload_performed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_authentication_performed"] is False
    assert status["kaggle_submission_sent"] is False
    assert status["competitive_score_claim_allowed"] is False
    assert status["official_score_claim_allowed"] is False
    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True
    assert status["local_only"] is True
    assert status["deterministic"] is True
    assert status["public_safe"] is True
    assert status["external_api_dependency"] is False
    assert status["internet_during_eval"] is False


def test_validation_payload_and_artifacts(tmp_path, monkeypatch) -> None:
    artifact_dir = tmp_path / "examples" / "milestone-18" / "controlled-technical-solver-improvement-opening-gate-v1"
    doc_path = tmp_path / "docs" / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_milestone_18_controlled_technical_solver_improvement_opening_gate_artifacts()
    payload = m.opening_gate_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["opening_gate_failure_count"] == 0
    assert status["opening_gate_count"] >= 60
    assert m.validate_milestone_18_controlled_technical_solver_improvement_opening_gate(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["milestone_18_name"] == "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
    assert index_payload["source_milestone_17_terminal_stop_commit"] == "bd94b8a"
    assert index_payload["source_milestone_17_terminal_stop_signature"] == "B0355A824F6C64C7"
    assert index_payload["opening_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_OPENING_GATE_ONLY"
    assert index_payload["milestone_18_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert index_payload["operator_direction_received"] is True
    assert index_payload["milestone_18_opened"] is True
    assert index_payload["implementation_blocked"] is True
    assert index_payload["runtime_execution_allowed"] is False
    assert index_payload["kaggle_submission_sent"] is False
    assert m.OPENING_GATE_MARKER in markdown
    assert "This opening gate authorizes planning only." in markdown
    assert "It does not authorize implementation." in markdown
    assert "It does not authorize runtime execution." in markdown
    assert "It does not authorize Kaggle authentication, upload, or submission." in markdown
    assert "opening_gate_count=" in manifest
    assert "opening_gate_failure_count=0" in manifest
    assert (artifact_dir / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.json").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-improvement-opening-gate-index-v1.json").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-improvement-opening-gate-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-18-controlled-technical-solver-improvement-opening-gate-v1.md")
