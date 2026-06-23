"""Milestone #19 Task 90 - SRSC diagnostic adapter implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_89 = ROOT / "docs" / "milestone-19-task-89-srsc-diagnostic-adapter-local-implementation-v1.md"
DOC_TASK_90 = ROOT / "docs" / "milestone-19-task-90-srsc-diagnostic-adapter-implementation-review-v1.md"
ADAPTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter.py"
ADAPTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-implementation-review-v1"
    / "task-90-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-implementation-review-v1"
    / "task-90-index.txt"
)


def test_task_90_required_files_exist() -> None:
    assert DOC_TASK_89.exists()
    assert DOC_TASK_90.exists()
    assert ADAPTER_MODULE.exists()
    assert ADAPTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_90_dependency_markers() -> None:
    text = DOC_TASK_89.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_89_ADAPTER_IMPLEMENTATION_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_89_LOCAL_STANDALONE_ADAPTER=true" in text
    assert "MILESTONE_19_TASK_89_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_89_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_89_RUNTIME_WIRING_ALLOWED=false" in text


def test_task_90_canonical_markers() -> None:
    text = DOC_TASK_90.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_90_STATUS=ADAPTER_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_90_MODE=REVIEW_ONLY_NO_ADAPTER_ACTIVATION" in text
    assert "MILESTONE_19_TASK_90_DECISION=AUTHORIZE_NEXT_TASK_ADAPTER_ACTIVATION_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_ACTIVATION_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_90_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_90_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_90_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_90_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_90_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_90_FAIL_CLOSED_ACTIVE=true" in text


def test_task_90_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "ADAPTER_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ADAPTER_ACTIVATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_ADAPTER_ACTIVATION_PLANNING_ONLY"
    assert manifest["adapterImplementationReviewPerformed"] is True
    assert manifest["adapterActivationPlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask90"] is False
    assert manifest["adapterModifiedInTask90"] is False
    assert manifest["adapterActivatedInTask90"] is False
    assert manifest["runtimeActivationAuthorized"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["candidateGeneratorModified"] is False
    assert manifest["rankerModified"] is False
    assert manifest["verifierModified"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["realEvaluationPerformed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["internetDuringEval"] is False
    assert manifest["externalApiDependency"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedRequired"] is True
    assert manifest["failClosedActive"] is True


def test_task_90_reviewed_adapter_is_not_activation() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModule"] == "src/hbce_arc_agi3/srsc_diagnostic_adapter.py"
    assert "tests/test_srsc_diagnostic_adapter.py" in manifest["reviewedTests"]
    assert manifest["futurePlanningTarget"] == "MILESTONE_19_TASK_91_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_PLANNING_V1"
    assert "adapter activation in Task 90" in manifest["blockedBindings"]
    assert "adapter runtime wiring" in manifest["blockedBindings"]
    assert "solver runtime binding" in manifest["blockedBindings"]
    assert "Kaggle submission binding" in manifest["blockedBindings"]
