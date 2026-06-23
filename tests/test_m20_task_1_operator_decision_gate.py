
from hbce_arc_agi3.m20_task_1_operator_decision_gate import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_1_identity_and_handoff():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 1
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "96D4D3402FD43306"
    assert r["previousStage"] == "MILESTONE_19"
    assert r["sourceMilestone19Closed"] is True
    assert r["sourceRecursiveArchiveChainStopped"] is True
    assert r["sourceHandoffToMilestone20"] is True

def test_operator_decision_gate_state():
    r = build_record()
    assert r["operatorDecisionGateOnly"] is True
    assert r["operatorDecisionGateReady"] is True
    assert r["operatorDecisionGateCreated"] is True
    assert r["operatorDecisionGateOpen"] is True
    assert r["operatorDecisionGateClosed"] is False
    assert r["operatorDecisionRequired"] is True
    assert r["operatorDecisionReceived"] is False
    assert r["operatorDecisionRecordRequired"] is True

def test_decision_options_are_presented_but_not_selected():
    r = build_record()
    assert r["decisionOptionCount"] == 5
    assert r["operatorPromptOptionCount"] == 5
    assert r["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert r["explicitOperatorDecisionValueSelected"] is False
    assert all(item["presentedToOperator"] is True for item in r["decisionOptionItems"])
    assert all(item["selected"] is False for item in r["decisionOptionItems"])
    assert all(item["recorded"] is False for item in r["decisionOptionItems"])

def test_task_1_implementation_boundary_blocked():
    r = build_record()
    for key in [
        "controlledLocalImplementationAuthorizedNow",
        "implementationAuthorized",
        "implementationAuthorizationReceived",
        "implementationPatchCreated",
        "implementationPatchApplied",
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
    assert r["failClosedActive"] is True
    assert r["localOnly"] is True
    assert r["deterministic"] is True
    assert r["publicSafe"] is True

def test_task_1_gates():
    r = build_record()
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_1_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["operatorDecisionGateOpen"] is True
    assert "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_START" in (
        tmp_path / result["paths"]["milestone20_index"]
    ).read_text(encoding="utf-8")
