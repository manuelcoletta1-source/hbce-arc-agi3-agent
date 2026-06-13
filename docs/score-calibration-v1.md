# ARC-AGI-3 Score Calibration v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_SCORE_CALIBRATION_V1  
Boundary: deterministic score calibration only.

## Purpose

Score Calibration v1 converts Outcome Verification v1 results into calibrated score, grade, quality band, confidence, and deterministic signature.

It creates an operational interpretation layer for verification results.

A raw score alone is not enough. The system must also say whether that score means perfect match, partial match, failed match, or unverifiable output.

## Pipeline position

Score Calibration v1 extends the Milestone #2 chain:

task_loader → observer → world_model → object_model → rule_hypothesis → planner_strategy → outcome_verification → score_calibration → verification_scoring → trace_schema

## Capabilities

Score Calibration v1 provides:

- raw score extraction from outcome verification
- calibrated score
- grade
- quality band
- confidence
- exact-match calibration
- partial-match calibration
- shape-mismatch calibration
- expected-unavailable calibration
- deterministic score signature
- validation contract
- public-safe metadata

## Calibration bands

Initial deterministic bands:

- A_PLUS / PERFECT: exact match
- A / EXCELLENT: score >= 0.90
- B / STRONG: score >= 0.75
- C / PARTIAL: score >= 0.50
- D / WEAK: score > 0.00
- F / FAILED: score == 0.00 with expected output available
- UNVERIFIED / UNVERIFIED: expected output unavailable

## Safety boundary

Score Calibration v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Score Calibration v1 is PASS only if:

- all tests pass
- exact matches calibrate to A_PLUS / PERFECT
- partial matches calibrate deterministically
- shape mismatches calibrate to failed
- expected-unavailable results calibrate to unverifiable
- outcome verification input is accepted
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_SCORE_CALIBRATION_V1_READY=true  
ARC_AGI3_SCORE_CALIBRATION_STATUS=SCORE_CALIBRATION_READY  
ARC_AGI3_SCORE_CALIBRATION_PIPELINE_STATUS=SCORE_CALIBRATION_PIPELINE_READY  
ARC_AGI3_SCORE_CALIBRATION_VALIDATION=SCORE_CALIBRATION_VALID  
ARC_AGI3_SCORE_CALIBRATION_USES_OUTCOME_VERIFICATION=true  
ARC_AGI3_SCORE_CALIBRATION_DETERMINISTIC_SIGNATURE=true  
ARC_AGI3_MILESTONE_2_TASK_7_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
