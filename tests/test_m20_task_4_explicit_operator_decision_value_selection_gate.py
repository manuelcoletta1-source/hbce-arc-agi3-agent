
from hbce_arc_agi3.m20_task_4_explicit_operator_decision_value_selection_gate import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_4_identity_and_source_review():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 4
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "4DFB116D4A18C4D0"
    assert r["sourceOperatorDecisionRecordReviewPassed"] is True
    assert r["sourceExplicitOperatorDecisionValueSelectionRequired"] is True
    assert r["sourceExplicitOperatorDecisionValueSelectionGateCreated"] is False

def test_selection_gate_created_and_open():
    r = build_record()
    assert r["explicitOperatorDecisionValueSelectionGateOnly"] is True
    assert r["explicitOperatorDecisionValueSelectionGateReady"] is True
    assert r["explicitOperatorDecisionValueSelectionGateCreated"] is True
    assert r["explicitOperatorDecisionValueSelectionGateOpen"] is True
    assert r["explicitOperatorDecisionValueSelectionGateClosed"] is False
    assert r["explicitOperatorDecisionValueSelectionGateLocked"] is False

def test_selection_required_but_not_received():
    r = build_record()
    assert r["explicitOperatorDecisionValueSelectionRequired"] is True
    assert r["explicitOperatorDecisionValueSelectionReceived"] is False
    assert r["explicitOperatorDecisionValueSelectionRecorded"] is False
    assert r["explicitOperatorDecisionValueSelectionValidated"] is False
    assert r["explicitOperatorDecisionValueSelectionRecordRequired"] is True
    assert r["explicitOperatorDecisionValueSelectionRecordCreated"] is False
    assert r["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert r["explicitOperatorDecisionValueSelected"] is False

def test_selection_options_presented():
    r = build_record()
    assert r["selectionGateItemCount"] == 5
    assert r["operatorPromptOptionCount"] == 5
    assert r["validOperatorDecisionValueCount"] == 5
    assert all(item["availableForSelection"] is True for item in r["selectionGateItems"])
    assert all(item["presentedToOperator"] is True for item in r["selectionGateItems"])
    assert all(item["selected"] is False for item in r["selectionGateItems"])

def test_task_4_implementation_boundary_blocked():
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

def test_task_4_gates_and_artifacts(tmp_path):
    r = build_record()
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

    result = write_artifacts(tmp_path)
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_START" in (
        tmp_path / result["paths"]["milestone20_index"]
    ).read_text(encoding="utf-8")
