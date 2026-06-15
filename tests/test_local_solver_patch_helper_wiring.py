from hbce_arc_agi3.local_solver_patch_helper_wiring import (
    LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION,
    LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS,
    action_policy_validity_guard_adapter,
    goal_inference_terminal_state_adapter,
    planner_loop_recovery_adapter,
    run_local_solver_patch_helper_wiring_dry_run,
    transition_verifier_feedback_adapter,
    world_model_state_tracking_adapter,
)


def _records():
    return (
        {
            "fixture_id": "fx_a",
            "episode_id": "ep_a",
            "initial_signature": "A",
            "final_signature": "B",
            "goal_signature": "B",
            "goal_reached": True,
            "trace": [
                {"action": "RIGHT", "verifier_match": True},
                {"action": "VERIFY", "verifier_match": True},
            ],
        },
        {
            "fixture_id": "fx_b",
            "episode_id": "ep_b",
            "initial_signature": "C",
            "final_signature": "D",
            "goal_signature": "D",
            "goal_reached": True,
            "trace": [
                {"action": "UP", "verifier_match": True},
                {"action": "UP", "verifier_match": True},
                {"action": "UP", "verifier_match": False},
            ],
        },
    )


def _assert_adapter_output(rows, layer):
    assert len(rows) == 2
    assert all(item["adapter_target_layer"] == layer for item in rows)
    assert all(item["adapter_status"] == "DRY_RUN_PASS" for item in rows)
    assert all(item["wiring_dry_run"] is True for item in rows)
    assert all(item["diagnostic_only"] is True for item in rows)
    assert all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in rows)
    assert all(item["score_claim_allowed"] is False for item in rows)
    assert all(item["submission_artifact_allowed"] is False for item in rows)
    assert all(item["runtime_solver_modified"] is False for item in rows)
    assert all(item["ranker_runtime_modified"] is False for item in rows)


def test_world_model_adapter():
    _assert_adapter_output(world_model_state_tracking_adapter(_records()), "world_model")


def test_goal_inference_adapter():
    _assert_adapter_output(goal_inference_terminal_state_adapter(_records()), "goal_inference")


def test_planner_adapter():
    _assert_adapter_output(planner_loop_recovery_adapter(_records()), "planner")


def test_transition_verifier_adapter():
    _assert_adapter_output(transition_verifier_feedback_adapter(_records()), "verifier")


def test_action_policy_adapter():
    _assert_adapter_output(action_policy_validity_guard_adapter(_records()), "action_policy")


def test_local_wiring_dry_run_bundle_boundary_safe():
    bundle = run_local_solver_patch_helper_wiring_dry_run(_records())
    assert bundle["revision"] == LOCAL_SOLVER_PATCH_HELPER_WIRING_REVISION
    assert bundle["status"] == LOCAL_SOLVER_PATCH_HELPER_WIRING_STATUS
    assert bundle["adapter_count"] == 5
    assert bundle["record_count"] == 2
    assert bundle["dry_run_output_count"] == 10
    assert bundle["dry_run_pass_count"] == 10
    assert bundle["dry_run_failure_count"] == 0
    assert bundle["wiring_dry_run"] is True
    assert bundle["wiring_performed"] is False
    assert bundle["runtime_solver_modified"] is False
    assert bundle["ranker_runtime_modified"] is False
    assert bundle["external_solver_dependency"] is False
    assert bundle["diagnostic_only"] is True
    assert bundle["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert bundle["kaggle_submission_sent"] is False
    assert bundle["legal_certification"] is False
