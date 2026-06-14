# ARC AGI3 Milestone #8 - Expanded Runtime Benchmark v2

Milestone #8 Task 6 evaluates the current local runtime stack on expanded deterministic benchmark cases.

The benchmark links the candidate generator runtime and ranker runtime, then checks family coverage, rank order, deduplication, repeatability, and conservative submission boundaries.

## Baseline

- baseline ranker commit: 537b277 Add ARC AGI3 ranker runtime upgrade
- benchmark mode: EXPANDED_RUNTIME_BENCHMARK_V2_LOCAL_ONLY
- benchmark scope: STRESS_RUNTIME_GENERATOR_AND_RANKER_ON_EXPANDED_LOCAL_CASES
- benchmark verdict: EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH
- next allowed stage: MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2
- family count: 4
- expanded case count: 12
- expanded pass count: 12
- expanded failure count: 0
- sample ranked candidate count: 4
- regression guard count: 12
- real submission created: false
- real submission allowed: false
- ready for real Kaggle submission: false
- Kaggle submission sent: false
- upload performed: false
- Kaggle authentication performed: false

## Expanded runtime coverage

1. color family ranking
2. color training-pair mapping
3. background preservation
4. object family ranking
5. object translation candidate coverage
6. shape family ranking
7. shape reflection candidate coverage
8. cross-family score ordering
9. cross-family deduplication
10. deterministic repeatability
11. runtime stack linkage
12. boundary guard

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

Expanded Runtime Benchmark v2 is ready for submission candidate refresh. The next stage is Task 7.

## Markers

ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_READY=true  
ARC_AGI3_MILESTONE_8_EXPANDED_RUNTIME_BENCHMARK_V2_VALID=true  
ARC_AGI3_MILESTONE_8_BENCHMARK_MODE=EXPANDED_RUNTIME_BENCHMARK_V2_LOCAL_ONLY  
ARC_AGI3_MILESTONE_8_BENCHMARK_VERDICT=EXPANDED_RUNTIME_BENCHMARK_V2_READY_FOR_SUBMISSION_CANDIDATE_REFRESH  
ARC_AGI3_MILESTONE_8_BASELINE_RANKER_COMMIT=537b277  
ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4  
ARC_AGI3_MILESTONE_8_EXPANDED_CASE_COUNT=12  
ARC_AGI3_MILESTONE_8_EXPANDED_PASS_COUNT=12  
ARC_AGI3_MILESTONE_8_EXPANDED_FAILURE_COUNT=0  
ARC_AGI3_MILESTONE_8_SAMPLE_RANKED_CANDIDATE_COUNT=4  
ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_7_SUBMISSION_CANDIDATE_REFRESH_V2  
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false  
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false  
ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
