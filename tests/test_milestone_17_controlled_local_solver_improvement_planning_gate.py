from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_planning_gate as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["planning_gate_status_marker"] == m.PLANNING_GATE_STATUS_MARKER
    assert status["task_mode"] == m.TASK_MODE
    assert status["source_task_8_final_baseline_commit"] == m.SOURCE_TASK_8_FINAL_BASELINE_COMMIT
    assert status["source_task_8_final_signature"] == m.SOURCE_TASK_8_FINAL_SIGNATURE
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_selected_option_and_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()

    assert status["selected_option_id"] == "M17-OPT-1"
    assert status["selected_option_name"] == "Controlled local solver improvement planning"
    assert status["selected_option_value"] == "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING"
    assert status["selected_option_class"] == "CONTROLLED_PLANNING_ONLY"
    assert status["selected_option_review_status"] == "CONFIRMED_PLANNING_ONLY_SELECTION"
    assert status["verdict"] == m.PLANNING_GATE_VERDICT
    assert status["decision"] == m.PLANNING_GATE_DECISION
    assert status["planning_gate_reason"] == m.PLANNING_GATE_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_planning_gate()
    status_b = m.build_controlled_local_solver_improvement_planning_gate()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_planning_gate_is_planning_only() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()

    assert status["controlled_local_solver_improvement_planning_gate_ready"] is True
    assert status["controlled_local_solver_improvement_planning_gate_open"] is True
    assert status["controlled_local_solver_improvement_planning_gate_passed"] is True
    assert status["controlled_local_solver_improvement_planning_gate_closed"] is True
    assert status["planning_authorized"] is True
    assert status["planning_authorization_scope"] == "PLANNING_ONLY"
    assert status["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"


def test_planning_workstreams_are_six_safe_candidates() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()
    workstreams = status["planning_workstreams"]
    ids = [item["workstream_id"] for item in workstreams]

    assert status["planning_workstream_count"] == 6
    assert len(workstreams) == 6
    assert len(ids) == len(set(ids))

    for item in workstreams:
        assert item["status"] == "PLANNING_CANDIDATE"
        assert item["implementation_allowed"] is False
        assert item["runtime_allowed"] is False
        assert item["submission_allowed"] is False


def test_no_implementation_runtime_or_submission_authorized() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()

    assert status["implementation_authorization_granted"] is False
    assert status["implementation_authorized"] is False
    assert status["implementation_blocked"] is True
    assert status["implementation_performed"] is False
    assert status["runtime_solver_patch_allowed"] is False
    assert status["runtime_solver_modified"] is False
    assert status["ranker_runtime_patch_allowed"] is False
    assert status["ranker_runtime_modified"] is False
    assert status["candidate_generator_patch_allowed"] is False
    assert status["candidate_generator_modified"] is False
    assert status["runtime_wiring_allowed"] is False
    assert status["runtime_wiring_performed"] is False
    assert status["runtime_activation_authorized"] is False
    assert status["runtime_execution_allowed"] is False
    assert status["runtime_execution_performed"] is False
    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["upload_performed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_authentication_performed"] is False
    assert status["kaggle_submission_sent"] is False


def test_boundary_and_validation() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()

    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True
    assert status["planning_gate_failure_count"] == 0
    assert status["planning_gate_check_count"] >= 41
    assert m.validate_controlled_local_solver_improvement_planning_gate(status) == []


def test_payload_index_markdown_manifest_are_ready() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate()
    payload = m.planning_gate_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"
    assert m.PLANNING_GATE_STATUS_MARKER in markdown
    assert "selected_option_id=M17-OPT-1" in manifest
    assert "planning_workstream_count=6" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest


def test_write_artifacts(tmp_path, monkeypatch) -> None:
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-planning-gate-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_planning_gate_artifacts()

    assert status["task_name"] == m.TASK_NAME
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-planning-gate-v1.md")
