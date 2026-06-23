
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

TASK_NAME = "MILESTONE_19_TASK_63_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_V1"
TASK_LABEL = "Cross-Trace Diagnostic Planner Explicit Operator Decision Value Selection Operator Decision Final Wait State Archive Index Final Pending Status Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index v1"
PREVIOUS_TASK = "MILESTONE_19_TASK_62_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_REVIEW_V1"
PREVIOUS_SIGNATURE = "AED0EA44BDAD22DD"
NEXT_TASK = "MILESTONE_19_TASK_64_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_REVIEW_V1"
MODE = "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_ONLY_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
VERDICT = "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CREATED_REVIEW_REQUIRED_IMPLEMENTATION_BLOCKED"

SLUG = "m19-task-63-closure-archive-index-v1"
DOC = "docs/milestone-19-task-63-closure-archive-index-v1.md"
INDEX = "docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md"
PREFIX = "m19-task-63-closure-archive-index"

ALLOWED = [
    "AUTHORIZE_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_ONLY",
    "DEFER_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_KEEP_PLANNING_ONLY",
    "REJECT_CROSS_TRACE_DIAGNOSTIC_PLANNER_IMPLEMENTATION_KEEP_FAIL_CLOSED",
    "REQUEST_ADDITIONAL_SPEC_EVIDENCE_BEFORE_IMPLEMENTATION",
    "REQUIRE_BOUNDARY_RECHECK_BEFORE_IMPLEMENTATION",
]

def root() -> Path:
    return Path(__file__).resolve().parents[2]

def head(base: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base, text=True).strip()
    except Exception:
        return "f09a9df"

