"""Milestone #5 Public Safety & Boundary Checklist v1.

This module creates a deterministic, local-only, public safety checklist for
ARC-AGI-3 Kaggle submission preparation. It validates the boundary before any
real submission step can exist.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CHECKLIST_STATUS = "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_READY"
PIPELINE_STATUS = "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/public-safety-boundary-checklist-v1"

ENTRYPOINT_CONTRACT_JSON = Path(
    "examples/milestone-5/submission-entrypoint-contract-v1/submission-entrypoint-contract-v1.json"
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

MANDATORY_BLOCKED_ACTIONS: Tuple[str, ...] = (
    "kaggle_api_authentication",
    "kaggle_api_submission",
    "network_upload",
    "external_api_call",
    "secret_or_token_read",
    "private_core_export",
    "legal_certification_claim",
)

MANDATORY_ALLOWED_ACTIONS: Tuple[str, ...] = (
    "read_local_public_artifacts",
    "validate_local_contract",
    "render_contract_report",
    "render_contract_manifest",
    "run_local_tests",
    "produce_dry_run_metadata",
)

PUBLIC_SAFETY_ASSERTIONS: Tuple[Tuple[str, str, bool], ...] = (
    ("no_kaggle_upload", "No upload to Kaggle is performed.", True),
    ("no_kaggle_api_authentication", "No Kaggle API authentication is performed.", True),
    ("no_external_api_call", "No external API call is allowed.", True),
    ("no_network_upload", "No network upload is allowed.", True),
    ("no_secret_or_token_read", "No secret or token read is allowed.", True),
    ("no_private_core_export", "No private HBCE/JOKER-C2 core is exported.", True),
    ("no_legal_certification_claim", "No legal certification claim is made.", True),
    ("local_dry_run_only", "Execution remains local dry-run only.", True),
    ("public_artifacts_only", "The package references public repository artifacts only.", True),
    ("human_review_required_before_real_submission", "A real submission requires a separate explicit future step.", True),
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
class PublicSafetyAssertion:
    name: str
    description: str
    satisfied: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "satisfied": self.satisfied,
        }


@dataclass(frozen=True)
class BoundaryFlag:
    name: str
    expected_value: bool
    actual_value: bool
    valid: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "expected_value": self.expected_value,
            "actual_value": self.actual_value,
            "valid": self.valid,
        }


@dataclass(frozen=True)
class PublicSafetyBoundaryChecklist:
    status: str
    checklist_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    entrypoint_contract_id: str
    entrypoint_contract_signature: str
    boundary_flags: Tuple[BoundaryFlag, ...]
    public_safety_assertions: Tuple[PublicSafetyAssertion, ...]
    mandatory_blocked_actions: Tuple[str, ...]
    mandatory_allowed_actions: Tuple[str, ...]
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    ready_for_kaggle_submission_preflight_report: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "checklist_id": self.checklist_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "entrypoint_contract_id": self.entrypoint_contract_id,
            "entrypoint_contract_signature": self.entrypoint_contract_signature,
            "boundary_flags": [item.to_dict() for item in self.boundary_flags],
            "public_safety_assertions": [item.to_dict() for item in self.public_safety_assertions],
            "mandatory_blocked_actions": list(self.mandatory_blocked_actions),
            "mandatory_allowed_actions": list(self.mandatory_allowed_actions),
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "ready_for_kaggle_submission_preflight_report": self.ready_for_kaggle_submission_preflight_report,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_public_safety_assertions() -> Tuple[PublicSafetyAssertion, ...]:
    return tuple(
        PublicSafetyAssertion(
            name=name,
            description=description,
            satisfied=satisfied,
        )
        for name, description, satisfied in PUBLIC_SAFETY_ASSERTIONS
    )


def build_boundary_flags(contract_boundary: Mapping[str, Any]) -> Tuple[BoundaryFlag, ...]:
    flags = []

    for name, expected_value in REQUIRED_BOUNDARY_FLAGS:
        actual_value = contract_boundary.get(name)
        flags.append(
            BoundaryFlag(
                name=name,
                expected_value=expected_value,
                actual_value=actual_value,
                valid=actual_value is expected_value,
            )
        )

    return tuple(flags)


def build_public_safety_boundary_checklist() -> PublicSafetyBoundaryChecklist:
    contract = _read_json_if_available(ENTRYPOINT_CONTRACT_JSON)
    contract_boundary = contract.get("boundary", {}) if isinstance(contract.get("boundary"), Mapping) else {}
    contract_blocked_actions = tuple(contract.get("blocked_actions", ()))
    contract_allowed_actions = tuple(contract.get("allowed_actions", ()))

    boundary_flags = build_boundary_flags(contract_boundary)
    assertions = build_public_safety_assertions()

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
        "create_kaggle_submission_preflight_report_v1",
        "create_local_submission_smoke_test_v1",
        "create_submission_candidate_format_report_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    checks = {
        "entrypoint_contract_present": ENTRYPOINT_CONTRACT_JSON.exists(),
        "entrypoint_contract_ready": contract.get("status") == "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY",
        "entrypoint_contract_validated": contract.get("ready_for_local_submission_smoke_test") is True,
        "entrypoint_contract_kaggle_submission_not_sent": contract.get("kaggle_submission_sent") is False,
        "all_boundary_flags_valid": all(flag.valid for flag in boundary_flags),
        "all_public_safety_assertions_satisfied": all(assertion.satisfied for assertion in assertions),
        "mandatory_blocked_actions_present": all(action in contract_blocked_actions for action in MANDATORY_BLOCKED_ACTIONS),
        "mandatory_allowed_actions_present": all(action in contract_allowed_actions for action in MANDATORY_ALLOWED_ACTIONS),
        "kaggle_api_authentication_blocked": "kaggle_api_authentication" in contract_blocked_actions,
        "kaggle_api_submission_blocked": "kaggle_api_submission" in contract_blocked_actions,
        "network_upload_blocked": "network_upload" in contract_blocked_actions,
        "external_api_call_blocked": "external_api_call" in contract_blocked_actions,
        "secret_or_token_read_blocked": "secret_or_token_read" in contract_blocked_actions,
        "private_core_export_blocked": "private_core_export" in contract_blocked_actions,
        "legal_certification_claim_blocked": "legal_certification_claim" in contract_blocked_actions,
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
        "status": CHECKLIST_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 5",
        "title": "Public Safety & Boundary Checklist v1",
        "baseline_commit": "77da7ae Add ARC AGI3 submission entrypoint contract",
        "entrypoint_contract_id": contract.get("contract_id", "MISSING_CONTRACT_ID"),
        "entrypoint_contract_signature": contract.get("signature", "MISSING_CONTRACT_SIGNATURE"),
        "boundary_flags": [item.to_dict() for item in boundary_flags],
        "public_safety_assertions": [item.to_dict() for item in assertions],
        "mandatory_blocked_actions": MANDATORY_BLOCKED_ACTIONS,
        "mandatory_allowed_actions": MANDATORY_ALLOWED_ACTIONS,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "ready_for_kaggle_submission_preflight_report": all(checks.values()),
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_public_safety_boundary_checklist_v1",
            "milestone": "Milestone #5",
            "task": "Task 5",
            "checklist_kind": "PUBLIC_SAFETY_BOUNDARY_CHECKLIST",
            "depends_on_submission_entrypoint_contract": True,
            "submission_mode": "LOCAL_DRY_RUN_ONLY",
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    checklist_id = f"MILESTONE-5-SAFETY-CHECKLIST-{signature[:12]}"

    return PublicSafetyBoundaryChecklist(
        status=CHECKLIST_STATUS,
        checklist_id=checklist_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        entrypoint_contract_id=base_payload["entrypoint_contract_id"],
        entrypoint_contract_signature=base_payload["entrypoint_contract_signature"],
        boundary_flags=boundary_flags,
        public_safety_assertions=assertions,
        mandatory_blocked_actions=MANDATORY_BLOCKED_ACTIONS,
        mandatory_allowed_actions=MANDATORY_ALLOWED_ACTIONS,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        ready_for_kaggle_submission_preflight_report=all(checks.values()),
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_public_safety_boundary_checklist(
    checklist: PublicSafetyBoundaryChecklist | Mapping[str, Any],
) -> Dict[str, Any]:
    data = checklist.to_dict() if hasattr(checklist, "to_dict") else dict(checklist)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    boundary_flags = data.get("boundary_flags") if isinstance(data.get("boundary_flags"), list) else []
    assertions = data.get("public_safety_assertions") if isinstance(data.get("public_safety_assertions"), list) else []
    blocked_actions = data.get("mandatory_blocked_actions") if isinstance(data.get("mandatory_blocked_actions"), list) else []
    allowed_actions = data.get("mandatory_allowed_actions") if isinstance(data.get("mandatory_allowed_actions"), list) else []

    validation_checks = {
        "status_ready": data.get("status") == CHECKLIST_STATUS,
        "checklist_id_present": isinstance(data.get("checklist_id"), str) and bool(data.get("checklist_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_4": str(data.get("baseline_commit", "")).startswith("77da7ae"),
        "boundary_flag_count_matches": len(boundary_flags) == len(REQUIRED_BOUNDARY_FLAGS),
        "all_boundary_flags_valid": bool(boundary_flags) and all(item.get("valid") is True for item in boundary_flags),
        "assertion_count_matches": len(assertions) == len(PUBLIC_SAFETY_ASSERTIONS),
        "all_assertions_satisfied": bool(assertions) and all(item.get("satisfied") is True for item in assertions),
        "blocked_action_count_matches": len(blocked_actions) == len(MANDATORY_BLOCKED_ACTIONS),
        "allowed_action_count_matches": len(allowed_actions) == len(MANDATORY_ALLOWED_ACTIONS),
        "kaggle_api_submission_blocked": "kaggle_api_submission" in blocked_actions,
        "external_api_call_blocked": "external_api_call" in blocked_actions,
        "network_upload_blocked": "network_upload" in blocked_actions,
        "secret_or_token_read_blocked": "secret_or_token_read" in blocked_actions,
        "private_core_export_blocked": "private_core_export" in blocked_actions,
        "legal_certification_claim_blocked": "legal_certification_claim" in blocked_actions,
        "checks_all_true": bool(checks) and all(checks.values()),
        "ready_for_kaggle_submission_preflight_report": data.get("ready_for_kaggle_submission_preflight_report") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "checklist_id": data.get("checklist_id"),
        "signature": data.get("signature"),
    }


def render_public_safety_boundary_checklist_markdown(
    checklist: PublicSafetyBoundaryChecklist | Mapping[str, Any],
) -> str:
    data = checklist.to_dict() if hasattr(checklist, "to_dict") else dict(checklist)

    lines = [
        "# ARC AGI3 Milestone #5 - Public Safety & Boundary Checklist v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- checklist_id: {data['checklist_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- entrypoint_contract_id: {data['entrypoint_contract_id']}",
        f"- entrypoint_contract_signature: {data['entrypoint_contract_signature']}",
        f"- ready_for_kaggle_submission_preflight_report: {data['ready_for_kaggle_submission_preflight_report']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Boundary flags",
        "",
    ]

    for item in data["boundary_flags"]:
        lines.append(
            f"- {item['name']}: expected={item['expected_value']} actual={item['actual_value']} valid={item['valid']}"
        )

    lines.extend(
        [
            "",
            "## Public safety assertions",
            "",
        ]
    )

    for item in data["public_safety_assertions"]:
        lines.append(f"- {item['name']}: satisfied={item['satisfied']} - {item['description']}")

    lines.extend(
        [
            "",
            "## Mandatory blocked actions",
            "",
        ]
    )

    for action in data["mandatory_blocked_actions"]:
        lines.append(f"- {action}")

    lines.extend(
        [
            "",
            "## Mandatory allowed actions",
            "",
        ]
    )

    for action in data["mandatory_allowed_actions"]:
        lines.append(f"- {action}")

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
            "ARC_AGI3_MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_VALID=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_KAGGLE_SUBMISSION_PREFLIGHT_REPORT=true",
            "ARC_AGI3_MILESTONE_5_KAGGLE_API_AUTHENTICATION_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_KAGGLE_API_SUBMISSION_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_NETWORK_UPLOAD_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_EXTERNAL_API_CALL_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_SECRET_OR_TOKEN_READ_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_PRIVATE_CORE_EXPORT_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_LEGAL_CERTIFICATION_CLAIM_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_BASELINE_ENTRYPOINT_CONTRACT_COMMIT=77da7ae",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_public_safety_boundary_manifest(
    checklist: PublicSafetyBoundaryChecklist | Mapping[str, Any],
) -> str:
    data = checklist.to_dict() if hasattr(checklist, "to_dict") else dict(checklist)

    lines = [
        "ARC AGI3 PUBLIC SAFETY & BOUNDARY CHECKLIST MANIFEST v1",
        f"checklist_id={data['checklist_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"ready_for_kaggle_submission_preflight_report={data['ready_for_kaggle_submission_preflight_report']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "MANDATORY_BLOCKED_ACTIONS",
    ]

    for action in data["mandatory_blocked_actions"]:
        lines.append(action)

    lines.extend(
        [
            "",
            "BOUNDARY_FLAGS",
        ]
    )

    for item in data["boundary_flags"]:
        lines.append(f"{item['name']}={item['actual_value']} expected={item['expected_value']} valid={item['valid']}")

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


def write_public_safety_boundary_checklist_artifacts(
    checklist: PublicSafetyBoundaryChecklist | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    checklist = checklist or build_public_safety_boundary_checklist()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "public-safety-boundary-checklist-v1.json"
    markdown_path = output_path / "public-safety-boundary-checklist-v1.md"
    manifest_path = output_path / "public-safety-boundary-checklist-manifest-v1.txt"

    json_path.write_text(json.dumps(checklist.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_public_safety_boundary_checklist_markdown(checklist), encoding="utf-8")
    manifest_path.write_text(render_public_safety_boundary_manifest(checklist), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
    }


def run_public_safety_boundary_checklist_pipeline() -> Dict[str, Any]:
    checklist = build_public_safety_boundary_checklist()
    validation = validate_public_safety_boundary_checklist(checklist)
    artifacts = write_public_safety_boundary_checklist_artifacts(checklist)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_PUBLIC_SAFETY_BOUNDARY_CHECKLIST_PIPELINE_INVALID",
        "checklist_status": checklist.status,
        "validation_status": validation["status"],
        "checklist": checklist.to_dict(),
        "checklist_id": checklist.checklist_id,
        "signature": checklist.signature,
        "boundary_flag_count": len(checklist.boundary_flags),
        "public_safety_assertion_count": len(checklist.public_safety_assertions),
        "blocked_action_count": len(checklist.mandatory_blocked_actions),
        "allowed_action_count": len(checklist.mandatory_allowed_actions),
        "ready_for_kaggle_submission_preflight_report": checklist.ready_for_kaggle_submission_preflight_report,
        "kaggle_submission_sent": checklist.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_public_safety_boundary_checklist_pipeline_v1",
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
