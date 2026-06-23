"""Milestone #19 Task 96 - SRSC controlled activation usage implementation authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_95 = ROOT / "docs" / "milestone-19-task-95-srsc-diagnostic-adapter-controlled-activation-usage-planning-v1.md"
DOC_TASK_96 = ROOT / "docs" / "milestone-19-task-96-srsc-diagnostic-adapter-controlled-activation-usage-implementation-authorization-review-v1.md"
ACTIVATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation.py"
ACTIVATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-implementation-authorization-review-v1"
    / "task-96-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-implementation-authorization-review-v1"
    / "task-96-index.txt"
)


def test_task_96_required_files_exist() -> None:
    assert DOC_TASK_95.exists()
    assert DOC_TASK_96.exists()
    assert ACTIVATION_MODULE.exists()
    assert ACTIVATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_96_dependency_markers() -> None:
    text = DOC_TASK_95.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_95_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_95_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_95_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_95_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_95_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_95_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_95_SOLVER_RUNTIME_BINDING=false" in text


def test_task_96_canonical_markers() -> None:
    text = DOC_TASK_96.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_96_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_96_STATUS=CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_96_MODE=REVIEW_ONLY_NO_USAGE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_96_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_DIAGNOSTIC_USAGE_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_96_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_96_CONTROLLED_DIAGNOSTIC_USAGE_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_96_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_96_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_96_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_96_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_96_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_96_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_96_FAIL_CLOSED_ACTIVE=true" in text


def test_task_96_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_96_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_USAGE_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_95_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_DIAGNOSTIC_USAGE_IMPLEMENTATION_ONLY"
    assert manifest["controlledActivationUsageImplementationAuthorizationReviewPerformed"] is True
    assert manifest["controlledDiagnosticUsageImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask96"] is False
    assert manifest["usageImplementedInTask96"] is False
    assert manifest["activationModifiedInTask96"] is False
    assert manifest["adapterModifiedInTask96"] is False
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


def test_task_96_authorized_future_modules_are_usage_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    modules = manifest["authorizedFutureModules"]

    assert modules == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage.py",
    ]
    assert all("solver" not in module for module in modules)
    assert all("ranker" not in module for module in modules)
    assert all("verifier" not in module for module in modules)
    assert all("candidate" not in module for module in modules)


def test_task_96_authorized_types_and_blocked_bindings() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    usage_types = manifest["authorizedFutureUsageTypes"]
    blocked = manifest["blockedBindings"]

    assert "DiagnosticActivationUsageRequest" in usage_types
    assert "DiagnosticActivationUsageResult" in usage_types
    assert "DiagnosticActivationUsageBlockedRequest" in usage_types
    assert "run_controlled_activation_usage" in usage_types
    assert "run_controlled_activation_usage_batch" in usage_types

    assert "usage implementation in Task 96" in blocked
    assert "activation wrapper modification in Task 96" in blocked
    assert "adapter modification in Task 96" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
