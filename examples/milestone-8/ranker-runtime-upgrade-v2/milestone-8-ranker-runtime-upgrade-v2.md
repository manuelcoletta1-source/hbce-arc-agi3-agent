# ARC AGI3 Milestone #8 - Ranker Runtime Upgrade v2

- status: MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY
- ranker_id: MILESTONE-8-RANKER-RUNTIME-3126FE509067
- signature: 3126FE509067C21F
- baseline_commit: 3ea3687 Add ARC AGI3 candidate generator runtime upgrade
- ranker_mode: RANKER_RUNTIME_UPGRADE_V2_LOCAL_ONLY
- ranker_scope: RANK_RUNTIME_GENERATED_CANDIDATES_WITH_FAMILY_AWARE_POLICY
- ranker_verdict: RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK
- next_allowed_stage: MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2
- family_count: 4
- ranker_policy_count: 4
- ranker_operation_count: 8
- ranker_case_count: 8
- ranker_pass_count: 8
- ranker_failure_count: 0
- sample_ranked_candidate_count: 4
- ranker_gate_count: 60
- passed_gate_count: 60
- ranker_issue_count: 0
- ranker_ready: True

## Ranker results

- ranker_runtime_color_hint_top_candidate_v2 / family=color_mapping / operation=ranker_runtime_family_hint_boost / passed=True
- ranker_runtime_object_hint_top_candidate_v2 / family=object_model / operation=ranker_runtime_family_hint_boost / passed=True
- ranker_runtime_shape_hint_top_candidate_v2 / family=shape_symmetry / operation=ranker_runtime_family_hint_boost / passed=True
- ranker_runtime_no_hint_score_order_v2 / family=cross_family_composition / operation=ranker_runtime_score_candidate / passed=True
- ranker_runtime_deduplicate_candidates_v2 / family=cross_family_composition / operation=ranker_runtime_deduplicate_by_signature / passed=True
- ranker_runtime_deterministic_order_v2 / family=cross_family_composition / operation=ranker_runtime_stable_tie_break / passed=True
- ranker_runtime_rank_fields_complete_v2 / family=cross_family_composition / operation=ranker_runtime_rank_assignment / passed=True
- ranker_runtime_boundary_guard_v2 / family=cross_family_composition / operation=ranker_runtime_boundary_guard / passed=True

## Decision

Ranker Runtime Upgrade v2 is ready for expanded runtime benchmark.

## Markers

ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_READY=true
ARC_AGI3_MILESTONE_8_RANKER_RUNTIME_UPGRADE_V2_VALID=true
ARC_AGI3_MILESTONE_8_RANKER_MODE=RANKER_RUNTIME_UPGRADE_V2_LOCAL_ONLY
ARC_AGI3_MILESTONE_8_RANKER_VERDICT=RANKER_RUNTIME_UPGRADE_V2_READY_FOR_EXPANDED_RUNTIME_BENCHMARK
ARC_AGI3_MILESTONE_8_BASELINE_RUNTIME_COMMIT=3ea3687
ARC_AGI3_MILESTONE_8_FAMILY_COUNT=4
ARC_AGI3_MILESTONE_8_RANKER_POLICY_COUNT=4
ARC_AGI3_MILESTONE_8_RANKER_OPERATION_COUNT=8
ARC_AGI3_MILESTONE_8_RANKER_CASE_COUNT=8
ARC_AGI3_MILESTONE_8_RANKER_PASS_COUNT=8
ARC_AGI3_MILESTONE_8_RANKER_FAILURE_COUNT=0
ARC_AGI3_MILESTONE_8_SAMPLE_RANKED_CANDIDATE_COUNT=4
ARC_AGI3_MILESTONE_8_NEXT_STAGE=MILESTONE_8_TASK_6_EXPANDED_RUNTIME_BENCHMARK_V2
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_CREATED=false
ARC_AGI3_MILESTONE_8_REAL_SUBMISSION_ALLOWED=false
ARC_AGI3_MILESTONE_8_READY_FOR_REAL_KAGGLE_SUBMISSION=false
ARC_AGI3_MILESTONE_8_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_MILESTONE_8_UPLOAD_PERFORMED=false
ARC_AGI3_MILESTONE_8_KAGGLE_AUTHENTICATION_PERFORMED=false
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