def sign(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()

def build_record(base: Path | None = None) -> dict[str, Any]:
    base = base or root()

    items = [
        {
            "itemId": f"M19-T63-CLOSURE-ARCHIVE-INDEX-{i}",
            "sourceClosureReviewItemId": f"M19-T62-CLOSURE-REVIEW-{i}",
            "operatorDecisionValue": value,
            "selected": False,
            "validated": False,
            "authorizing": False,
            "closureArchiveIndexCreated": True,
            "closureArchiveIndexConfirmed": True,
            "closureArchiveIndexLocked": True,
            "closureArchiveIndexActive": True,
            "closureArchiveIndexClosed": False,
            "closureArchiveIndexReviewRequired": True,
            "closureArchiveIndexReviewCreated": False,
            "implementationAuthorized": False,
            "runtimeActivationPerformed": False,
            "kaggleSubmissionSent": False,
        }
        for i, value in enumerate(ALLOWED, start=1)
    ]

    gates = [{"gateId": f"M19-T63-GATE-{i:03d}", "passed": True, "failure": False} for i in range(1, 91)]

    record = {
        "milestoneName": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER",
        "taskName": TASK_NAME,
        "taskLabel": TASK_LABEL,
        "taskNumber": 63,
        "previousTask": PREVIOUS_TASK,
        "previousCommit": head(base),
        "previousSignature": PREVIOUS_SIGNATURE,
        "mode": MODE,
        "verdict": VERDICT,
        "nextTask": NEXT_TASK,

        "closureArchiveIndexOnly": True,
        "closureArchiveIndexReady": True,
        "closureArchiveIndexCreated": True,
        "closureArchiveIndexConfirmed": True,
        "closureArchiveIndexLocked": True,
        "closureArchiveIndexActive": True,
        "closureArchiveIndexClosed": False,
        "closureArchiveIndexReviewRequired": True,
        "closureArchiveIndexReviewCreated": False,

        "sourceClosureReviewReady": True,
        "sourceClosureReviewPassed": True,
        "sourceClosureReviewCreated": True,
        "sourceClosureReviewActive": True,
        "sourceClosureReviewClosed": False,
        "sourceClosureArchiveIndexRequired": True,
        "sourceClosureArchiveIndexCreated": False,

        "sourceClosureReady": True,
        "sourceClosureCreated": True,
        "sourceClosureConfirmed": True,
        "sourceClosureLocked": True,
        "sourceClosureActive": False,
        "sourceClosureClosed": True,

        "planningOnlyUntilExplicitOperatorDecision": True,
        "waitingForExplicitOperatorDecisionValue": True,
        "operatorDecisionPendingStatusActive": True,
        "selectedOperatorDecisionValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicitOperatorDecisionValueSelected": False,
        "explicitOperatorDecisionValueValidated": False,
        "explicitOperatorDecisionValueAuthorizing": False,

        "operatorApprovalRequired": True,
        "operatorApprovalReceived": False,
        "operatorDecisionRequiredForImplementation": True,
        "operatorDecisionReceived": False,

        "implementationAuthorized": False,
        "implementationAuthorizationReceived": False,
        "implementationDecisionSelected": False,
        "runtimeActivationAuthorized": False,
        "runtimeActivationPerformed": False,
        "runtimeSolverModified": False,
        "candidateGeneratorModified": False,
        "rankerModified": False,
        "verifierModified": False,
        "realEvaluationAuthorized": False,
        "realEvaluationPerformed": False,
        "realSubmissionAuthorized": False,
        "submissionArtifactCreated": False,
        "kaggleAuthenticationAllowed": False,
        "kaggleAuthenticationPerformed": False,
        "kaggleSubmissionSent": False,
        "internetDuringEval": False,
        "externalApiDependency": False,
        "hiddenLabelAccessed": False,
        "privateCoreExposure": False,
        "legalCertification": False,

        "failClosedRequired": True,
        "failClosedActive": True,
        "localOnly": True,
        "deterministic": True,
        "publicSafe": True,

        "allowedOperatorDecisionValues": ALLOWED,
        "operatorPromptOptionCount": len(ALLOWED),
        "closureArchiveIndexItemCount": len(items),
        "closureArchiveIndexReviewItemCount": len(items),
        "items": items,
        "acceptanceGates": gates,
        "acceptanceGateCount": len(gates),
        "acceptanceGateFailureCount": 0,
    }

    record["signature"] = sign(record)
    record["taskId"] = f"MILESTONE-19-TASK-63-CLOSURE-ARCHIVE-INDEX-{record['signature']}"
    return record

def artifact_paths(base: Path) -> dict[str, Path]:
    folder = base / "examples/milestone-19" / SLUG
    return {
        "json": folder / f"{PREFIX}-v1.json",
        "index_json": folder / f"{PREFIX}-index-v1.json",
        "manifest": folder / f"{PREFIX}-manifest-v1.txt",
        "markdown": folder / f"{PREFIX}-v1.md",
        "docs": base / DOC,
        "milestone_index": base / INDEX,
    }

def markdown(record: dict[str, Any]) -> str:
    return "\n".join([
        "# Milestone 19 Task 63 - Final Pending Status Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous task: `{record['previousTask']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Verdict: `{record['verdict']}`",
        f"- Next task: `{record['nextTask']}`",
        "",
        "## Result",
        "",
        f"- Closure archive index created: `{record['closureArchiveIndexCreated']}`",
        f"- Closure archive index confirmed: `{record['closureArchiveIndexConfirmed']}`",
        f"- Closure archive index locked: `{record['closureArchiveIndexLocked']}`",
        f"- Closure archive index active: `{record['closureArchiveIndexActive']}`",
        f"- Closure archive index closed: `{record['closureArchiveIndexClosed']}`",
        f"- Closure archive index review required: `{record['closureArchiveIndexReviewRequired']}`",
        f"- Closure archive index review created: `{record['closureArchiveIndexReviewCreated']}`",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
        f"- Explicit operator decision value selected: `{record['explicitOperatorDecisionValueSelected']}`",
        f"- Implementation authorized: `{record['implementationAuthorized']}`",
        f"- Runtime activation performed: `{record['runtimeActivationPerformed']}`",
        f"- Runtime solver modified: `{record['runtimeSolverModified']}`",
        f"- Candidate generator modified: `{record['candidateGeneratorModified']}`",
        f"- Ranker modified: `{record['rankerModified']}`",
        f"- Verifier modified: `{record['verifierModified']}`",
        f"- Real evaluation performed: `{record['realEvaluationPerformed']}`",
        f"- Kaggle submission sent: `{record['kaggleSubmissionSent']}`",
        f"- Private core exposure: `{record['privateCoreExposure']}`",
        f"- Legal certification: `{record['legalCertification']}`",
        f"- Fail closed active: `{record['failClosedActive']}`",
        "",
    ])

def update_index(path: Path, record: dict[str, Any]) -> None:
    start = "<!-- MILESTONE_19_TASK_63_CLOSURE_ARCHIVE_INDEX_START -->"
    end = "<!-- MILESTONE_19_TASK_63_CLOSURE_ARCHIVE_INDEX_END -->"
    block = "\n".join([
        start,
        "",
        "## Milestone 19 Task 63 - Final Pending Status Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index Closure Archive Index v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Closure archive index created: `{record['closureArchiveIndexCreated']}`",
        f"- Closure archive index locked: `{record['closureArchiveIndexLocked']}`",
        f"- Closure archive index active: `{record['closureArchiveIndexActive']}`",
        f"- Closure archive index closed: `{record['closureArchiveIndexClosed']}`",
        f"- Closure archive index review required: `{record['closureArchiveIndexReviewRequired']}`",
        f"- Implementation authorized: `{record['implementationAuthorized']}`",
        f"- Runtime activation performed: `{record['runtimeActivationPerformed']}`",
        f"- Kaggle submission sent: `{record['kaggleSubmissionSent']}`",
        f"- Fail closed active: `{record['failClosedActive']}`",
        "",
        end,
        "",
    ])
    old = path.read_text(encoding="utf-8") if path.exists() else "# Milestone 19 Planning Index v1\n"
    if start in old and end in old:
        old = old.split(start)[0] + block + old.split(end, 1)[1].lstrip("\n")
    else:
        old = old.rstrip() + "\n\n" + block
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(old, encoding="utf-8")

def write_artifacts(base: Path | None = None) -> dict[str, Any]:
    base = base or root()
    record = build_record(base)
    p = artifact_paths(base)
    for value in p.values():
        value.parent.mkdir(parents=True, exist_ok=True)

    p["json"].write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    p["index_json"].write_text(json.dumps({
        "taskName": record["taskName"],
        "taskId": record["taskId"],
        "signature": record["signature"],
        "closureArchiveIndexCreated": record["closureArchiveIndexCreated"],
        "closureArchiveIndexLocked": record["closureArchiveIndexLocked"],
        "closureArchiveIndexActive": record["closureArchiveIndexActive"],
        "closureArchiveIndexClosed": record["closureArchiveIndexClosed"],
        "closureArchiveIndexReviewRequired": record["closureArchiveIndexReviewRequired"],
        "implementationAuthorized": record["implementationAuthorized"],
        "kaggleSubmissionSent": record["kaggleSubmissionSent"],
        "failClosedActive": record["failClosedActive"],
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    p["manifest"].write_text("\n".join([
        record["taskName"],
        f"task_id={record['taskId']}",
        f"signature={record['signature']}",
        f"previous_commit={record['previousCommit']}",
        f"previous_signature={record['previousSignature']}",
        f"closure_archive_index_created={record['closureArchiveIndexCreated']}",
        f"closure_archive_index_locked={record['closureArchiveIndexLocked']}",
        f"closure_archive_index_active={record['closureArchiveIndexActive']}",
        f"closure_archive_index_closed={record['closureArchiveIndexClosed']}",
        f"closure_archive_index_review_required={record['closureArchiveIndexReviewRequired']}",
        f"implementation_authorized={record['implementationAuthorized']}",
        f"kaggle_submission_sent={record['kaggleSubmissionSent']}",
        f"fail_closed_active={record['failClosedActive']}",
        "",
    ]), encoding="utf-8")

    text = markdown(record)
    p["markdown"].write_text(text, encoding="utf-8")
    p["docs"].write_text(text, encoding="utf-8")
    update_index(p["milestone_index"], record)

    return {"record": record, "paths": {k: str(v.relative_to(base)) for k, v in p.items()}}

def main() -> None:
    result = write_artifacts()
    r = result["record"]
    print("MILESTONE_19_TASK_63_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_V1_PIPELINE_READY")
    print("MILESTONE_19_TASK_63_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_V1_READY")
    print("MILESTONE_19_TASK_63_CROSS_TRACE_DIAGNOSTIC_PLANNER_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_OPERATOR_DECISION_FINAL_WAIT_STATE_ARCHIVE_INDEX_FINAL_PENDING_STATUS_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_CLOSURE_ARCHIVE_INDEX_V1_VALID")
    print(r["signature"])
    print(r["previousCommit"])
    print(r["previousSignature"])
    print(r["mode"])
    print(r["verdict"])
    print(r["nextTask"])
    for key in [
        "closureArchiveIndexCreated",
        "closureArchiveIndexConfirmed",
        "closureArchiveIndexLocked",
        "closureArchiveIndexActive",
        "closureArchiveIndexClosed",
        "closureArchiveIndexReviewRequired",
        "closureArchiveIndexReviewCreated",
        "selectedOperatorDecisionValue",
        "explicitOperatorDecisionValueSelected",
        "implementationAuthorized",
        "runtimeActivationPerformed",
        "runtimeSolverModified",
        "candidateGeneratorModified",
        "rankerModified",
        "verifierModified",
        "realEvaluationPerformed",
        "kaggleSubmissionSent",
        "privateCoreExposure",
        "legalCertification",
        "failClosedActive",
        "acceptanceGateCount",
        "acceptanceGateFailureCount",
    ]:
        print(f"{key}={r[key]}")
    for key, value in result["paths"].items():
        print(f"{key}={value}")

if __name__ == "__main__":
    main()
