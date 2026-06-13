from hbce_arc_agi3.score_calibration import calibrate_and_validate_score


def main() -> None:
    payload = {
        "id": "score-calibration-smoke",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    result = calibrate_and_validate_score(payload)
    calibration = result["score_calibration"]
    validation = result["validation"]

    print(result["status"])
    print(calibration["status"])
    print(validation["status"])
    print(calibration["calibration_status"])
    print(calibration["raw_score"])
    print(calibration["calibrated_score"])
    print(calibration["grade"])
    print(calibration["quality_band"])
    print(calibration["confidence"])
    print(calibration["signature"])
    print(calibration["metadata"])


if __name__ == "__main__":
    main()
