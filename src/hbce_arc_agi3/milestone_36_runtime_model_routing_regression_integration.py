"""Milestone 36 Task 5 runtime model routing boundary regression integration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from hbce_arc_agi3.milestone_36_runtime_model_routing import (
    run_milestone_36_runtime_model_routing_implementation,
)
from hbce_arc_agi3.milestone_36_runtime_model_routing_validation import (
    run_milestone_36_runtime_model_routing_validation,
    validate_milestone_36_runtime_model_routing_validation_report,
)

TASK_ID = "MILESTONE_36_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_REGRESSION_INTEGRATION_V1"
SOURCE_VALIDATION_TASK_ID = "MILESTONE_36_TASK_4_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_VALIDATION_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_36_SCOPE_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY"
HARNESS_MODE_ID = "ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY"
REGRESSION_INTEGRATION_REVISION = "MILESTONE_36_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_REGRESSION_INTEGRATION_V1"
INTEGRATION_ID = "MILESTONE-36-ARC-AGI3-RUNTIME-MODEL-ROUTING-INTEGRATION-FDC8E31DA830C4A4"
NEXT_STAGE = "MILESTONE_36_TASK_6_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_FINAL_CLOSURE_V1"
TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 5
GENERATED_ARTIFACT_COUNT = 5
INTEGRATION_CASE_COUNT = 20

ARTIFACT_DIR = Path("examples/milestone-36/hbce-arc-agi3-interactive-runtime-runtime-model-routing-boundary-regression-integration-v1")
DOC_PATH = Path("docs/milestone-36-task-5-hbce-arc-agi3-interactive-runtime-runtime-model-routing-boundary-regression-integration-v1.md")


def _bool(value: bool) -> str:
    return "true" if value else "false"


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest().upper()[:16]


TASK_5_SIGNATURE = _digest(
    {
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
    }
)
INTEGRATION_SIGNATURE = _digest(
    {
        "integration_id": INTEGRATION_ID,
        "task_5_signature": TASK_5_SIGNATURE,
        "case_count": INTEGRATION_CASE_COUNT,
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


def build_regression_event_trace(validation_report: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    report = validation_report or run_milestone_36_runtime_model_routing_validation()
    return [
        {
            "event_id": "M34-T5-EVT-001",
            "event_type": "source-validation-bound",
            "status": report["validation_status"],
            "fingerprint": report["validation_signature"],
        },
        {
            "event_id": "M34-T5-EVT-002",
            "event_type": "replay-record-bound",
            "status": "BOUND",
            "fingerprint": report["replay_id"],
        },
        {
            "event_id": "M34-T5-EVT-003",
            "event_type": "regression-snapshot-bound",
            "status": "BOUND",
            "fingerprint": report["regression_snapshot_id"],
        },
        {
            "event_id": "M34-T5-EVT-004",
            "event_type": "audit-artifact-bound",
            "status": "BOUND",
            "fingerprint": report["audit_id"],
        },
    ]


def build_milestone_36_runtime_model_routing_regression_integration_cases(
    validation_report: dict[str, Any] | None = None,
    implementation_report: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    validation = validation_report or run_milestone_36_runtime_model_routing_validation()
    implementation = implementation_report or run_milestone_36_runtime_model_routing_implementation()
    events = build_regression_event_trace(validation)

    return [
        _case("M34-T5-001", "Source validation report validates", validate_milestone_36_runtime_model_routing_validation_report(validation), validation.get("task_id")),
        _case("M34-T5-002", "Source validation task id is bound", validation.get("task_id") == SOURCE_VALIDATION_TASK_ID, validation.get("task_id")),
        _case("M34-T5-003", "Source validation status is VALID", validation.get("validation_status") == "VALID", validation.get("validation_status")),
        _case("M34-T5-004", "Source validation passed", validation.get("validation_passed") is True, validation.get("validation_passed")),
        _case("M34-T5-005", "Selected objective remains locked", validation.get("selected_objective_id") == SELECTED_OBJECTIVE_ID, validation.get("selected_objective_id")),
        _case("M34-T5-006", "Scope lock remains bound", validation.get("scope_lock_id") == SCOPE_LOCK_ID, validation.get("scope_lock_id")),
        _case("M34-T5-007", "Harness mode remains bound", validation.get("harness_mode_id") == HARNESS_MODE_ID, validation.get("harness_mode_id")),
        _case("M34-T5-008", "Implementation report remains ready", implementation.get("implementation_status") == "READY", implementation.get("implementation_status")),
        _case("M34-T5-009", "Replay boundary remains true", validation.get("runtime_model_routing_boundary") is True, validation.get("runtime_model_routing_boundary")),
        _case("M34-T5-010", "Replayable event trace remains required", validation.get("replayable_event_trace_required") is True, validation.get("replayable_event_trace_required")),
        _case("M34-T5-011", "Local evaluation record remains required", validation.get("local_evaluation_record_required") is True, validation.get("local_evaluation_record_required")),
        _case("M34-T5-012", "Regression snapshot remains required", validation.get("regression_snapshot_required") is True, validation.get("regression_snapshot_required")),
        _case("M34-T5-013", "Audit artifact remains required", validation.get("audit_artifact_required") is True, validation.get("audit_artifact_required")),
        _case("M34-T5-014", "Regression event trace has four bound events", len(events) == 4, len(events)),
        _case("M34-T5-015", "Regression event trace entries are all bound", all(event["status"] in {"VALID", "BOUND"} for event in events), events),
        _case("M34-T5-016", "Technical evaluation only remains true", validation.get("technical_evaluation_only") is True, validation.get("technical_evaluation_only")),
        _case("M34-T5-017", "Legal certification remains denied", validation.get("legal_certification") is False, validation.get("legal_certification")),
        _case("M34-T5-018", "Kaggle score claim remains denied", validation.get("kaggle_score_claim") is False, validation.get("kaggle_score_claim")),
        _case("M34-T5-019", "Official benchmark certification remains denied", validation.get("official_benchmark_certification") is False, validation.get("official_benchmark_certification")),
        _case("M34-T5-020", "Integration next stage advances to final closure", NEXT_STAGE.endswith("FINAL_CLOSURE_V1"), NEXT_STAGE),
    ]


def run_milestone_36_runtime_model_routing_regression_integration() -> dict[str, Any]:
    validation = run_milestone_36_runtime_model_routing_validation()
    implementation = run_milestone_36_runtime_model_routing_implementation()
    cases = build_milestone_36_runtime_model_routing_regression_integration_cases(validation, implementation)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    events = build_regression_event_trace(validation)

    return {
        "ready": fail_count == 0,
        "task_id": TASK_ID,
        "source_validation_task_id": SOURCE_VALIDATION_TASK_ID,
        "source_validation_status": validation.get("validation_status"),
        "source_validation_passed": validation.get("validation_passed"),
        "source_implementation_status": implementation.get("implementation_status"),
        "source_implementation_passed": implementation.get("implementation_passed"),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "regression_integration_revision": REGRESSION_INTEGRATION_REVISION,
        "task_5_signature": TASK_5_SIGNATURE,
        "integration_id": INTEGRATION_ID,
        "integration_signature": INTEGRATION_SIGNATURE,
        "integration_status": "VALID" if fail_count == 0 else "INVALID",
        "integration_case_count": len(cases),
        "pass_count": pass_count,
        "fail_count": fail_count,
        "integration_passed": fail_count == 0,
        "runtime_model_routing_boundary": validation.get("runtime_model_routing_boundary"),
        "replayable_event_trace_required": validation.get("replayable_event_trace_required"),
        "local_evaluation_record_required": validation.get("local_evaluation_record_required"),
        "regression_snapshot_required": validation.get("regression_snapshot_required"),
        "audit_artifact_required": validation.get("audit_artifact_required"),
        "technical_evaluation_only": validation.get("technical_evaluation_only"),
        "legal_certification": validation.get("legal_certification"),
        "kaggle_score_claim": validation.get("kaggle_score_claim"),
        "official_benchmark_certification": validation.get("official_benchmark_certification"),
        "network_access_allowed": validation.get("network_access_allowed"),
        "shell_execution_allowed": validation.get("shell_execution_allowed"),
        "repository_mutation_allowed": validation.get("repository_mutation_allowed"),
        "regression_event_count": len(events),
        "regression_event_trace": events,
        "regression_event_trace_fingerprint": _digest(events),
        "replay_id": validation.get("replay_id"),
        "local_evaluation_id": validation.get("local_evaluation_id"),
        "regression_snapshot_id": validation.get("regression_snapshot_id"),
        "audit_id": validation.get("audit_id"),
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
        "cases": cases,
        "source_validation_report": validation,
    }


def validate_milestone_36_runtime_model_routing_regression_integration_report(report: dict[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_validation_task_id") != SOURCE_VALIDATION_TASK_ID:
        return False
    if report.get("source_validation_status") != "VALID":
        return False
    if report.get("source_validation_passed") is not True:
        return False
    if report.get("source_implementation_status") != "READY":
        return False
    if report.get("source_implementation_passed") is not True:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("integration_status") != "VALID":
        return False
    if report.get("integration_case_count") != INTEGRATION_CASE_COUNT:
        return False
    if report.get("pass_count") != INTEGRATION_CASE_COUNT or report.get("fail_count") != 0:
        return False
    if report.get("integration_passed") is not True:
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
    if len(report.get("cases", [])) != INTEGRATION_CASE_COUNT:
        return False
    return all(case.get("passed") is True for case in report["cases"])


def _md(report: dict[str, Any]) -> str:
    lines = [
        "# Milestone 36 Task 5 Runtime Model Routing Boundary Regression Integration Report",
        "",
        f"- Integration ID: `{report['integration_id']}`",
        f"- Integration Status: `{report['integration_status']}`",
        f"- Cases: `{report['pass_count']}/{report['integration_case_count']}`",
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
    return f"""# Milestone 36 Task 5 - HBCE ARC AGI3 Interactive Runtime Runtime Model Routing Boundary Regression Integration v1

