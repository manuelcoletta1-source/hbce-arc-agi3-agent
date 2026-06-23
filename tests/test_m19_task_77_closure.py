
from hbce_arc_agi3.m19_task_77_closure import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_77_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 77
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "E20C4373023DDDC3"
    assert r["taskId"].startswith("MILESTONE-19-TASK-77-")

def test_task_77_closure_state():
    r = build_record()
    assert r["closureOnly"] is True
    assert r["closureReady"] is True
    assert r["closureCreated"] is True
    assert r["closureConfirmed"] is True
    assert r["closureLocked"] is True
    assert r["closureActive"] is False
    assert r["closureClosed"] is True
    assert r["closureReviewRequired"] is True
    assert r["closureReviewCreated"] is False

def test_task_77_boundary_blocked():
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

def test_task_77_items_and_gates():
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureItemCount"] == 5
    assert r["closureReviewItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_77_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["closureCreated"] is True
    assert r["closureClosed"] is True
    assert r["closureReviewRequired"] is True
    assert "MILESTONE_19_TASK_77_CLOSURE_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
