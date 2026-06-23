from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_decision_final_wait_state_archive_index_final_pending_status_closure_archive_index_review_task_48 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
    MODE,
    NEXT_TASK_NAME,
    PREVIOUS_SIGNATURE_FALLBACK,
    PREVIOUS_TASK_NAME,
    TASK_NAME,
    VERDICT,
    build_record,
    write_artifacts,
)


def test_task_48_identity_is_stable():
    record = build_record()

    assert record["taskName"] == TASK_NAME
    assert record["previousTask"] == PREVIOUS_TASK_NAME
    assert record["previousSignature"] == PREVIOUS_SIGNATURE_FALLBACK
    assert record["mode"] == MODE
    assert record["verdict"] == VERDICT
    assert record["nextTask"] == NEXT_TASK_NAME
    assert record["taskNumber"] == 48
    assert record["signature"]
    assert record["taskId"].startswith("MILESTONE-19-TASK-48-")


def test_task_48_creates_closure_archive_index_review():
    record = build_record()

    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewOnly"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewReady"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewPassed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewConfirmed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewCreated"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewActive"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewClosed"] is False


def test_task_48_requires_closure_next():
    record = build_record()

    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexClosureRequired"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexClosureCreated"] is False
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexClosureRequired"] is True
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexClosureCreated"] is False


def test_task_48_confirms_task_47_archive_index_chain():
    record = build_record()

    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReady"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexCreated"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexConfirmed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexLocked"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexActive"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexClosed"] is False


def test_task_48_keeps_prior_pending_states_closed():
    record = build_record()

    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureReviewClosed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureClosed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusReviewClosed"] is True
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusActive"] is False
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosed"] is True
    assert record["operatorDecisionFinalPendingStatusActive"] is False
    assert record["operatorDecisionFinalPendingStatusClosed"] is True
    assert record["operatorDecisionFinalPendingStatusClosureReviewClosed"] is True
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexCreated"] is True
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexActive"] is True
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexClosed"] is False


