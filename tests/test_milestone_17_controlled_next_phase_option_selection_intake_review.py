from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_17_controlled_next_phase_option_selection_intake_review import (
    DOC_PATH,
    INTAKE_REVIEW_DECISION,
    INTAKE_REVIEW_REASON,
    INTAKE_REVIEW_STATUS_MARKER,
    INTAKE_REVIEW_VERDICT,
    NEXT_STAGE,
    OPERATOR_SELECTION_RAW,
    PREVIOUS_STAGE,
    REVIEWED_OPTIONS,
    SELECTED_OPTION_CLASS,
    SELECTED_OPTION_ID,
    SELECTED_OPTION_NAME,
    SELECTED_OPTION_REVIEW_STATUS,
    SELECTED_OPTION_VALUE,
    SOURCE_TASK_7_FINAL_BASELINE_COMMIT,
    SOURCE_TASK_7_FINAL_SIGNATURE,
    TASK_MODE,
    TASK_NAME,
    TASK_READY_MARKER,
    TASK_VALID_MARKER,
    build_controlled_next_phase_option_selection_intake_review,
    build_index_payload,
    build_manifest,
    build_markdown,
    compute_signature,
    intake_review_to_dict,
    validate_controlled_next_phase_option_selection_intake_review,
)


def test_identity_markers_are_canonical() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["task_name"] == TASK_NAME
    assert status["task_ready_marker"] == TASK_READY_MARKER
    assert status["task_valid_marker"] == TASK_VALID_MARKER
    assert status["intake_review_status_marker"] == INTAKE_REVIEW_STATUS_MARKER
    assert status["task_mode"] == TASK_MODE


def test_source_binding_is_task_17_7() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["source_task_7_final_baseline_commit"] == SOURCE_TASK_7_FINAL_BASELINE_COMMIT
    assert status["source_task_7_final_signature"] == SOURCE_TASK_7_FINAL_SIGNATURE
    assert status["previous_stage"] == PREVIOUS_STAGE
    assert status["next_stage"] == NEXT_STAGE


def test_review_confirms_selected_option_m17_opt_1() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["operator_selection_raw"] == OPERATOR_SELECTION_RAW
    assert status["selected_option_id"] == SELECTED_OPTION_ID
    assert status["selected_option_name"] == SELECTED_OPTION_NAME
    assert status["selected_option_value"] == SELECTED_OPTION_VALUE
    assert status["selected_option_class"] == SELECTED_OPTION_CLASS
    assert status["selected_option_review_status"] == SELECTED_OPTION_REVIEW_STATUS
    assert status["selected_option_count"] == 1
    assert status["selected_option_authorized"] is True
    assert status["selected_option_authorization_scope"] == "PLANNING_ONLY"


def test_verdict_decision_and_reason() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["verdict"] == INTAKE_REVIEW_VERDICT
    assert status["decision"] == INTAKE_REVIEW_DECISION
    assert status["intake_review_reason"] == INTAKE_REVIEW_REASON


def test_signature_is_deterministic() -> None:
    status_a = build_controlled_next_phase_option_selection_intake_review()
    status_b = build_controlled_next_phase_option_selection_intake_review()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"] == status_a["signature"].upper()


def test_signature_changes_with_payload() -> None:
    one = compute_signature({"a": 1})
    two = compute_signature({"a": 2})

    assert one != two
    assert len(one) == 16
    assert len(two) == 16


def test_exactly_one_reviewed_option_is_selected() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()
    selected = [option for option in status["reviewed_options"] if option["selected"] is True]

    assert status["available_option_count"] == 5
    assert tuple(status["reviewed_options"]) == REVIEWED_OPTIONS
    assert len(selected) == 1
    assert selected[0]["option_id"] == "M17-OPT-1"
    assert selected[0]["review_status"] == SELECTED_OPTION_REVIEW_STATUS


