from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_planning_gate_review as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["planning_gate_review_status_marker"] == m.PLANNING_GATE_REVIEW_STATUS_MARKER
    assert status["task_mode"] == m.TASK_MODE
    assert status["source_task_9_final_baseline_commit"] == "3b9b714"
    assert status["source_task_9_final_signature"] == "D4A38C390CDADBA4"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_selected_option_and_review_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status["selected_option_id"] == "M17-OPT-1"
    assert status["selected_option_name"] == "Controlled local solver improvement planning"
    assert status["selected_option_value"] == "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLANNING"
    assert status["selected_option_class"] == "CONTROLLED_PLANNING_ONLY"
    assert status["selected_option_review_status"] == "CONFIRMED_PLANNING_ONLY_SELECTION"
    assert status["verdict"] == m.PLANNING_GATE_REVIEW_VERDICT
    assert status["decision"] == m.PLANNING_GATE_REVIEW_DECISION
    assert status["planning_gate_review_reason"] == m.PLANNING_GATE_REVIEW_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_planning_gate_review()
    status_b = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_planning_gate_review_confirms_planning_only_scope() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"
    assert status["planning_authorized"] is True
    assert status["planning_authorization_scope"] == "PLANNING_ONLY"
    assert status["planning_gate_review_scope"] == "REVIEW_ONLY_CONFIRM_PLANNING_GATE"

    assert status["controlled_local_solver_improvement_planning_gate_ready"] is True
    assert status["controlled_local_solver_improvement_planning_gate_open"] is True
    assert status["controlled_local_solver_improvement_planning_gate_passed"] is True
    assert status["controlled_local_solver_improvement_planning_gate_closed"] is True
    assert status["controlled_local_solver_improvement_planning_gate_review_ready"] is True
    assert status["controlled_local_solver_improvement_planning_gate_review_passed"] is True
    assert status["controlled_local_solver_improvement_planning_gate_review_closed"] is True


def test_reviewed_workstreams_are_six_unique_planning_only_items() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()
    workstreams = status["reviewed_planning_workstreams"]
    ids = [item["workstream_id"] for item in workstreams]

    assert status["planning_workstream_count"] == 6
    assert status["reviewed_planning_workstream_count"] == 6
    assert len(workstreams) == 6
    assert len(ids) == len(set(ids))

    for item in workstreams:
        assert item["source_status"] == "PLANNING_CANDIDATE"
        assert item["status"] == "REVIEWED_PLANNING_CANDIDATE"
        assert item["review_result"].startswith("CONFIRMED_PLANNING_ONLY")
        assert item["implementation_allowed"] is False
        assert item["runtime_allowed"] is False
        assert item["submission_allowed"] is False


def test_implementation_runtime_and_submission_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

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
    assert status["runtime_activation_performed"] is False
    assert status["runtime_execution_allowed"] is False
    assert status["runtime_execution_performed"] is False


def test_evaluation_kaggle_and_boundary_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["upload_performed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_authentication_performed"] is False
    assert status["kaggle_submission_sent"] is False
    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True


def test_validation_passes() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()

    assert status["planning_gate_review_failure_count"] == 0
    assert status["planning_gate_review_check_count"] >= 52
    assert m.validate_controlled_local_solver_improvement_planning_gate_review(status) == []


def test_payload_index_markdown_manifest_are_ready() -> None:
    status = m.build_controlled_local_solver_improvement_planning_gate_review()
    payload = m.planning_gate_review_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"
    assert index_payload["planning_gate_review_scope"] == "REVIEW_ONLY_CONFIRM_PLANNING_GATE"
    assert m.PLANNING_GATE_REVIEW_STATUS_MARKER in markdown
    assert "selected_option_id=M17-OPT-1" in manifest
    assert "reviewed_planning_workstream_count=6" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest


def test_write_artifacts(tmp_path, monkeypatch) -> None:
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-planning-gate-review-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-planning-gate-review-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_planning_gate_review_artifacts()

    assert status["task_name"] == m.TASK_NAME
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-review-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-review-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-review-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-planning-gate-review-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-planning-gate-review-v1.md")
