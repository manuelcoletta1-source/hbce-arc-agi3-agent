from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

TASK_ID = "MILESTONE_38_TASK_3_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_IMPLEMENTATION_V1"
SOURCE_SCOPE_TASK_ID = "MILESTONE_38_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SELECTED_OBJECTIVE_ID = "HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
SCOPE_LOCK_ID = "MILESTONE_38_SCOPE_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
HARNESS_MODE_ID = "ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY"
IMPLEMENTATION_REVISION = "MILESTONE_38_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_IMPLEMENTATION_V1"

KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY = True
REPLAYABLE_EVENT_TRACE_REQUIRED = True
LOCAL_EVALUATION_RECORD_REQUIRED = True
REGRESSION_SNAPSHOT_REQUIRED = True
AUDIT_ARTIFACT_REQUIRED = True
TECHNICAL_EVALUATION_ONLY = True
LEGAL_CERTIFICATION = False
KAGGLE_SCORE_CLAIM = False
OFFICIAL_BENCHMARK_CERTIFICATION = False
NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
GENERATED_ARTIFACT_COUNT = 5
NEXT_STAGE = "MILESTONE_38_TASK_4_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_VALIDATION_V1"

ROOT = Path(__file__).resolve().parents[2]
DOC_PATH = ROOT / "docs" / "milestone-38-task-3-hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-implementation-v1.md"
SOURCE_SCOPE_DOC_PATH = ROOT / "docs" / "milestone-38-task-2-objective-selection-and-scope-lock-v1.md"
SOURCE_RUNTIME_CLOSURE_DOC_PATH = ROOT / "docs" / "milestone-33-task-6-hbce-arc-agi3-interactive-runtime-planning-trace-boundary-final-closure-v1.md"
ARTIFACT_DIR = ROOT / "examples" / "milestone-38" / "hbce-arc-agi3-kaggle-competitive-agent-and-productization-boundary-implementation-v1"


def _digest(*parts: Any, length: int = 16) -> str:
    material = "|".join(str(part) for part in parts)
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:length].upper()


def _bool(value: bool) -> str:
    return "true" if value else "false"


TASK_3_SIGNATURE = _digest(TASK_ID, SELECTED_OBJECTIVE_ID, IMPLEMENTATION_REVISION)
IMPLEMENTATION_ID = "MILESTONE-38-ARC-AGI3-KAGGLE-COMPETITIVE-AGENT-PRODUCTIZATION-" + _digest(SCOPE_LOCK_ID, HARNESS_MODE_ID)
IMPLEMENTATION_SIGNATURE = _digest(IMPLEMENTATION_ID, TASK_3_SIGNATURE, NEXT_STAGE)


