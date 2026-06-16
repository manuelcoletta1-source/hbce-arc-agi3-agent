# Milestone #12 Task 9 - Candidate Ranker Policy v1

Task 9 ranks the deterministic candidate proposals emitted by Task 8.

The policy ranks candidates per case and selects the top candidate for each case while preserving public-safe, local-only, non-submission boundaries.

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Ranker targets

- case_count
- candidate_count
- ranked_candidate_count
- selected_candidate_count
- top_replay_candidate_count
- ranker_ready_candidate_count
- mean_rank_score
- minimum_rank_score
- maximum_rank_score
- ranker_issue_count

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- candidate_ranker_policy_only=true
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

MILESTONE_12_TASK_10_RANKED_CANDIDATE_BENCHMARK_V1
