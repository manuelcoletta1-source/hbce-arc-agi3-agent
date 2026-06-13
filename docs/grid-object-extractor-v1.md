# ARC-AGI-3 Milestone #4 Task 2 — Grid Object Extractor v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Task: #2  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Target: deterministic object/state extraction for the solver engine.

## Purpose

Grid Object Extractor v1 converts an ARC-style grid into deterministic object/state features.

This is the first Milestone #4 module that moves beyond strategy plumbing and starts producing useful state for solving. The solver needs objects, positions, colors, masks, bounding boxes and signatures before it can reason about transformations, movement, symmetry, ranking or agentic actions.

Without object extraction, the solver is just staring at cells. With object extraction, it begins to see entities.

## Extracted features

Grid Object Extractor v1 produces:

- color inventory
- inferred or supplied background color
- connected same-color objects
- object area
- bounding box
- centroid
- border-touch flag
- relative binary mask
- deterministic object signature
- deterministic extraction report signature
- object density

## Connectivity

The extractor supports:

- 4-neighbor connectivity
- 8-neighbor connectivity

The default mode is 4-neighbor connectivity because it is stricter and usually safer for first-pass ARC object extraction.

## Solver relevance

Grid Object Extractor v1 is designed as an agentic state feature layer.

It supports future modules:

- Color Transform Detector v1
- Shape / Symmetry Detector v1
- Candidate Generator v1
- Candidate Ranker v1
- Expanded Batch Benchmark v2
- Score Regression Report v1

## Leaderboard orientation

Milestone #4 target profile remains active:

- top 10 entry score target: `0.60`
- top 5 target: `0.65`
- podium attack target: `0.68`
- leader score target: `1.30`

The object extractor does not itself guarantee score improvement. It creates the state representation needed for score-improving strategies.

## Boundary

Grid Object Extractor v1 does not:

- send Kaggle submissions
- call external APIs
- read credentials
- import private HBCE/JOKER-C2 runtime logic
- expose private IPR memory
- claim legal certification

## Acceptance criteria

Grid Object Extractor v1 is PASS only if:

- all tests pass
- object extraction is deterministic
- 4-neighbor connected components are supported
- 8-neighbor connected components are supported
- background exclusion is supported
- background inclusion is supported
- object area is computed
- object bounding box is computed
- object centroid is computed
- object mask is computed
- object signatures are computed
- extraction report is validated
- JSON artifact is generated
- Markdown artifact is generated
- public-safe metadata is true
- score-oriented metadata is true
- agentic state feature metadata is true
- external API dependency is false
- Kaggle submission sent is false
- private core exposure is false

## Operational markers

ARC_AGI3_MILESTONE_4_TASK_2_GRID_OBJECT_EXTRACTOR_V1_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_STATUS=GRID_OBJECT_EXTRACTOR_READY  
ARC_AGI3_MILESTONE_4_TASK_2_PIPELINE_STATUS=GRID_OBJECT_EXTRACTOR_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_2_VALIDATION=GRID_OBJECT_EXTRACTION_VALID  
ARC_AGI3_MILESTONE_4_TASK_2_OBJECT_COUNT_SMOKE=3  
ARC_AGI3_MILESTONE_4_TASK_2_OBJECT_DENSITY_SMOKE=0.583333  
ARC_AGI3_MILESTONE_4_TASK_2_CONNECTIVITY_4_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_CONNECTIVITY_8_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_BACKGROUND_EXCLUSION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_BACKGROUND_INCLUSION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_BBOX_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_CENTROID_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_MASK_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_SIGNATURE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_AGENTIC_STATE_FEATURE=true  
ARC_AGI3_MILESTONE_4_TASK_2_SCORE_ORIENTED=true  
ARC_AGI3_MILESTONE_4_TASK_2_PRIZE_ORIENTED_SOLVER_TARGET=true  
ARC_AGI3_MILESTONE_4_TASK_2_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_2_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
