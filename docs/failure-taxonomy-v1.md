# ARC-AGI-3 Failure Taxonomy v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #3  
Task: #5  
Mode: PUBLIC_FAILURE_TAXONOMY_V1  
Boundary: deterministic public failure classification only.

## Purpose

Failure Taxonomy v1 classifies deterministic public benchmark outcomes into stable failure classes.

It consumes the Strategy Selection Index v1 and Multi-Task Outcome Aggregator v1 chain, then generates per-outcome taxonomy entries and a report-level summary.

The purpose is not to claim model intelligence. The purpose is to create a transparent public evaluation layer that says exactly where the current public strategy matched, partially matched, failed, or remained unverified.

## Pipeline position

Failure Taxonomy v1 extends the Milestone #3 chain:

dataset_sample_registry → batch_benchmark_runner → multi_task_outcome_aggregator → strategy_selection_index → failure_taxonomy → report_index_generator → local_submission_candidate_builder → public_readiness_audit → milestone_3_dry_run_release_package → milestone_3_closure

## Input

Failure Taxonomy v1 consumes:

- Strategy Selection Index v1
- Multi-Task Outcome Aggregator v1
- selected strategy ID
- selected strategy name
- aggregate ID
- batch ID
- registry ID
- outcome records
- exact match flags
- cell accuracy
- mismatch counts
- outcome status

## Output

Failure Taxonomy v1 produces:

- failure taxonomy report ID
- taxonomy entries
- exact match count
- partial count
- failure count
- unverified count
- primary failure class
- severity band
- remediation hints
- taxonomy signatures
- JSON artifact
- Markdown artifact

## Current taxonomy state

For the current public sample registry and identity baseline:

- total_outcomes=3
- exact_match_count=2
- partial_count=1
- failure_count=0
- unverified_count=0
- primary_failure_class=PARTIAL_TRANSFORM_REFERENCE_MISMATCH
- severity_band=LOW

## Failure classes

Failure Taxonomy v1 currently supports:

- NO_FAILURE_EXACT_MATCH
- PARTIAL_TRANSFORM_REFERENCE_MISMATCH
- HARD_FAILURE_ZERO_OR_INVALID_ACCURACY
- UNVERIFIED_OUTCOME
- UNKNOWN_OUTCOME_CLASS

## Safety boundary

Failure Taxonomy v1 does not:

- execute dataset code
- import dataset Python modules
- call external APIs
- read API keys
- read Kaggle tokens
- expose private HBCE/JOKER-C2 runtime code
- expose private IPR memory
- expose private strategy logic
- send a Kaggle submission

## Acceptance criteria

Failure Taxonomy v1 is PASS only if:

- all tests pass
- Strategy Selection Index v1 is consumed
- Multi-Task Outcome Aggregator v1 is consumed
- aggregate payload validation is enforced
- strategy index validation is enforced
- taxonomy entries are generated
- primary failure class is calculated
- severity band is calculated
- remediation hints are generated
- Markdown artifact is generated
- JSON artifact is generated
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_FAILURE_TAXONOMY_V1_READY=true  
ARC_AGI3_FAILURE_TAXONOMY_STATUS=FAILURE_TAXONOMY_READY  
ARC_AGI3_FAILURE_TAXONOMY_PIPELINE_STATUS=FAILURE_TAXONOMY_PIPELINE_READY  
ARC_AGI3_FAILURE_TAXONOMY_VALIDATION=FAILURE_TAXONOMY_VALID  
ARC_AGI3_FAILURE_TAXONOMY_USES_STRATEGY_SELECTION_INDEX=true  
ARC_AGI3_FAILURE_TAXONOMY_USES_MULTI_TASK_OUTCOME_AGGREGATOR=true  
ARC_AGI3_FAILURE_TAXONOMY_USES_BATCH_BENCHMARK_RUNNER=true  
ARC_AGI3_FAILURE_TAXONOMY_USES_DATASET_SAMPLE_REGISTRY=true  
ARC_AGI3_FAILURE_TAXONOMY_TOTAL_OUTCOMES=3  
ARC_AGI3_FAILURE_TAXONOMY_EXACT_MATCH_COUNT=2  
ARC_AGI3_FAILURE_TAXONOMY_PARTIAL_COUNT=1  
ARC_AGI3_FAILURE_TAXONOMY_FAILURE_COUNT=0  
ARC_AGI3_FAILURE_TAXONOMY_UNVERIFIED_COUNT=0  
ARC_AGI3_FAILURE_TAXONOMY_PRIMARY_CLASS=PARTIAL_TRANSFORM_REFERENCE_MISMATCH  
ARC_AGI3_FAILURE_TAXONOMY_SEVERITY_BAND=LOW  
ARC_AGI3_FAILURE_TAXONOMY_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_3_TASK_5_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