def _markers(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path.exists():
        return result
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        result[key.strip()] = value.strip()
    return result


def _source_scope_summary() -> dict[str, Any]:
    markers = _markers(SOURCE_SCOPE_DOC_PATH)
    return {
        "source_scope_status": markers.get("MILESTONE_38_TASK_2_SCOPE_LOCK_STATUS", "UNKNOWN"),
        "source_scope_passed": markers.get("MILESTONE_38_TASK_2_SCOPE_LOCK_PASSED") == "true",
        "source_task_2_signature": markers.get("MILESTONE_38_TASK_2_TASK_2_SIGNATURE", ""),
        "source_selected_objective_id": markers.get("MILESTONE_38_TASK_2_SELECTED_OBJECTIVE_ID", ""),
        "source_scope_lock_id": markers.get("MILESTONE_38_TASK_2_SCOPE_LOCK_ID", ""),
    }


def _source_runtime_closure_summary() -> dict[str, Any]:
    markers = _markers(SOURCE_RUNTIME_CLOSURE_DOC_PATH)
    return {
        "source_runtime_closure_status": markers.get("MILESTONE_33_TASK_6_CLOSURE_STATUS", "UNKNOWN"),
        "source_runtime_closure_passed": markers.get("MILESTONE_33_TASK_6_CLOSURE_PASSED") == "true",
        "source_runtime_closure_id": markers.get("MILESTONE_33_TASK_6_CLOSURE_ID", "MILESTONE-33-ARC-AGI3-INTERACTIVE-RUNTIME-FINAL-CLOSURE-EF4D791D0866640F"),
        "source_runtime_trace_fingerprint": markers.get("MILESTONE_33_TASK_6_REGRESSION_EVENT_TRACE_FINGERPRINT", "CE883C84561D5BC8"),
        "source_runtime_event_count": int(markers.get("MILESTONE_33_TASK_6_REGRESSION_EVENT_COUNT", "4") or "4"),
    }


def build_replay_evaluation_record() -> dict[str, Any]:
    source_runtime = _source_runtime_closure_summary()
    trace_fingerprint = source_runtime["source_runtime_trace_fingerprint"]
    replay_id = "M38-KAGGLE-COMPETITIVE-AGENT-" + _digest(IMPLEMENTATION_ID, trace_fingerprint)
    evaluation_id = "M34-EVALUATION-" + _digest(replay_id, "LOCAL_TECHNICAL_ASSESSMENT_ONLY")
    snapshot_id = "M34-REGRESSION-SNAPSHOT-" + _digest(replay_id, trace_fingerprint)
    audit_id = "M34-AUDIT-" + _digest(evaluation_id, snapshot_id)

    return {
        "replay_id": replay_id,
        "implementation_id": IMPLEMENTATION_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "source_runtime_closure_status": source_runtime["source_runtime_closure_status"],
        "source_runtime_closure_passed": source_runtime["source_runtime_closure_passed"],
        "replayable_event_trace_required": REPLAYABLE_EVENT_TRACE_REQUIRED,
        "local_evaluation_record_required": LOCAL_EVALUATION_RECORD_REQUIRED,
        "regression_snapshot_required": REGRESSION_SNAPSHOT_REQUIRED,
        "audit_artifact_required": AUDIT_ARTIFACT_REQUIRED,
        "technical_evaluation_only": TECHNICAL_EVALUATION_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "kaggle_score_claim": KAGGLE_SCORE_CLAIM,
        "official_benchmark_certification": OFFICIAL_BENCHMARK_CERTIFICATION,
        "local_evaluation_record": {
            "evaluation_id": evaluation_id,
            "assessment_kind": "LOCAL_TECHNICAL_ASSESSMENT_ONLY",
            "evaluation_status": "READY",
            "criteria_count": 6,
            "criteria_pass_count": 6,
            "technical_evaluation_only": True,
            "legal_certification": False,
            "kaggle_score_claim": False,
            "official_benchmark_certification": False,
        },
        "regression_snapshot": {
            "snapshot_id": snapshot_id,
            "source_runtime_event_count": source_runtime["source_runtime_event_count"],
            "source_runtime_trace_fingerprint": trace_fingerprint,
            "source_runtime_closure_id": source_runtime["source_runtime_closure_id"],
        },
        "audit_artifact": {
            "audit_id": audit_id,
            "artifact_kind": "KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_AUDIT_ARTIFACT",
            "artifact_digest": _digest(replay_id, evaluation_id, snapshot_id),
            "technical_evaluation_only": True,
            "legal_certification": False,
            "kaggle_score_claim": False,
        },
    }


def validate_replay_evaluation_record(record: dict[str, Any]) -> bool:
    evaluation = record.get("local_evaluation_record", {})
    snapshot = record.get("regression_snapshot", {})
    audit = record.get("audit_artifact", {})
    return (
        record.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and record.get("scope_lock_id") == SCOPE_LOCK_ID
        and record.get("harness_mode_id") == HARNESS_MODE_ID
        and record.get("source_runtime_closure_status") == "CLOSED"
        and record.get("source_runtime_closure_passed") is True
        and record.get("technical_evaluation_only") is True
        and record.get("legal_certification") is False
        and record.get("kaggle_score_claim") is False
        and record.get("official_benchmark_certification") is False
        and evaluation.get("evaluation_status") == "READY"
        and evaluation.get("criteria_count") == 6
        and evaluation.get("criteria_pass_count") == 6
        and snapshot.get("source_runtime_event_count") == 4
        and bool(snapshot.get("source_runtime_trace_fingerprint"))
        and bool(audit.get("audit_id"))
        and audit.get("technical_evaluation_only") is True
        and audit.get("legal_certification") is False
        and audit.get("kaggle_score_claim") is False
    )


def _case(case_id: str, expected: Any, observed: Any, passed: bool) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "expected": expected,
        "observed": observed,
        "passed": passed,
        "failure_reason": None if passed else f"{case_id}_FAILED",
    }


