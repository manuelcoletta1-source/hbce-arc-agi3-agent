# ARC AGI3 Milestone #7 - Baseline Solver Failure Taxonomy v1

- status: MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_READY
- taxonomy_id: MILESTONE-7-FAILURE-TAXONOMY-2F64CB679DF9
- signature: 2F64CB679DF90127
- baseline_commit: 70a8d44 Open ARC AGI3 milestone 7 competitive solver improvement
- taxonomy_mode: BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD
- taxonomy_scope: CLASSIFY_CURRENT_SOLVER_FAILURES_FOR_MEASURABLE_IMPROVEMENT
- taxonomy_verdict: BASELINE_FAILURE_TAXONOMY_READY_SOLVER_IMPROVEMENT_REQUIRED
- next_allowed_stage: MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION
- failure_class_count: 7
- open_failure_count: 7
- closed_failure_count: 0
- priority_p0_count: 4
- target_task_count: 5
- taxonomy_gate_count: 40
- passed_gate_count: 40
- taxonomy_issue_count: 0
- taxonomy_ready: True
- taxonomy_locked: True
- real_submission_allowed: False
- kaggle_submission_sent: False
- upload_performed: False

## Failure classes

- P0 color_transform_undercoverage / family=color_mapping / target=Task 3 Task-Family Solver Expansion v1 / measurement=Increase exact or partial match rate on deterministic color-family local cases.
- P0 object_segmentation_undercoverage / family=object_model / target=Task 3 Task-Family Solver Expansion v1 / measurement=Track object-family cases and verify deterministic object-aware candidate selection.
- P0 spatial_symmetry_undercoverage / family=shape_symmetry / target=Task 3 Task-Family Solver Expansion v1 / measurement=Improve deterministic local matches on symmetry and geometry families.
- P0 candidate_generator_low_diversity / family=candidate_generation / target=Task 4 Candidate Generator Improvement v1 / measurement=Increase deterministic valid candidate count while keeping full test suite green.
- P1 ranker_evidence_weakness / family=candidate_ranking / target=Task 5 Ranker Evidence Upgrade v1 / measurement=Show improved top-1 candidate selection on deterministic local benchmark cases.
- P1 regression_guard_incomplete / family=regression_safety / target=Task 6 Regression Benchmark v1 / measurement=Full suite remains green and old deterministic artifacts remain compatible.
- P2 competitive_score_evidence_absent / family=competitive_readiness / target=Task 7 Local Score Improvement Report v1 / measurement=Produce a local improvement report with before/after metrics and no unsupported claim.

## Decision

Baseline solver failures are classified. Next step is task-family solver expansion.

## Markers

ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_V1_READY=true
ARC_AGI3_MILESTONE_7_BASELINE_SOLVER_FAILURE_TAXONOMY_VALID=true
ARC_AGI3_MILESTONE_7_TAXONOMY_MODE=BASELINE_SOLVER_FAILURE_TAXONOMY_ONLY_NO_UPLOAD
ARC_AGI3_MILESTONE_7_TAXONOMY_VERDICT=BASELINE_FAILURE_TAXONOMY_READY_SOLVER_IMPROVEMENT_REQUIRED
ARC_AGI3_MILESTONE_7_FAILURE_CLASS_COUNT=7
ARC_AGI3_MILESTONE_7_OPEN_FAILURE_COUNT=7
ARC_AGI3_MILESTONE_7_CLOSED_FAILURE_COUNT=0
ARC_AGI3_MILESTONE_7_PRIORITY_P0_COUNT=4
ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_3_TASK_FAMILY_SOLVER_EXPANSION
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false
ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false
ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false
ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false
ARC_AGI3_MILESTONE_7_BASELINE_PLAN_COMMIT=70a8d44
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
