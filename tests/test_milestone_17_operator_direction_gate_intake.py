from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_17_operator_direction_gate_intake import (
    DOC_PATH,
    INTAKE_DECISION,
    INTAKE_REASON,
    INTAKE_STATUS_MARKER,
    INTAKE_VERDICT,
    NEXT_STAGE,
    OPERATOR_DIRECTION_CLASS,
    OPERATOR_DIRECTION_RAW,
    OPERATOR_DIRECTION_VALUE,
    PREVIOUS_STAGE,
    SOURCE_TASK_31_FINAL_BASELINE_COMMIT,
    SOURCE_TASK_31_FINAL_SIGNATURE,
    TASK_MODE,
    TASK_NAME,
    TASK_READY_MARKER,
    TASK_VALID_MARKER,
    build_index_payload,
    build_manifest,
    build_markdown,
    build_operator_direction_gate_intake,
    compute_signature,
    intake_to_dict,
    validate_operator_direction_gate_intake,
)


def test_identity_markers_are_canonical() -> None:
    status = build_operator_direction_gate_intake()

    assert status["task_name"] == TASK_NAME
    assert status["task_ready_marker"] == TASK_READY_MARKER
    assert status["task_valid_marker"] == TASK_VALID_MARKER
    assert status["intake_status_marker"] == INTAKE_STATUS_MARKER
    assert status["task_mode"] == TASK_MODE


def test_source_binding_is_task_31() -> None:
    status = build_operator_direction_gate_intake()

    assert status["source_task_31_final_baseline_commit"] == SOURCE_TASK_31_FINAL_BASELINE_COMMIT
    assert status["source_task_31_final_signature"] == SOURCE_TASK_31_FINAL_SIGNATURE
    assert status["previous_stage"] == PREVIOUS_STAGE
    assert status["next_stage"] == NEXT_STAGE


def test_operator_direction_is_recorded_and_normalized() -> None:
    status = build_operator_direction_gate_intake()

    assert status["operator_direction_raw"] == OPERATOR_DIRECTION_RAW
    assert status["operator_direction_value"] == OPERATOR_DIRECTION_VALUE
    assert status["operator_direction_class"] == OPERATOR_DIRECTION_CLASS
    assert status["operator_direction_required"] is True
    assert status["operator_direction_received"] is True
    assert status["operator_direction_accepted"] is True


def test_verdict_decision_and_reason() -> None:
    status = build_operator_direction_gate_intake()

    assert status["verdict"] == INTAKE_VERDICT
    assert status["decision"] == INTAKE_DECISION
    assert status["intake_reason"] == INTAKE_REASON


def test_signature_is_deterministic() -> None:
    status_a = build_operator_direction_gate_intake()
    status_b = build_operator_direction_gate_intake()

    assert status_a["signature"] == status_b["signature"]
    assert len(status_a["signature"]) == 16
    assert status_a["signature"] == status_a["signature"].upper()


def test_signature_changes_with_payload() -> None:
    one = compute_signature({"a": 1})
    two = compute_signature({"a": 2})

    assert one != two
    assert len(one) == 16
    assert len(two) == 16


def test_controlled_planning_opens_without_runtime() -> None:
    status = build_operator_direction_gate_intake()

    assert status["controlled_next_phase_planning_opened"] is True
    assert status["implementation_authorization_granted"] is False
    assert status["implementation_authorized"] is False
    assert status["implementation_blocked"] is True
    assert status["implementation_performed"] is False
    assert status["runtime_execution_allowed"] is False
    assert status["runtime_execution_performed"] is False


def test_submission_and_kaggle_remain_blocked() -> None:
    status = build_operator_direction_gate_intake()

    assert status["real_evaluation_allowed"] is False
    assert status["real_submission_allowed"] is False
    assert status["manual_upload_allowed"] is False
    assert status["upload_performed"] is False
    assert status["kaggle_authentication_allowed"] is False
    assert status["kaggle_authentication_performed"] is False
    assert status["kaggle_submission_sent"] is False


def test_boundary_flags_are_safe() -> None:
    status = build_operator_direction_gate_intake()

    assert status["private_core_exposure"] is False
    assert status["legal_certification"] is False
    assert status["fail_closed_required"] is True
    assert status["fail_closed_active"] is True
    assert status["intake_failure_count"] == 0
    assert status["intake_check_count"] >= 22


def test_validate_operator_direction_gate_intake_passes() -> None:
    status = build_operator_direction_gate_intake()

    assert validate_operator_direction_gate_intake(status) == []


def test_payload_and_index_are_json_ready() -> None:
    status = build_operator_direction_gate_intake()
    payload = intake_to_dict(status)
    index_payload = build_index_payload(status)

    encoded_payload = json.dumps(payload, sort_keys=True)
    encoded_index = json.dumps(index_payload, sort_keys=True)

    assert TASK_NAME in encoded_payload
    assert INTAKE_STATUS_MARKER in encoded_index
    assert index_payload["artifact_count"] == 5


def test_markdown_and_manifest_include_markers() -> None:
    status = build_operator_direction_gate_intake()
    markdown = build_markdown(status)
    manifest = build_manifest(status)

    assert TASK_NAME in markdown
    assert INTAKE_STATUS_MARKER in markdown
    assert INTAKE_VERDICT in markdown
    assert TASK_VALID_MARKER in manifest
    assert "operator_direction_received=True" in manifest
    assert "controlled_next_phase_planning_opened=True" in manifest
    assert "implementation_blocked=True" in manifest
    assert "runtime_execution_allowed=False" in manifest
    assert "kaggle_submission_sent=False" in manifest
    assert "fail_closed_active=True" in manifest


def test_write_operator_direction_gate_intake_artifacts(tmp_path, monkeypatch) -> None:
    import hbce_arc_agi3.milestone_17_operator_direction_gate_intake as module

    artifact_dir = tmp_path / "examples" / "milestone-17" / "operator-direction-gate-intake-v1"
    doc_path = tmp_path / "docs" / "milestone-17-operator-direction-gate-intake-v1.md"

    monkeypatch.setattr(module, "ARTIFACT_DIR", artifact_dir)
    monkeypatch.setattr(module, "DOC_PATH", doc_path)

    status = module.write_operator_direction_gate_intake_artifacts()

    assert status["task_name"] == TASK_NAME
    assert (artifact_dir / "milestone-17-operator-direction-gate-intake-v1.json").exists()
    assert (artifact_dir / "milestone-17-operator-direction-gate-intake-index-v1.json").exists()
    assert (artifact_dir / "milestone-17-operator-direction-gate-intake-manifest-v1.txt").exists()
    assert (artifact_dir / "milestone-17-operator-direction-gate-intake-v1.md").exists()
    assert doc_path.exists()

    payload = json.loads(
        (artifact_dir / "milestone-17-operator-direction-gate-intake-v1.json").read_text(
            encoding="utf-8"
        )
    )

    assert payload["task_name"] == TASK_NAME
    assert payload["intake_status_marker"] == INTAKE_STATUS_MARKER
    assert payload["operator_direction_received"] is True
    assert payload["implementation_blocked"] is True
    assert payload["kaggle_submission_sent"] is False


def test_default_doc_path_is_docs_file() -> None:
    assert DOC_PATH == Path("docs/milestone-17-operator-direction-gate-intake-v1.md")
