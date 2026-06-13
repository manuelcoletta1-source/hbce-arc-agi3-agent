from pathlib import Path
from tempfile import TemporaryDirectory

from hbce_arc_agi3.environment_harness import run_and_validate_task_file


def main() -> None:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        task_path = root / "environment-harness-smoke.json"
        task_path.write_text(
            '{"id":"environment-harness-smoke","grid":[[1,0],[2,2]],"goal":"solve"}',
            encoding="utf-8",
        )

        result = run_and_validate_task_file(task_path, base_dir=root)

        print(result["status"])
        print(result["run"]["status"])
        print(result["validation"]["status"])
        print(result["run"]["task_id"])
        print(result["run"]["trace_validation"]["status"])
        print(result["run"]["metadata"])


if __name__ == "__main__":
    main()
