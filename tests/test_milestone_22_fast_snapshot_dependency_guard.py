"""Tests for Milestone #22 fast snapshot dependency guard."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_fast_snapshot_dependency_guard import (
    FAST_SNAPSHOT_DEPENDENCY_GUARD_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_closed_milestone_snapshot,
    build_default_milestone_20_snapshot,
    build_default_milestone_21_snapshot,
    build_fast_snapshot_dependency_guard,
    detect_forbidden_runtime_traversal,
    validate_fast_snapshot_dependency_guard,
)


def test_fast_snapshot_guard_contract() -> None:
    guard = build_fast_snapshot_dependency_guard(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
    assert REVISION == "MILESTONE_22_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_v1"
    assert NEXT_STAGE == "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert FAST_SNAPSHOT_DEPENDENCY_GUARD_READY is True
    assert guard.task_budget_max == 8
    assert guard.current_task_number == 3
    assert guard.recommended_closure_task_number == 6
    assert guard.snapshot_count == 2
    assert len(guard.allowed_dependency_modes) == 3
    assert len(guard.forbidden_dependency_modes) == 4
    assert len(guard.guard_checks) == 10
    assert guard.guard_ok is True
    assert guard.valid is True
    assert validate_fast_snapshot_dependency_guard(guard) == ()


def test_fast_snapshot_guard_public_payload() -> None:
    payload = build_fast_snapshot_dependency_guard().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_3_FAST_SNAPSHOT_DEPENDENCY_GUARD_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["scopeLockId"] == "MILESTONE_22_SCOPE_FAST_SNAPSHOT_DEPENDENCY_GUARD_LOCAL_ONLY"
    assert payload["sourceScopeLockValid"] is True
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 3
    assert payload["remainingBudgetAfterCurrentTask"] == 5
    assert payload["snapshotCount"] == 2
    assert payload["requiredSnapshotFieldCount"] == 8
    assert payload["allowedDependencyModeCount"] == 3
    assert payload["forbiddenDependencyModeCount"] == 4
    assert payload["forbiddenRuntimeTraversalTokenCount"] == 5
    assert payload["guardCheckCount"] == 10
    assert payload["fastSnapshotDependencyGuardReady"] is True
    assert payload["fastSnapshotDependencyGuardImplemented"] is True
    assert payload["localOnlyGuard"] is True
    assert payload["snapshotPatternEnforced"] is True
    assert payload["documentEvidencePreserved"] is True
    assert payload["deepRecursiveTraversalBlocked"] is True
    assert payload["readyForValidationArtifacts"] is True
    assert payload["milestone21Task7Required"] is False
    assert payload["milestone21Task8Required"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["kaggleAuthenticationAllowed"] is False
    assert payload["kaggleUploadAllowed"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["legalCertification"] is False
    assert payload["historicalMilestoneRewrite"] is False
    assert payload["failClosedActive"] is True
    assert payload["guardOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["guardId"].startswith("MILESTONE-22-FAST-SNAPSHOT-GUARD-")


def test_default_snapshots_are_valid() -> None:
    m21 = build_default_milestone_21_snapshot()
    m20 = build_default_milestone_20_snapshot()

    assert m21.valid is True
    assert m21.milestone_id == "MILESTONE_21"
    assert m21.task_7_used is False
    assert m21.task_8_used is False
    assert m21.marker_count == 4

    assert m20.valid is True
    assert m20.milestone_id == "MILESTONE_20"
    assert m20.final_task_number == 7
    assert m20.task_7_used is True
    assert m20.task_8_used is False
    assert m20.marker_count == 3


def test_custom_snapshot_requires_document_markers() -> None:
    snapshot = build_closed_milestone_snapshot(
        milestone_id="MILESTONE_X",
        final_status="CLOSED",
        task_budget_max=8,
        final_task_number=6,
        task_7_used=False,
        task_8_used=False,
        evidence_doc_path="docs/example.md",
        evidence_markers=("A=true", "B=false", "C=ready"),
    )

    assert snapshot.valid is True
    assert snapshot.marker_count == 3
    assert snapshot.snapshot_id.startswith("FAST-SNAPSHOT-MILESTONE_X-")


def test_forbidden_runtime_traversal_detection() -> None:
    detected = detect_forbidden_runtime_traversal(
        [
            "safe_static_snapshot",
            "closed_milestone.to_public_dict()",
            "recursive_runtime_dependency_walk",
        ]
    )

    assert detected == (
        "closed_milestone.to_public_dict()",
        "recursive_runtime_dependency_walk",
    )
