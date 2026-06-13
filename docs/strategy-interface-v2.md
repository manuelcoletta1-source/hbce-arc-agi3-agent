# ARC-AGI-3 Milestone #4 Task 1 — Strategy Interface v2

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Task: #1  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Target: prize-oriented deterministic solver engine.

## Purpose

Strategy Interface v2 defines the common public contract for Milestone #4 solver strategies.

Milestone #3 closed the verified public pipeline. Milestone #4 now moves toward scoring. The strategy interface exists so every solver module can receive a normalized input, return a deterministic candidate output, expose metadata, and remain compatible with benchmark, ranking, regression and local submission-format tooling.

The interface is deliberately boring in the right places. Boring contracts are how we avoid a solver engine that behaves like a drawer full of cables.

## Components

Strategy Interface v2 introduces:

- normalized grid validation
- strategy training example contract
- strategy input contract
- strategy descriptor contract
- strategy result contract
- solver strategy protocol
- default strategy registry
- identity baseline strategy v2
- deterministic pipeline smoke test
- JSON and Markdown smoke artifacts

## Leaderboard target orientation

Strategy Interface v2 is now linked to the Milestone #4 Leaderboard Target Profile v1.

Current live target bands:

- `top_10_entry_score=0.60`
- `top_5_score=0.65`
- `podium_attack_score=0.68`
- `leader_score=1.30`
- `leader_team=Tufa Labs`

This means the strategy interface must support future solver components that rank not only final grids, but also action policies, episode states and agentic exploration behavior.

Static grid transformation is useful, but it is not sufficient by itself for the ARC-AGI-3 target profile.


## Result orientation

This task is not a final solver. It is the public strategy foundation for a solver engine that must improve score under Milestone #4.

Milestone #4 remains:

- prize-oriented
- score-oriented
- result-required
- local-only
- dry-run-only
- public-safe
- deterministic

## Boundary

Strategy Interface v2 does not:

- send Kaggle submissions
- call external APIs
- read credentials
- import private HBCE/JOKER-C2 runtime logic
- expose private IPR memory
- claim legal certification

## Acceptance criteria

Strategy Interface v2 is PASS only if:

- all tests pass
- normalized grid validation is present
- strategy descriptor validation is present
- strategy result validation is present
- default registry is present
- identity baseline v2 is present
- pipeline smoke test returns valid payload
- artifact JSON is generated
- artifact Markdown is generated
- public-safe metadata is true
- score-oriented metadata is true
- prize-oriented solver target is true
- external API dependency is false
- Kaggle submission sent is false
- private core exposure is false

## Operational markers

ARC_AGI3_MILESTONE_4_TASK_1_STRATEGY_INTERFACE_V2_READY=true  
ARC_AGI3_MILESTONE_4_TASK_1_LEADERBOARD_PROFILE_ATTACHED=true  
ARC_AGI3_MILESTONE_4_TASK_1_OFFICIAL_TOTAL_PRIZE_USD=850000  
ARC_AGI3_MILESTONE_4_TASK_1_OFFICIAL_GRAND_PRIZE_USD=700000  
ARC_AGI3_MILESTONE_4_TASK_1_OFFICIAL_TOP_SCORE_AWARD_POOL_USD=75000  
ARC_AGI3_MILESTONE_4_TASK_1_OFFICIAL_MILESTONE_PRIZE_POOL_USD=75000  
ARC_AGI3_MILESTONE_4_TASK_1_TARGET_TOP_10_ENTRY_SCORE=0.60  
ARC_AGI3_MILESTONE_4_TASK_1_TARGET_TOP_5_SCORE=0.65  
ARC_AGI3_MILESTONE_4_TASK_1_TARGET_PODIUM_ATTACK_SCORE=0.68  
ARC_AGI3_MILESTONE_4_TASK_1_TARGET_LEADER_SCORE=1.30  
ARC_AGI3_MILESTONE_4_TASK_1_AGENTIC_EXTENSION_REQUIRED=true  
ARC_AGI3_MILESTONE_4_TASK_1_STATUS=STRATEGY_INTERFACE_V2_READY  
ARC_AGI3_MILESTONE_4_TASK_1_PIPELINE_STATUS=STRATEGY_INTERFACE_V2_PIPELINE_READY  
ARC_AGI3_MILESTONE_4_TASK_1_VALIDATION=STRATEGY_INTERFACE_V2_VALID  
ARC_AGI3_MILESTONE_4_TASK_1_REGISTRY_READY=true  
ARC_AGI3_MILESTONE_4_TASK_1_IDENTITY_BASELINE_READY=true  
ARC_AGI3_MILESTONE_4_TASK_1_STRATEGY_COUNT=1  
ARC_AGI3_MILESTONE_4_TASK_1_CANDIDATE_COUNT=1  
ARC_AGI3_MILESTONE_4_TASK_1_SCORE_ORIENTED=true  
ARC_AGI3_MILESTONE_4_TASK_1_PRIZE_ORIENTED_SOLVER_TARGET=true  
ARC_AGI3_MILESTONE_4_TASK_1_RESULT_REQUIRED=true  
ARC_AGI3_MILESTONE_4_TASK_1_SCORE_IMPROVEMENT_REQUIRED=true  
ARC_AGI3_MILESTONE_4_TASK_1_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_4_TASK_1_STATUS_FOR_COMMIT=PASS_READY_FOR_COMMIT  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
