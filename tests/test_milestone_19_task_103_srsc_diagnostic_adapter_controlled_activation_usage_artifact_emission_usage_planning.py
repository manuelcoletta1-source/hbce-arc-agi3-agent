"""Milestone #19 Task 103 - SRSC controlled artifact emission usage planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_102 = ROOT / "docs" / "milestone-19-task-102-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-implementation-review-v1.md"
DOC_TASK_103 = ROOT / "docs" / "milestone-19-task-103-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-planning-v1.md"
EMITTER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
EMITTER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emitter.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-planning-v1"
    / "task-103-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-planning-v1"
    / "task-103-index.txt"
)


def test_task_103_required_files_exist() -> None:
    assert DOC_TASK_102.exists()
    assert DOC_TASK_103.exists()
    assert EMITTER_MODULE.exists()
    assert EMITTER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_103_dependency_markers() -> None:
    text = DOC_TASK_102.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_102_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_102_CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_102_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_102_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_102_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_102_SOLVER_RUNTIME_BINDING=false" in text


def test_task_103_canonical_markers() -> None:
    text = DOC_TASK_103.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_103_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_103_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_103_MODE=PLANNING_ONLY_NO_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_103_DECISION=PLAN_CONTROLLED_ARTIFACT_EMISSION_USAGE_ONLY" in text
    assert "MILESTONE_19_TASK_103_CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_103_CONTROLLED_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_103_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_103_ARTIFACT_EMISSION_USAGE_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_103_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_103_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_103_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_103_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_103_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_103_FAIL_CLOSED_ACTIVE=true" in text


def test_task_103_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_103_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_102_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_CONTROLLED_ARTIFACT_EMISSION_USAGE_ONLY"
    assert manifest["controlledArtifactEmissionUsagePlanningPerformed"] is True
    assert manifest["controlledArtifactEmissionUsageImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask103"] is False
    assert manifest["artifactEmissionUsageImplementedInTask103"] is False
    assert manifest["artifactEmitterModifiedInTask103"] is False
    assert manifest["usageModifiedInTask103"] is False
    assert manifest["activationModifiedInTask103"] is False
    assert manifest["adapterModifiedInTask103"] is False
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


def test_task_103_future_modules_are_planning_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["plannedFutureModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py",
    ]
    assert manifest["artifactEmissionUsageImplementedInTask103"] is False
    assert "DiagnosticArtifactEmissionUsagePlan" in manifest["plannedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageRequest" in manifest["plannedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageResult" in manifest["plannedFutureTypes"]
    assert "run_controlled_artifact_emission_usage" in manifest["plannedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_batch" in manifest["plannedFutureTypes"]


def test_task_103_usage_flows_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    flows = manifest["plannedControlledUsageFlows"]
    allowed = manifest["plannedAllowedUsageContexts"]
    forbidden = manifest["plannedForbiddenUsageContexts"]

    assert "single diagnostic report emission flow" in flows
    assert "diagnostic report bundle emission flow" in flows
    assert "milestone evidence package emission flow" in flows
    assert "public-safe audit summary emission flow" in flows
    assert "blocked usage report emission flow" in flows
    assert "cross-trace planner attachment emission flow" in flows

    assert "local diagnostic artifact usage" in allowed
    assert "local milestone artifact bundle usage" in allowed
    assert "local evidence package artifact usage" in allowed
    assert "local deterministic index artifact usage" in allowed

    assert "solver runtime artifact usage" in forbidden
    assert "candidate generator artifact usage" in forbidden
    assert "ranker score artifact usage" in forbidden
    assert "verifier score artifact usage" in forbidden
    assert "benchmark artifact usage" in forbidden
    assert "Kaggle submission artifact usage" in forbidden
    assert "legal certification artifact usage" in forbidden


def test_task_103_blocked_bindings_preserve_no_runtime() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocked = manifest["blockedBindings"]

    assert "controlled artifact emission usage implementation in Task 103" in blocked
    assert "artifact emitter modification in Task 103" in blocked
    assert "usage layer modification in Task 103" in blocked
    assert "activation wrapper modification in Task 103" in blocked
    assert "adapter modification in Task 103" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
    assert "legal certification binding" in blocked
