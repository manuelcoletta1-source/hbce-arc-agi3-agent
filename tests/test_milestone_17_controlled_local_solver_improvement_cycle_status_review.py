from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_cycle_status_review as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["cycle_status_review_status_marker"] == m.CYCLE_STATUS_REVIEW_STATUS_MARKER
    assert status["source_task_13_final_baseline_commit"] == "e3b6528"
    assert status["source_task_13_final_signature"] == "D992AEA3A992CA7F"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_cycle_status_scope_and_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()

    assert status["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"
    assert status["plan_scope"] == "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert status["plan_review_scope"] == "REVIEW_ONLY_CONFIRM_PLAN"
    assert status["closure_scope"] == "CLOSE_PLAN_AND_REVIEW_CYCLE_ONLY"
    assert status["cycle_status_review_scope"] == "STATUS_REVIEW_ONLY"
    assert status["plan_authorization_scope"] == "PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.CYCLE_STATUS_REVIEW_VERDICT
    assert status["decision"] == m.CYCLE_STATUS_REVIEW_DECISION
    assert status["cycle_status_review_reason"] == m.CYCLE_STATUS_REVIEW_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_cycle_status_review()
    status_b = m.build_controlled_local_solver_improvement_cycle_status_review()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_cycle_stages_are_three_closed_non_executing_stages() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()
    stages = status["cycle_stages"]
    ids = [stage["stage_id"] for stage in stages]

    assert status["cycle_stage_count"] == 3
    assert status["closed_cycle_stage_count"] == 3
    assert len(stages) == 3
    assert len(ids) == len(set(ids))

    for stage in stages:
        assert stage["status"] == "CLOSED"
        assert stage["commit"]
        assert stage["signature"]
        assert stage["implementation_authorized"] is False
        assert stage["runtime_execution_allowed"] is False
        assert stage["submission_allowed"] is False


def test_cycle_status_flags_are_ready_passed_locked() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()

    assert status["controlled_local_solver_improvement_plan_closed"] is True
    assert status["controlled_local_solver_improvement_plan_review_closed"] is True
    assert status["controlled_local_solver_improvement_plan_closure_closed"] is True
    assert status["controlled_local_solver_improvement_cycle_status_review_ready"] is True
    assert status["controlled_local_solver_improvement_cycle_status_review_passed"] is True
    assert status["controlled_local_solver_improvement_cycle_status_review_locked"] is True


def test_implementation_runtime_and_submission_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()

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


def test_evaluation_kaggle_score_claims_and_boundary_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_cycle_status_review()

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
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-cycle-status-review-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-cycle-status-review-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_cycle_status_review_artifacts()
    payload = m.cycle_status_review_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["cycle_status_review_gate_failure_count"] == 0
    assert status["cycle_status_review_gate_count"] >= 53
    assert m.validate_controlled_local_solver_improvement_cycle_status_review(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["cycle_status_review_scope"] == "STATUS_REVIEW_ONLY"
    assert m.CYCLE_STATUS_REVIEW_STATUS_MARKER in markdown
    assert "cycle_stage_count=3" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "official_score_claim_allowed=False" in manifest
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-cycle-status-review-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-cycle-status-review-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-cycle-status-review-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-cycle-status-review-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-cycle-status-review-v1.md")
