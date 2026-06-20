# Milestone 18 Task 4 — Controlled Technical Candidate Generator Improvement Map v1

## Status

- Task: `MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1`
- Map ID: `MILESTONE-18-TASK-4-CANDIDATE-GENERATOR-IMPROVEMENT-MAP-D52615F216F01836`
- Signature: `D52615F216F01836`
- Previous task: `MILESTONE_18_TASK_3_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_V1`
- Previous commit: `ff72908`
- Previous signature: `38A0F948AFF91AC9`
- Verdict: `CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_READY_NO_IMPLEMENTATION`
- Next stage: `MILESTONE_18_TASK_5_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_V1`

## Boundary

- planning-only: true
- implementation authorized: false
- runtime execution allowed: false
- real evaluation allowed: false
- real submission allowed: false
- Kaggle submission sent: false
- private core exposure: false
- legalCertification: false
- fail-closed: active

## Improvement Map

### M18-CGIM-1 — solver coverage

- Source review item: `M18-REV-1`
- Source limitation: `M18-LIM-1`
- Confirmed limitation: Candidate generation must support broader transform hypotheses without pretending solver coverage is solved.
- Controlled improvement: Map candidate families for color mapping, object transformation, symmetry, grid completion, and cross-family composition.
- Expected evidence: Each candidate family must expose family_id, transform_hypothesis, input_observation_basis, expected_output_constraint, and rejection_reason fields.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

### M18-CGIM-2 — candidate generation

- Source review item: `M18-REV-2`
- Source limitation: `M18-LIM-2`
- Confirmed limitation: Candidate generation needs structured hypothesis diversity, not a single brittle answer path.
- Controlled improvement: Define a multi-candidate proposal map with deterministic ordering, family labels, confidence_hint, and evidence slots.
- Expected evidence: Generated candidates must preserve deterministic order, candidate_id, family_id, transform_summary, and confidence_hint without claiming official score impact.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

### M18-CGIM-3 — ranker evidence

- Source review item: `M18-REV-3`
- Source limitation: `M18-LIM-3`
- Confirmed limitation: Ranker evidence must receive structured candidate metadata without changing ranker behavior yet.
- Controlled improvement: Map ranker-neutral evidence fields: observation_count, transform_specificity, contradiction_count, grid_consistency_notes, and fallback_reason.
- Expected evidence: Candidate records must be inspectable by future ranker review while leaving ranker runtime untouched in Task 4.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

### M18-CGIM-4 — local diagnostics

- Source review item: `M18-REV-4`
- Source limitation: `M18-LIM-4`
- Confirmed limitation: Candidate generator changes require local diagnostic visibility before any implementation.
- Controlled improvement: Define a fixture-driven diagnostic matrix linking candidate families to local public-safe benchmark cases.
- Expected evidence: Each mapped diagnostic must include fixture_id, family_under_test, expected_candidate_count, rejection_path_required, and regression_guard.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

### M18-CGIM-5 — submission discipline

- Source review item: `M18-REV-5`
- Source limitation: `M18-LIM-5`
- Confirmed limitation: Candidate generation must not silently become submission generation.
- Controlled improvement: Separate candidate proposal artifacts from submission artifacts with explicit real_submission_allowed=false gates.
- Expected evidence: Artifacts must state no Kaggle upload, no manual upload, no submission.json production, and no official score claim.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

### M18-CGIM-6 — authorization boundary

- Source review item: `M18-REV-6`
- Source limitation: `M18-LIM-6`
- Confirmed limitation: Task 4 may map improvements but must not authorize implementation.
- Controlled improvement: Preserve hard authorization flags across map, artifacts, docs, and tests.
- Expected evidence: All generated records must expose implementation_authorized=false, runtime_execution_allowed=false, and fail_closed_active=true.
- Implementation status: `PLANNING_ONLY_NOT_IMPLEMENTED`
- Review required before implementation: `True`
- Implementation authorized: `False`

## Acceptance

- Acceptance gate count: `45`
- Acceptance gate failures: `0`
- Blocking issue count: `0`

Task 4 creates a controlled technical map only. It does not modify the solver, candidate generator runtime, ranker runtime, or submission pipeline.
