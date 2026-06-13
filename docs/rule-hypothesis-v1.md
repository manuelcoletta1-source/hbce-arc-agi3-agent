# ARC-AGI-3 Rule Hypothesis v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_RULE_HYPOTHESIS_V1  
Boundary: deterministic candidate-rule generation only.

## Purpose

Rule Hypothesis v1 creates deterministic candidate transformation hypotheses from ARC-like grids and Object Model v1.

It does not claim to solve ARC-AGI-3. It creates a traceable hypothesis layer for later planner strategy expansion.

This is the bridge between object perception and actual strategy selection.

## Pipeline position

Rule Hypothesis v1 extends the Milestone #2 chain:

task_loader → observer → world_model → object_model → rule_hypothesis → planner → verification_scoring → trace_schema

## Capabilities

Rule Hypothesis v1 provides candidate hypotheses for:

- structure preservation
- object count invariance
- dominant non-background value focus
- horizontal symmetry
- vertical symmetry
- largest object anchor
- copy, move, expand candidate operations

## Safety boundary

Rule Hypothesis v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Rule Hypothesis v1 is PASS only if:

- all tests pass
- hypotheses are deterministic
- grid payloads are supported
- object model payloads are supported
- loaded task payloads are supported
- validation rejects broken contracts
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_RULE_HYPOTHESIS_V1_READY=true  
ARC_AGI3_RULE_HYPOTHESIS_STATUS=RULE_HYPOTHESIS_READY  
ARC_AGI3_RULE_HYPOTHESIS_VALIDATION=RULE_HYPOTHESIS_VALID  
ARC_AGI3_RULE_HYPOTHESIS_DETERMINISTIC_SIGNATURE=true  
ARC_AGI3_RULE_HYPOTHESIS_USES_OBJECT_MODEL=true  
ARC_AGI3_MILESTONE_2_TASK_4_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
