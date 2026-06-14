# ARC AGI3 Milestone #8 - Family Benchmark Cases v2

Milestone #8 Task 3 creates deterministic local family benchmark cases for Competitive Solver Kernel v2.

The benchmark validates kernel behavior across four local families: color mapping, object model, shape symmetry, and cross-family composition. It does not claim Kaggle score, does not create a real submission, and does not perform upload or authentication.

## Baseline

- baseline kernel commit: 4a93654 Add ARC AGI3 competitive solver kernel
- benchmark mode: FAMILY_BENCHMARK_CASES_V2_LOCAL_ONLY
- benchmark scope: MEASURE_KERNEL_V2_ON_LOCAL_FAMILY_CASES
- benchmark verdict: FAMILY_BENCHMARK_CASES_V2_READY_FOR_CANDIDATE_GENERATOR_RUNTIME_UPGRADE
- next allowed stage: MILESTONE_8_TASK_4_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2
- family count: 4
- benchmark case count: 8
- benchmark pass count: 8
- benchmark failure count: 0
- evidence field count: 8
- regression guard count: 8
- real submission created: false
- real submission allowed: false
- ready for real Kaggle submission: false
- Kaggle submission sent: false
- upload performed: false
- Kaggle authentication performed: false

## Family coverage

1. color mapping
2. object model
3. shape symmetry
4. cross-family composition

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

Family Benchmark Cases v2 are ready for candidate generator runtime upgrade. The next stage is Task 4.

## Markers

ARC_AGI3_MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_READY=true  
ARC_AGI3_MILESTONE_8_FAMILY_BENCHMARK_CASES_V2_VALID=true  
ARC_AGI3_MILESTONE_8_BENCHMARK_MODE=FAMILY_BENCHMARK_CASES_V2_LOCAL_ONLY  
ARC_AGI3_MILESTONE_8_BENCHMARK_VERDICT=FAMILY_BENCHMARK_CASES_V2_READY_FOR_CANDIDATE_GENERATOR_RUNTIME_UPGRADE  
ARC_AGI3_MILESTONE_8_BASELINE_KERNEL_COMMIT=4a93654  
ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4  
ARC_AGI3_MILESTONE_8_BENCHMARK_CASE_COUNT=8  
ARC_AGI3_MILESTONE_8_BENCHMARK_PASS_COUNT=8  
ARC_AGI3_MILESTONE_8_BENCHMARK_FAILURE_COUNT=0  
ARC_AGI3_MILESTONE_8_EVIDENCE_FIELD_COUNT=8  
ARC_AGI3_MILESTONE_8_REGRESSION_GUARD_COUNT=8  
ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_4_CANDIDATE_GENERATOR_RUNTIME_UPGRADE_V2  
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false  
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false  
ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
