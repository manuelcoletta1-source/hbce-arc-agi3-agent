"""Milestone #19 Task 92 - SRSC diagnostic adapter activation implementation authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_91 = ROOT / "docs" / "milestone-19-task-91-srsc-diagnostic-adapter-activation-planning-v1.md"
DOC_TASK_92 = ROOT / "docs" / "milestone-19-task-92-srsc-diagnostic-adapter-activation-implementation-authorization-review-v1.md"
ADAPTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter.py"
ADAPTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-activation-implementation-authorization-review-v1"
    / "task-92-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-activation-implementation-authorization-review-v1"
    / "task-92-index.txt"
)


def test_task_92_required_files_exist() -> None:
    assert DOC_TASK_91.exists()
    assert DOC_TASK_92.exists()
    assert ADAPTER_MODULE.exists()
    assert ADAPTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_92_dependency_markers() -> None:
    text = DOC_TASK_91.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_91_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_91_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_91_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_91_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_91_SOLVER_RUNTIME_BINDING=false" in text


def test_task_92_canonical_markers() -> None:
    text = DOC_TASK_92.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_92_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_92_STATUS=ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_92_MODE=REVIEW_ONLY_NO_ACTIVATION_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_92_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_DIAGNOSTIC_ACTIVATION_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_92_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_92_CONTROLLED_DIAGNOSTIC_ACTIVATION_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_92_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_92_ACTIVATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_92_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_92_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_92_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_92_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_92_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_92_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_92_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_92_FAIL_CLOSED_ACTIVE=true" in text


def test_task_92_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_92_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ACTIVATION_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_91_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_DIAGNOSTIC_ACTIVATION_IMPLEMENTATION_ONLY"
    assert manifest["adapterActivationImplementationAuthorizationReviewPerformed"] is True
    assert manifest["controlledDiagnosticActivationImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask92"] is False
    assert manifest["activationImplementedInTask92"] is False
    assert manifest["adapterModifiedInTask92"] is False
    assert manifest["adapterActivatedInTask92"] is False
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


def test_task_92_authorized_future_modules_are_activation_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["authorizedFutureModules"]

    assert modules == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation.py",
        "tests/test_srsc_diagnostic_adapter_activation.py",
    ]
    assert all("solver" not in module for module in modules)
    assert all("ranker" not in module for module in modules)
    assert all("verifier" not in module for module in modules)


def test_task_92_authorized_types_and_blocked_bindings() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    activation_types = manifest["authorizedFutureActivationTypes"]
    blocked = manifest["blockedBindings"]

    assert "DiagnosticAdapterActivationInput" in activation_types
    assert "DiagnosticAdapterActivationResult" in activation_types
    assert "DiagnosticAdapterActivationBlockedCall" in activation_types
    assert "activate_diagnostic_adapter_for_diagnostic_path" in activation_types
    assert "activate_diagnostic_adapter_batch_for_diagnostic_path" in activation_types

    assert "activation implementation in Task 92" in blocked
    assert "adapter modification in Task 92" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
