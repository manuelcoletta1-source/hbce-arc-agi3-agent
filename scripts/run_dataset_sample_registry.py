from hbce_arc_agi3.dataset_sample_registry import (
    generate_and_validate_dataset_sample_registry,
    write_dataset_sample_registry_artifacts,
)


def main() -> None:
    result = generate_and_validate_dataset_sample_registry()
    registry = result["dataset_sample_registry"]
    validation = result["validation"]
    artifacts = write_dataset_sample_registry_artifacts(registry)

    print(result["status"])
    print(registry["status"])
    print(validation["status"])
    print(registry["registry_status"])
    print(registry["registry_id"])
    print(registry["sample_count"])
    print(registry["signature"])
    print(artifacts["json_path"])
    print(artifacts["markdown_path"])
    print(registry["metadata"])


if __name__ == "__main__":
    main()
