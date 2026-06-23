# Milestone #19 Task 89 - SRSC Diagnostic Adapter Local Implementation v1

Project: HBCE ARC-AGI-3 Agent
Organization: HERMETICUM B.C.E. S.r.l.
Task ID: MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_V1
Status: LOCAL_ADAPTER_IMPLEMENTATION_READY
Mode: LOCAL_STANDALONE_ADAPTER_NO_RUNTIME_WIRING
Boundary: legalCertification=false; technical proof receipt only.

## 1. Purpose

Task 89 implements the local standalone SRSC Diagnostic Adapter authorized by Task 88.

Implemented module:

- src/hbce_arc_agi3/srsc_diagnostic_adapter.py

Implemented test:

- tests/test_srsc_diagnostic_adapter.py

The adapter transforms explicit local diagnostic payloads into SRSC diagnostic reference records without creating solver runtime wiring.

## 2. Dependency

Task 89 depends on:

MILESTONE_19_TASK_88_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1

Task 88 authorized local adapter implementation only.

## 3. Implemented Adapter Types

The implementation defines:

- DiagnosticAdapterInput
- DiagnosticAdapterResult
- DiagnosticAdapterBlockedReference
- adapt_diagnostic_input_to_reference
- adapt_diagnostic_inputs_to_references

## 4. Adapter Behavior

The adapter may:

- accept explicit local diagnostic source payloads;
- validate source type;
- validate source path;
- validate diagnostic scope;
- validate SRSC claim and gate identifiers;
- validate claim state and evidence state;
- validate evidence references;
- create SrscDiagnosticReferenceRecord objects;
- return deterministic public JSON;
- return blocked reference reports.

The adapter must not:

- activate inside solver runtime;
- read solver runtime state;
- mutate solver runtime state;
- call candidate generation;
- call ranking;
- call verification;
- execute benchmarks;
- authenticate with Kaggle;
- submit to Kaggle;
- use internet during evaluation;
- expose private core;
- claim legal certification.

## 5. Fail-Closed Rules

The adapter blocks records when:

- input construction fails;
- source path is missing;
- diagnostic scope is missing;
- SRSC identifiers are malformed;
- evidence is missing;
- boundary state is not public-safe;
- claim state is UNKNOWN, CONFLICTING or BLOCKED;
- reference validation fails.

The adapter does not silently repair missing evidence.

The adapter does not convert unknown claims into verified references.

## 6. Controlled Boundary

adapter_implementation_performed=true
local_standalone_adapter=true
adapter_activated=false
runtime_activation_authorized=false
runtime_solver_modified=false
runtime_wiring_allowed=false
candidate_generator_modified=false
ranker_modified=false
verifier_modified=false
benchmark_score_claimed=false
real_evaluation_performed=false
real_submission_authorized=false
kaggle_authentication_performed=false
kaggle_submission_sent=false
internet_during_eval=false
external_api_dependency=false
private_core_exposure=false
legal_certification=false
fail_closed_required=true
fail_closed_active=true

## 7. Canonical Decision

MILESTONE_19_TASK_89_SRSC_DIAGNOSTIC_ADAPTER_LOCAL_IMPLEMENTATION_READY=true
MILESTONE_19_TASK_89_STATUS=LOCAL_ADAPTER_IMPLEMENTATION_READY
MILESTONE_19_TASK_89_MODE=LOCAL_STANDALONE_ADAPTER_NO_RUNTIME_WIRING
MILESTONE_19_TASK_89_ADAPTER_IMPLEMENTATION_PERFORMED=true
MILESTONE_19_TASK_89_LOCAL_STANDALONE_ADAPTER=true
MILESTONE_19_TASK_89_ADAPTER_ACTIVATED=false
MILESTONE_19_TASK_89_RUNTIME_SOLVER_MODIFIED=false
MILESTONE_19_TASK_89_RUNTIME_WIRING_ALLOWED=false
MILESTONE_19_TASK_89_CANDIDATE_GENERATOR_MODIFIED=false
MILESTONE_19_TASK_89_RANKER_MODIFIED=false
MILESTONE_19_TASK_89_VERIFIER_MODIFIED=false
MILESTONE_19_TASK_89_BENCHMARK_SCORE_CLAIMED=false
MILESTONE_19_TASK_89_REAL_EVALUATION_PERFORMED=false
MILESTONE_19_TASK_89_KAGGLE_SUBMISSION_SENT=false
MILESTONE_19_TASK_89_PRIVATE_CORE_EXPOSURE=false
MILESTONE_19_TASK_89_LEGAL_CERTIFICATION=false
MILESTONE_19_TASK_89_FAIL_CLOSED_ACTIVE=true
MILESTONE_19_TASK_89_NEXT_STAGE=MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_V1

## 8. Completion Criteria

Task 89 is complete when:

- Task 88 dependency exists;
- local adapter module exists;
- local adapter tests exist;
- this implementation document exists;
- artifact manifest exists;
- artifact index exists;
- targeted tests pass;
- task chain tests pass;
- full test suite passes;
- repository is committed and pushed cleanly.

## 9. Next Stage

MILESTONE_19_TASK_90_SRSC_DIAGNOSTIC_ADAPTER_IMPLEMENTATION_REVIEW_V1

Task 90 may review the local adapter implementation and decide whether future adapter activation planning is authorized.

Task 90 must not activate the adapter inside solver runtime without a separate explicit authorization.
