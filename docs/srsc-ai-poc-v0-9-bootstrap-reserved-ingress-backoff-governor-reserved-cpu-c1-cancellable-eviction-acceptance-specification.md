# SRSC-AI PoC v0.9 Bootstrap-Reserved Ingress, Backoff Governor, Reserved CPU and C1 Cancellable Eviction Acceptance Specification

Organization: HERMETICUM B.C.E. S.r.l.  
Version: v0.9  
Status: POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED  
Maturity: DESIGNED / NOT_IMPLEMENTED / NOT_TESTED  
Boundary: legalCertification=false; technical proof receipt only.

## 1. Scope

This document is an acceptance specification only.

It does not claim runtime implementation.

It does not claim benchmark validation.

It does not claim fault-injection validation.

It does not claim production readiness.

It does not claim legal certification.

It replaces the older PoC v0.x source for the local SRSC programming chain as the active PoC v0.9 acceptance specification.

## 2. Objective

The PoC v0.9 addresses deterministic local runtime hardening for:

- bootstrap-reserved ingress;
- anonymous best-effort ingress isolation;
- registered ingress isolation;
- bounded backoff governor;
- reserved CPU/hash budget;
- C1 volatile context cancellation;
- health/status reserve;
- fail-closed rejection records.

A fully anonymous channel cannot reliably distinguish legitimate traffic from flood traffic. Therefore, protected initial capacity requires a control-plane issued BootstrapPermit. Anonymous traffic remains best-effort.

## 3. Ingress Classes

Ingress classes:

- ANONYMOUS_BEST_EFFORT
- BOOTSTRAP_RESERVED
- REGISTERED

Rules:

1. Anonymous traffic cannot consume bootstrap-reserved slots.
2. Anonymous traffic cannot consume registered slots.
3. BootstrapPermit is single-use.
4. BootstrapPermit has bounded TTL.
5. BootstrapPermit is issued outside payload body by control plane/test runner.
6. Expired, reused or invalid BootstrapPermit is rejected before body read.
7. Body fixture cannot assign its own ingress class.
8. Per-class queues are fixed-size.
9. Overflow does not create dynamic unbounded structures.

Acceptance configuration:

- anonymousSlots: 8
- bootstrapReservedSlots: 2
- registeredSlots: 8
- maxQueuedPerSlot: 1
- bootstrapPermitTtlMs: 500
- bootstrapPermitSingleUse: true

## 4. BootstrapPermit Minimum Record

Required permit fields:

- permitIdHash
- issuedBy
- issuedAtMonotonicMs
- expiresAtMonotonicMs
- boundIngressClass
- boundScenarioId
- singleUse
- usedAtMonotonicMs
- reuseDecision

Permit TTL and backoff authorization MUST use monotonic runtime time.

Wall-clock ISO-8601 timestamps MAY appear in reports but MUST NOT drive retry or permit authorization.

## 5. Backoff Governor

Backoff states:

- READY
- BACKING_OFF
- RECOVERY_LOCKED

Rules:

1. Recovery retries are bounded.
2. Backoff grows exponentially until maxBackoffMs.
3. nextAttemptNotBefore is report-visible.
4. maxAutomaticRecoveryAttempts leads to RECOVERY_LOCKED.
5. RECOVERY_LOCKED blocks A1 automatic recovery.
6. Untrusted input cannot reset recovery counters.
7. Backoff history is bounded.

## 6. Reserved CPU/Hash Budget

CPU/hash budget is isolated per ingress class.

Required controls:

- anonymous maxHashOps: 5
- anonymous maxHashBytes: 8192
- bootstrap maxHashOps: 5
- bootstrap maxHashBytes: 8192
- registered maxHashOps: 20
- registered maxHashBytes: 65536
- windowMs: 1000
- headerParseMaxOps: constant-bounded
- preAdmissionHeaderBytes: 2048
- preAdmissionHeaderFields: 32
- onPreAdmissionExhaustion: SRSC-REJECTED:PRE_ADMISSION_PARSE_BUDGET_EXCEEDED
- onHashBudgetExhaustion: SRSC-REJECTED:DEDUP_CPU_BUDGET_EXCEEDED

