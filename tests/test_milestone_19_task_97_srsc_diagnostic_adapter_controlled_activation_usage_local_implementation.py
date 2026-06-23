"""Milestone #19 Task 97 - SRSC controlled activation usage local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_96 = ROOT / "docs" / "milestone-19-task-96-srsc-diagnostic-adapter-controlled-activation-usage-implementation-authorization-review-v1.md"
DOC_TASK_97 = ROOT / "docs" / "milestone-19-task-97-srsc-diagnostic-adapter-controlled-activation-usage-local-implementation-v1.md"
USAGE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage.py"
USAGE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-local-implementation-v1"
    / "task-97-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-local-implementation-v1"
    / "task-97-index.txt"
)


def test_task_97_required_files_exist() -> None:
    assert DOC_TASK_96.exists()
    assert DOC_TASK_97.exists()
    assert USAGE_MODULE.exists()
    assert USAGE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_97_dependency_markers() -> None:
    text = DOC_TASK_96.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_96_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_96_CONTROLLED_DIAGNOSTIC_USAGE_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_96_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_96_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_96_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_96_SOLVER_RUNTIME_BINDING=false" in text


def test_task_97_canonical_markers() -> None:
    text = DOC_TASK_97.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_97_STATUS=CONTROLLED_DIAGNOSTIC_USAGE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_97_MODE=LOCAL_DIAGNOSTIC_ONLY_USAGE_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_97_CONTROLLED_USAGE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_97_DIAGNOSTIC_USAGE_ONLY=true" in text
    assert "MILESTONE_19_TASK_97_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_97_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_97_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_97_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_97_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_97_FAIL_CLOSED_ACTIVE=true" in text


def test_task_97_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_DIAGNOSTIC_USAGE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_USAGE_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_96_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["controlledUsageImplemented"] is True
    assert manifest["diagnosticUsageOnly"] is True
    assert manifest["activationWrapperModified"] is False
    assert manifest["adapterModified"] is False
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


def test_task_97_usage_module_is_local_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == ["src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage.py"]
    assert manifest["implementedTests"] == ["tests/test_srsc_diagnostic_adapter_activation_usage.py"]
    assert "DiagnosticActivationUsageRequest" in manifest["implementedUsageTypes"]
    assert "DiagnosticActivationUsageResult" in manifest["implementedUsageTypes"]
    assert "DiagnosticActivationUsageBlockedRequest" in manifest["implementedUsageTypes"]
    assert "run_controlled_activation_usage" in manifest["implementedUsageTypes"]
    assert "run_controlled_activation_usage_batch" in manifest["implementedUsageTypes"]


def test_task_97_usage_context_contract_is_present() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "local SRSC diagnostic report generation" in manifest["allowedUsageContexts"]
    assert "local milestone evidence packaging" in manifest["allowedUsageContexts"]
    assert "local cross-trace planner evidence attachment" in manifest["allowedUsageContexts"]
    assert "solver runtime execution" in manifest["forbiddenUsageContexts"]
    assert "candidate generation" in manifest["forbiddenUsageContexts"]
    assert "candidate ranking" in manifest["forbiddenUsageContexts"]
    assert "verifier execution" in manifest["forbiddenUsageContexts"]
    assert "benchmark execution" in manifest["forbiddenUsageContexts"]
    assert "Kaggle submission packaging" in manifest["forbiddenUsageContexts"]
