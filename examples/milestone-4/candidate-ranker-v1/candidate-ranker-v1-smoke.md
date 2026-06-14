# ARC-AGI-3 Milestone #4 Task 6 — Candidate Ranker v1 Smoke

Status: CANDIDATE_RANKER_PIPELINE_READY
Ranker status: CANDIDATE_RANKING_READY
Validation status: CANDIDATE_RANKING_VALID
Ranking ID: CANDIDATE-RANKING-92172049C00B
Generation ID: CANDIDATE-GENERATION-EDBF7855D4FE
Candidate count: 4
Best candidate type: COLOR_SHAPE_COMBINED
Best candidate score: 0.94
Best candidate matches expected smoke: true
Evidence score: 1.0
Signature: 92172049C00B9EE3

## Ranking

1. COLOR_SHAPE_COMBINED score=0.94 penalties=NONE signature=2514D12A5036C7C7
2. SHAPE_TRANSFORM score=0.838 penalties=NONE signature=4818A144B8F31312
3. COLOR_REMAP score=0.73 penalties=NONE signature=9E94C50B7F3977B1
4. IDENTITY_BASELINE score=0.0 penalties=LOW_CONFIDENCE,LOW_SCORE_HINT,IDENTITY_BASELINE_LOW_PRIORITY signature=5F8CBF1B09E2B4B5

## Boundary

- public_safe=true
- deterministic=true
- local_only=true
- dry_run_only=true
- score_oriented=true
- prize_oriented_solver_target=true
- agentic_state_feature=true
- uses_candidate_generator_v1=true
- uses_grid_object_extractor_v1=true
- uses_color_transform_detector_v1=true
- uses_shape_symmetry_detector_v1=true
- candidate_ranker_output=true
- expanded_batch_benchmark_input=true
- external_api_dependency=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false
