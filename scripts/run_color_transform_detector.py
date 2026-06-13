from hbce_arc_agi3.color_transform_detector import (
    run_color_transform_detector_pipeline,
    write_color_transform_detector_artifacts,
)


def main() -> None:
    payload = run_color_transform_detector_pipeline()
    artifacts = write_color_transform_detector_artifacts(payload)
    report = payload["detection_report"]

    print(payload["status"])
    print(payload["detector_status"])
    print(payload["validation_status"])
    print(report["detection_id"])
    print(report["pair_count"])
    print(payload["stable_mapping_count"])
    print(payload["transform_type"])
    print(payload["confidence"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
