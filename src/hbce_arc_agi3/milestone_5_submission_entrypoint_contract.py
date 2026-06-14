"""Milestone #5 Submission Entrypoint Contract v1.

This module defines the deterministic local-only contract for a future Kaggle
submission entrypoint. It does not upload, submit, authenticate, or call Kaggle.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


CONTRACT_STATUS = "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_READY"
PIPELINE_STATUS = "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/submission-entrypoint-contract-v1"

DRY_RUN_PACKAGE_JSON = Path(
    "examples/milestone-5/kaggle-submission-dry-run-package-v1/kaggle-submission-dry-run-package-v1.json"
)

ENTRYPOINT_NAME = "arc_agi3_submission_entrypoint"
ENTRYPOINT_MODE = "CONTRACT_ONLY_LOCAL_DRY_RUN"
ENTRYPOINT_RUNTIME = "PYTHON_LOCAL_ONLY"
EXPECTED_OUTPUT_FILE = "submission.json"
EXPECTED_SMOKE_MODE = "LOCAL_CONTRACT_SMOKE_ONLY"

REQUIRED_INPUTS: Tuple[Tuple[str, str, bool], ...] = (
    ("repo_root", "Path to local repository root.", True),
    ("source_package", "src/hbce_arc_agi3 local source tree.", True),
    ("test_suite", "tests local validation suite.", True),
    ("dry_run_package", "Milestone #5 Task 3 dry-run package JSON.", True),
    ("public_repo_index", "Milestone #5 Task 2 public repo release index JSON.", True),
)

EXPECTED_OUTPUTS: Tuple[Tuple[str, str, bool], ...] = (
    ("submission_candidate_path", EXPECTED_OUTPUT_FILE, False),
    ("entrypoint_report_json", "submission-entrypoint-contract-v1.json", True),
    ("entrypoint_report_markdown", "submission-entrypoint-contract-v1.md", True),
    ("entrypoint_contract_manifest", "submission-entrypoint-contract-manifest-v1.txt", True),
)

BLOCKED_ACTIONS: Tuple[str, ...] = (
    "kaggle_api_authentication",
    "kaggle_api_submission",
    "network_upload",
    "external_api_call",
    "secret_or_token_read",
    "private_core_export",
    "legal_certification_claim",
)

ALLOWED_ACTIONS: Tuple[str, ...] = (
    "read_local_public_artifacts",
    "validate_local_contract",
    "render_contract_report",
    "render_contract_manifest",
    "run_local_tests",
    "produce_dry_run_metadata",
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
class EntrypointInputContract:
    name: str
    description: str
    required: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "required": self.required,
        }


@dataclass(frozen=True)
class EntrypointOutputContract:
    name: str
    path: str
    produced_by_contract_task: bool

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "produced_by_contract_task": self.produced_by_contract_task,
        }


@dataclass(frozen=True)
class SubmissionEntrypointContract:
    status: str
    contract_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    dry_run_package_id: str
    dry_run_package_signature: str
    entrypoint_name: str
    entrypoint_mode: str
    entrypoint_runtime: str
    expected_output_file: str
    expected_smoke_mode: str
    required_inputs: Tuple[EntrypointInputContract, ...]
    expected_outputs: Tuple[EntrypointOutputContract, ...]
    allowed_actions: Tuple[str, ...]
    blocked_actions: Tuple[str, ...]
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    ready_for_local_submission_smoke_test: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "contract_id": self.contract_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "dry_run_package_id": self.dry_run_package_id,
            "dry_run_package_signature": self.dry_run_package_signature,
            "entrypoint_name": self.entrypoint_name,
            "entrypoint_mode": self.entrypoint_mode,
            "entrypoint_runtime": self.entrypoint_runtime,
            "expected_output_file": self.expected_output_file,
            "expected_smoke_mode": self.expected_smoke_mode,
            "required_inputs": [item.to_dict() for item in self.required_inputs],
            "expected_outputs": [item.to_dict() for item in self.expected_outputs],
            "allowed_actions": list(self.allowed_actions),
            "blocked_actions": list(self.blocked_actions),
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "ready_for_local_submission_smoke_test": self.ready_for_local_submission_smoke_test,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_entrypoint_inputs() -> Tuple[EntrypointInputContract, ...]:
    return tuple(
        EntrypointInputContract(name=name, description=description, required=required)
        for name, description, required in REQUIRED_INPUTS
    )


def build_entrypoint_outputs() -> Tuple[EntrypointOutputContract, ...]:
    return tuple(
        EntrypointOutputContract(
            name=name,
            path=path,
            produced_by_contract_task=produced_by_contract_task,
        )
        for name, path, produced_by_contract_task in EXPECTED_OUTPUTS
    )


def build_submission_entrypoint_contract() -> SubmissionEntrypointContract:
    dry_run_package = _read_json_if_available(DRY_RUN_PACKAGE_JSON)

    required_inputs = build_entrypoint_inputs()
    expected_outputs = build_entrypoint_outputs()

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
        "create_public_safety_and_boundary_checklist_v1",
        "create_kaggle_submission_preflight_report_v1",
        "create_local_submission_smoke_test_v1",
        "create_submission_candidate_format_report_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    checks = {
        "dry_run_package_present": DRY_RUN_PACKAGE_JSON.exists(),
        "dry_run_package_ready": dry_run_package.get("status") == "MILESTONE_5_KAGGLE_SUBMISSION_DRY_RUN_PACKAGE_READY",
        "dry_run_package_validated": dry_run_package.get("ready_for_submission_entrypoint_contract") is True,
        "dry_run_package_local_only": dry_run_package.get("submission_mode") == "LOCAL_DRY_RUN_ONLY",
        "dry_run_package_real_submission_blocked": dry_run_package.get("real_submission_blocked") is True,
        "dry_run_package_kaggle_submission_not_sent": dry_run_package.get("kaggle_submission_sent") is False,
        "entrypoint_mode_contract_only": ENTRYPOINT_MODE == "CONTRACT_ONLY_LOCAL_DRY_RUN",
        "entrypoint_runtime_local_only": ENTRYPOINT_RUNTIME == "PYTHON_LOCAL_ONLY",
        "expected_output_file_is_submission_json": EXPECTED_OUTPUT_FILE == "submission.json",
        "required_inputs_count_is_5": len(REQUIRED_INPUTS) == 5,
        "expected_outputs_count_is_4": len(EXPECTED_OUTPUTS) == 4,
        "blocked_actions_count_is_7": len(BLOCKED_ACTIONS) == 7,
        "allowed_actions_count_is_6": len(ALLOWED_ACTIONS) == 6,
        "kaggle_api_submission_blocked": "kaggle_api_submission" in BLOCKED_ACTIONS,
        "external_api_call_blocked": "external_api_call" in BLOCKED_ACTIONS,
        "network_upload_blocked": "network_upload" in BLOCKED_ACTIONS,
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
        "status": CONTRACT_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 4",
        "title": "Submission Entrypoint Contract v1",
        "baseline_commit": "8dfb106 Add ARC AGI3 Kaggle submission dry-run package",
        "dry_run_package_id": dry_run_package.get("package_id", "MISSING_PACKAGE_ID"),
        "dry_run_package_signature": dry_run_package.get("signature", "MISSING_PACKAGE_SIGNATURE"),
        "entrypoint_name": ENTRYPOINT_NAME,
        "entrypoint_mode": ENTRYPOINT_MODE,
        "entrypoint_runtime": ENTRYPOINT_RUNTIME,
        "expected_output_file": EXPECTED_OUTPUT_FILE,
        "expected_smoke_mode": EXPECTED_SMOKE_MODE,
        "required_inputs": [item.to_dict() for item in required_inputs],
        "expected_outputs": [item.to_dict() for item in expected_outputs],
        "allowed_actions": ALLOWED_ACTIONS,
        "blocked_actions": BLOCKED_ACTIONS,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "ready_for_local_submission_smoke_test": all(checks.values()),
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_submission_entrypoint_contract_v1",
            "milestone": "Milestone #5",
            "task": "Task 4",
            "contract_kind": "SUBMISSION_ENTRYPOINT_CONTRACT",
            "depends_on_kaggle_submission_dry_run_package": True,
            "submission_mode": "CONTRACT_ONLY_LOCAL_DRY_RUN",
            "upload_performed": False,
        },
    }

    signature = _stable_signature(base_payload)
    contract_id = f"MILESTONE-5-ENTRYPOINT-CONTRACT-{signature[:12]}"

    return SubmissionEntrypointContract(
        status=CONTRACT_STATUS,
        contract_id=contract_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        dry_run_package_id=base_payload["dry_run_package_id"],
        dry_run_package_signature=base_payload["dry_run_package_signature"],
        entrypoint_name=ENTRYPOINT_NAME,
        entrypoint_mode=ENTRYPOINT_MODE,
        entrypoint_runtime=ENTRYPOINT_RUNTIME,
        expected_output_file=EXPECTED_OUTPUT_FILE,
        expected_smoke_mode=EXPECTED_SMOKE_MODE,
        required_inputs=required_inputs,
        expected_outputs=expected_outputs,
        allowed_actions=ALLOWED_ACTIONS,
        blocked_actions=BLOCKED_ACTIONS,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        ready_for_local_submission_smoke_test=all(checks.values()),
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_submission_entrypoint_contract(
    contract: SubmissionEntrypointContract | Mapping[str, Any],
) -> Dict[str, Any]:
    data = contract.to_dict() if hasattr(contract, "to_dict") else dict(contract)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    blocked_actions = data.get("blocked_actions") if isinstance(data.get("blocked_actions"), list) else []
    allowed_actions = data.get("allowed_actions") if isinstance(data.get("allowed_actions"), list) else []
    required_inputs = data.get("required_inputs") if isinstance(data.get("required_inputs"), list) else []
    expected_outputs = data.get("expected_outputs") if isinstance(data.get("expected_outputs"), list) else []

    validation_checks = {
        "status_ready": data.get("status") == CONTRACT_STATUS,
        "contract_id_present": isinstance(data.get("contract_id"), str) and bool(data.get("contract_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_task_3": str(data.get("baseline_commit", "")).startswith("8dfb106"),
        "entrypoint_mode_contract_only": data.get("entrypoint_mode") == ENTRYPOINT_MODE,
        "entrypoint_runtime_local_only": data.get("entrypoint_runtime") == ENTRYPOINT_RUNTIME,
        "expected_output_file_submission_json": data.get("expected_output_file") == EXPECTED_OUTPUT_FILE,
        "required_inputs_count_matches": len(required_inputs) == len(REQUIRED_INPUTS),
        "expected_outputs_count_matches": len(expected_outputs) == len(EXPECTED_OUTPUTS),
        "blocked_actions_count_matches": len(blocked_actions) == len(BLOCKED_ACTIONS),
        "allowed_actions_count_matches": len(allowed_actions) == len(ALLOWED_ACTIONS),
        "kaggle_api_submission_blocked": "kaggle_api_submission" in blocked_actions,
        "network_upload_blocked": "network_upload" in blocked_actions,
        "external_api_call_blocked": "external_api_call" in blocked_actions,
        "local_contract_validation_allowed": "validate_local_contract" in allowed_actions,
        "checks_all_true": bool(checks) and all(checks.values()),
        "ready_for_local_submission_smoke_test": data.get("ready_for_local_submission_smoke_test") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "contract_id": data.get("contract_id"),
        "signature": data.get("signature"),
    }


def render_submission_entrypoint_contract_markdown(
    contract: SubmissionEntrypointContract | Mapping[str, Any],
) -> str:
    data = contract.to_dict() if hasattr(contract, "to_dict") else dict(contract)

    lines = [
        "# ARC AGI3 Milestone #5 - Submission Entrypoint Contract v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- contract_id: {data['contract_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- dry_run_package_id: {data['dry_run_package_id']}",
        f"- dry_run_package_signature: {data['dry_run_package_signature']}",
        f"- entrypoint_name: {data['entrypoint_name']}",
        f"- entrypoint_mode: {data['entrypoint_mode']}",
        f"- entrypoint_runtime: {data['entrypoint_runtime']}",
        f"- expected_output_file: {data['expected_output_file']}",
        f"- expected_smoke_mode: {data['expected_smoke_mode']}",
        f"- ready_for_local_submission_smoke_test: {data['ready_for_local_submission_smoke_test']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Required inputs",
        "",
    ]

    for item in data["required_inputs"]:
        lines.append(f"- {item['name']}: required={item['required']} - {item['description']}")

    lines.extend(
        [
            "",
            "## Expected outputs",
            "",
        ]
    )

    for item in data["expected_outputs"]:
        lines.append(
            f"- {item['name']}: `{item['path']}` produced_by_contract_task={item['produced_by_contract_task']}"
        )

    lines.extend(
        [
            "",
            "## Allowed actions",
            "",
        ]
    )

    for action in data["allowed_actions"]:
        lines.append(f"- {action}")

    lines.extend(
        [
            "",
            "## Blocked actions",
            "",
        ]
    )

    for action in data["blocked_actions"]:
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
            "ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_V1_READY=true",
            "ARC_AGI3_MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_VALID=true",
            "ARC_AGI3_MILESTONE_5_ENTRYPOINT_MODE=CONTRACT_ONLY_LOCAL_DRY_RUN",
            "ARC_AGI3_MILESTONE_5_EXPECTED_OUTPUT_FILE=submission.json",
            "ARC_AGI3_MILESTONE_5_READY_FOR_LOCAL_SUBMISSION_SMOKE_TEST=true",
            "ARC_AGI3_MILESTONE_5_KAGGLE_API_SUBMISSION_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_NETWORK_UPLOAD_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_EXTERNAL_API_CALL_BLOCKED=true",
            "ARC_AGI3_MILESTONE_5_BASELINE_DRY_RUN_PACKAGE_COMMIT=8dfb106",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def render_submission_entrypoint_contract_manifest(
    contract: SubmissionEntrypointContract | Mapping[str, Any],
) -> str:
    data = contract.to_dict() if hasattr(contract, "to_dict") else dict(contract)

    lines = [
        "ARC AGI3 SUBMISSION ENTRYPOINT CONTRACT MANIFEST v1",
        f"contract_id={data['contract_id']}",
        f"signature={data['signature']}",
        f"status={data['status']}",
        f"entrypoint_name={data['entrypoint_name']}",
        f"entrypoint_mode={data['entrypoint_mode']}",
        f"entrypoint_runtime={data['entrypoint_runtime']}",
        f"expected_output_file={data['expected_output_file']}",
        f"expected_smoke_mode={data['expected_smoke_mode']}",
        f"ready_for_local_submission_smoke_test={data['ready_for_local_submission_smoke_test']}",
        f"kaggle_submission_sent={data['kaggle_submission_sent']}",
        "",
        "BLOCKED_ACTIONS",
    ]

    for action in data["blocked_actions"]:
        lines.append(action)

    lines.extend(
        [
            "",
            "ALLOWED_ACTIONS",
        ]
    )

    for action in data["allowed_actions"]:
        lines.append(action)

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


def write_submission_entrypoint_contract_artifacts(
    contract: SubmissionEntrypointContract | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    contract = contract or build_submission_entrypoint_contract()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "submission-entrypoint-contract-v1.json"
    markdown_path = output_path / "submission-entrypoint-contract-v1.md"
    manifest_path = output_path / "submission-entrypoint-contract-manifest-v1.txt"

    json_path.write_text(json.dumps(contract.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_submission_entrypoint_contract_markdown(contract), encoding="utf-8")
    manifest_path.write_text(render_submission_entrypoint_contract_manifest(contract), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
        "manifest_path": str(manifest_path),
    }


def run_submission_entrypoint_contract_pipeline() -> Dict[str, Any]:
    contract = build_submission_entrypoint_contract()
    validation = validate_submission_entrypoint_contract(contract)
    artifacts = write_submission_entrypoint_contract_artifacts(contract)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_SUBMISSION_ENTRYPOINT_CONTRACT_PIPELINE_INVALID",
        "contract_status": contract.status,
        "validation_status": validation["status"],
        "contract": contract.to_dict(),
        "contract_id": contract.contract_id,
        "signature": contract.signature,
        "entrypoint_name": contract.entrypoint_name,
        "entrypoint_mode": contract.entrypoint_mode,
        "entrypoint_runtime": contract.entrypoint_runtime,
        "expected_output_file": contract.expected_output_file,
        "blocked_action_count": len(contract.blocked_actions),
        "allowed_action_count": len(contract.allowed_actions),
        "ready_for_local_submission_smoke_test": contract.ready_for_local_submission_smoke_test,
        "kaggle_submission_sent": contract.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_submission_entrypoint_contract_pipeline_v1",
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
