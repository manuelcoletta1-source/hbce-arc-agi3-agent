# ARC-AGI-3 Failure Taxonomy v1

Status: FAILURE_TAXONOMY_READY
Taxonomy status: FAILURE_TAXONOMY_VALID
Taxonomy report ID: FAILURE-TAXONOMY-REPORT-FC3663E93EA3
Strategy index ID: STRATEGY-SELECTION-INDEX-6DA2C585190E
Aggregate ID: MULTI-TASK-OUTCOME-9A52836EEB09
Batch ID: BATCH-BENCHMARK-5748D8399B3A
Registry ID: DATASET-SAMPLE-REGISTRY-21F03BA2C85E
Selected strategy: identity_baseline_v1
Total outcomes: 3
Exact match count: 2
Partial count: 1
Failure count: 0
Unverified count: 0
Primary failure class: PARTIAL_TRANSFORM_REFERENCE_MISMATCH
Severity band: LOW

## Taxonomy entries

### FAILURE-TAXONOMY-6F67521D9808

- Task ID: BATCH-TASK-CF3376CA69F0
- Sample ID: SAMPLE-B4DD92F8949D
- Sample name: partial-transform-reference
- Outcome status: OUTCOME_PARTIAL
- Failure class: PARTIAL_TRANSFORM_REFERENCE_MISMATCH
- Severity: LOW
- Partial: true
- Failure: false
- Remediation hint: Inspect transformation reference and add targeted repair strategy before release candidate selection.
- Signature: 6F67521D98085EEB

### FAILURE-TAXONOMY-AF2E8D0B01FF

- Task ID: BATCH-TASK-CCC2336D8AF5
- Sample ID: SAMPLE-84E8BE15DED7
- Sample name: identity-single-object
- Outcome status: OUTCOME_MATCH
- Failure class: NO_FAILURE_EXACT_MATCH
- Severity: NONE
- Partial: false
- Failure: false
- Remediation hint: No remediation required for exact public benchmark match.
- Signature: AF2E8D0B01FF531A

### FAILURE-TAXONOMY-D702E7054DFA

- Task ID: BATCH-TASK-CCBB59ECD386
- Sample ID: SAMPLE-1DE9E816D958
- Sample name: preserve-non-background
- Outcome status: OUTCOME_MATCH
- Failure class: NO_FAILURE_EXACT_MATCH
- Severity: NONE
- Partial: false
- Failure: false
- Remediation hint: No remediation required for exact public benchmark match.
- Signature: D702E7054DFA7C3E

## Boundary

- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false

Taxonomy signature: FC3663E93EA3B387
