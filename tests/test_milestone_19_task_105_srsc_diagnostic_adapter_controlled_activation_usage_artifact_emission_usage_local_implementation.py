"""Milestone #19 Task 105 - SRSC controlled artifact emission usage local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_104 = ROOT / "docs" / "milestone-19-task-104-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-authorization-review-v1.md"
DOC_TASK_105 = ROOT / "docs" / "milestone-19-task-105-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1.md"
USAGE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
USAGE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1"
    / "task-105-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1"
    / "task-105-index.txt"
)


def test_task_105_required_files_exist() -> None:
    assert DOC_TASK_104.exists()
    assert DOC_TASK_105.exists()
    assert USAGE_MODULE.exists()
    assert USAGE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_105_dependency_markers() -> None:
    text = DOC_TASK_104.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_104_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_104_CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_104_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_104_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_104_SOLVER_RUNTIME_BINDING=false" in text


def test_task_105_canonical_markers() -> None:
    text = DOC_TASK_105.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_105_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_105_MODE=LOCAL_DIAGNOSTIC_ONLY_ARTIFACT_EMISSION_USAGE_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_105_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_105_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY=true" in text
    assert "MILESTONE_19_TASK_105_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_USAGE_LAYER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_105_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_105_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_105_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_105_FAIL_CLOSED_ACTIVE=true" in text


def test_task_105_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_ARTIFACT_EMISSION_USAGE_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_104_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["controlledArtifactEmissionUsageImplemented"] is True
    assert manifest["diagnosticArtifactEmissionUsageOnly"] is True
    assert manifest["artifactEmitterModified"] is False
    assert manifest["usageLayerModified"] is False
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


def test_task_105_implemented_module_is_usage_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
    ]
    assert manifest["implementedTests"] == [
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
    ]
    assert "DiagnosticArtifactEmissionUsagePlan" in manifest["implementedTypes"]
    assert "DiagnosticArtifactEmissionUsageRequest" in manifest["implementedTypes"]
    assert "DiagnosticArtifactEmissionUsageBlockedRequest" in manifest["implementedTypes"]
    assert "DiagnosticArtifactEmissionUsageResult" in manifest["implementedTypes"]
    assert "run_controlled_artifact_emission_usage" in manifest["implementedTypes"]
    assert "run_controlled_artifact_emission_usage_batch" in manifest["implementedTypes"]


def test_task_105_usage_contract_is_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "local diagnostic artifact usage" in manifest["authorizedUsageContexts"]
    assert "local milestone artifact bundle usage" in manifest["authorizedUsageContexts"]
    assert "local evidence package artifact usage" in manifest["authorizedUsageContexts"]
    assert "local public-safe audit artifact usage" in manifest["authorizedUsageContexts"]
    assert "local deterministic index artifact usage" in manifest["authorizedUsageContexts"]

    assert "solver runtime artifact usage" in manifest["forbiddenUsageContexts"]
    assert "candidate generator artifact usage" in manifest["forbiddenUsageContexts"]
    assert "ranker score artifact usage" in manifest["forbiddenUsageContexts"]
    assert "verifier score artifact usage" in manifest["forbiddenUsageContexts"]
    assert "benchmark artifact usage" in manifest["forbiddenUsageContexts"]
    assert "Kaggle submission artifact usage" in manifest["forbiddenUsageContexts"]
    assert "legal certification artifact usage" in manifest["forbiddenUsageContexts"]
