from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_milestone_17_final_project_final_record_review as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["pipeline_ready_marker"] == m.PIPELINE_READY_MARKER
    assert status["final_project_final_record_review_marker"] == m.FINAL_PROJECT_FINAL_RECORD_REVIEW_MARKER
    assert status["source_task_55_final_baseline_commit"] == "876f5d2"
    assert status["source_task_55_final_signature"] == "BC63EDB93B00033A"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_record_review_scope_verdict_and_decision() -> None:
    status = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()

    assert status["final_project_final_record_scope"] == "FINAL_PROJECT_FINAL_RECORD_ONLY"
    assert status["final_project_final_record_review_scope"] == "REVIEW_FINAL_PROJECT_FINAL_RECORD_ONLY"
    assert status["final_project_final_closure_scope"] == "FINAL_PROJECT_FINAL_CLOSURE_ONLY"
    assert status["final_project_final_closure_review_scope"] == "REVIEW_FINAL_PROJECT_FINAL_CLOSURE_ONLY"
    assert status["final_project_final_closure_review_closure_scope"] == "CLOSE_FINAL_PROJECT_FINAL_CLOSURE_REVIEW_ONLY"
    assert status["final_project_final_index_scope"] == "FINAL_PROJECT_FINAL_INDEX_ONLY"
    assert status["final_project_final_index_review_scope"] == "REVIEW_FINAL_PROJECT_FINAL_INDEX_ONLY"
    assert status["final_project_final_index_review_closure_scope"] == "CLOSE_FINAL_PROJECT_FINAL_INDEX_REVIEW_ONLY"
    assert status["plan_authorization_scope"] == "PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.FINAL_PROJECT_FINAL_RECORD_REVIEW_VERDICT
    assert status["decision"] == m.FINAL_PROJECT_FINAL_RECORD_REVIEW_DECISION
    assert status["final_project_final_record_review_reason"] == m.FINAL_PROJECT_FINAL_RECORD_REVIEW_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()
    status_b = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert all(ch in "0123456789ABCDEF" for ch in status_a["signature"])


def test_reviewed_final_project_final_record_stages_are_forty_five_non_executing_stages() -> None:
    status = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()
    stages = status["reviewed_final_project_final_record_stages"]
    ids = [stage["stage_id"] for stage in stages]

    assert status["reviewed_final_project_final_record_stage_count"] == 45
    assert len(stages) == 45
    assert len(ids) == len(set(ids))
    assert stages[-1]["task"] == m.PREVIOUS_STAGE
    assert stages[-1]["commit"] == "876f5d2"
    assert stages[-1]["signature"] == "BC63EDB93B00033A"
    assert stages[-1]["review_status"] == "FINAL_PROJECT_FINAL_RECORD_REVIEW_CONFIRMED"

    for stage in stages:
        assert stage["review_status"]
        assert stage["commit"]
        assert stage["signature"]
        assert stage["implementation_authorized"] is False
        assert stage["runtime_execution_allowed"] is False
        assert stage["submission_allowed"] is False


def test_record_review_flags_are_ready_passed_locked_and_reviewed() -> None:
    status = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()

    assert status["controlled_local_solver_improvement_milestone_17_final_project_final_record_review_ready"] is True
    assert status["controlled_local_solver_improvement_milestone_17_final_project_final_record_review_passed"] is True
    assert status["controlled_local_solver_improvement_milestone_17_final_project_final_record_review_locked"] is True
    assert status["milestone_17_final_project_final_record_reviewed"] is True
    assert status["controlled_local_solver_improvement_milestone_17_project_final_record_reviewed"] is True


def test_implementation_runtime_submission_and_boundary_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_milestone_17_final_project_final_record_review()

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


def test_validation_payload_and_artifacts(tmp_path, monkeypatch) -> None:
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-milestone-17-final-project-final-record-review-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_milestone_17_final_project_final_record_review_artifacts()
    payload = m.final_project_final_record_review_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["final_project_final_record_review_gate_failure_count"] == 0
    assert status["final_project_final_record_review_gate_count"] >= 76
    assert m.validate_controlled_local_solver_improvement_milestone_17_final_project_final_record_review(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["final_project_final_record_review_scope"] == "REVIEW_FINAL_PROJECT_FINAL_RECORD_ONLY"
    assert index_payload["milestone_17_final_project_final_record_reviewed"] is True
    assert index_payload["controlled_local_solver_improvement_milestone_17_project_final_record_reviewed"] is True
    assert m.FINAL_PROJECT_FINAL_RECORD_REVIEW_MARKER in markdown
    assert "reviewed_final_project_final_record_stage_count=45" in manifest
    assert "milestone_17_final_project_final_record_reviewed=True" in manifest
    assert "controlled_local_solver_improvement_milestone_17_project_final_record_reviewed=True" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "official_score_claim_allowed=False" in manifest
    assert "No implementation authorization is granted." in markdown
    assert "No Kaggle submission is authorized." in markdown
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-milestone-17-final-project-final-record-review-v1.md")
