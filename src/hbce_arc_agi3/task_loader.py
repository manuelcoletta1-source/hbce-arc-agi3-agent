"""Safe local task loader for HBCE ARC-AGI-3 public baseline.

Task Loader v1 reads controlled local JSON task-like files, validates basic
file boundaries, and normalizes payloads through the public task adapter.

It does not execute dataset code.
It does not call external APIs.
It does not load credentials.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from hbce_arc_agi3.task_adapter import normalize_task


MAX_TASK_JSON_BYTES = 2_000_000


@dataclass(frozen=True)
class LoadedTask:
    status: str
    task_id: str
    source_path: str
    raw_keys: List[str]
    normalized: Dict[str, Any]
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _resolve_within_base(path: Path, base_dir: Optional[Path]) -> Path:
    resolved = path.expanduser().resolve()

    if base_dir is None:
        return resolved

    resolved_base = base_dir.expanduser().resolve()

    try:
        resolved.relative_to(resolved_base)
    except ValueError as exc:
        raise ValueError(f"Task path escapes base_dir: {resolved}") from exc

    return resolved


def _validate_json_task_path(path: Path) -> None:
    if path.suffix.lower() != ".json":
        raise ValueError(f"Task file must be .json: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Task file not found: {path}")

    if not path.is_file():
        raise ValueError(f"Task path is not a file: {path}")

    if path.stat().st_size > MAX_TASK_JSON_BYTES:
        raise ValueError(f"Task file too large: {path}")


def load_task_file(path: str | Path, *, base_dir: str | Path | None = None) -> LoadedTask:
    """Load one local JSON task file safely and normalize it.

    The loader only parses JSON data. It never imports or executes dataset code.
    """

    base_path = Path(base_dir) if base_dir is not None else None
    resolved_path = _resolve_within_base(Path(path), base_path)
    _validate_json_task_path(resolved_path)

    try:
        raw = json.loads(resolved_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON task file: {resolved_path}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"Task JSON root must be an object: {resolved_path}")

    normalized_task = normalize_task(raw)
    normalized_state = normalized_task.to_agent_state()

    return LoadedTask(
        status="TASK_LOADER_READY",
        task_id=normalized_task.task_id,
        source_path=str(resolved_path),
        raw_keys=sorted(str(key) for key in raw.keys()),
        normalized=normalized_state,
        metadata={
            "source": "task_loader_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
            "contains_api_keys": False,
            "base_dir_enforced": base_path is not None,
            "file_size_bytes": resolved_path.stat().st_size,
        },
    )


def list_task_json_files(directory: str | Path, *, recursive: bool = False) -> List[str]:
    """Return deterministic JSON task file paths from a local directory."""

    root = Path(directory).expanduser().resolve()

    if not root.exists():
        raise FileNotFoundError(f"Task directory not found: {root}")

    if not root.is_dir():
        raise ValueError(f"Task path is not a directory: {root}")

    pattern = "**/*.json" if recursive else "*.json"
    files = sorted(path.resolve() for path in root.glob(pattern) if path.is_file())

    return [str(path) for path in files]


def load_task_directory(directory: str | Path, *, recursive: bool = False) -> List[LoadedTask]:
    """Load all local JSON task files in deterministic order."""

    root = Path(directory).expanduser().resolve()
    files = list_task_json_files(root, recursive=recursive)

    return [load_task_file(path, base_dir=root) for path in files]


def validate_loaded_task(task: LoadedTask | Dict[str, Any]) -> Dict[str, Any]:
    """Validate the public loaded-task contract."""

    data = task.to_dict() if isinstance(task, LoadedTask) else task
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    checks = {
        "status_ready": data.get("status") == "TASK_LOADER_READY",
        "task_id_present": bool(data.get("task_id")),
        "source_path_present": bool(data.get("source_path")),
        "raw_keys_present": isinstance(data.get("raw_keys"), list),
        "normalized_present": isinstance(data.get("normalized"), dict),
        "metadata_public_safe": metadata.get("public_safe") is True,
        "metadata_deterministic": metadata.get("deterministic") is True,
        "external_api_dependency_false": metadata.get("external_api_dependency") is False,
        "executes_dataset_code_false": metadata.get("executes_dataset_code") is False,
        "contains_api_keys_false": metadata.get("contains_api_keys") is False,
    }

    valid = all(checks.values())

    return {
        "status": "TASK_LOADER_VALID" if valid else "TASK_LOADER_INVALID",
        "valid": valid,
        "checks": checks,
        "task_id": data.get("task_id"),
        "metadata": {
            "source": "task_loader_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
        },
    }


def load_and_validate_task_file(
    path: str | Path,
    *,
    base_dir: str | Path | None = None,
) -> Dict[str, Any]:
    """Compatibility wrapper for loading and validating one task file."""

    loaded = load_task_file(path, base_dir=base_dir)
    validation = validate_loaded_task(loaded)

    return {
        "status": "TASK_LOADER_PIPELINE_READY",
        "loaded_task": loaded.to_dict(),
        "validation": validation,
        "metadata": {
            "source": "task_loader_v1",
            "public_safe": True,
            "deterministic": True,
            "external_api_dependency": False,
            "executes_dataset_code": False,
        },
    }
