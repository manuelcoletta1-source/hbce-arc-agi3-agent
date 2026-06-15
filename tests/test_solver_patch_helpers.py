from hbce_arc_agi3.solver_patch_helpers import (
    M11_SOLVER_PATCH_HELPERS_REVISION,
    M11_SOLVER_PATCH_HELPERS_STATUS,
    build_action_policy_validity_guard_hints,
    build_goal_inference_terminal_state_hints,
    build_planner_loop_recovery_hints,
    build_solver_patch_helper_bundle,
    build_transition_verifier_feedback_hints,
    build_world_model_state_tracking_hints,
)


def _sample_records():
    return (
        {
            "fixture_id": "fx_001",
            "episode_id": "ep_001",
            "initial_signature": "A",
            "final_signature": "B",
            "goal_signature": "B",
            "goal_reached": True,
            "step_count": 3,
            "trace": [
                {"action": "RIGHT", "verifier_match": True},
                {"action": "RIGHT", "verifier_match": True},
                {"action": "VERIFY", "verifier_match": True},
            ],
        },
        {
            "fixture_id": "fx_002",
            "episode_id": "ep_002",
            "initial_signature": "C",
            "final_signature": "D",
            "goal_signature": "D",
            "goal_reached": True,
            "step_count": 4,
            "trace": [
                {"action": "UP", "verifier_match": True},
                {"action": "UP", "verifier_match": True},
                {"action": "UP", "verifier_match": True},
                {"action": "VERIFY", "verifier_match": False},
            ],
        },
    )


def test_world_model_state_tracking_hints():
    hints = build_world_model_state_tracking_hints(_sample_records())
    assert len(hints) == 2
    assert all(item["target_layer"] == "world_model" for item in hints)
    assert all(item["state_transition_observed"] is True for item in hints)
    assert all(item["diagnostic_only"] is True for item in hints)
    assert all(item["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE" for item in hints)
    assert all(item["score_claim_allowed"] is False for item in hints)


def test_goal_inference_terminal_state_hints():
    hints = build_goal_inference_terminal_state_hints(_sample_records())
    assert len(hints) == 2
    assert all(item["target_layer"] == "goal_inference" for item in hints)
    assert all(item["goal_signal_present"] is True for item in hints)
    assert all(item["confidence"] == 1.0 for item in hints)
    assert all(item["score_claim_allowed"] is False for item in hints)


def test_planner_loop_recovery_hints():
    hints = build_planner_loop_recovery_hints(_sample_records())
    assert len(hints) == 2
    assert all(item["target_layer"] == "planner" for item in hints)
    assert hints[0]["fallback_required"] is False
    assert hints[1]["fallback_required"] is True
    assert all(item["diagnostic_only"] is True for item in hints)


def test_transition_verifier_feedback_hints():
    hints = build_transition_verifier_feedback_hints(_sample_records())
    assert len(hints) == 2
    assert all(item["target_layer"] == "verifier" for item in hints)
    assert hints[0]["verifier_feedback_required"] is False
    assert hints[1]["verifier_feedback_required"] is True
    assert hints[1]["verifier_mismatch_count"] == 1


def test_action_policy_validity_guard_hints():
    hints = build_action_policy_validity_guard_hints(_sample_records())
    assert len(hints) == 2
    assert all(item["target_layer"] == "action_policy" for item in hints)
    assert all(item["action_policy_valid"] is True for item in hints)
    assert all(item["score_claim_allowed"] is False for item in hints)


def test_solver_patch_helper_bundle_is_boundary_safe():
    bundle = build_solver_patch_helper_bundle(_sample_records())
    assert bundle["revision"] == M11_SOLVER_PATCH_HELPERS_REVISION
    assert bundle["status"] == M11_SOLVER_PATCH_HELPERS_STATUS
    assert bundle["record_count"] == 2
    assert len(bundle["world_model_hints"]) == 2
    assert len(bundle["goal_inference_hints"]) == 2
    assert len(bundle["planner_hints"]) == 2
    assert len(bundle["transition_verifier_hints"]) == 2
    assert len(bundle["action_policy_hints"]) == 2
    assert bundle["diagnostic_only"] is True
    assert bundle["kaggle_score_semantics"] == "NOT_A_KAGGLE_SCORE"
    assert bundle["official_score_claim_allowed"] is False
    assert bundle["competitive_score_claim_allowed"] is False
    assert bundle["runtime_solver_modified"] is False
    assert bundle["ranker_runtime_modified"] is False
    assert bundle["external_solver_dependency"] is False
    assert bundle["kaggle_submission_sent"] is False