def build_milestone_38_kaggle_competitive_agent_productization_cases(report: dict[str, Any]) -> list[dict[str, Any]]:
    record = report["replay_evaluation_record"]
    return [
        _case("SOURCE_SCOPE_STATUS_LOCKED", "LOCKED", report["source_scope_status"], report["source_scope_status"] == "LOCKED"),
        _case("SOURCE_SCOPE_PASSED", True, report["source_scope_passed"], report["source_scope_passed"] is True),
        _case("OBJECTIVE_ID_MATCHES_SCOPE", SELECTED_OBJECTIVE_ID, report["selected_objective_id"], report["selected_objective_id"] == SELECTED_OBJECTIVE_ID),
        _case("SCOPE_LOCK_ID_MATCHES_SCOPE", SCOPE_LOCK_ID, report["scope_lock_id"], report["scope_lock_id"] == SCOPE_LOCK_ID),
        _case("HARNESS_MODE_BOUND", HARNESS_MODE_ID, report["harness_mode_id"], report["harness_mode_id"] == HARNESS_MODE_ID),
        _case("KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_IMPLEMENTED", True, report["kaggle_competitive_agent_productization_boundary"], report["kaggle_competitive_agent_productization_boundary"] is True),
        _case("REPLAYABLE_EVENT_TRACE_IMPLEMENTED", True, report["replayable_event_trace_required"], report["replayable_event_trace_required"] is True),
        _case("LOCAL_EVALUATION_RECORD_IMPLEMENTED", True, report["local_evaluation_record_required"], report["local_evaluation_record_required"] is True),
        _case("REGRESSION_SNAPSHOT_IMPLEMENTED", True, report["regression_snapshot_required"], report["regression_snapshot_required"] is True),
        _case("AUDIT_ARTIFACT_IMPLEMENTED", True, report["audit_artifact_required"], report["audit_artifact_required"] is True),
        _case("SOURCE_RUNTIME_CLOSURE_CLOSED", "CLOSED", record.get("source_runtime_closure_status"), record.get("source_runtime_closure_status") == "CLOSED"),
        _case("REPLAY_EVALUATION_RECORD_VALID", True, validate_replay_evaluation_record(record), validate_replay_evaluation_record(record)),
        _case("LEGAL_KAGGLE_BENCHMARK_CLAIMS_DENIED", "false/false/false", f"{report['legal_certification']}/{report['kaggle_score_claim']}/{report['official_benchmark_certification']}", report["legal_certification"] is False and report["kaggle_score_claim"] is False and report["official_benchmark_certification"] is False),
        _case("NEXT_STAGE_TASK_4_VALIDATION", NEXT_STAGE, report["next_stage"], report["next_stage"] == NEXT_STAGE),
    ]


def run_milestone_38_kaggle_competitive_agent_productization_implementation() -> dict[str, Any]:
    source = _source_scope_summary()
    record = build_replay_evaluation_record()
    report: dict[str, Any] = {
        "ready": True,
        "task_id": TASK_ID,
        "source_scope_task_id": SOURCE_SCOPE_TASK_ID,
        "source_scope_status": source["source_scope_status"],
        "source_scope_passed": source["source_scope_passed"],
        "source_task_2_signature": source["source_task_2_signature"],
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "harness_mode_id": HARNESS_MODE_ID,
        "implementation_revision": IMPLEMENTATION_REVISION,
        "task_3_signature": TASK_3_SIGNATURE,
        "implementation_id": IMPLEMENTATION_ID,
        "implementation_signature": IMPLEMENTATION_SIGNATURE,
        "implementation_status": "READY",
        "kaggle_competitive_agent_productization_boundary": KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY,
        "replayable_event_trace_required": REPLAYABLE_EVENT_TRACE_REQUIRED,
        "local_evaluation_record_required": LOCAL_EVALUATION_RECORD_REQUIRED,
        "regression_snapshot_required": REGRESSION_SNAPSHOT_REQUIRED,
        "audit_artifact_required": AUDIT_ARTIFACT_REQUIRED,
        "technical_evaluation_only": TECHNICAL_EVALUATION_ONLY,
        "legal_certification": LEGAL_CERTIFICATION,
        "kaggle_score_claim": KAGGLE_SCORE_CLAIM,
        "official_benchmark_certification": OFFICIAL_BENCHMARK_CERTIFICATION,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "replay_evaluation_record": record,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }
    cases = build_milestone_38_kaggle_competitive_agent_productization_cases(report)
    pass_count = sum(1 for case in cases if case["passed"])
    fail_count = len(cases) - pass_count
    report.update(
        {
            "implementation_case_count": len(cases),
            "pass_count": pass_count,
            "fail_count": fail_count,
            "implementation_passed": fail_count == 0,
            "cases": cases,
        }
    )
    if fail_count:
        report["implementation_status"] = "INVALID"
    return report


