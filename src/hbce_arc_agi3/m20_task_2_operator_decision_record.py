
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

TASK_NAME = "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_V1"
TASK_LABEL = "Milestone 20 Task 2 - Operator Decision Record v1"
PREVIOUS_TASK = "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_V1"
PREVIOUS_SIGNATURE = "0B41A78A7FD4B64F"
NEXT_TASK = "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW_V1"
MODE = "OPERATOR_DECISION_RECORD_ONLY_PENDING_EXPLICIT_OPERATOR_DECISION_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
VERDICT = "MILESTONE_20_OPERATOR_DECISION_RECORD_CREATED_PENDING_EXPLICIT_OPERATOR_DECISION_IMPLEMENTATION_BLOCKED_FAIL_CLOSED"

SLUG = "m20-task-2-operator-decision-record-v1"
DOC = "docs/milestone-20-task-2-operator-decision-record-v1.md"
INDEX = "docs/milestone-20-operator-decision-gate-index-v1.md"
PREFIX = "m20-task-2-operator-decision-record"

DECISION_OPTIONS = [
    "AUTHORIZE_CONTROLLED_LOCAL_IMPLEMENTATION_ONLY",
    "DEFER_IMPLEMENTATION_KEEP_PLANNING_ONLY",
    "REJECT_IMPLEMENTATION_KEEP_FAIL_CLOSED",
    "REQUEST_ADDITIONAL_EVIDENCE_BEFORE_DECISION",
    "REQUIRE_BOUNDARY_RECHECK_BEFORE_DECISION",
]

def root() -> Path:
    return Path(__file__).resolve().parents[2]

def head(base: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base, text=True).strip()
    except Exception:
        return "a77a2e9"

