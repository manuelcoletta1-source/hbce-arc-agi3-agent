# HBCE ARC-AGI-3 Milestone #1 Plan

Status date: 2026-06-13
Target milestone: 2026-06-30
Repository: hbce-arc-agi3-agent
Mode: PUBLIC_RND_COMPETITION_BRANCH
Boundary: offline, reproducible, no external API dependency, no private HBCE/JOKER-C2 core exposure

## Objective

Milestone #1 establishes the first public technical foundation for the HBCE ARC-AGI-3 agent.

The objective is not leaderboard performance yet.
The objective is to create a reliable, offline, trace-first baseline capable of:

- loading or inspecting ARC-AGI-3 public game/task structures
- producing normalized observations
- constructing a minimal world model
- planning candidate actions
- verifying decisions
- generating auditable traces
- packaging a reproducible submission skeleton

## Current baseline

Current public baseline status:

- pytest: 5 passed
- scripts/run_local.py: ARC_AGI3_SMOKE_AGENT_READY
- scripts/run_public_games.py: PUBLIC_GAMES_SMOKE_READY
- scripts/package_submission.py: PACKAGE_SUBMISSION_SMOKE_READY
- branch: main
- public repository: https://github.com/manuelcoletta1-source/hbce-arc-agi3-agent

## Milestone #1 technical tasks

### 1. Dataset and game structure inspection

Goal: inspect the Kaggle ARC-AGI-3 raw archive and identify usable public game/task files.

Deliverables:
- docs/dataset-inspection.md
- scripts/inspect_dataset.py
- test coverage for archive presence and safe inspection

### 2. Task adapter layer

Goal: create a stable adapter that converts raw game/task input into the internal HBCE agent state format.

Deliverables:
- src/hbce_arc_agi3/task_adapter.py
- tests/test_task_adapter.py

### 3. Trace schema v1

Goal: define a reproducible trace object for observation, model, goal, plan, action, verification and score.

Deliverables:
- docs/trace-schema-v1.md
- src/hbce_arc_agi3/trace_schema.py
- tests/test_trace_schema.py

### 4. Observer and world-model upgrade

Goal: move beyond smoke baseline by extracting structured entities, grid dimensions, symbolic features and uncertainty markers.

Deliverables:
- updated src/hbce_arc_agi3/observer.py
- updated src/hbce_arc_agi3/world_model.py
- tests/test_observer_world_model.py

### 5. Planner baseline v1

Goal: create a deterministic baseline planner that can propose candidate actions from the world model.

Deliverables:
- updated src/hbce_arc_agi3/planner.py
- tests/test_planner.py

### 6. Verification and scoring v1

Goal: define initial verification rules and scoring signals for public benchmark evidence.

Deliverables:
- updated src/hbce_arc_agi3/scoring.py
- tests/test_scoring.py

### 7. Submission package skeleton

Goal: create a reproducible packaging path without exposing private systems or external dependencies.

Deliverables:
- submission/README.md
- scripts/package_submission.py
- tests/test_package_submission.py

### 8. Milestone #1 report

Goal: document what works, what fails and what must improve for Milestone #2.

Deliverables:
- docs/milestone-1-report.md

## Public benchmark evidence

Milestone #1 must produce benchmark-grade evidence, not just code.

Required evidence:
- passing tests
- deterministic script output
- trace examples
- dataset inspection report
- known limitations
- next-step plan

## Non-goals

Milestone #1 does not attempt to:
- win the competition
- claim AGI
- use private JOKER-C2 runtime code
- call external LLM APIs
- expose private IPR memory
- publish private corpus content
- create operational engineering systems

## Strategic alignment

This milestone supports the wider HBCE / JOKER-C2 / MATRIX Kaggle strategy:

- ARC-AGI-3 = public agentic cognition benchmark
- JOKER-C2 / MATRIX V = trace-first runtime inspiration
- Benchmark Task Author Target = evidence-building path
- SSBSP-LUNA and Orbit Wars = downstream strategic scenario layers, not part of the ARC-AGI-3 physical implementation

## Acceptance criteria

Milestone #1 is PASS only if:

- pytest passes
- local runner passes
- dataset inspection script runs safely
- task adapter tests pass
- trace schema tests pass
- package submission smoke check passes
- no private key, private runtime, private memory or full private corpus is exposed

## Operational markers

HBCE_ARC_AGI3_MILESTONE_1_PLAN_READY=true
ARC_AGI3_MILESTONE_1_TARGET=2026-06-30
ARC_AGI3_PUBLIC_RND_BRANCH=true
ARC_AGI3_TRACE_FIRST_BASELINE=true
ARC_AGI3_OFFLINE_REPRODUCIBLE_AGENT=true
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_MILESTONE_1_ACCEPTANCE_TESTS_DEFINED=true
legalCertification=false
