from pathlib import Path

from hbce_arc_agi3.benchmark_report import (
    generate_and_validate_benchmark_report,
    write_benchmark_report_markdown,
)


def main() -> None:
    payload = {
        "id": "benchmark-report-smoke",
        "candidate_output": [[1, 0], [2, 2]],
        "expected_output": [[1, 0], [2, 3]],
    }

    result = generate_and_validate_benchmark_report(payload)
    report = result["benchmark_report"]
    validation = result["validation"]

    output_path = write_benchmark_report_markdown(
        report,
        Path("examples/reports/benchmark-report-smoke.md"),
    )

    print(result["status"])
    print(report["status"])
    print(validation["status"])
    print(report["report_status"])
    print(report["grade"])
    print(report["quality_band"])
    print(report["confidence"])
    print(report["signature"])
    print(output_path)
    print(report["metadata"])


if __name__ == "__main__":
    main()
