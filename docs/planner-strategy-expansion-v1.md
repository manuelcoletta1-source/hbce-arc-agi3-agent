# ARC-AGI-3 Planner Strategy Expansion v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_PLANNER_STRATEGY_EXPANSION_V1  
Boundary: deterministic hypothesis-driven strategy selection only.

## Purpose

Planner Strategy Expansion v1 connects Rule Hypothesis v1 to deterministic planner strategy selection.

It does not claim to solve ARC-AGI-3. It gives the planner a public, traceable, hypothesis-driven strategy layer instead of relying only on generic baseline planning.

## Pipeline position

Planner Strategy Expansion v1 extends the Milestone #2 chain:

task_loader → observer → world_model → object_model → rule_hypothesis → planner_strategy → planner → verification_scoring → trace_schema

## Capabilities

Planner Strategy Expansion v1 provides:

- deterministic hypothesis ranking
- highest-confidence strategy selection
- selected rule type
- selected hypothesis id
- selected action
- confidence
- rationale
- evidence and parameters
- ranked hypothesis list
- validation contract
- public-safe metadata

## Strategy mapping

The initial deterministic mapping is:

- preserve_structure → preserve_non_background_structure
- object_count_invariant → preserve_object_count
- dominant_value_focus → transform_or_preserve_dominant_value
- horizontal_symmetry_candidate → evaluate_horizontal_mirror
- vertical_symmetry_candidate → evaluate_vertical_mirror
- largest_object_anchor → anchor_largest_object_copy_move_expand

## Safety boundary

Planner Strategy Expansion v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Planner Strategy Expansion v1 is PASS only if:

- all tests pass
- hypothesis selection is deterministic
- grid payloads are supported
- loaded task payloads are supported
- strategy validation rejects broken contracts
- public-safe metadata is explicit
- rule hypothesis and object model usage are explicit

## Operational markers

ARC_AGI3_PLANNER_STRATEGY_EXPANSION_V1_READY=true  
ARC_AGI3_PLANNER_STRATEGY_STATUS=PLANNER_STRATEGY_READY  
ARC_AGI3_PLANNER_STRATEGY_PIPELINE_STATUS=PLANNER_STRATEGY_PIPELINE_READY  
ARC_AGI3_PLANNER_STRATEGY_VALIDATION=PLANNER_STRATEGY_VALID  
ARC_AGI3_PLANNER_STRATEGY_USES_RULE_HYPOTHESIS=true  
ARC_AGI3_PLANNER_STRATEGY_USES_OBJECT_MODEL=true  
ARC_AGI3_MILESTONE_2_TASK_5_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
