"""Milestone #19 Task 94 - SRSC controlled activation implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_93 = ROOT / "docs" / "milestone-19-task-93-srsc-diagnostic-adapter-controlled-activation-local-implementation-v1.md"
DOC_TASK_94 = ROOT / "docs" / "milestone-19-task-94-srsc-diagnostic-adapter-controlled-activation-implementation-review-v1.md"
ACTIVATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation.py"
ACTIVATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-implementation-review-v1"
    / "task-94-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-implementation-review-v1"
    / "task-94-index.txt"
)


def test_task_94_required_files_exist() -> None:
    assert DOC_TASK_93.exists()
    assert DOC_TASK_94.exists()
    assert ACTIVATION_MODULE.exists()
    assert ACTIVATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_94_dependency_markers() -> None:
    text = DOC_TASK_93.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_93_CONTROLLED_ACTIVATION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_93_DIAGNOSTIC_ONLY_ACTIVATION=true" in text
    assert "MILESTONE_19_TASK_93_ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY=true" in text
    assert "MILESTONE_19_TASK_93_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_93_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_93_SOLVER_RUNTIME_BINDING=false" in text


def test_task_94_canonical_markers() -> None:
    text = DOC_TASK_94.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_94_STATUS=CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_94_MODE=REVIEW_ONLY_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_94_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ACTIVATION_USAGE_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_94_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_94_CONTROLLED_ACTIVATION_USAGE_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_94_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_94_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_94_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_94_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_94_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_94_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_94_FAIL_CLOSED_ACTIVE=true" in text


def test_task_94_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_ACTIVATION_USAGE_PLANNING_ONLY"
    assert manifest["controlledActivationImplementationReviewPerformed"] is True
    assert manifest["controlledActivationUsagePlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask94"] is False
    assert manifest["activationModifiedInTask94"] is False
    assert manifest["adapterModifiedInTask94"] is False
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


def test_task_94_reviewed_activation_is_not_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModule"] == "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation.py"
    assert "tests/test_srsc_diagnostic_adapter_activation.py" in manifest["reviewedTests"]
    assert manifest["futurePlanningTarget"] == "MILESTONE_19_TASK_95_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_PLANNING_V1"
    assert "activation runtime wiring" in manifest["blockedBindings"]
    assert "solver runtime binding" in manifest["blockedBindings"]
    assert "candidate generator binding" in manifest["blockedBindings"]
    assert "Kaggle submission binding" in manifest["blockedBindings"]


def test_task_94_reviewed_call_site_contract_is_preserved() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed = manifest["reviewedAllowedCallSites"]
    forbidden = manifest["reviewedForbiddenCallSites"]

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
