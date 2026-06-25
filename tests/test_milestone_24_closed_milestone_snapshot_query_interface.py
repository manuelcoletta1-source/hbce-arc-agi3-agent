"""Tests for Milestone #24 closed milestone snapshot query interface."""

from __future__ import annotations

from hbce_arc_agi3.milestone_24_closed_milestone_snapshot_query_interface import (
    NEXT_STAGE,
    QUERY_INTERFACE_IMPLEMENTED,
    QUERY_INTERFACE_READY,
    REVISION,
    TASK_ID,
    build_milestone_24_query_interface_implementation,
    get_closed_milestone_snapshot,
    list_closed_milestone_snapshots,
    summarize_closed_milestone_snapshot,
    validate_milestone_24_query_interface_implementation,
    validate_query_result_boundary,
)


def test_query_interface_contract() -> None:
    implementation = build_milestone_24_query_interface_implementation(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert REVISION == "MILESTONE_24_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_v1"
    assert NEXT_STAGE == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert QUERY_INTERFACE_READY is True
    assert QUERY_INTERFACE_IMPLEMENTED is True
    assert implementation.task_budget_min == 4
    assert implementation.task_budget_max == 8
    assert implementation.current_task_number == 3
    assert implementation.recommended_closure_task_number == 6
    assert len(implementation.allowed_query_operations) == 4
    assert len(implementation.forbidden_operations) == 5
    assert len(implementation.required_snapshot_fields) == 10
    assert len(implementation.implementation_checks) == 12
    assert implementation.implementation_ok is True
    assert implementation.valid is True
    assert validate_milestone_24_query_interface_implementation(implementation) == ()


def test_list_closed_milestone_snapshots() -> None:
    snapshots = list_closed_milestone_snapshots()

    assert len(snapshots) == 3
    assert [snapshot["milestoneId"] for snapshot in snapshots] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert all(snapshot["valid"] is True for snapshot in snapshots)
    assert all(snapshot["milestoneClosed"] is True for snapshot in snapshots)
    assert all(snapshot["taskBudgetMax"] == 8 for snapshot in snapshots)
    assert all(snapshot["task8Used"] is False for snapshot in snapshots)
    assert all(snapshot["legalCertification"] is False for snapshot in snapshots)


def test_get_closed_milestone_snapshot() -> None:
    m20 = get_closed_milestone_snapshot("milestone-20")
    m21 = get_closed_milestone_snapshot("MILESTONE_21")
    m22 = get_closed_milestone_snapshot(" milestone_22 ")

    assert m20["found"] is True
    assert m20["snapshot"]["milestoneId"] == "MILESTONE_20"
    assert m20["snapshot"]["task7Used"] is True
    assert m20["snapshot"]["task8Used"] is False
    assert m21["found"] is True
    assert m21["snapshot"]["task7Used"] is False
    assert m22["found"] is True
    assert m22["snapshot"]["finalTaskNumber"] == 6

    missing = get_closed_milestone_snapshot("MILESTONE_999")
    assert missing["found"] is False
    assert missing["valid"] is False
    assert missing["issues"] == ["MILESTONE_SNAPSHOT_NOT_FOUND"]


def test_summarize_closed_milestone_snapshot() -> None:
    summary = summarize_closed_milestone_snapshot("MILESTONE_22")
    missing = summarize_closed_milestone_snapshot("MILESTONE_999")

    assert summary["found"] is True
    assert summary["valid"] is True
    assert "MILESTONE_22 closed" in summary["summary"]
    assert "task7Used=false" in summary["summary"]
    assert "task8Used=false" in summary["summary"]
    assert missing["found"] is False
    assert missing["valid"] is False


def test_validate_query_result_boundary() -> None:
    snapshot = get_closed_milestone_snapshot("MILESTONE_21")["snapshot"]
    boundary = validate_query_result_boundary(snapshot)

    assert boundary["operation"] == "validate_query_result_boundary"
    assert boundary["valid"] is True
    assert boundary["issues"] == []
    assert boundary["requiredFieldCount"] == 10
    assert boundary["readOnly"] is True
    assert boundary["localOnly"] is True
    assert boundary["legalCertification"] is False

    broken = dict(snapshot)
    broken["task8Used"] = True
    broken_boundary = validate_query_result_boundary(broken)
    assert broken_boundary["valid"] is False
    assert "TASK_8_USED" in broken_boundary["issues"]


def test_query_interface_public_payload() -> None:
    payload = build_milestone_24_query_interface_implementation().to_public_dict()

    assert payload["taskId"] == "MILESTONE_24_TASK_3_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_IMPLEMENTATION_V1"
    assert payload["milestoneId"] == "MILESTONE_24"
    assert payload["sourceLockValid"] is True
    assert payload["sourceLockOk"] is True
    assert payload["sourceScopeLockId"] == "MILESTONE_24_SCOPE_CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert payload["sourceSelectedObjectiveId"] == "CLOSED_MILESTONE_SNAPSHOT_QUERY_INTERFACE_LOCAL_ONLY"
    assert payload["sourceImplementationAllowedNext"] is True
    assert payload["sourceFastOpeningSnapshot"] is True
    assert payload["nextStage"] == "MILESTONE_24_TASK_4_VALIDATION_AND_ARTIFACTS_V1"
    assert payload["taskBudgetMax"] == 8
    assert payload["currentTaskNumber"] == 3
    assert payload["snapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["m21Task7Used"] is False
    assert payload["m22Task7Used"] is False
    assert payload["m22Task8Used"] is False
    assert payload["missingSnapshotFound"] is False
    assert payload["queryInterfaceReady"] is True
    assert payload["queryInterfaceImplemented"] is True
    assert payload["queryInterfaceReadOnly"] is True
    assert payload["fastSourceScopeLockSnapshot"] is True
    assert payload["deepRecursiveDependencyTraversalAllowed"] is False
    assert payload["runtimeSolverModified"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["implementationOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["implementationId"].startswith("MILESTONE-24-QUERY-INTERFACE-")
