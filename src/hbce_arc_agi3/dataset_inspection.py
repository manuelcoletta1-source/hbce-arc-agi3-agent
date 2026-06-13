"""Safe dataset inspection utilities for ARC-AGI-3 public R&D.

This module inspects archive metadata only.
It does not execute files, import dataset code, or expose private data.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List
from zipfile import ZipFile, BadZipFile


@dataclass(frozen=True)
class DatasetInspection:
    status: str
    archive_path: str
    archive_exists: bool
    file_count: int
    top_level_entries: List[str]
    extension_counts: Dict[str, int]
    sample_files: List[str]
    error: str | None = None

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


def inspect_archive(archive_path: str | Path, sample_limit: int = 25) -> DatasetInspection:
    path = Path(archive_path)

    if not path.exists():
        return DatasetInspection(
            status="DATASET_ARCHIVE_MISSING",
            archive_path=str(path),
            archive_exists=False,
            file_count=0,
            top_level_entries=[],
            extension_counts={},
            sample_files=[],
            error="archive_not_found",
        )

    try:
        with ZipFile(path) as zf:
            names = sorted(name for name in zf.namelist() if name and not name.endswith("/"))
    except BadZipFile:
        return DatasetInspection(
            status="DATASET_ARCHIVE_INVALID",
            archive_path=str(path),
            archive_exists=True,
            file_count=0,
            top_level_entries=[],
            extension_counts={},
            sample_files=[],
            error="bad_zip_file",
        )

    top_level = sorted({name.split("/", 1)[0] for name in names if name})
    extension_counts: Dict[str, int] = {}
    for name in names:
        suffix = Path(name).suffix.lower() or "[no_extension]"
        extension_counts[suffix] = extension_counts.get(suffix, 0) + 1

    return DatasetInspection(
        status="DATASET_INSPECTION_READY",
        archive_path=str(path),
        archive_exists=True,
        file_count=len(names),
        top_level_entries=top_level,
        extension_counts=dict(sorted(extension_counts.items())),
        sample_files=names[:sample_limit],
    )
