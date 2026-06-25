"""Tests for Milestone #23 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_23_closure import (
    FINAL_STATUS,
    MILESTONE_CLOSED,
    MILESTONE_CLOSURE_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_23_closure,
    validate_milestone_23_closure,
)


def test_milestone_23_closure_contract() -> None:
    closure = build_milestone_23_closure(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"
    assert REVISION == "MILESTONE_23_MILESTONE_CLOSURE_v1"
    assert NEXT_STAGE == "MILESTONE_23_CLOSED_NO_TASK_7_OR_8_USED"
    assert FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert MILESTONE_CLOSURE_READY is True
    assert MILESTONE_CLOSED is True
    assert closure.final_status == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert closure.technical_status == "PASS"
    assert closure.process_status == "GOVERNED_WITHIN_TASK_BUDGET"
    assert closure.task_budget_min == 4
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert closure.completed_task_count == 6
    assert closure.task_7_used is False
    assert closure.task_8_used is False
    assert closure.reserve_unused is True
    assert closure.emergency_reserve_unused is True
    assert len(closure.closure_checks) == 16
    assert len(closure.generated_artifacts) == 4
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_23_closure(closure) == ()


def test_milestone_23_closure_public_payload() -> None:
    payload = build_milestone_23_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_23_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_23"
    assert payload["nextStage"] == "MILESTONE_23_CLOSED_NO_TASK_7_OR_8_USED"
    assert payload["sourceIntegrationValid"] is True
    assert payload["sourceIntegrationOk"] is True
    assert payload["sourceReadyForMilestoneClosure"] is True
    assert payload["registryValid"] is True
    assert payload["registrySnapshotCount"] == 3
    assert payload["registeredMilestoneIds"] == ["MILESTONE_20", "MILESTONE_21", "MILESTONE_22"]
    assert payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["taskBudgetMin"] == 4
    assert payload["taskBudgetMax"] == 8
    assert payload["finalTaskNumber"] == 6
    assert payload["completedTaskCount"] == 6
    assert payload["task7Used"] is False
    assert payload["task8Used"] is False
    assert payload["reserveUnused"] is True
    assert payload["emergencyReserveUnused"] is True
    assert payload["closureCheckCount"] == 16
    assert payload["generatedArtifactCount"] == 4
    assert payload["milestoneClosureReady"] is True
    assert payload["milestoneClosed"] is True
    assert payload["taskChainClosed"] is True
    assert payload["registryChainClosed"] is True
    assert payload["integrationRegressionClosed"] is True
    assert payload["closureArtifactsCreated"] is True
    assert payload["noTask7Or8Used"] is True
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
    assert payload["m22Task7Used"] is False
    assert payload["m22Task8Used"] is False
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
    assert payload["closureOk"] is True
    assert payload["valid"] is True
    assert payload["issues"] == []
    assert payload["closureId"].startswith("MILESTONE-23-CLOSURE-")


def test_closure_checks_are_explicit() -> None:
    closure = build_milestone_23_closure()

    assert "task_1_governed_opening_closed" in closure.closure_checks
    assert "task_2_objective_scope_lock_closed" in closure.closure_checks
    assert "task_3_snapshot_registry_implementation_closed" in closure.closure_checks
    assert "task_4_validation_artifacts_closed" in closure.closure_checks
    assert "task_5_integration_regression_closed" in closure.closure_checks
    assert "registry_snapshot_count_3_preserved" in closure.closure_checks
    assert "m22_task7_unused_preserved" in closure.closure_checks
    assert "m22_task8_unused_preserved" in closure.closure_checks
    assert "task_7_unused" in closure.closure_checks
    assert "task_8_unused" in closure.closure_checks
