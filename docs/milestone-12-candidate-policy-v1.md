# Milestone #12 Task 8 - Candidate Policy v1

Task 8 converts verified episode memory into deterministic candidate proposals for the next ranker stage.

The policy emits three candidate families per verified episode:

- VERIFIED_EPISODE_REPLAY
- PREFIX_SAFE_REPLAY
- FAMILY_HEURISTIC_REPLAY

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Candidate targets

- case_count
- episode_count
- candidate_count
- verified_candidate_count
- replay_candidate_count
- prefix_candidate_count
- heuristic_candidate_count
- mean_candidate_length
- ranker_ready_candidate_count
- candidate_issue_count

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- candidate_policy_only=true
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

MILESTONE_12_TASK_9_CANDIDATE_RANKER_POLICY_V1
