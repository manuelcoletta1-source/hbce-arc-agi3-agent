# ARC-AGI-3 Report Index Generator v1

Status: REPORT_INDEX_GENERATOR_READY
Index status: REPORT_INDEX_VALID
Report index ID: REPORT-INDEX-380079FFB6E9
Milestone: Milestone #3
Indexed report count: 5
Indexed artifact count: 15
Ready report count: 5

## Source chain

- dataset_sample_registry_id: DATASET-SAMPLE-REGISTRY-21F03BA2C85E
- batch_id: BATCH-BENCHMARK-5748D8399B3A
- multi_task_outcome_aggregate_id: MULTI-TASK-OUTCOME-9A52836EEB09
- strategy_selection_index_id: STRATEGY-SELECTION-INDEX-6DA2C585190E
- failure_taxonomy_report_id: FAILURE-TAXONOMY-REPORT-FC3663E93EA3
- selected_strategy_id: STRATEGY-IDENTITY-BASELINE-v1
- selected_strategy_name: identity_baseline_v1
- primary_failure_class: PARTIAL_TRANSFORM_REFERENCE_MISMATCH
- severity_band: LOW

## Indexed reports

### Batch Benchmark Runner v1

- Key: batch_benchmark_runner_v1
- Type: public_benchmark_report
- Task: Task 2
- Module: batch_benchmark_runner
- Primary path: `docs/batch-benchmark-runner-v1.md`
- Ready marker: `ARC_AGI3_BATCH_BENCHMARK_RUNNER_V1_READY=true`
- Signature: BD641A236E139AC7

Artifacts:

- `examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.json`
- `examples/milestone-3/batch-benchmark-runner/batch-benchmark-run.md`

### Dataset Sample Registry v1

- Key: dataset_sample_registry_v1
- Type: public_registry_report
- Task: Task 1
- Module: dataset_sample_registry
- Primary path: `docs/dataset-sample-registry-v1.md`
- Ready marker: `ARC_AGI3_DATASET_SAMPLE_REGISTRY_V1_READY=true`
- Signature: 7789DA2624655648

Artifacts:

- `examples/milestone-3/dataset-sample-registry/dataset-sample-registry.json`
- `examples/milestone-3/dataset-sample-registry/dataset-sample-registry.md`

### Failure Taxonomy v1

- Key: failure_taxonomy_v1
- Type: public_failure_taxonomy_report
- Task: Task 5
- Module: failure_taxonomy
- Primary path: `docs/failure-taxonomy-v1.md`
- Ready marker: `ARC_AGI3_FAILURE_TAXONOMY_V1_READY=true`
- Signature: 1EA5B0AAB473E370

Artifacts:

- `examples/milestone-3/failure-taxonomy/failure-taxonomy-report.json`
- `examples/milestone-3/failure-taxonomy/failure-taxonomy-report.md`

### Multi-Task Outcome Aggregator v1

- Key: multi_task_outcome_aggregator_v1
- Type: public_outcome_aggregate_report
- Task: Task 3
- Module: multi_task_outcome_aggregator
- Primary path: `docs/multi-task-outcome-aggregator-v1.md`
- Ready marker: `ARC_AGI3_MULTI_TASK_OUTCOME_AGGREGATOR_V1_READY=true`
- Signature: 767628F9C7956DED

Artifacts:

- `examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.json`
- `examples/milestone-3/multi-task-outcome-aggregator/multi-task-outcome-aggregate.md`

### Strategy Selection Index v1

- Key: strategy_selection_index_v1
- Type: public_strategy_selection_report
- Task: Task 4
- Module: strategy_selection_index
- Primary path: `docs/strategy-selection-index-v1.md`
- Ready marker: `ARC_AGI3_STRATEGY_SELECTION_INDEX_V1_READY=true`
- Signature: 1023A5072C380288

Artifacts:

- `examples/milestone-3/strategy-selection-index/strategy-selection-index.json`
- `examples/milestone-3/strategy-selection-index/strategy-selection-index.md`

## Boundary

- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false

Report index signature: 380079FFB6E9B6DC
