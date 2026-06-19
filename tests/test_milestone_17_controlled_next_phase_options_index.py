from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_17_controlled_next_phase_options_index import (
    CONTROLLED_OPTIONS,
    DOC_PATH,
    NEXT_STAGE,
    OPERATOR_DIRECTION_CLASS,
    OPERATOR_DIRECTION_VALUE,
    OPTIONS_INDEX_DECISION,
    OPTIONS_INDEX_REASON,
    OPTIONS_INDEX_STATUS_MARKER,
    OPTIONS_INDEX_VERDICT,
    PREVIOUS_STAGE,
    SOURCE_TASK_1_FINAL_BASELINE_COMMIT,
    SOURCE_TASK_1_FINAL_SIGNATURE,
    TASK_MODE,
    TASK_NAME,
    TASK_READY_MARKER,
    TASK_VALID_MARKER,
    build_controlled_next_phase_options_index,
    build_index_payload,
    build_manifest,
    build_markdown,
    compute_signature,
    options_index_to_dict,
    validate_controlled_next_phase_options_index,
)


def test_identity_markers_are_canonical() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["task_name"] == TASK_NAME
    assert status["task_ready_marker"] == TASK_READY_MARKER
    assert status["task_valid_marker"] == TASK_VALID_MARKER
    assert status["options_index_status_marker"] == OPTIONS_INDEX_STATUS_MARKER
    assert status["task_mode"] == TASK_MODE


def test_source_binding_is_task_17_1() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["source_task_1_final_baseline_commit"] == SOURCE_TASK_1_FINAL_BASELINE_COMMIT
    assert status["source_task_1_final_signature"] == SOURCE_TASK_1_FINAL_SIGNATURE
    assert status["previous_stage"] == PREVIOUS_STAGE
    assert status["next_stage"] == NEXT_STAGE


def test_operator_direction_is_controlled_planning_only() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["operator_direction_value"] == OPERATOR_DIRECTION_VALUE
    assert status["operator_direction_class"] == OPERATOR_DIRECTION_CLASS
    assert status["operator_direction_received"] is True
    assert status["controlled_next_phase_planning_opened"] is True


def test_verdict_decision_and_reason() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["verdict"] == OPTIONS_INDEX_VERDICT
    assert status["decision"] == OPTIONS_INDEX_DECISION
    assert status["options_index_reason"] == OPTIONS_INDEX_REASON


def test_signature_is_deterministic() -> None:
    status_a = build_controlled_next_phase_options_index()
    status_b = build_controlled_next_phase_options_index()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"] == status_a["signature"].upper()


def test_signature_changes_with_payload() -> None:
    one = compute_signature({"a": 1})
    two = compute_signature({"a": 2})

    assert one != two
    assert len(one) == 16
    assert len(two) == 16


def test_controlled_options_are_five_unique_planning_options() -> None:
    status = build_controlled_next_phase_options_index()
    option_ids = [option["option_id"] for option in status["controlled_options"]]

    assert status["controlled_option_count"] == 5
    assert tuple(status["controlled_options"]) == CONTROLLED_OPTIONS
    assert len(option_ids) == len(set(option_ids))
    assert status["selected_option_id"] == "NONE"
    assert status["selected_option_count"] == 0


def test_no_option_authorizes_implementation_runtime_or_submission() -> None:
    status = build_controlled_next_phase_options_index()

    for option in status["controlled_options"]:
        assert option["stage"] == "PLANNING_ONLY"
        assert option["implementation_allowed"] is False
        assert option["runtime_allowed"] is False
        assert option["submission_allowed"] is False


def test_options_index_is_closed_but_execution_is_blocked() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["controlled_next_phase_options_index_ready"] is True
    assert status["controlled_next_phase_options_index_passed"] is True
    assert status["controlled_next_phase_options_index_closed"] is True
    assert status["implementation_authorization_granted"] is False
    assert status["implementation_authorized"] is False
    assert status["implementation_blocked"] is True
    assert status["runtime_execution_allowed"] is False


def test_submission_and_kaggle_remain_blocked() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["upload_performed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_authentication_performed"] is False
    assert status["kaggle_submission_sent"] is False


def test_boundary_flags_are_safe() -> None:
    status = build_controlled_next_phase_options_index()

    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True
    assert status["options_index_failure_count"] == 0
    assert status["options_index_check_count"] >= 29


def test_validate_options_index_passes() -> None:
    status = build_controlled_next_phase_options_index()

    assert validate_controlled_next_phase_options_index(status) == []


def test_payload_and_index_are_json_ready() -> None:
    status = build_controlled_next_phase_options_index()
    payload = options_index_to_dict(status)
    index_payload = build_index_payload(status)

    encoded_payload = json.dumps(payload, sort_keys=True)
    encoded_index = json.dumps(index_payload, sort_keys=True)

    assert TASK_NAME in encoded_payload
    assert OPTIONS_INDEX_STATUS_MARKER in encoded_index
    assert index_payload["artifact_count"] == 5


def test_markdown_and_manifest_include_markers() -> None:
    status = build_controlled_next_phase_options_index()
    markdown = build_markdown(status)
    manifest = build_manifest(status)

    assert TASK_NAME in markdown
    assert OPTIONS_INDEX_STATUS_MARKER in markdown
    assert OPTIONS_INDEX_VERDICT in markdown
    assert TASK_VALID_MARKER in manifest
    assert "controlled_option_count=5" in manifest
    assert "selected_option_id=NONE" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "fail_closed_active=True" in manifest


def test_write_options_index_artifacts(tmp_path, monkeypatch) -> None:
    import hbce_arc_agi3.milestone_17_controlled_next_phase_options_index as module

    artifact_dir = tmp_path / "examples" / "milestone-17" / "controlled-next-phase-options-index-v1"
    doc_path = tmp_path / "docs" / "milestone-17-controlled-next-phase-options-index-v1.md"

    monkeypatch.setattr(module, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(module, "DOC_PATH", doc_path)

    status = module.write_controlled_next_phase_options_index_artifacts()

    assert status["task_name"] == TASK_NAME
    assert (artifact_dir / "milestone-17-controlled-next-phase-options-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-options-index-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-options-index-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-controlled-next-phase-options-index-v1.md").exists()
    assert doc_path.exists()

    payload = json.loads(
        (artifact_dir / "milestone-17-controlled-next-phase-options-index-v1.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["task_name"] == TASK_NAME
    assert payload["options_index_status_marker"] == OPTIONS_INDEX_STATUS_MARKER
    assert payload["controlled_option_count"] == 5
    assert payload["implementation_blocked"] is True
    assert payload["kaggle_submission_sent"] is False


def test_default_doc_path_is_docs_file() -> None:
    assert DOC_PATH == Path("docs/milestone-17-controlled-next-phase-options-index-v1.md")
