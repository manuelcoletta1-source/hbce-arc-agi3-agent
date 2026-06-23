
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_closure_archive_index_closure_archive_index_closure_archive_index_closure_review_task_58 import (
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_record,
    write_artifacts,
)

def test_task_58_identity():
    r = build_record()
    assert r["taskName"] == TASK_NAME
    assert r["taskNumber"] == 58
    assert r["previousSignature"] == PREVIOUS_SIGNATURE
    assert r["previousSignature"] == "C21790A60EDE25C0"
    assert r["taskId"].startswith("MILESTONE-19-TASK-58-")

def test_task_58_review_state():
    r = build_record()
    assert r["closureReviewOnly"] is True
    assert r["closureReviewReady"] is True
    assert r["closureReviewPassed"] is True
    assert r["closureReviewConfirmed"] is True
    assert r["closureReviewCreated"] is True
    assert r["closureReviewActive"] is True
    assert r["closureReviewClosed"] is False
    assert r["closureArchiveIndexRequired"] is True
    assert r["closureArchiveIndexCreated"] is False

def test_task_58_boundary_blocked():
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

def test_task_58_items_and_gates():
    r = build_record()
    assert r["operatorPromptOptionCount"] == 5
    assert r["closureReviewItemCount"] == 5
    assert r["closureArchiveIndexItemCount"] == 5
    assert r["acceptanceGateCount"] == 90
    assert r["acceptanceGateFailureCount"] == 0
    assert all(g["passed"] and not g["failure"] for g in r["acceptanceGates"])

def test_task_58_artifacts(tmp_path):
    result = write_artifacts(tmp_path)
    r = result["record"]
    for rel in result["paths"].values():
        p = tmp_path / rel
        assert p.exists()
        assert p.read_text(encoding="utf-8").strip()
    assert r["closureReviewPassed"] is True
    assert r["closureArchiveIndexRequired"] is True
    assert "MILESTONE_19_TASK_58_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_REVIEW_START" in (
        tmp_path / result["paths"]["milestone_index"]
    ).read_text(encoding="utf-8")
