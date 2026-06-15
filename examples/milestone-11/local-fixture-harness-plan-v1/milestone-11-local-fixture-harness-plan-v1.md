# ARC AGI3 Milestone #11 Task 4 - Local Fixture Harness Plan v1

- status: MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY
- task_4_id: MILESTONE-11-LOCAL-FIXTURE-HARNESS-PLAN-7A69A3427DCA
- signature: 7A69A3427DCAA7E7
- baseline_commit: b609069 Add ARC AGI3 public game failure taxonomy
- task_mode: MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY
- task_scope: LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_PLAN_NO_SCORE_NO_SUBMISSION
- task_verdict: LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION
- next_stage: MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1
- task_4_ready: True
- primary_condition: NO_LOCAL_PUBLIC_FIXTURES
- primary_classification: MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE
- solver_failure_detected: False
- solver_not_measured: True
- harness_component_count: 8
- fixture_class_count: 6
- measurement_axis_count: 5
- boundary_rule_count: 5
- diagnostic_only: True
- fixture_generation_performed: False
- fixture_generation_deferred_to: MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1
- official_score_claim_allowed: False
- real_public_score_claimed: False
- private_score_claimed: False
- real_benchmark_score: None
- real_submission_allowed: False
- kaggle_submission_sent: False
- fail_closed_active: True

## Harness components

- local_fixture_loader_v1 / layer=fixture_io / priority=P0 / purpose=Load local diagnostic fixtures from deterministic JSON files.
- episode_runner_v1 / layer=runtime / priority=P0 / purpose=Execute deterministic local episodes without external services.
- observation_trace_recorder_v1 / layer=trace / priority=P0 / purpose=Record observations, actions, predicted transitions, and actual transitions.
- world_model_probe_v1 / layer=world_model / priority=P0 / purpose=Measure whether the solver models objects, state, transitions, and rules.
- goal_inference_probe_v1 / layer=goal_inference / priority=P0 / purpose=Measure whether the solver infers candidate goals from state changes.
- planner_probe_v1 / layer=planner / priority=P0 / purpose=Measure planning quality, loop avoidance, and action sequence selection.
- transition_verifier_probe_v1 / layer=verifier / priority=P0 / purpose=Compare predicted and observed transitions after every action.
- score_boundary_guard_v1 / layer=boundary / priority=P0 / purpose=Prevent diagnostic fixture results from being treated as Kaggle scores.

## Fixture classes

- object_persistence_fixture_v1 / target=world_model / purpose=Test whether objects persist across observations and transformations.
- color_rule_fixture_v1 / target=rule_inference / purpose=Test simple color remap and rule tracking.
- movement_transition_fixture_v1 / target=transition_model / purpose=Test deterministic movement, collision, and state transition predictions.
- goal_inference_fixture_v1 / target=goal_inference / purpose=Test inferred objective from reward-like terminal conditions.
- planner_loop_fixture_v1 / target=planner / purpose=Test loop detection, fallback exploration, and progress tracking.
- verifier_mismatch_fixture_v1 / target=verifier / purpose=Test correction when predicted transition differs from actual transition.

## Measurement axes

- world_model_accuracy_v1 / scope=diagnostic_only / Measures internal state and transition prediction quality.
- goal_inference_quality_v1 / scope=diagnostic_only / Measures whether the solver infers goals from local feedback.
- planner_progress_v1 / scope=diagnostic_only / Measures progress, loop avoidance, and plan stability.
- transition_verification_v1 / scope=diagnostic_only / Measures predicted versus observed transition agreement.
- action_policy_safety_v1 / scope=diagnostic_only / Measures whether action choice avoids repeated non-progress actions.

## Boundary rules

- no_kaggle_score_claim_from_local_fixture_v1 / severity=BLOCKING / Local fixture harness results must never be reported as Kaggle public or private score.
- no_submission_json_from_harness_v1 / severity=BLOCKING / The harness plan must not create submission.json.
- no_upload_package_from_harness_v1 / severity=BLOCKING / The harness plan must not create an upload package.
- no_external_api_dependency_v1 / severity=BLOCKING / Harness execution must remain local-only and must not call external APIs.
- diagnostic_result_label_required_v1 / severity=BLOCKING / Every harness result must be labelled diagnostic-only.

## Validation results

