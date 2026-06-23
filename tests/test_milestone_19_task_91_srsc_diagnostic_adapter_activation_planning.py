"""Milestone #19 Task 91 - SRSC diagnostic adapter activation planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_90 = ROOT / "docs" / "milestone-19-task-90-srsc-diagnostic-adapter-implementation-review-v1.md"
DOC_TASK_91 = ROOT / "docs" / "milestone-19-task-91-srsc-diagnostic-adapter-activation-planning-v1.md"
ADAPTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter.py"
ADAPTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-activation-planning-v1"
    / "task-91-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-activation-planning-v1"
    / "task-91-index.txt"
)


def test_task_91_required_files_exist() -> None:
    assert DOC_TASK_90.exists()
    assert DOC_TASK_91.exists()
    assert ADAPTER_MODULE.exists()
    assert ADAPTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_91_dependency_markers() -> None:
    text = DOC_TASK_90.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_ACTIVATION_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_90_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_90_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_91_canonical_markers() -> None:
    text = DOC_TASK_91.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_91_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_91_STATUS=ADAPTER_ACTIVATION_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_91_MODE=PLANNING_ONLY_NO_ADAPTER_ACTIVATION" in text
    assert "MILESTONE_19_TASK_91_DECISION=PLAN_CONTROLLED_ADAPTER_ACTIVATION_ONLY" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_ACTIVATION_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_91_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_91_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_91_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_91_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_91_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_91_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_91_FAIL_CLOSED_ACTIVE=true" in text


def test_task_91_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_91_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_PLANNING_V1"
    assert manifest["status"] == "ADAPTER_ACTIVATION_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_ADAPTER_ACTIVATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_CONTROLLED_ADAPTER_ACTIVATION_ONLY"
    assert manifest["adapterActivationPlanningPerformed"] is True
    assert manifest["adapterActivationImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask91"] is False
    assert manifest["adapterModifiedInTask91"] is False
    assert manifest["adapterActivatedInTask91"] is False
    assert manifest["runtimeActivationAuthorized"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["solverRuntimeBinding"] is False
    assert manifest["candidateGeneratorModified"] is False
    assert manifest["candidateGeneratorBinding"] is False
    assert manifest["rankerModified"] is False
    assert manifest["rankerBinding"] is False
    assert manifest["verifierModified"] is False
    assert manifest["verifierBinding"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["benchmarkBinding"] is False
    assert manifest["realEvaluationPerformed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["kaggleSubmissionBinding"] is False
    assert manifest["internetDuringEval"] is False
    assert manifest["externalApiDependency"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedRequired"] is True
    assert manifest["failClosedActive"] is True


def test_task_91_allowed_and_forbidden_call_sites() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed = manifest["plannedAllowedCallSites"]
    forbidden = manifest["plannedForbiddenCallSites"]

    assert "local diagnostic scripts" in allowed
    assert "public-safe audit artifact builders" in allowed
    assert "cross-trace diagnostic planners" in allowed

    assert "solver runtime loop" in forbidden
    assert "candidate generator" in forbidden
    assert "candidate ranker" in forbidden
    assert "verifier" in forbidden
    assert "benchmark executor" in forbidden
    assert "Kaggle submission package builder" in forbidden
    assert "network or API clients" in forbidden


def test_task_91_allowed_outputs_do_not_include_scores_or_submission() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed_outputs = manifest["plannedAllowedOutputs"]
    forbidden_outputs = manifest["plannedForbiddenOutputs"]

    assert "DiagnosticAdapterResult" in allowed_outputs
    assert "deterministic public JSON" in allowed_outputs
    assert "blocked reference reports" in allowed_outputs

    assert "benchmark score" in forbidden_outputs
    assert "Kaggle submission file" in forbidden_outputs
    assert "public score claim" in forbidden_outputs
    assert "private score claim" in forbidden_outputs
    assert "legal certification claim" in forbidden_outputs
