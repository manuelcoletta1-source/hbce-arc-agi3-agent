"""Milestone 38 Task 4 Kaggle competitive agent and productization boundary validation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_38_kaggle_competitive_agent_productization import (
    run_milestone_38_kaggle_competitive_agent_productization_implementation,
    validate_milestone_38_kaggle_competitive_agent_productization_report,
)

TASK_ID = "MILESTONE_38_TASK_4_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_VALIDATION_V1"
SOURCE_IMPLEMENTATION_TASK_ID = "MILESTONE_38_TASK_3_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_IMPLEMENTATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_38_SCOPE_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
HARNESS_MODE_ID = "ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
VALIDATION_REVISION = "MILESTONE_38_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_VALIDATION_V1"
VALIDATION_ID = "MILESTONE-38-ARC-AGI3-KAGGLE-COMPETITIVE-AGENT-PRODUCTIZATION-VALIDATION-FDC8E31DA830C4A4"
NEXT_STAGE = "MILESTONE_38_TASK_5_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_REGRESSION_INTEGRATION_V1"
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 4
GENERATED_ARTIFACT_COUNT = 5
VALIDATION_CASE_COUNT = 17

ARTIFACT_DIR = Path("examples/milestone-38/hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-validation-v1")
DOC_PATH = Path("docs/milestone-38-task-4-hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-validation-v1.md")


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()[:16]


TASK_4_SIGNATURE = _digest(
    {
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
    }
)
VALIDATION_SIGNATURE = _digest(
    {
        "validation_id": VALIDATION_ID,
        "task_4_signature": TASK_4_SIGNATURE,
        "case_count": VALIDATION_CASE_COUNT,
        "next_stage": NEXT_STAGE,
    }
)


def _case(case_id: str, description: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "description": description,
        "passed": bool(passed),
        "evidence": evidence,
    }


def build_milestone_38_kaggle_competitive_agent_productization_validation_cases(
    source_report: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    source = source_report or run_milestone_38_kaggle_competitive_agent_productization_implementation()
    return [
        _case("M34-T4-001", "Source implementation report validates", validate_milestone_38_kaggle_competitive_agent_productization_report(source), source.get("task_id")),
        _case("M34-T4-002", "Source implementation task id is bound", source.get("task_id") == SOURCE_IMPLEMENTATION_TASK_ID, source.get("task_id")),
        _case("M34-T4-003", "Selected objective remains locked", source.get("selected_objective_id") == SELECTED_OBJECTIVE_ID, source.get("selected_objective_id")),
        _case("M34-T4-004", "Scope lock remains bound", source.get("scope_lock_id") == SCOPE_LOCK_ID, source.get("scope_lock_id")),
        _case("M34-T4-005", "Harness mode remains bound", source.get("harness_mode_id") == HARNESS_MODE_ID, source.get("harness_mode_id")),
        _case("M34-T4-006", "Implementation status is READY", source.get("implementation_status") == "READY", source.get("implementation_status")),
        _case("M34-T4-007", "Implementation passed", source.get("implementation_passed") is True, source.get("implementation_passed")),
        _case("M34-T4-008", "Replay evaluation harness boundary is present", source.get("kaggle_competitive_agent_productization_boundary") is True, source.get("kaggle_competitive_agent_productization_boundary")),
        _case("M34-T4-009", "Replayable event trace is required", source.get("replayable_event_trace_required") is True, source.get("replayable_event_trace_required")),
        _case("M34-T4-010", "Local evaluation record is required", source.get("local_evaluation_record_required") is True, source.get("local_evaluation_record_required")),
        _case("M34-T4-011", "Regression snapshot is required", source.get("regression_snapshot_required") is True, source.get("regression_snapshot_required")),
        _case("M34-T4-012", "Audit artifact is required", source.get("audit_artifact_required") is True, source.get("audit_artifact_required")),
        _case("M34-T4-013", "Evaluation remains technical only", source.get("technical_evaluation_only") is True, source.get("technical_evaluation_only")),
        _case("M34-T4-014", "Legal certification remains denied", source.get("legal_certification") is False, source.get("legal_certification")),
        _case("M34-T4-015", "Kaggle score claim remains denied", source.get("kaggle_score_claim") is False, source.get("kaggle_score_claim")),
        _case("M34-T4-016", "Official benchmark certification remains denied", source.get("official_benchmark_certification") is False, source.get("official_benchmark_certification")),
        _case(
            "M34-T4-017",
            "Validation next stage advances to regression integration",
            NEXT_STAGE.endswith("REGRESSION_INTEGRATION_V1"),
            NEXT_STAGE,
        ),
    ]


def run_milestone_38_kaggle_competitive_agent_productization_validation() -> dict[str, Any]:
    source = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    cases = build_milestone_38_kaggle_competitive_agent_productization_validation_cases(source)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count

    record = source.get("replay_evaluation_record", {})
    local_record = record.get("local_evaluation_record", {})
    snapshot = record.get("regression_snapshot", {})
    audit = record.get("audit_artifact", {})

    return {
        "ready": fail_count == 0,
        "task_id": TASK_ID,
        "source_implementation_task_id": SOURCE_IMPLEMENTATION_TASK_ID,
        "source_implementation_status": source.get("implementation_status"),
        "source_implementation_passed": source.get("implementation_passed"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "validation_revision": VALIDATION_REVISION,
        "task_4_signature": TASK_4_SIGNATURE,
        "validation_id": VALIDATION_ID,
        "validation_signature": VALIDATION_SIGNATURE,
        "validation_status": "VALID" if fail_count == 0 else "INVALID",
        "validation_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "validation_passed": fail_count == 0,
        "kaggle_competitive_agent_productization_boundary": source.get("kaggle_competitive_agent_productization_boundary"),
        "replayable_event_trace_required": source.get("replayable_event_trace_required"),
        "local_evaluation_record_required": source.get("local_evaluation_record_required"),
        "regression_snapshot_required": source.get("regression_snapshot_required"),
        "audit_artifact_required": source.get("audit_artifact_required"),
        "technical_evaluation_only": source.get("technical_evaluation_only"),
        "legal_certification": source.get("legal_certification"),
        "kaggle_score_claim": source.get("kaggle_score_claim"),
        "official_benchmark_certification": source.get("official_benchmark_certification"),
        "network_access_allowed": source.get("network_access_allowed"),
        "shell_execution_allowed": source.get("shell_execution_allowed"),
        "repository_mutation_allowed": source.get("repository_mutation_allowed"),
        "replay_id": record.get("replay_id"),
        "local_evaluation_id": local_record.get("evaluation_id"),
        "regression_snapshot_id": snapshot.get("snapshot_id"),
        "source_runtime_event_count": snapshot.get("source_runtime_event_count"),
        "source_runtime_trace_fingerprint": snapshot.get("source_runtime_trace_fingerprint"),
        "audit_id": audit.get("audit_id"),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
        "cases": cases,
        "source_implementation_report": source,
    }


def validate_milestone_38_kaggle_competitive_agent_productization_validation_report(report: dict[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_implementation_task_id") != SOURCE_IMPLEMENTATION_TASK_ID:
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_implementation_passed") is not True:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("validation_status") != "VALID":
        return False
    if report.get("validation_case_count") != VALIDATION_CASE_COUNT:
        return False
    if report.get("pass_count") != VALIDATION_CASE_COUNT or report.get("fail_count") != 0:
        return False
    if report.get("validation_passed") is not True:
        return False
    if report.get("legal_certification") is not False:
        return False
    if report.get("kaggle_score_claim") is not False:
        return False
    if report.get("official_benchmark_certification") is not False:
        return False
    if report.get("network_access_allowed") is not False:
        return False
    if report.get("shell_execution_allowed") is not False:
        return False
    if report.get("repository_mutation_allowed") is not False:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    if len(report.get("cases", [])) != VALIDATION_CASE_COUNT:
        return False
    return all(case.get("passed") is True for case in report["cases"])


def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 38 Task 4 Runtime Model Routing Boundary Validation Report",
        "",
        f"- Validation ID: `{report['validation_id']}`",
        f"- Validation Status: `{report['validation_status']}`",
        f"- Cases: `{report['pass_count']}/{report['validation_case_count']}`",
        f"- Failures: `{report['fail_count']}`",
        "",
        "## Cases",
        "",
    ]
    for case in report["cases"]:
        lines.append(f"- `{case['case_id']}` `{_bool(case['passed'])}` - {case['description']}")
    lines.append("")
    return "\n".join(lines)


def _doc(report: dict[str, Any]) -> str:
    return f"""# Milestone 38 Task 4 - HBCE ARC AGI3 Interactive Runtime Runtime Model Routing Boundary Validation v1

