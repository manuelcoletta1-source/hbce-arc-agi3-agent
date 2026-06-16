# Milestone #13 Task 5 - Program Synthesis Candidate Generator Plan v1

- revision: `MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_V1`
- task_id: `MILESTONE-13-PROGRAM-SYNTHESIS-CANDIDATE-GENERATOR-PLAN-85195151C772`
- signature: `85195151C7720763`
- baseline_commit: `440a5a2 Add ARC AGI3 milestone 13 program synthesis candidate generator plan`
- task_verdict: `MILESTONE_13_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_READY`
- plan_verdict: `PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION`
- next_stage: `MILESTONE_13_TASK_6_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_CONTROLLED_IMPLEMENTATION_V1`

## Plan Summary

- source_plan_ready: `True`
- source_object_plan_ok: `True`
- synthesis_stage_count: `6`
- program_template_count: `12`
- candidate_family_count: `7`
- search_control_count: `8`
- implementation_lane_count: `6`
- candidate_generator_wiring_authorized: `False`
- runtime_wiring_authorized: `False`
- runtime_solver_modified: `False`

## Synthesis Stages

- `SYN-STAGE-01` `training_pair_feature_read`: read grid, object, color and relation features from local training pairs
- `SYN-STAGE-02` `program_template_selection`: select bounded program templates from primitive and object-centric families
- `SYN-STAGE-03` `bounded_parameter_binding`: bind colors, object selectors, directions, bbox references and symmetry axes
- `SYN-STAGE-04` `candidate_program_execution`: execute candidate programs locally against training examples
- `SYN-STAGE-05` `candidate_evidence_packaging`: package match evidence for future verifier and ranker layers
- `SYN-STAGE-06` `fail_closed_candidate_export`: export only deterministic public-safe candidates for the next controlled stage

## Candidate Families

- `CAND-FAMILY-01` priority `1` `primitive_sequence_candidates`: bounded sequences of deterministic grid primitives
- `CAND-FAMILY-02` priority `2` `object_transform_candidates`: extract, move, copy, remove, recolor or compose detected objects
- `CAND-FAMILY-03` priority `3` `color_rule_candidates`: palette remaps, swaps and conditional recolor rules
- `CAND-FAMILY-04` priority `4` `symmetry_completion_candidates`: complete missing grid or object structure using symmetry hypotheses
- `CAND-FAMILY-05` priority `5` `crop_pad_resize_candidates`: shape and canvas transforms around object or non-background bounds
- `CAND-FAMILY-06` priority `6` `relation_graph_candidates`: generate candidates from object alignment, containment and adjacency relations
- `CAND-FAMILY-07` priority `7` `composite_program_candidates`: small bounded compositions of primitive, object and color programs

## Implementation Lanes

1. `program_template_schema` → stable schema for local candidate program templates
2. `parameter_binding_contract` → bounded deterministic binding of colors, objects, vectors and axes
3. `candidate_execution_contract` → local-only execution contract for generated candidate programs
4. `candidate_evidence_schema` → evidence structure for future verifier and ranker integration
5. `bounded_search_policy` → depth, count and deterministic ordering rules for candidate search
6. `controlled_implementation_entrypoint` → next-stage implementation entrypoint with runtime still blocked

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