- m11_task4_source_task3_ready_v1 / area=source_binding / operation=verify_task_3_failure_taxonomy_source / passed=True
- m11_task4_measurement_constraint_loaded_v1 / area=constraint / operation=verify_measurement_constraint_not_solver_failure / passed=True
- m11_task4_harness_components_ready_v1 / area=harness_components / operation=verify_harness_components / passed=True
- m11_task4_fixture_classes_ready_v1 / area=fixture_plan / operation=verify_fixture_classes / passed=True
- m11_task4_measurement_axes_ready_v1 / area=measurement / operation=verify_measurement_axes / passed=True
- m11_task4_boundary_rules_ready_v1 / area=boundary / operation=verify_boundary_rules / passed=True
- m11_task4_diagnostic_only_enforced_v1 / area=score_boundary / operation=verify_diagnostic_only_enforced / passed=True
- m11_task4_real_submission_blocked_v1 / area=submission_boundary / operation=verify_real_submission_blocked / passed=True
- m11_task4_next_stage_valid_v1 / area=next_stage / operation=verify_next_stage / passed=True
- m11_task4_metadata_safe_v1 / area=metadata / operation=verify_public_safe_metadata / passed=True

## Decision

Task 4 creates a local diagnostic fixture harness plan. It does not generate fixtures yet, does not claim score, and does not authorize real submission.

## Markers

ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_READY=true
ARC_AGI3_MILESTONE_11_TASK_4_LOCAL_FIXTURE_HARNESS_PLAN_V1_VALID=true
ARC_AGI3_MILESTONE_11_TASK_4_READY=true
ARC_AGI3_MILESTONE_11_TASK_4_MODE=MILESTONE_11_LOCAL_FIXTURE_HARNESS_PLAN_V1_LOCAL_ONLY
ARC_AGI3_MILESTONE_11_TASK_4_VERDICT=LOCAL_FIXTURE_HARNESS_PLAN_READY_FOR_DIAGNOSTIC_FIXTURE_GENERATION
ARC_AGI3_MILESTONE_11_TASK_4_BASELINE_COMMIT=b609069
ARC_AGI3_MILESTONE_11_TASK_4_NEXT_STAGE=MILESTONE_11_TASK_5_LOCAL_DIAGNOSTIC_FIXTURE_HARNESS_V1
ARC_AGI3_MILESTONE_11_PRIMARY_CLASSIFICATION=MEASUREMENT_CONSTRAINT_NOT_SOLVER_FAILURE
ARC_AGI3_MILESTONE_11_SOLVER_FAILURE_DETECTED=false
ARC_AGI3_MILESTONE_11_SOLVER_NOT_MEASURED=true
ARC_AGI3_MILESTONE_11_HARNESS_COMPONENT_COUNT=8
ARC_AGI3_MILESTONE_11_FIXTURE_CLASS_COUNT=6
ARC_AGI3_MILESTONE_11_MEASUREMENT_AXIS_COUNT=5
ARC_AGI3_MILESTONE_11_BOUNDARY_RULE_COUNT=5
ARC_AGI3_MILESTONE_11_DIAGNOSTIC_ONLY=true
ARC_AGI3_MILESTONE_11_FIXTURE_GENERATION_PERFORMED=false
ARC_AGI3_MILESTONE_11_OFFICIAL_SCORE_CLAIM_ALLOWED=false
ARC_AGI3_MILESTONE_11_SYNTHETIC_FIXTURE_SCORE_CLAIM_ALLOWED=false
ARC_AGI3_MILESTONE_11_REAL_PUBLIC_SCORE_CLAIMED=false
ARC_AGI3_MILESTONE_11_PRIVATE_SCORE_CLAIMED=false
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_CANDIDATE_CREATED=false
ARC_AGI3_MILESTONE_11_SUBMISSION_JSON_CREATED=false
ARC_AGI3_MILESTONE_11_UPLOAD_PACKAGE_CREATED=false
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_DECISION=NOT_AUTHORIZED
ARC_AGI3_MILESTONE_11_REAL_SUBMISSION_ALLOWED=false
ARC_AGI3_MILESTONE_11_KAGGLE_AUTHENTICATION_ALLOWED=false
ARC_AGI3_MILESTONE_11_KAGGLE_SUBMISSION_SENT=false
ARC_AGI3_MILESTONE_11_FAIL_CLOSED_REQUIRED=true
ARC_AGI3_MILESTONE_11_FAIL_CLOSED_ACTIVE=true
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
ARC_AGI3_LEGAL_CERTIFICATION=false
