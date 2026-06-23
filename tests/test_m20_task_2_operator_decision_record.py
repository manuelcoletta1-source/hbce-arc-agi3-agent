
from hbce_arc_agi3.m20_task_2_operator_decision_record import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_2_identity_and_gate_source():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 2
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "0B41A78A7FD4B64F"
    assert r["sourceOperatorDecisionGateOpen"] is True
    assert r["sourceOperatorDecisionRequired"] is True
    assert r["sourceOperatorDecisionReceived"] is False

def test_operator_decision_record_created_but_pending():
    r = build_record()
    assert r["operatorDecisionRecordOnly"] is True
    assert r["operatorDecisionRecordReady"] is True
    assert r["operatorDecisionRecordCreated"] is True
    assert r["operatorDecisionRecordConfirmed"] is True
    assert r["operatorDecisionRecordLocked"] is True
    assert r["operatorDecisionRecordClosed"] is True
    assert r["operatorDecisionRecordReviewRequired"] is True
    assert r["operatorDecisionRecordReviewCreated"] is False
    assert r["operatorDecisionRecorded"] is True
    assert r["operatorDecisionRecordedValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"

def test_no_explicit_operator_decision_selected():
    r = build_record()
    assert r["operatorDecisionReceived"] is False
    assert r["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert r["explicitOperatorDecisionValueSelected"] is False
    assert r["explicitOperatorDecisionValueValidated"] is False
    assert r["explicitOperatorDecisionValueAuthorizing"] is False
    assert r["validOperatorDecisionValueCount"] == 5
    assert all(item["selected"] is False for item in r["decisionRecordItems"])
    assert all(item["pendingDecisionRecorded"] is True for item in r["decisionRecordItems"])

def test_task_2_implementation_boundary_blocked():
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

def test_task_2_gates():
    r = build_record()
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_2_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["operatorDecisionRecordCreated"] is True
    assert "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_START" in (
        tmp_path / result["paths"]["milestone20_index"]
    ).read_text(encoding="utf-8")