MILESTONE_38_TASK_4_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_VALIDATION_READY={_bool(report['ready'])}
MILESTONE_38_TASK_4_TASK_ID={report['task_id']}
MILESTONE_38_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID={report['source_implementation_task_id']}
MILESTONE_38_TASK_4_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}
MILESTONE_38_TASK_4_SOURCE_IMPLEMENTATION_PASSED={_bool(report['source_implementation_passed'])}
MILESTONE_38_TASK_4_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_38_TASK_4_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_38_TASK_4_HARNESS_MODE_ID={report['harness_mode_id']}
MILESTONE_38_TASK_4_VALIDATION_REVISION={report['validation_revision']}
MILESTONE_38_TASK_4_TASK_4_SIGNATURE={report['task_4_signature']}
MILESTONE_38_TASK_4_VALIDATION_ID={report['validation_id']}
MILESTONE_38_TASK_4_VALIDATION_SIGNATURE={report['validation_signature']}
MILESTONE_38_TASK_4_VALIDATION_STATUS={report['validation_status']}
MILESTONE_38_TASK_4_VALIDATION_CASE_COUNT={report['validation_case_count']}
MILESTONE_38_TASK_4_PASS_COUNT={report['pass_count']}
MILESTONE_38_TASK_4_FAIL_COUNT={report['fail_count']}
MILESTONE_38_TASK_4_VALIDATION_PASSED={_bool(report['validation_passed'])}
MILESTONE_38_TASK_4_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY={_bool(report['kaggle_competitive_agent_productization_boundary'])}
MILESTONE_38_TASK_4_REPLAYABLE_EVENT_TRACE_REQUIRED={_bool(report['replayable_event_trace_required'])}
MILESTONE_38_TASK_4_LOCAL_EVALUATION_RECORD_REQUIRED={_bool(report['local_evaluation_record_required'])}
MILESTONE_38_TASK_4_REGRESSION_SNAPSHOT_REQUIRED={_bool(report['regression_snapshot_required'])}
MILESTONE_38_TASK_4_AUDIT_ARTIFACT_REQUIRED={_bool(report['audit_artifact_required'])}
MILESTONE_38_TASK_4_TECHNICAL_EVALUATION_ONLY={_bool(report['technical_evaluation_only'])}
MILESTONE_38_TASK_4_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_38_TASK_4_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_38_TASK_4_OFFICIAL_BENCHMARK_CERTIFICATION={_bool(report['official_benchmark_certification'])}
MILESTONE_38_TASK_4_NETWORK_ACCESS_ALLOWED={_bool(report['network_access_allowed'])}
MILESTONE_38_TASK_4_SHELL_EXECUTION_ALLOWED={_bool(report['shell_execution_allowed'])}
MILESTONE_38_TASK_4_REPOSITORY_MUTATION_ALLOWED={_bool(report['repository_mutation_allowed'])}
MILESTONE_38_TASK_4_REPLAY_ID={report['replay_id']}
MILESTONE_38_TASK_4_LOCAL_EVALUATION_ID={report['local_evaluation_id']}
MILESTONE_38_TASK_4_REGRESSION_SNAPSHOT_ID={report['regression_snapshot_id']}
MILESTONE_38_TASK_4_SOURCE_RUNTIME_EVENT_COUNT={report['source_runtime_event_count']}
MILESTONE_38_TASK_4_SOURCE_RUNTIME_TRACE_FINGERPRINT={report['source_runtime_trace_fingerprint']}
MILESTONE_38_TASK_4_AUDIT_ID={report['audit_id']}
MILESTONE_38_TASK_4_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_38_TASK_4_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_38_TASK_4_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_38_TASK_4_NEXT_STAGE={report['next_stage']}

