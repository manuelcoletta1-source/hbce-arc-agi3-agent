"""Tests for Milestone #23 closed milestone snapshot registry."""

from __future__ import annotations

import pytest

from hbce_arc_agi3.milestone_23_closed_milestone_snapshot_registry import (
    NEXT_STAGE,
    REGISTRY_IMPLEMENTATION_READY,
    REGISTRY_IMPLEMENTED,
    REVISION,
    TASK_ID,
    build_closed_milestone_snapshot_registry,
    build_milestone_23_closed_milestone_snapshot_registry_implementation,
    detect_forbidden_registry_traversal,
    validate_milestone_23_closed_milestone_snapshot_registry_implementation,
)


def test_registry_contract() -> None:
    registry = build_closed_milestone_snapshot_registry()

    assert registry.valid is True
    assert registry.snapshot_count == 3
    assert registry.valid_snapshot_count == 3
    assert registry.milestone_ids == ("MILESTONE_20", "MILESTONE_21", "MILESTONE_22")
    assert registry.contains("MILESTONE_22") is True
    assert registry.contains("MILESTONE_99") is False
    assert registry.registry_id.startswith("CLOSED-MILESTONE-SNAPSHOT-REGISTRY-")


def test_registry_lookup() -> None:
    registry = build_closed_milestone_snapshot_registry()

    m22 = registry.get("MILESTONE_22")
    assert m22.valid is True
    assert m22.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert m22.final_task_number == 6
    assert m22.task_7_used is False
    assert m22.task_8_used is False
    assert m22.reserve_unused is True
    assert m22.emergency_reserve_unused is True
    assert m22.marker_count == 5

    m20 = registry.get("MILESTONE_20")
    assert m20.task_7_used is True
    assert m20.task_8_used is False

    assert registry.try_get("MILESTONE_404") is None
    with pytest.raises(KeyError):
        registry.get("MILESTONE_404")


def test_forbidden_traversal_detection() -> None:
    detected = detect_forbidden_registry_traversal(
        (
            "static_registry_lookup",
            "closed_milestone.to_public_dict()",
            "runtime_object_graph_walk",
            "safe_document_marker_evidence",
        )
    )

    assert detected == ("closed_milestone.to_public_dict()", "runtime_object_graph_walk")


def test_implementation_contract() -> None:
    implementation = build_milestone_23_closed_milestone_snapshot_registry_implementation(
        metadata={"case": "contract"}
    )

    assert TASK_ID == "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
    assert REVISION == "MILESTONE_23_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_v1"
    assert NEXT_STAGE == "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert REGISTRY_IMPLEMENTATION_READY is True
    assert REGISTRY_IMPLEMENTED is True
    assert implementation.task_budget_min == 4
    assert implementation.task_budget_max == 8
    assert implementation.current_task_number == 3
    assert implementation.recommended_closure_task_number == 6
    assert implementation.registry.valid is True
    assert len(implementation.implementation_checks) == 12
    assert implementation.implementation_ok is True
    assert implementation.valid is True
    assert validate_milestone_23_closed_milestone_snapshot_registry_implementation(implementation) == ()


def test_implementation_public_payload() -> None:
    payload = build_milestone_23_closed_milestone_snapshot_registry_implementation().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_3_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["sourceScopeLockValid"] is True
    assert payload["scopeLockId"] == "MILESTONE_23_SCOPE_CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert payload["selectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_REGISTRY_LOCAL_ONLY"
    assert payload["registryValid"] is True
    assert payload["registrySnapshotCount"] == 3
    assert payload["registryValidSnapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["requiredSnapshotFieldCount"] == 10
    assert payload["forbiddenTraversalTokenCount"] == 5
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 3
    assert payload["implementationCheckCount"] == 12
    assert payload["registryImplementationReady"] is True
    assert payload["registryImplemented"] is True
    assert payload["registryLookupReady"] is True
    assert payload["readyForValidationArtifacts"] is True
    assert payload["localOnly"] is True
    assert payload["deterministic"] is True
    assert payload["publicSafe"] is True
    assert payload["fastSnapshotDependencyMode"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
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
    assert payload["implementationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["implementationId"].startswith("MILESTONE-23-SNAPSHOT-REGISTRY-")
