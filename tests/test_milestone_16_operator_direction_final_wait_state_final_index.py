from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_16_operator_direction_final_wait_state_final_index import (
    DOC_PATH,
    INDEX_DECISION,
    INDEX_REASON,
    INDEX_STATUS_MARKER,
    INDEX_VERDICT,
    INDEXED_STAGES,
    NEXT_STAGE,
    PREVIOUS_STAGE,
    SOURCE_TASK_17_FINAL_BASELINE_COMMIT,
    SOURCE_TASK_17_FINAL_SIGNATURE,
    TASK_MODE,
    TASK_NAME,
    TASK_READY_MARKER,
    TASK_VALID_MARKER,
    build_final_wait_state_final_index,
    build_index_payload,
    build_manifest,
    build_markdown,
    compute_signature,
    final_index_to_dict,
    validate_final_wait_state_final_index,
)


def test_identity_markers_are_canonical() -> None:
    status = build_final_wait_state_final_index()

    assert status.task_name == TASK_NAME
    assert status.task_ready_marker == TASK_READY_MARKER
    assert status.task_valid_marker == TASK_VALID_MARKER
    assert status.index_status_marker == INDEX_STATUS_MARKER
    assert status.task_mode == TASK_MODE


def test_source_binding_is_task_17() -> None:
    status = build_final_wait_state_final_index()

    assert status.source_task_17_final_baseline_commit == SOURCE_TASK_17_FINAL_BASELINE_COMMIT
    assert status.source_task_17_final_signature == SOURCE_TASK_17_FINAL_SIGNATURE
    assert status.previous_stage == PREVIOUS_STAGE
    assert status.next_stage == NEXT_STAGE


def test_verdict_decision_and_reason() -> None:
    status = build_final_wait_state_final_index()

    assert status.verdict == INDEX_VERDICT
    assert status.decision == INDEX_DECISION
    assert status.index_reason == INDEX_REASON


def test_signature_is_deterministic() -> None:
    status_a = build_final_wait_state_final_index()
    status_b = build_final_wait_state_final_index()

    assert status_a.signature == status_b.signature
    assert len(status_a.signature) == 16
    assert status_a.signature == status_a.signature.upper()


def test_signature_changes_with_payload() -> None:
    one = compute_signature({"a": 1})
    two = compute_signature({"a": 2})

    assert one != two
    assert len(one) == 16
    assert len(two) == 16


def test_indexed_stage_count_and_order() -> None:
    status = build_final_wait_state_final_index()

    assert status.indexed_stage_count == 11
    assert status.indexed_stages == INDEXED_STAGES
    assert status.indexed_stages[0].endswith("WAIT_STATE_CLOSURE_V1")
    assert status.indexed_stages[-1].endswith("PACKAGE_CLOSURE_REVIEW_V1")


def test_final_index_is_closed() -> None:
    status = build_final_wait_state_final_index()

    assert status.final_wait_state_package_closure_review_ready is True
    assert status.final_wait_state_package_closure_review_passed is True
    assert status.final_wait_state_package_closure_review_closed is True
    assert status.final_wait_state_final_index_ready is True
    assert status.final_wait_state_final_index_passed is True
    assert status.final_wait_state_final_index_closed is True


def test_wait_state_remains_active_not_closed() -> None:
    status = build_final_wait_state_final_index()

    assert status.wait_state_ready is True
    assert status.wait_state_active is True
    assert status.wait_state_closed is False
    assert status.decision_gate_ready is True
    assert status.decision_gate_open is False
    assert status.decision_gate_blocked is True


def test_operator_direction_is_still_missing() -> None:
    status = build_final_wait_state_final_index()

    assert status.direction_option_count == 5
    assert status.direction_option_selected is False
    assert status.selected_direction_option_id == "NONE"
    assert status.operator_direction_required is True
    assert status.operator_direction_received is False
    assert status.operator_direction_value == "PENDING_EXPLICIT_OPERATOR_DIRECTION"


def test_runtime_and_submission_are_blocked() -> None:
    status = build_final_wait_state_final_index()

    assert status.implementation_blocked is True
    assert status.implementation_performed is False
    assert status.runtime_execution_allowed is False
    assert status.runtime_execution_performed is False
    assert status.real_evaluation_allowed is False
    assert status.real_submission_allowed is False
    assert status.manual_upload_allowed is False
    assert status.kaggle_authentication_performed is False
    assert status.kaggle_submission_sent is False


def test_boundary_flags_are_safe() -> None:
    status = build_final_wait_state_final_index()

    assert status.private_core_exposure is False
    assert status.legal_certification is False
    assert status.fail_closed_required is True
    assert status.fail_closed_active is True
    assert status.index_failure_count == 0
    assert status.index_check_count >= 30


def test_validate_final_index_passes() -> None:
    status = build_final_wait_state_final_index()

    assert validate_final_wait_state_final_index(status) == []


def test_payload_and_index_are_json_ready() -> None:
    status = build_final_wait_state_final_index()
    payload = final_index_to_dict(status)
    index_payload = build_index_payload(status)

    encoded_payload = json.dumps(payload, sort_keys=True)
    encoded_index = json.dumps(index_payload, sort_keys=True)

    assert TASK_NAME in encoded_payload
    assert INDEX_STATUS_MARKER in encoded_index
    assert index_payload["artifact_count"] == 5


def test_markdown_and_manifest_include_markers() -> None:
    status = build_final_wait_state_final_index()
    markdown = build_markdown(status)
    manifest = build_manifest(status)

    assert TASK_NAME in markdown
    assert INDEX_STATUS_MARKER in markdown
    assert INDEX_VERDICT in markdown
    assert TASK_VALID_MARKER in manifest
    assert "indexed_stage_count=11" in manifest
    assert "wait_state_active=True" in manifest
    assert "wait_state_closed=False" in manifest
    assert "implementation_blocked=True" in manifest
    assert "fail_closed_active=True" in manifest


def test_write_final_index_artifacts(tmp_path, monkeypatch) -> None:
    import hbce_arc_agi3.milestone_16_operator_direction_final_wait_state_final_index as module

    artifact_dir = tmp_path / "examples" / "milestone-16" / "operator-direction-final-wait-state-final-index-v1"
    doc_path = tmp_path / "docs" / "milestone-16-operator-direction-final-wait-state-final-index-v1.md"

    monkeypatch.setattr(module, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(module, "DOC_PATH", doc_path)

    status = module.write_final_wait_state_final_index_artifacts()

    assert status.task_name == TASK_NAME
    assert (artifact_dir / "milestone-16-operator-direction-final-wait-state-final-index-v1.json").exists()
    assert (artifact_dir / "milestone-16-operator-direction-final-wait-state-final-index-index-v1.json").exists()
    assert (artifact_dir / "milestone-16-operator-direction-final-wait-state-final-index-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-16-operator-direction-final-wait-state-final-index-v1.md").exists()
    assert doc_path.exists()

    payload = json.loads(
        (artifact_dir / "milestone-16-operator-direction-final-wait-state-final-index-v1.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["task_name"] == TASK_NAME
    assert payload["index_status_marker"] == INDEX_STATUS_MARKER
    assert payload["wait_state_active"] is True
    assert payload["wait_state_closed"] is False
    assert payload["implementation_blocked"] is True


def test_default_doc_path_is_docs_file() -> None:
    assert DOC_PATH == Path("docs/milestone-16-operator-direction-final-wait-state-final-index-v1.md")
