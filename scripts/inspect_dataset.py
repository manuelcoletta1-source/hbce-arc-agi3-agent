#!/usr/bin/env python3
"""Inspect ARC-AGI-3 raw dataset archive safely."""

from __future__ import annotations

from hbce_arc_agi3.dataset_inspection import inspect_archive


ARCHIVE_PATH = "data/raw/arc-prize-2026-arc-agi-3.zip"


def main() -> int:
    result = inspect_archive(ARCHIVE_PATH)
    data = result.to_dict()

    print(data["status"])
    print(f"archive={data['archive_path']}")
    print(f"archive_exists={data['archive_exists']}")
    print(f"file_count={data['file_count']}")
    print(f"top_level_entries={','.join(data['top_level_entries'])}")
    print(f"extension_counts={data['extension_counts']}")

    if data["sample_files"]:
        print("sample_files:")
        for name in data["sample_files"][:10]:
            print(f"- {name}")

    return 0 if data["status"] == "DATASET_INSPECTION_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
