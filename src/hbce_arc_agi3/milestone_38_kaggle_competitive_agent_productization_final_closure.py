"""Milestone 38 Task 6 Kaggle competitive agent and productization boundary final closure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_38_kaggle_competitive_agent_productization_regression_integration import (
    run_milestone_38_kaggle_competitive_agent_productization_regression_integration,
    validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report,
)

TASK_ID = "MILESTONE_38_TASK_6_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_FINAL_CLOSURE_V1"
SOURCE_REGRESSION_TASK_ID = "MILESTONE_38_TASK_5_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_REGRESSION_INTEGRATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_38_SCOPE_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
HARNESS_MODE_ID = "ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
FINAL_CLOSURE_REVISION = "MILESTONE_38_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_FINAL_CLOSURE_V1"
CLOSURE_ID = "MILESTONE-38-ARC-AGI3-KAGGLE-COMPETITIVE-AGENT-PRODUCTIZATION-FINAL-CLOSURE-FDC8E31DA830C4A4"
NEXT_STAGE = "MILESTONE_39_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1"
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 6
GENERATED_ARTIFACT_COUNT = 5
CLOSURE_CASE_COUNT = 16

ARTIFACT_DIR = Path("examples/milestone-38/hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-final-closure-v1")
DOC_PATH = Path("docs/milestone-38-task-6-hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-final-closure-v1.md")


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()[:16]


TASK_6_SIGNATURE = _digest(
    {
        "task_id": TASK_ID,
        "source_regression_task_id": SOURCE_REGRESSION_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
    }
)
CLOSURE_SIGNATURE = _digest(
    {
        "closure_id": CLOSURE_ID,
        "task_6_signature": TASK_6_SIGNATURE,
        "case_count": CLOSURE_CASE_COUNT,
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


def build_milestone_38_kaggle_competitive_agent_productization_final_closure_cases(
    integration_report: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    source = integration_report or run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    return [
        _case("M34-T6-001", "Source regression integration report validates", validate_milestone_38_kaggle_competitive_agent_productization_regression_integration_report(source), source.get("task_id")),
        _case("M34-T6-002", "Source regression task id is bound", source.get("task_id") == SOURCE_REGRESSION_TASK_ID, source.get("task_id")),
        _case("M34-T6-003", "Source integration status is VALID", source.get("integration_status") == "VALID", source.get("integration_status")),
        _case("M34-T6-004", "Source integration passed", source.get("integration_passed") is True, source.get("integration_passed")),
        _case("M34-T6-005", "Selected objective remains locked", source.get("selected_objective_id") == SELECTED_OBJECTIVE_ID, source.get("selected_objective_id")),
        _case("M34-T6-006", "Scope lock remains bound", source.get("scope_lock_id") == SCOPE_LOCK_ID, source.get("scope_lock_id")),
        _case("M34-T6-007", "Harness mode remains bound", source.get("harness_mode_id") == HARNESS_MODE_ID, source.get("harness_mode_id")),
        _case("M34-T6-008", "Replay harness boundary remains true", source.get("kaggle_competitive_agent_productization_boundary") is True, source.get("kaggle_competitive_agent_productization_boundary")),
        _case("M34-T6-009", "Replayable event trace remains required", source.get("replayable_event_trace_required") is True, source.get("replayable_event_trace_required")),
        _case("M34-T6-010", "Local evaluation record remains required", source.get("local_evaluation_record_required") is True, source.get("local_evaluation_record_required")),
        _case("M34-T6-011", "Regression snapshot remains required", source.get("regression_snapshot_required") is True, source.get("regression_snapshot_required")),
        _case("M34-T6-012", "Audit artifact remains required", source.get("audit_artifact_required") is True, source.get("audit_artifact_required")),
        _case("M34-T6-013", "Regression event trace remains bound", source.get("regression_event_count") == 4, source.get("regression_event_count")),
        _case("M34-T6-014", "Legal certification remains denied", source.get("legal_certification") is False, source.get("legal_certification")),
        _case("M34-T6-015", "Kaggle and benchmark claims remain denied", source.get("kaggle_score_claim") is False and source.get("official_benchmark_certification") is False, {"kaggle": source.get("kaggle_score_claim"), "benchmark": source.get("official_benchmark_certification")}),
        _case("M34-T6-016", "Milestone 38 closes into Milestone 38 governed opening", NEXT_STAGE == "MILESTONE_39_TASK_1_GOVERNED_OPENING_WITH_TASK_BUDGET_V1", NEXT_STAGE),
    ]


def run_milestone_38_kaggle_competitive_agent_productization_final_closure() -> dict[str, Any]:
    source = run_milestone_38_kaggle_competitive_agent_productization_regression_integration()
    cases = build_milestone_38_kaggle_competitive_agent_productization_final_closure_cases(source)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count

    return {
        "ready": fail_count == 0,
        "task_id": TASK_ID,
        "source_regression_task_id": SOURCE_REGRESSION_TASK_ID,
        "source_integration_status": source.get("integration_status"),
        "source_integration_passed": source.get("integration_passed"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "final_closure_revision": FINAL_CLOSURE_REVISION,
        "task_6_signature": TASK_6_SIGNATURE,
        "closure_id": CLOSURE_ID,
        "closure_signature": CLOSURE_SIGNATURE,
        "closure_status": "CLOSED" if fail_count == 0 else "OPEN",
        "closure_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "closure_passed": fail_count == 0,
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
        "regression_event_count": source.get("regression_event_count"),
        "regression_event_trace_fingerprint": source.get("regression_event_trace_fingerprint"),
        "replay_id": source.get("replay_id"),
        "local_evaluation_id": source.get("local_evaluation_id"),
        "regression_snapshot_id": source.get("regression_snapshot_id"),
        "audit_id": source.get("audit_id"),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
        "cases": cases,
        "source_regression_integration_report": source,
    }


def validate_milestone_38_kaggle_competitive_agent_productization_final_closure_report(report: dict[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_regression_task_id") != SOURCE_REGRESSION_TASK_ID:
        return False
    if report.get("source_integration_status") != "VALID":
        return False
    if report.get("source_integration_passed") is not True:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("closure_status") != "CLOSED":
        return False
    if report.get("closure_case_count") != CLOSURE_CASE_COUNT:
        return False
    if report.get("pass_count") != CLOSURE_CASE_COUNT or report.get("fail_count") != 0:
        return False
    if report.get("closure_passed") is not True:
        return False
    if report.get("regression_event_count") != 4:
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
    if len(report.get("cases", [])) != CLOSURE_CASE_COUNT:
        return False
    return all(case.get("passed") is True for case in report["cases"])


def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 38 Task 6 Runtime Model Routing Boundary Final Closure Report",
        "",
        f"- Closure ID: `{report['closure_id']}`",
        f"- Closure Status: `{report['closure_status']}`",
        f"- Cases: `{report['pass_count']}/{report['closure_case_count']}`",
        f"- Failures: `{report['fail_count']}`",
        f"- Regression Event Trace Fingerprint: `{report['regression_event_trace_fingerprint']}`",
        "",
        "## Cases",
        "",
    ]
    for case in report["cases"]:
        lines.append(f"- `{case['case_id']}` `{_bool(case['passed'])}` - {case['description']}")
    lines.append("")
    return "\n".join(lines)


def _doc(report: dict[str, Any]) -> str:
    return f"""# Milestone 38 Task 6 - HBCE ARC AGI3 Interactive Runtime Runtime Model Routing Boundary Final Closure v1

