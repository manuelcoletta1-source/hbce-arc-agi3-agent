from hbce_arc_agi3.rule_hypothesis import generate_rule_hypotheses, validate_rule_hypothesis_set


def main() -> None:
    payload = {
        "id": "rule-hypothesis-smoke",
        "grid": [
            [1, 0, 2, 2],
            [1, 0, 0, 2],
            [0, 3, 3, 0],
        ],
        "goal": "solve",
    }

    hypotheses = generate_rule_hypotheses(payload)
    validation = validate_rule_hypothesis_set(hypotheses)

    print(hypotheses.status)
    print(validation["status"])
    print(hypotheses.hypothesis_count)
    print(hypotheses.task_id)
    print(hypotheses.metadata["signature"])
    print(hypotheses.metadata)


if __name__ == "__main__":
    main()
