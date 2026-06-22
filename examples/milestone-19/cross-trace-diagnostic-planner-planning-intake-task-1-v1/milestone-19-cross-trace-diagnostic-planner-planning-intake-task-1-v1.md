# Milestone 19 Task 1 - Cross-Trace Diagnostic Planner Planning Intake v1

- Task: `MILESTONE_19_TASK_1_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_V1`
- Planning intake ID: `MILESTONE-19-TASK-1-CROSS-TRACE-DIAGNOSTIC-PLANNER-PLANNING-INTAKE-8EEA061B18EC2B9A`
- Signature: `8EEA061B18EC2B9A`
- Previous milestone: `MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT`
- Previous closure commit: `287d1d9`
- Previous closure signature: `811221A25BFEB5AF`
- Verdict: `MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_PLANNING_INTAKE_READY_IMPLEMENTATION_BLOCKED`
- Implementation status: `PLANNING_ALLOWED_IMPLEMENTATION_BLOCKED_RUNTIME_BLOCKED_EVALUATION_BLOCKED_SUBMISSION_BLOCKED`
- Next stage: `MILESTONE_19_TASK_2_CROSS_TRACE_DIAGNOSTIC_PLANNER_SPEC_REVIEW_V1`

## Purpose

Milestone 19 opens the Cross-Trace Diagnostic Planner as a planning-only R&D layer. It prepares deterministic diagnostic records for later separately authorized candidate generation and verification.

## Pipeline Model

- `task_parser`
- `deterministic_feature_extractor`
- `cross_trace_diagnostic_planner`
- `authorized_candidate_generator`
- `existing_verifier`
- `ranker_or_benchmark_report`

## Feature Families

- `color`
- `geometry`
- `position`
- `count`
- `transformation`
- `invariance`
- `contradiction`
- `complexity`

## Required Output Fields

- `diagnosticId`
- `taskId`
- `sourceScope`
- `observation`
- `evidence`
- `hypothesis`
- `invariants`
- `contradictions`
- `confidence`
- `verificationStatus`
- `candidateInterface`
- `boundary`

## Boundary

- planning_only: true
- implementation_authorized: false
- runtime_activation_performed: false
- runtime_solver_modified: false
- real_evaluation_performed: false
- kaggle_submission_sent: false
- internet_during_eval: false
- external_api_dependency: false
- private_core_exposure: false
- operator_approval_required: true
- operator_approval_received: false
- fail_closed_active: true

## Test Plan

- `CTDP-T1`: deterministic_feature_extraction -> same_training_pair_yields_identical_snapshot_and_hash
- `CTDP-T2`: cross_pair_relation_classification -> known_fixture_relations_classified_correctly
- `CTDP-T3`: contradiction_handling -> candidate_failing_one_training_pair_is_not_marked_consistent
- `CTDP-T4`: boundary_enforcement -> network_external_source_hidden_label_private_core_paths_denied
- `CTDP-T5`: candidate_handoff_integrity -> diagnostic_record_preserves_source_pair_refs_and_cannot_alter_verifier_output
- `CTDP-T6`: regression_and_determinism -> same_fixtures_version_seed_produce_same_diagnostic_records

## Acceptance

- Acceptance gate count: `50`
- Acceptance gate failures: `0`

Task 1 stores the planner as a planning intake artifact only. It does not authorize implementation, runtime activation, evaluation, upload, or submission.
