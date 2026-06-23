"""Milestone #19 Task 101 - SRSC controlled usage artifact emission local implementation validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_100 = ROOT / "docs" / "milestone-19-task-100-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-implementation-authorization-review-v1.md"
DOC_TASK_101 = ROOT / "docs" / "milestone-19-task-101-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-local-implementation-v1.md"
EMITTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
EMITTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-local-implementation-v1"
    / "task-101-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-local-implementation-v1"
    / "task-101-index.txt"
)


def test_task_101_required_files_exist() -> None:
    assert DOC_TASK_100.exists()
    assert DOC_TASK_101.exists()
    assert EMITTER_MODULE.exists()
    assert EMITTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_101_dependency_markers() -> None:
    text = DOC_TASK_100.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_100_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_100_CONTROLLED_DIAGNOSTIC_ARTIFACT_EMISSION_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_100_ARTIFACT_EMISSION_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_100_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_100_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_100_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_100_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_100_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_100_SOLVER_RUNTIME_BINDING=false" in text


def test_task_101_canonical_markers() -> None:
    text = DOC_TASK_101.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_101_STATUS=CONTROLLED_DIAGNOSTIC_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_101_MODE=LOCAL_DIAGNOSTIC_ONLY_ARTIFACT_EMISSION_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_101_CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_101_DIAGNOSTIC_ARTIFACT_EMISSION_ONLY=true" in text
    assert "MILESTONE_19_TASK_101_USAGE_LAYER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_101_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_101_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_101_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_101_FAIL_CLOSED_ACTIVE=true" in text


def test_task_101_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_DIAGNOSTIC_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_ARTIFACT_EMISSION_NO_RUNTIME_WIRING"
    assert manifest["dependency"] == "MILESTONE_19_TASK_100_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["controlledArtifactEmissionImplemented"] is True
    assert manifest["diagnosticArtifactEmissionOnly"] is True
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


def test_task_101_emitter_module_is_local_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
    ]
    assert manifest["implementedTests"] == [
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
    ]
    assert "DiagnosticUsageArtifactEmissionRequest" in manifest["implementedTypes"]
    assert "DiagnosticUsageArtifact" in manifest["implementedTypes"]
    assert "DiagnosticUsageArtifactEmissionBlockedRequest" in manifest["implementedTypes"]
    assert "DiagnosticUsageArtifactEmissionResult" in manifest["implementedTypes"]
    assert "emit_controlled_usage_artifact" in manifest["implementedTypes"]
    assert "emit_controlled_usage_artifact_batch" in manifest["implementedTypes"]


def test_task_101_artifact_contract_is_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert "local diagnostic report JSON" in manifest["authorizedArtifactFamilies"]
    assert "local diagnostic report Markdown" in manifest["authorizedArtifactFamilies"]
    assert "local milestone evidence package JSON" in manifest["authorizedArtifactFamilies"]
    assert "local public-safe audit summary JSON" in manifest["authorizedArtifactFamilies"]
    assert "local blocked usage report JSON" in manifest["authorizedArtifactFamilies"]
    assert "local cross-trace planner attachment JSON" in manifest["authorizedArtifactFamilies"]
    assert "local deterministic index TXT" in manifest["authorizedArtifactFamilies"]

    assert "solver performance proof" in manifest["forbiddenArtifactFamilies"]
    assert "benchmark proof" in manifest["forbiddenArtifactFamilies"]
    assert "Kaggle evidence" in manifest["forbiddenArtifactFamilies"]
    assert "legal certification evidence" in manifest["forbiddenArtifactFamilies"]
    assert "score report" in manifest["forbiddenArtifactFamilies"]
