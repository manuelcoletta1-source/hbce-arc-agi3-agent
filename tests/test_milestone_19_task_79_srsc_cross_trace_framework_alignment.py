"""Milestone #19 Task 79 - SRSC + Cross-Trace Framework Alignment validation."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DOC_SRSC = ROOT / "docs" / "srsc-ai-framework-anti-allucinazioni-v1-0.md"
DOC_CROSS = ROOT / "docs" / "arc-agi3-cross-trace-diagnostic-planner-v1.md"
DOC_TASK = ROOT / "docs" / "milestone-19-task-79-srsc-cross-trace-framework-alignment-v1.md"
MANIFEST = ROOT / "examples" / "milestone-19" / "srsc-cross-trace-framework-alignment-v1" / "task-79-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "srsc-cross-trace-framework-alignment-v1" / "task-79-index.txt"


def test_task_79_documents_exist() -> None:
    assert DOC_SRSC.exists()
    assert DOC_CROSS.exists()
    assert DOC_TASK.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()


def test_task_79_canonical_markers() -> None:
    text = DOC_TASK.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_79_SRSC_CROSS_TRACE_FRAMEWORK_ALIGNMENT_READY=true" in text
    assert "MILESTONE_19_TASK_79_STATUS=PLANNING_READY_DOCUMENTATION_ALIGNED" in text
    assert "MILESTONE_19_TASK_79_IMPLEMENTATION_PERFORMED=false" in text
    assert "MILESTONE_19_TASK_79_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_79_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_79_FAIL_CLOSED_ACTIVE=true" in text


def test_task_79_srsc_framework_boundary() -> None:
    text = DOC_SRSC.read_text(encoding="utf-8")
    assert "SRSC_AI_FRAMEWORK_ANTI_ALLUCINAZIONI_V1_0_READY=true" in text
    assert "SRSC_AI_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "SRSC_AI_LEGAL_CERTIFICATION=false" in text
    assert "SRSC_AI_FAIL_CLOSED_ACTIVE=true" in text


def test_task_79_cross_trace_boundary() -> None:
    text = DOC_CROSS.read_text(encoding="utf-8")
    assert "ARC_AGI3_CROSS_TRACE_DIAGNOSTIC_PLANNER_V1_READY=true" in text
    assert "ARC_AGI3_CROSS_TRACE_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "ARC_AGI3_CROSS_TRACE_REAL_EVALUATION_PERFORMED=false" in text
    assert "ARC_AGI3_CROSS_TRACE_KAGGLE_SUBMISSION_SENT=false" in text


def test_task_79_manifest_boundary() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["taskId"] == "MILESTONE_19_TASK_79_SRSC_CROSS_TRACE_FRAMEWORK_ALIGNMENT_V1"
    assert manifest["status"] == "PLANNING_READY_DOCUMENTATION_ALIGNED"
    assert manifest["mode"] == "DOCUMENTATION_AND_FRAMEWORK_ALIGNMENT_ONLY"
    assert manifest["implementationAuthorized"] is False
    assert manifest["implementationPerformed"] is False
    assert manifest["runtimeActivationAuthorized"] is False
    assert manifest["runtimeSolverModified"] is False
    assert manifest["realEvaluationPerformed"] is False
    assert manifest["kaggleSubmissionSent"] is False
    assert manifest["internetDuringEval"] is False
    assert manifest["externalApiDependency"] is False
    assert manifest["privateCoreExposure"] is False
    assert manifest["legalCertification"] is False
    assert manifest["failClosedRequired"] is True
    assert manifest["failClosedActive"] is True
