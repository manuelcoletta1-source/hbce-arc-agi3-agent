"""Tests for Milestone #22 closure."""

from __future__ import annotations

from hbce_arc_agi3.milestone_22_closure import (
    FINAL_STATUS,
    MILESTONE_CLOSED,
    MILESTONE_CLOSURE_READY,
    NEXT_STAGE,
    REVISION,
    TASK_ID,
    build_milestone_22_closure,
    validate_milestone_22_closure,
)


def test_milestone_22_closure_contract() -> None:
    closure = build_milestone_22_closure(metadata={"case": "contract"})

    assert TASK_ID == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert REVISION == "MILESTONE_22_MILESTONE_CLOSURE_v1"
    assert NEXT_STAGE == "MILESTONE_22_CLOSED_NO_TASK_7_OR_8_USED"
    assert FINAL_STATUS == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert MILESTONE_CLOSURE_READY is True
    assert MILESTONE_CLOSED is True
    assert closure.task_budget_max == 8
    assert closure.final_task_number == 6
    assert closure.recommended_closure_task_number == 6
    assert closure.reserve_task_number == 7
    assert closure.emergency_only_task_number == 8
    assert len(closure.completed_task_ids) == 6
    assert len(closure.closure_checks) == 12
    assert len(closure.generated_artifacts) == 4
    assert closure.closure_ok is True
    assert closure.valid is True
    assert validate_milestone_22_closure(closure) == ()


def test_milestone_22_closure_public_payload() -> None:
    payload = build_milestone_22_closure().to_public_dict()

    assert payload["taskId"] == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert payload["milestoneId"] == "MILESTONE_22"
    assert payload["nextStage"] == "MILESTONE_22_CLOSED_NO_TASK_7_OR_8_USED"
    assert payload["finalStatus"] == "CLOSED_WITH_TASK_BUDGET_MAX_8_AT_TASK_6"
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "GOVERNED_WITHIN_TASK_BUDGET"
    assert payload["taskBudgetMax"] == 8
    assert payload["finalTaskNumber"] == 6
    assert payload["completedTaskCount"] == 6
    assert payload["closureCheckCount"] == 12
    assert payload["generatedArtifactCount"] == 4
    assert payload["sourceIntegrationValid"] is True
    assert payload["sourceIntegrationOk"] is True
    assert payload["task7Used"] is False
    assert payload["task8Used"] is False
    assert payload["reserveUnused"] is True
    assert payload["emergencyReserveUnused"] is True
    assert payload["milestoneClosureReady"] is True
    assert payload["milestoneClosed"] is True
    assert payload["taskChainClosed"] is True
    assert payload["fastSnapshotGuardClosed"] is True
    assert payload["validationArtifactsClosed"] is True
    assert payload["integrationRegressionClosed"] is True
    assert payload["postClosureReopenRequired"] is False
    assert payload["m20FinalTaskNumber"] == 7
    assert payload["m20Task7Used"] is True
    assert payload["m20Task8Used"] is False
    assert payload["m21Task7Used"] is False
    assert payload["m21Task8Used"] is False
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
    assert payload["closureId"].startswith("MILESTONE-22-CLOSURE-")


def test_milestone_22_completed_task_ids_are_bounded() -> None:
    closure = build_milestone_22_closure()

    assert closure.completed_task_ids[0] == "MILESTONE_22_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
    assert closure.completed_task_ids[-1] == "MILESTONE_22_TASK_6_MILESTONE_CLOSURE_V1"
    assert "MILESTONE_22_TASK_7" not in " ".join(closure.completed_task_ids)
    assert "MILESTONE_22_TASK_8" not in " ".join(closure.completed_task_ids)
