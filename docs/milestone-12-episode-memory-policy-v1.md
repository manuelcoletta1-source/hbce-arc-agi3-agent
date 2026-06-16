# Milestone #12 Task 7 - Episode Memory Policy v1

Task 7 converts verified planner outputs into deterministic episode memory records.

The episode memory stores case-level action traces, prefixes, remaining actions and reusable memory features for the next candidate policy stage.

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Episode memory targets

- case_count
- episode_count
- verified_episode_count
- memory_record_count
- trace_step_count
- mean_episode_length
- minimum_episode_length
- maximum_episode_length
- reuse_candidate_count
- episode_issue_count

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- episode_memory_only=true
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

MILESTONE_12_TASK_8_CANDIDATE_POLICY_V1
