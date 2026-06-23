"""Milestone #19 Task 102 - SRSC controlled artifact emission implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_101 = ROOT / "docs" / "milestone-19-task-101-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-local-implementation-v1.md"
DOC_TASK_102 = ROOT / "docs" / "milestone-19-task-102-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-implementation-review-v1.md"
EMITTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
EMITTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-implementation-review-v1"
    / "task-102-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-implementation-review-v1"
    / "task-102-index.txt"
)


def test_task_102_required_files_exist() -> None:
    assert DOC_TASK_101.exists()
    assert DOC_TASK_102.exists()
    assert EMITTER_MODULE.exists()
    assert EMITTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_102_dependency_markers() -> None:
    text = DOC_TASK_101.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_101_CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_101_DIAGNOSTIC_ARTIFACT_EMISSION_ONLY=true" in text
    assert "MILESTONE_19_TASK_101_USAGE_LAYER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_101_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_101_SOLVER_RUNTIME_BINDING=false" in text


def test_task_102_canonical_markers() -> None:
    text = DOC_TASK_102.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_102_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_102_STATUS=CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_102_MODE=REVIEW_ONLY_NO_ARTIFACT_EMITTER_MODIFICATION" in text
    assert "MILESTONE_19_TASK_102_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_102_CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_102_CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_102_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_102_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_102_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_102_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_102_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_102_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_102_FAIL_CLOSED_ACTIVE=true" in text


def test_task_102_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_102_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ARTIFACT_EMITTER_MODIFICATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_101_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_ONLY"
    assert manifest["controlledArtifactEmissionImplementationReviewPerformed"] is True
    assert manifest["controlledArtifactEmissionUsagePlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask102"] is False
    assert manifest["artifactEmitterModifiedInTask102"] is False
    assert manifest["artifactEmissionUsageImplementedInTask102"] is False
    assert manifest["usageModifiedInTask102"] is False
    assert manifest["activationModifiedInTask102"] is False
    assert manifest["adapterModifiedInTask102"] is False
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


def test_task_102_reviewed_emitter_is_not_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModule"] == "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
    assert "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py" in manifest["reviewedTests"]
    assert manifest["futurePlanningTarget"] == "MILESTONE_19_TASK_103_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_PLANNING_V1"
    assert "usage runtime wiring" in manifest["blockedBindings"]
    assert "solver runtime binding" in manifest["blockedBindings"]
    assert "candidate generator binding" in manifest["blockedBindings"]
    assert "benchmark score binding" in manifest["blockedBindings"]
    assert "Kaggle submission binding" in manifest["blockedBindings"]


def test_task_102_reviewed_artifact_contract_is_preserved() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    reviewed_types = manifest["reviewedTypes"]
    authorized = manifest["reviewedAuthorizedArtifactFamilies"]
    forbidden = manifest["reviewedForbiddenArtifactFamilies"]

    assert "DiagnosticUsageArtifactEmissionRequest" in reviewed_types
    assert "DiagnosticUsageArtifact" in reviewed_types
    assert "DiagnosticUsageArtifactEmissionBlockedRequest" in reviewed_types
    assert "DiagnosticUsageArtifactEmissionResult" in reviewed_types
    assert "emit_controlled_usage_artifact" in reviewed_types
    assert "emit_controlled_usage_artifact_batch" in reviewed_types

    assert "local diagnostic report JSON" in authorized
    assert "local diagnostic report Markdown" in authorized
    assert "local deterministic index TXT" in authorized

    assert "solver performance proof" in forbidden
    assert "benchmark proof" in forbidden
    assert "Kaggle evidence" in forbidden
    assert "legal certification evidence" in forbidden
    assert "score report" in forbidden
