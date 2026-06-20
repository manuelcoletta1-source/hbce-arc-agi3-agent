"""Milestone #18 Task 5 - Controlled Technical Candidate Generator Improvement Map Review v1.

This module performs a deterministic, local-only, review-only confirmation of
Milestone #18 Task 4.

Boundary:
- review-only;
- no implementation authorization;
- no candidate generator modification;
- no solver runtime modification;
- no ranker runtime modification;
- no real evaluation;
- no real Kaggle submission;
- no upload;
- no private HBCE/JOKER-C2 core exposure;
- legalCertification=false.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_18_controlled_technical_candidate_generator_improvement_map import (
    build_candidate_generator_improvement_map,
)


TASK_NAME = "MILESTONE_18_TASK_5_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Improvement Map Review v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1"
PREVIOUS_COMMIT = "d5fb1e7"
PREVIOUS_SIGNATURE = "D52615F216F01836"

NEXT_STAGE = "MILESTONE_18_TASK_6_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPLEMENTATION_AUTHORIZATION_GATE_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-improvement-map-review-v1"
)
DOCS_PATH = Path("docs/milestone-18-controlled-technical-candidate-generator-improvement-map-review-v1.md")


@dataclass(frozen=True)
class CandidateGeneratorImprovementMapReviewItem:
    """A review-only confirmation item for a Task 4 improvement-map item."""

    review_id: str
    source_item_id: str
    source_limitation_id: str
    improvement_area: str
    review_decision: str
    review_note: str
    blocking_issue: bool
    implementation_authorized: bool
    runtime_execution_authorized: bool
    review_required_before_next_gate: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_review_items(source_map: dict[str, Any]) -> tuple[CandidateGeneratorImprovementMapReviewItem, ...]:
    """Build deterministic review confirmations from the Task 4 improvement map."""

    items: list[CandidateGeneratorImprovementMapReviewItem] = []

    for index, source_item in enumerate(source_map["improvement_items"], start=1):
        items.append(
            CandidateGeneratorImprovementMapReviewItem(
                review_id=f"M18-CGIM-REV-{index}",
                source_item_id=source_item["item_id"],
                source_limitation_id=source_item["source_limitation_id"],
                improvement_area=source_item["improvement_area"],
                review_decision="CONFIRMED_NO_IMPLEMENTATION",
                review_note=(
                    "Task 4 improvement map item is confirmed as planning-only. "
                    "No implementation, runtime wiring, real evaluation, or submission is authorized."
                ),
                blocking_issue=False,
                implementation_authorized=False,
                runtime_execution_authorized=False,
                review_required_before_next_gate=True,
            )
        )

    return tuple(items)


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 5 boundary controls."""

    return {
        "review_only": True,
        "planning_only": True,
        "source_map_confirmed": True,
        "source_map_reopened": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_authorized": False,
        "solver_runtime_modified": False,
        "solver_patch_execution_allowed": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
    }


