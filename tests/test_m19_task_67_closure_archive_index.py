
from hbce_arc_agi3.m19_task_67_closure_archive_index import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_67_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 67
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "51DA31031BA75A82"
    assert r["taskId"].startswith("MILESTONE-19-TASK-67-")

def test_task_67_archive_index_state():
    r = build_record()
    assert r["closureArchiveIndexOnly"] is True
    assert r["closureArchiveIndexReady"] is True
    assert r["closureArchiveIndexCreated"] is True
    assert r["closureArchiveIndexConfirmed"] is True
    assert r["closureArchiveIndexLocked"] is True
    assert r["closureArchiveIndexActive"] is True
    assert r["closureArchiveIndexClosed"] is False
    assert r["closureArchiveIndexReviewRequired"] is True
    assert r["closureArchiveIndexReviewCreated"] is False

def test_task_67_boundary_blocked():
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

def test_task_67_items_and_gates():
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureArchiveIndexItemCount"] == 5
    assert r["closureArchiveIndexReviewItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_67_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["closureArchiveIndexCreated"] is True
    assert r["closureArchiveIndexReviewRequired"] is True
    assert "MILESTONE_19_TASK_67_CLOSURE_ARCHIVE_INDEX_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
