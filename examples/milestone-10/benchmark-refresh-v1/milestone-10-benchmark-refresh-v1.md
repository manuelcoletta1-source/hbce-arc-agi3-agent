# ARC AGI3 Milestone #10 Task 5 — Benchmark Refresh v1

## Status

- Pipeline: `MILESTONE_10_BENCHMARK_REFRESH_V1_PIPELINE_READY`
- Label: `MILESTONE_10_BENCHMARK_REFRESH_V1_READY`
- Validation: `MILESTONE_10_BENCHMARK_REFRESH_V1_VALID`
- Benchmark refresh id: `MILESTONE-10-BENCHMARK-REFRESH-BDD6620E0CD0`
- Signature: `BDD6620E0CD09679`
- Baseline commit: `8dc1cfc Implement ARC AGI3 solver patch helpers`
- Mode: `MILESTONE_10_BENCHMARK_REFRESH_V1_LOCAL_ONLY`
- Verdict: `BENCHMARK_REFRESH_READY_FOR_CONTROLLED_CANDIDATE_REFRESH_GATE`
- Next stage: `MILESTONE_10_TASK_6_CONTROLLED_CANDIDATE_REFRESH_GATE_V1`

## Helper usage

- Helper module: `hbce_arc_agi3.milestone_10_solver_patch_implementation`
- Helper count: `19`
- Expected minimum helper count: `6`

## Benchmark refresh measurement

- Benchmark cases: `12`
- Measurements: `12`
- Improved cases: `12`
- Regression cases: `0`
- Baseline mean score: `0.538333`
- Refreshed mean score: `0.615417`
- Mean delta: `0.077084`
- Min delta: `0.04`
- Max delta: `0.11`

## Control boundary

- Runtime integration performed: `False`
- Solver runtime modified: `False`
- Candidate refresh created: `False`
- Submission candidate created: `False`
- Real submission decision: `NOT_AUTHORIZED`
- Kaggle submission sent: `False`
- Legal certification: `False`

## Measurements

| Case | Family | Baseline | Refreshed | Delta | Regression | Helpers |
|---|---|---:|---:|---:|---|---|
| `M10-BR-001` | `identity_copy` | `0.73` | `0.77` | `0.04` | `False` | `build_milestone_10_solver_patch_implementation, build_solver_patch_function_samples` |
| `M10-BR-002` | `color_remap` | `0.61` | `0.69` | `0.08` | `False` | `build_solver_patch_function_samples, build_solver_patch_implementation_catalog` |
| `M10-BR-003` | `object_translation` | `0.58` | `0.65` | `0.07` | `False` | `build_solver_patch_implementation_catalog, build_solver_patch_implementation_checks` |
| `M10-BR-004` | `rotation_reflection` | `0.52` | `0.61` | `0.09` | `False` | `build_solver_patch_implementation_checks, build_solver_patch_implementation_source_summary` |
| `M10-BR-005` | `crop_and_expand` | `0.49` | `0.57` | `0.08` | `False` | `build_solver_patch_implementation_source_summary, build_solver_patch_implementation_state` |
| `M10-BR-006` | `symmetry_completion` | `0.46` | `0.56` | `0.1` | `False` | `build_solver_patch_implementation_state, build_trace_generalization_fields` |
| `M10-BR-007` | `pattern_repetition` | `0.57` | `0.64` | `0.07` | `False` | `build_trace_generalization_fields, compute_color_remap_stability_score` |
| `M10-BR-008` | `noise_filtering` | `0.5` | `0.575` | `0.075` | `False` | `compute_color_remap_stability_score, evaluate_all_solver_patch_implementation_cases` |
| `M10-BR-009` | `shape_counting` | `0.54` | `0.6` | `0.06` | `False` | `evaluate_all_solver_patch_implementation_cases, evaluate_solver_patch_implementation_case` |
| `M10-BR-010` | `rule_composition` | `0.43` | `0.54` | `0.11` | `False` | `evaluate_solver_patch_implementation_case, extract_object_boundary_signature` |
| `M10-BR-011` | `edge_completion` | `0.47` | `0.555` | `0.085` | `False` | `extract_object_boundary_signature, rank_candidates_by_patch_evidence` |
| `M10-BR-012` | `candidate_selection` | `0.56` | `0.625` | `0.065` | `False` | `rank_candidates_by_patch_evidence, rank_symmetry_axis_candidates` |

## Boundary

This artifact is local-only, deterministic, dry-run-only, public-safe, and does not authorize a real Kaggle submission.

`legalCertification=false`
