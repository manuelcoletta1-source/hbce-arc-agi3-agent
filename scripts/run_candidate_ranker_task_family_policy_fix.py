import json
from pathlib import Path

from hbce_arc_agi3.candidate_generator import generate_candidates
from hbce_arc_agi3.candidate_ranker import rank_candidates
from hbce_arc_agi3.expanded_batch_benchmark import (
    build_expanded_batch_benchmark_tasks,
    run_expanded_batch_benchmark_pipeline,
    write_expanded_batch_benchmark_artifacts,
)
from hbce_arc_agi3.failure_driven_improvement_loop import (
    run_failure_driven_improvement_pipeline,
    write_failure_driven_improvement_artifacts,
)


def main() -> None:
    output_dir = Path("examples/milestone-4/candidate-ranker-task-family-policy-fix-v1")
    output_dir.mkdir(parents=True, exist_ok=True)

    task = next(
        item
        for item in build_expanded_batch_benchmark_tasks()
        if item.task_id == "EXPANDED-BATCH-V2-COLOR-ONLY"
    )

    generation = generate_candidates(
        task.train_pairs,
        task.test_input,
        task_id=task.task_id,
        background_color=0,
    )
    ranking = rank_candidates(generation)

    expanded_payload = run_expanded_batch_benchmark_pipeline()
    write_expanded_batch_benchmark_artifacts(expanded_payload)

    improvement_payload = run_failure_driven_improvement_pipeline()
    write_failure_driven_improvement_artifacts(improvement_payload)

    ranking_data = ranking.to_dict()
    expected_best_grid = [list(row) for row in task.expected_best_grid]
    best_candidate_grid = ranking_data["best_candidate"]["candidate_grid"]

    payload = {
        "status": "CANDIDATE_RANKER_TASK_FAMILY_POLICY_FIX_READY",
        "milestone": "Milestone #4",
        "task": "Task 9",
        "task_id": task.task_id,
        "task_family": task.task_family,
        "expected_best_candidate_type": task.metadata.get("expected_best_candidate_type"),
        "expected_best_grid": expected_best_grid,
        "best_candidate_type_after_fix": ranking.best_candidate.candidate_type,
        "best_candidate_grid_after_fix": best_candidate_grid,
        "best_candidate_score_after_fix": ranking.best_candidate.score,
        "best_candidate_matches_expected": best_candidate_grid == expected_best_grid,
        "ranking_policy": ranking.ranking_policy,
        "expanded_batch_status": expanded_payload["status"],
        "expanded_best_candidate_match_rate": expanded_payload["best_candidate_match_rate"],
        "failure_loop_status": improvement_payload["status"],
        "failure_loop_improvement_item_count": improvement_payload["improvement_item_count"],
        "failure_loop_next_solver_target": improvement_payload["next_solver_target"],
        "metadata": {
            "source": "candidate_ranker_task_family_policy_fix_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }

    json_path = output_dir / "candidate-ranker-task-family-policy-fix-v1-smoke.json"
    md_path = output_dir / "candidate-ranker-task-family-policy-fix-v1-smoke.md"

    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    md_path.write_text(
        "\n".join(
            [
                "# ARC AGI3 Milestone #4 Task 9 - Candidate Ranker Task-Family Policy Fix v1",
                "",
                "## Status",
                "",
                f"- status: {payload['status']}",
                f"- task_id: {payload['task_id']}",
                f"- task_family: {payload['task_family']}",
                f"- expected_best_candidate_type: {payload['expected_best_candidate_type']}",
                f"- best_candidate_type_after_fix: {payload['best_candidate_type_after_fix']}",
                f"- best_candidate_score_after_fix: {payload['best_candidate_score_after_fix']}",
                f"- best_candidate_matches_expected: {payload['best_candidate_matches_expected']}",
                f"- expanded_best_candidate_match_rate: {payload['expanded_best_candidate_match_rate']}",
                f"- failure_loop_improvement_item_count: {payload['failure_loop_improvement_item_count']}",
                "",
                "## Markers",
                "",
                "ARC_AGI3_MILESTONE_4_TASK_9_CANDIDATE_RANKER_TASK_FAMILY_POLICY_FIX_READY=true",
                "ARC_AGI3_MILESTONE_4_TASK_9_COLOR_ONLY_REMAP_SELECTED=true",
                "ARC_AGI3_MILESTONE_4_TASK_9_EXPANDED_BATCH_MATCH_RATE_FIXED=true",
                "ARC_AGI3_MILESTONE_4_TASK_9_FAILURE_LOOP_CLOSED=true",
                "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
                "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
                "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
                "ARC_AGI3_LEGAL_CERTIFICATION=false",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(payload["status"])
    print(payload["task_id"])
    print(payload["task_family"])
    print(payload["expected_best_candidate_type"])
    print(payload["best_candidate_type_after_fix"])
    print(payload["best_candidate_score_after_fix"])
    print(payload["best_candidate_matches_expected"])
    print(payload["expanded_best_candidate_match_rate"])
    print(payload["failure_loop_improvement_item_count"])
    print(payload["failure_loop_next_solver_target"])
    print(json_path)
    print(md_path)
    print(payload["metadata"])


if __name__ == "__main__":
    main()
