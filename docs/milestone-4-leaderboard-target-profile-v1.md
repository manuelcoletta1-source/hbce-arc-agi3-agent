# ARC-AGI-3 Milestone #4 — Leaderboard Target Profile v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Source: user-provided live leaderboard snapshot, verified against public Kaggle leaderboard direction.  
Mode: PRIZE_ORIENTED_SOLVER_TARGET_PROFILE  

## Purpose

This profile records the live competitive target for Milestone #4 Solver Engine v1.

Milestone #4 is not only a code milestone. It is a score-oriented milestone. The solver engine must be judged by measurable ranking progress.

The current strategic objective is:

1. enter top 10
2. pass top 5 threshold
3. reach podium range
4. prepare long-range path toward leader score

## Live leaderboard target snapshot

| Rank | Team | Score | Strategic meaning |
|---:|---|---:|---|
| 1 | Tufa Labs | 1.30 | Leader target |
| 2 | Redfield Rentals | 0.68 | Podium threshold |
| 3 | Barada Sahu | 0.66 | Podium / top 3 band |
| 4 | Kevin E R MILLE | 0.66 | Podium / top 5 band |
| 5 | SVG | 0.65 | Top 5 threshold |
| 6 | Matthew Philip Poetker | 0.64 | Top 10 upper band |
| 7 | [a-z A-Z] [1-9] | 0.63 | Top 10 band |
| 8 | face-of-agi | 0.63 | Top 10 band |
| 9 | Kamado Tanjiro | 0.61 | Top 10 lower band |
| 10 | Tong Hui Kang | 0.60 | Top 10 entry threshold |

## Score targets

- Top 10 entry target: `0.60`
- Top 5 target: `0.65`
- Podium attack target: `0.68`
- Leader target: `1.30`
- Minimum useful Milestone #4 result: measurable improvement over Milestone #3 local baseline
- Strategic Milestone #4 result: local solver architecture capable of targeting the `0.60+` public leaderboard band

## Official prize split reference

Official ARC-AGI-3 prize structure used for planning:

- total prize pool: `$850,000`
- grand prize target: `$700,000`
- top score award pool: `$75,000`
- milestone prize pool: `$75,000`
- guaranteed non-grand-prize pool: `$150,000`

This repository treats the prize values as planning targets only. No prize claim is made by this repository.

## Strategy implication

The public solver cannot remain only a static grid transformer.

ARC-AGI-3 is an interactive reasoning benchmark. The solver direction must therefore include:

- action policy interface
- episode state memory
- exploration strategy
- reward/progress detection
- transition observation
- candidate action generation
- candidate action ranking
- fallback policy
- replay-driven regression

Grid transformation remains useful as a submodule, but the scoring target requires agentic behavior.

## Immediate impact on Task 1

Strategy Interface v2 must be treated as the first layer of a broader agentic solver interface.

It should support:

- normalized task input
- deterministic strategy descriptors
- deterministic result payloads
- scoring hints
- ranking hints
- leaderboard target metadata
- future action-policy extension
- future episode-state extension

## Operational markers

ARC_AGI3_MILESTONE_4_LEADERBOARD_TARGET_PROFILE_V1_READY=true  
ARC_AGI3_MILESTONE_4_OFFICIAL_TOTAL_PRIZE_USD=850000  
ARC_AGI3_MILESTONE_4_OFFICIAL_GRAND_PRIZE_USD=700000  
ARC_AGI3_MILESTONE_4_OFFICIAL_TOP_SCORE_AWARD_POOL_USD=75000  
ARC_AGI3_MILESTONE_4_OFFICIAL_MILESTONE_PRIZE_POOL_USD=75000  
ARC_AGI3_MILESTONE_4_OFFICIAL_GUARANTEED_NON_GRAND_PRIZE_POOL_USD=150000  
ARC_AGI3_MILESTONE_4_CURRENT_TOP_10_ENTRY_SCORE=0.60  
ARC_AGI3_MILESTONE_4_CURRENT_TOP_5_SCORE=0.65  
ARC_AGI3_MILESTONE_4_CURRENT_PODIUM_ATTACK_SCORE=0.68  
ARC_AGI3_MILESTONE_4_CURRENT_LEADER_SCORE=1.30  
ARC_AGI3_MILESTONE_4_CURRENT_LEADER_TEAM=Tufa_Labs  
ARC_AGI3_MILESTONE_4_TARGET_ENTER_TOP_10=true  
ARC_AGI3_MILESTONE_4_TARGET_PASS_TOP_5=true  
ARC_AGI3_MILESTONE_4_TARGET_ATTACK_PODIUM=true  
ARC_AGI3_MILESTONE_4_AGENTIC_SOLVER_REQUIRED=true  
ARC_AGI3_MILESTONE_4_STATIC_GRID_ONLY_INSUFFICIENT=true  
ARC_AGI3_MILESTONE_4_TASK_1_LEADERBOARD_PROFILE_ATTACHED=true  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