def test_task_48_keeps_operator_decision_pending():
    record = build_record()

    assert record["planningOnlyUntilExplicitOperatorDecision"] is True
    assert record["waitingForExplicitOperatorDecisionValue"] is True
    assert record["operatorDecisionPendingStatusActive"] is True
    assert record["operatorDecisionFinalWaitStateActive"] is False
    assert record["operatorDecisionFinalWaitStateClosed"] is True
    assert record["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
    assert record["explicitOperatorDecisionValueSelected"] is False
    assert record["explicitOperatorDecisionValueValidated"] is False
    assert record["explicitOperatorDecisionValueAuthorizing"] is False


def test_task_48_keeps_all_runtime_and_submission_boundaries_blocked():
    record = build_record()

    blocked_false_fields = [
        "operatorApprovalReceived",
        "operatorDecisionReceived",
        "implementationAuthorized",
        "implementationAuthorizationReceived",
        "implementationDecisionSelected",
        "runtimeActivationAuthorized",
        "runtimeActivationPerformed",
        "runtimeSolverModified",
        "candidateGeneratorModified",
        "rankerModified",
        "verifierModified",
        "realEvaluationAuthorized",
        "realEvaluationPerformed",
        "realSubmissionAuthorized",
        "submissionArtifactCreated",
        "kaggleAuthenticationAllowed",
        "kaggleAuthenticationPerformed",
        "kaggleSubmissionSent",
        "internetDuringEval",
        "externalApiDependency",
        "hiddenLabelAccessed",
        "privateCoreExposure",
        "legalCertification",
    ]

    for field in blocked_false_fields:
        assert record[field] is False, field

    assert record["operatorApprovalRequired"] is True
    assert record["operatorDecisionRequiredForImplementation"] is True
    assert record["failClosedRequired"] is True
    assert record["failClosedActive"] is True
    assert record["localOnly"] is True
    assert record["deterministic"] is True
    assert record["publicSafe"] is True


def test_task_48_allowed_values_are_reviewed_not_selected():
    record = build_record()

    assert record["allowedOperatorDecisionValues"] == ALLOWED_OPERATOR_DECISION_VALUES
    assert record["operatorPromptOptionCount"] == 5
    assert record["operatorDecisionFinalPendingStatusClosureArchiveIndexReviewItemCount"] == 5

    for option in record["operatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewOptions"]:
        assert option["value"] in ALLOWED_OPERATOR_DECISION_VALUES
        assert option["selected"] is False
        assert option["validated"] is False
        assert option["authorizing"] is False
        assert option["status"] == "VALUE_AVAILABLE_NOT_SELECTED_CLOSURE_ARCHIVE_INDEX_REVIEWED"


def test_task_48_archive_index_review_items_are_consistent():
    record = build_record()

    items = record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewItems"]
    assert len(items) == 5

    for item in items:
        assert item["operatorDecisionValue"] in ALLOWED_OPERATOR_DECISION_VALUES
        assert item["finalPendingStatusClosureArchiveIndexReview"] == "FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_REVIEW_PASSED_VALUE_AVAILABLE_NOT_SELECTED"
        assert item["confirmationStatus"] == "CONFIRMED_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_REVIEW_VALUE_AVAILABLE_NOT_SELECTED"
        assert item["nextArchiveIndexClosureStatus"] == "FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_REQUIRED_NO_SELECTION_NO_IMPLEMENTATION"
        assert item["blockingStatus"] == "IMPLEMENTATION_BLOCKED_NO_SELECTION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
        assert item["waitingForExplicitOperatorDecisionValue"] is True
        assert item["operatorDecisionPendingStatusActive"] is True
        assert item["operatorDecisionFinalPendingStatusActive"] is False
        assert item["operatorDecisionFinalPendingStatusClosed"] is True
        assert item["operatorDecisionFinalPendingStatusReviewActive"] is False
        assert item["operatorDecisionFinalPendingStatusReviewClosed"] is True
        assert item["operatorDecisionFinalPendingStatusClosureActive"] is False
        assert item["operatorDecisionFinalPendingStatusClosureClosed"] is True
        assert item["operatorDecisionFinalPendingStatusClosureReviewActive"] is False
        assert item["operatorDecisionFinalPendingStatusClosureReviewClosed"] is True
        assert item["operatorDecisionFinalPendingStatusClosureArchiveIndexActive"] is True
        assert item["operatorDecisionFinalPendingStatusClosureArchiveIndexClosed"] is False
        assert item["operatorDecisionFinalPendingStatusClosureArchiveIndexReviewActive"] is True
        assert item["operatorDecisionFinalPendingStatusClosureArchiveIndexReviewClosed"] is False
        assert item["operatorDecisionFinalWaitStateActive"] is False
        assert item["operatorDecisionFinalWaitStateClosed"] is True
        assert item["selectedOperatorDecisionValue"] == "PENDING_EXPLICIT_OPERATOR_DECISION"
        assert item["explicitOperatorDecisionValueSelected"] is False
        assert item["implementationAuthorized"] is False
        assert item["operatorDecisionReceived"] is False
        assert item["runtimeSolverModified"] is False
        assert item["candidateGeneratorModified"] is False
        assert item["rankerModified"] is False
        assert item["verifierModified"] is False
        assert item["realEvaluationPerformed"] is False
        assert item["kaggleSubmissionSent"] is False
        assert item["blockingIssue"] is False


def test_task_48_acceptance_gates_pass():
    record = build_record()

    assert record["acceptanceGateCount"] == len(record["acceptanceGates"])
    assert record["acceptanceGateCount"] >= 90
    assert record["acceptanceGateFailureCount"] == 0

    for gate in record["acceptanceGates"]:
        assert gate["passed"] is True
        assert gate["failure"] is False


def test_task_48_artifacts_are_written(tmp_path):
    result = write_artifacts(tmp_path)

    record = result["record"]
    paths = result["paths"]

    expected_path_keys = {
        "json",
        "index_json",
        "manifest",
        "markdown",
        "docs",
        "milestone_index",
    }

    assert set(paths) == expected_path_keys

    for relative_path in paths.values():
        path = tmp_path / relative_path
        assert path.exists(), relative_path
        assert path.read_text(encoding="utf-8").strip()

    assert record["taskName"] == TASK_NAME
    assert record["explicitOperatorDecisionValueSelectionOperatorDecisionFinalWaitStateArchiveIndexFinalPendingStatusClosureArchiveIndexReviewPassed"] is True
    assert "MILESTONE_19_TASK_48_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_REVIEW_START" in (
        tmp_path / paths["milestone_index"]
    ).read_text(encoding="utf-8")


def test_task_48_docs_contain_boundary_flags(tmp_path):
    result = write_artifacts(tmp_path)
    docs_path = tmp_path / result["paths"]["docs"]
    text = docs_path.read_text(encoding="utf-8")

    assert "Final Pending Status Closure Archive Index Review v1" in text
    assert "PENDING_EXPLICIT_OPERATOR_DECISION" in text
    assert "Closure archive index review passed: `True`" in text
    assert "Closure archive index closure required: `True`" in text
    assert "Implementation authorized: `False`" in text
    assert "Runtime activation performed: `False`" in text
    assert "Kaggle submission sent: `False`" in text
    assert "Fail closed active: `True`" in text


def test_task_48_manifest_contains_artifact_paths(tmp_path):
    result = write_artifacts(tmp_path)
    manifest_path = tmp_path / result["paths"]["manifest"]
    text = manifest_path.read_text(encoding="utf-8")

    assert "json=" in text
    assert "index_json=" in text
    assert "manifest=" in text
    assert "markdown=" in text
    assert "docs=" in text
    assert "milestone_index=" in text
    assert "closure_archive_index_review_passed=True" in text
    assert "closure_archive_index_closure_required=True" in text
    assert "implementation_authorized=False" in text
    assert "kaggle_submission_sent=False" in text
