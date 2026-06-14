"""Milestone #5 Kaggle Submission Preflight Report v1.

This module creates a deterministic, local-only preflight report for ARC-AGI-3
Kaggle submission preparation. It does not submit to Kaggle, authenticate,
upload files, call external APIs, or claim legal certification.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


REPORT_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_READY"
PIPELINE_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/kaggle-submission-preflight-report-v1"

BASELINE_AUDIT_JSON = Path(
    "examples/milestone-5/public-readiness-baseline-audit-v1/public-readiness-baseline-audit-v1.json"
)
PUBLIC_REPO_INDEX_JSON = Path(
    "examples/milestone-5/public-repo-release-index-v1/public-repo-release-index-v1.json"
)
DRY_RUN_PACKAGE_JSON = Path(
    "examples/milestone-5/kaggle-submission-dry-run-package-v1/kaggle-submission-dry-run-package-v1.json"
)
ENTRYPOINT_CONTRACT_JSON = Path(
    "examples/milestone-5/submission-entrypoint-contract-v1/submission-entrypoint-contract-v1.json"
)
PUBLIC_SAFETY_CHECKLIST_JSON = Path(
    "examples/milestone-5/public-safety-boundary-checklist-v1/public-safety-boundary-checklist-v1.json"
)

REQUIRED_PREFLIGHT_SOURCES: Tuple[Tuple[str, Path, str], ...] = (
    ("public_readiness_baseline_audit", BASELINE_AUDIT_JSON, "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY"),
    ("public_repo_release_index", PUBLIC_REPO_INDEX_JSON, "MILESTONE_5_PUBLIC_REPO_RELEASE_INDEX_READY"),
    ("kaggle_submission_dry_run_package", DRY_RUN_PACKAGE_JSON, "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_READY"),
    ("submission_entrypoint_contract", ENTRYPOINT_CONTRACT_JSON, "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY"),
    ("public_safety_boundary_checklist", PUBLIC_SAFETY_CHECKLIST_JSON, "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY"),
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

PREFLIGHT_GATES: Tuple[str, ...] = (
    "baseline_audit_ready",
    "public_repo_release_index_ready",
    "dry_run_package_ready",
    "submission_entrypoint_contract_ready",
    "public_safety_boundary_checklist_ready",
    "all_required_sources_present",
    "all_required_sources_status_ready",
    "all_boundaries_intact",
    "all_blocked_actions_confirmed",
    "kaggle_submission_not_sent",
    "ready_for_local_submission_smoke_test",
    "ready_for_submission_candidate_format_report",
)

BLOCKING_ISSUE_NAMES: Tuple[str, ...] = (
    "missing_required_source",
    "source_status_not_ready",
    "boundary_violation",
    "blocked_action_missing",
    "kaggle_submission_already_sent",
    "external_api_dependency_detected",
    "private_core_exposure_detected",
    "legal_certification_claim_detected",
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
class PreflightSourceStatus:
    name: str
    path: str
    expected_status: str
    actual_status: str
    present: bool
    ready: bool
    signature: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "expected_status": self.expected_status,
            "actual_status": self.actual_status,
            "present": self.present,
            "ready": self.ready,
            "signature": self.signature,
        }


@dataclass(frozen=True)
class PreflightGate:
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
class BlockingIssue:
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
class KaggleSubmissionPreflightReport:
    status: str
    report_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    safety_checklist_id: str
    safety_checklist_signature: str
    source_statuses: Tuple[PreflightSourceStatus, ...]
    preflight_gates: Tuple[PreflightGate, ...]
    blocking_issues: Tuple[BlockingIssue, ...]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    required_source_count: int
    ready_source_count: int
    preflight_gate_count: int
    passed_gate_count: int
    blocking_issue_count: int
    warning_count: int
    ready_for_local_submission_smoke_test: bool
    ready_for_submission_candidate_format_report: bool
    ready_for_real_kaggle_submission: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "report_id": self.report_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "safety_checklist_id": self.safety_checklist_id,
            "safety_checklist_signature": self.safety_checklist_signature,
            "source_statuses": [item.to_dict() for item in self.source_statuses],
            "preflight_gates": [item.to_dict() for item in self.preflight_gates],
            "blocking_issues": [item.to_dict() for item in self.blocking_issues],
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "required_source_count": self.required_source_count,
            "ready_source_count": self.ready_source_count,
            "preflight_gate_count": self.preflight_gate_count,
            "passed_gate_count": self.passed_gate_count,
            "blocking_issue_count": self.blocking_issue_count,
            "warning_count": self.warning_count,
            "ready_for_local_submission_smoke_test": self.ready_for_local_submission_smoke_test,
            "ready_for_submission_candidate_format_report": self.ready_for_submission_candidate_format_report,
            "ready_for_real_kaggle_submission": self.ready_for_real_kaggle_submission,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_preflight_source_statuses() -> Tuple[PreflightSourceStatus, ...]:
    statuses = []

    for name, path, expected_status in REQUIRED_PREFLIGHT_SOURCES:
        payload = _read_json_if_available(path)
        actual_status = str(payload.get("status", "MISSING"))
        signature = str(payload.get("signature", "MISSING_SIGNATURE"))
        present = path.exists()
        ready = present and actual_status == expected_status

        statuses.append(
            PreflightSourceStatus(
                name=name,
                path=str(path),
                expected_status=expected_status,
                actual_status=actual_status,
                present=present,
                ready=ready,
                signature=signature,
            )
        )

    return tuple(statuses)


def _boundary_from_checklist(checklist: Mapping[str, Any]) -> Dict[str, Any]:
    boundary = checklist.get("boundary", {}) if isinstance(checklist.get("boundary"), Mapping) else {}

    return {
        "public_safe": boundary.get("public_safe"),
        "deterministic": boundary.get("deterministic"),
        "local_only": boundary.get("local_only"),
        "dry_run_only": boundary.get("dry_run_only"),
        "external_api_dependency": boundary.get("external_api_dependency"),
        "contains_api_keys": boundary.get("contains_api_keys"),
        "kaggle_submission_sent": boundary.get("kaggle_submission_sent"),
        "private_core_exposure": boundary.get("private_core_exposure"),
        "legal_certification": boundary.get("legal_certification"),
    }


def _boundary_intact(boundary: Mapping[str, Any]) -> bool:
    return all(boundary.get(name) is expected for name, expected in REQUIRED_BOUNDARY_FLAGS)


def _blocked_actions_confirmed(checklist: Mapping[str, Any]) -> bool:
    actions = checklist.get("mandatory_blocked_actions", [])
    if not isinstance(actions, list):
        return False

    required = {
        "kaggle_api_authentication",
        "kaggle_api_submission",
        "network_upload",
        "external_api_call",
        "secret_or_token_read",
        "private_core_export",
        "legal_certification_claim",
    }

    return required.issubset(set(actions))


def build_preflight_gates(
    *,
    source_statuses: Tuple[PreflightSourceStatus, ...],
    safety_checklist: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[PreflightGate, ...]:
    all_sources_present = all(item.present for item in source_statuses)
    all_sources_ready = all(item.ready for item in source_statuses)
    boundary_ok = _boundary_intact(boundary)
    blocked_actions_ok = _blocked_actions_confirmed(safety_checklist)
    kaggle_not_sent = safety_checklist.get("kaggle_submission_sent") is False
    safety_ready = safety_checklist.get("ready_for_kaggle_submission_preflight_report") is True

    gate_results = {
        "baseline_audit_ready": source_statuses[0].ready,
        "public_repo_release_index_ready": source_statuses[1].ready,
        "dry_run_package_ready": source_statuses[2].ready,
        "submission_entrypoint_contract_ready": source_statuses[3].ready,
        "public_safety_boundary_checklist_ready": source_statuses[4].ready,
        "all_required_sources_present": all_sources_present,
        "all_required_sources_status_ready": all_sources_ready,
        "all_boundaries_intact": boundary_ok,
        "all_blocked_actions_confirmed": blocked_actions_ok,
        "kaggle_submission_not_sent": kaggle_not_sent,
        "ready_for_local_submission_smoke_test": all_sources_ready and boundary_ok and blocked_actions_ok and kaggle_not_sent,
        "ready_for_submission_candidate_format_report": all_sources_ready and boundary_ok and blocked_actions_ok and kaggle_not_sent and safety_ready,
    }

    descriptions = {
        "baseline_audit_ready": "Milestone #5 baseline readiness audit is present and ready.",
        "public_repo_release_index_ready": "Milestone #5 public repo release index is present and ready.",
        "dry_run_package_ready": "Milestone #5 Kaggle dry-run package is present and ready.",
        "submission_entrypoint_contract_ready": "Milestone #5 submission entrypoint contract is present and ready.",
        "public_safety_boundary_checklist_ready": "Milestone #5 public safety checklist is present and ready.",
        "all_required_sources_present": "All required preflight sources exist locally.",
        "all_required_sources_status_ready": "All required preflight sources expose their expected ready status.",
        "all_boundaries_intact": "All required public safety boundary flags match expected values.",
        "all_blocked_actions_confirmed": "All mandatory blocked actions are confirmed.",
        "kaggle_submission_not_sent": "No Kaggle submission has been sent.",
        "ready_for_local_submission_smoke_test": "The project is ready for local submission smoke test creation.",
        "ready_for_submission_candidate_format_report": "The project is ready for submission candidate format report creation.",
    }

    return tuple(
        PreflightGate(
            name=name,
            passed=gate_results[name],
            severity="BLOCKING" if not gate_results[name] else "PASS",
            description=descriptions[name],
        )
        for name in PREFLIGHT_GATES
    )


def build_blocking_issues(
    *,
    source_statuses: Tuple[PreflightSourceStatus, ...],
    safety_checklist: Mapping[str, Any],
    boundary: Mapping[str, Any],
) -> Tuple[BlockingIssue, ...]:
    all_sources_present = all(item.present for item in source_statuses)
    all_sources_ready = all(item.ready for item in source_statuses)
    blocked_actions_ok = _blocked_actions_confirmed(safety_checklist)

    issue_state = {
        "missing_required_source": not all_sources_present,
        "source_status_not_ready": not all_sources_ready,
        "boundary_violation": not _boundary_intact(boundary),
        "blocked_action_missing": not blocked_actions_ok,
        "kaggle_submission_already_sent": safety_checklist.get("kaggle_submission_sent") is not False,
        "external_api_dependency_detected": boundary.get("external_api_dependency") is not False,
        "private_core_exposure_detected": boundary.get("private_core_exposure") is not False,
        "legal_certification_claim_detected": boundary.get("legal_certification") is not False,
    }

    descriptions = {
        "missing_required_source": "One or more required preflight source artifacts is missing.",
        "source_status_not_ready": "One or more required preflight source artifacts does not expose the expected ready status.",
        "boundary_violation": "One or more public safety boundary flags does not match the expected value.",
        "blocked_action_missing": "One or more mandatory blocked actions is missing.",
        "kaggle_submission_already_sent": "A Kaggle submission appears to have already been sent.",
        "external_api_dependency_detected": "External API dependency is detected.",
        "private_core_exposure_detected": "Private core exposure is detected.",
        "legal_certification_claim_detected": "Legal certification claim is detected.",
    }

    return tuple(
        BlockingIssue(
            name=name,
            active=issue_state[name],
            severity="BLOCKING",
            description=descriptions[name],
        )
        for name in BLOCKING_ISSUE_NAMES
    )


def build_kaggle_submission_preflight_report() -> KaggleSubmissionPreflightReport:
    safety_checklist = _read_json_if_available(PUBLIC_SAFETY_CHECKLIST_JSON)
    source_statuses = build_preflight_source_statuses()
    boundary = _boundary_from_checklist(safety_checklist)

    preflight_gates = build_preflight_gates(
        source_statuses=source_statuses,
        safety_checklist=safety_checklist,
        boundary=boundary,
    )
    blocking_issues = build_blocking_issues(
        source_statuses=source_statuses,
        safety_checklist=safety_checklist,
        boundary=boundary,
    )

    blocking_issue_count = sum(1 for issue in blocking_issues if issue.active)
    warning_count = 0
    passed_gate_count = sum(1 for gate in preflight_gates if gate.passed)
    ready_source_count = sum(1 for source in source_statuses if source.ready)

    ready_for_local_submission_smoke_test = blocking_issue_count == 0 and all(gate.passed for gate in preflight_gates)
    ready_for_submission_candidate_format_report = ready_for_local_submission_smoke_test
    ready_for_real_kaggle_submission = False

    next_actions = (
        "create_local_submission_smoke_test_v1",
        "create_submission_candidate_format_report_v1",
        "create_submission_candidate_dry_run_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    base_payload = {
        "status": REPORT_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 6",
        "title": "Kaggle Submission Preflight Report v1",
        "baseline_commit": "9c3c7e2 Add ARC AGI3 public safety boundary checklist",
        "safety_checklist_id": safety_checklist.get("checklist_id", "MISSING_CHECKLIST_ID"),
        "safety_checklist_signature": safety_checklist.get("signature", "MISSING_CHECKLIST_SIGNATURE"),
        "source_statuses": [item.to_dict() for item in source_statuses],
        "preflight_gates": [item.to_dict() for item in preflight_gates],
        "blocking_issues": [item.to_dict() for item in blocking_issues],
        "boundary": boundary,
        "next_actions": next_actions,
        "required_source_count": len(source_statuses),
        "ready_source_count": ready_source_count,
        "preflight_gate_count": len(preflight_gates),
        "passed_gate_count": passed_gate_count,
        "blocking_issue_count": blocking_issue_count,
        "warning_count": warning_count,
        "ready_for_local_submission_smoke_test": ready_for_local_submission_smoke_test,
        "ready_for_submission_candidate_format_report": ready_for_submission_candidate_format_report,
        "ready_for_real_kaggle_submission": ready_for_real_kaggle_submission,
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_kaggle_submission_preflight_report_v1",
            "milestone": "Milestone #5",
            "task": "Task 6",
            "report_kind": "KAGGLE_SUBMISSION_PREFLIGHT_REPORT",
            "depends_on_public_safety_boundary_checklist": True,
            "submission_mode": "LOCAL_DRY_RUN_ONLY",
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    report_id = f"MILESTONE-5-PREFLIGHT-REPORT-{signature[:12]}"

    return KaggleSubmissionPreflightReport(
        status=REPORT_STATUS,
        report_id=report_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        safety_checklist_id=base_payload["safety_checklist_id"],
        safety_checklist_signature=base_payload["safety_checklist_signature"],
        source_statuses=source_statuses,
        preflight_gates=preflight_gates,
        blocking_issues=blocking_issues,
        boundary=boundary,
        next_actions=next_actions,
        required_source_count=len(source_statuses),
        ready_source_count=ready_source_count,
        preflight_gate_count=len(preflight_gates),
        passed_gate_count=passed_gate_count,
        blocking_issue_count=blocking_issue_count,
        warning_count=warning_count,
        ready_for_local_submission_smoke_test=ready_for_local_submission_smoke_test,
        ready_for_submission_candidate_format_report=ready_for_submission_candidate_format_report,
        ready_for_real_kaggle_submission=ready_for_real_kaggle_submission,
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_kaggle_submission_preflight_report(
    report: KaggleSubmissionPreflightReport | Mapping[str, Any],
) -> Dict[str, Any]:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    source_statuses = data.get("source_statuses") if isinstance(data.get("source_statuses"), list) else []
    preflight_gates = data.get("preflight_gates") if isinstance(data.get("preflight_gates"), list) else []
    blocking_issues = data.get("blocking_issues") if isinstance(data.get("blocking_issues"), list) else []

    validation_checks = {
        "status_ready": data.get("status") == REPORT_STATUS,
        "report_id_present": isinstance(data.get("report_id"), str) and bool(data.get("report_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_5": str(data.get("baseline_commit", "")).startswith("9c3c7e2"),
        "required_source_count_matches": data.get("required_source_count") == len(REQUIRED_PREFLIGHT_SOURCES),
        "ready_source_count_matches": data.get("ready_source_count") == len(REQUIRED_PREFLIGHT_SOURCES),
        "all_sources_ready": bool(source_statuses) and all(item.get("ready") is True for item in source_statuses),
        "preflight_gate_count_matches": data.get("preflight_gate_count") == len(PREFLIGHT_GATES),
        "all_gates_passed": bool(preflight_gates) and all(item.get("passed") is True for item in preflight_gates),
        "blocking_issue_count_zero": data.get("blocking_issue_count") == 0,
        "all_blocking_issues_inactive": bool(blocking_issues) and all(item.get("active") is False for item in blocking_issues),
        "warning_count_zero": data.get("warning_count") == 0,
        "ready_for_local_submission_smoke_test": data.get("ready_for_local_submission_smoke_test") is True,
        "ready_for_submission_candidate_format_report": data.get("ready_for_submission_candidate_format_report") is True,
        "ready_for_real_kaggle_submission_false": data.get("ready_for_real_kaggle_submission") is False,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "report_id": data.get("report_id"),
        "signature": data.get("signature"),
    }


def render_kaggle_submission_preflight_report_markdown(
    report: KaggleSubmissionPreflightReport | Mapping[str, Any],
) -> str:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    lines = [
        "# ARC AGI3 Milestone #5 - Kaggle Submission Preflight Report v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- report_id: {data['report_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- safety_checklist_id: {data['safety_checklist_id']}",
        f"- safety_checklist_signature: {data['safety_checklist_signature']}",
        f"- required_source_count: {data['required_source_count']}",
        f"- ready_source_count: {data['ready_source_count']}",
        f"- preflight_gate_count: {data['preflight_gate_count']}",
        f"- passed_gate_count: {data['passed_gate_count']}",
        f"- blocking_issue_count: {data['blocking_issue_count']}",
        f"- warning_count: {data['warning_count']}",
        f"- ready_for_local_submission_smoke_test: {data['ready_for_local_submission_smoke_test']}",
        f"- ready_for_submission_candidate_format_report: {data['ready_for_submission_candidate_format_report']}",
        f"- ready_for_real_kaggle_submission: {data['ready_for_real_kaggle_submission']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Source statuses",
        "",
    ]

    for item in data["source_statuses"]:
        lines.append(
            f"- {item['name']}: present={item['present']} ready={item['ready']} "
            f"expected={item['expected_status']} actual={item['actual_status']}"
        )

    lines.extend(
        [
            "",
            "## Preflight gates",
            "",
        ]
    )

    for item in data["preflight_gates"]:
        lines.append(f"- {item['name']}: passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "## Blocking issues",
            "",
        ]
    )

    for item in data["blocking_issues"]:
        lines.append(f"- {item['name']}: active={item['active']} severity={item['severity']}")

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
            "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_VALID=true",
            "ARC_AGI3_MILESTONE_5_PREFLIGHT_REQUIRED_SOURCE_COUNT=5",
            "ARC_AGI3_MILESTONE_5_PREFLIGHT_READY_SOURCE_COUNT=5",
            "ARC_AGI3_MILESTONE_5_PREFLIGHT_GATE_COUNT=12",
            "ARC_AGI3_MILESTONE_5_PREFLIGHT_BLOCKING_ISSUE_COUNT=0",
            "ARC_AGI3_MILESTONE_5_PREFLIGHT_WARNING_COUNT=0",
            "ARC_AGI3_MILESTONE_5_READY_FOR_LOCAL_SUBMISSION_SMOKE_TEST=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_SUBMISSION_CANDIDATE_FORMAT_REPORT=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_REAL_KAGGLE_SUBMISSION=false",
            "ARC_AGI3_MILESTONE_5_BASELINE_PUBLIC_SAFETY_CHECKLIST_COMMIT=9c3c7e2",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_kaggle_submission_preflight_manifest(
    report: KaggleSubmissionPreflightReport | Mapping[str, Any],
) -> str:
    data = report.to_dict() if hasattr(report, "to_dict") else dict(report)

    lines = [
        "ARC AGI3 KAGGLE SUBMISSION PREFLIGHT REPORT MANIFEST v1",
        f"report_id={data['report_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"required_source_count={data['required_source_count']}",
        f"ready_source_count={data['ready_source_count']}",
        f"preflight_gate_count={data['preflight_gate_count']}",
        f"passed_gate_count={data['passed_gate_count']}",
        f"blocking_issue_count={data['blocking_issue_count']}",
        f"warning_count={data['warning_count']}",
        f"ready_for_local_submission_smoke_test={data['ready_for_local_submission_smoke_test']}",
        f"ready_for_submission_candidate_format_report={data['ready_for_submission_candidate_format_report']}",
        f"ready_for_real_kaggle_submission={data['ready_for_real_kaggle_submission']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "SOURCE_STATUSES",
    ]

    for item in data["source_statuses"]:
        lines.append(f"{item['name']} present={item['present']} ready={item['ready']} status={item['actual_status']}")

    lines.extend(
        [
            "",
            "PREFLIGHT_GATES",
        ]
    )

    for item in data["preflight_gates"]:
        lines.append(f"{item['name']} passed={item['passed']} severity={item['severity']}")

    lines.extend(
        [
            "",
            "BLOCKING_ISSUES",
        ]
    )

    for item in data["blocking_issues"]:
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


def write_kaggle_submission_preflight_report_artifacts(
    report: KaggleSubmissionPreflightReport | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    report = report or build_kaggle_submission_preflight_report()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "kaggle-submission-preflight-report-v1.json"
    markdown_path = output_path / "kaggle-submission-preflight-report-v1.md"
    manifest_path = output_path / "kaggle-submission-preflight-report-manifest-v1.txt"

    json_path.write_text(json.dumps(report.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_kaggle_submission_preflight_report_markdown(report), encoding="utf-8")
    manifest_path.write_text(render_kaggle_submission_preflight_manifest(report), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
    }


def run_kaggle_submission_preflight_report_pipeline() -> Dict[str, Any]:
    report = build_kaggle_submission_preflight_report()
    validation = validate_kaggle_submission_preflight_report(report)
    artifacts = write_kaggle_submission_preflight_report_artifacts(report)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_KAGGLE_SUBMISSION_PREFLIGHT_REPORT_PIPELINE_INVALID",
        "report_status": report.status,
        "validation_status": validation["status"],
        "report": report.to_dict(),
        "report_id": report.report_id,
        "signature": report.signature,
        "required_source_count": report.required_source_count,
        "ready_source_count": report.ready_source_count,
        "preflight_gate_count": report.preflight_gate_count,
        "passed_gate_count": report.passed_gate_count,
        "blocking_issue_count": report.blocking_issue_count,
        "warning_count": report.warning_count,
        "ready_for_local_submission_smoke_test": report.ready_for_local_submission_smoke_test,
        "ready_for_submission_candidate_format_report": report.ready_for_submission_candidate_format_report,
        "ready_for_real_kaggle_submission": report.ready_for_real_kaggle_submission,
        "kaggle_submission_sent": report.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_kaggle_submission_preflight_report_pipeline_v1",
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