MILESTONE_38_TASK_6_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_FINAL_CLOSURE_READY={_bool(report['ready'])}
MILESTONE_38_TASK_6_TASK_ID={report['task_id']}
MILESTONE_38_TASK_6_SOURCE_REGRESSION_TASK_ID={report['source_regression_task_id']}
MILESTONE_38_TASK_6_SOURCE_INTEGRATION_STATUS={report['source_integration_status']}
MILESTONE_38_TASK_6_SOURCE_INTEGRATION_PASSED={_bool(report['source_integration_passed'])}
MILESTONE_38_TASK_6_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_38_TASK_6_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_38_TASK_6_HARNESS_MODE_ID={report['harness_mode_id']}
MILESTONE_38_TASK_6_FINAL_CLOSURE_REVISION={report['final_closure_revision']}
MILESTONE_38_TASK_6_TASK_6_SIGNATURE={report['task_6_signature']}
MILESTONE_38_TASK_6_CLOSURE_ID={report['closure_id']}
MILESTONE_38_TASK_6_CLOSURE_SIGNATURE={report['closure_signature']}
MILESTONE_38_TASK_6_CLOSURE_STATUS={report['closure_status']}
MILESTONE_38_TASK_6_CLOSURE_CASE_COUNT={report['closure_case_count']}
MILESTONE_38_TASK_6_PASS_COUNT={report['pass_count']}
MILESTONE_38_TASK_6_FAIL_COUNT={report['fail_count']}
MILESTONE_38_TASK_6_CLOSURE_PASSED={_bool(report['closure_passed'])}
MILESTONE_38_TASK_6_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY={_bool(report['kaggle_competitive_agent_productization_boundary'])}
MILESTONE_38_TASK_6_REPLAYABLE_EVENT_TRACE_REQUIRED={_bool(report['replayable_event_trace_required'])}
MILESTONE_38_TASK_6_LOCAL_EVALUATION_RECORD_REQUIRED={_bool(report['local_evaluation_record_required'])}
MILESTONE_38_TASK_6_REGRESSION_SNAPSHOT_REQUIRED={_bool(report['regression_snapshot_required'])}
MILESTONE_38_TASK_6_AUDIT_ARTIFACT_REQUIRED={_bool(report['audit_artifact_required'])}
MILESTONE_38_TASK_6_TECHNICAL_EVALUATION_ONLY={_bool(report['technical_evaluation_only'])}
MILESTONE_38_TASK_6_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_38_TASK_6_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_38_TASK_6_OFFICIAL_BENCHMARK_CERTIFICATION={_bool(report['official_benchmark_certification'])}
MILESTONE_38_TASK_6_NETWORK_ACCESS_ALLOWED={_bool(report['network_access_allowed'])}
MILESTONE_38_TASK_6_SHELL_EXECUTION_ALLOWED={_bool(report['shell_execution_allowed'])}
MILESTONE_38_TASK_6_REPOSITORY_MUTATION_ALLOWED={_bool(report['repository_mutation_allowed'])}
MILESTONE_38_TASK_6_REGRESSION_EVENT_COUNT={report['regression_event_count']}
MILESTONE_38_TASK_6_REGRESSION_EVENT_TRACE_FINGERPRINT={report['regression_event_trace_fingerprint']}
MILESTONE_38_TASK_6_REPLAY_ID={report['replay_id']}
MILESTONE_38_TASK_6_LOCAL_EVALUATION_ID={report['local_evaluation_id']}
MILESTONE_38_TASK_6_REGRESSION_SNAPSHOT_ID={report['regression_snapshot_id']}
MILESTONE_38_TASK_6_AUDIT_ID={report['audit_id']}
MILESTONE_38_TASK_6_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_38_TASK_6_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_38_TASK_6_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_38_TASK_6_NEXT_STAGE={report['next_stage']}

