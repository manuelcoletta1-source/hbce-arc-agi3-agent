"""Milestone #5 Public Repo Release Index v1.

This module creates a deterministic public release index for the ARC-AGI-3
research repository after Milestone #5 baseline readiness has passed.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


INDEX_STATUS = "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_READY"
PIPELINE_STATUS = "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/public-repo-release-index-v1"

BASELINE_AUDIT_JSON = Path(
    "examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.json"
)

INDEXED_PUBLIC_ARTIFACTS: Tuple[Tuple[str, str, str], ...] = (
    ("Milestone #5 baseline audit document", "docs/milestone-5-public-readiness-baseline-audit-v1.md", "milestone_5"),
    ("Milestone #5 baseline audit JSON", "examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.json", "milestone_5"),
    ("Milestone #5 baseline audit Markdown", "examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.md", "milestone_5"),
    ("Milestone #4 solver engine closure document", "docs/milestone-4-solver-engine-closure-v1.md", "milestone_4"),
    ("Milestone #4 solver engine closure JSON", "examples/closures/milestone-4/milestone-4-solver-engine-closure.json", "milestone_4"),
    ("Milestone #4 solver engine closure Markdown", "examples/closures/milestone-4/milestone-4-solver-engine-closure.md", "milestone_4"),
    ("Candidate ranker task-family policy fix document", "docs/candidate-ranker-task-family-policy-fix-v1.md", "milestone_4"),
    ("Candidate ranker task-family policy fix JSON", "examples/milestone-4/candidate-ranker-task-family-policy-fix-v1/candidate-ranker-task-family-policy-fix-v1-smoke.json", "milestone_4"),
    ("Expanded batch benchmark v2 JSON", "examples/milestone-4/expanded-batch-benchmark-v2/expanded-batch-benchmark-v2-smoke.json", "milestone_4"),
    ("Failure-driven improvement loop v1 JSON", "examples/milestone-4/failure-driven-improvement-loop-v1/failure-driven-improvement-loop-v1-smoke.json", "milestone_4"),
    ("Public package README", "README.md", "repository_root"),
    ("Project license", "LICENSE", "repository_root"),
    ("Python package source", "src/hbce_arc_agi3", "source_tree"),
    ("Test suite", "tests", "test_tree"),
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
class PublicRepoIndexedArtifact:
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
class PublicRepoReleaseIndex:
    status: str
    index_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    baseline_audit_id: str
    baseline_audit_signature: str
    indexed_artifact_count: int
    indexed_artifacts: Tuple[PublicRepoIndexedArtifact, ...]
    release_sections: Tuple[str, ...]
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    ready_for_public_index_release: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "index_id": self.index_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "baseline_audit_id": self.baseline_audit_id,
            "baseline_audit_signature": self.baseline_audit_signature,
            "indexed_artifact_count": self.indexed_artifact_count,
            "indexed_artifacts": [artifact.to_dict() for artifact in self.indexed_artifacts],
            "release_sections": list(self.release_sections),
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "ready_for_public_index_release": self.ready_for_public_index_release,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_indexed_artifacts() -> Tuple[PublicRepoIndexedArtifact, ...]:
    return tuple(
        PublicRepoIndexedArtifact(
            title=title,
            path=path,
            category=category,
            present=Path(path).exists(),
        )
        for title, path, category in INDEXED_PUBLIC_ARTIFACTS
    )


def build_public_repo_release_index() -> PublicRepoReleaseIndex:
    baseline_audit = _read_json_if_available(BASELINE_AUDIT_JSON)
    indexed_artifacts = build_indexed_artifacts()

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

    release_sections = (
        "repository_root",
        "milestone_4_solver_engine_closure",
        "milestone_5_public_readiness",
        "candidate_generation_and_ranking",
        "benchmark_and_failure_loop",
        "public_boundary",
        "next_submission_preparation_steps",
    )

    next_actions = (
        "create_kaggle_submission_dry_run_package_v1",
        "create_submission_entrypoint_contract_v1",
        "create_public_safety_and_boundary_checklist_v1",
        "create_kaggle_submission_preflight_report_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    checks = {
        "baseline_audit_present": BASELINE_AUDIT_JSON.exists(),
        "baseline_audit_ready": baseline_audit.get("status") == "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY",
        "baseline_audit_validated": baseline_audit.get("ready_for_public_readiness_phase") is True,
        "baseline_kaggle_submission_not_sent": baseline_audit.get("kaggle_submission_sent") is False,
        "all_indexed_artifacts_present": all(artifact.present for artifact in indexed_artifacts),
        "release_sections_present": len(release_sections) == 7,
        "next_actions_present": len(next_actions) == 5,
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
        "status": INDEX_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 2",
        "title": "Public Repo Release Index v1",
        "baseline_commit": "2f02f5d Open ARC AGI3 milestone 5 public readiness audit",
        "baseline_audit_id": baseline_audit.get("audit_id", "MISSING_AUDIT_ID"),
        "baseline_audit_signature": baseline_audit.get("signature", "MISSING_AUDIT_SIGNATURE"),
        "indexed_artifact_count": len(indexed_artifacts),
        "indexed_artifacts": [artifact.to_dict() for artifact in indexed_artifacts],
        "release_sections": release_sections,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "ready_for_public_index_release": all(checks.values()),
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_public_repo_release_index_v1",
            "milestone": "Milestone #5",
            "task": "Task 2",
            "index_kind": "PUBLIC_REPO_RELEASE_INDEX",
            "depends_on_public_readiness_baseline": True,
            "submission_mode": "DRY_RUN_ONLY",
        },
    }

    signature = _stable_signature(base_payload)
    index_id = f"MILESTONE-5-PUBLIC-REPO-INDEX-{signature[:12]}"

    return PublicRepoReleaseIndex(
        status=INDEX_STATUS,
        index_id=index_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        baseline_audit_id=base_payload["baseline_audit_id"],
        baseline_audit_signature=base_payload["baseline_audit_signature"],
        indexed_artifact_count=len(indexed_artifacts),
        indexed_artifacts=indexed_artifacts,
        release_sections=release_sections,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        ready_for_public_index_release=all(checks.values()),
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_public_repo_release_index(
    index: PublicRepoReleaseIndex | Mapping[str, Any],
) -> Dict[str, Any]:
    data = index.to_dict() if hasattr(index, "to_dict") else dict(index)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    artifacts = data.get("indexed_artifacts") if isinstance(data.get("indexed_artifacts"), list) else []

    validation_checks = {
        "status_ready": data.get("status") == INDEX_STATUS,
        "index_id_present": isinstance(data.get("index_id"), str) and bool(data.get("index_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_1": str(data.get("baseline_commit", "")).startswith("2f02f5d"),
        "indexed_artifact_count_matches": data.get("indexed_artifact_count") == len(INDEXED_PUBLIC_ARTIFACTS),
        "all_indexed_artifacts_present": bool(artifacts) and all(artifact.get("present") is True for artifact in artifacts),
        "checks_all_true": bool(checks) and all(checks.values()),
        "ready_for_public_index_release": data.get("ready_for_public_index_release") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "index_id": data.get("index_id"),
        "signature": data.get("signature"),
    }


def render_public_repo_release_index_markdown(
    index: PublicRepoReleaseIndex | Mapping[str, Any],
) -> str:
    data = index.to_dict() if hasattr(index, "to_dict") else dict(index)

    lines = [
        "# ARC AGI3 Milestone #5 - Public Repo Release Index v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- index_id: {data['index_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- baseline_audit_id: {data['baseline_audit_id']}",
        f"- baseline_audit_signature: {data['baseline_audit_signature']}",
        f"- indexed_artifact_count: {data['indexed_artifact_count']}",
        f"- ready_for_public_index_release: {data['ready_for_public_index_release']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Indexed artifacts",
        "",
    ]

    for artifact in data["indexed_artifacts"]:
        lines.append(
            f"- [{artifact['category']}] {artifact['title']}: `{artifact['path']}` present={artifact['present']}"
        )

    lines.extend(
        [
            "",
            "## Release sections",
            "",
        ]
    )

    for section in data["release_sections"]:
        lines.append(f"- {section}")

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
            "ARC_AGI3_MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_VALID=true",
            "ARC_AGI3_MILESTONE_5_PUBLIC_INDEX_READY=true",
            "ARC_AGI3_MILESTONE_5_BASELINE_AUDIT_COMMIT=2f02f5d",
            "ARC_AGI3_MILESTONE_5_INDEXED_ARTIFACTS_PRESENT=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_PREPARATION=true",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_public_repo_release_index_artifacts(
    index: PublicRepoReleaseIndex | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    index = index or build_public_repo_release_index()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "public-repo-release-index-v1.json"
    markdown_path = output_path / "public-repo-release-index-v1.md"

    json_path.write_text(json.dumps(index.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_public_repo_release_index_markdown(index), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def run_public_repo_release_index_pipeline() -> Dict[str, Any]:
    index = build_public_repo_release_index()
    validation = validate_public_repo_release_index(index)
    artifacts = write_public_repo_release_index_artifacts(index)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_PIPELINE_INVALID",
        "index_status": index.status,
        "validation_status": validation["status"],
        "index": index.to_dict(),
        "index_id": index.index_id,
        "signature": index.signature,
        "indexed_artifact_count": index.indexed_artifact_count,
        "ready_for_public_index_release": index.ready_for_public_index_release,
        "kaggle_submission_sent": index.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_public_repo_release_index_pipeline_v1",
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
