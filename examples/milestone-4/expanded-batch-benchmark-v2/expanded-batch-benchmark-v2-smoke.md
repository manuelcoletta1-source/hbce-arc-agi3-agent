# ARC AGI3 Milestone #4 Task 7 - Expanded Batch Benchmark v2

## Status

- status: `EXPANDED_BATCH_BENCHMARK_PIPELINE_READY`
- validation: `EXPANDED_BATCH_BENCHMARK_VALID`
- benchmark_id: `EXPANDED-BATCH-BENCHMARK-E9B711359952`
- signature: `E9B7113599525583`

## Metrics

- task_count: `3`
- tasks_processed: `3`
- candidate_generation_success_rate: `1.0`
- ranking_success_rate: `1.0`
- best_candidate_match_rate: `1.0`
- average_best_score: `0.9458`
- best_task_score: `1.0`
- worst_task_score: `0.8975`

## Task results

| task_id | family | candidates | best_type | best_score | match |
|---|---|---:|---|---:|---:|
| EXPANDED-BATCH-V2-COLOR-SHAPE-SMOKE | color_shape_combined | 4 | COLOR_SHAPE_COMBINED | 0.94 | True |
| EXPANDED-BATCH-V2-IDENTITY | identity_baseline | 4 | COLOR_SHAPE_COMBINED | 0.8975 | True |
| EXPANDED-BATCH-V2-COLOR-ONLY | color_transform | 4 | COLOR_REMAP | 1.0 | True |

## Boundary

- public_safe: `true`
- deterministic: `true`
- local_only: `true`
- dry_run_only: `true`
- external_api_dependency: `false`
- contains_api_keys: `false`
- kaggle_submission_sent: `false`
- private_core_exposure: `false`
- legal_certification: `false`

## Markers

ARC_AGI3_MILESTONE_4_TASK_7_EXPANDED_BATCH_BENCHMARK_V2_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_STATUS=EXPANDED_BATCH_BENCHMARK_READY  
ARC_AGI3_MILESTONE_4_TASK_7_PIPELINE_STATUS=EXPANDED_BATCH_BENCHMARK_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_7_VALIDATION=EXPANDED_BATCH_BENCHMARK_VALID  
ARC_AGI3_MILESTONE_4_TASK_7_TASKS_PROCESSED_MINIMUM_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_CANDIDATE_GENERATION_SUCCESS_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_RANKING_SUCCESS_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_BEST_CANDIDATE_MATCH_RATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_AVERAGE_BEST_SCORE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_GENERATOR_V1=true  
ARC_AGI3_MILESTONE_4_TASK_7_USES_CANDIDATE_RANKER_V1=true  
ARC_AGI3_MILESTONE_4_TASK_7_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_7_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
