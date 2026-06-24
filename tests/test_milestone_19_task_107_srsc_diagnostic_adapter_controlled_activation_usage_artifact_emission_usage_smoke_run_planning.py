"""Milestone #19 Task 107 - SRSC controlled artifact emission usage smoke-run planning validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_106 = ROOT / "docs" / "milestone-19-task-106-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-implementation-review-v1.md"
DOC_TASK_107 = ROOT / "docs" / "milestone-19-task-107-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-planning-v1.md"
USAGE_RUNNER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
USAGE_RUNNER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-planning-v1"
    / "task-107-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-planning-v1"
    / "task-107-index.txt"
)


def test_task_107_required_files_exist() -> None:
    assert DOC_TASK_106.exists()
    assert DOC_TASK_107.exists()
    assert USAGE_RUNNER_MODULE.exists()
    assert USAGE_RUNNER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_107_dependency_markers() -> None:
    text = DOC_TASK_106.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_106_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_106_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_106_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_106_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_106_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_106_SOLVER_RUNTIME_BINDING=false" in text


def test_task_107_canonical_markers() -> None:
    text = DOC_TASK_107.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_107_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_107_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_READY" in text
    assert "MILESTONE_19_TASK_107_MODE=PLANNING_ONLY_NO_SMOKE_RUN_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_107_DECISION=PLAN_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY" in text
    assert "MILESTONE_19_TASK_107_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_107_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_107_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_107_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_107_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_107_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_107_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_107_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_107_FAIL_CLOSED_ACTIVE=true" in text


def test_task_107_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_107_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_READY"
    assert manifest["mode"] == "PLANNING_ONLY_NO_SMOKE_RUN_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_106_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_IMPLEMENTATION_REVIEW_V1"
    assert manifest["decision"] == "PLAN_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY"
    assert manifest["controlledArtifactEmissionUsageSmokeRunPlanningPerformed"] is True
    assert manifest["controlledArtifactEmissionUsageSmokeRunImplementationAuthorizationReviewRequiredNext"] is True
    assert manifest["implementationPerformedInTask107"] is False
    assert manifest["artifactEmissionUsageSmokeRunImplementedInTask107"] is False
    assert manifest["usageRunnerModifiedInTask107"] is False
    assert manifest["artifactEmitterModifiedInTask107"] is False
    assert manifest["usageModifiedInTask107"] is False
    assert manifest["activationModifiedInTask107"] is False
    assert manifest["adapterModifiedInTask107"] is False
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


def test_task_107_future_modules_are_planning_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["plannedFutureModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py",
    ]
    assert manifest["artifactEmissionUsageSmokeRunImplementedInTask107"] is False
    assert "DiagnosticArtifactEmissionUsageSmokeRunPlan" in manifest["plannedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunCase" in manifest["plannedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunResult" in manifest["plannedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunSuiteResult" in manifest["plannedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_smoke_run" in manifest["plannedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_smoke_run_suite" in manifest["plannedFutureTypes"]


def test_task_107_smoke_run_cases_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cases = manifest["plannedSmokeRunCases"]
    allowed = manifest["plannedAllowedSmokeRunScope"]
    forbidden = manifest["plannedForbiddenSmokeRunScope"]

    assert "happy-path diagnostic report smoke-run" in cases
    assert "custom artifact bundle smoke-run" in cases
    assert "deterministic index smoke-run" in cases
    assert "forbidden usage context smoke-run" in cases
    assert "forbidden artifact family smoke-run" in cases
    assert "boundary marker smoke-run" in cases
    assert "no-score and no-submission marker smoke-run" in cases

    assert "local diagnostic artifact usage smoke-run" in allowed
    assert "local milestone artifact bundle smoke-run" in allowed
    assert "local evidence package artifact smoke-run" in allowed
    assert "fail-closed context validation smoke-run" in allowed
    assert "fail-closed artifact-family validation smoke-run" in allowed

    assert "solver runtime smoke-run" in forbidden
    assert "candidate generator smoke-run" in forbidden
    assert "ranker score smoke-run" in forbidden
    assert "verifier score smoke-run" in forbidden
    assert "benchmark smoke-run" in forbidden
    assert "Kaggle submission smoke-run" in forbidden
    assert "legal certification smoke-run" in forbidden


def test_task_107_blocked_bindings_preserve_no_runtime() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocked = manifest["blockedBindings"]

    assert "controlled smoke-run implementation in Task 107" in blocked
    assert "usage runner modification in Task 107" in blocked
    assert "artifact emitter modification in Task 107" in blocked
    assert "usage layer modification in Task 107" in blocked
    assert "activation wrapper modification in Task 107" in blocked
    assert "adapter modification in Task 107" in blocked
    assert "runtime smoke-run wiring" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
    assert "legal certification binding" in blocked
