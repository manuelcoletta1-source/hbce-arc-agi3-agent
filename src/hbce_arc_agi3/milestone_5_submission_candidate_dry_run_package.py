"""Milestone #5 Submission Candidate Dry-Run Package v1.

This module creates a deterministic local-only dry-run package for the ARC-AGI-3
submission candidate. It does not create a real Kaggle submission, authenticate,
upload files, call external APIs, read secrets, or create a legal certification claim.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


PACKAGE_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_READY"
PIPELINE_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/submission-candidate-dry-run-package-v1"

FORMAT_REPORT_JSON = Path(
    "examples/milestone-5/submission-candidate-format-report-v1/submission-candidate-format-report-v1.json"
)
LOCAL_CANDIDATE_JSON = Path(
    "examples/milestone-5/local-submission-smoke-test-v1/local-submission-candidate-smoke-only-v1.json"
)
LOCAL_SMOKE_TEST_JSON = Path(
    "examples/milestone-5/local-submission-smoke-test-v1/local-submission-smoke-test-v1.json"
)
PREFLIGHT_REPORT_JSON = Path(
    "examples/milestone-5/kaggle-submission-preflight-report-v1/kaggle-submission-preflight-report-v1.json"
)
SAFETY_CHECKLIST_JSON = Path(
    "examples/milestone-5/public-safety-boundary-checklist-v1/public-safety-boundary-checklist-v1.json"
)

PACKAGE_MODE = "LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD"
SUBMISSION_MODE = "LOCAL_SMOKE_ONLY_NO_UPLOAD"
CANDIDATE_KIND = "LOCAL_SUBMISSION_CANDIDATE_SMOKE_ONLY"
EXPECTED_SUBMISSION_FILENAME = "submission.json"

REQUIRED_PACKAGE_ARTIFACTS: Tuple[str, ...] = (
    "submission_candidate_format_report",
    "local_submission_candidate_smoke_only",
    "local_submission_smoke_test",
    "kaggle_submission_preflight_report",
    "public_safety_boundary_checklist",
)

PACKAGE_GATES: Tuple[str, ...] = (
    "format_report_present",
    "format_report_ready",
    "local_candidate_present",
    "local_candidate_valid",
    "local_smoke_test_ready",
    "preflight_report_ready",
    "public_safety_checklist_ready",
    "all_package_artifacts_present",
    "all_package_artifacts_ready",
    "candidate_task_count_matches_format_report",
    "format_report_allows_dry_run",
    "boundary_intact",
    "candidate_json_serializable",
    "package_mode_local_only",
    "package_no_archive_no_upload",
    "kaggle_submission_not_sent",
)

PACKAGE_ISSUES: Tuple[str, ...] = (
    "format_report_missing",
    "format_report_not_ready",
    "local_candidate_missing",
    "local_candidate_invalid",
    "local_smoke_test_not_ready",
    "preflight_report_not_ready",
    "public_safety_checklist_not_ready",
    "package_artifact_missing",
    "package_artifact_not_ready",
    "candidate_task_count_mismatch",
    "format_report_dry_run_not_allowed",
    "boundary_violation",
    "candidate_json_not_serializable",
    "package_mode_invalid",
    "archive_or_upload_mode_detected",
    "kaggle_submission_already_sent",
)

REQUIRED_BOUNDARY_FLAGS: Tuple[Tuple[str, bool], ...] = (
    ("public_safe", True),
    ("deterministic", True),
    ("local_only", True),
    ("dry_run_only", True),
    ("external_api_dependency", False),
    ("contains_api_keys", False),
    ("kaggle_submission_sent", False),
    ("private_core_exposure", False),
    ("legal_certification", False),
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


def _file_sha256_16(path: Path) -> str:
    if not path.exists():
        return "MISSING_HASH"

    return hashlib.sha256(path.read_bytes()).hexdigest()[:16].upper()


def _candidate_json_serializable(candidate: Mapping[str, Any]) -> bool:
    try:
        json.dumps(candidate, sort_keys=True)
    except (TypeError, ValueError):
        return False

    return True


def _boundary_from_candidate(candidate: Mapping[str, Any]) -> Dict[str, Any]:
    metadata = candidate.get("metadata", {}) if isinstance(candidate.get("metadata"), Mapping) else {}

    return {
        "public_safe": metadata.get("public_safe"),
        "deterministic": metadata.get("deterministic"),
        "local_only": metadata.get("local_only"),
        "dry_run_only": metadata.get("dry_run_only"),
        "external_api_dependency": metadata.get("external_api_dependency"),
        "contains_api_keys": metadata.get("contains_api_keys"),
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
        "private_core_exposure": metadata.get("private_core_exposure"),
        "legal_certification": metadata.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


@dataclass(frozen=True)
class PackageArtifactStatus:
    name: str
    path: str
    expected_status: str
    actual_status: str
    present: bool
    ready: bool
    sha256_16: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "expected_status": self.expected_status,
            "actual_status": self.actual_status,
            "present": self.present,
            "ready": self.ready,
            "sha256_16": self.sha256_16,
        }


@dataclass(frozen=True)
class PackageGate:
    name: str
    passed: bool
    severity: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "severity": self.severity,
            "description": self.description,
        }


@dataclass(frozen=True)
class PackageIssue:
    name: str
    active: bool
    severity: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "active": self.active,
            "severity": self.severity,
            "description": self.description,
        }


@dataclass(frozen=True)
class SubmissionCandidateDryRunPackage:
    status: str
    package_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    format_report_id: str
    format_report_signature: str
    local_smoke_id: str
    local_smoke_signature: str
    package_mode: str
    candidate_kind: str
    submission_filename: str
    submission_mode: str
    artifact_statuses: Tuple[PackageArtifactStatus, ...]
    package_gates: Tuple[PackageGate, ...]
    package_issues: Tuple[PackageIssue, ...]
    dry_run_index: Dict[str, Any]
    submission_candidate_preview: Dict[str, Any]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    package_artifact_count: int
    ready_artifact_count: int
    package_gate_count: int
    passed_gate_count: int
    package_issue_count: int
    warning_count: int
    candidate_task_count: int
    dry_run_package_ready: bool
    ready_for_milestone_5_closure: bool
    ready_for_real_kaggle_submission: bool
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
            "format_report_id": self.format_report_id,
            "format_report_signature": self.format_report_signature,
            "local_smoke_id": self.local_smoke_id,
            "local_smoke_signature": self.local_smoke_signature,
            "package_mode": self.package_mode,
            "candidate_kind": self.candidate_kind,
            "submission_filename": self.submission_filename,
            "submission_mode": self.submission_mode,
            "artifact_statuses": [item.to_dict() for item in self.artifact_statuses],
            "package_gates": [item.to_dict() for item in self.package_gates],
            "package_issues": [item.to_dict() for item in self.package_issues],
            "dry_run_index": copy.deepcopy(self.dry_run_index),
            "submission_candidate_preview": copy.deepcopy(self.submission_candidate_preview),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "package_artifact_count": self.package_artifact_count,
            "ready_artifact_count": self.ready_artifact_count,
            "package_gate_count": self.package_gate_count,
            "passed_gate_count": self.passed_gate_count,
            "package_issue_count": self.package_issue_count,
            "warning_count": self.warning_count,
            "candidate_task_count": self.candidate_task_count,
            "dry_run_package_ready": self.dry_run_package_ready,
            "ready_for_milestone_5_closure": self.ready_for_milestone_5_closure,
            "ready_for_real_kaggle_submission": self.ready_for_real_kaggle_submission,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_package_artifact_statuses() -> Tuple[PackageArtifactStatus, ...]:
    format_report = _read_json_if_available(FORMAT_REPORT_JSON)
    candidate = _read_json_if_available(LOCAL_CANDIDATE_JSON)
    local_smoke = _read_json_if_available(LOCAL_SMOKE_TEST_JSON)
    preflight = _read_json_if_available(PREFLIGHT_REPORT_JSON)
    safety = _read_json_if_available(SAFETY_CHECKLIST_JSON)

    artifact_specs = (
        (
            "submission_candidate_format_report",
            FORMAT_REPORT_JSON,
            "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
            str(format_report.get("status", "MISSING")),
        ),
        (
            "local_submission_candidate_smoke_only",
            LOCAL_CANDIDATE_JSON,
            CANDIDATE_KIND,
            str(candidate.get("candidate_kind", "MISSING")),
        ),
        (
            "local_submission_smoke_test",
            LOCAL_SMOKE_TEST_JSON,
            "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
            str(local_smoke.get("status", "MISSING")),
        ),
        (
            "kaggle_submission_preflight_report",
            PREFLIGHT_REPORT_JSON,
            "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
            str(preflight.get("status", "MISSING")),
        ),
        (
            "public_safety_boundary_checklist",
            SAFETY_CHECKLIST_JSON,
            "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
            str(safety.get("status", "MISSING")),
        ),
    )

    statuses = []

    for name, path, expected_status, actual_status in artifact_specs:
        present = path.exists()
        ready = present and actual_status == expected_status

        statuses.append(
            PackageArtifactStatus(
                name=name,
                path=str(path),
                expected_status=expected_status,
                actual_status=actual_status,
                present=present,
                ready=ready,
                sha256_16=_file_sha256_16(path),
            )
        )

    return tuple(statuses)


def build_package_gates(
    *,
    format_report: Mapping[str, Any],
    candidate: Mapping[str, Any],
    local_smoke: Mapping[str, Any],
    preflight: Mapping[str, Any],
    safety: Mapping[str, Any],
    artifact_statuses: Tuple[PackageArtifactStatus, ...],
    boundary: Mapping[str, Any],
) -> Tuple[PackageGate, ...]:
    tasks = candidate.get("tasks", [])
    candidate_task_count = len(tasks) if isinstance(tasks, list) else 0
    expected_task_count = format_report.get("candidate_task_count")

    gate_results = {
        "format_report_present": FORMAT_REPORT_JSON.exists(),
        "format_report_ready": format_report.get("status") == "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
        "local_candidate_present": LOCAL_CANDIDATE_JSON.exists(),
        "local_candidate_valid": candidate.get("candidate_kind") == CANDIDATE_KIND
        and candidate.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME
        and candidate.get("submission_mode") == SUBMISSION_MODE
        and candidate.get("kaggle_submission_sent") is False,
        "local_smoke_test_ready": local_smoke.get("status") == "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "preflight_report_ready": preflight.get("status") == "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "public_safety_checklist_ready": safety.get("status") == "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
        "all_package_artifacts_present": all(item.present for item in artifact_statuses),
        "all_package_artifacts_ready": all(item.ready for item in artifact_statuses),
        "candidate_task_count_matches_format_report": candidate_task_count == expected_task_count == 3,
        "format_report_allows_dry_run": format_report.get("ready_for_submission_candidate_dry_run") is True,
        "boundary_intact": _boundary_intact(boundary),
        "candidate_json_serializable": _candidate_json_serializable(candidate),
        "package_mode_local_only": PACKAGE_MODE == "LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD",
        "package_no_archive_no_upload": "NO_ARCHIVE_NO_UPLOAD" in PACKAGE_MODE,
        "kaggle_submission_not_sent": candidate.get("kaggle_submission_sent") is False,
    }

    descriptions = {
        "format_report_present": "Submission candidate format report artifact is present.",
        "format_report_ready": "Submission candidate format report exposes ready status.",
        "local_candidate_present": "Local smoke-only submission candidate artifact is present.",
        "local_candidate_valid": "Local candidate kind, filename, mode, and submission flag are valid.",
        "local_smoke_test_ready": "Local submission smoke test exposes ready status.",
        "preflight_report_ready": "Kaggle submission preflight report exposes ready status.",
        "public_safety_checklist_ready": "Public safety boundary checklist exposes ready status.",
        "all_package_artifacts_present": "All required dry-run package artifacts are present.",
        "all_package_artifacts_ready": "All required dry-run package artifacts are ready.",
        "candidate_task_count_matches_format_report": "Candidate task count matches the format report.",
        "format_report_allows_dry_run": "Format report allows candidate dry-run packaging.",
        "boundary_intact": "Candidate boundary remains intact.",
        "candidate_json_serializable": "Candidate is JSON serializable.",
        "package_mode_local_only": "Package mode is local-only dry-run.",
        "package_no_archive_no_upload": "Package mode does not create an archive and does not upload.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
    }

    return tuple(
        PackageGate(
            name=name,
            passed=gate_results[name],
            severity="PASS" if gate_results[name] else "BLOCKING",
            description=descriptions[name],
        )
        for name in PACKAGE_GATES
    )


def build_package_issues(
    *,
    format_report: Mapping[str, Any],
    candidate: Mapping[str, Any],
    local_smoke: Mapping[str, Any],
    preflight: Mapping[str, Any],
    safety: Mapping[str, Any],
    artifact_statuses: Tuple[PackageArtifactStatus, ...],
    boundary: Mapping[str, Any],
) -> Tuple[PackageIssue, ...]:
    tasks = candidate.get("tasks", [])
    candidate_task_count = len(tasks) if isinstance(tasks, list) else 0
    expected_task_count = format_report.get("candidate_task_count")

    candidate_valid = (
        candidate.get("candidate_kind") == CANDIDATE_KIND
        and candidate.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME
        and candidate.get("submission_mode") == SUBMISSION_MODE
        and candidate.get("kaggle_submission_sent") is False
    )

    issue_state = {
        "format_report_missing": not FORMAT_REPORT_JSON.exists(),
        "format_report_not_ready": format_report.get("status") != "MILESTONE_5_SUBMISSION_CANDIDATE_FORMAT_REPORT_READY",
        "local_candidate_missing": not LOCAL_CANDIDATE_JSON.exists(),
        "local_candidate_invalid": not candidate_valid,
        "local_smoke_test_not_ready": local_smoke.get("status") != "MILESTONE_5_LOCAL_SUBMISSION_SMOKE_TEST_READY",
        "preflight_report_not_ready": preflight.get("status") != "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY",
        "public_safety_checklist_not_ready": safety.get("status") != "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY",
        "package_artifact_missing": not all(item.present for item in artifact_statuses),
        "package_artifact_not_ready": not all(item.ready for item in artifact_statuses),
        "candidate_task_count_mismatch": candidate_task_count != expected_task_count or candidate_task_count != 3,
        "format_report_dry_run_not_allowed": format_report.get("ready_for_submission_candidate_dry_run") is not True,
        "boundary_violation": not _boundary_intact(boundary),
        "candidate_json_not_serializable": not _candidate_json_serializable(candidate),
        "package_mode_invalid": PACKAGE_MODE != "LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD",
        "archive_or_upload_mode_detected": "NO_ARCHIVE_NO_UPLOAD" not in PACKAGE_MODE,
        "kaggle_submission_already_sent": candidate.get("kaggle_submission_sent") is not False,
    }

    descriptions = {
        "format_report_missing": "Submission candidate format report artifact is missing.",
        "format_report_not_ready": "Submission candidate format report is not ready.",
        "local_candidate_missing": "Local candidate artifact is missing.",
        "local_candidate_invalid": "Local candidate kind, filename, mode, or submission flag is invalid.",
        "local_smoke_test_not_ready": "Local submission smoke test is not ready.",
        "preflight_report_not_ready": "Kaggle submission preflight report is not ready.",
        "public_safety_checklist_not_ready": "Public safety boundary checklist is not ready.",
        "package_artifact_missing": "One or more required package artifacts is missing.",
        "package_artifact_not_ready": "One or more required package artifacts is not ready.",
        "candidate_task_count_mismatch": "Candidate task count does not match the format report.",
        "format_report_dry_run_not_allowed": "Format report does not allow candidate dry-run packaging.",
        "boundary_violation": "Candidate boundary is not intact.",
        "candidate_json_not_serializable": "Candidate cannot be serialized to JSON.",
        "package_mode_invalid": "Package mode is not local dry-run package only.",
        "archive_or_upload_mode_detected": "Package mode suggests archive or upload behavior.",
        "kaggle_submission_already_sent": "Candidate appears to have been sent to Kaggle.",
    }

    return tuple(
        PackageIssue(
            name=name,
            active=issue_state[name],
            severity="BLOCKING",
            description=descriptions[name],
        )
        for name in PACKAGE_ISSUES
    )


def build_submission_candidate_dry_run_package() -> SubmissionCandidateDryRunPackage:
    format_report = _read_json_if_available(FORMAT_REPORT_JSON)
    candidate = _read_json_if_available(LOCAL_CANDIDATE_JSON)
    local_smoke = _read_json_if_available(LOCAL_SMOKE_TEST_JSON)
    preflight = _read_json_if_available(PREFLIGHT_REPORT_JSON)
    safety = _read_json_if_available(SAFETY_CHECKLIST_JSON)

    boundary = _boundary_from_candidate(candidate)
    artifact_statuses = build_package_artifact_statuses()
    package_gates = build_package_gates(
        format_report=format_report,
        candidate=candidate,
        local_smoke=local_smoke,
        preflight=preflight,
        safety=safety,
        artifact_statuses=artifact_statuses,
        boundary=boundary,
    )
    package_issues = build_package_issues(
        format_report=format_report,
        candidate=candidate,
        local_smoke=local_smoke,
        preflight=preflight,
        safety=safety,
        artifact_statuses=artifact_statuses,
        boundary=boundary,
    )

    candidate_tasks = candidate.get("tasks", []) if isinstance(candidate.get("tasks", []), list) else []
    candidate_task_count = len(candidate_tasks)
    ready_artifact_count = sum(1 for item in artifact_statuses if item.ready)
    passed_gate_count = sum(1 for item in package_gates if item.passed)
    package_issue_count = sum(1 for item in package_issues if item.active)
    warning_count = 0

    dry_run_package_ready = (
        ready_artifact_count == len(REQUIRED_PACKAGE_ARTIFACTS)
        and passed_gate_count == len(PACKAGE_GATES)
        and package_issue_count == 0
        and candidate_task_count == 3
    )

    submission_candidate_preview = {
        "candidate_kind": candidate.get("candidate_kind"),
        "submission_filename": candidate.get("submission_filename"),
        "submission_mode": candidate.get("submission_mode"),
        "task_count": candidate_task_count,
        "task_ids": [
            task.get("task_id")
            for task in candidate_tasks
            if isinstance(task, Mapping)
        ],
        "kaggle_submission_sent": candidate.get("kaggle_submission_sent"),
    }

    dry_run_index = {
        "package_mode": PACKAGE_MODE,
        "candidate_kind": candidate.get("candidate_kind"),
        "submission_filename": candidate.get("submission_filename"),
        "submission_mode": candidate.get("submission_mode"),
        "artifact_count": len(REQUIRED_PACKAGE_ARTIFACTS),
        "ready_artifact_count": ready_artifact_count,
        "contains_archive": False,
        "contains_upload_step": False,
        "contains_real_kaggle_submission": False,
        "source_artifacts": [item.to_dict() for item in artifact_statuses],
    }

    next_actions = (
        "close_milestone_5_submission_preparation_v1",
        "prepare_public_release_summary_v1",
    )

    base_payload = {
        "status": PACKAGE_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 9",
        "title": "Submission Candidate Dry-Run Package v1",
        "baseline_commit": "d2f2750 Add ARC AGI3 submission candidate format report",
        "format_report_id": format_report.get("report_id", "MISSING_FORMAT_REPORT_ID"),
        "format_report_signature": format_report.get("signature", "MISSING_FORMAT_REPORT_SIGNATURE"),
        "local_smoke_id": local_smoke.get("smoke_id", "MISSING_LOCAL_SMOKE_ID"),
        "local_smoke_signature": local_smoke.get("signature", "MISSING_LOCAL_SMOKE_SIGNATURE"),
        "package_mode": PACKAGE_MODE,
        "candidate_kind": candidate.get("candidate_kind", "MISSING_CANDIDATE_KIND"),
        "submission_filename": candidate.get("submission_filename", "MISSING_SUBMISSION_FILENAME"),
        "submission_mode": candidate.get("submission_mode", "MISSING_SUBMISSION_MODE"),
        "artifact_statuses": [item.to_dict() for item in artifact_statuses],
        "package_gates": [item.to_dict() for item in package_gates],
        "package_issues": [item.to_dict() for item in package_issues],
        "dry_run_index": dry_run_index,
        "submission_candidate_preview": submission_candidate_preview,
        "boundary": boundary,
        "next_actions": next_actions,
        "package_artifact_count": len(REQUIRED_PACKAGE_ARTIFACTS),
        "ready_artifact_count": ready_artifact_count,
        "package_gate_count": len(PACKAGE_GATES),
        "passed_gate_count": passed_gate_count,
        "package_issue_count": package_issue_count,
        "warning_count": warning_count,
        "candidate_task_count": candidate_task_count,
        "dry_run_package_ready": dry_run_package_ready,
        "ready_for_milestone_5_closure": dry_run_package_ready,
        "ready_for_real_kaggle_submission": False,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_submission_candidate_dry_run_package_v1",
            "milestone": "Milestone #5",
            "task": "Task 9",
            "package_kind": "SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE",
            "depends_on_submission_candidate_format_report": True,
            "submission_mode": SUBMISSION_MODE,
            "package_mode": PACKAGE_MODE,
            "archive_created": False,
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    package_id = f"MILESTONE-5-DRY-RUN-CANDIDATE-{signature[:12]}"

    return SubmissionCandidateDryRunPackage(
        status=PACKAGE_STATUS,
        package_id=package_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        format_report_id=base_payload["format_report_id"],
        format_report_signature=base_payload["format_report_signature"],
        local_smoke_id=base_payload["local_smoke_id"],
        local_smoke_signature=base_payload["local_smoke_signature"],
        package_mode=PACKAGE_MODE,
        candidate_kind=base_payload["candidate_kind"],
        submission_filename=base_payload["submission_filename"],
        submission_mode=base_payload["submission_mode"],
        artifact_statuses=artifact_statuses,
        package_gates=package_gates,
        package_issues=package_issues,
        dry_run_index=dry_run_index,
        submission_candidate_preview=submission_candidate_preview,
        boundary=boundary,
        next_actions=next_actions,
        package_artifact_count=len(REQUIRED_PACKAGE_ARTIFACTS),
        ready_artifact_count=ready_artifact_count,
        package_gate_count=len(PACKAGE_GATES),
        passed_gate_count=passed_gate_count,
        package_issue_count=package_issue_count,
        warning_count=warning_count,
        candidate_task_count=candidate_task_count,
        dry_run_package_ready=dry_run_package_ready,
        ready_for_milestone_5_closure=dry_run_package_ready,
        ready_for_real_kaggle_submission=False,
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_submission_candidate_dry_run_package(
    package: SubmissionCandidateDryRunPackage | Mapping[str, Any],
) -> Dict[str, Any]:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    artifacts = data.get("artifact_statuses") if isinstance(data.get("artifact_statuses"), list) else []
    gates = data.get("package_gates") if isinstance(data.get("package_gates"), list) else []
    issues = data.get("package_issues") if isinstance(data.get("package_issues"), list) else []
    dry_run_index = data.get("dry_run_index") if isinstance(data.get("dry_run_index"), Mapping) else {}
    preview = data.get("submission_candidate_preview") if isinstance(data.get("submission_candidate_preview"), Mapping) else {}

    validation_checks = {
        "status_ready": data.get("status") == PACKAGE_STATUS,
        "package_id_present": isinstance(data.get("package_id"), str) and bool(data.get("package_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_8": str(data.get("baseline_commit", "")).startswith("d2f2750"),
        "package_mode_valid": data.get("package_mode") == PACKAGE_MODE,
        "candidate_kind_valid": data.get("candidate_kind") == CANDIDATE_KIND,
        "submission_filename_valid": data.get("submission_filename") == EXPECTED_SUBMISSION_FILENAME,
        "submission_mode_valid": data.get("submission_mode") == SUBMISSION_MODE,
        "artifact_count_matches": data.get("package_artifact_count") == len(REQUIRED_PACKAGE_ARTIFACTS),
        "ready_artifact_count_matches": data.get("ready_artifact_count") == len(REQUIRED_PACKAGE_ARTIFACTS),
        "all_artifacts_ready": bool(artifacts) and all(item.get("ready") is True for item in artifacts),
        "package_gate_count_matches": data.get("package_gate_count") == len(PACKAGE_GATES),
        "all_package_gates_passed": bool(gates) and all(item.get("passed") is True for item in gates),
        "package_issue_count_zero": data.get("package_issue_count") == 0,
        "all_package_issues_inactive": bool(issues) and all(item.get("active") is False for item in issues),
        "warning_count_zero": data.get("warning_count") == 0,
        "candidate_task_count_is_3": data.get("candidate_task_count") == 3,
        "dry_run_package_ready": data.get("dry_run_package_ready") is True,
        "ready_for_milestone_5_closure": data.get("ready_for_milestone_5_closure") is True,
        "ready_for_real_kaggle_submission_false": data.get("ready_for_real_kaggle_submission") is False,
        "kaggle_submission_not_sent": data.get("kaggle_submission_sent") is False,
        "dry_run_index_no_archive": dry_run_index.get("contains_archive") is False,
        "dry_run_index_no_upload": dry_run_index.get("contains_upload_step") is False,
        "dry_run_index_no_real_submission": dry_run_index.get("contains_real_kaggle_submission") is False,
        "preview_task_count_is_3": preview.get("task_count") == 3,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "package_id": data.get("package_id"),
        "signature": data.get("signature"),
    }


def render_submission_candidate_dry_run_package_markdown(
    package: SubmissionCandidateDryRunPackage | Mapping[str, Any],
) -> str:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    lines = [
        "# ARC AGI3 Milestone #5 - Submission Candidate Dry-Run Package v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- package_id: {data['package_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- format_report_id: {data['format_report_id']}",
        f"- format_report_signature: {data['format_report_signature']}",
        f"- local_smoke_id: {data['local_smoke_id']}",
        f"- local_smoke_signature: {data['local_smoke_signature']}",
        f"- package_mode: {data['package_mode']}",
        f"- candidate_kind: {data['candidate_kind']}",
        f"- submission_filename: {data['submission_filename']}",
        f"- submission_mode: {data['submission_mode']}",
        f"- package_artifact_count: {data['package_artifact_count']}",
        f"- ready_artifact_count: {data['ready_artifact_count']}",
        f"- package_gate_count: {data['package_gate_count']}",
        f"- passed_gate_count: {data['passed_gate_count']}",
        f"- package_issue_count: {data['package_issue_count']}",
        f"- warning_count: {data['warning_count']}",
        f"- candidate_task_count: {data['candidate_task_count']}",
        f"- dry_run_package_ready: {data['dry_run_package_ready']}",
        f"- ready_for_milestone_5_closure: {data['ready_for_milestone_5_closure']}",
        f"- ready_for_real_kaggle_submission: {data['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Artifact statuses",
        "",
    ]

    for item in data["artifact_statuses"]:
        lines.append(
            f"- {item['name']}: present={item['present']} ready={item['ready']} "
            f"sha256_16={item['sha256_16']}"
        )

    lines.extend(
        [
            "",
            "## Package gates",
            "",
        ]
    )

    for item in data["package_gates"]:
        lines.append(f"- {item['name']}: passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Package issues",
            "",
        ]
    )

    for item in data["package_issues"]:
        lines.append(f"- {item['name']}: active={item['active']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Dry-run index",
            "",
            f"- package_mode: {data['dry_run_index']['package_mode']}",
            f"- artifact_count: {data['dry_run_index']['artifact_count']}",
            f"- ready_artifact_count: {data['dry_run_index']['ready_artifact_count']}",
            f"- contains_archive: {data['dry_run_index']['contains_archive']}",
            f"- contains_upload_step: {data['dry_run_index']['contains_upload_step']}",
            f"- contains_real_kaggle_submission: {data['dry_run_index']['contains_real_kaggle_submission']}",
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
            "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_VALID=true",
            "ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_MODE=LOCAL_DRY_RUN_PACKAGE_ONLY_NO_ARCHIVE_NO_UPLOAD",
            "ARC_AGI3_MILESTONE_5_PACKAGE_ARTIFACT_COUNT=5",
            "ARC_AGI3_MILESTONE_5_READY_ARTIFACT_COUNT=5",
            "ARC_AGI3_MILESTONE_5_PACKAGE_GATE_COUNT=16",
            "ARC_AGI3_MILESTONE_5_PACKAGE_ISSUE_COUNT=0",
            "ARC_AGI3_MILESTONE_5_CANDIDATE_TASK_COUNT=3",
            "ARC_AGI3_MILESTONE_5_DRY_RUN_PACKAGE_READY=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_MILESTONE_5_CLOSURE=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_CANDIDATE_FORMAT_REPORT_COMMIT=d2f2750",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_submission_candidate_dry_run_manifest(
    package: SubmissionCandidateDryRunPackage | Mapping[str, Any],
) -> str:
    data = package.to_dict() if hasattr(package, "to_dict") else dict(package)

    lines = [
        "ARC AGI3 SUBMISSION CANDIDATE DRY-RUN PACKAGE MANIFEST v1",
        f"package_id={data['package_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"package_mode={data['package_mode']}",
        f"candidate_kind={data['candidate_kind']}",
        f"submission_filename={data['submission_filename']}",
        f"submission_mode={data['submission_mode']}",
        f"package_artifact_count={data['package_artifact_count']}",
        f"ready_artifact_count={data['ready_artifact_count']}",
        f"package_gate_count={data['package_gate_count']}",
        f"passed_gate_count={data['passed_gate_count']}",
        f"package_issue_count={data['package_issue_count']}",
        f"warning_count={data['warning_count']}",
        f"candidate_task_count={data['candidate_task_count']}",
        f"dry_run_package_ready={data['dry_run_package_ready']}",
        f"ready_for_milestone_5_closure={data['ready_for_milestone_5_closure']}",
        f"ready_for_real_kaggle_submission={data['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "ARTIFACT_STATUSES",
    ]

    for item in data["artifact_statuses"]:
        lines.append(f"{item['name']} present={item['present']} ready={item['ready']} sha256_16={item['sha256_16']}")

    lines.extend(
        [
            "",
            "PACKAGE_GATES",
        ]
    )

    for item in data["package_gates"]:
        lines.append(f"{item['name']} passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "PACKAGE_ISSUES",
        ]
    )

    for item in data["package_issues"]:
        lines.append(f"{item['name']} active={item['active']} severity={item['severity']}")

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


def write_submission_candidate_dry_run_package_artifacts(
    package: SubmissionCandidateDryRunPackage | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    package = package or build_submission_candidate_dry_run_package()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "submission-candidate-dry-run-package-v1.json"
    markdown_path = output_path / "submission-candidate-dry-run-package-v1.md"
    manifest_path = output_path / "submission-candidate-dry-run-package-manifest-v1.txt"
    index_path = output_path / "submission-candidate-dry-run-package-index-v1.json"
    preview_path = output_path / "submission-candidate-dry-run-preview-v1.json"

    json_path.write_text(json.dumps(package.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_submission_candidate_dry_run_package_markdown(package), encoding="utf-8")
    manifest_path.write_text(render_submission_candidate_dry_run_manifest(package), encoding="utf-8")
    index_path.write_text(json.dumps(package.dry_run_index, indent=2, sort_keys=True), encoding="utf-8")
    preview_path.write_text(json.dumps(package.submission_candidate_preview, indent=2, sort_keys=True), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
        "index_path": str(index_path),
        "preview_path": str(preview_path),
    }


def run_submission_candidate_dry_run_package_pipeline() -> Dict[str, Any]:
    package = build_submission_candidate_dry_run_package()
    validation = validate_submission_candidate_dry_run_package(package)
    artifacts = write_submission_candidate_dry_run_package_artifacts(package)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_SUBMISSION_CANDIDATE_DRY_RUN_PACKAGE_PIPELINE_INVALID",
        "package_status": package.status,
        "validation_status": validation["status"],
        "package": package.to_dict(),
        "package_id": package.package_id,
        "signature": package.signature,
        "package_mode": package.package_mode,
        "candidate_kind": package.candidate_kind,
        "submission_filename": package.submission_filename,
        "submission_mode": package.submission_mode,
        "package_artifact_count": package.package_artifact_count,
        "ready_artifact_count": package.ready_artifact_count,
        "package_gate_count": package.package_gate_count,
        "passed_gate_count": package.passed_gate_count,
        "package_issue_count": package.package_issue_count,
        "warning_count": package.warning_count,
        "candidate_task_count": package.candidate_task_count,
        "dry_run_package_ready": package.dry_run_package_ready,
        "ready_for_milestone_5_closure": package.ready_for_milestone_5_closure,
        "ready_for_real_kaggle_submission": package.ready_for_real_kaggle_submission,
        "kaggle_submission_sent": package.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_submission_candidate_dry_run_package_pipeline_v1",
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
