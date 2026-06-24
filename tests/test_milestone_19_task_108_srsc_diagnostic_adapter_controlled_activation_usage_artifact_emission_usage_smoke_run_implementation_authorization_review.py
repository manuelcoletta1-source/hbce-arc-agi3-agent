"""Milestone #19 Task 108 - SRSC controlled artifact emission usage smoke-run implementation authorization review validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_107 = ROOT / "docs" / "milestone-19-task-107-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-planning-v1.md"
DOC_TASK_108 = ROOT / "docs" / "milestone-19-task-108-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-authorization-review-v1.md"
USAGE_RUNNER_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
USAGE_RUNNER_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_usage.py"
MANIFEST = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-authorization-review-v1"
    / "task-108-manifest.json"
)
INDEX = (
    ROOT
    / "examples"
    / "milestone-19"
    / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-authorization-review-v1"
    / "task-108-index.txt"
)


def test_task_108_required_files_exist() -> None:
    assert DOC_TASK_107.exists()
    assert DOC_TASK_108.exists()
    assert USAGE_RUNNER_MODULE.exists()
    assert USAGE_RUNNER_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_108_dependency_markers() -> None:
    text = DOC_TASK_107.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_107_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_READY=true" in text
    assert "MILESTONE_19_TASK_107_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_REQUIRED_NEXT=true" in text
    assert "MILESTONE_19_TASK_107_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_107_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_107_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_107_SOLVER_RUNTIME_BINDING=false" in text


def test_task_108_canonical_markers() -> None:
    text = DOC_TASK_108.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_108_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_108_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_108_MODE=REVIEW_ONLY_NO_SMOKE_RUN_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_108_DECISION=AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_ONLY" in text
    assert "MILESTONE_19_TASK_108_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_108_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_108_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_108_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_108_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_USAGE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_ACTIVATION_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_ADAPTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_108_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_108_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_108_KAGGLE_SUBMISSION_BINDING=false" in text
    assert "MILESTONE_19_TASK_108_FAIL_CLOSED_ACTIVE=true" in text


def test_task_108_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_108_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_SMOKE_RUN_IMPLEMENTATION"
    assert manifest["dependency"] == "MILESTONE_19_TASK_107_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_PLANNING_V1"
    assert manifest["decision"] == "AUTHORIZE_NEXT_TASK_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_ONLY"
    assert manifest["controlledArtifactEmissionUsageSmokeRunImplementationAuthorizationReviewPerformed"] is True
    assert manifest["controlledArtifactEmissionUsageSmokeRunLocalImplementationAuthorizedForNextTask"] is True
    assert manifest["implementationPerformedInTask108"] is False
    assert manifest["artifactEmissionUsageSmokeRunImplementedInTask108"] is False
    assert manifest["usageRunnerModifiedInTask108"] is False
    assert manifest["artifactEmitterModifiedInTask108"] is False
    assert manifest["usageModifiedInTask108"] is False
    assert manifest["activationModifiedInTask108"] is False
    assert manifest["adapterModifiedInTask108"] is False
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


def test_task_108_authorized_future_modules_are_smoke_run_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["authorizedFutureModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py",
        "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py",
    ]
    assert "DiagnosticArtifactEmissionUsageSmokeRunPlan" in manifest["authorizedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunCase" in manifest["authorizedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunResult" in manifest["authorizedFutureTypes"]
    assert "DiagnosticArtifactEmissionUsageSmokeRunSuiteResult" in manifest["authorizedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_smoke_run" in manifest["authorizedFutureTypes"]
    assert "run_controlled_artifact_emission_usage_smoke_run_suite" in manifest["authorizedFutureTypes"]


def test_task_108_authorized_smoke_run_cases_are_diagnostic_only() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    authorized = manifest["authorizedFutureSmokeRunCases"]
    forbidden = manifest["forbiddenFutureSmokeRunCases"]

    assert "happy-path diagnostic report smoke-run" in authorized
    assert "custom artifact bundle smoke-run" in authorized
    assert "deterministic index smoke-run" in authorized
    assert "public-safe audit summary smoke-run" in authorized
    assert "forbidden usage context smoke-run" in authorized
    assert "unknown usage context smoke-run" in authorized
    assert "forbidden artifact family smoke-run" in authorized
    assert "mixed allowed and blocked artifact family smoke-run" in authorized
    assert "batch usage smoke-run" in authorized
    assert "boundary marker smoke-run" in authorized
    assert "no-score and no-submission marker smoke-run" in authorized

    assert "solver runtime smoke-run" in forbidden
    assert "candidate generator smoke-run" in forbidden
    assert "ranker score smoke-run" in forbidden
    assert "verifier score smoke-run" in forbidden
    assert "benchmark smoke-run" in forbidden
    assert "Kaggle submission smoke-run" in forbidden
    assert "legal certification smoke-run" in forbidden


def test_task_108_blocked_bindings_preserve_no_runtime_wiring() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    blocked = manifest["blockedBindings"]

    assert "controlled smoke-run implementation in Task 108" in blocked
    assert "usage runner modification in Task 108" in blocked
    assert "artifact emitter modification in Task 108" in blocked
    assert "usage layer modification in Task 108" in blocked
    assert "activation wrapper modification in Task 108" in blocked
    assert "adapter modification in Task 108" in blocked
    assert "runtime smoke-run wiring" in blocked
    assert "solver runtime binding" in blocked
    assert "candidate generator binding" in blocked
    assert "ranker score binding" in blocked
    assert "verifier binding" in blocked
    assert "benchmark score binding" in blocked
    assert "Kaggle submission binding" in blocked
    assert "legal certification binding" in blocked
