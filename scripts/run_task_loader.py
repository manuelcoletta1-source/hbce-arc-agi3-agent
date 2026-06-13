from pathlib import Path
from tempfile import TemporaryDirectory

from hbce_arc_agi3.task_loader import load_and_validate_task_file


def main() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        task_path = root / "task-loader-smoke.json"
        task_path.write_text(
            '{"id":"task-loader-smoke","grid":[[1,0],[2,2]],"goal":"solve"}',
            encoding="utf-8",
        )

        result = load_and_validate_task_file(task_path, base_dir=root)

        print(result["status"])
        print(result["loaded_task"]["status"])
        print(result["validation"]["status"])
        print(result["loaded_task"]["task_id"])
        print(result["loaded_task"]["metadata"])


if __name__ == "__main__":
    main()
