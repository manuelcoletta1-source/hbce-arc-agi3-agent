"""Milestone #19 Task 142 final closure and recursion guard validation."""

from __future__ import annotations

import json
from pathlib import Path

from hbce_arc_agi3.milestone_task_budget_governance import (
    MILESTONE_19_ACTUAL_TASK_COUNT,
    build_milestone_19_final_closure,
    build_standard_milestone_policy,
    validate_milestone_19_final_closure,
)


ROOT = Path(__file__).resolve().parents[1]

DOC = ROOT / "docs" / "milestone-19-task-142-final-closure-and-recursion-guard-v1.md"
MODULE = ROOT / "src" / "hbce_arc_agi3" / "milestone_task_budget_governance.py"
MODULE_TEST = ROOT / "tests" / "test_milestone_task_budget_governance.py"
MANIFEST = ROOT / "examples" / "milestone-19" / "final-closure-and-recursion-guard-v1" / "task-142-manifest.json"
INDEX = ROOT / "examples" / "milestone-19" / "final-closure-and-recursion-guard-v1" / "task-142-index.txt"
JSON_ARTIFACT = ROOT / "examples" / "milestone-19" / "final-closure-and-recursion-guard-v1" / "task-142-milestone-19-final-closure.json"
MD_ARTIFACT = ROOT / "examples" / "milestone-19" / "final-closure-and-recursion-guard-v1" / "task-142-milestone-19-final-closure.md"
TASK_141_DOC = ROOT / "docs" / "milestone-19-task-141-srsc-diagnostic-adapter-controlled-activation-usage-artifact-emission-usage-smoke-run-result-archive-closure-final-chain-closure-final-review-archive-closure-finalization-local-implementation-v1.md"


def test_task_142_files_exist() -> None:
    assert DOC.exists()
    assert MODULE.exists()
    assert MODULE_TEST.exists()
    assert MANIFEST.exists()
    assert INDEX.exists()
    assert JSON_ARTIFACT.exists()
    assert MD_ARTIFACT.exists()
    assert TASK_141_DOC.exists()


def test_task_142_dependency_task_141_is_closed() -> None:
    text = TASK_141_DOC.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_141_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_ARTIFACT_EMISSION_USAGE_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_LOCAL_IMPLEMENTATION_READY=true" in text
    assert "MILESTONE_19_TASK_141_CONTROLLED_SMOKE_RUN_RESULT_ARCHIVE_CLOSURE_FINAL_CHAIN_CLOSURE_FINAL_REVIEW_ARCHIVE_CLOSURE_FINALIZATION_IMPLEMENTED=true" in text
    assert "MILESTONE_19_TASK_141_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_141_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_141_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_141_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_141_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_141_LEGAL_CERTIFICATION=false" in text


def test_task_142_final_closure_contract() -> None:
    closure = build_milestone_19_final_closure()

    assert MILESTONE_19_ACTUAL_TASK_COUNT == 63
    assert closure.closure_ok is True
    assert closure.technical_status == "PASS"
    assert closure.process_status == "OVERSIZED_RECURSIVE_CORRECTED"
    assert closure.final_status == "CLOSED_WITH_PROCESS_CORRECTION"
    assert closure.rewrite_required is False
    assert closure.rollback_required is False
    assert closure.continue_recursive_tasks is False
    assert closure.future_budget_policy_required is True
    assert closure.no_recursive_meta_layer_required is True
    assert closure.closure_required_for_future_milestones is True
    assert validate_milestone_19_final_closure(closure) == ()


def test_task_142_future_policy_is_bounded() -> None:
    policy = build_standard_milestone_policy(
        milestone_id="MILESTONE_20",
        objective="Governed execution after Milestone 19 closure",
        stop_condition="task budget declared, implementation tested, full suite passed, closure committed and pushed",
    )

    assert policy.valid is True
    assert policy.task_budget_max == 8
    assert policy.max_review_depth == 1
    assert policy.max_authorization_depth == 1
    assert policy.max_finalization_depth == 1
    assert policy.no_recursive_meta_layer is True
    assert policy.closure_required is True


def test_task_142_canonical_markers() -> None:
    text = DOC.read_text(encoding="utf-8")
    assert "MILESTONE_19_TASK_142_FINAL_CLOSURE_AND_RECURSION_GUARD_READY=true" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_TECHNICAL_STATUS=PASS" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_PROCESS_STATUS=OVERSIZED_RECURSIVE_CORRECTED" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_FINAL_STATUS=CLOSED_WITH_PROCESS_CORRECTION" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_REWRITE_REQUIRED=false" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_ROLLBACK_REQUIRED=false" in text
    assert "MILESTONE_19_TASK_142_MILESTONE_19_CONTINUE_RECURSIVE_TASKS=false" in text
    assert "MILESTONE_19_TASK_142_FUTURE_BUDGET_POLICY_REQUIRED=true" in text
    assert "MILESTONE_19_TASK_142_NO_RECURSIVE_META_LAYER_REQUIRED=true" in text
    assert "MILESTONE_19_TASK_142_STANDARD_MILESTONE_TASK_MAX=8" in text
    assert "MILESTONE_19_TASK_142_COMPLEX_MILESTONE_TASK_MAX=12" in text
    assert "MILESTONE_19_TASK_142_EXCEPTIONAL_MILESTONE_TASK_MAX=15" in text
    assert "MILESTONE_19_TASK_142_MAX_REVIEW_DEPTH=1" in text
    assert "MILESTONE_19_TASK_142_MAX_AUTHORIZATION_DEPTH=1" in text
    assert "MILESTONE_19_TASK_142_MAX_FINALIZATION_DEPTH=1" in text
    assert "MILESTONE_19_TASK_142_RUNTIME_SOLVER_MODIFIED=false" in text
    assert "MILESTONE_19_TASK_142_RUNTIME_WIRING_ALLOWED=false" in text
    assert "MILESTONE_19_TASK_142_KAGGLE_SUBMISSION_SENT=false" in text
    assert "MILESTONE_19_TASK_142_RAW_REQUEST_BODY_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_142_SECRET_PERSISTED=false" in text
    assert "MILESTONE_19_TASK_142_LEGAL_CERTIFICATION=false" in text
    assert "MILESTONE_19_TASK_142_NEXT_STAGE=MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8" in text


def test_task_142_manifest_and_artifact() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = json.loads(JSON_ARTIFACT.read_text(encoding="utf-8"))

    assert manifest["taskId"] == "MILESTONE_19_TASK_142_FINAL_CLOSURE_AND_RECURSION_GUARD_V1"
    assert manifest["technicalStatus"] == "PASS"
    assert manifest["processStatus"] == "OVERSIZED_RECURSIVE_CORRECTED"
    assert manifest["finalStatus"] == "CLOSED_WITH_PROCESS_CORRECTION"
    assert manifest["actualTaskCount"] == 63
    assert manifest["rewriteRequired"] is False
    assert manifest["rollbackRequired"] is False
    assert manifest["continueRecursiveTasks"] is False
    assert manifest["futureBudgetPolicyRequired"] is True
    assert manifest["standardMilestoneTaskMax"] == 8
    assert manifest["complexMilestoneTaskMax"] == 12
    assert manifest["exceptionalMilestoneTaskMax"] == 15
    assert artifact["continueRecursiveTasks"] is False
    assert artifact["recommendedNextMode"] == "MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8"
