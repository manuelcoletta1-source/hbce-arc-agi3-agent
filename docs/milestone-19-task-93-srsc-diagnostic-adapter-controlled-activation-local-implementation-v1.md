# Milestone #19 Task 93 - SRSC Diagnostic Adapter Controlled Activation Local Implementation v1

Project: HBCE ARC-AGI-3 Agent
Organization: HERMETICUM B.C.E. S.r.l.
Task ID: MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_V1
Status: CONTROLLED_DIAGNOSTIC_ACTIVATION_LOCAL_IMPLEMENTATION_READY
Mode: LOCAL_DIAGNOSTIC_ONLY_ACTIVATION_NO_RUNTIME_WIRING
Boundary: legalCertification=false; technical proof receipt only.

## 1. Purpose

Task 93 implements the local controlled diagnostic-only activation wrapper authorized by Task 92.

Implemented module:

- src/hbce_arc_agi3/srsc_diagnostic_adapter_activation.py

Implemented test:

- tests/test_srsc_diagnostic_adapter_activation.py

The activation wrapper exposes the SRSC Diagnostic Adapter only through approved diagnostic call-sites.

The activation wrapper does not wire the adapter into solver runtime.

## 2. Dependency

Task 93 depends on:

MILESTONE_19_TASK_92_SRSC_DIAGNOSTIC_ADAPTER_ACTIVATION_IMPLEMENTATION_AUTHORIZATION_REVIEW_V1

Task 92 authorized controlled diagnostic activation implementation only.

## 3. Implemented Activation Types

The implementation defines:

- DiagnosticAdapterActivationInput
- DiagnosticAdapterActivationResult
- DiagnosticAdapterActivationBlockedCall
- activate_diagnostic_adapter_for_diagnostic_path
- activate_diagnostic_adapter_batch_for_diagnostic_path

## 4. Activation Behavior

The activation wrapper may:

- accept explicit local diagnostic payloads;
- validate call-site names;
- allow approved diagnostic call-sites;
- block forbidden call-sites;
- call the local SRSC Diagnostic Adapter;
- return DiagnosticAdapterResult;
- return blocked activation calls;
- return deterministic public JSON;
- preserve fail-closed markers.

The activation wrapper must not:

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

## 5. Allowed Diagnostic Call-Sites

Allowed diagnostic call-sites:

- local diagnostic scripts;
- public-safe audit artifact builders;
- SRSC review artifact generators;
- milestone closure evidence builders;
- cross-trace diagnostic planners.

## 6. Forbidden Call-Sites

Forbidden call-sites:

- solver runtime loop;
- agent planner;
- world model;
- observer runtime path;
- candidate generator;
- candidate ranker;
- verifier;
- benchmark executor;
- Kaggle submission package builder;
- real evaluation runner;
- private core modules;
- network or API clients.

## 7. Controlled Boundary

controlled_activation_implemented=true
diagnostic_only_activation=true
adapter_activated_for_diagnostic_path_only=true
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

MILESTONE_19_TASK_93_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_LOCAL_IMPLEMENTATION_READY=true
MILESTONE_19_TASK_93_STATUS=CONTROLLED_DIAGNOSTIC_ACTIVATION_LOCAL_IMPLEMENTATION_READY
MILESTONE_19_TASK_93_MODE=LOCAL_DIAGNOSTIC_ONLY_ACTIVATION_NO_RUNTIME_WIRING
MILESTONE_19_TASK_93_CONTROLLED_ACTIVATION_IMPLEMENTED=true
MILESTONE_19_TASK_93_DIAGNOSTIC_ONLY_ACTIVATION=true
MILESTONE_19_TASK_93_ADAPTER_ACTIVATED_FOR_DIAGNOSTIC_PATH_ONLY=true
MILESTONE_19_TASK_93_RUNTIME_SOLVER_MODIFIED=false
MILESTONE_19_TASK_93_RUNTIME_WIRING_ALLOWED=false
MILESTONE_19_TASK_93_SOLVER_RUNTIME_BINDING=false
MILESTONE_19_TASK_93_CANDIDATE_GENERATOR_MODIFIED=false
MILESTONE_19_TASK_93_CANDIDATE_GENERATOR_BINDING=false
MILESTONE_19_TASK_93_RANKER_MODIFIED=false
MILESTONE_19_TASK_93_RANKER_BINDING=false
MILESTONE_19_TASK_93_VERIFIER_MODIFIED=false
MILESTONE_19_TASK_93_VERIFIER_BINDING=false
MILESTONE_19_TASK_93_BENCHMARK_SCORE_CLAIMED=false
MILESTONE_19_TASK_93_BENCHMARK_BINDING=false
MILESTONE_19_TASK_93_REAL_EVALUATION_PERFORMED=false
MILESTONE_19_TASK_93_KAGGLE_SUBMISSION_SENT=false
MILESTONE_19_TASK_93_KAGGLE_SUBMISSION_BINDING=false
MILESTONE_19_TASK_93_PRIVATE_CORE_EXPOSURE=false
MILESTONE_19_TASK_93_LEGAL_CERTIFICATION=false
MILESTONE_19_TASK_93_FAIL_CLOSED_ACTIVE=true
MILESTONE_19_TASK_93_NEXT_STAGE=MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_V1

## 9. Completion Criteria

Task 93 is complete when:

- Task 92 dependency exists;
- local activation module exists;
- local activation tests exist;
- this implementation document exists;
- artifact manifest exists;
- artifact index exists;
- targeted tests pass;
- task chain tests pass;
- full test suite passes;
- repository is committed and pushed cleanly.

## 10. Next Stage

MILESTONE_19_TASK_94_SRSC_DIAGNOSTIC_ADAPTER_CONTROLLED_ACTIVATION_IMPLEMENTATION_REVIEW_V1

Task 94 may review the controlled activation implementation.

Task 94 must not wire activation into solver runtime without a separate explicit authorization.
