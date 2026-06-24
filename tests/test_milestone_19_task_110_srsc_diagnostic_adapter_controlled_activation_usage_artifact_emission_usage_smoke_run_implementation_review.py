"""Milestone #19 Task 110 - SRSC smoke-run implementation review validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run import (
    BENCHMARK_SCORE_CLAIMED,
    CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED,
    DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY,
    FAIL_CLOSED_ACTIVE,
    KAGGLE_SUBMISSION_SENT,
    LEGAL_CERTIFICATION,
    POC_V0_9_BENCHMARKED,
    POC_V0_9_FAULT_INJECTION_PERFORMED,
    POC_V0_9_MATURITY,
    POC_V0_9_PRODUCTION_READY,
    POC_V0_9_RUNTIME_IMPLEMENTED,
    POC_V0_9_STATUS,
    PRIVATE_CORE_EXPOSURE,
    RUNTIME_SOLVER_MODIFIED,
    RUNTIME_WIRING_ALLOWED,
    SMOKE_RUN_REVISION,
    SOLVER_RUNTIME_BINDING,
    TASK_ID,
    USAGE_RUNNER_MODIFIED,
    run_controlled_artifact_emission_usage_smoke_run_suite,
)


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_109 = ROOT / "docs" / "milestone-19-task-109-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-local-implementation-v1.md"
DOC_TASK_110 = ROOT / "docs" / "milestone-19-task-110-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-review-v1.md"
POC_DOC = ROOT / "docs" / "srsc-ai-poc-v0-9-bootstrap-reserved-ingress-backoff-governor-reserved-cpu-c1-cancellable-eviction-acceptance-specification.md"
SMOKE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py"
SMOKE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-review-v1" / "task-110-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-review-v1" / "task-110-index.txt"


def test_task_110_required_files_exist() -> None:
    assert DOC_TASK_109.exists()
    assert DOC_TASK_110.exists()
    assert POC_DOC.exists()
    assert SMOKE_MODULE.exists()
    assert SMOKE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_110_dependency_markers() -> None:
    text = DOC_TASK_109.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_109_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_109_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY=true" in text
    assert "MILESTONE_19_TASK_109_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_109_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_109_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_109_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_109_POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_109_POC_V0_9_BENCHMARKED=false" in text


def test_task_110_poc_v0_9_remains_specification_only() -> None:
    text = POC_DOC.read_text(encoding="utf-8")
    assert "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED" in text
    assert "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED" in text
    assert "POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "POC_V0_9_BENCHMARKED=false" in text
    assert "POC_V0_9_FAULT_INJECTION_PERFORMED=false" in text
    assert "POC_V0_9_PRODUCTION_READY=false" in text
    assert "POC-T106 Bootstrap permit single-use and class-isolated ingress slots" in text
    assert "POC-T113 Health reserve survives C1 eviction storm" in text


def test_task_110_smoke_run_module_contract_is_reviewed_without_modification() -> None:
    suite = run_controlled_artifact_emission_usage_smoke_run_suite()

    assert TASK_ID == "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_V1"
    assert SMOKE_RUN_REVISION == "SRSC_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_STANDALONE_V1"
    assert suite.suite_ok is True
    assert suite.case_count == 8
    assert suite.passed_count == 8
    assert suite.failed_count == 0

    assert CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED is True
    assert DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY is True
    assert USAGE_RUNNER_MODIFIED is False
    assert RUNTIME_SOLVER_MODIFIED is False
    assert RUNTIME_WIRING_ALLOWED is False
    assert SOLVER_RUNTIME_BINDING is False
    assert BENCHMARK_SCORE_CLAIMED is False
    assert KAGGLE_SUBMISSION_SENT is False
    assert PRIVATE_CORE_EXPOSURE is False
    assert LEGAL_CERTIFICATION is False
    assert FAIL_CLOSED_ACTIVE is True

    assert POC_V0_9_STATUS == "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
    assert POC_V0_9_MATURITY == "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED"
    assert POC_V0_9_RUNTIME_IMPLEMENTED is False
    assert POC_V0_9_BENCHMARKED is False
    assert POC_V0_9_FAULT_INJECTION_PERFORMED is False
    assert POC_V0_9_PRODUCTION_READY is False


def test_task_110_canonical_markers() -> None:
    text = DOC_TASK_110.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_110_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_110_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_REVIEW_READY" in text
    assert "MILESTONE_19_TASK_110_MODE=REVIEW_ONLY_NO_SMOKE_RUN_MODIFICATION" in text
    assert "MILESTONE_19_TASK_110_DECISION=ACCEPT_TASK_109_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION" in text
    assert "MILESTONE_19_TASK_110_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_REVIEW_PERFORMED=true" in text
    assert "MILESTONE_19_TASK_110_TASK_109_SMOKE_RUN_IMPLEMENTATION_ACCEPTED=true" in text
    assert "MILESTONE_19_TASK_110_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_110_SMOKE_RUN_MODULE_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_110_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_110_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_110_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_110_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_110_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_110_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_110_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_110_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_110_POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_110_POC_V0_9_BENCHMARKED=false" in text
    assert "MILESTONE_19_TASK_110_POC_V0_9_PRODUCTION_READY=false" in text


def test_task_110_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_110_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_REVIEW_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_REVIEW_READY"
    assert manifest["mode"] == "REVIEW_ONLY_NO_SMOKE_RUN_MODIFICATION"
    assert manifest["decision"] == "ACCEPT_TASK_109_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION"
    assert manifest["controlledArtifactEmissionUsageSmokeRunImplementationReviewPerformed"] is True
    assert manifest["task109SmokeRunImplementationAccepted"] is True
    assert manifest["implementationPerformedInTask110"] is False
    assert manifest["smokeRunModuleModifiedInTask110"] is False
    assert manifest["usageRunnerModifiedInTask110"] is False
    assert manifest["artifactEmitterModifiedInTask110"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["solverRuntimeBinding"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedActive"] is True
    assert manifest["pocV09RuntimeImplemented"] is False
    assert manifest["pocV09Benchmarked"] is False
    assert manifest["pocV09FaultInjectionPerformed"] is False
    assert manifest["pocV09ProductionReady"] is False
