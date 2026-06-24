"""Milestone task budget governance.

This module prevents ARC-AGI/HBCE milestones from turning into recursive
audit-machines. A milestone must now declare a task budget, a stop condition,
and hard limits for review/authorization/finalization depth.

The embarrassing lesson from Milestone #19 is preserved instead of rewritten:
technical PASS, process OVERSIZED, corrected by governance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from typing import Any, Mapping


TASK_ID = "MILESTONE_19_TASK_142_FINAL_CLOSURE_AND_RECURSION_GUARD_V1"
REVISION = "MILESTONE_TASK_BUDGET_GOVERNANCE_v1"

SMALL_MILESTONE_TASK_MAX = 5
STANDARD_MILESTONE_TASK_MAX = 8
COMPLEX_MILESTONE_TASK_MAX = 12
EXCEPTIONAL_MILESTONE_TASK_MAX = 15

DEFAULT_MAX_REVIEW_DEPTH = 1
DEFAULT_MAX_AUTHORIZATION_DEPTH = 1
DEFAULT_MAX_FINALIZATION_DEPTH = 1

MILESTONE_19_FIRST_SRSC_TASK = 79
MILESTONE_19_LAST_SRSC_TASK = 141
MILESTONE_19_ACTUAL_TASK_COUNT = MILESTONE_19_LAST_SRSC_TASK - MILESTONE_19_FIRST_SRSC_TASK + 1

MILESTONE_19_TECHNICAL_STATUS = "PASS"
MILESTONE_19_PROCESS_STATUS = "OVERSIZED_RECURSIVE_CORRECTED"
MILESTONE_19_FINAL_STATUS = "CLOSED_WITH_PROCESS_CORRECTION"
MILESTONE_19_REWRITE_REQUIRED = False
MILESTONE_19_ROLLBACK_REQUIRED = False
MILESTONE_19_CONTINUE_RECURSIVE_TASKS = False

FUTURE_MILESTONE_TASK_BUDGET_REQUIRED = True
NO_RECURSIVE_META_LAYER_REQUIRED = True
CLOSURE_REQUIRED = True


def _digest(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
    return sha256(encoded).hexdigest()[:16].upper()


def classify_task_budget(task_budget_max: int) -> str:
    if task_budget_max <= SMALL_MILESTONE_TASK_MAX:
        return "SMALL"
    if task_budget_max <= STANDARD_MILESTONE_TASK_MAX:
        return "STANDARD"
    if task_budget_max <= COMPLEX_MILESTONE_TASK_MAX:
        return "COMPLEX"
    if task_budget_max <= EXCEPTIONAL_MILESTONE_TASK_MAX:
        return "EXCEPTIONAL"
    return "INVALID_OVERSIZED"


@dataclass(frozen=True)
class MilestoneTaskBudgetPolicy:
    milestone_id: str
    objective: str
    task_budget_min: int
    task_budget_max: int
    stop_condition: str
    closure_required: bool = True
    no_recursive_meta_layer: bool = True
    max_review_depth: int = DEFAULT_MAX_REVIEW_DEPTH
    max_authorization_depth: int = DEFAULT_MAX_AUTHORIZATION_DEPTH
    max_finalization_depth: int = DEFAULT_MAX_FINALIZATION_DEPTH
    exceptional_budget_justification: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def budget_class(self) -> str:
        return classify_task_budget(self.task_budget_max)

    @property
    def policy_id(self) -> str:
        return f"MILESTONE-BUDGET-POLICY-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def issues(self) -> tuple[str, ...]:
        issues: list[str] = []

        if not self.milestone_id.strip():
            issues.append("MILESTONE_ID_EMPTY")
        if not self.objective.strip():
            issues.append("OBJECTIVE_EMPTY")
        if self.task_budget_min < 1:
            issues.append("TASK_BUDGET_MIN_INVALID")
        if self.task_budget_max < self.task_budget_min:
            issues.append("TASK_BUDGET_MAX_BELOW_MIN")
        if self.task_budget_max > EXCEPTIONAL_MILESTONE_TASK_MAX:
            issues.append("TASK_BUDGET_MAX_EXCEEDS_EXCEPTIONAL_LIMIT")
        if self.task_budget_max > COMPLEX_MILESTONE_TASK_MAX and not self.exceptional_budget_justification.strip():
            issues.append("EXCEPTIONAL_BUDGET_REQUIRES_JUSTIFICATION")
        if not self.stop_condition.strip():
            issues.append("STOP_CONDITION_EMPTY")
        if not self.closure_required:
            issues.append("CLOSURE_NOT_REQUIRED")
        if not self.no_recursive_meta_layer:
            issues.append("RECURSIVE_META_LAYER_ALLOWED")
        if self.max_review_depth > 1:
            issues.append("MAX_REVIEW_DEPTH_EXCEEDS_1")
        if self.max_authorization_depth > 1:
            issues.append("MAX_AUTHORIZATION_DEPTH_EXCEEDS_1")
        if self.max_finalization_depth > 1:
            issues.append("MAX_FINALIZATION_DEPTH_EXCEEDS_1")

        return tuple(issues)

    @property
    def valid(self) -> bool:
        return self.issues == ()

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "milestoneId": self.milestone_id,
            "objective": self.objective,
            "taskBudgetMin": self.task_budget_min,
            "taskBudgetMax": self.task_budget_max,
            "budgetClass": self.budget_class,
            "stopCondition": self.stop_condition,
            "closureRequired": self.closure_required,
            "noRecursiveMetaLayer": self.no_recursive_meta_layer,
            "maxReviewDepth": self.max_review_depth,
            "maxAuthorizationDepth": self.max_authorization_depth,
            "maxFinalizationDepth": self.max_finalization_depth,
            "exceptionalBudgetJustification": self.exceptional_budget_justification,
            "valid": self.valid,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
            "revision": REVISION,
        }
        if include_id:
            payload["policyId"] = self.policy_id
        return payload


@dataclass(frozen=True)
class MilestoneFinalClosure:
    milestone_id: str
    technical_status: str
    process_status: str
    final_status: str
    actual_task_count: int
    first_task: int
    last_task: int
    rewrite_required: bool
    rollback_required: bool
    continue_recursive_tasks: bool
    future_budget_policy_required: bool
    no_recursive_meta_layer_required: bool
    closure_required_for_future_milestones: bool
    recommended_next_mode: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def closure_id(self) -> str:
        return f"MILESTONE-FINAL-CLOSURE-{_digest(self.to_public_dict(include_id=False))}"

    @property
    def closure_ok(self) -> bool:
        return (
            self.technical_status == "PASS"
            and self.final_status == "CLOSED_WITH_PROCESS_CORRECTION"
            and self.rewrite_required is False
            and self.rollback_required is False
            and self.continue_recursive_tasks is False
            and self.future_budget_policy_required is True
            and self.no_recursive_meta_layer_required is True
            and self.closure_required_for_future_milestones is True
        )

    @property
    def issues(self) -> tuple[str, ...]:
        issues: list[str] = []
        if self.technical_status != "PASS":
            issues.append("TECHNICAL_STATUS_NOT_PASS")
        if self.final_status != "CLOSED_WITH_PROCESS_CORRECTION":
            issues.append("FINAL_STATUS_NOT_CLOSED_WITH_PROCESS_CORRECTION")
        if self.rewrite_required:
            issues.append("REWRITE_SHOULD_NOT_BE_REQUIRED")
        if self.rollback_required:
            issues.append("ROLLBACK_SHOULD_NOT_BE_REQUIRED")
        if self.continue_recursive_tasks:
            issues.append("RECURSIVE_TASK_CONTINUATION_NOT_ALLOWED")
        if not self.future_budget_policy_required:
            issues.append("FUTURE_BUDGET_POLICY_NOT_REQUIRED")
        if not self.no_recursive_meta_layer_required:
            issues.append("NO_RECURSIVE_META_LAYER_NOT_REQUIRED")
        if not self.closure_required_for_future_milestones:
            issues.append("FUTURE_CLOSURE_NOT_REQUIRED")
        return tuple(issues)

    def to_public_dict(self, *, include_id: bool = True) -> dict[str, Any]:
        payload = {
            "milestoneId": self.milestone_id,
            "technicalStatus": self.technical_status,
            "processStatus": self.process_status,
            "finalStatus": self.final_status,
            "actualTaskCount": self.actual_task_count,
            "firstTask": self.first_task,
            "lastTask": self.last_task,
            "rewriteRequired": self.rewrite_required,
            "rollbackRequired": self.rollback_required,
            "continueRecursiveTasks": self.continue_recursive_tasks,
            "futureBudgetPolicyRequired": self.future_budget_policy_required,
            "noRecursiveMetaLayerRequired": self.no_recursive_meta_layer_required,
            "closureRequiredForFutureMilestones": self.closure_required_for_future_milestones,
            "recommendedNextMode": self.recommended_next_mode,
            "closureOk": self.closure_ok,
            "issues": list(self.issues),
            "metadata": dict(sorted(self.metadata.items())),
            "revision": REVISION,
        }
        if include_id:
            payload["closureId"] = self.closure_id
        return payload


def build_standard_milestone_policy(
    *,
    milestone_id: str,
    objective: str,
    stop_condition: str,
    task_budget_min: int = 4,
    task_budget_max: int = STANDARD_MILESTONE_TASK_MAX,
    metadata: Mapping[str, Any] | None = None,
) -> MilestoneTaskBudgetPolicy:
    return MilestoneTaskBudgetPolicy(
        milestone_id=milestone_id,
        objective=objective,
        task_budget_min=task_budget_min,
        task_budget_max=task_budget_max,
        stop_condition=stop_condition,
        closure_required=True,
        no_recursive_meta_layer=True,
        max_review_depth=1,
        max_authorization_depth=1,
        max_finalization_depth=1,
        metadata={} if metadata is None else metadata,
    )


def build_milestone_19_final_closure() -> MilestoneFinalClosure:
    return MilestoneFinalClosure(
        milestone_id="MILESTONE_19",
        technical_status=MILESTONE_19_TECHNICAL_STATUS,
        process_status=MILESTONE_19_PROCESS_STATUS,
        final_status=MILESTONE_19_FINAL_STATUS,
        actual_task_count=MILESTONE_19_ACTUAL_TASK_COUNT,
        first_task=MILESTONE_19_FIRST_SRSC_TASK,
        last_task=MILESTONE_19_LAST_SRSC_TASK,
        rewrite_required=MILESTONE_19_REWRITE_REQUIRED,
        rollback_required=MILESTONE_19_ROLLBACK_REQUIRED,
        continue_recursive_tasks=MILESTONE_19_CONTINUE_RECURSIVE_TASKS,
        future_budget_policy_required=FUTURE_MILESTONE_TASK_BUDGET_REQUIRED,
        no_recursive_meta_layer_required=NO_RECURSIVE_META_LAYER_REQUIRED,
        closure_required_for_future_milestones=CLOSURE_REQUIRED,
        recommended_next_mode="MILESTONE_20_GOVERNED_EXECUTION_WITH_TASK_BUDGET_MAX_8",
        metadata={
            "reason": "Milestone 19 technical chain passed but process became oversized and recursive.",
            "correction": "Do not rewrite milestone 19; freeze it and enforce future milestone task budgets.",
        },
    )


def validate_milestone_19_final_closure(closure: MilestoneFinalClosure) -> tuple[str, ...]:
    return closure.issues


__all__ = [
    "TASK_ID",
    "REVISION",
    "SMALL_MILESTONE_TASK_MAX",
    "STANDARD_MILESTONE_TASK_MAX",
    "COMPLEX_MILESTONE_TASK_MAX",
    "EXCEPTIONAL_MILESTONE_TASK_MAX",
    "MILESTONE_19_ACTUAL_TASK_COUNT",
    "MilestoneTaskBudgetPolicy",
    "MilestoneFinalClosure",
    "build_standard_milestone_policy",
    "build_milestone_19_final_closure",
    "classify_task_budget",
    "validate_milestone_19_final_closure",
]
