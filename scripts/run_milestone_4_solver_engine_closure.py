from hbce_arc_agi3.milestone_4_solver_engine_closure import (
    run_milestone_4_solver_engine_closure_pipeline,
)


def main() -> None:
    payload = run_milestone_4_solver_engine_closure_pipeline()
    closure = payload["closure"]
    solver = closure["solver_engine_result"]

    print(payload["status"])
    print(payload["closure_status"])
    print(payload["validation_status"])
    print(payload["closure_id"])
    print(payload["signature"])
    print(payload["closed_task_count"])
    print(payload["final_test_count_before_closure"])
    print(payload["ready_for_next_phase"])
    print(payload["kaggle_submission_sent"])
    print(solver["expanded_best_candidate_match_rate"])
    print(solver["failure_loop_improvement_item_count"])
    print(solver["failure_loop_next_solver_target"])
    print(payload["artifacts"]["json_path"])
    print(payload["artifacts"]["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
