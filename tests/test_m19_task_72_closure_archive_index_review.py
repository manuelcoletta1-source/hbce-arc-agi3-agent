
from hbce_arc_agi3.m19_task_72_closure_archive_index_review import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_72_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 72
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "4E2A37B24E5AEDC2"
    assert r["taskId"].startswith("MILESTONE-19-TASK-72-")

def test_task_72_review_state():
    r = build_record()
    assert r["closureArchiveIndexReviewOnly"] is True
    assert r["closureArchiveIndexReviewReady"] is True
    assert r["closureArchiveIndexReviewPassed"] is True
    assert r["closureArchiveIndexReviewConfirmed"] is True
    assert r["closureArchiveIndexReviewCreated"] is True
    assert r["closureArchiveIndexReviewActive"] is True
    assert r["closureArchiveIndexReviewClosed"] is False
    assert r["closureRequired"] is True
    assert r["closureCreated"] is False

def test_task_72_boundary_blocked():
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

def test_task_72_items_and_gates():
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureArchiveIndexReviewItemCount"] == 5
    assert r["closureItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_72_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["closureArchiveIndexReviewPassed"] is True
    assert r["closureRequired"] is True
    assert "MILESTONE_19_TASK_72_CLOSURE_ARCHIVE_INDEX_REVIEW_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
