# Milestone #13 Task 3 - Transformation Primitive Expansion Plan v1

- revision: `MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_V1`
- task_id: `MILESTONE-13-TRANSFORMATION-PRIMITIVE-EXPANSION-PLAN-85611EC0C049`
- signature: `85611EC0C049CDCE`
- baseline_commit: `2ab1228 Add ARC AGI3 milestone 13 transformation primitive expansion plan`
- task_verdict: `MILESTONE_13_TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY`
- plan_verdict: `TRANSFORMATION_PRIMITIVE_EXPANSION_PLAN_READY_FOR_CONTROLLED_IMPLEMENTATION`
- next_stage: `MILESTONE_13_TASK_4_OBJECT_CENTRIC_REASONING_PLAN_V1`

## Plan Summary

- source_audit_ready: `True`
- source_top_priority_ok: `True`
- primitive_group_count: `7`
- primitive_count: `43`
- implementation_slice_count: `6`
- runtime_wiring_authorized: `False`
- runtime_solver_modified: `False`

## Primitive Groups

- `PRIM-GEOMETRIC-CORE` priority `1`: 7 primitives
- `PRIM-CROP-PAD-TRANSLATE` priority `2`: 6 primitives
- `PRIM-COLOR-PALETTE` priority `3`: 6 primitives
- `PRIM-OBJECT-BBOX` priority `4`: 6 primitives
- `PRIM-PATTERN-SYMMETRY` priority `5`: 6 primitives
- `PRIM-COMPOSITION-MASKS` priority `6`: 6 primitives
- `PRIM-SCALE-TILE` priority `7`: 6 primitives

## Implementation Slices

1. `deterministic_primitive_library` → pure local functions with explicit input/output contracts
2. `primitive_unit_examples` → small synthetic examples for each primitive family
3. `candidate_generator_adapter_plan` → controlled adapter plan for future candidate generation
4. `verifier_feature_plan` → evidence features for verifier and ranker scoring
5. `anti_overfit_guard_plan` → guardrails against public-set memorization
6. `local_benchmark_plan` → local-only benchmark hooks, no Kaggle call

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
