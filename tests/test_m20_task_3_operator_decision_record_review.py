
from hbce_arc_agi3.m20_task_3_operator_decision_record_review import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_3_identity_and_source_record():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 3
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "86CED93414333D7E"
    assert r["sourceOperatorDecisionRecordCreated"] is True
    assert r["sourceOperatorDecisionRecordLocked"] is True
    assert r["sourceOperatorDecisionRecordedValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"

def test_operator_decision_record_review_passes():
    r = build_record()
    assert r["operatorDecisionRecordReviewOnly"] is True
    assert r["operatorDecisionRecordReviewReady"] is True
    assert r["operatorDecisionRecordReviewCreated"] is True
    assert r["operatorDecisionRecordReviewPassed"] is True
    assert r["operatorDecisionRecordReviewConfirmed"] is True
    assert r["operatorDecisionRecordReviewLocked"] is True
    assert r["operatorDecisionRecordReviewClosed"] is True

def test_explicit_selection_required_next():
    r = build_record()
    assert r["explicitOperatorDecisionValueSelectionRequired"] is True
    assert r["explicitOperatorDecisionValueSelectionGateRequired"] is True
    assert r["explicitOperatorDecisionValueSelectionGateCreated"] is False
    assert r["nextTask"] == "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_V1"
    assert r["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert r["explicitOperatorDecisionValueSelected"] is False
    assert r["validOperatorDecisionValueCount"] == 5

def test_task_3_implementation_boundary_blocked():
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

def test_task_3_review_items_and_gates():
    r = build_record()
    assert r["reviewItemCount"] == 5
    assert r["operatorPromptOptionCount"] == 5
    assert all(item["reviewPassed"] is True for item in r["reviewItems"])
    assert all(item["explicitSelectionStillRequired"] is True for item in r["reviewItems"])
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_3_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["operatorDecisionRecordReviewPassed"] is True
    assert "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW_START" in (
        tmp_path / result["paths"]["milestone20_index"]
    ).read_text(encoding="utf-8")
