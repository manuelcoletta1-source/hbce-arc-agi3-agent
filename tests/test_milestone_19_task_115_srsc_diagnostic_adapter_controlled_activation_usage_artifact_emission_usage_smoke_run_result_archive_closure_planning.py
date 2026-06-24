"""Milestone #19 Task 115 - SRSC smoke-run result archive closure planning validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    run_controlled_artifact_emission_usage_smoke_run_suite,
)
from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run_result_archive import (
    FAIL_CLOSED_ACTIVE,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    PRIVATE_CORE_EXPOSURE,
    RAW_REQUEST_BODY_PERSISTED,
    SECRET_PERSISTED,
    archive_controlled_smoke_run_suite_result,
    validate_controlled_smoke_run_result_archive,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_114 = ROOT / "docs" / "milestone-19-task-114-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-implementation-review-v1.md"
DOC_TASK_115 = ROOT / "docs" / "milestone-19-task-115-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-planning-v1.md"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-planning-v1" / "task-115-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-planning-v1" / "task-115-index.txt"
ARCHIVE_JSON = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-local-implementation-v1" / "task-113-smoke-run-result-archive.json"


def test_task_115_required_files_exist() -> None:
    assert DOC_TASK_114.exists()
    assert DOC_TASK_115.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert ARCHIVE_JSON.exists()


def test_task_115_dependency_markers() -> None:
    text = DOC_TASK_114.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_114_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_114_DECISION=ACCEPT_TASK_113_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_114_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_114_RESULT_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_114_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_114_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_114_LEGAL_CERTIFICATION=false" in text


def test_task_115_archive_still_valid_for_closure_planning() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()
    archive = archive_controlled_smoke_run_suite_result(suite)
    assert archive.archive_ok is True
    assert validate_controlled_smoke_run_result_archive(archive) == ()
    assert archive.archived_case_count == 8
    assert archive.archived_passed_count == 8
    assert archive.archived_failed_count == 0
    assert PRIVATE_CORE_EXPOSURE is False
    assert RAW_REQUEST_BODY_PERSISTED is False
    assert SECRET_PERSISTED is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True
    assert POC_V0_9_RUNTIME_IMPLEMENTED is False
    assert POC_V0_9_BENCHMARKED is False
    assert POC_V0_9_FAULT_INJECTION_PERFORMED is False
    assert POC_V0_9_PRODUCTION_READY is False


def test_task_115_static_archive_artifact_is_public_safe() -> None:
    payload = json.loads(ARCHIVE_JSON.read_text(encoding="utf-8"))
    assert payload["archiveOk"] is True
    assert payload["validationIssues"] == []
    assert payload["runtimeSolverModified"] is False
    assert payload["runtimeWiringAllowed"] is False
    assert payload["solverRuntimeBinding"] is False
    assert payload["benchmarkScoreClaimed"] is False
    assert payload["kaggleSubmissionSent"] is False
    assert payload["legalCertification"] is False
    assert payload["rawRequestBodyPersisted"] is False
    assert payload["secretPersisted"] is False
    assert payload["credentialPersisted"] is False
    assert payload["apiKeyPersisted"] is False


def test_task_115_canonical_markers() -> None:
    text = DOC_TASK_115.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_115_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_115_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_115_MODE=PLANNING_ONLY_NO_ARCHIVE_CLOSURE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_115_DECISION=PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY" in text
    assert "MILESTONE_19_TASK_115_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_115_ARCHIVE_CLOSURE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_115_RESULT_ARCHIVE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_115_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_115_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_115_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_115_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_115_FAIL_CLOSED_ACTIVE=true" in text


def test_task_115_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_115_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_ARCHIVE_CLOSURE_IMPLEMENTATION"
    assert manifest["decision"] == "PLAN_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_ONLY"
    assert manifest["controlledSmokeRunResultArchiveClosurePlanningPerformed"] is True
    assert manifest["controlledSmokeRunResultArchiveClosureAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask115"] is False
    assert manifest["archiveClosureImplemented"] is False
    assert manifest["resultArchiveModified"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["rawRequestBodyPersisted"] is False
    assert manifest["secretPersisted"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedActive"] is True
    assert manifest["pocV09RuntimeImplemented"] is False
    assert manifest["pocV09Benchmarked"] is False
    assert manifest["pocV09FaultInjectionPerformed"] is False
    assert manifest["pocV09ProductionReady"] is False
