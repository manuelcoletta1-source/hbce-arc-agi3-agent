# ARC-AGI-3 Milestone #4 Task 3 — Color Transform Detector v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Task: #3  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Target: deterministic color transform detection for Candidate Generator and Candidate Ranker.

## Purpose

Color Transform Detector v1 detects how colors change between ARC-style input/output training pairs.

This module converts training examples into transformation signals that future solver modules can use to generate and rank candidates. It detects preserved colors, replaced colors, added colors, removed colors, ambiguous mappings, background mapping and stable aggregate mappings.

The purpose is simple: stop guessing colors like a lottery machine with anxiety.

## Extracted signals

Color Transform Detector v1 produces:

- input palette
- output palette
- added colors
- removed colors
- preserved colors
- changed source colors
- ambiguous source colors
- ambiguous target colors
- dominant color mappings
- background mapping
- pair transform type
- aggregate transform type
- stable mappings across training pairs
- unstable source colors
- deterministic signatures

## Solver relevance

This module feeds future Milestone #4 modules:

- Candidate Generator v1
- Candidate Ranker v1
- Expanded Batch Benchmark v2
- Score Regression Report v1

It also depends on the previous solver foundation:

- Strategy Interface v2
- Grid Object Extractor v1

## Leaderboard orientation

Milestone #4 target profile remains active:

- top 10 entry score target: `0.60`
- top 5 target: `0.65`
- podium attack target: `0.68`
- leader score target: `1.30`

Color Transform Detector v1 does not itself guarantee score improvement. It creates candidate-generation and ranking signals required for score-improving strategies.

## Boundary

Color Transform Detector v1 does not:

- send Kaggle submissions
- call external APIs
- read credentials
- import private HBCE/JOKER-C2 runtime logic
- expose private IPR memory
- claim legal certification

## Acceptance criteria

Color Transform Detector v1 is PASS only if:

- all tests pass
- identity color preservation is detected
- stable color remapping is detected
- palette expansion is detected
- palette reduction is detected
- ambiguous source mapping is detected
- unstable aggregate mappings are detected
- background mapping is detected
- stable mappings can be applied to a grid
- detection report is validated
- JSON artifact is generated
- Markdown artifact is generated
- public-safe metadata is true
- score-oriented metadata is true
- candidate generator signal metadata is true
- candidate ranker signal metadata is true
- external API dependency is false
- Kaggle submission sent is false
- private core exposure is false

## Operational markers

ARC_AGI3_MILESTONE_4_TASK_3_COLOR_TRANSFORM_DETECTOR_V1_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_STATUS=COLOR_TRANSFORM_DETECTOR_READY  
ARC_AGI3_MILESTONE_4_TASK_3_PIPELINE_STATUS=COLOR_TRANSFORM_DETECTOR_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_3_VALIDATION=COLOR_TRANSFORM_DETECTION_VALID  
ARC_AGI3_MILESTONE_4_TASK_3_PAIR_COUNT_SMOKE=2  
ARC_AGI3_MILESTONE_4_TASK_3_STABLE_MAPPING_COUNT_SMOKE=3  
ARC_AGI3_MILESTONE_4_TASK_3_TRANSFORM_TYPE_SMOKE=AGGREGATE_STABLE_COLOR_REMAP  
ARC_AGI3_MILESTONE_4_TASK_3_IDENTITY_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_REMAP_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_PALETTE_EXPANSION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_PALETTE_REDUCTION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_AMBIGUOUS_MAPPING_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_BACKGROUND_MAPPING_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_APPLY_MAPPING_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_CANDIDATE_GENERATOR_SIGNAL=true  
ARC_AGI3_MILESTONE_4_TASK_3_CANDIDATE_RANKER_SIGNAL=true  
ARC_AGI3_MILESTONE_4_TASK_3_AGENTIC_STATE_FEATURE=true  
ARC_AGI3_MILESTONE_4_TASK_3_SCORE_ORIENTED=true  
ARC_AGI3_MILESTONE_4_TASK_3_PRIZE_ORIENTED_SOLVER_TARGET=true  
ARC_AGI3_MILESTONE_4_TASK_3_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_3_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