Anonymous and bootstrap traffic MUST NOT consume registered CPU/hash reserve.

Raw request bodies MUST NOT be persisted in reports.

Only bounded metadata, class counters, hashed identifiers and structured rejection/cancellation states may be emitted.

## 7. C1 Volatile Arena and Cancellable Eviction

C1 context classes:

- HEALTH_STATUS
- DIAGNOSTIC_READ
- FIXTURE_RESEARCH

Rules:

1. HEALTH_STATUS has reserved capacity.
2. FIXTURE_RESEARCH is evictable.
3. C1 eviction uses cancellation token.
4. Cancelled C1 contexts emit structured NARROW result.
5. Cancelled C1 contexts MUST NOT emit partial unsupported conclusions.
6. Repeated cancellation of same context is idempotent.
7. Memory is released once.
8. If no evictable context exists, request is rejected fail-closed.

## 8. Acceptance Cases

POC-S-26 Anonymous flood: anonymous rejected; bootstrap/registered untouched.

POC-S-27 Reused/expired bootstrap permits: permit rejected before body read.

POC-S-28 Repeated recovery jitter: backoff then RECOVERY_LOCKED.

POC-S-29 Header flood parallel classes: registered CPU/hash reserve preserved.

POC-S-30 Volatile arena pressure: evictable C1 cancelled; health/status remains available.

POC-C1-11 C1 eviction cancellation: structured NARROW, memory released once.

POC-A1-33 A1 after RECOVERY_LOCKED: SRSC-BLOCKED; no automatic lease.

## 9. Required Tests

POC-T106 Bootstrap permit single-use and class-isolated ingress slots

POC-T107 Recovery watchdog exponential backoff and terminal lock

POC-T108 Reserved CPU/hash budgets across ingress classes

POC-T109 Volatile C1 cancellation, eviction and health reserve

POC-T110 No anonymous payload can reserve bootstrap or registered capacity

POC-T111 Concurrent reuse of same BootstrapPermit

POC-T112 C1 eviction cancellation is idempotent

POC-T113 Health reserve survives C1 eviction storm

POC-T64 through POC-T113 are not markable NOT_APPLICABLE.

## 10. Required Report Fields

The v0.9 report must include:

- ingress class configuration;
- ingress class counters;
- bootstrap permit lifecycle records;
- bounded backoff history;
- RECOVERY_LOCKED visibility;
- CPU/hash budget per class;
- C1 cancellation records;
- C1 eviction records;
- health/status availability under pressure;
- anonymous best-effort limitation notice;
- no raw request body persistence;
- no benchmark claim unless benchmark implementation exists;
- no production readiness claim;
- no legal certification claim.

## 11. Gate

POC_V0_9_READY if and only if:

- POC_v0_8 acceptance requirements PASS;
- POC-S-26 through POC-S-30 PASS;
- POC-C1-11 PASS;
- POC-A1-33 PASS;
- POC-T64 through POC-T113 PASS;
- anonymous input cannot consume bootstrap/registered slots;
- anonymous input cannot consume registered CPU/hash budget;
- recovery retries are bounded and terminally visible;
- C1 eviction never emits unsupported partial conclusions;
- benchmark and fault-injection evidence exists.

Otherwise:

POC_V0_9_NOT_READY:<reason>

## 12. Current State

POC_V0_9_SPECIFICATION_READY / IMPLEMENTATION_NOT_STARTED

DESIGNED / NOT_IMPLEMENTED / NOT_TESTED

POC_V0_9_RUNTIME_IMPLEMENTED=false

POC_V0_9_BENCHMARKED=false

POC_V0_9_FAULT_INJECTION_PERFORMED=false

POC_V0_9_PRODUCTION_READY=false

legalCertification=false

technical proof receipt only