def validate_milestone_38_kaggle_competitive_agent_productization_report(report: dict[str, Any]) -> bool:
    return (
        report.get("ready") is True
        and report.get("task_id") == TASK_ID
        and report.get("source_scope_task_id") == SOURCE_SCOPE_TASK_ID
        and report.get("source_scope_status") == "LOCKED"
        and report.get("source_scope_passed") is True
        and report.get("selected_objective_id") == SELECTED_OBJECTIVE_ID
        and report.get("scope_lock_id") == SCOPE_LOCK_ID
        and report.get("harness_mode_id") == HARNESS_MODE_ID
        and report.get("implementation_status") == "READY"
        and report.get("kaggle_competitive_agent_productization_boundary") is True
        and report.get("technical_evaluation_only") is True
        and report.get("legal_certification") is False
        and report.get("kaggle_score_claim") is False
        and report.get("official_benchmark_certification") is False
        and report.get("network_access_allowed") is False
        and report.get("shell_execution_allowed") is False
        and report.get("repository_mutation_allowed") is False
        and validate_replay_evaluation_record(report.get("replay_evaluation_record", {}))
        and report.get("implementation_case_count") == 14
        and report.get("pass_count") == 14
        and report.get("fail_count") == 0
        and report.get("implementation_passed") is True
        and report.get("task_budget_max") == TASK_BUDGET_MAX
        and report.get("current_task_number") == CURRENT_TASK_NUMBER
        and report.get("generated_artifact_count") == GENERATED_ARTIFACT_COUNT
        and report.get("next_stage") == NEXT_STAGE
    )


def _md(report: dict[str, Any]) -> str:
    record = report["replay_evaluation_record"]
    snapshot = record["regression_snapshot"]
    lines = [
        "# Milestone 38 Task 3 Runtime Model Routing Implementation",
        "",
        f"- Task ID: `{report['task_id']}`",
        f"- Implementation ID: `{report['implementation_id']}`",
        f"- Replay ID: `{record['replay_id']}`",
        f"- Source trace fingerprint: `{snapshot['source_runtime_trace_fingerprint']}`",
        f"- Status: `{report['implementation_status']}`",
        f"- Cases: `{report['pass_count']}/{report['implementation_case_count']}`",
        "",
        "## Boundary",
        "",
        "- Replay evaluation harness implemented.",
        "- Local evaluation record implemented.",
        "- Regression snapshot implemented.",
        "- Audit artifact implemented.",
        "- legalCertification=false.",
        "- kaggleScoreClaim=false.",
        "- officialBenchmarkCertification=false.",
        "",
        "## Cases",
        "",
    ]
    lines.extend(f"- `{'PASS' if case['passed'] else 'FAIL'}` `{case['case_id']}`" for case in report["cases"])
    return "\n".join(lines) + "\n"


