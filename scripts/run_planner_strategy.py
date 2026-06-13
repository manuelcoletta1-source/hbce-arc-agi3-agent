from hbce_arc_agi3.planner_strategy import build_strategy_from_grid_payload


def main() -> None:
    payload = {
        "id": "planner-strategy-smoke",
        "grid": [
            [1, 0, 2, 2],
            [1, 0, 0, 2],
            [0, 3, 3, 0],
        ],
        "goal": "solve",
    }

    result = build_strategy_from_grid_payload(payload)
    strategy = result["planner_strategy"]
    validation = result["validation"]

    print(result["status"])
    print(strategy["status"])
    print(validation["status"])
    print(strategy["task_id"])
    print(strategy["selected_rule_type"])
    print(strategy["selected_action"])
    print(strategy["confidence"])
    print(strategy["metadata"])


if __name__ == "__main__":
    main()
