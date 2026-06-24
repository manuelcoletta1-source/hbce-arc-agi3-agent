"""Tests for milestone task budget governance."""

from __future__ import annotations

from hbce_arc_agi3.milestone_task_budget_governance import (
    COMPLEX_MILESTONE_TASK_MAX,
    EXCEPTIONAL_MILESTONE_TASK_MAX,
    MILESTONE_19_ACTUAL_TASK_COUNT,
    REVISION,
    STANDARD_MILESTONE_TASK_MAX,
    TASK_ID,
    MilestoneTaskBudgetPolicy,
    build_milestone_19_final_closure,
    build_standard_milestone_policy,
    classify_task_budget,
    validate_milestone_19_final_closure,
)


def test_task_budget_classes_are_deterministic() -> None:
    assert classify_task_budget(5) == "SMALL"
    assert classify_task_budget(8) == "STANDARD"
    assert classify_task_budget(12) == "COMPLEX"
    assert classify_task_budget(15) == "EXCEPTIONAL"
    assert classify_task_budget(16) == "INVALID_OVERSIZED"


def test_standard_milestone_policy_is_valid() -> None:
    policy = build_standard_milestone_policy(
        milestone_id="MILESTONE_20",
        objective="Explicit operator decision value selection gate",
        stop_condition="operator decision gate validated, documented, tested, committed and pushed",
    )

    assert policy.valid is True
    assert policy.issues == ()
    assert policy.task_budget_max == STANDARD_MILESTONE_TASK_MAX
    assert policy.max_review_depth == 1
    assert policy.max_authorization_depth == 1
    assert policy.max_finalization_depth == 1
    assert policy.no_recursive_meta_layer is True
    assert policy.closure_required is True
    assert policy.policy_id.startswith("MILESTONE-BUDGET-POLICY-")


def test_invalid_recursive_policy_is_rejected() -> None:
    policy = MilestoneTaskBudgetPolicy(
        milestone_id="MILESTONE_BAD",
        objective="Recursive audit maze",
        task_budget_min=1,
        task_budget_max=16,
        stop_condition="never",
        closure_required=False,
        no_recursive_meta_layer=False,
        max_review_depth=3,
        max_authorization_depth=2,
        max_finalization_depth=2,
    )

    assert policy.valid is False
    assert "TASK_BUDGET_MAX_EXCEEDS_EXCEPTIONAL_LIMIT" in policy.issues
    assert "CLOSURE_NOT_REQUIRED" in policy.issues
    assert "RECURSIVE_META_LAYER_ALLOWED" in policy.issues
    assert "MAX_REVIEW_DEPTH_EXCEEDS_1" in policy.issues
    assert "MAX_AUTHORIZATION_DEPTH_EXCEEDS_1" in policy.issues
    assert "MAX_FINALIZATION_DEPTH_EXCEEDS_1" in policy.issues


def test_milestone_19_final_closure_freezes_without_rewrite() -> None:
    closure = build_milestone_19_final_closure()

    assert TASK_ID == "MILESTONE_19_TASK_142_FINAL_CLOSURE_AND_RECURSION_GUARD_V1"
    assert REVISION == "MILESTONE_TASK_BUDGET_GOVERNANCE_v1"
    assert MILESTONE_19_ACTUAL_TASK_COUNT == 63
    assert closure.milestone_id == "MILESTONE_19"
    assert closure.technical_status == "PASS"
    assert closure.process_status == "OVERSIZED_RECURSIVE_CORRECTED"
    assert closure.final_status == "CLOSED_WITH_PROCESS_CORRECTION"
    assert closure.actual_task_count == 63
    assert closure.first_task == 79
    assert closure.last_task == 141
    assert closure.rewrite_required is False
    assert closure.rollback_required is False
    assert closure.continue_recursive_tasks is False
    assert closure.future_budget_policy_required is True
    assert closure.no_recursive_meta_layer_required is True
    assert closure.closure_required_for_future_milestones is True
    assert closure.closure_ok is True
    assert validate_milestone_19_final_closure(closure) == ()


def test_public_payload_contains_future_limits() -> None:
    closure = build_milestone_19_final_closure()
    payload = closure.to_public_dict()

    assert payload["closureOk"] is True
    assert payload["technicalStatus"] == "PASS"
    assert payload["processStatus"] == "OVERSIZED_RECURSIVE_CORRECTED"
    assert payload["rewriteRequired"] is False
    assert payload["rollbackRequired"] is False
    assert payload["continueRecursiveTasks"] is False
    assert payload["futureBudgetPolicyRequired"] is True
    assert payload["noRecursiveMetaLayerRequired"] is True
    assert payload["closureRequiredForFutureMilestones"] is True
    assert payload["recommendedNextMode"] == "MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8"
    assert payload["closureId"].startswith("MILESTONE-FINAL-CLOSURE-")


def test_budget_max_constants() -> None:
    assert STANDARD_MILESTONE_TASK_MAX == 8
    assert COMPLEX_MILESTONE_TASK_MAX == 12
    assert EXCEPTIONAL_MILESTONE_TASK_MAX == 15