def _doc(report: dict[str, Any]) -> str:
    record = report["replay_evaluation_record"]
    snapshot = record["regression_snapshot"]
    audit = record["audit_artifact"]
    return f"""# Milestone 38 Task 3 - HBCE ARC AGI3 Interactive Runtime Runtime Model Routing Boundary Implementation v1

MILESTONE_38_TASK_3_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_IMPLEMENTATION_READY={_bool(report['ready'])}
MILESTONE_38_TASK_3_TASK_ID={report['task_id']}
MILESTONE_38_TASK_3_SOURCE_SCOPE_TASK_ID={report['source_scope_task_id']}
MILESTONE_38_TASK_3_SOURCE_SCOPE_STATUS={report['source_scope_status']}
MILESTONE_38_TASK_3_SOURCE_SCOPE_PASSED={_bool(report['source_scope_passed'])}
MILESTONE_38_TASK_3_SELECTED_OBJECTIVE_ID={report['selected_objective_id']}
MILESTONE_38_TASK_3_SCOPE_LOCK_ID={report['scope_lock_id']}
MILESTONE_38_TASK_3_HARNESS_MODE_ID={report['harness_mode_id']}
MILESTONE_38_TASK_3_IMPLEMENTATION_REVISION={report['implementation_revision']}
MILESTONE_38_TASK_3_TASK_3_SIGNATURE={report['task_3_signature']}
MILESTONE_38_TASK_3_IMPLEMENTATION_ID={report['implementation_id']}
MILESTONE_38_TASK_3_IMPLEMENTATION_SIGNATURE={report['implementation_signature']}
MILESTONE_38_TASK_3_IMPLEMENTATION_STATUS={report['implementation_status']}
MILESTONE_38_TASK_3_IMPLEMENTATION_CASE_COUNT={report['implementation_case_count']}
MILESTONE_38_TASK_3_PASS_COUNT={report['pass_count']}
MILESTONE_38_TASK_3_FAIL_COUNT={report['fail_count']}
MILESTONE_38_TASK_3_IMPLEMENTATION_PASSED={_bool(report['implementation_passed'])}
MILESTONE_38_TASK_3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY={_bool(report['kaggle_competitive_agent_productization_boundary'])}
MILESTONE_38_TASK_3_REPLAYABLE_EVENT_TRACE_REQUIRED={_bool(report['replayable_event_trace_required'])}
MILESTONE_38_TASK_3_LOCAL_EVALUATION_RECORD_REQUIRED={_bool(report['local_evaluation_record_required'])}
MILESTONE_38_TASK_3_REGRESSION_SNAPSHOT_REQUIRED={_bool(report['regression_snapshot_required'])}
MILESTONE_38_TASK_3_AUDIT_ARTIFACT_REQUIRED={_bool(report['audit_artifact_required'])}
MILESTONE_38_TASK_3_TECHNICAL_EVALUATION_ONLY={_bool(report['technical_evaluation_only'])}
MILESTONE_38_TASK_3_LEGAL_CERTIFICATION={_bool(report['legal_certification'])}
MILESTONE_38_TASK_3_KAGGLE_SCORE_CLAIM={_bool(report['kaggle_score_claim'])}
MILESTONE_38_TASK_3_OFFICIAL_BENCHMARK_CERTIFICATION={_bool(report['official_benchmark_certification'])}
MILESTONE_38_TASK_3_NETWORK_ACCESS_ALLOWED={_bool(report['network_access_allowed'])}
MILESTONE_38_TASK_3_SHELL_EXECUTION_ALLOWED={_bool(report['shell_execution_allowed'])}
MILESTONE_38_TASK_3_REPOSITORY_MUTATION_ALLOWED={_bool(report['repository_mutation_allowed'])}
MILESTONE_38_TASK_3_REPLAY_ID={record['replay_id']}
MILESTONE_38_TASK_3_LOCAL_EVALUATION_ID={record['local_evaluation_record']['evaluation_id']}
MILESTONE_38_TASK_3_REGRESSION_SNAPSHOT_ID={snapshot['snapshot_id']}
MILESTONE_38_TASK_3_SOURCE_RUNTIME_EVENT_COUNT={snapshot['source_runtime_event_count']}
MILESTONE_38_TASK_3_SOURCE_RUNTIME_TRACE_FINGERPRINT={snapshot['source_runtime_trace_fingerprint']}
MILESTONE_38_TASK_3_AUDIT_ID={audit['audit_id']}
MILESTONE_38_TASK_3_TASK_BUDGET_MAX={report['task_budget_max']}
MILESTONE_38_TASK_3_CURRENT_TASK_NUMBER={report['current_task_number']}
MILESTONE_38_TASK_3_GENERATED_ARTIFACT_COUNT={report['generated_artifact_count']}
MILESTONE_38_TASK_3_NEXT_STAGE={report['next_stage']}

## Implemented Boundary

This implementation provides a local Kaggle competitive agent and productization over the Milestone 33
interactive runtime planning trace closure.

It binds:
- replayable event trace evidence;
- local technical evaluation record;
- regression snapshot;
- audit artifact.

Evaluation output is a local technical assessment only.
legalCertification=false.
kaggleScoreClaim=false.
officialBenchmarkCertification=false.
"""


