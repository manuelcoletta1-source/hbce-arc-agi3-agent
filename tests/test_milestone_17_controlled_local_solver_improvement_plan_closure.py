from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_17_controlled_local_solver_improvement_plan_closure as m


def test_identity_and_source_binding() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["closure_status_marker"] == m.CLOSURE_STATUS_MARKER
    assert status["source_task_12_final_baseline_commit"] == "ee29733"
    assert status["source_task_12_final_signature"] == "B83CF1D86F83BDE8"
    assert status["previous_stage"] == m.PREVIOUS_STAGE
    assert status["next_stage"] == m.NEXT_STAGE


def test_closure_scope_and_verdict() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()

    assert status["planning_scope"] == "LOCAL_SOLVER_IMPROVEMENT_ONLY"
    assert status["plan_scope"] == "CONTROLLED_LOCAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert status["plan_review_scope"] == "REVIEW_ONLY_CONFIRM_PLAN"
    assert status["closure_scope"] == "CLOSE_PLAN_AND_REVIEW_CYCLE_ONLY"
    assert status["plan_authorization_scope"] == "PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.CLOSURE_VERDICT
    assert status["decision"] == m.CLOSURE_DECISION
    assert status["closure_reason"] == m.CLOSURE_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_controlled_local_solver_improvement_plan_closure()
    status_b = m.build_controlled_local_solver_improvement_plan_closure()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"].isupper()


def test_closed_plan_items_are_six_unique_non_executing_items() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()
    items = status["closed_plan_items"]
    ids = [item["plan_item_id"] for item in items]

    assert status["plan_item_count"] == 6
    assert status["closed_plan_item_count"] == 6
    assert len(items) == 6
    assert len(ids) == len(set(ids))

    for item in items:
        assert item["workstream_id"].startswith("M17-LSIG-WS-")
        assert item["closure_result"].startswith("CLOSED_PLAN_CONFIRMED")
        assert item["implementation_allowed"] is False
        assert item["runtime_allowed"] is False
        assert item["submission_allowed"] is False


def test_closure_flags_are_closed_ready_passed_locked() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()

    assert status["controlled_local_solver_improvement_plan_closed"] is True
    assert status["controlled_local_solver_improvement_plan_review_closed"] is True
    assert status["controlled_local_solver_improvement_plan_closure_ready"] is True
    assert status["controlled_local_solver_improvement_plan_closure_passed"] is True
    assert status["controlled_local_solver_improvement_plan_closure_locked"] is True


def test_implementation_runtime_and_submission_are_blocked() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()

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
    status = m.build_controlled_local_solver_improvement_plan_closure()

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


def test_validation_passes() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()

    assert status["closure_gate_failure_count"] == 0
    assert status["closure_gate_count"] >= 49
    assert m.validate_controlled_local_solver_improvement_plan_closure(status) == []


def test_payload_index_markdown_manifest_are_ready() -> None:
    status = m.build_controlled_local_solver_improvement_plan_closure()
    payload = m.closure_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["closure_scope"] == "CLOSE_PLAN_AND_REVIEW_CYCLE_ONLY"
    assert m.CLOSURE_STATUS_MARKER in markdown
    assert "closed_plan_item_count=6" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "official_score_claim_allowed=False" in manifest


def test_write_artifacts(tmp_path, monkeypatch) -> None:
    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-local-solver-improvement-plan-closure-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_controlled_local_solver_improvement_plan_closure_artifacts()

    assert status["task_name"] == m.TASK_NAME
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-plan-closure-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-plan-closure-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-local-solver-improvement-plan-closure-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-17-controlled-local-solver-improvement-plan-closure-v1.md")
