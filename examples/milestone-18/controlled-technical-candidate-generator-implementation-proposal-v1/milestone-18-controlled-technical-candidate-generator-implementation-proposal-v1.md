# Milestone 18 Task 10 - Controlled Technical Candidate Generator Implementation Proposal v1

## Status

- Task: `MILESTONE_18_TASK_10_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_V1`
- Implementation proposal ID: `MILESTONE-18-TASK-10-CANDIDATE-GENERATOR-IMPLEMENTATION-PROPOSAL-A2BE24B5965B838E`
- Signature: `A2BE24B5965B838E`
- Previous task: `MILESTONE_18_TASK_9_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_DECISION_GATE_REVIEW_V1`
- Previous commit: `51a7e3b`
- Previous signature: `3C632A7BAA041134`
- Source decision gate review ID: `MILESTONE-18-TASK-9-CANDIDATE-GENERATOR-IMPLEMENTATION-DECISION-GATE-REVIEW-3C632A7BAA041134`
- Source decision gate review signature: `3C632A7BAA041134`
- Verdict: `CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_READY_NO_CODE_NO_RUNTIME`
- Next stage: `MILESTONE_18_TASK_11_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_PROPOSAL_REVIEW_V1`

## Boundary

- implementation proposal only: true
- implementation proposal created: true
- implementation proposal review required: true
- implementation code authorized: false
- candidate generator modified: false
- runtime execution allowed: false
- real evaluation allowed: false
- real submission allowed: false
- Kaggle submission sent: false
- private core exposure: false
- legalCertification: false
- fail-closed: active

## Proposal Items

### M18-CG-IMPL-PROPOSAL-1 - solver coverage

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-1`
- Source decision: `M18-CG-IMPL-DECISION-1`
- Source improvement item: `M18-CGIM-1`
- Source limitation: `M18-LIM-1`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define controlled candidate-family coverage expansion without altering solver runtime behavior.

Deterministic constraints:
- candidate family IDs must be stable and deterministic
- coverage labels must be diagnostic-only
- no official score claim may be derived from proposal artifacts

Test expectations:
- public-safe local fixtures cover every proposed candidate family
- proposal output remains stable across repeated local runs
- no runtime solver mutation is performed

Guardrails:
- no solver runtime modification
- no private core exposure
- no real evaluation execution

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

### M18-CG-IMPL-PROPOSAL-2 - candidate generation

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-2`
- Source decision: `M18-CG-IMPL-DECISION-2`
- Source improvement item: `M18-CGIM-2`
- Source limitation: `M18-LIM-2`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define deterministic candidate construction rules with stable IDs, ordering, confidence hints, and rejection paths.

Deterministic constraints:
- candidate ordering must be deterministic
- candidate IDs must be reproducible
- confidence hints must not overwrite ranker evidence

Test expectations:
- candidate list is reproducible across repeated runs
- invalid candidate paths are rejected fail-closed
- confidence hints remain metadata-only

Guardrails:
- no runtime patch in this task
- no generated submission artifact
- no hidden network dependency

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

### M18-CG-IMPL-PROPOSAL-3 - ranker evidence

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-3`
- Source decision: `M18-CG-IMPL-DECISION-3`
- Source improvement item: `M18-CGIM-3`
- Source limitation: `M18-LIM-3`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define ranker-neutral evidence metadata mapping without modifying ranker weights or runtime ranking logic.

Deterministic constraints:
- ranker inputs must remain unchanged
- evidence metadata must be additive and diagnostic-only
- score claims must remain blocked

Test expectations:
- ranker output compatibility is preserved
- metadata emission is deterministic
- no ranker weight mutation occurs

Guardrails:
- no ranker runtime modification
- no competitive score claim
- no official score claim

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

### M18-CG-IMPL-PROPOSAL-4 - local diagnostics

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-4`
- Source decision: `M18-CG-IMPL-DECISION-4`
- Source improvement item: `M18-CGIM-4`
- Source limitation: `M18-LIM-4`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define public-safe diagnostic fixtures and regression guards for future controlled implementation review.

Deterministic constraints:
- fixtures must be local-only
- fixtures must contain no private datasets
- diagnostic outputs must be deterministic

Test expectations:
- fixture manifest validates expected cases
- regression guard blocks missing fixture coverage
- local-only execution remains enforced

Guardrails:
- no external API dependency
- no internet during evaluation
- no private dataset exposure

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

### M18-CG-IMPL-PROPOSAL-5 - submission discipline

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-5`
- Source decision: `M18-CG-IMPL-DECISION-5`
- Source improvement item: `M18-CGIM-5`
- Source limitation: `M18-LIM-5`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define separation rules between candidate artifacts and submission artifacts.

Deterministic constraints:
- candidate artifacts must not become submission.json
- real submission must remain blocked
- manual upload must remain blocked

Test expectations:
- candidate artifact generation is distinguishable from submission generation
- submission path remains disabled
- Kaggle authentication remains blocked

Guardrails:
- no submission.json creation
- no Kaggle authentication
- no Kaggle submission

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

### M18-CG-IMPL-PROPOSAL-6 - authorization boundary

- Source review item: `M18-CG-IMPL-DECISION-GATE-REV-6`
- Source decision: `M18-CG-IMPL-DECISION-6`
- Source improvement item: `M18-CGIM-6`
- Source limitation: `M18-LIM-6`
- Proposal kind: `CONTROLLED_IMPLEMENTATION_PROPOSAL_ONLY`
- Implementation scope: `PROPOSAL_ONLY_NO_CODE_NO_RUNTIME`
- Design intent: Define the authorization boundary for any future implementation patch and keep fail-closed active.

Deterministic constraints:
- operator authorization must be explicit
- implementation review must pass before code changes
- fail-closed must remain active until a separate implementation authorization step

Test expectations:
- proposal records explicit authorization requirements
- implementation remains blocked
- boundary controls are all validated

Guardrails:
- no implicit authorization
- no runtime execution
- no legal certification claim

- Proposal review required: `True`
- Implementation code authorized: `False`
- Runtime execution authorized: `False`
- Real submission authorized: `False`

## Acceptance

- Proposal item count: `6`
- Acceptance gate count: `55`
- Acceptance gate failures: `0`
- Blocking issue count: `0`

Task 10 creates a controlled implementation proposal only. It does not authorize code implementation, runtime execution, real evaluation, upload, or submission.
