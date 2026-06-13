from hbce_arc_agi3.failure_taxonomy import (
    generate_and_validate_failure_taxonomy_report,
    write_failure_taxonomy_artifacts,
)


def main() -> None:
    result = generate_and_validate_failure_taxonomy_report()
    report = result["failure_taxonomy_report"]
    validation = result["validation"]
    artifacts = write_failure_taxonomy_artifacts(report)

    print(result["status"])
    print(report["status"])
    print(validation["status"])
    print(report["taxonomy_status"])
    print(report["taxonomy_report_id"])
    print(report["index_id"])
    print(report["aggregate_id"])
    print(report["batch_id"])
    print(report["registry_id"])
    print(report["selected_strategy_id"])
    print(report["selected_strategy_name"])
    print(report["total_outcomes"])
    print(report["exact_match_count"])
    print(report["partial_count"])
    print(report["failure_count"])
    print(report["unverified_count"])
    print(report["primary_failure_class"])
    print(report["severity_band"])
    print(report["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(report["metadata"])


if __name__ == "__main__":
    main()
