"""Milestone #19 Task 106 - SRSC controlled artifact emission usage implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_105 = ROOT / "docs" / "milestone-19-task-105-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-local-implementation-v1.md"
DOC_TASK_106 = ROOT / "docs" / "milestone-19-task-106-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-review-v1.md"
USAGE_RUNNER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
USAGE_RUNNER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-review-v1"
    / "task-106-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-review-v1"
    / "task-106-index.txt"
)


def test_task_106_required_files_exist() -> None:
    assert DOC_TASK_105.exists()
    assert DOC_TASK_106.exists()
    assert USAGE_RUNNER_MODULE.exists()
    assert USAGE_RUNNER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_106_dependency_markers() -> None:
    text = DOC_TASK_105.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_105_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_105_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_ONLY=true" in text
    assert "MILESTONE_19_TASK_105_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_USAGE_LAYER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_ACTIVATION_WRAPPER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_105_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_105_SOLVER_RUNTIME_BINDING=false" in text


def test_task_106_canonical_markers() -> None:
    text = DOC_TASK_106.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_106_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_106_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_106_MODE=REVIEW_ONLY_NO_ARTIFACT_EMISSION_USAGE_MODIFICATION" in text
    assert "MILESTONE_19_TASK_106_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_ONLY" in text
    assert "MILESTONE_19_TASK_106_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_106_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_106_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_106_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_106_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_106_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_106_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_106_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_106_FAIL_CLOSED_ACTIVE=true" in text


def test_task_106_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_106_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ARTIFACT_EMISSION_USAGE_MODIFICATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_105_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_ONLY"
    assert manifest["controlledArtifactEmissionUsageImplementationReviewPerformed"] is True
    assert manifest["controlledArtifactEmissionUsageSmokeRunPlanningAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask106"] is False
    assert manifest["usageRunnerModifiedInTask106"] is False
    assert manifest["artifactEmitterModifiedInTask106"] is False
    assert manifest["artifactEmissionUsageSmokeRunImplementedInTask106"] is False
    assert manifest["usageModifiedInTask106"] is False
    assert manifest["activationModifiedInTask106"] is False
    assert manifest["adapterModifiedInTask106"] is False
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


def test_task_106_reviewed_usage_runner_is_not_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["reviewedModule"] == "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
    assert "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py" in manifest["reviewedTests"]
    assert manifest["futurePlanningTarget"] == "MILESTONE_19_TASK_107_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_V1"
    assert "runtime usage wiring" in manifest["blockedBindings"]
    assert "solver runtime binding" in manifest["blockedBindings"]
    assert "candidate generator binding" in manifest["blockedBindings"]
    assert "benchmark score binding" in manifest["blockedBindings"]
    assert "Kaggle submission binding" in manifest["blockedBindings"]


def test_task_106_reviewed_usage_contract_is_preserved() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    reviewed_types = manifest["reviewedTypes"]
    authorized = manifest["reviewedAuthorizedUsageContexts"]
    forbidden = manifest["reviewedForbiddenUsageContexts"]

    assert "DiagnosticArtifactEmissionUsagePlan" in reviewed_types
    assert "DiagnosticArtifactEmissionUsageRequest" in reviewed_types
    assert "DiagnosticArtifactEmissionUsageBlockedRequest" in reviewed_types
    assert "DiagnosticArtifactEmissionUsageResult" in reviewed_types
    assert "build_controlled_artifact_emission_usage_plan" in reviewed_types
    assert "run_controlled_artifact_emission_usage" in reviewed_types
    assert "run_controlled_artifact_emission_usage_batch" in reviewed_types

    assert "local diagnostic artifact usage" in authorized
    assert "local milestone artifact bundle usage" in authorized
    assert "local deterministic index artifact usage" in authorized

    assert "solver runtime artifact usage" in forbidden
    assert "candidate generator artifact usage" in forbidden
    assert "benchmark artifact usage" in forbidden
    assert "Kaggle submission artifact usage" in forbidden
    assert "legal certification artifact usage" in forbidden
