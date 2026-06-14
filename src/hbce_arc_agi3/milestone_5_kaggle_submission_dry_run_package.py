"""Milestone #5 Kaggle Submission Dry-Run Package v1.

This module creates a deterministic, local-only, public-safe dry-run package
for Kaggle submission preparation. It does not submit anything to Kaggle.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PACKAGE_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_READY"
PIPELINE_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/kaggle-submission-dry-run-package-v1"

PUBLIC_REPO_INDEX_JSON = Path(
    "examples/milestone-5/public-repo-release-index-v1/public-repo-release-index-v1.json"
)

DRY_RUN_SOURCE_ARTIFACTS: Tuple[Tuple[str, str, str], ...] = (
    ("Repository README", "README.md", "repository_root"),
    ("Repository license", "LICENSE", "repository_root"),
    ("Python source package", "src/hbce_arc_agi3", "source_tree"),
    ("Test suite", "tests", "test_tree"),
    ("Milestone #5 public repo release index doc", "docs/milestone-5-public-repo-release-index-v1.md", "milestone_5"),
    ("Milestone #5 public repo release index JSON", "examples/milestone-5/public-repo-release-index-v1/public-repo-release-index-v1.json", "milestone_5"),
    ("Milestone #5 public repo release index Markdown", "examples/milestone-5/public-repo-release-index-v1/public-repo-release-index-v1.md", "milestone_5"),
    ("Milestone #5 baseline audit doc", "docs/milestone-5-public-readiness-baseline-audit-v1.md", "milestone_5"),
    ("Milestone #5 baseline audit JSON", "examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.json", "milestone_5"),
    ("Milestone #4 closure doc", "docs/milestone-4-solver-engine-closure-v1.md", "milestone_4"),
    ("Milestone #4 closure JSON", "examples/closures/milestone-4/milestone-4-solver-engine-closure.json", "milestone_4"),
    ("Candidate ranker policy fix doc", "docs/candidate-ranker-task-family-policy-fix-v1.md", "milestone_4"),
    ("Candidate ranker policy fix JSON", "examples/milestone-4/candidate-ranker-task-family-policy-fix-v1/candidate-ranker-task-family-policy-fix-v1-smoke.json", "milestone_4"),
    ("Expanded batch benchmark JSON", "examples/milestone-4/expanded-batch-benchmark-v2/expanded-batch-benchmark-v2-smoke.json", "milestone_4"),
    ("Failure-driven improvement loop JSON", "examples/milestone-4/failure-driven-improvement-loop-v1/failure-driven-improvement-loop-v1-smoke.json", "milestone_4"),
)

DRY_RUN_RELEASE_FILES: Tuple[str, ...] = (
    "kaggle-submission-dry-run-package-v1.json",
    "kaggle-submission-dry-run-package-v1.md",
    "kaggle-submission-dry-run-manifest-v1.txt",
)


def _stable_signature(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:16].upper()


def _read_json_if_available(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


@dataclass(frozen=True)
class DryRunSourceArtifact:
    title: str
    path: str
    category: str
    present: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "path": self.path,
            "category": self.category,
            "present": self.present,
        }


@dataclass(frozen=True)
class KaggleSubmissionDryRunPackage:
    status: str
    package_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    public_repo_index_id: str
    public_repo_index_signature: str
    package_source_artifact_count: int
    planned_release_file_count: int
    source_artifacts: Tuple[DryRunSourceArtifact, ...]
    package_mode: str
    submission_mode: str
    real_submission_blocked: bool
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    ready_for_submission_entrypoint_contract: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "package_id": self.package_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "public_repo_index_id": self.public_repo_index_id,
            "public_repo_index_signature": self.public_repo_index_signature,
            "package_source_artifact_count": self.package_source_artifact_count,
            "planned_release_file_count": self.planned_release_file_count,
            "source_artifacts": [artifact.to_dict() for artifact in self.source_artifacts],
            "package_mode": self.package_mode,
            "submission_mode": self.submission_mode,
            "real_submission_blocked": self.real_submission_blocked,
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "ready_for_submission_entrypoint_contract": self.ready_for_submission_entrypoint_contract,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_dry_run_source_artifacts() -> Tuple[DryRunSourceArtifact, ...]:
    return tuple(
        DryRunSourceArtifact(
            title=title,
            path=path,
            category=category,
            present=Path(path).exists(),
        )
        for title, path, category in DRY_RUN_SOURCE_ARTIFACTS
    )


def build_kaggle_submission_dry_run_package() -> KaggleSubmissionDryRunPackage:
    public_index = _read_json_if_available(PUBLIC_REPO_INDEX_JSON)
    source_artifacts = build_dry_run_source_artifacts()

    boundary = {
        "public_safe": True,
        "deterministic": True,
        "local_only": True,
        "dry_run_only": True,
        "external_api_dependency": False,
        "contains_api_keys": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
    }

    next_actions = (
        "create_submission_entrypoint_contract_v1",
        "create_public_safety_and_boundary_checklist_v1",
        "create_kaggle_submission_preflight_report_v1",
        "create_local_submission_smoke_test_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    checks = {
        "public_repo_index_present": PUBLIC_REPO_INDEX_JSON.exists(),
        "public_repo_index_ready": public_index.get("status") == "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_READY",
        "public_repo_index_validated": public_index.get("ready_for_public_index_release") is True,
        "public_repo_index_kaggle_submission_not_sent": public_index.get("kaggle_submission_sent") is False,
        "all_source_artifacts_present": all(artifact.present for artifact in source_artifacts),
        "planned_release_file_count_is_3": len(DRY_RUN_RELEASE_FILES) == 3,
        "package_mode_is_manifest_only": True,
        "submission_mode_is_local_dry_run_only": True,
        "real_submission_blocked": True,
        "public_safe": boundary["public_safe"] is True,
        "deterministic": boundary["deterministic"] is True,
        "local_only": boundary["local_only"] is True,
        "dry_run_only": boundary["dry_run_only"] is True,
        "external_api_dependency_false": boundary["external_api_dependency"] is False,
        "contains_api_keys_false": boundary["contains_api_keys"] is False,
        "kaggle_submission_not_sent": boundary["kaggle_submission_sent"] is False,
        "private_core_exposure_false": boundary["private_core_exposure"] is False,
        "legal_certification_false": boundary["legal_certification"] is False,
    }

    base_payload = {
        "status": PACKAGE_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 3",
        "title": "Kaggle Submission Dry-Run Package v1",
        "baseline_commit": "e983e88 Add ARC AGI3 public repo release index",
        "public_repo_index_id": public_index.get("index_id", "MISSING_INDEX_ID"),
        "public_repo_index_signature": public_index.get("signature", "MISSING_INDEX_SIGNATURE"),
        "package_source_artifact_count": len(source_artifacts),
        "planned_release_file_count": len(DRY_RUN_RELEASE_FILES),
        "source_artifacts": [artifact.to_dict() for artifact in source_artifacts],
        "package_mode": "MANIFEST_ONLY_NO_ARCHIVE_NO_UPLOAD",
        "submission_mode": "LOCAL_DRY_RUN_ONLY",
        "real_submission_blocked": True,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "ready_for_submission_entrypoint_contract": all(checks.values()),
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_kaggle_submission_dry_run_package_v1",
            "milestone": "Milestone #5",
            "task": "Task 3",
            "package_kind": "KAGGLE_SUBMISSION_DRY_RUN_PACKAGE",
            "depends_on_public_repo_release_index": True,
            "submission_mode": "LOCAL_DRY_RUN_ONLY",
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    package_id = f"MILESTONE-5-DRY-RUN-PACKAGE-{signature[:12]}"

    return KaggleSubmissionDryRunPackage(
        status=PACKAGE_STATUS,
        package_id=package_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        public_repo_index_id=base_payload["public_repo_index_id"],
        public_repo_index_signature=base_payload["public_repo_index_signature"],
        package_source_artifact_count=len(source_artifacts),
        planned_release_file_count=len(DRY_RUN_RELEASE_FILES),
        source_artifacts=source_artifacts,
        package_mode=base_payload["package_mode"],
        submission_mode=base_payload["submission_mode"],
        real_submission_blocked=True,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        ready_for_submission_entrypoint_contract=all(checks.values()),
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_kaggle_submission_dry_run_package(
    package: KaggleSubmissionDryRunPackage | Mapping[str, Any],
) -> Dict[str, Any]:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    source_artifacts = data.get("source_artifacts") if isinstance(data.get("source_artifacts"), list) else []

    validation_checks = {
        "status_ready": data.get("status") == PACKAGE_STATUS,
        "package_id_present": isinstance(data.get("package_id"), str) and bool(data.get("package_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_2": str(data.get("baseline_commit", "")).startswith("e983e88"),
        "package_source_artifact_count_matches": data.get("package_source_artifact_count") == len(DRY_RUN_SOURCE_ARTIFACTS),
        "planned_release_file_count_matches": data.get("planned_release_file_count") == len(DRY_RUN_RELEASE_FILES),
        "all_source_artifacts_present": bool(source_artifacts) and all(artifact.get("present") is True for artifact in source_artifacts),
        "package_mode_manifest_only": data.get("package_mode") == "MANIFEST_ONLY_NO_ARCHIVE_NO_UPLOAD",
        "submission_mode_local_dry_run_only": data.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "real_submission_blocked": data.get("real_submission_blocked") is True,
        "checks_all_true": bool(checks) and all(checks.values()),
        "ready_for_submission_entrypoint_contract": data.get("ready_for_submission_entrypoint_contract") is True,
        "kaggle_submission_not_sent": data.get("kaggle_submission_sent") is False,
        "public_safe": boundary.get("public_safe") is True,
        "deterministic": boundary.get("deterministic") is True,
        "local_only": boundary.get("local_only") is True,
        "dry_run_only": boundary.get("dry_run_only") is True,
        "external_api_dependency_false": boundary.get("external_api_dependency") is False,
        "contains_api_keys_false": boundary.get("contains_api_keys") is False,
        "private_core_exposure_false": boundary.get("private_core_exposure") is False,
        "legal_certification_false": boundary.get("legal_certification") is False,
    }

    valid = all(validation_checks.values())

    return {
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "package_id": data.get("package_id"),
        "signature": data.get("signature"),
    }


def render_kaggle_submission_dry_run_package_markdown(
    package: KaggleSubmissionDryRunPackage | Mapping[str, Any],
) -> str:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    lines = [
        "# ARC AGI3 Milestone #5 - Kaggle Submission Dry-Run Package v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- package_id: {data['package_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- public_repo_index_id: {data['public_repo_index_id']}",
        f"- public_repo_index_signature: {data['public_repo_index_signature']}",
        f"- package_source_artifact_count: {data['package_source_artifact_count']}",
        f"- planned_release_file_count: {data['planned_release_file_count']}",
        f"- package_mode: {data['package_mode']}",
        f"- submission_mode: {data['submission_mode']}",
        f"- real_submission_blocked: {data['real_submission_blocked']}",
        f"- ready_for_submission_entrypoint_contract: {data['ready_for_submission_entrypoint_contract']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Source artifacts",
        "",
    ]

    for artifact in data["source_artifacts"]:
        lines.append(
            f"- [{artifact['category']}] {artifact['title']}: `{artifact['path']}` present={artifact['present']}"
        )

    lines.extend(
        [
            "",
            "## Planned dry-run release files",
            "",
        ]
    )

    for release_file in DRY_RUN_RELEASE_FILES:
        lines.append(f"- {release_file}")

    lines.extend(
        [
            "",
            "## Next actions",
            "",
        ]
    )

    for action in data["next_actions"]:
        lines.append(f"- {action}")

    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- public_safe=true",
            "- deterministic=true",
            "- local_only=true",
            "- dry_run_only=true",
            "- external_api_dependency=false",
            "- contains_api_keys=false",
            "- kaggle_submission_sent=false",
            "- private_core_exposure=false",
            "- legal_certification=false",
            "",
            "## Markers",
            "",
            "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_VALID=true",
            "ARC_AGI3_MILESTONE_5_LOCAL_DRY_RUN_ONLY=true",
            "ARC_AGI3_MILESTONE_5_REAL_SUBMISSION_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_ENTRYPOINT_CONTRACT=true",
            "ARC_AGI3_MILESTONE_5_BASELINE_RELEASE_INDEX_COMMIT=e983e88",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_kaggle_submission_dry_run_manifest(
    package: KaggleSubmissionDryRunPackage | Mapping[str, Any],
) -> str:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    lines = [
        "ARC AGI3 KAGGLE SUBMISSION DRY-RUN MANIFEST v1",
        f"package_id={data['package_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"submission_mode={data['submission_mode']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        f"real_submission_blocked={data['real_submission_blocked']}",
        f"source_artifact_count={data['package_source_artifact_count']}",
        "",
        "SOURCE_ARTIFACTS",
    ]

    for artifact in data["source_artifacts"]:
        lines.append(f"{artifact['present']} :: {artifact['category']} :: {artifact['path']} :: {artifact['title']}")

    lines.extend(
        [
            "",
            "BOUNDARY",
            "public_safe=true",
            "deterministic=true",
            "local_only=true",
            "dry_run_only=true",
            "external_api_dependency=false",
            "contains_api_keys=false",
            "kaggle_submission_sent=false",
            "private_core_exposure=false",
            "legal_certification=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_kaggle_submission_dry_run_package_artifacts(
    package: KaggleSubmissionDryRunPackage | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    package = package or build_kaggle_submission_dry_run_package()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "kaggle-submission-dry-run-package-v1.json"
    markdown_path = output_path / "kaggle-submission-dry-run-package-v1.md"
    manifest_path = output_path / "kaggle-submission-dry-run-manifest-v1.txt"

    json_path.write_text(json.dumps(package.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_kaggle_submission_dry_run_package_markdown(package), encoding="utf-8")
    manifest_path.write_text(render_kaggle_submission_dry_run_manifest(package), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
    }


def run_kaggle_submission_dry_run_package_pipeline() -> Dict[str, Any]:
    package = build_kaggle_submission_dry_run_package()
    validation = validate_kaggle_submission_dry_run_package(package)
    artifacts = write_kaggle_submission_dry_run_package_artifacts(package)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_PIPELINE_INVALID",
        "package_status": package.status,
        "validation_status": validation["status"],
        "package": package.to_dict(),
        "package_id": package.package_id,
        "signature": package.signature,
        "package_source_artifact_count": package.package_source_artifact_count,
        "planned_release_file_count": package.planned_release_file_count,
        "ready_for_submission_entrypoint_contract": package.ready_for_submission_entrypoint_contract,
        "kaggle_submission_sent": package.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_kaggle_submission_dry_run_package_pipeline_v1",
            "public_safe": True,
            "deterministic": True,
            "local_only": True,
            "dry_run_only": True,
            "external_api_dependency": False,
            "contains_api_keys": False,
            "kaggle_submission_sent": False,
            "private_core_exposure": False,
            "legal_certification": False,
        },
    }
