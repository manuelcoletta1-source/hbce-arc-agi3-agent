from hbce_arc_agi3.object_model import build_object_model, validate_object_model


def main() -> None:
    payload = {
        "id": "object-model-smoke",
        "grid": [
            [1, 0, 2, 2],
            [1, 0, 0, 2],
            [0, 3, 3, 0],
        ],
        "goal": "solve",
    }

    model = build_object_model(payload)
    validation = validate_object_model(model)

    print(model.status)
    print(validation["status"])
    print(model.object_count)
    print(model.object_density)
    print(model.signature)
    print(model.metadata)


if __name__ == "__main__":
    main()
