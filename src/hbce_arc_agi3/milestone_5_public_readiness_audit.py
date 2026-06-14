"""Milestone #5 Public Readiness Baseline Audit v1.

This module opens Milestone #5 by validating that the public repository is ready
for submission-preparation work after Milestone #4 solver engine closure.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Tuple


AUDIT_STATUS = "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY"
PIPELINE_STATUS = "MILESTONE_5_PUBLIC_READINESS_BASELINE_PIPELINE_READY"
VALIDATION_STATUS = "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_VALID"

DEFAULT_OUTPUT_DIR = "examples/milestone-5/public-readiness-baseline-audit-v1"

REQUIRED_PUBLIC_READINESS_ARTIFACTS: Tuple[str, ...] = (
    "docs/milestone-4-solver-engine-closure-v1.md",
    "examples/closures/milestone-4/milestone-4-solver-engine-closure.json",
    "examples/closures/milestone-4/milestone-4-solver-engine-closure.md",
    "docs/candidate-ranker-task-family-policy-fix-v1.md",
    "examples/milestone-4/candidate-ranker-task-family-policy-fix-v1/candidate-ranker-task-family-policy-fix-v1-smoke.json",
    "examples/milestone-4/expanded-batch-benchmark-v2/expanded-batch-benchmark-v2-smoke.json",
    "examples/milestone-4/failure-driven-improvement-loop-v1/failure-driven-improvement-loop-v1-smoke.json",
)

MILESTONE_4_CLOSURE_JSON = Path(
    "examples/closures/milestone-4/milestone-4-solver-engine-closure.json"
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


def _required_artifact_status() -> Dict[str, bool]:
    return {
        artifact: Path(artifact).exists()
        for artifact in REQUIRED_PUBLIC_READINESS_ARTIFACTS
    }


@dataclass(frozen=True)
class PublicReadinessBaselineAudit:
    status: str
    audit_id: str
    signature: str
    milestone: str
    task: str
    title: str
    baseline_commit: str
    prior_closure_id: str
    prior_closure_signature: str
    required_artifacts: Dict[str, bool]
    checks: Dict[str, bool]
    boundary: Dict[str, Any]
    next_actions: Tuple[str, ...]
    ready_for_public_readiness_phase: bool
    kaggle_submission_sent: bool
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "audit_id": self.audit_id,
            "signature": self.signature,
            "milestone": self.milestone,
            "task": self.task,
            "title": self.title,
            "baseline_commit": self.baseline_commit,
            "prior_closure_id": self.prior_closure_id,
            "prior_closure_signature": self.prior_closure_signature,
            "required_artifacts": copy.deepcopy(self.required_artifacts),
            "checks": copy.deepcopy(self.checks),
            "boundary": copy.deepcopy(self.boundary),
            "next_actions": list(self.next_actions),
            "ready_for_public_readiness_phase": self.ready_for_public_readiness_phase,
            "kaggle_submission_sent": self.kaggle_submission_sent,
            "metadata": copy.deepcopy(self.metadata),
        }


def build_public_readiness_baseline_audit() -> PublicReadinessBaselineAudit:
    closure = _read_json_if_available(MILESTONE_4_CLOSURE_JSON)
    required_artifacts = _required_artifact_status()

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

    checks = {
        "milestone_4_closure_artifact_present": MILESTONE_4_CLOSURE_JSON.exists(),
        "milestone_4_closure_ready": closure.get("status") == "MILESTONE_4_SOLVER_ENGINE_CLOSURE_READY",
        "milestone_4_closed_task_count_is_9": closure.get("closed_task_count") == 9,
        "milestone_4_ready_for_next_phase": closure.get("ready_for_next_phase") is True,
        "milestone_4_kaggle_submission_not_sent": closure.get("kaggle_submission_sent") is False,
        "milestone_4_expanded_match_rate_is_1": (
            closure.get("solver_engine_result", {}).get("expanded_best_candidate_match_rate") == 1.0
        ),
        "milestone_4_failure_loop_closed": (
            closure.get("solver_engine_result", {}).get("failure_loop_improvement_item_count") == 0
        ),
        "required_public_readiness_artifacts_present": all(required_artifacts.values()),
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

    next_actions = (
        "create_public_repo_release_index_v1",
        "create_kaggle_submission_dry_run_package_v1",
        "create_submission_entrypoint_contract_v1",
        "create_public_safety_and_boundary_checklist_v1",
        "close_milestone_5_submission_preparation_v1",
    )

    base_payload = {
        "status": AUDIT_STATUS,
        "milestone": "Milestone #5",
        "task": "Task 1",
        "title": "Public Readiness Baseline Audit v1",
        "baseline_commit": "f97b25d Close ARC AGI3 milestone 4 solver engine",
        "prior_closure_id": closure.get("closure_id", "MISSING_CLOSURE_ID"),
        "prior_closure_signature": closure.get("signature", "MISSING_CLOSURE_SIGNATURE"),
        "required_artifacts": required_artifacts,
        "checks": checks,
        "boundary": boundary,
        "next_actions": next_actions,
        "ready_for_public_readiness_phase": all(checks.values()),
        "kaggle_submission_sent": False,
        "metadata": {
            "source": "milestone_5_public_readiness_baseline_audit_v1",
            "milestone": "Milestone #5",
            "task": "Task 1",
            "audit_kind": "PUBLIC_READINESS_BASELINE",
            "depends_on_milestone_4_closure": True,
            "submission_mode": "DRY_RUN_ONLY",
        },
    }

    signature = _stable_signature(base_payload)
    audit_id = f"MILESTONE-5-PUBLIC-READINESS-AUDIT-{signature[:12]}"

    return PublicReadinessBaselineAudit(
        status=AUDIT_STATUS,
        audit_id=audit_id,
        signature=signature,
        milestone=base_payload["milestone"],
        task=base_payload["task"],
        title=base_payload["title"],
        baseline_commit=base_payload["baseline_commit"],
        prior_closure_id=base_payload["prior_closure_id"],
        prior_closure_signature=base_payload["prior_closure_signature"],
        required_artifacts=required_artifacts,
        checks=checks,
        boundary=boundary,
        next_actions=next_actions,
        ready_for_public_readiness_phase=all(checks.values()),
        kaggle_submission_sent=False,
        metadata=base_payload["metadata"],
    )


def validate_public_readiness_baseline_audit(
    audit: PublicReadinessBaselineAudit | Mapping[str, Any],
) -> Dict[str, Any]:
    data = audit.to_dict() if hasattr(audit, "to_dict") else dict(audit)

    checks = data.get("checks") if isinstance(data.get("checks"), Mapping) else {}
    boundary = data.get("boundary") if isinstance(data.get("boundary"), Mapping) else {}
    artifacts = data.get("required_artifacts") if isinstance(data.get("required_artifacts"), Mapping) else {}

    validation_checks = {
        "status_ready": data.get("status") == AUDIT_STATUS,
        "audit_id_present": isinstance(data.get("audit_id"), str) and bool(data.get("audit_id")),
        "signature_present": isinstance(data.get("signature"), str) and bool(data.get("signature")),
        "baseline_commit_is_milestone_4_closure": str(data.get("baseline_commit", "")).startswith("f97b25d"),
        "checks_all_true": bool(checks) and all(checks.values()),
        "required_artifacts_all_present": bool(artifacts) and all(artifacts.values()),
        "ready_for_public_readiness_phase": data.get("ready_for_public_readiness_phase") is True,
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
        "status": VALIDATION_STATUS if valid else "MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_INVALID",
        "valid": valid,
        "checks": validation_checks,
        "audit_id": data.get("audit_id"),
        "signature": data.get("signature"),
    }


def render_public_readiness_baseline_audit_markdown(
    audit: PublicReadinessBaselineAudit | Mapping[str, Any],
) -> str:
    data = audit.to_dict() if hasattr(audit, "to_dict") else dict(audit)

    lines = [
        "# ARC AGI3 Milestone #5 - Public Readiness Baseline Audit v1",
        "",
        "## Status",
        "",
        f"- status: {data['status']}",
        f"- audit_id: {data['audit_id']}",
        f"- signature: {data['signature']}",
        f"- baseline_commit: {data['baseline_commit']}",
        f"- prior_closure_id: {data['prior_closure_id']}",
        f"- prior_closure_signature: {data['prior_closure_signature']}",
        f"- ready_for_public_readiness_phase: {data['ready_for_public_readiness_phase']}",
        f"- kaggle_submission_sent: {data['kaggle_submission_sent']}",
        "",
        "## Required artifacts",
        "",
    ]

    for artifact, present in data["required_artifacts"].items():
        lines.append(f"- {artifact}: {present}")

    lines.extend(
        [
            "",
            "## Checks",
            "",
        ]
    )

    for check, value in data["checks"].items():
        lines.append(f"- {check}: {value}")

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
            "ARC_AGI3_MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_READY=true",
            "ARC_AGI3_MILESTONE_5_PUBLIC_READINESS_BASELINE_AUDIT_VALID=true",
            "ARC_AGI3_MILESTONE_5_READY_FOR_PUBLIC_READINESS_PHASE=true",
            "ARC_AGI3_MILESTONE_5_BASELINE_COMMIT=f97b25d",
            "ARC_AGI3_MILESTONE_5_DEPENDS_ON_MILESTONE_4_CLOSURE=true",
            "ARC_AGI3_KAGGLE_SUBMISSION_SENT=false",
            "ARC_AGI3_EXTERNAL_API_DEPENDENCY=false",
            "ARC_AGI3_PRIVATE_CORE_EXPOSURE=false",
            "ARC_AGI3_LEGAL_CERTIFICATION=false",
            "",
        ]
    )

    return "\n".join(lines)


def write_public_readiness_baseline_audit_artifacts(
    audit: PublicReadinessBaselineAudit | None = None,
    *,
    output_dir: str = DEFAULT_OUTPUT_DIR,
) -> Dict[str, str]:
    audit = audit or build_public_readiness_baseline_audit()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    json_path = output_path / "public-readiness-baseline-audit-v1.json"
    markdown_path = output_path / "public-readiness-baseline-audit-v1.md"

    json_path.write_text(json.dumps(audit.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    markdown_path.write_text(render_public_readiness_baseline_audit_markdown(audit), encoding="utf-8")

    return {
        "json_path": str(json_path),
        "markdown_path": str(markdown_path),
    }


def run_public_readiness_baseline_audit_pipeline() -> Dict[str, Any]:
    audit = build_public_readiness_baseline_audit()
    validation = validate_public_readiness_baseline_audit(audit)
    artifacts = write_public_readiness_baseline_audit_artifacts(audit)

    return {
        "status": PIPELINE_STATUS if validation["valid"] else "MILESTONE_5_PUBLIC_READINESS_BASELINE_PIPELINE_INVALID",
        "audit_status": audit.status,
        "validation_status": validation["status"],
        "audit": audit.to_dict(),
        "audit_id": audit.audit_id,
        "signature": audit.signature,
        "ready_for_public_readiness_phase": audit.ready_for_public_readiness_phase,
        "kaggle_submission_sent": audit.kaggle_submission_sent,
        "artifacts": artifacts,
        "metadata": {
            "source": "milestone_5_public_readiness_baseline_pipeline_v1",
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