## Closed Boundary

Milestone 38 is closed for the Kaggle competitive agent and productization boundary.

Closure confirms:
- source regression integration is valid;
- Kaggle competitive agent and productization evidence remains bound;
- local evaluation record remains bound;
- regression snapshot remains bound;
- audit artifact remains bound;
- no legal certification, Kaggle score claim, or official benchmark certification is produced.

Next stage is Milestone 38 governed opening.
"""


def write_milestone_38_task_6_artifacts() -> dict[str, str]:
    report = run_milestone_38_kaggle_competitive_agent_productization_final_closure()
    if not validate_milestone_38_kaggle_competitive_agent_productization_final_closure_report(report):
        raise ValueError("Milestone 38 Task 6 Kaggle competitive agent and productization final closure report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases = ARTIFACT_DIR / "task-6-kaggle-competitive-agent-and-productization-final-closure-cases.json"
    report_json = ARTIFACT_DIR / "task-6-kaggle-competitive-agent-and-productization-final-closure-report.json"
    report_md = ARTIFACT_DIR / "task-6-kaggle-competitive-agent-and-productization-final-closure-report.md"
    index = ARTIFACT_DIR / "task-6-index.txt"
    manifest = ARTIFACT_DIR / "task-6-manifest.json"

    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text(
        "\n".join(
            [
                "MILESTONE_38_TASK_6_ARTIFACT_INDEX",
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
                "closure_id": CLOSURE_ID,
                "closure_signature": CLOSURE_SIGNATURE,
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
    write_milestone_38_task_6_artifacts()
    report = run_milestone_38_kaggle_competitive_agent_productization_final_closure()
    markers = {
        "MILESTONE_38_TASK_6_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_FINAL_CLOSURE_READY": report["ready"],
        "MILESTONE_38_TASK_6_TASK_ID": report["task_id"],
        "MILESTONE_38_TASK_6_SOURCE_REGRESSION_TASK_ID": report["source_regression_task_id"],
        "MILESTONE_38_TASK_6_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_38_TASK_6_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_38_TASK_6_HARNESS_MODE_ID": report["harness_mode_id"],
        "MILESTONE_38_TASK_6_CLOSURE_ID": report["closure_id"],
        "MILESTONE_38_TASK_6_CLOSURE_STATUS": report["closure_status"],
        "MILESTONE_38_TASK_6_CLOSURE_CASE_COUNT": report["closure_case_count"],
        "MILESTONE_38_TASK_6_PASS_COUNT": report["pass_count"],
        "MILESTONE_38_TASK_6_FAIL_COUNT": report["fail_count"],
        "MILESTONE_38_TASK_6_CLOSURE_PASSED": report["closure_passed"],
        "MILESTONE_38_TASK_6_REGRESSION_EVENT_TRACE_FINGERPRINT": report["regression_event_trace_fingerprint"],
        "MILESTONE_38_TASK_6_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_38_TASK_6_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_38_TASK_6_OFFICIAL_BENCHMARK_CERTIFICATION": report["official_benchmark_certification"],
        "MILESTONE_38_TASK_6_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")


if __name__ == "__main__":
    main()
