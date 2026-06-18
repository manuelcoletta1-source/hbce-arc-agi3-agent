from __future__ import annotations

import json

from hbce_arc_agi3.qiv_runtime_constraints import (
    NEXT_STAGE,
    PREVIOUS_STAGE,
    QIV_LINK_VALID,
    QIV_REQUIRED_FIELDS,
    build_example_qiv_runtime_constraint_record,
    build_qiv_runtime_constraint_link,
    validate_qiv_runtime_constraint_link,
    validate_qiv_runtime_constraint_record,
    write_qiv_runtime_constraint_link_artifacts,
)


def test_qiv_example_record_is_complete() -> None:
    record = build_example_qiv_runtime_constraint_record()
    validation = validate_qiv_runtime_constraint_record(record)

    assert validation.valid is True
    assert validation.status == QIV_LINK_VALID
    assert validation.issue_count == 0


def test_qiv_required_field_count_matches_v2_4_operational_completeness() -> None:
    assert len(QIV_REQUIRED_FIELDS) == 17


def test_qiv_link_is_valid() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")
    validation = validate_qiv_runtime_constraint_link(link)

    assert validation.valid is True
    assert validation.status == QIV_LINK_VALID
    assert validation.issue_count == 0


def test_qiv_link_connects_after_task_8_and_before_task_9() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert link.previous_stage == PREVIOUS_STAGE
    assert link.next_stage == NEXT_STAGE
    assert "TASK_8" in link.previous_stage
    assert "TASK_9" in link.next_stage


def test_qiv_engine_map_has_four_blocks() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert set(link.qiv_engine_map) == {"QEngine", "CEngine", "IEngine", "ProofEngine"}


def test_qiv_is_not_solver_direct_and_does_not_authorize_runtime() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert link.qiv_is_solver_direct is False
    assert link.qiv_changes_runtime_solver is False
    assert link.qiv_authorizes_implementation is False
    assert link.qiv_overrides_operator_gate is False
    assert link.runtime_activation_performed is False
    assert link.implementation_performed is False
    assert link.real_submission_allowed is False


def test_qiv_links_to_training_runtime_audit_and_fail_closed() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert link.qiv_linked_to_programming is True
    assert link.qiv_linked_to_training is True
    assert link.qiv_linked_to_runtime_audit is True
    assert link.qiv_linked_to_fail_closed is True
    assert link.qiv_linked_to_arc_agi3_diagnostics is True


def test_qiv_public_boundary_is_safe() -> None:
    link = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert link.public_safe is True
    assert link.deterministic is True
    assert link.local_only is True
    assert link.legal_certification is False
    assert link.private_core_exposure is False
    assert link.fail_closed_required is True
    assert link.fail_closed_active is True


def test_qiv_artifacts_are_written(tmp_path) -> None:
    output_dir = tmp_path / "qiv"
    doc_path = tmp_path / "qiv-doc.md"

    link, validation, paths = write_qiv_runtime_constraint_link_artifacts(
        output_dir=output_dir,
        doc_path=doc_path,
    )

    assert validation.valid is True
    assert link.qiv_linked_to_programming is True
    assert doc_path.exists()

    for key in ("json", "index", "manifest", "markdown", "doc"):
        assert paths[key]

    payload = json.loads((output_dir / "qiv-runtime-constraint-link-v1.json").read_text())
    assert payload["validation"]["status"] == QIV_LINK_VALID
    assert payload["record"]["source_document_version"] == "v2.4"


def test_qiv_signature_is_deterministic_for_same_baseline() -> None:
    first = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")
    second = build_qiv_runtime_constraint_link(baseline_commit="TESTBASE")

    assert first.signature == second.signature
