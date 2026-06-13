# ARC-AGI-3 Milestone #4 Task 5 — Candidate Generator v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Task: #5  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Target: deterministic candidate generation from object, color and shape signals.

## Purpose

Candidate Generator v1 creates deterministic candidate output grids from the solver signals already built in Milestone #4.

This is the first Milestone #4 module that produces candidate outputs instead of only describing the input. It combines object extraction, stable color remapping and shape/symmetry transformation signals into ranked candidate grids.

The purpose is simple: start producing answer candidates, not just increasingly sophisticated excuses for why the grid is complicated.

## Inputs

Candidate Generator v1 uses:

- training pairs
- test input grid
- Strategy Interface v2
- Grid Object Extractor v1
- Color Transform Detector v1
- Shape / Symmetry Detector v1

## Generated candidate types

Candidate Generator v1 produces:

- `IDENTITY_BASELINE`
- `COLOR_REMAP`
- `SHAPE_TRANSFORM`
- `COLOR_SHAPE_COMBINED`

The combined candidate is ranked first when both stable color and stable shape signals exist.

## Solver relevance

This module feeds future Milestone #4 modules:

- Candidate Ranker v1
- Expanded Batch Benchmark v2
- Score Regression Report v1
- Local Submission Format Candidate v1

## Leaderboard orientation

Milestone #4 target profile remains active:

- top 10 entry score target: `0.60`
- top 5 target: `0.65`
- podium attack target: `0.68`
- leader score target: `1.30`

Candidate Generator v1 does not itself guarantee score improvement. It creates deterministic candidate outputs that can be ranked, tested and benchmarked.

## Boundary

Candidate Generator v1 does not:

- send Kaggle submissions
- call external APIs
- read credentials
- import private HBCE/JOKER-C2 runtime logic
- expose private IPR memory
- claim legal certification

## Acceptance criteria

Candidate Generator v1 is PASS only if:

- all tests pass
- candidate generation is deterministic
- identity candidate is generated
- color remap candidate is generated
- shape transform candidate is generated
- combined color+shape candidate is generated
- combined candidate is ranked first in smoke case
- previous solver modules are used
- best candidate matches expected smoke output
- generation report is validated
- JSON artifact is generated
- Markdown artifact is generated
- public-safe metadata is true
- score-oriented metadata is true
- candidate generator output metadata is true
- candidate ranker input metadata is true
- external API dependency is false
- Kaggle submission sent is false
- private core exposure is false

## Operational markers

ARC_AGI3_MILESTONE_4_TASK_5_CANDIDATE_GENERATOR_V1_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_STATUS=CANDIDATE_GENERATOR_READY  
ARC_AGI3_MILESTONE_4_TASK_5_PIPELINE_STATUS=CANDIDATE_GENERATOR_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_5_VALIDATION=CANDIDATE_GENERATION_VALID  
ARC_AGI3_MILESTONE_4_TASK_5_CANDIDATE_COUNT_SMOKE=4  
ARC_AGI3_MILESTONE_4_TASK_5_BEST_CANDIDATE_TYPE_SMOKE=COLOR_SHAPE_COMBINED  
ARC_AGI3_MILESTONE_4_TASK_5_BEST_CANDIDATE_MATCHES_EXPECTED_SMOKE=true  
ARC_AGI3_MILESTONE_4_TASK_5_IDENTITY_CANDIDATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_COLOR_REMAP_CANDIDATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_SHAPE_TRANSFORM_CANDIDATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_COLOR_SHAPE_COMBINED_CANDIDATE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_USES_STRATEGY_INTERFACE_V2=true  
ARC_AGI3_MILESTONE_4_TASK_5_USES_GRID_OBJECT_EXTRACTOR_V1=true  
ARC_AGI3_MILESTONE_4_TASK_5_USES_COLOR_TRANSFORM_DETECTOR_V1=true  
ARC_AGI3_MILESTONE_4_TASK_5_USES_SHAPE_SYMMETRY_DETECTOR_V1=true  
ARC_AGI3_MILESTONE_4_TASK_5_CANDIDATE_GENERATOR_OUTPUT=true  
ARC_AGI3_MILESTONE_4_TASK_5_CANDIDATE_RANKER_INPUT=true  
ARC_AGI3_MILESTONE_4_TASK_5_AGENTIC_STATE_FEATURE=true  
ARC_AGI3_MILESTONE_4_TASK_5_SCORE_ORIENTED=true  
ARC_AGI3_MILESTONE_4_TASK_5_PRIZE_ORIENTED_SOLVER_TARGET=true  
ARC_AGI3_MILESTONE_4_TASK_5_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_5_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
