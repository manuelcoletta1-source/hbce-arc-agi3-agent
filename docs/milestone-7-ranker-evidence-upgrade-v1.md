# ARC AGI3 Milestone #7 - Ranker Evidence Upgrade v1

Milestone #7 Task 5 converts candidate generator profiles into deterministic ranker evidence profiles.

The scope is local, bounded, and registry-first. The task defines ranker evidence channels, scoring rules, calibration rules, regression guards, score bounds, and tie-breakers for color mapping, object modeling, and shape/symmetry without claiming competitive readiness and without performing a real submission.

This task does not submit to Kaggle, does not authenticate with Kaggle, does not upload files, does not call external APIs, does not read secrets or tokens, does not create an upload archive, and does not create legal certification claims.

## Baseline

- baseline generator commit: 0dfd280 Add ARC AGI3 candidate generator improvement
- ranker mode: RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD
- ranker scope: UPGRADE_DETERMINISTIC_RANKER_EVIDENCE_FROM_CANDIDATE_GENERATOR_PROFILES
- ranker verdict: RANKER_EVIDENCE_UPGRADE_READY_FOR_REGRESSION_BENCHMARK
- next allowed stage: MILESTONE_7_TASK_6_REGRESSION_BENCHMARK
- profile count: 3
- source generator count: 3
- evidence channel count: 12
- scoring rule count: 12
- calibration rule count: 9
- regression guard count: 9
- aggregate max score: 300
- runtime solver modified: false
- ranker runtime modified: false
- ranker evidence profiles ready: true
- real submission allowed: false
- ready for real Kaggle submission: false
- Kaggle submission sent: false
- upload performed: false
- Kaggle authentication performed: false

## Ranker evidence profiles

1. ranker_evidence_color_mapping_v1
2. ranker_evidence_object_model_v1
3. ranker_evidence_shape_symmetry_v1

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

Ranker evidence profiles are ready. The next stage is Task 6, Regression Benchmark v1.

## Markers

ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_V1_READY=true  
ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_UPGRADE_VALID=true  
ARC_AGI3_MILESTONE_7_RANKER_MODE=RANKER_EVIDENCE_UPGRADE_ONLY_NO_UPLOAD  
ARC_AGI3_MILESTONE_7_RANKER_VERDICT=RANKER_EVIDENCE_UPGRADE_READY_FOR_REGRESSION_BENCHMARK  
ARC_AGI3_MILESTONE_7_PROFILE_COUNT=3  
ARC_AGI3_MILESTONE_7_SOURCE_GENERATOR_COUNT=3  
ARC_AGI3_MILESTONE_7_EVIDENCE_CHANNEL_COUNT=12  
ARC_AGI3_MILESTONE_7_SCORING_RULE_COUNT=12  
ARC_AGI3_MILESTONE_7_CALIBRATION_RULE_COUNT=9  
ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=9  
ARC_AGI3_MILESTONE_7_AGGREGATE_MAX_SCORE=300  
ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false  
ARC_AGI3_MILESTONE_7_RANKER_RUNTIME_MODIFIED=false  
ARC_AGI3_MILESTONE_7_RANKER_EVIDENCE_PROFILES_READY=true  
ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_6_REGRESSION_BENCHMARK  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false  
ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false  
ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false  
ARC_AGI3_MILESTONE_7_BASELINE_GENERATOR_COMMIT=0dfd280  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
