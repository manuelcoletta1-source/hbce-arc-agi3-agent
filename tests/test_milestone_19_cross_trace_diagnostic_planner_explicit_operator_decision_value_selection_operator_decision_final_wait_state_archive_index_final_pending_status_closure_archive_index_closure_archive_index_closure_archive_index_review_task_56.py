
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_closure_archive_index_closure_archive_index_closure_archive_index_review_task_56 import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_56_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 56
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "79DD265DD497325C"
    assert r["taskId"].startswith("MILESTONE-19-TASK-56-")

def test_task_56_review_state():
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

def test_task_56_boundary_blocked():
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

def test_task_56_items_and_gates():
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureArchiveIndexReviewItemCount"] == 5
    assert r["closureItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_56_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["closureArchiveIndexReviewPassed"] is True
    assert "MILESTONE_19_TASK_56_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_REVIEW_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
