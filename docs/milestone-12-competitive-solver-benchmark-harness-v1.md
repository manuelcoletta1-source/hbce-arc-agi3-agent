# Milestone #12 Task 2 - Competitive Solver Benchmark Harness v1

Task 2 creates the first deterministic local benchmark harness for the Milestone #12 competitive solver runtime branch.

The harness measures whether a solver candidate completes synthetic ARC-AGI-3-style cases and how efficiently it does so.

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Harness targets

- completion_rate
- completed_case_count
- failed_case_count
- mean_action_count
- median_action_count
- mean_action_efficiency
- minimum_action_count_sum
- excess_action_count
- public_overfit_signal_count
- regression_failure_count

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- benchmark_harness_only=true
- public_overfit_allowed=false
- public_overfit_guard_required=true
- external_api_dependency=false
- internet_during_eval=false
- real_submission_allowed=false
- manual_upload_allowed=false
- kaggle_submission_sent=false
- kaggle_authentication_performed=false
- private_core_exposure=false
- legal_certification=false

## Next stage

MILESTONE_12_TASK_3_INFORMATION_GAIN_EXPLORER_POLICY_V1
