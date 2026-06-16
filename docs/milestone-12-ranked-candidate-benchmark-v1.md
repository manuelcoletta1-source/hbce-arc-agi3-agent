# Milestone #12 Task 10 - Ranked Candidate Benchmark v1

Task 10 benchmarks the selected ranked candidates emitted by Task 9.

The benchmark validates that the selected candidates are deterministic, verified, ranker-ready and still inside the public-safe no-submission boundary.

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Benchmark targets

- case_count
- selected_candidate_count
- benchmark_case_count
- benchmark_pass_count
- benchmark_warning_count
- benchmark_failure_count
- top_replay_candidate_count
- mean_rank_score
- minimum_rank_score
- maximum_rank_score

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- ranked_candidate_benchmark_only=true
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

MILESTONE_12_TASK_11_PUBLIC_OVERFIT_GUARD_V1