MILESTONE_36_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_REGRESSION_INTEGRATION_READY={_bool(report['ready'])}
MILESTONE_36_TASK_5_TASK_ID={report['task_id']}
MILESTONE_36_TASK_5_SOURCE_VALIDATION_TASK_ID={report['source_validation_task_id']}
MILESTONE_36_TASK_5_SOURCE_VALIDATION_STATUS={report['source_validation_status']}
MILESTONE_36_TASK_5_SOURCE_VALIDATION_PASSED={_bool(report['source_validation_passed'])}
MILESTONE_36_TASK_5_SOURCE_IMPLEMENTATION_STATUS={report['source_implementation_status']}
MILESTONE_36_TASK_5_SOURCE_IMPLEMENTATION_PASSED={_bool(report['source_implementation_passed'])}
MILESTONE_36_TASK_5_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_36_TASK_5_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_36_TASK_5_HARNESS_MODE_ID={report['harness_mode_id']}
MILESTONE_36_TASK_5_REGRESSION_INTEGRATION_REVISION={report['regression_integration_revision']}
MILESTONE_36_TASK_5_TASK_5_SIGNATURE={report['task_5_signature']}
MILESTONE_36_TASK_5_INTEGRATION_ID={report['integration_id']}
MILESTONE_36_TASK_5_INTEGRATION_SIGNATURE={report['integration_signature']}
MILESTONE_36_TASK_5_INTEGRATION_STATUS={report['integration_status']}
MILESTONE_36_TASK_5_INTEGRATION_CASE_COUNT={report['integration_case_count']}
MILESTONE_36_TASK_5_PASS_COUNT={report['pass_count']}
MILESTONE_36_TASK_5_FAIL_COUNT={report['fail_count']}
MILESTONE_36_TASK_5_INTEGRATION_PASSED={_bool(report['integration_passed'])}
MILESTONE_36_TASK_5_RUNTIME_MODEL_ROUTING_BOUNDARY={_bool(report['runtime_model_routing_boundary'])}
MILESTONE_36_TASK_5_REPLAYABLE_EVENT_TRACE_REQUIRED={_bool(report['replayable_event_trace_required'])}
MILESTONE_36_TASK_5_LOCAL_EVALUATION_RECORD_REQUIRED={_bool(report['local_evaluation_record_required'])}
MILESTONE_36_TASK_5_REGRESSION_SNAPSHOT_REQUIRED={_bool(report['regression_snapshot_required'])}
MILESTONE_36_TASK_5_AUDIT_ARTIFACT_REQUIRED={_bool(report['audit_artifact_required'])}
MILESTONE_36_TASK_5_TECHNICAL_EVALUATION_ONLY={_bool(report['technical_evaluation_only'])}
MILESTONE_36_TASK_5_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_36_TASK_5_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_36_TASK_5_OFFICIAL_BENCHMARK_CERTIFICATION={_bool(report['official_benchmark_certification'])}
MILESTONE_36_TASK_5_NETWORK_ACCESS_ALLOWED={_bool(report['network_access_allowed'])}
MILESTONE_36_TASK_5_SHELL_EXECUTION_ALLOWED={_bool(report['shell_execution_allowed'])}
MILESTONE_36_TASK_5_REPOSITORY_MUTATION_ALLOWED={_bool(report['repository_mutation_allowed'])}
MILESTONE_36_TASK_5_REGRESSION_EVENT_COUNT={report['regression_event_count']}
MILESTONE_36_TASK_5_REGRESSION_EVENT_TRACE_FINGERPRINT={report['regression_event_trace_fingerprint']}
MILESTONE_36_TASK_5_REPLAY_ID={report['replay_id']}
MILESTONE_36_TASK_5_LOCAL_EVALUATION_ID={report['local_evaluation_id']}
MILESTONE_36_TASK_5_REGRESSION_SNAPSHOT_ID={report['regression_snapshot_id']}
MILESTONE_36_TASK_5_AUDIT_ID={report['audit_id']}
MILESTONE_36_TASK_5_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_36_TASK_5_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_36_TASK_5_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_36_TASK_5_NEXT_STAGE={report['next_stage']}

