from pathlib import Path

from hbce_arc_agi3.dataset_inspection import inspect_archive


def test_dataset_archive_inspection_contract():
    archive = Path("data/raw/arc-prize-2026-arc-agi-3.zip")
    result = inspect_archive(archive)

    assert result.archive_path == str(archive)
    assert result.status in {"DATASET_INSPECTION_READY", "DATASET_ARCHIVE_MISSING"}

    if archive.exists():
        assert result.archive_exists is True
        assert result.file_count > 0
        assert isinstance(result.extension_counts, dict)
        assert isinstance(result.sample_files, list)
    else:
        assert result.archive_exists is False
        assert result.file_count == 0
        assert result.error == "archive_not_found"
