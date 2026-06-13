# ARC-AGI-3 Milestone #4 Task 4 — Shape / Symmetry Detector v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Task: #4  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Target: deterministic shape and symmetry detection for Candidate Generator and Candidate Ranker.

## Purpose

Shape / Symmetry Detector v1 detects how foreground shapes move or transform between ARC-style input/output training pairs.

This module converts grid pairs into geometric signals that future solver modules can use to generate and rank candidates. It detects foreground masks, bounding boxes, centroid movement, rotations, reflections, translations and basic symmetry profiles.

The purpose is simple: make the solver understand that a shape moved or rotated, instead of treating every grid like a cursed spreadsheet.

## Extracted signals

Shape / Symmetry Detector v1 produces:

- foreground cells
- foreground bounding box
- foreground centroid
- foreground binary mask
- mask signatures
- identity shape signal
- rotation 90 / 180 / 270 signal
- horizontal reflection signal
- vertical reflection signal
- translation vector
- bbox delta
- centroid delta
- symmetry profile
- pair transform type
- aggregate dominant transform type
- stable transform type across pairs
- deterministic signatures

## Solver relevance

This module feeds future Milestone #4 modules:

- Candidate Generator v1
- Candidate Ranker v1
- Expanded Batch Benchmark v2
- Score Regression Report v1

It builds on the previous solver modules:

- Strategy Interface v2
- Grid Object Extractor v1
- Color Transform Detector v1

## Leaderboard orientation

Milestone #4 target profile remains active:

- top 10 entry score target: `0.60`
- top 5 target: `0.65`
- podium attack target: `0.68`
- leader score target: `1.30`

Shape / Symmetry Detector v1 does not itself guarantee score improvement. It creates geometric candidate-generation and ranking signals required for score-improving strategies.

## Boundary

Shape / Symmetry Detector v1 does not:

- send Kaggle submissions
- call external APIs
- read credentials
- import private HBCE/JOKER-C2 runtime logic
- expose private IPR memory
- claim legal certification

## Acceptance criteria

Shape / Symmetry Detector v1 is PASS only if:

- all tests pass
- mask normalization is present
- foreground mask extraction is present
- bounding box extraction is present
- centroid extraction is present
- rotation 90 is detected
- rotation 180 is detected
- rotation 270 is detected
- horizontal reflection is detected
- vertical reflection is detected
- translation is detected
- symmetry profile is computed
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

ARC_AGI3_MILESTONE_4_TASK_4_SHAPE_SYMMETRY_DETECTOR_V1_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_STATUS=SHAPE_SYMMETRY_DETECTOR_READY  
ARC_AGI3_MILESTONE_4_TASK_4_PIPELINE_STATUS=SHAPE_SYMMETRY_DETECTOR_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_4_VALIDATION=SHAPE_SYMMETRY_DETECTION_VALID  
ARC_AGI3_MILESTONE_4_TASK_4_PAIR_COUNT_SMOKE=2  
ARC_AGI3_MILESTONE_4_TASK_4_DOMINANT_TRANSFORM_TYPE_SMOKE=ROTATE_90  
ARC_AGI3_MILESTONE_4_TASK_4_STABLE_TRANSFORM_TYPE_SMOKE=ROTATE_90  
ARC_AGI3_MILESTONE_4_TASK_4_ROTATION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_REFLECTION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_TRANSLATION_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_BBOX_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_CENTROID_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_MASK_SIGNATURE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_SYMMETRY_PROFILE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_CANDIDATE_GENERATOR_SIGNAL=true  
ARC_AGI3_MILESTONE_4_TASK_4_CANDIDATE_RANKER_SIGNAL=true  
ARC_AGI3_MILESTONE_4_TASK_4_AGENTIC_STATE_FEATURE=true  
ARC_AGI3_MILESTONE_4_TASK_4_SCORE_ORIENTED=true  
ARC_AGI3_MILESTONE_4_TASK_4_PRIZE_ORIENTED_SOLVER_TARGET=true  
ARC_AGI3_MILESTONE_4_TASK_4_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_4_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
