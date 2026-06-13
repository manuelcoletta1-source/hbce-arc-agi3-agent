# ARC-AGI-3 Strategy Selection Index v1

Status: STRATEGY_SELECTION_INDEX_READY
Index status: STRATEGY_SELECTION_INDEX_VALID
Index ID: STRATEGY-SELECTION-INDEX-6DA2C585190E
Aggregate ID: MULTI-TASK-OUTCOME-9A52836EEB09
Batch ID: BATCH-BENCHMARK-5748D8399B3A
Registry ID: DATASET-SAMPLE-REGISTRY-21F03BA2C85E
Candidate count: 3
Selected strategy ID: STRATEGY-IDENTITY-BASELINE-v1
Selected strategy name: identity_baseline_v1
Selected score: 0.916667
Selected quality band: STRONG

## Strategy candidates

### Rank 1 - identity_baseline_v1

- Strategy ID: STRATEGY-IDENTITY-BASELINE-v1
- Family: public_baseline
- Score: 0.916667
- Confidence: 0.666667
- Quality band: STRONG
- Selected: true
- Reason: Highest validated public score from current batch outcome aggregate
- Signature: 238D4462F04F0372

### Rank 2 - partial_repair_public_v1

- Strategy ID: STRATEGY-PARTIAL-REPAIR-v1
- Family: public_candidate
- Score: 0.833333
- Confidence: 0.333333
- Quality band: GOOD
- Selected: false
- Reason: Candidate retained for partial-outcome exploration; not selected in this batch
- Signature: A72FAAB0DF475B8D

### Rank 3 - object_preservation_public_v1

- Strategy ID: STRATEGY-OBJECT-PRESERVATION-v1
- Family: public_candidate
- Score: 0.666667
- Confidence: 1.0
- Quality band: PARTIAL
- Selected: false
- Reason: Candidate retained for later public ranking; not selected over validated runner
- Signature: F7AEAA0391890E1A

## Boundary

- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false

Index signature: 6DA2C585190E0C5F