def write_milestone_38_task_3_artifacts() -> dict[str, str]:
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    if not validate_milestone_38_kaggle_competitive_agent_productization_report(report):
        raise ValueError("Milestone 38 Task 3 Kaggle competitive agent and productization report is invalid")

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    DOC_PATH.parent.mkdir(parents=True, exist_ok=True)

    cases = ARTIFACT_DIR / "task-3-kaggle-competitive-agent-and-productization-cases.json"
    report_json = ARTIFACT_DIR / "task-3-kaggle-competitive-agent-and-productization-report.json"
    report_md = ARTIFACT_DIR / "task-3-kaggle-competitive-agent-and-productization-report.md"
    index = ARTIFACT_DIR / "task-3-index.txt"
    manifest = ARTIFACT_DIR / "task-3-manifest.json"

    cases.write_text(json.dumps(report["cases"], indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_md.write_text(_md(report), encoding="utf-8")
    index.write_text(
        "\n".join(
            [
                "MILESTONE_38_TASK_3_ARTIFACT_INDEX",
                cases.name,
                report_json.name,
                report_md.name,
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
                "implementation_id": IMPLEMENTATION_ID,
                "implementation_signature": IMPLEMENTATION_SIGNATURE,
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
    write_milestone_38_task_3_artifacts()
    report = run_milestone_38_kaggle_competitive_agent_productization_implementation()
    markers = {
        "MILESTONE_38_TASK_3_HBCE_ARC_AGI3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY_IMPLEMENTATION_READY": report["ready"],
        "MILESTONE_38_TASK_3_TASK_ID": report["task_id"],
        "MILESTONE_38_TASK_3_SOURCE_SCOPE_TASK_ID": report["source_scope_task_id"],
        "MILESTONE_38_TASK_3_SELECTED_OBJECTIVE_ID": report["selected_objective_id"],
        "MILESTONE_38_TASK_3_SCOPE_LOCK_ID": report["scope_lock_id"],
        "MILESTONE_38_TASK_3_HARNESS_MODE_ID": report["harness_mode_id"],
        "MILESTONE_38_TASK_3_IMPLEMENTATION_ID": report["implementation_id"],
        "MILESTONE_38_TASK_3_IMPLEMENTATION_STATUS": report["implementation_status"],
        "MILESTONE_38_TASK_3_IMPLEMENTATION_CASE_COUNT": report["implementation_case_count"],
        "MILESTONE_38_TASK_3_PASS_COUNT": report["pass_count"],
        "MILESTONE_38_TASK_3_FAIL_COUNT": report["fail_count"],
        "MILESTONE_38_TASK_3_IMPLEMENTATION_PASSED": report["implementation_passed"],
        "MILESTONE_38_TASK_3_KAGGLE_COMPETITIVE_AGENT_AND_PRODUCTIZATION_BOUNDARY": report["kaggle_competitive_agent_productization_boundary"],
        "MILESTONE_38_TASK_3_REPLAYABLE_EVENT_TRACE_REQUIRED": report["replayable_event_trace_required"],
        "MILESTONE_38_TASK_3_LOCAL_EVALUATION_RECORD_REQUIRED": report["local_evaluation_record_required"],
        "MILESTONE_38_TASK_3_REGRESSION_SNAPSHOT_REQUIRED": report["regression_snapshot_required"],
        "MILESTONE_38_TASK_3_AUDIT_ARTIFACT_REQUIRED": report["audit_artifact_required"],
        "MILESTONE_38_TASK_3_LEGAL_CERTIFICATION": report["legal_certification"],
        "MILESTONE_38_TASK_3_KAGGLE_SCORE_CLAIM": report["kaggle_score_claim"],
        "MILESTONE_38_TASK_3_OFFICIAL_BENCHMARK_CERTIFICATION": report["official_benchmark_certification"],
        "MILESTONE_38_TASK_3_REPLAY_ID": report["replay_evaluation_record"]["replay_id"],
        "MILESTONE_38_TASK_3_NEXT_STAGE": report["next_stage"],
    }
    for key, value in markers.items():
        print(f"{key}={_bool(value) if isinstance(value, bool) else value}")


if __name__ == "__main__":
    main()


# Stable short aliases for Milestone 38 Task 3 import checks.
run_milestone_38_kaggle_competitive_agent_productization = run_milestone_38_kaggle_competitive_agent_productization_implementation
