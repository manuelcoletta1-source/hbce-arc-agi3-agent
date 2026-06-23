
from hbce_arc_agi3.m19_task_82_closure_review import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_82_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 82
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "B7983B1C9B0ADBFB"
    assert r["taskId"].startswith("MILESTONE-19-TASK-82-")

def test_task_82_final_closure_review_state():
    r = build_record()
    assert r["closureReviewOnly"] is True
    assert r["closureReviewReady"] is True
    assert r["closureReviewPassed"] is True
    assert r["closureReviewConfirmed"] is True
    assert r["closureReviewCreated"] is True
    assert r["closureReviewActive"] is True
    assert r["closureReviewClosed"] is False
    assert r["finalMilestone19CloseoutRequired"] is True
    assert r["finalMilestone19CloseoutCreated"] is False

def test_task_82_recursion_stop_boundary():
    r = build_record()
    assert r["recursiveArchiveChainStopRequired"] is True
    assert r["recursiveArchiveChainStopRecommended"] is True
    assert r["recursiveArchiveChainStopped"] is False
    assert r["additionalRecursiveArchiveIndexRequired"] is False
    assert r["nextRecursiveArchiveIndexRequired"] is False

def test_task_82_blocked_operational_boundary():
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

def test_task_82_items_gates_and_artifacts(tmp_path):
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureReviewItemCount"] == 5
    assert r["finalCloseoutItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

    result = write_artifacts(tmp_path)
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert "MILESTONE_19_TASK_82_FINAL_CLOSURE_REVIEW_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
