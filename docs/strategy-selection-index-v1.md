# ARC-AGI-3 Strategy Selection Index v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #3  
Task: #4  
Mode: PUBLIC_STRATEGY_SELECTION_INDEX_V1  
Boundary: deterministic public strategy selection only.

## Purpose

Strategy Selection Index v1 builds a deterministic public index of strategy candidates from the Multi-Task Outcome Aggregator v1 result.

It ranks public strategy candidates, selects the current best validated public strategy, records score and confidence, and produces JSON and Markdown artifacts.

The module does not expose private HBCE/JOKER-C2 strategy logic. It only uses public benchmark signals already generated in the repository.

## Pipeline position

Strategy Selection Index v1 extends the Milestone #3 chain:

dataset_sample_registry → batch_benchmark_runner → multi_task_outcome_aggregator → strategy_selection_index → failure_taxonomy → report_index_generator → local_submission_candidate_builder → public_readiness_audit → milestone_3_dry_run_release_package → milestone_3_closure

## Input

Strategy Selection Index v1 consumes:

- Multi-Task Outcome Aggregator v1
- aggregate ID
- batch ID
- registry ID
- matched count
- partial count
- failed count
- unverified count
- average calibrated score
- exact match rate
- aggregate verdict

## Output

Strategy Selection Index v1 produces:

- strategy selection index ID
- strategy candidates
- deterministic ranking
- selected strategy ID
- selected strategy name
- selected score
- selected quality band
- candidate signatures
- index signature
- JSON artifact
- Markdown artifact

## Current selection

The current selected public strategy is:

`identity_baseline_v1`

Reason:

It has the highest validated public score from the current multi-task outcome aggregate.

Current public score:

`0.916667`

Current quality band:

`STRONG`

## Safety boundary

Strategy Selection Index v1 does not:

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

Strategy Selection Index v1 is PASS only if:

- all tests pass
- Multi-Task Outcome Aggregator v1 is consumed
- aggregate payload validation is enforced
- strategy candidates are generated
- exactly one strategy is selected
- selected strategy is deterministic
- candidate ranking is deterministic
- selected score is recorded
- selected quality band is recorded
- Markdown artifact is generated
- JSON artifact is generated
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_STRATEGY_SELECTION_INDEX_V1_READY=true  
ARC_AGI3_STRATEGY_SELECTION_STATUS=STRATEGY_SELECTION_INDEX_READY  
ARC_AGI3_STRATEGY_SELECTION_PIPELINE_STATUS=STRATEGY_SELECTION_INDEX_PIPELINE_READY  
ARC_AGI3_STRATEGY_SELECTION_VALIDATION=STRATEGY_SELECTION_INDEX_VALID  
ARC_AGI3_STRATEGY_SELECTION_USES_MULTI_TASK_OUTCOME_AGGREGATOR=true  
ARC_AGI3_STRATEGY_SELECTION_USES_BATCH_BENCHMARK_RUNNER=true  
ARC_AGI3_STRATEGY_SELECTION_USES_DATASET_SAMPLE_REGISTRY=true  
ARC_AGI3_STRATEGY_SELECTION_CANDIDATE_COUNT=3  
ARC_AGI3_STRATEGY_SELECTION_SELECTED_ID=STRATEGY-IDENTITY-BASELINE-v1  
ARC_AGI3_STRATEGY_SELECTION_SELECTED_NAME=identity_baseline_v1  
ARC_AGI3_STRATEGY_SELECTION_SELECTED_SCORE=0.916667  
ARC_AGI3_STRATEGY_SELECTION_SELECTED_QUALITY_BAND=STRONG  
ARC_AGI3_STRATEGY_SELECTION_ARTIFACTS_READY=true  
ARC_AGI3_MILESTONE_3_TASK_4_STATUS=PASS_READY_FOR_COMMIT  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
