# ARC AGI3 Milestone #7 - Regression Benchmark v1

Milestone #7 Task 6 converts ranker evidence profiles into deterministic regression benchmark records.

The scope is local, bounded, and registry-first. The task defines family-specific regression cases for color mapping, object modeling, and shape/symmetry without claiming competitive readiness and without performing a real submission.

This task does not submit to Kaggle, does not authenticate with Kaggle, does not upload files, does not call external APIs, does not read secrets or tokens, does not create an upload archive, and does not create legal certification claims.

## Baseline

- baseline ranker commit: f4035fa Add ARC AGI3 ranker evidence upgrade
- benchmark mode: REGRESSION_BENCHMARK_ONLY_NO_UPLOAD
- benchmark scope: BENCHMARK_RANKER_EVIDENCE_UPGRADE_WITH_FAMILY_REGRESSION_GUARDS
- benchmark verdict: REGRESSION_BENCHMARK_READY_FOR_LOCAL_SCORE_IMPROVEMENT_REPORT
- next allowed stage: MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT
- ranker profile count: 3
- benchmark case count: 6
- family count: 3
- evidence check count: 24
- regression guard count: 18
- measurement count: 6
- pass count: 6
- failure count: 0
- runtime solver modified: false
- ranker runtime modified: false
- benchmark runtime modified: false
- regression benchmark records ready: true
- real submission allowed: false
- ready for real Kaggle submission: false
- Kaggle submission sent: false
- upload performed: false
- Kaggle authentication performed: false

## Regression cases

1. regression_color_palette_stability_v1
2. regression_color_background_preservation_v1
3. regression_object_component_count_v1
4. regression_object_spatial_delta_v1
5. regression_shape_axis_symmetry_v1
6. regression_shape_translation_bounds_v1

## Boundary

public_safe=true  
deterministic=true  
local_only=true  
dry_run_only=true  
external_api_dependency=false  
contains_api_keys=false  
kaggle_submission_sent=false  
private_core_exposure=false  
legal_certification=false  

## Decision

Regression benchmark records are ready. The next stage is Task 7, Local Score Improvement Report v1.

## Markers

ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_V1_READY=true  
ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_VALID=true  
ARC_AGI3_MILESTONE_7_BENCHMARK_MODE=REGRESSION_BENCHMARK_ONLY_NO_UPLOAD  
ARC_AGI3_MILESTONE_7_BENCHMARK_VERDICT=REGRESSION_BENCHMARK_READY_FOR_LOCAL_SCORE_IMPROVEMENT_REPORT  
ARC_AGI3_MILESTONE_7_RANKER_PROFILE_COUNT=3  
ARC_AGI3_MILESTONE_7_BENCHMARK_CASE_COUNT=6  
ARC_AGI3_MILESTONE_7_FAMILY_COUNT=3  
ARC_AGI3_MILESTONE_7_EVIDENCE_CHECK_COUNT=24  
ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=18  
ARC_AGI3_MILESTONE_7_MEASUREMENT_COUNT=6  
ARC_AGI3_MILESTONE_7_PASS_COUNT=6  
ARC_AGI3_MILESTONE_7_FAILURE_COUNT=0  
ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false  
ARC_AGI3_MILESTONE_7_RANKER_RUNTIME_MODIFIED=false  
ARC_AGI3_MILESTONE_7_BENCHMARK_RUNTIME_MODIFIED=false  
ARC_AGI3_MILESTONE_7_REGRESSION_BENCHMARK_RECORDS_READY=true  
ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_7_LOCAL_SCORE_IMPROVEMENT_REPORT  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false  
ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false  
ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false  
ARC_AGI3_MILESTONE_7_BASELINE_RANKER_COMMIT=f4035fa  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