## Integrated Regression Boundary

This integration binds the validated runtime model routing into the regression chain.

It preserves:
- source validation status;
- implementation readiness;
- objective and scope lock continuity;
- replay event trace continuity;
- local evaluation record continuity;
- regression snapshot continuity;
- audit artifact continuity.

No legal certification is produced.
No Kaggle score claim is produced.
No official benchmark certification is produced.
"""


def write_milestone_36_task_5_artifacts() -> dict[str, str]:
    report = run_milestone_36_runtime_model_routing_regression_integration()
    if not validate_milestone_36_runtime_model_routing_regression_integration_report(report):
        raise ValueError("Milestone 36 Task 5 runtime model routing regression integration report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases = ARTIFACT_DIR / "task-5-runtime-model-routing-regression-integration-cases.json"
    report_json = ARTIFACT_DIR / "task-5-runtime-model-routing-regression-integration-report.json"
    report_md = ARTIFACT_DIR / "task-5-runtime-model-routing-regression-integration-report.md"
    index = ARTIFACT_DIR / "task-5-index.txt"
    manifest = ARTIFACT_DIR / "task-5-manifest.json"

    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text(
        "\n".join(
            [
                "MILESTONE_36_TASK_5_ARTIFACT_INDEX",
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
                "integration_id": INTEGRATION_ID,
                "integration_signature": INTEGRATION_SIGNATURE,
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
    write_milestone_36_task_5_artifacts()
    report = run_milestone_36_runtime_model_routing_regression_integration()
    markers = {
        "MILESTONE_36_TASK_5_HBCE_ARC_AGI3_INTERACTIVE_RUNTIME_RUNTIME_MODEL_ROUTING_BOUNDARY_REGRESSION_INTEGRATION_READY": report["ready"],
        "MILESTONE_36_TASK_5_TASK_ID": report["task_id"],
        "MILESTONE_36_TASK_5_SOURCE_VALIDATION_TASK_ID": report["source_validation_task_id"],
        "MILESTONE_36_TASK_5_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_36_TASK_5_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_36_TASK_5_HARNESS_MODE_ID": report["harness_mode_id"],
        "MILESTONE_36_TASK_5_INTEGRATION_ID": report["integration_id"],
        "MILESTONE_36_TASK_5_INTEGRATION_STATUS": report["integration_status"],
        "MILESTONE_36_TASK_5_INTEGRATION_CASE_COUNT": report["integration_case_count"],
        "MILESTONE_36_TASK_5_PASS_COUNT": report["pass_count"],
        "MILESTONE_36_TASK_5_FAIL_COUNT": report["fail_count"],
        "MILESTONE_36_TASK_5_INTEGRATION_PASSED": report["integration_passed"],
        "MILESTONE_36_TASK_5_REGRESSION_EVENT_COUNT": report["regression_event_count"],
        "MILESTONE_36_TASK_5_REGRESSION_EVENT_TRACE_FINGERPRINT": report["regression_event_trace_fingerprint"],
        "MILESTONE_36_TASK_5_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_36_TASK_5_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_36_TASK_5_OFFICIAL_BENCHMARK_CERTIFICATION": report["official_benchmark_certification"],
        "MILESTONE_36_TASK_5_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")


if __name__ == "__main__":
    main()
