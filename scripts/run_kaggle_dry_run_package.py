from hbce_arc_agi3.kaggle_dry_run_package import build_and_validate_kaggle_dry_run_package


def main() -> None:
    payload = {
        "id": "kaggle-dry-run-smoke",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    result = build_and_validate_kaggle_dry_run_package(payload)
    package = result["kaggle_dry_run_package"]
    validation = result["validation"]

    print(result["status"])
    print(package["status"])
    print(validation["status"])
    print(package["package_status"])
    print(package["package_id"])
    print(package["task_id"])
    print(package["package_signature"])
    print(package["output_dir"])
    print(package["files"])
    print(package["metadata"])


if __name__ == "__main__":
    main()
