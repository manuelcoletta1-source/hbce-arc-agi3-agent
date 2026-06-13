# ARC-AGI-3 Milestone #4 — Solver Engine v1

Status date: 2026-06-13  
Repository: hbce-arc-agi3-agent  
Milestone: #4  
Mode: PUBLIC_RND_SOLVER_ENGINE_BRANCH  
Previous milestone: Milestone #3  
Previous milestone status: MILESTONE_3_CLOSED_PASS  
Previous milestone closure commit: 0ca0df9  
Previous milestone closure ID: MILESTONE-3-CLOSURE-B110830EA9E2  

## Purpose

Milestone #4 starts the transition from a verified public benchmark pipeline to an actual solver engine.

Milestone #3 proved that the repository can inspect dataset metadata, build sample registries, run local batches, aggregate outcomes, classify failures, generate reports, build a local submission candidate, pass a public readiness audit, produce a dry-run release package, and close a milestone without exposing private HBCE/JOKER-C2 core logic.

Milestone #4 now focuses on improving task-solving ability.

The goal is not to send a Kaggle submission immediately. The goal is to build a better deterministic local solver stack that can recognize grid objects, color transformations, spatial structure, candidate outputs, and ranking logic.

## Strategic position

Milestone #4 is the first solver-focused milestone after the public pipeline foundation.

The repository remains:

- public-safe
- deterministic
- local-only
- dry-run-only
- free from external API dependency
- free from credentials
- free from private HBCE/JOKER-C2 core exposure

The solver engine must remain compatible with the existing benchmark chain created in Milestone #1, Milestone #2, and Milestone #3.

## Solver direction

Milestone #4 introduces a modular solver engine built around:

1. strategy interface
2. grid object extraction
3. color transform detection
4. shape and symmetry detection
5. candidate output generation
6. candidate ranking
7. expanded batch evaluation
8. score regression reporting
9. local submission format candidate
10. milestone closure

The solver must be explainable enough for local audit. It should avoid opaque external calls. It should not depend on hosted models. It should not rely on hidden private code.

## Planned task chain

| Task | Module | Goal |
|---:|---|---|
| 1 | Strategy Interface v2 | Define a clean strategy protocol for multiple solver strategies |
| 2 | Grid Object Extractor v1 | Extract connected objects, colors, bounding boxes and basic object metadata |
| 3 | Color Transform Detector v1 | Detect palette shifts, color substitutions and stable color mappings |
| 4 | Shape / Symmetry Detector v1 | Detect rotations, reflections, translations, repetition and simple symmetry |
| 5 | Candidate Generator v1 | Generate candidate outputs from strategy modules |
| 6 | Candidate Ranker v1 | Rank candidates using deterministic scoring heuristics |
| 7 | Expanded Batch Benchmark v2 | Run larger batch evaluation across available sample tasks |
| 8 | Score Regression Report v1 | Compare Milestone #4 score against previous baseline |
| 9 | Local Submission Format Candidate v1 | Produce local-only candidate package closer to submission format |
| 10 | Milestone #4 Closure v1 | Close Milestone #4 with report, artifacts, tests and parent registry target |

## Expected architecture

Milestone #4 should introduce or evolve these modules:

- `src/hbce_arc_agi3/strategy_interface_v2.py`
- `src/hbce_arc_agi3/grid_object_extractor.py`
- `src/hbce_arc_agi3/color_transform_detector.py`
- `src/hbce_arc_agi3/shape_symmetry_detector.py`
- `src/hbce_arc_agi3/candidate_generator.py`
- `src/hbce_arc_agi3/candidate_ranker.py`
- `src/hbce_arc_agi3/expanded_batch_benchmark.py`
- `src/hbce_arc_agi3/score_regression_report.py`
- `src/hbce_arc_agi3/local_submission_format_candidate.py`
- `src/hbce_arc_agi3/milestone_4_closure_report.py`

The implementation may adjust exact filenames if the existing public repository structure requires it, but each task must remain traceable.

## Baseline inherited from Milestone #3

Milestone #3 closure state:

- `MILESTONE_3_CLOSED_PASS`
- closure commit: `0ca0df9`
- closure ID: `MILESTONE-3-CLOSURE-B110830EA9E2`
- dry-run release package ID: `MILESTONE-3-DRY-RUN-RELEASE-PACKAGE-11E2F3C9D396`
- public readiness audit ID: `PUBLIC-READINESS-AUDIT-C37C53F41756`
- local submission candidate ID: `LOCAL-SUBMISSION-CANDIDATE-E226DE7C08C2`
- final tests passed: `208`
- `kaggle_submission_sent=false`
- `external_api_dependency=false`
- `private_core_exposure=false`

## Acceptance criteria

Milestone #4 is considered complete only if:

- all planned tasks are completed or explicitly superseded with documented reason
- solver modules are deterministic
- tests pass
- no external API dependency is introduced
- no API keys are introduced
- no Kaggle submission is sent automatically
- no private HBCE/JOKER-C2 core code is exposed
- local benchmark score is measured
- regression report compares against Milestone #3 baseline
- local submission format candidate is generated locally
- closure report is generated
- parent repo registry can be updated after closure

## Safety boundary

Milestone #4 must not:

- send a Kaggle submission
- call external model APIs
- require OpenAI, Anthropic, Google, Kaggle API keys or any hosted inference key
- execute untrusted dataset code
- expose private JOKER-C2 runtime internals
- expose private IPR memory
- use private HBCE operational code
- claim legal certification

## Operational markers

ARC_AGI3_MILESTONE_4_SOLVER_ENGINE_PLAN_V1_READY=true  
ARC_AGI3_MILESTONE_4_STATUS=OPEN_READY  
ARC_AGI3_MILESTONE_4_PREVIOUS_MILESTONE=MILESTONE_3_CLOSED_PASS  
ARC_AGI3_MILESTONE_4_PREVIOUS_CLOSURE_COMMIT=0ca0df9  
ARC_AGI3_MILESTONE_4_PREVIOUS_CLOSURE_ID=MILESTONE-3-CLOSURE-B110830EA9E2  
ARC_AGI3_MILESTONE_4_SOLVER_ENGINE_TARGET=true  
ARC_AGI3_MILESTONE_4_TASKS_PLANNED=10  
ARC_AGI3_MILESTONE_4_TASK_1=STRATEGY_INTERFACE_V2  
ARC_AGI3_MILESTONE_4_TASK_2=GRID_OBJECT_EXTRACTOR_V1  
ARC_AGI3_MILESTONE_4_TASK_3=COLOR_TRANSFORM_DETECTOR_V1  
ARC_AGI3_MILESTONE_4_TASK_4=SHAPE_SYMMETRY_DETECTOR_V1  
ARC_AGI3_MILESTONE_4_TASK_5=CANDIDATE_GENERATOR_V1  
ARC_AGI3_MILESTONE_4_TASK_6=CANDIDATE_RANKER_V1  
ARC_AGI3_MILESTONE_4_TASK_7=EXPANDED_BATCH_BENCHMARK_V2  
ARC_AGI3_MILESTONE_4_TASK_8=SCORE_REGRESSION_REPORT_V1  
ARC_AGI3_MILESTONE_4_TASK_9=LOCAL_SUBMISSION_FORMAT_CANDIDATE_V1  
ARC_AGI3_MILESTONE_4_TASK_10=MILESTONE_4_CLOSURE_V1  
ARC_AGI3_KAGGLE_SUBMISSION_SENT=false  
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false  
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false  
ARC_AGI3_LEGAL_CERTIFICATION=false  
legalCertification=false
