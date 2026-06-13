# ARC-AGI-3 Benchmark Report Generator v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #2  
Mode: PUBLIC_BENCHMARK_REPORT_GENERATOR_V1  
Boundary: deterministic public benchmark report generation only.

## Purpose

Benchmark Report Generator v1 converts Score Calibration v1 results into deterministic public benchmark reports.

It creates a readable artifact containing task id, score, grade, quality band, confidence, findings, signatures, metadata, and public safety boundary.

The goal is simple: a benchmark result should be reproducible, readable, and auditable. Apparently this must be stated because terminal output is where evidence goes to become archaeology.

## Pipeline position

Benchmark Report Generator v1 extends the Milestone #2 chain:

task_loader → observer → world_model → object_model → rule_hypothesis → planner_strategy → outcome_verification → score_calibration → benchmark_report → verification_scoring → trace_schema

## Capabilities

Benchmark Report Generator v1 provides:

- deterministic benchmark report generation
- score calibration ingestion
- outcome verification signature linking
- score calibration signature linking
- report status
- task id
- raw score
- calibrated score
- grade
- quality band
- confidence
- findings
- deterministic Markdown rendering
- report signature
- validation contract
- public-safe metadata

## Report statuses

Initial deterministic statuses:

- BENCHMARK_REPORT_MATCH
- BENCHMARK_REPORT_PARTIAL
- BENCHMARK_REPORT_FAILED
- BENCHMARK_REPORT_UNVERIFIED
- BENCHMARK_REPORT_READY

## Safety boundary

Benchmark Report Generator v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- send a Kaggle submission

## Acceptance criteria

Benchmark Report Generator v1 is PASS only if:

- all tests pass
- partial reports are generated
- exact-match reports are generated
- expected-unavailable reports are generated
- score calibration inputs are accepted
- Markdown rendering is deterministic
- Markdown writing works locally
- report validation rejects broken contracts
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_BENCHMARK_REPORT_GENERATOR_V1_READY=true  
ARC_AGI3_BENCHMARK_REPORT_STATUS=BENCHMARK_REPORT_READY  
ARC_AGI3_BENCHMARK_REPORT_PIPELINE_STATUS=BENCHMARK_REPORT_PIPELINE_READY  
ARC_AGI3_BENCHMARK_REPORT_VALIDATION=BENCHMARK_REPORT_VALID  
ARC_AGI3_BENCHMARK_REPORT_USES_SCORE_CALIBRATION=true  
ARC_AGI3_BENCHMARK_REPORT_USES_OUTCOME_VERIFICATION=true  
ARC_AGI3_BENCHMARK_REPORT_MARKDOWN_READY=true  
ARC_AGI3_BENCHMARK_REPORT_DETERMINISTIC_SIGNATURE=true  
ARC_AGI3_MILESTONE_2_TASK_8_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
