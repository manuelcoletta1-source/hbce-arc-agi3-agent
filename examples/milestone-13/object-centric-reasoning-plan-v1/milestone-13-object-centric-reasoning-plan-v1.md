# Milestone #13 Task 4 - Object-Centric Reasoning Plan v1

- revision: `MILESTONE_13_OBJECT_CENTRIC_REASONING_PLAN_V1`
- task_id: `MILESTONE-13-OBJECT-CENTRIC-REASONING-PLAN-A6753DD23F15`
- signature: `A6753DD23F1557C2`
- baseline_commit: `3c019f9 Update ARC AGI3 milestone 13 transformation primitive expansion plan artifacts`
- task_verdict: `MILESTONE_13_OBJECT_CENTRIC_REASONING_PLAN_READY`
- plan_verdict: `OBJECT_CENTRIC_REASONING_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION`
- next_stage: `MILESTONE_13_TASK_5_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1`

## Plan Summary

- source_plan_ready: `True`
- source_primitive_plan_ok: `True`
- object_reasoning_stage_count: `6`
- object_feature_count: `14`
- object_operation_group_count: `7`
- object_operation_count: `35`
- implementation_lane_count: `6`
- runtime_wiring_authorized: `False`
- runtime_solver_modified: `False`

## Object Reasoning Stages

- `OBJ-STAGE-01` `connected_component_extraction`: detect non-background connected components under deterministic connectivity rules
- `OBJ-STAGE-02` `object_feature_encoding`: encode color, area, bbox, shape mask, centroid and border contact features
- `OBJ-STAGE-03` `object_relation_graph`: represent relative position, containment, alignment, distance and symmetry relations
- `OBJ-STAGE-04` `object_transform_hypotheses`: derive candidate object moves, copies, removals, recolors and recompositions
- `OBJ-STAGE-05` `object_level_verification_features`: score candidates using object preservation, relation preservation and target fit
- `OBJ-STAGE-06` `object_memory_replay_cases`: convert object-centric failures into reusable local replay tests

## Object Operation Groups

- `OBJ-OP-EXTRACT` priority `1`: 5 operations
- `OBJ-OP-FILTER` priority `2`: 5 operations
- `OBJ-OP-RELATE` priority `3`: 5 operations
- `OBJ-OP-MOVE` priority `4`: 5 operations
- `OBJ-OP-RECOLOR` priority `5`: 5 operations
- `OBJ-OP-COMPOSE` priority `6`: 5 operations
- `OBJ-OP-COMPLETE` priority `7`: 5 operations

## Implementation Lanes

1. `object_extractor_contracts` → deterministic extraction contracts and local examples
2. `object_feature_schema` → stable public-safe object feature schema
3. `object_relation_graph_schema` → relation graph schema for future verifier and planner use
4. `object_transform_candidate_plan` → controlled object-level candidate generation plan
5. `object_verifier_feature_plan` → future verifier and ranker evidence hooks
6. `object_failure_replay_plan` → local-only replay cases for object-centric failures

## Boundary

- real_evaluation_performed: `False`
- real_submission_allowed: `False`
- ready_for_real_kaggle_submission: `False`
- kaggle_authentication_allowed: `False`
- kaggle_submission_sent: `False`
- external_api_dependency: `False`
- internet_during_eval: `False`
- private_core_exposure: `False`
- legal_certification: `False`
