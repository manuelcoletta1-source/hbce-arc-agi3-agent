# ARC-AGI-3 Milestone #4 Task 5 — Candidate Generator v1 Smoke

Status: CANDIDATE_GENERATOR_PIPELINE_READY
Generator status: CANDIDATE_GENERATION_READY
Validation status: CANDIDATE_GENERATION_VALID
Generation ID: CANDIDATE-GENERATION-EDBF7855D4FE
Candidate count: 4
Best candidate type: COLOR_SHAPE_COMBINED
Best candidate signature: 3E792F2E511716F9
Best candidate matches expected smoke: true
Signature: EDBF7855D4FE7A8D

## Candidate ranking

- COLOR_SHAPE_COMBINED score_hint=0.95 confidence=0.875 rank_hint=50 signature=3E792F2E511716F9
- SHAPE_TRANSFORM score_hint=0.7 confidence=1.0 rank_hint=150 signature=7B7EBB67FE53742C
- COLOR_REMAP score_hint=0.65 confidence=0.75 rank_hint=200 signature=FC4C9C88E1CEB528
- IDENTITY_BASELINE score_hint=0.1 confidence=0.1 rank_hint=400 signature=4FFFCD3D3A3FAFAD

## Best candidate grid

```json
[[0, 3, 3], [0, 3, 0], [0, 0, 0]]
```

## Boundary

- public_safe=true
- deterministic=true
- local_only=true
- dry_run_only=true
- score_oriented=true
- prize_oriented_solver_target=true
- agentic_state_feature=true
- uses_strategy_interface_v2=true
- uses_grid_object_extractor_v1=true
- uses_color_transform_detector_v1=true
- uses_shape_symmetry_detector_v1=true
- candidate_generator_output=true
- candidate_ranker_input=true
- external_api_dependency=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false