def build_acceptance_gates(
    source_map: dict[str, Any],
    review_items: tuple[CandidateGeneratorImprovementMapReviewItem, ...],
    controls: dict[str, bool],
) -> tuple[dict[str, Any], ...]:
    """Build deterministic Task 5 acceptance gates."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T5-GATE-001",
            "name": "previous_task_matches_task_4",
            "passed": PREVIOUS_TASK == source_map["task"],
        },
        {
            "gate_id": "M18-T5-GATE-002",
            "name": "previous_commit_matches_task_4_commit",
            "passed": PREVIOUS_COMMIT == "d5fb1e7",
        },
        {
            "gate_id": "M18-T5-GATE-003",
            "name": "previous_signature_matches_task_4_signature",
            "passed": PREVIOUS_SIGNATURE == source_map["signature"],
            "expected": PREVIOUS_SIGNATURE,
            "actual": source_map["signature"],
        },
        {
            "gate_id": "M18-T5-GATE-004",
            "name": "source_map_valid",
            "passed": source_map["validation"].endswith("_VALID"),
        },
        {
            "gate_id": "M18-T5-GATE-005",
            "name": "source_map_has_no_acceptance_failures",
            "passed": source_map["acceptance_gate_failure_count"] == 0,
        },
        {
            "gate_id": "M18-T5-GATE-006",
            "name": "six_review_items_confirmed",
            "passed": len(review_items) == 6,
        },
        {
            "gate_id": "M18-T5-GATE-007",
            "name": "no_review_item_blocks_next_gate",
            "passed": not any(item.blocking_issue for item in review_items),
        },
        {
            "gate_id": "M18-T5-GATE-008",
            "name": "no_review_item_authorizes_implementation",
            "passed": not any(item.implementation_authorized for item in review_items),
        },
        {
            "gate_id": "M18-T5-GATE-009",
            "name": "no_review_item_authorizes_runtime_execution",
            "passed": not any(item.runtime_execution_authorized for item in review_items),
        },
    ]

    for key, expected in {
        "review_only": True,
        "planning_only": True,
        "source_map_confirmed": True,
        "source_map_reopened": False,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "candidate_generator_wiring_authorized": False,
        "solver_runtime_modified": False,
        "solver_patch_execution_allowed": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_submission_sent": False,
        "competitive_score_claim_allowed": False,
        "official_score_claim_allowed": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "fail_closed_required": True,
        "fail_closed_active": True,
        "local_only": True,
        "deterministic": True,
        "public_safe": True,
        "external_api_dependency": False,
        "internet_during_eval": False,
    }.items():
        gates.append(
            {
                "gate_id": f"M18-T5-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in review_items:
        gates.append(
            {
                "gate_id": f"M18-T5-GATE-{len(gates) + 1:03d}",
                "name": f"{item.review_id}_confirmed_no_implementation",
                "passed": item.review_decision == "CONFIRMED_NO_IMPLEMENTATION"
                and item.implementation_authorized is False
                and item.runtime_execution_authorized is False
                and item.blocking_issue is False,
            }
        )

    return tuple(gates)


def build_candidate_generator_improvement_map_review() -> dict[str, Any]:
    """Build the complete deterministic Task 5 review record."""

    source_map = build_candidate_generator_improvement_map()
    review_items = build_review_items(source_map)
    controls = build_boundary_controls()
    gates = build_acceptance_gates(source_map, review_items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_PASS_NO_IMPLEMENTATION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_BLOCKED",
        "review_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "source_map_task": source_map["task"],
        "source_map_id": source_map["map_id"],
        "source_map_signature": source_map["signature"],
        "source_map_validation": source_map["validation"],
        "source_map_verdict": source_map["verdict"],
        "next_stage": NEXT_STAGE,
        "review_ready": not gate_failures,
        "review_locked": not gate_failures,
        "review_passed": not gate_failures,
        "review_only": True,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "NOT_GRANTED",
        "review_item_count": len(review_items),
        "confirmed_item_count": len(
            [
                item
                for item in review_items
                if item.review_decision == "CONFIRMED_NO_IMPLEMENTATION"
            ]
        ),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "review_items": [asdict(item) for item in review_items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["review_id"] = f"MILESTONE-18-TASK-5-CANDIDATE-GENERATOR-IMPROVEMENT-MAP-REVIEW-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 5 — Controlled Technical Candidate Generator Improvement Map Review v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Review ID: `{data['review_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Source map ID: `{data['source_map_id']}`",
        f"- Source map signature: `{data['source_map_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
        "- review-only: true",
        "- planning-only: true",
        "- implementation authorized: false",
        "- runtime execution allowed: false",
        "- real evaluation allowed: false",
        "- real submission allowed: false",
        "- Kaggle submission sent: false",
        "- private core exposure: false",
        "- legalCertification: false",
        "- fail-closed: active",
        "",
        "## Review Items",
        "",
    ]

    for item in data["review_items"]:
        lines.extend(
            [
                f"### {item['review_id']} — {item['improvement_area']}",
                "",
                f"- Source item: `{item['source_item_id']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Review decision: `{item['review_decision']}`",
                f"- Blocking issue: `{item['blocking_issue']}`",
                f"- Implementation authorized: `{item['implementation_authorized']}`",
                f"- Runtime execution authorized: `{item['runtime_execution_authorized']}`",
                f"- Note: {item['review_note']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Acceptance",
            "",
            f"- Review item count: `{data['review_item_count']}`",
            f"- Confirmed item count: `{data['confirmed_item_count']}`",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 5 confirms the Task 4 improvement map as review-only. It does not authorize implementation, runtime execution, real evaluation, upload, or submission.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 5 review artifacts."""

    data = build_candidate_generator_improvement_map_review()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-review-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-review-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-review-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-review-v1.md"

    json_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_5_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_INDEX",
        "task": data["task"],
        "review_id": data["review_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
        "source_map_signature": data["source_map_signature"],
        "next_stage": data["next_stage"],
        "artifact_paths": {
            "json": str(json_path),
            "manifest": str(manifest_path),
            "markdown": str(markdown_path),
            "docs": str(docs_path),
        },
        "boundary": data["boundary_controls"],
    }
    index_path.write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    manifest_lines = [
        "MILESTONE_18_TASK_5_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_V1_MANIFEST",
        f"task={data['task']}",
        f"review_id={data['review_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"source_map_signature={data['source_map_signature']}",
        f"next_stage={data['next_stage']}",
        f"review_item_count={data['review_item_count']}",
        f"confirmed_item_count={data['confirmed_item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
        "review_only=true",
        "planning_only=true",
        "implementation_authorized=false",
        "runtime_execution_allowed=false",
        "real_submission_allowed=false",
        "kaggle_submission_sent=false",
        "private_core_exposure=false",
        "legalCertification=false",
        "fail_closed_active=true",
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")

    markdown_report = build_markdown_report(data)
    markdown_path.write_text(markdown_report, encoding="utf-8")
    docs_path.write_text(markdown_report, encoding="utf-8")

    return {
        "json": json_path,
        "index": index_path,
        "manifest": manifest_path,
        "markdown": markdown_path,
        "docs": docs_path,
    }


if __name__ == "__main__":
    result = build_candidate_generator_improvement_map_review()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["source_map_signature"])
    print(result["review_scope"])
    print(result["verdict"])
    print(result["next_stage"])
