from hbce_arc_agi3.milestone_2_closure import (
    generate_and_validate_milestone_2_closure_report,
    write_milestone_2_closure_artifacts,
)


def main() -> None:
    result = generate_and_validate_milestone_2_closure_report()
    report = result["milestone_2_closure"]
    validation = result["validation"]
    artifacts = write_milestone_2_closure_artifacts(report)

    print(result["status"])
    print(report["status"])
    print(validation["status"])
    print(report["closure_status"])
    print(report["milestone_status"])
    print(report["closed_tasks"])
    print(report["total_tasks"])
    print(report["tests_passed"])
    print(report["dry_run_package"]["package_id"])
    print(report["signature"])
    print(artifacts["markdown_path"])
    print(artifacts["json_path"])
    print(report["metadata"])


if __name__ == "__main__":
    main()
