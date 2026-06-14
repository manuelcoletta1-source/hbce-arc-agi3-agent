# ARC AGI3 Milestone #7 - Candidate Generator Improvement v1

Milestone #7 Task 4 converts task-family solver expansion branches into deterministic candidate generator profiles.

The scope is local, bounded, and registry-first. The task defines candidate generation templates for color mapping, object modeling, and shape/symmetry without claiming competitive readiness and without performing a real submission.

This task does not submit to Kaggle, does not authenticate with Kaggle, does not upload files, does not call external APIs, does not read secrets or tokens, does not create an upload archive, and does not create legal certification claims.

## Baseline

- baseline expansion commit: 3ec630b Add ARC AGI3 task-family solver expansion
- generator mode: CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD
- generator scope: GENERATE_DETERMINISTIC_CANDIDATE_TEMPLATES_FROM_TASK_FAMILIES
- generator verdict: CANDIDATE_GENERATOR_IMPROVEMENT_READY_FOR_RANKER_EVIDENCE_UPGRADE
- next allowed stage: MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE
- profile count: 3
- source family count: 3
- template count: 12
- evidence field count: 15
- deterministic rule count: 12
- regression guard count: 9
- max candidate count: 24
- runtime solver modified: false
- candidate generator profiles ready: true
- real submission allowed: false
- ready for real Kaggle submission: false
- Kaggle submission sent: false
- upload performed: false
- Kaggle authentication performed: false

## Generator profiles

1. candidate_generator_color_mapping_v1
2. candidate_generator_object_model_v1
3. candidate_generator_shape_symmetry_v1

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

Candidate generator profiles are ready. The next stage is Task 5, Ranker Evidence Upgrade v1.

## Markers

ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_V1_READY=true  
ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_IMPROVEMENT_VALID=true  
ARC_AGI3_MILESTONE_7_GENERATOR_MODE=CANDIDATE_GENERATOR_IMPROVEMENT_ONLY_NO_UPLOAD  
ARC_AGI3_MILESTONE_7_GENERATOR_VERDICT=CANDIDATE_GENERATOR_IMPROVEMENT_READY_FOR_RANKER_EVIDENCE_UPGRADE  
ARC_AGI3_MILESTONE_7_PROFILE_COUNT=3  
ARC_AGI3_MILESTONE_7_SOURCE_FAMILY_COUNT=3  
ARC_AGI3_MILESTONE_7_TEMPLATE_COUNT=12  
ARC_AGI3_MILESTONE_7_EVIDENCE_FIELD_COUNT=15  
ARC_AGI3_MILESTONE_7_DETERMINISTIC_RULE_COUNT=12  
ARC_AGI3_MILESTONE_7_REGRESSION_GUARD_COUNT=9  
ARC_AGI3_MILESTONE_7_MAX_CANDIDATE_COUNT=24  
ARC_AGI3_MILESTONE_7_RUNTIME_SOLVER_MODIFIED=false  
ARC_AGI3_MILESTONE_7_CANDIDATE_GENERATOR_PROFILES_READY=true  
ARC_AGI3_MILESTONE_7_NEXT_STAGE=MILESTONE_7_TASK_5_RANKER_EVIDENCE_UPGRADE  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_ALLOWED=false  
ARC_AGI3_MILESTONE_7_READY_FOR_REAL_KAGGLE_SUBMISSION=false  
ARC_AGI3_MILESTONE_7_REAL_SUBMISSION_CREATED=false  
ARC_AGI3_MILESTONE_7_UPLOAD_PERFORMED=false  
ARC_AGI3_MILESTONE_7_KAGGLE_AUTHENTICATION_PERFORMED=false  
ARC_AGI3_MILESTONE_7_BASELINE_EXPANSION_COMMIT=3ec630b  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
