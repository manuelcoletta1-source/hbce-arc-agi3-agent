"""Milestone #19 Task 109 validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_TASK_108 = ROOT / "docs" / "milestone-19-task-108-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-implementation-authorization-review-v1.md"
DOC_TASK_109 = ROOT / "docs" / "milestone-19-task-109-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-local-implementation-v1.md"
POC_DOC = ROOT / "docs" / "srsc-ai-poc-v0-9-bootstrap-reserved-ingress-backoff-governor-reserved-cpu-c1-cancellable-eviction-acceptance-specification.md"
SMOKE_MODULE = ROOT / "src" / "hbce_arc_agi3" / "srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py"
SMOKE_TEST = ROOT / "tests" / "test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-local-implementation-v1" / "task-109-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-local-implementation-v1" / "task-109-index.txt"


def test_task_109_required_files_exist() -> None:
    assert DOC_TASK_108.exists()
    assert DOC_TASK_109.exists()
    assert POC_DOC.exists()
    assert SMOKE_MODULE.exists()
    assert SMOKE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_109_dependency_markers() -> None:
    text = DOC_TASK_108.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_108_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTATION_AUTHORIZATION_REVIEW_READY=true" in text
    assert "MILESTONE_19_TASK_108_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_AUTHORIZED_FOR_NEXT_TASK=true" in text
    assert "MILESTONE_19_TASK_108_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_108_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_108_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_108_SOLVER_RUNTIME_BINDING=false" in text


def test_task_109_poc_v0_9_source_markers() -> None:
    text = POC_DOC.read_text(encoding="utf-8")
    assert "SRSC-AI PoC v0.9 Bootstrap-Reserved Ingress" in text
    assert "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED" in text
    assert "POC-T106 Bootstrap permit single-use and class-isolated ingress slots" in text
    assert "POC-T107 Recovery watchdog exponential backoff and terminal lock" in text
    assert "POC-T108 Reserved CPU/hash budgets across ingress classes" in text
    assert "POC-T109 Volatile C1 cancellation, eviction and health reserve" in text
    assert "POC-T110 No anonymous payload can reserve bootstrap or registered capacity" in text
    assert "POC-T111 Concurrent reuse of same BootstrapPermit" in text
    assert "POC-T112 C1 eviction cancellation is idempotent" in text
    assert "POC-T113 Health reserve survives C1 eviction storm" in text
    assert "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED" in text
    assert "POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "POC_V0_9_BENCHMARKED=false" in text
    assert "POC_V0_9_PRODUCTION_READY=false" in text


def test_task_109_canonical_markers() -> None:
    text = DOC_TASK_109.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_109_STATUS=CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_READY" in text
    assert "MILESTONE_19_TASK_109_MODE=LOCAL_DIAGNOSTIC_ONLY_SMOKE_RUN_NO_RUNTIME_WIRING" in text
    assert "MILESTONE_19_TASK_109_CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_109_DIAGNOSTIC_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_ONLY=true" in text
    assert "MILESTONE_19_TASK_109_USAGE_RUNNER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_ARTIFACT_EMITTER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_109_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_109_SOLVER_RUNTIME_BINDING=false" in text
    assert "MILESTONE_19_TASK_109_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_109_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_109_FAIL_CLOSED_ACTIVE=true" in text
    assert "MILESTONE_19_TASK_109_POC_V0_9_RUNTIME_IMPLEMENTED=false" in text
    assert "MILESTONE_19_TASK_109_POC_V0_9_BENCHMARKED=false" in text
    assert "MILESTONE_19_TASK_109_POC_V0_9_PRODUCTION_READY=false" in text


def test_task_109_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_109_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_V1"
    assert manifest["status"] == "CONTROLLED_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_LOCAL_IMPLEMENTATION_READY"
    assert manifest["mode"] == "LOCAL_DIAGNOSTIC_ONLY_SMOKE_RUN_NO_RUNTIME_WIRING"
    assert manifest["pocV09Status"] == "POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED"
    assert manifest["pocV09Maturity"] == "DESIGNED / NOT_IMPLEMENTED / NOT_TESTED"
    assert manifest["pocV09RuntimeImplemented"] is False
    assert manifest["pocV09Benchmarked"] is False
    assert manifest["pocV09FaultInjectionPerformed"] is False
    assert manifest["pocV09ProductionReady"] is False
    assert manifest["controlledArtifactEmissionUsageSmokeRunImplemented"] is True
    assert manifest["diagnosticArtifactEmissionUsageSmokeRunOnly"] is True
    assert manifest["usageRunnerModified"] is False
    assert manifest["artifactEmitterModified"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["runtimeWiringAllowed"] is False
    assert manifest["solverRuntimeBinding"] is False
    assert manifest["benchmarkScoreClaimed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedActive"] is True


def test_task_109_implemented_module_contract() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["implementedModules"] == [
        "src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py"
    ]
    assert "tests/test_srsc_diagnostic_adapter_activation_usage_artifact_emission_smoke_run.py" in manifest["implementedTests"]
    assert "tests/test_milestone_19_task_109_srsc_diagnostic_adapter_controlled_activation_usage_artifact_emission_usage_smoke_run_local_implementation.py" in manifest["implementedTests"]
