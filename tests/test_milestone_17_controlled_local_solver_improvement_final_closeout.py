from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_final_closeout as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["pipeline_ready_marker"] == m.PIPELINE_READY_MARKER
    assert status["final_closeout_marker"] == m.FINAL_CLOSEOUT_MARKER
    assert status["source_task_24_final_baseline_commit"] == "a504ef8"
    assert status["source_task_24_final_signature"] == "CE3EDC58EE745A70"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_final_closeout_scope_and_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()

    assert status["final_closeout_scope"] == "CLOSE_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_ONLY"
    assert status["final_archive_index_review_closure_scope"] == "CLOSE_FINAL_ARCHIVE_INDEX_REVIEW_ONLY"
    assert status["plan_authorization_scope"] == "PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.FINAL_CLOSEOUT_VERDICT
    assert status["decision"] == m.FINAL_CLOSEOUT_DECISION
    assert status["final_closeout_reason"] == m.FINAL_CLOSEOUT_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_final_closeout()
    status_b = m.build_controlled_local_solver_improvement_final_closeout()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_closed_final_closeout_stages_are_fourteen_non_executing_stages() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()
    stages = status["closed_final_closeout_stages"]
    ids = [stage["stage_id"] for stage in stages]

    assert status["closed_final_closeout_stage_count"] == 14
    assert len(stages) == 14
    assert len(ids) == len(set(ids))

    expected_tasks = {
        "MILESTONE_17_TASK_11_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_V1",
        "MILESTONE_17_TASK_12_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_REVIEW_V1",
        "MILESTONE_17_TASK_13_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_CLOSURE_V1",
        "MILESTONE_17_TASK_14_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_V1",
        "MILESTONE_17_TASK_15_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_CYCLE_STATUS_REVIEW_CLOSURE_V1",
        "MILESTONE_17_TASK_16_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_ARCHIVE_V1",
        "MILESTONE_17_TASK_17_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_V1",
        "MILESTONE_17_TASK_18_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_ARCHIVE_REVIEW_CLOSURE_V1",
        "MILESTONE_17_TASK_19_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_V1",
        "MILESTONE_17_TASK_20_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_V1",
        "MILESTONE_17_TASK_21_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_CYCLE_CLOSURE_REVIEW_CLOSURE_V1",
        "MILESTONE_17_TASK_22_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_V1",
        "MILESTONE_17_TASK_23_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_REVIEW_V1",
        "MILESTONE_17_TASK_24_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_FINAL_ARCHIVE_INDEX_REVIEW_CLOSURE_V1",
    }

    assert {stage["task"] for stage in stages} == expected_tasks

    for stage in stages:
        assert stage["closeout_status"]
        assert stage["commit"]
        assert stage["signature"]
        assert stage["implementation_authorized"] is False
        assert stage["runtime_execution_allowed"] is False
        assert stage["submission_allowed"] is False


def test_final_closeout_flags_are_ready_passed_locked_and_closed() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()

    assert status["controlled_local_solver_improvement_final_closeout_ready"] is True
    assert status["controlled_local_solver_improvement_final_closeout_passed"] is True
    assert status["controlled_local_solver_improvement_final_closeout_locked"] is True
    assert status["milestone_17_closed"] is True
    assert status["controlled_local_solver_improvement_cycle_closed"] is True


def test_implementation_runtime_and_submission_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()

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


def test_evaluation_kaggle_score_claims_and_boundary_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_final_closeout()

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
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-final-closeout-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-final-closeout-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_final_closeout_artifacts()
    payload = m.final_closeout_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["final_closeout_gate_failure_count"] == 0
    assert status["final_closeout_gate_count"] >= 49
    assert m.validate_controlled_local_solver_improvement_final_closeout(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["final_closeout_scope"] == "CLOSE_FULL_CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_MILESTONE_17_ONLY"
    assert index_payload["milestone_17_closed"] is True
    assert index_payload["controlled_local_solver_improvement_cycle_closed"] is True
    assert m.FINAL_CLOSEOUT_MARKER in markdown
    assert "closed_final_closeout_stage_count=14" in manifest
    assert "milestone_17_closed=True" in manifest
    assert "controlled_local_solver_improvement_cycle_closed=True" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "official_score_claim_allowed=False" in manifest
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-final-closeout-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-final-closeout-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-final-closeout-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-final-closeout-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-final-closeout-v1.md")
