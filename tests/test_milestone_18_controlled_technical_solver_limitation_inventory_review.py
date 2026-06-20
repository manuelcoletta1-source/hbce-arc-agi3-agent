from __future__ import annotations

import json
from pathlib import Path

import hbce_arc_agi3.milestone_18_controlled_technical_solver_limitation_inventory_review as m


def test_identity_and_source_binding() -> None:
    status = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()

    assert status["task_name"] == m.TASK_NAME
    assert status["task_ready_marker"] == m.TASK_READY_MARKER
    assert status["task_valid_marker"] == m.TASK_VALID_MARKER
    assert status["pipeline_ready_marker"] == m.PIPELINE_READY_MARKER
    assert status["review_marker"] == m.REVIEW_MARKER
    assert status["milestone_18_name"] == "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
    assert status["source_task_2_commit"] == "34372a5"
    assert status["source_task_2_signature"] == "15D8A0172179B3EB"
    assert status["source_task_2_stage"] == m.SOURCE_TASK_2_STAGE
    assert status["previous_stage"] == m.SOURCE_TASK_2_STAGE
    assert status["next_stage"] == "MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1"


def test_scope_verdict_decision_and_reason() -> None:
    status = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()

    assert status["review_scope"] == "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_ONLY"
    assert status["milestone_18_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert status["implementation_authorization_scope"] == "NOT_GRANTED"
    assert status["runtime_authorization_scope"] == "NOT_GRANTED"
    assert status["submission_authorization_scope"] == "NOT_GRANTED"
    assert status["verdict"] == m.REVIEW_VERDICT
    assert status["decision"] == "REVIEW_AND_CONFIRM_SOLVER_LIMITATION_INVENTORY_PLAN_ONLY"
    assert status["review_reason"] == m.REVIEW_REASON


def test_signature_is_deterministic() -> None:
    status_a = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()
    status_b = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert all(ch in "0123456789ABCDEF" for ch in status_a["signature"])


def test_review_items_confirm_all_six_limitations() -> None:
    status = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()
    items = status["review_items"]

    assert status["controlled_technical_solver_limitation_inventory_review_ready"] is True
    assert status["controlled_technical_solver_limitation_inventory_review_passed"] is True
    assert status["controlled_technical_solver_limitation_inventory_review_locked"] is True
    assert status["review_only"] is True
    assert status["planning_only"] is True
    assert status["review_count"] == 6
    assert status["blocking_issue_count"] == 0
    assert len(items) == 6

    expected_source_ids = {
        "M18-LIM-1",
        "M18-LIM-2",
        "M18-LIM-3",
        "M18-LIM-4",
        "M18-LIM-5",
        "M18-LIM-6",
    }
    assert {item["source_limitation_id"] for item in items} == expected_source_ids

    expected_areas = {
        "solver coverage",
        "candidate generation",
        "ranker evidence",
        "local diagnostics",
        "submission discipline",
        "authorization boundary",
    }
    assert {item["area"] for item in items} == expected_areas

    for item in items:
        assert item["review_id"]
        assert item["review_status"] == "CONFIRMED"
        assert item["review_note"]
        assert item["blocking_issue"] is False
        assert item["implementation_authorized"] is False


def test_implementation_runtime_submission_and_boundary_are_blocked() -> None:
    status = m.build_milestone_18_controlled_technical_solver_limitation_inventory_review()

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
    artifact_dir = tmp_path / "examples" / "milestone-18" / "controlled-technical-solver-limitation-inventory-review-v1"
    doc_path = tmp_path / "docs" / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md"

    monkeypatch.setattr(m, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(m, "DOC_PATH", doc_path)

    status = m.write_milestone_18_controlled_technical_solver_limitation_inventory_review_artifacts()
    payload = m.review_to_dict(status)
    index_payload = m.build_index_payload(status)
    markdown = m.build_markdown(status)
    manifest = m.build_manifest(status)

    assert status["review_gate_failure_count"] == 0
    assert status["review_gate_count"] >= 68
    assert m.validate_milestone_18_controlled_technical_solver_limitation_inventory_review(status) == []
    assert m.TASK_NAME in json.dumps(payload, sort_keys=True)
    assert index_payload["artifact_count"] == 5
    assert index_payload["milestone_18_name"] == "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"
    assert index_payload["source_task_2_commit"] == "34372a5"
    assert index_payload["source_task_2_signature"] == "15D8A0172179B3EB"
    assert index_payload["review_scope"] == "CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_ONLY"
    assert index_payload["milestone_18_scope"] == "CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT_PLAN_ONLY"
    assert index_payload["review_only"] is True
    assert index_payload["planning_only"] is True
    assert index_payload["review_count"] == 6
    assert index_payload["blocking_issue_count"] == 0
    assert index_payload["implementation_blocked"] is True
    assert index_payload["runtime_execution_allowed"] is False
    assert index_payload["kaggle_submission_sent"] is False
    assert m.REVIEW_MARKER in markdown
    assert "This limitation inventory review authorizes review and planning only." in markdown
    assert "It does not authorize implementation." in markdown
    assert "It does not authorize runtime execution." in markdown
    assert "It does not authorize Kaggle authentication, upload, or submission." in markdown
    assert "review_count=6" in manifest
    assert "blocking_issue_count=0" in manifest
    assert "review_gate_failure_count=0" in manifest
    assert (artifact_dir / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.json").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-limitation-inventory-review-index-v1.json").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-limitation-inventory-review-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md").exists()
    assert doc_path.exists()


def test_default_doc_path() -> None:
    assert m.DOC_PATH == Path("docs/milestone-18-controlled-technical-solver-limitation-inventory-review-v1.md")
