
from hbce_arc_agi3.m19_task_83_final_closeout import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_83_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 83
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "D54A0FD0B0FDAB29"
    assert r["taskId"].startswith("MILESTONE-19-TASK-83-")

def test_task_83_final_closeout_state():
    r = build_record()
    assert r["finalCloseoutOnly"] is True
    assert r["finalMilestone19CloseoutReady"] is True
    assert r["finalMilestone19CloseoutCreated"] is True
    assert r["finalMilestone19CloseoutConfirmed"] is True
    assert r["finalMilestone19CloseoutLocked"] is True
    assert r["finalMilestone19CloseoutClosed"] is True
    assert r["milestone19Closed"] is True
    assert r["milestone19Frozen"] is True

def test_task_83_recursion_stopped():
    r = build_record()
    assert r["recursiveArchiveChainStopped"] is True
    assert r["recursiveArchiveChainStoppedAtTask"] == 83
    assert r["additionalRecursiveArchiveIndexRequired"] is False
    assert r["nextRecursiveArchiveIndexRequired"] is False
    assert r["noFurtherMilestone19TasksRequired"] is True
    assert r["noFurtherMilestone19ClosureLoopRequired"] is True

def test_task_83_handoff_to_milestone_20():
    r = build_record()
    assert r["handoffToMilestone20"] is True
    assert r["nextStage"] == "MILESTONE_20"
    assert r["nextRecommendedTask"] == "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_V1"
    assert r["milestone20ReadyForOperatorDecisionGate"] is True
    assert r["milestone20ImplementationAuthorizedNow"] is False

def test_task_83_blocked_operational_boundary():
    r = build_record()
    for key in [
        "explicitOperatorDecisionValueSelected",
        "operatorApprovalReceived",
        "operatorDecisionReceived",
        "implementationAuthorized",
        "runtimeActivationPerformed",
        "runtimeSolverModified",
        "candidateGeneratorModified",
        "rankerModified",
        "verifierModified",
        "realEvaluationPerformed",
        "kaggleSubmissionSent",
        "privateCoreExposure",
        "legalCertification",
    ]:
        assert r[key] is False, key
    assert r["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert r["failClosedActive"] is True
    assert r["localOnly"] is True
    assert r["deterministic"] is True
    assert r["publicSafe"] is True

def test_task_83_items_gates_and_artifacts(tmp_path):
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["finalCloseoutItemCount"] == 5
    assert r["handoffItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

    result = write_artifacts(tmp_path)
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert "MILESTONE_19_TASK_83_FINAL_CLOSEOUT_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
