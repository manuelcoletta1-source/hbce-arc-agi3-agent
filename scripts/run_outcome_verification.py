from hbce_arc_agi3.outcome_verification import verify_and_validate_outcome


def main() -> None:
    payload = {
        "id": "outcome-verification-smoke",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    result = verify_and_validate_outcome(payload)
    verification = result["outcome_verification"]
    validation = result["validation"]

    print(result["status"])
    print(verification["status"])
    print(validation["status"])
    print(verification["verification_status"])
    print(verification["cell_accuracy"])
    print(verification["signature"])
    print(verification["metadata"])


if __name__ == "__main__":
    main()
