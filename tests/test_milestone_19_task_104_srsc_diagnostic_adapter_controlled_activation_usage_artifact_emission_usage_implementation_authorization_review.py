"""Milestone #19 Task 104 - SRSC controlled artifact emission usage implementation authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_103 = ROOT / "docs" / "milestone-19-task-103-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-planning-v1.md"
DOC_TASK_104 = ROOT / "docs" / "milestone-19-task-104-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-authorization-review-v1.md"
EMITTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
EMITTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-authorization-review-v1"
    / "task-104-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-authorization-review-v1"
    / "task-104-index.txt"
)


def test_task_104_required_files_exist() -> None:
    assert DOC_TASK_103.exists()
    assert DOC_TASK_104.exists()
    assert EMITTER_MODULE.exists()
    assert EMITTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_104_dependency_markers() -> None:
    text = DOC_TASK_103.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_103_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_103_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_103_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_103_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_103_SOLVER_RUNTIME_BINDING=false" in text


def test_task_104_canonical_markers() -> None:
    text = DOC_TASK_104.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_104_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_104_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_104_MODE=REVIEW_ONLY_NO_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_104_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_104_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_104_CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_104_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_104_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_104_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_104_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_104_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_104_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_104_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_104_FAIL_CLOSED_ACTIVE=true" in text


def test_task_104_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_104_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_103_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_LOCAL_IMPLEMENTATION_ONLY"
    assert manifest["controlledArtifactEmissionUsageImplementationAuthorizationReviewPerformed"] is True
    assert manifest["controlledArtifactEmissionUsageLocalImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask104"] is False
    assert manifest["artifactEmissionUsageImplementedInTask104"] is False
    assert manifest["artifactEmitterModifiedInTask104"] is False
    assert manifest["usageModifiedInTask104"] is False
    assert manifest["activationModifiedInTask104"] is False
    assert manifest["adapterModifiedInTask104"] is False
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


def test_task_104_authorized_future_modules_are_usage_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["authorizedFutureModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py",
    ]
    assert "DiagnosticArtifactEmissionUsagePlan" in manifest["authorizedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageRequest" in manifest["authorizedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageResult" in manifest["authorizedFutureTypes"]
    assert "build_controlled_artifact_emission_usage_plan" in manifest["authorizedFutureTypes"]
    assert "run_controlled_artifact_emission_usage" in manifest["authorizedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_batch" in manifest["authorizedFutureTypes"]


def test_task_104_authorized_usage_flows_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    authorized = manifest["authorizedFutureUsageFlows"]
    forbidden = manifest["forbiddenFutureUsageFlows"]

    assert "single diagnostic report emission flow" in authorized
    assert "diagnostic report bundle emission flow" in authorized
    assert "milestone evidence package emission flow" in authorized
    assert "public-safe audit summary emission flow" in authorized
    assert "blocked usage report emission flow" in authorized
    assert "cross-trace planner attachment emission flow" in authorized
    assert "deterministic index emission flow" in authorized

    assert "solver runtime artifact usage" in forbidden
    assert "candidate generator artifact usage" in forbidden
    assert "ranker score artifact usage" in forbidden
    assert "verifier score artifact usage" in forbidden
    assert "benchmark artifact usage" in forbidden
    assert "Kaggle submission artifact usage" in forbidden
    assert "legal certification artifact usage" in forbidden


def test_task_104_blocked_bindings_preserve_no_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocked = manifest["blockedBindings"]

    assert "controlled artifact emission usage implementation in Task 104" in blocked
    assert "artifact emitter modification in Task 104" in blocked
    assert "usage layer modification in Task 104" in blocked
    assert "activation wrapper modification in Task 104" in blocked
    assert "adapter modification in Task 104" in blocked
    assert "runtime usage wiring" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
    assert "legal certification binding" in blocked