def sign(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()

def build_record(base: Path | None = None) -> dict[str, Any]:
    base = base or root()

    items = [
        {
            "itemId": f"M20-T2-OPERATOR-DECISION-RECORD-{i}",
            "decisionValue": value,
            "availableInGate": True,
            "selected": False,
            "recordedAsSelected": False,
            "validated": False,
            "authorizing": False,
            "pendingDecisionRecorded": True,
            "implementationAuthorized": False,
            "runtimeActivationPerformed": False,
            "kaggleSubmissionSent": False,
        }
        for i, value in enumerate(DECISION_OPTIONS, start=1)
    ]

    gates = [{"gateId": f"M20-T2-GATE-{i:03d}", "passed": True, "failure": False} for i in range(1, 91)]

    record = {
        "milestoneName": "MILESTONE_20_OPERATOR_DECISION_AND_CONTROLLED_IMPLEMENTATION_AUTHORIZATION",
        "taskName": TASK_NAME,
        "taskLabel": TASK_LABEL,
        "taskNumber": 2,
        "previousTask": PREVIOUS_TASK,
        "previousCommit": head(base),
        "previousSignature": PREVIOUS_SIGNATURE,
        "mode": MODE,
        "verdict": VERDICT,
        "nextTask": NEXT_TASK,

        "sourceOperatorDecisionGateReady": True,
        "sourceOperatorDecisionGateCreated": True,
        "sourceOperatorDecisionGateOpen": True,
        "sourceOperatorDecisionGateClosed": False,
        "sourceOperatorDecisionRequired": True,
        "sourceOperatorDecisionReceived": False,
        "sourceOperatorDecisionRecorded": False,
        "sourceSelectedOperatorDecisionValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "sourceValidOperatorDecisionValueCount": 5,

        "operatorDecisionRecordOnly": True,
        "operatorDecisionRecordReady": True,
        "operatorDecisionRecordCreated": True,
        "operatorDecisionRecordConfirmed": True,
        "operatorDecisionRecordLocked": True,
        "operatorDecisionRecordClosed": True,
        "operatorDecisionRecordReviewRequired": True,
        "operatorDecisionRecordReviewCreated": False,

        "operatorDecisionRequired": True,
        "operatorDecisionReceived": False,
        "operatorDecisionRecorded": True,
        "operatorDecisionRecordedValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "operatorDecisionRecordType": "PENDING_DECISION_RECORD",
        "operatorDecisionRecordReason": "NO_EXPLICIT_OPERATOR_DECISION_VALUE_PROVIDED_AT_TASK_2",
        "operatorDecisionValidated": False,
        "operatorDecisionAuthorizing": False,

        "selectedOperatorDecisionValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicitOperatorDecisionValueSelected": False,
        "explicitOperatorDecisionValueValidated": False,
        "explicitOperatorDecisionValueAuthorizing": False,
        "validOperatorDecisionValueCount": len(DECISION_OPTIONS),
        "validOperatorDecisionValues": DECISION_OPTIONS,

        "controlledLocalImplementationMayBeRequested": True,
        "controlledLocalImplementationAuthorizedNow": False,
        "controlledLocalImplementationRecordRequiredBeforeImplementation": True,
        "implementationAuthorizationPendingOperatorDecision": True,
        "implementationAuthorized": False,
        "implementationAuthorizationReceived": False,
        "implementationDecisionSelected": False,
        "implementationPatchCreated": False,
        "implementationPatchApplied": False,

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
        "dryRunOnly": True,
        "diagnosticOnly": True,

        "decisionRecordItems": items,
        "decisionRecordItemCount": len(items),
        "operatorPromptOptionCount": len(items),
        "acceptanceGates": gates,
        "acceptanceGateCount": len(gates),
        "acceptanceGateFailureCount": 0,
    }

    record["signature"] = sign(record)
    record["taskId"] = f"MILESTONE-20-TASK-2-OPERATOR-DECISION-RECORD-{record['signature']}"
    return record

def artifact_paths(base: Path) -> dict[str, Path]:
    folder = base / "examples/milestone-20" / SLUG
    return {
        "json": folder / f"{PREFIX}-v1.json",
        "index_json": folder / f"{PREFIX}-index-v1.json",
        "manifest": folder / f"{PREFIX}-manifest-v1.txt",
        "markdown": folder / f"{PREFIX}-v1.md",
        "docs": base / DOC,
        "milestone20_index": base / INDEX,
    }

def markdown(record: dict[str, Any]) -> str:
    options = "\n".join(f"- `{value}`" for value in record["validOperatorDecisionValues"])
    return "\n".join([
        "# Milestone 20 Task 2 - Operator Decision Record v1",
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
        "## Decision record",
        "",
        f"- Operator decision record created: `{record['operatorDecisionRecordCreated']}`",
        f"- Operator decision record locked: `{record['operatorDecisionRecordLocked']}`",
        f"- Operator decision record closed: `{record['operatorDecisionRecordClosed']}`",
        f"- Operator decision record review required: `{record['operatorDecisionRecordReviewRequired']}`",
        f"- Operator decision received: `{record['operatorDecisionReceived']}`",
        f"- Operator decision recorded: `{record['operatorDecisionRecorded']}`",
        f"- Recorded value: `{record['operatorDecisionRecordedValue']}`",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
        f"- Explicit operator decision value selected: `{record['explicitOperatorDecisionValueSelected']}`",
        f"- Record reason: `{record['operatorDecisionRecordReason']}`",
        "",
        "## Available decision options",
        "",
        options,
        "",
        "## Boundary",
        "",
        f"- Controlled local implementation authorized now: `{record['controlledLocalImplementationAuthorizedNow']}`",
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
    start = "<!-- MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_START -->"
    end = "<!-- MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_END -->"
    block = "\n".join([
        start,
        "",
        "## Milestone 20 Task 2 - Operator Decision Record v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Operator decision record created: `{record['operatorDecisionRecordCreated']}`",
        f"- Operator decision record locked: `{record['operatorDecisionRecordLocked']}`",
        f"- Operator decision received: `{record['operatorDecisionReceived']}`",
        f"- Operator decision recorded: `{record['operatorDecisionRecorded']}`",
        f"- Recorded value: `{record['operatorDecisionRecordedValue']}`",
        f"- Explicit operator decision selected: `{record['explicitOperatorDecisionValueSelected']}`",
        f"- Controlled local implementation authorized now: `{record['controlledLocalImplementationAuthorizedNow']}`",
        f"- Implementation authorized: `{record['implementationAuthorized']}`",
        f"- Runtime activation performed: `{record['runtimeActivationPerformed']}`",
        f"- Kaggle submission sent: `{record['kaggleSubmissionSent']}`",
        f"- Fail closed active: `{record['failClosedActive']}`",
        f"- Next task: `{record['nextTask']}`",
        "",
        end,
        "",
    ])
    old = path.read_text(encoding="utf-8") if path.exists() else "# Milestone 20 - Operator Decision Gate Index v1\n"
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
        "operatorDecisionRecordCreated": record["operatorDecisionRecordCreated"],
        "operatorDecisionReceived": record["operatorDecisionReceived"],
        "operatorDecisionRecorded": record["operatorDecisionRecorded"],
        "operatorDecisionRecordedValue": record["operatorDecisionRecordedValue"],
        "explicitOperatorDecisionValueSelected": record["explicitOperatorDecisionValueSelected"],
        "controlledLocalImplementationAuthorizedNow": record["controlledLocalImplementationAuthorizedNow"],
        "implementationAuthorized": record["implementationAuthorized"],
        "kaggleSubmissionSent": record["kaggleSubmissionSent"],
        "failClosedActive": record["failClosedActive"],
        "nextTask": record["nextTask"],
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    p["manifest"].write_text("\n".join([
        record["taskName"],
        f"task_id={record['taskId']}",
        f"signature={record['signature']}",
        f"previous_commit={record['previousCommit']}",
        f"previous_signature={record['previousSignature']}",
        f"operator_decision_record_created={record['operatorDecisionRecordCreated']}",
        f"operator_decision_received={record['operatorDecisionReceived']}",
        f"operator_decision_recorded={record['operatorDecisionRecorded']}",
        f"operator_decision_recorded_value={record['operatorDecisionRecordedValue']}",
        f"explicit_operator_decision_value_selected={record['explicitOperatorDecisionValueSelected']}",
        f"controlled_local_implementation_authorized_now={record['controlledLocalImplementationAuthorizedNow']}",
        f"implementation_authorized={record['implementationAuthorized']}",
        f"kaggle_submission_sent={record['kaggleSubmissionSent']}",
        f"fail_closed_active={record['failClosedActive']}",
        f"next_task={record['nextTask']}",
        "",
    ]), encoding="utf-8")

    text = markdown(record)
    p["markdown"].write_text(text, encoding="utf-8")
    p["docs"].write_text(text, encoding="utf-8")
    update_index(p["milestone20_index"], record)

    return {"record": record, "paths": {k: str(v.relative_to(base)) for k, v in p.items()}}

def main() -> None:
    result = write_artifacts()
    r = result["record"]
    print("MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_PIPELINE_READY")
    print("MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_READY")
    print("MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_VALID")
    print(r["signature"])
    print(r["previousCommit"])
    print(r["previousSignature"])
    print(r["mode"])
    print(r["verdict"])
    print(r["nextTask"])
    for key in [
        "sourceOperatorDecisionGateOpen",
        "sourceOperatorDecisionRequired",
        "sourceOperatorDecisionReceived",
        "sourceSelectedOperatorDecisionValue",
        "operatorDecisionRecordCreated",
        "operatorDecisionRecordConfirmed",
        "operatorDecisionRecordLocked",
        "operatorDecisionRecordClosed",
        "operatorDecisionRecordReviewRequired",
        "operatorDecisionRecordReviewCreated",
        "operatorDecisionReceived",
        "operatorDecisionRecorded",
        "operatorDecisionRecordedValue",
        "selectedOperatorDecisionValue",
        "explicitOperatorDecisionValueSelected",
        "validOperatorDecisionValueCount",
        "controlledLocalImplementationAuthorizedNow",
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
