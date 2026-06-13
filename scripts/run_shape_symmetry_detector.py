from hbce_arc_agi3.shape_symmetry_detector import (
    run_shape_symmetry_detector_pipeline,
    write_shape_symmetry_detector_artifacts,
)


def main() -> None:
    payload = run_shape_symmetry_detector_pipeline()
    artifacts = write_shape_symmetry_detector_artifacts(payload)
    report = payload["detection_report"]

    print(payload["status"])
    print(payload["detector_status"])
    print(payload["validation_status"])
    print(report["detection_id"])
    print(report["pair_count"])
    print(payload["dominant_transform_type"])
    print(payload["stable_transform_type"])
    print(payload["has_rotation_signal"])
    print(payload["has_reflection_signal"])
    print(payload["has_translation_signal"])
    print(payload["confidence"])
    print(payload["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(payload["metadata"])


if __name__ == "__main__":
    main()
