# ARC-AGI-3 Dataset Sample Registry v1

Status: DATASET_SAMPLE_REGISTRY_READY
Registry status: DATASET_SAMPLE_REGISTRY_VALID
Registry ID: DATASET-SAMPLE-REGISTRY-21F03BA2C85E
Sample count: 3

## Samples

### SAMPLE-1DE9E816D958

- Name: preserve-non-background
- Split: public-smoke
- Input shape: [3, 3]
- Expected shape: [3, 3]
- Signature: A2C6C96F7FD4A5B2
- Tags: preserve-structure, smoke, vertical-object

### SAMPLE-84E8BE15DED7

- Name: identity-single-object
- Split: public-smoke
- Input shape: [3, 3]
- Expected shape: [3, 3]
- Signature: 74D13AA0B3EDAF50
- Tags: identity, object-preservation, smoke

### SAMPLE-B4DD92F8949D

- Name: partial-transform-reference
- Split: public-smoke
- Input shape: [2, 2]
- Expected shape: [2, 2]
- Signature: 06B949481F5B43D2
- Tags: partial, score-calibration, smoke

## Boundary

- public_safe=true
- deterministic=true
- external_api_dependency=false
- executes_dataset_code=false
- contains_api_keys=false
- kaggle_submission_sent=false
- private_core_exposure=false

Registry signature: 21F03BA2C85EF72F
