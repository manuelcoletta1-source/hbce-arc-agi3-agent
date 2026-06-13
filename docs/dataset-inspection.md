# ARC-AGI-3 Dataset Inspection

Status date: 2026-06-13
Archive: data/raw/arc-prize-2026-arc-agi-3.zip
Mode: SAFE_ARCHIVE_METADATA_INSPECTION

## Inspection output

DATASET_INSPECTION_READY
archive=data/raw/arc-prize-2026-arc-agi-3.zip
archive_exists=True
file_count=148
top_level_entries=ARC-AGI-3-Agents,arc_agi_3_wheels,environment_files
extension_counts={'.example': 1, '.idx': 1, '.ini': 1, '.json': 25, '.lock': 1, '.md': 4, '.pack': 1, '.py': 51, '.rev': 1, '.sample': 14, '.toml': 1, '.txt': 1, '.whl': 31, '.yaml': 1, '[no_extension]': 14}
sample_files:
- ARC-AGI-3-Agents/.env.example
- ARC-AGI-3-Agents/.git/HEAD
- ARC-AGI-3-Agents/.git/config
- ARC-AGI-3-Agents/.git/description
- ARC-AGI-3-Agents/.git/hooks/applypatch-msg.sample
- ARC-AGI-3-Agents/.git/hooks/commit-msg.sample
- ARC-AGI-3-Agents/.git/hooks/fsmonitor-watchman.sample
- ARC-AGI-3-Agents/.git/hooks/post-update.sample
- ARC-AGI-3-Agents/.git/hooks/pre-applypatch.sample
- ARC-AGI-3-Agents/.git/hooks/pre-commit.sample

## Boundary

- archive metadata inspection only
- no dataset code execution
- no external API calls
- no private HBCE/JOKER-C2 core exposure
- legalCertification=false

## Operational markers

ARC_AGI3_DATASET_INSPECTION_READY=true
ARC_AGI3_SAFE_ARCHIVE_METADATA_INSPECTION=true
ARC_AGI3_EXTERNAL_API_DEPENDENCY=false
ARC_AGI3_PRIVATE_CORE_EXPOSURE=false
legalCertification=false
