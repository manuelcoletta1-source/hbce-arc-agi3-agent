"""Milestone #18 Task 4 - Controlled Technical Candidate Generator Improvement Map v1.

This module creates a deterministic, local-only, planning-only improvement map
for the ARC-AGI3 candidate generator.

Boundary:
- no runtime execution authorization;
- no solver patch execution;
- no ranker runtime modification;
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


TASK_NAME = "MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1"
TASK_LABEL = "Controlled Technical Candidate Generator Improvement Map v1"
MILESTONE_NAME = "MILESTONE_18_CONTROLLED_TECHNICAL_SOLVER_IMPROVEMENT"

PREVIOUS_TASK = "MILESTONE_18_TASK_3_CONTROLLED_TECHNICAL_SOLVER_LIMITATION_INVENTORY_REVIEW_V1"
PREVIOUS_COMMIT = "ff72908"
PREVIOUS_SIGNATURE = "38A0F948AFF91AC9"

NEXT_STAGE = "MILESTONE_18_TASK_5_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_REVIEW_V1"

ARTIFACT_DIR = Path(
    "examples/milestone-18/controlled-technical-candidate-generator-improvement-map-v1"
)
DOCS_PATH = Path("docs/milestone-18-controlled-technical-candidate-generator-improvement-map-v1.md")


@dataclass(frozen=True)
class CandidateGeneratorImprovementItem:
    """A planning-only improvement item for the candidate generator."""

    item_id: str
    source_review_item: str
    source_limitation_id: str
    improvement_area: str
    limitation_confirmed: str
    controlled_improvement: str
    expected_evidence: str
    implementation_status: str
    blocked_actions: tuple[str, ...]
    review_required_before_implementation: bool
    implementation_authorized: bool


def _canonical_json(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def _signature(data: dict[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(data).encode("utf-8")).hexdigest()[:16].upper()


def build_candidate_generator_improvement_items() -> tuple[CandidateGeneratorImprovementItem, ...]:
    """Return the deterministic Task 4 improvement map items."""

    return (
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-1",
            source_review_item="M18-REV-1",
            source_limitation_id="M18-LIM-1",
            improvement_area="solver coverage",
            limitation_confirmed="Candidate generation must support broader transform hypotheses without pretending solver coverage is solved.",
            controlled_improvement="Map candidate families for color mapping, object transformation, symmetry, grid completion, and cross-family composition.",
            expected_evidence="Each candidate family must expose family_id, transform_hypothesis, input_observation_basis, expected_output_constraint, and rejection_reason fields.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "solver_runtime_patch",
                "candidate_generator_runtime_wiring",
                "real_evaluation_execution",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-2",
            source_review_item="M18-REV-2",
            source_limitation_id="M18-LIM-2",
            improvement_area="candidate generation",
            limitation_confirmed="Candidate generation needs structured hypothesis diversity, not a single brittle answer path.",
            controlled_improvement="Define a multi-candidate proposal map with deterministic ordering, family labels, confidence_hint, and evidence slots.",
            expected_evidence="Generated candidates must preserve deterministic order, candidate_id, family_id, transform_summary, and confidence_hint without claiming official score impact.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "candidate_generator_modification",
                "runtime_candidate_execution",
                "submission_candidate_generation",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-3",
            source_review_item="M18-REV-3",
            source_limitation_id="M18-LIM-3",
            improvement_area="ranker evidence",
            limitation_confirmed="Ranker evidence must receive structured candidate metadata without changing ranker behavior yet.",
            controlled_improvement="Map ranker-neutral evidence fields: observation_count, transform_specificity, contradiction_count, grid_consistency_notes, and fallback_reason.",
            expected_evidence="Candidate records must be inspectable by future ranker review while leaving ranker runtime untouched in Task 4.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "ranker_runtime_modification",
                "ranker_weight_change",
                "competitive_score_claim",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-4",
            source_review_item="M18-REV-4",
            source_limitation_id="M18-LIM-4",
            improvement_area="local diagnostics",
            limitation_confirmed="Candidate generator changes require local diagnostic visibility before any implementation.",
            controlled_improvement="Define a fixture-driven diagnostic matrix linking candidate families to local public-safe benchmark cases.",
            expected_evidence="Each mapped diagnostic must include fixture_id, family_under_test, expected_candidate_count, rejection_path_required, and regression_guard.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "diagnostic_runtime_execution",
                "hidden_dataset_access",
                "internet_during_eval",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-5",
            source_review_item="M18-REV-5",
            source_limitation_id="M18-LIM-5",
            improvement_area="submission discipline",
            limitation_confirmed="Candidate generation must not silently become submission generation.",
            controlled_improvement="Separate candidate proposal artifacts from submission artifacts with explicit real_submission_allowed=false gates.",
            expected_evidence="Artifacts must state no Kaggle upload, no manual upload, no submission.json production, and no official score claim.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "submission_json_creation",
                "manual_upload",
                "kaggle_submission",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
        CandidateGeneratorImprovementItem(
            item_id="M18-CGIM-6",
            source_review_item="M18-REV-6",
            source_limitation_id="M18-LIM-6",
            improvement_area="authorization boundary",
            limitation_confirmed="Task 4 may map improvements but must not authorize implementation.",
            controlled_improvement="Preserve hard authorization flags across map, artifacts, docs, and tests.",
            expected_evidence="All generated records must expose implementation_authorized=false, runtime_execution_allowed=false, and fail_closed_active=true.",
            implementation_status="PLANNING_ONLY_NOT_IMPLEMENTED",
            blocked_actions=(
                "implementation_authorization",
                "runtime_activation",
                "private_core_exposure",
            ),
            review_required_before_implementation=True,
            implementation_authorized=False,
        ),
    )


def build_boundary_controls() -> dict[str, bool]:
    """Return canonical Task 4 boundary controls."""

    return {
        "planning_only": True,
        "review_required": True,
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


def build_acceptance_gates(items: tuple[CandidateGeneratorImprovementItem, ...], controls: dict[str, bool]) -> tuple[dict[str, Any], ...]:
    """Build deterministic acceptance gates for the planning-only map."""

    gates: list[dict[str, Any]] = [
        {
            "gate_id": "M18-T4-GATE-001",
            "name": "previous_task_closed",
            "passed": PREVIOUS_TASK.endswith("_V1"),
        },
        {
            "gate_id": "M18-T4-GATE-002",
            "name": "previous_commit_present",
            "passed": PREVIOUS_COMMIT == "ff72908",
        },
        {
            "gate_id": "M18-T4-GATE-003",
            "name": "previous_signature_present",
            "passed": PREVIOUS_SIGNATURE == "38A0F948AFF91AC9",
        },
        {
            "gate_id": "M18-T4-GATE-004",
            "name": "six_improvement_items_mapped",
            "passed": len(items) == 6,
        },
        {
            "gate_id": "M18-T4-GATE-005",
            "name": "all_items_require_review",
            "passed": all(item.review_required_before_implementation for item in items),
        },
        {
            "gate_id": "M18-T4-GATE-006",
            "name": "no_item_authorizes_implementation",
            "passed": not any(item.implementation_authorized for item in items),
        },
    ]

    for key, expected in {
        "planning_only": True,
        "implementation_authorization_granted": False,
        "implementation_authorized": False,
        "implementation_blocked": True,
        "implementation_performed": False,
        "candidate_generator_modified": False,
        "solver_runtime_modified": False,
        "ranker_runtime_modified": False,
        "runtime_execution_allowed": False,
        "runtime_execution_performed": False,
        "real_evaluation_allowed": False,
        "real_submission_allowed": False,
        "manual_upload_allowed": False,
        "upload_performed": False,
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
                "gate_id": f"M18-T4-GATE-{len(gates) + 1:03d}",
                "name": key,
                "expected": expected,
                "actual": controls.get(key),
                "passed": controls.get(key) is expected,
            }
        )

    for item in items:
        gates.append(
            {
                "gate_id": f"M18-T4-GATE-{len(gates) + 1:03d}",
                "name": f"{item.item_id}_has_blocked_actions",
                "passed": bool(item.blocked_actions),
            }
        )
        gates.append(
            {
                "gate_id": f"M18-T4-GATE-{len(gates) + 1:03d}",
                "name": f"{item.item_id}_planning_only_status",
                "passed": item.implementation_status == "PLANNING_ONLY_NOT_IMPLEMENTED",
            }
        )

    return tuple(gates)


def build_candidate_generator_improvement_map() -> dict[str, Any]:
    """Build the complete deterministic Task 4 improvement map."""

    items = build_candidate_generator_improvement_items()
    controls = build_boundary_controls()
    gates = build_acceptance_gates(items, controls)
    gate_failures = [gate for gate in gates if not gate["passed"]]

    payload: dict[str, Any] = {
        "task": TASK_NAME,
        "task_label": TASK_LABEL,
        "milestone_18_name": MILESTONE_NAME,
        "status": f"{TASK_NAME}_READY",
        "validation": f"{TASK_NAME}_VALID" if not gate_failures else f"{TASK_NAME}_INVALID",
        "verdict": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_READY_NO_IMPLEMENTATION"
        if not gate_failures
        else "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_BLOCKED",
        "map_scope": "CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_ONLY",
        "previous_task": PREVIOUS_TASK,
        "previous_commit": PREVIOUS_COMMIT,
        "previous_signature": PREVIOUS_SIGNATURE,
        "next_stage": NEXT_STAGE,
        "candidate_generator_improvement_map_ready": not gate_failures,
        "candidate_generator_improvement_map_locked": not gate_failures,
        "candidate_generator_improvement_map_review_required": True,
        "implementation_allowed_now": False,
        "implementation_authorization_scope": "NOT_GRANTED",
        "item_count": len(items),
        "improvement_area_count": len({item.improvement_area for item in items}),
        "blocking_issue_count": len(gate_failures),
        "boundary_controls": controls,
        "improvement_items": [asdict(item) for item in items],
        "acceptance_gates": gates,
        "acceptance_gate_count": len(gates),
        "acceptance_gate_failure_count": len(gate_failures),
        "acceptance_gate_failures": gate_failures,
    }

    payload["signature"] = _signature(payload)
    payload["map_id"] = f"MILESTONE-18-TASK-4-CANDIDATE-GENERATOR-IMPROVEMENT-MAP-{payload['signature']}"
    return payload


def build_markdown_report(data: dict[str, Any]) -> str:
    """Build a reusable markdown report for docs and artifacts."""

    lines = [
        "# Milestone 18 Task 4 — Controlled Technical Candidate Generator Improvement Map v1",
        "",
        "## Status",
        "",
        f"- Task: `{data['task']}`",
        f"- Map ID: `{data['map_id']}`",
        f"- Signature: `{data['signature']}`",
        f"- Previous task: `{data['previous_task']}`",
        f"- Previous commit: `{data['previous_commit']}`",
        f"- Previous signature: `{data['previous_signature']}`",
        f"- Verdict: `{data['verdict']}`",
        f"- Next stage: `{data['next_stage']}`",
        "",
        "## Boundary",
        "",
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
        "## Improvement Map",
        "",
    ]

    for item in data["improvement_items"]:
        lines.extend(
            [
                f"### {item['item_id']} — {item['improvement_area']}",
                "",
                f"- Source review item: `{item['source_review_item']}`",
                f"- Source limitation: `{item['source_limitation_id']}`",
                f"- Confirmed limitation: {item['limitation_confirmed']}",
                f"- Controlled improvement: {item['controlled_improvement']}",
                f"- Expected evidence: {item['expected_evidence']}",
                f"- Implementation status: `{item['implementation_status']}`",
                f"- Review required before implementation: `{item['review_required_before_implementation']}`",
                f"- Implementation authorized: `{item['implementation_authorized']}`",
                "",
            ]
        )

    lines.extend(
        [
            "## Acceptance",
            "",
            f"- Acceptance gate count: `{data['acceptance_gate_count']}`",
            f"- Acceptance gate failures: `{data['acceptance_gate_failure_count']}`",
            f"- Blocking issue count: `{data['blocking_issue_count']}`",
            "",
            "Task 4 creates a controlled technical map only. It does not modify the solver, candidate generator runtime, ranker runtime, or submission pipeline.",
            "",
        ]
    )

    return "\n".join(lines)


def write_artifacts(
    artifact_dir: Path = ARTIFACT_DIR,
    docs_path: Path = DOCS_PATH,
) -> dict[str, Path]:
    """Write deterministic Task 4 artifacts."""

    data = build_candidate_generator_improvement_map()

    artifact_dir.mkdir(parents=True, exist_ok=True)
    docs_path.parent.mkdir(parents=True, exist_ok=True)

    json_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-v1.json"
    index_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-index-v1.json"
    manifest_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-manifest-v1.txt"
    markdown_path = artifact_dir / "milestone-18-controlled-technical-candidate-generator-improvement-map-v1.md"

    json_text = json.dumps(data, indent=2, ensure_ascii=False)
    json_path.write_text(json_text + "\n", encoding="utf-8")

    index = {
        "artifact_type": "MILESTONE_18_TASK_4_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_INDEX",
        "task": data["task"],
        "map_id": data["map_id"],
        "signature": data["signature"],
        "previous_commit": data["previous_commit"],
        "previous_signature": data["previous_signature"],
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
        "MILESTONE_18_TASK_4_CONTROLLED_TECHNICAL_CANDIDATE_GENERATOR_IMPROVEMENT_MAP_V1_MANIFEST",
        f"task={data['task']}",
        f"map_id={data['map_id']}",
        f"signature={data['signature']}",
        f"previous_task={data['previous_task']}",
        f"previous_commit={data['previous_commit']}",
        f"previous_signature={data['previous_signature']}",
        f"next_stage={data['next_stage']}",
        f"item_count={data['item_count']}",
        f"acceptance_gate_count={data['acceptance_gate_count']}",
        f"acceptance_gate_failure_count={data['acceptance_gate_failure_count']}",
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
    result = build_candidate_generator_improvement_map()
    print(f"{TASK_NAME}_PIPELINE_READY")
    print(result["status"])
    print(result["validation"])
    print(result["signature"])
    print(result["previous_commit"])
    print(result["verdict"])
    print(result["next_stage"])
