# Milestone #12 Task 3 - Information Gain Explorer Policy v1

Task 3 creates the first deterministic information-gain explorer policy for the Milestone #12 competitive solver runtime branch.

The policy ranks candidate actions by expected information gain and selects one useful exploratory action per benchmark case.

## Strategy

EXECUTABLE_WORLD_MODEL_EXPLORE_VERIFY_PLAN

## Competitive objective

FIRST_PLACE_COMPETITIVE_SOLVER

## Explorer targets

- case_count
- selected_action_count
- mean_expected_information_gain
- median_expected_information_gain
- minimum_expected_information_gain
- max_expected_information_gain
- wait_action_selected_count
- invalid_action_selected_count
- first_optimal_action_selected_count
- exploration_confidence_mean

## Boundary

- local_only=true
- deterministic=true
- public_safe=true
- explorer_policy_only=true
- public_overfit_allowed=false
- public_overfit_guard_required=true
- external_api_dependency=false
- internet_during_eval=false
- real_submission_allowed=false
- manual_upload_allowed=false
- kaggle_submission_sent=false
- kaggle_authentication_performed=false
- private_core_exposure=false
- legal_certification=false

## Next stage

MILESTONE_12_TASK_4_EXECUTABLE_WORLD_MODEL_V1
