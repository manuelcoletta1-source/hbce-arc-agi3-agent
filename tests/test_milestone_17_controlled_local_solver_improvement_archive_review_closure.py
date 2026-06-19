from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_archive_review_closure as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_archive_review_closure()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["archive_review_closure_marker"] == m.ARCHIVE_REVIEW_CLOSURE_MARKER
    assert status["source_task_17_final_baseline_commit"] == "879ad75"
    assert status["source_task_17_final_signature"] == "B66AA97FFE0C8BD8"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_archive_review_closure_scope_and_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_archive_review_closure()

    assert status["final_cycle_archive_scope"] == "ARCHIVE_CLOSED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_ONLY"
    assert status["archive_review_scope"] == "REVIEW_FINAL_ARCHIVE_ONLY"
    assert status["archive_review_closure_scope"] == "CLOSE_ARCHIVE_REVIEW_ONLY"
    assert status["plan_authorization_scope"] == "PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.ARCHIVE_REVIEW_CLOSURE_VERDICT
    assert status["decision"] == m.ARCHIVE_REVIEW_CLOSURE_DECISION
    assert status["archive_review_closure_reason"] == m.ARCHIVE_REVIEW_CLOSURE_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_archive_review_closure()
    status_b = m.build_controlled_local_solver_improvement_archive_review_closure()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_closed_review_stages_are_seven_closed_non_executing_stages() -> None:
    status = m.build_controlled_local_solver_improvement_archive_review_closure()
    stages = status["closed_review_stages"]
    ids = [stage["stage_id"] for stage in stages]

    assert status["closed_review_stage_count"] == 7
    assert len(stages) == 7
    assert len(ids) == len(set(ids))

    expected_tasks = {
        "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1",
        "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1",
        "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1",
        "MILESTONE_17_TASK_14_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_V1",
        "MILESTONE_17_TASK_15_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_CLOSURE_V1",
        "MILESTONE_17_TASK_16_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_ARCHIVE_V1",
        "MILESTONE_17_TASK_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_V1",
    }

    assert {stage["task"] for stage in stages} == expected_tasks

    for stage in stages:
        assert stage["closure_status"]
        assert stage["commit"]
        assert stage["signature"]
        assert stage["implementation_authorized"] is False
        assert stage["runtime_execution_allowed"] is False
        assert stage["submission_allowed"] is False


def test_archive_review_closure_flags_are_ready_passed_locked() -> None:
    status = m.build_controlled_local_solver_improvement_archive_review_closure()

    assert status["controlled_local_solver_improvement_archive_review_closed"] is True
    assert status["controlled_local_solver_improvement_archive_review_closure_ready"] is True
    assert status["controlled_local_solver_improvement_archive_review_closure_passed"] is True
    assert status["controlled_local_solver_improvement_archive_review_closure_locked"] is True


def test_implementation_runtime_and_submission_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_archive_review_closure()

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
    status = m.build_controlled_local_solver_improvement_archive_review_closure()

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
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-archive-review-closure-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-archive-review-closure-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_archive_review_closure_artifacts()
    payload = m.archive_review_closure_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["archive_review_closure_gate_failure_count"] == 0
    assert status["archive_review_closure_gate_count"] >= 48
    assert m.validate_controlled_local_solver_improvement_archive_review_closure(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["archive_review_closure_scope"] == "CLOSE_ARCHIVE_REVIEW_ONLY"
    assert m.ARCHIVE_REVIEW_CLOSURE_MARKER in markdown
    assert "closed_review_stage_count=7" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "official_score_claim_allowed=False" in manifest
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-archive-review-closure-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-archive-review-closure-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-archive-review-closure-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-archive-review-closure-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-archive-review-closure-v1.md")
