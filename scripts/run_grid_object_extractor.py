from hbce_arc_agi3.grid_object_extractor import (
    run_grid_object_extractor_pipeline,
    write_grid_object_extractor_artifacts,
)


def main() -> None:
    payload = run_grid_object_extractor_pipeline()
    artifacts = write_grid_object_extractor_artifacts(payload)
    report = payload["extraction_report"]

    print(payload["status"])
    print(payload["extractor_status"])
    print(payload["validation_status"])
    print(report["extraction_id"])
    print(report["background_color"])
    print(report["connectivity"])
    print(report["object_count"])
    print(report["object_density"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