def test_non_selected_options_confirmed_not_selected() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    for option in status["reviewed_options"]:
        if option["option_id"] == "M17-OPT-1":
            assert option["selected"] is True
            assert option["selection_received"] is True
        else:
            assert option["selected"] is False
            assert option["selection_received"] is False
            assert option["review_status"] == "CONFIRMED_NOT_SELECTED"


def test_intake_review_closes_but_does_not_authorize_implementation() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["controlled_next_phase_option_selection_intake_review_ready"] is True
    assert status["controlled_next_phase_option_selection_intake_review_passed"] is True
    assert status["controlled_next_phase_option_selection_intake_review_closed"] is True
    assert status["option_selection_received"] is True
    assert status["implementation_authorization_granted"] is False
    assert status["implementation_authorized"] is False
    assert status["implementation_blocked"] is True


def test_no_reviewed_option_authorizes_execution() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    for option in status["reviewed_options"]:
        assert option["stage"] == "PLANNING_ONLY"
        assert option["implementation_allowed"] is False
        assert option["runtime_allowed"] is False
        assert option["submission_allowed"] is False


def test_runtime_and_submission_remain_blocked() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["runtime_solver_patch_allowed"] is False
    assert status["runtime_wiring_allowed"] is False
    assert status["runtime_activation_authorized"] is False
    assert status["runtime_execution_allowed"] is False
    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_submission_sent"] is False


def test_boundary_flags_are_safe() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True
    assert status["intake_review_failure_count"] == 0
    assert status["intake_review_check_count"] >= 37


def test_validate_intake_review_passes() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()

    assert validate_controlled_next_phase_option_selection_intake_review(status) == []


def test_payload_and_index_are_json_ready() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()
    payload = intake_review_to_dict(status)
    index_payload = build_index_payload(status)

    encoded_payload = json.dumps(payload, sort_keys=True)
    encoded_index = json.dumps(index_payload, sort_keys=True)

    assert TASK_NAME in encoded_payload
    assert INTAKE_REVIEW_STATUS_MARKER in encoded_index
    assert index_payload["artifact_count"] == 5
    assert index_payload["selected_option_id"] == "M17-OPT-1"


def test_markdown_and_manifest_include_markers() -> None:
    status = build_controlled_next_phase_option_selection_intake_review()
    markdown = build_markdown(status)
    manifest = build_manifest(status)

    assert TASK_NAME in markdown
    assert INTAKE_REVIEW_STATUS_MARKER in markdown
    assert INTAKE_REVIEW_VERDICT in markdown
    assert TASK_VALID_MARKER in manifest
    assert "selected_option_id=M17-OPT-1" in manifest
    assert "selected_option_count=1" in manifest
    assert "selected_option_authorization_scope=PLANNING_ONLY" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest


def test_write_intake_review_artifacts(tmp_path, monkeypatch) -> None:
    import hbce_arc_agi3.milestone_17_controlled_next_phase_option_selection_intake_review as module

    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-next-phase-option-selection-intake-review-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-next-phase-option-selection-intake-review-v1.md"

    monkeypatch.setattr(module, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(module, "DOC_PATH", doc_path)

    status = module.write_controlled_next_phase_option_selection_intake_review_artifacts()

    assert status["task_name"] == TASK_NAME
    assert (artifact_dir / "milestone-17-controlled-next-phase-option-selection-intake-review-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-option-selection-intake-review-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-option-selection-intake-review-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-option-selection-intake-review-v1.md").exists()
    assert doc_path.exists()

    payload = json.loads(
        (artifact_dir / "milestone-17-controlled-next-phase-option-selection-intake-review-v1.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["task_name"] == TASK_NAME
    assert payload["intake_review_status_marker"] == INTAKE_REVIEW_STATUS_MARKER
    assert payload["selected_option_id"] == "M17-OPT-1"
    assert payload["selected_option_count"] == 1
    assert payload["implementation_blocked"] is True
    assert payload["kaggle_submission_sent"] is False


def test_default_doc_path_is_docs_file() -> None:
    assert DOC_PATH == Path("docs/milestone-17-controlled-next-phase-option-selection-intake-review-v1.md")
