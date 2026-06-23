"""Milestone #19 Task 93 - SRSC controlled activation local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_92 = ROOT / "docs" / "milestone-19-task-92-srsc-diagnostic-adapter-activation-implementation-authorization-review-v1.md"
DOC_TASK_93 = ROOT / "docs" / "milestone-19-task-93-srsc-diagnostic-adapter-controlled-activation-local-implementation-v1.md"
ACTIVATION_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation.py"
ACTIVATION_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-local-implementation-v1"
    / "task-93-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-local-implementation-v1"
    / "task-93-index.txt"
)


def test_task_93_required_files_exist() -> None:
    assert DOC_TASK_92.exists()
    assert DOC_TASK_93.exists()
    assert ACTIVATION_MODULE.exists()
    assert ACTIVATION_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_93_dependency_markers() -> None:
    text = DOC_TASK_92.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_92_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_92_CONTROLLED_DIAGNOSTIC_ACTIVATION_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_92_ACTIVATION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_92_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_92_ADAPTER_ACTIVATED=false" in text
    assert "MILESTONE_19_TASK_92_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_92_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_92_SOLVER_RUNTIME_BINDING=false" in text


def test_task_93_canonical_markers() -> None:
    text = DOC_TASK_93.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_93_STATUS=CONTROLLED_DIAGNOSTIC_ACTIVATION_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_93_MODE=LOCAL_DIAGNOSTIC_ONLY_ACTIVATION_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_93_CONTROLLED_ACTIVATION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_93_DIAGNOSTIC_ONLY_ACTIVATION=true" in text
    assert "MILESTONE_19_TASK_93_ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY=true" in text
    assert "MILESTONE_19_TASK_93_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_93_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_93_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_93_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_93_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_93_FAIL_CLOSED_ACTIVE=true" in text


def test_task_93_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_DIAGNOSTIC_ACTIVATION_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_ACTIVATION_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_92_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["controlledActivationImplemented"] is True
    assert manifest["diagnosticOnlyActivation"] is True
    assert manifest["adapterActivatedForDiagnosticPathOnly"] is True
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


def test_task_93_activation_module_is_local_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == ["src/hbce_arc_agi3/srsc_diagnostic_adapter_activation.py"]
    assert manifest["implementedTests"] == ["tests/test_srsc_diagnostic_adapter_activation.py"]
    assert "DiagnosticAdapterActivationInput" in manifest["implementedActivationTypes"]
    assert "DiagnosticAdapterActivationResult" in manifest["implementedActivationTypes"]
    assert "DiagnosticAdapterActivationBlockedCall" in manifest["implementedActivationTypes"]
    assert "activate_diagnostic_adapter_for_diagnostic_path" in manifest["implementedActivationTypes"]
    assert "activate_diagnostic_adapter_batch_for_diagnostic_path" in manifest["implementedActivationTypes"]


def test_task_93_call_site_contract_is_present() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "local diagnostic scripts" in manifest["allowedCallSites"]
    assert "cross-trace diagnostic planners" in manifest["allowedCallSites"]
    assert "solver runtime loop" in manifest["forbiddenCallSites"]
    assert "candidate generator" in manifest["forbiddenCallSites"]
    assert "candidate ranker" in manifest["forbiddenCallSites"]
    assert "verifier" in manifest["forbiddenCallSites"]
    assert "benchmark executor" in manifest["forbiddenCallSites"]
    assert "Kaggle submission package builder" in manifest["forbiddenCallSites"]