## Validated Boundary

This validation confirms the Milestone 38 Kaggle competitive agent and productization boundary.

It validates:
- source implementation readiness;
- objective and scope lock continuity;
- replayable event trace requirement;
- local evaluation record requirement;
- regression snapshot requirement;
- audit artifact requirement;
- technical-only evaluation limits.

No legal certification is produced.
No Kaggle score claim is produced.
No official benchmark certification is produced.
"""


def write_milestone_38_task_4_artifacts() -> dict[str, str]:
    report = run_milestone_38_kaggle_competitive_agent_productization_validation()
    if not validate_milestone_38_kaggle_competitive_agent_productization_validation_report(report):
        raise ValueError("Milestone 38 Task 4 Kaggle competitive agent and productization validation report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases = ARTIFACT_DIR / "task-4-kaggle-competitive-agent-and-productization-validation-cases.json"
    report_json = ARTIFACT_DIR / "task-4-kaggle-competitive-agent-and-productization-validation-report.json"
    report_md = ARTIFACT_DIR / "task-4-kaggle-competitive-agent-and-productization-validation-report.md"
    index = ARTIFACT_DIR / "task-4-index.txt"
    manifest = ARTIFACT_DIR / "task-4-manifest.json"

    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text(
        "\n".join(
            [
                "MILESTONE_38_TASK_4_ARTIFACT_INDEX",
                cases.name,
                report_json.name,
                report_md.name,
                index.name,
                manifest.name,
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    manifest.write_text(
        json.dumps(
            {
                "task_id": TASK_ID,
                "validation_id": VALIDATION_ID,
                "validation_signature": VALIDATION_SIGNATURE,
                "artifact_count": GENERATED_ARTIFACT_COUNT,
                "artifacts": [cases.name, report_json.name, report_md.name, index.name, manifest.name],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    DOC_PATH.write_text(_doc(report), encoding="utf-8")
    return {
        "cases": cases.as_posix(),
        "report_json": report_json.as_posix(),
        "report_md": report_md.as_posix(),
        "index": index.as_posix(),
        "manifest": manifest.as_posix(),
        "doc": DOC_PATH.as_posix(),
    }


def main() -> None:
    write_milestone_38_task_4_artifacts()
    report = run_milestone_38_kaggle_competitive_agent_productization_validation()
    markers = {
        "MILESTONE_38_TASK_4_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_VALIDATION_READY": report["ready"],
        "MILESTONE_38_TASK_4_TASK_ID": report["task_id"],
        "MILESTONE_38_TASK_4_SOURCE_IMPLEMENTATION_TASK_ID": report["source_implementation_task_id"],
        "MILESTONE_38_TASK_4_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_38_TASK_4_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_38_TASK_4_HARNESS_MODE_ID": report["harness_mode_id"],
        "MILESTONE_38_TASK_4_VALIDATION_ID": report["validation_id"],
        "MILESTONE_38_TASK_4_VALIDATION_STATUS": report["validation_status"],
        "MILESTONE_38_TASK_4_VALIDATION_CASE_COUNT": report["validation_case_count"],
        "MILESTONE_38_TASK_4_PASS_COUNT": report["pass_count"],
        "MILESTONE_38_TASK_4_FAIL_COUNT": report["fail_count"],
        "MILESTONE_38_TASK_4_VALIDATION_PASSED": report["validation_passed"],
        "MILESTONE_38_TASK_4_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_38_TASK_4_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_38_TASK_4_OFFICIAL_BENCHMARK_CERTIFICATION": report["official_benchmark_certification"],
        "MILESTONE_38_TASK_4_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")


if __name__ == "__main__":
    main()
