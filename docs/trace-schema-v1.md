# ARC-AGI-3 Trace Schema v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Mode: PUBLIC_TRACE_SCHEMA_V1  
Boundary: offline, deterministic, JSON-serializable, public-safe benchmark evidence.

## Purpose

The trace schema defines the public audit path for the HBCE ARC-AGI-3 agent.

Its role is to record what the agent observed, how it modeled the task, what goal it pursued, what plan it proposed, what action it selected, how the decision was verified and how the result was scored.

The schema is not a private JOKER-C2 runtime trace. It is a public benchmark evidence structure.

## Trace flow

observation → model → goal → plan → action → verification → score

## Required top-level fields

- status
- schema_version
- trace_id
- task_id
- observation
- model
- goal
- plan
- action
- verification
- score
- steps
- metadata

## Deterministic trace id

The trace id is derived from a SHA-256 hash of the task id and canonical payload.

Example prefix:

ARC-TRACE-

This allows repeated runs over the same input to produce the same trace id, which is necessary for reproducible benchmark evidence.

## Public boundary

The trace schema must not contain:

- private HBCE/JOKER-C2 runtime code
- private IPR memory
- API keys
- proprietary full-text corpus content
- legal certification material
- operational weaponization material

## Acceptance criteria

Trace Schema v1 is PASS only if:

- tests pass
- traces are JSON-serializable
- trace ids are deterministic
- required fields are validated
- stage order is stable
- public-safe metadata is explicit

## Operational markers

ARC_AGI3_TRACE_SCHEMA_V1_READY=true  
ARC_AGI3_TRACE_SCHEMA_VERSION=HBCE_ARC_AGI3_TRACE_SCHEMA_v1  
ARC_AGI3_TRACE_FLOW=observation_model_goal_plan_action_verification_score  
ARC_AGI3_TRACE_ID_DETERMINISTIC=true  
ARC_AGI3_TRACE_JSON_SERIALIZABLE=true  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
legalCertification=false
