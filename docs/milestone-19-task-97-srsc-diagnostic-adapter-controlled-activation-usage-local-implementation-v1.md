# Milestone #19 Task 97 - SRSC Diagnostic Adapter Controlled Activation Usage Local Implementation v1

Project: HBCE ARC-AGI-3 Agent
Organization: HERMETICUM B.C.E. S.r.l.
Task ID: MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_V1
Status: CONTROLLED_DIAGNOSTIC_USAGE_LOCAL_IMPLEMENTATION_READY
Mode: LOCAL_DIAGNOSTIC_ONLY_USAGE_NO_RUNTIME_WIRING
Boundary: legalCertification=false; technical proof receipt only.

## 1. Purpose

Task 97 implements the local controlled diagnostic usage layer authorized by Task 96.

Implemented module:

- src/hbce_arc_agi3/srsc_diagnostic_adapter_activation_usage.py

Implemented test:

- tests/test_srsc_diagnostic_adapter_activation_usage.py

The usage layer coordinates controlled diagnostic activation calls for approved local evidence and audit flows.

The usage layer does not wire the activation wrapper into solver runtime.

## 2. Dependency

Task 97 depends on:

MILESTONE_19_TASK_96_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1

Task 96 authorized controlled diagnostic usage implementation only.

## 3. Implemented Usage Types

The implementation defines:

- DiagnosticActivationUsageRequest
- DiagnosticActivationUsageResult
- DiagnosticActivationUsageBlockedRequest
- run_controlled_activation_usage
- run_controlled_activation_usage_batch

## 4. Usage Behavior

The usage layer may:

- accept explicit local diagnostic payloads;
- validate usage contexts;
- validate approved diagnostic call-sites through the activation wrapper;
- call the controlled diagnostic activation wrapper;
- return deterministic public JSON;
- return blocked usage requests;
- preserve no-score markers;
- preserve no-submission markers;
- preserve fail-closed markers.

The usage layer must not:

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

## 5. Allowed Usage Contexts

Allowed usage contexts:

- local SRSC diagnostic report generation;
- local milestone evidence packaging;
- local public-safe audit summary creation;
- local cross-trace planner evidence attachment;
- local blocked-call report generation.

## 6. Forbidden Usage Contexts

Forbidden usage contexts:

- solver runtime execution;
- runtime planner execution;
- agent loop execution;
- candidate generation;
- candidate ranking;
- verifier execution;
- benchmark execution;
- real evaluation execution;
- Kaggle submission packaging;
- score reporting;
- private core execution;
- network/API execution;
- legal certification workflows.

## 7. Controlled Boundary

controlled_usage_implemented=true
diagnostic_usage_only=true
activation_wrapper_modified=false
adapter_modified=false
runtime_activation_authorized=false
runtime_solver_modified=false
runtime_wiring_allowed=false
solver_runtime_binding=false
candidate_generator_modified=false
candidate_generator_binding=false
ranker_modified=false
ranker_binding=false
verifier_modified=false
verifier_binding=false
benchmark_score_claimed=false
benchmark_binding=false
real_evaluation_performed=false
real_submission_authorized=false
kaggle_authentication_performed=false
kaggle_submission_sent=false
kaggle_submission_binding=false
internet_during_eval=false
external_api_dependency=false
private_core_exposure=false
legal_certification=false
fail_closed_required=true
fail_closed_active=true

## 8. Canonical Decision

MILESTONE_19_TASK_97_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_LOCAL_IMPLEMENTATION_READY=true
MILESTONE_19_TASK_97_STATUS=CONTROLLED_DIAGNOSTIC_USAGE_LOCAL_IMPLEMENTATION_READY
MILESTONE_19_TASK_97_MODE=LOCAL_DIAGNOSTIC_ONLY_USAGE_NO_RUNTIME_WIRING
MILESTONE_19_TASK_97_CONTROLLED_USAGE_IMPLEMENTED=true
MILESTONE_19_TASK_97_DIAGNOSTIC_USAGE_ONLY=true
MILESTONE_19_TASK_97_ACTIVATION_WRAPPER_MODIFIED=false
MILESTONE_19_TASK_97_ADAPTER_MODIFIED=false
MILESTONE_19_TASK_97_RUNTIME_SOLVER_MODIFIED=false
MILESTONE_19_TASK_97_RUNTIME_WIRING_ALLOWED=false
MILESTONE_19_TASK_97_SOLVER_RUNTIME_BINDING=false
MILESTONE_19_TASK_97_CANDIDATE_GENERATOR_MODIFIED=false
MILESTONE_19_TASK_97_CANDIDATE_GENERATOR_BINDING=false
MILESTONE_19_TASK_97_RANKER_MODIFIED=false
MILESTONE_19_TASK_97_RANKER_BINDING=false
MILESTONE_19_TASK_97_VERIFIER_MODIFIED=false
MILESTONE_19_TASK_97_VERIFIER_BINDING=false
MILESTONE_19_TASK_97_BENCHMARK_SCORE_CLAIMED=false
MILESTONE_19_TASK_97_BENCHMARK_BINDING=false
MILESTONE_19_TASK_97_REAL_EVALUATION_PERFORMED=false
MILESTONE_19_TASK_97_KAGGLE_SUBMISSION_SENT=false
MILESTONE_19_TASK_97_KAGGLE_SUBMISSION_BINDING=false
MILESTONE_19_TASK_97_PRIVATE_CORE_EXPOSURE=false
MILESTONE_19_TASK_97_LEGAL_CERTIFICATION=false
MILESTONE_19_TASK_97_FAIL_CLOSED_ACTIVE=true
MILESTONE_19_TASK_97_NEXT_STAGE=MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_V1

## 9. Completion Criteria

Task 97 is complete when:

- Task 96 dependency exists;
- local usage module exists;
- local usage tests exist;
- this implementation document exists;
- artifact manifest exists;
- artifact index exists;
- targeted tests pass;
- task chain tests pass;
- full test suite passes;
- repository is committed and pushed cleanly.

## 10. Next Stage

MILESTONE_19_TASK_98_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_USAGE_IMPLEMENTATION_REVIEW_V1

Task 98 may review the controlled usage implementation.

Task 98 must not wire usage into solver runtime without a separate explicit authorization.
