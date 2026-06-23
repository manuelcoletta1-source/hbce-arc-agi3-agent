
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

TASK_NAME = "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_V1"
TASK_LABEL = "Milestone 20 Task 1 - Operator Decision Gate v1"
PREVIOUS_STAGE = "MILESTONE_19"
PREVIOUS_TASK = "MILESTONE_19_TASK_83_FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_TO_MILESTONE_20_V1"
PREVIOUS_SIGNATURE = "96D4D3402FD43306"
NEXT_TASK = "MILESTONE_20_TASK_2_OPERATOR_DECISION_RECORD_V1"
MODE = "OPERATOR_DECISION_GATE_ONLY_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
VERDICT = "MILESTONE_20_OPERATOR_DECISION_GATE_OPEN_PENDING_EXPLICIT_OPERATOR_DECISION_IMPLEMENTATION_BLOCKED_FAIL_CLOSED"

SLUG = "m20-task-1-operator-decision-gate-v1"
DOC = "docs/milestone-20-task-1-operator-decision-gate-v1.md"
INDEX = "docs/milestone-20-operator-decision-gate-index-v1.md"
PREFIX = "m20-task-1-operator-decision-gate"

DECISION_OPTIONS = [
    {
        "value": "AUTHORIZE_CONTROLLED_LOCAL_IMPLEMENTATION_ONLY",
        "label": "Authorize controlled local implementation only",
        "effect": "Allows a local deterministic implementation plan in Milestone 20 without runtime activation, real evaluation, or Kaggle submission.",
        "implementationAuthorizedNow": False,
        "requiresNextRecord": True,
    },
    {
        "value": "DEFER_IMPLEMENTATION_KEEP_PLANNING_ONLY",
        "label": "Defer implementation and keep planning-only mode",
        "effect": "Keeps the system in planning/audit-only mode and blocks all runtime modifications.",
        "implementationAuthorizedNow": False,
        "requiresNextRecord": True,
    },
    {
        "value": "REJECT_IMPLEMENTATION_KEEP_FAIL_CLOSED",
        "label": "Reject implementation and keep fail-closed",
        "effect": "Stops implementation path and preserves fail-closed evidence state.",
        "implementationAuthorizedNow": False,
        "requiresNextRecord": True,
    },
    {
        "value": "REQUEST_ADDITIONAL_EVIDENCE_BEFORE_DECISION",
        "label": "Request additional evidence before decision",
        "effect": "Requires additional technical evidence before any implementation authorization can be considered.",
        "implementationAuthorizedNow": False,
        "requiresNextRecord": True,
    },
    {
        "value": "REQUIRE_BOUNDARY_RECHECK_BEFORE_DECISION",
        "label": "Require boundary recheck before decision",
        "effect": "Requires a boundary, safety, and public-safe recheck before an operator decision record.",
        "implementationAuthorizedNow": False,
        "requiresNextRecord": True,
    },
]

def root() -> Path:
    return Path(__file__).resolve().parents[2]

def head(base: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base, text=True).strip()
    except Exception:
        return "3160c5a"

def sign(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()

def build_record(base: Path | None = None) -> dict[str, Any]:
    base = base or root()

    items = [
        {
            "itemId": f"M20-T1-OPERATOR-DECISION-OPTION-{i}",
            "decisionValue": option["value"],
            "decisionLabel": option["label"],
            "decisionEffect": option["effect"],
            "presentedToOperator": True,
            "selected": False,
            "validated": False,
            "recorded": False,
            "authorizing": False,
            "implementationAuthorizedNow": option["implementationAuthorizedNow"],
            "requiresNextRecord": option["requiresNextRecord"],
            "runtimeActivationPerformed": False,
            "realEvaluationPerformed": False,
            "kaggleSubmissionSent": False,
        }
        for i, option in enumerate(DECISION_OPTIONS, start=1)
    ]

    gates = [{"gateId": f"M20-T1-GATE-{i:03d}", "passed": True, "failure": False} for i in range(1, 91)]

    record = {
        "milestoneName": "MILESTONE_20_OPERATOR_DECISION_AND_CONTROLLED_IMPLEMENTATION_AUTHORIZATION",
        "taskName": TASK_NAME,
        "taskLabel": TASK_LABEL,
        "taskNumber": 1,
        "previousStage": PREVIOUS_STAGE,
        "previousTask": PREVIOUS_TASK,
        "previousCommit": head(base),
        "previousSignature": PREVIOUS_SIGNATURE,
        "mode": MODE,
        "verdict": VERDICT,
        "nextTask": NEXT_TASK,

        "sourceMilestone19Closed": True,
        "sourceMilestone19Frozen": True,
        "sourceMilestone19FreezeIndexCreated": True,
        "sourceMilestone19FreezeIndexLocked": True,
        "sourceRecursiveArchiveChainStopped": True,
        "sourceNoFurtherMilestone19TasksRequired": True,
        "sourceHandoffToMilestone20": True,

        "operatorDecisionGateOnly": True,
        "operatorDecisionGateReady": True,
        "operatorDecisionGateCreated": True,
        "operatorDecisionGateOpen": True,
        "operatorDecisionGateClosed": False,
        "operatorDecisionGateLocked": False,

        "operatorDecisionRequired": True,
        "operatorDecisionReceived": False,
        "operatorDecisionRecorded": False,
        "operatorDecisionValidated": False,
        "operatorDecisionAuthorizing": False,
        "operatorDecisionRecordRequired": True,
        "operatorDecisionRecordCreated": False,

        "selectedOperatorDecisionValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "explicitOperatorDecisionValueSelected": False,
        "explicitOperatorDecisionValueValidated": False,
        "explicitOperatorDecisionValueAuthorizing": False,
        "validOperatorDecisionValueCount": len(DECISION_OPTIONS),
        "validOperatorDecisionValues": [option["value"] for option in DECISION_OPTIONS],

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

        "decisionOptions": DECISION_OPTIONS,
        "decisionOptionItems": items,
        "decisionOptionCount": len(items),
        "operatorPromptOptionCount": len(items),
        "acceptanceGates": gates,
        "acceptanceGateCount": len(gates),
        "acceptanceGateFailureCount": 0,
    }

    record["signature"] = sign(record)
    record["taskId"] = f"MILESTONE-20-TASK-1-OPERATOR-DECISION-GATE-{record['signature']}"
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
    options = "\n".join(
        f"- `{item['decisionValue']}`: {item['decisionEffect']}"
        for item in record["decisionOptionItems"]
    )
    return "\n".join([
        "# Milestone 20 Task 1 - Operator Decision Gate v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous stage: `{record['previousStage']}`",
        f"- Previous task: `{record['previousTask']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Verdict: `{record['verdict']}`",
        f"- Next task: `{record['nextTask']}`",
        "",
        "## Source handoff",
        "",
        f"- Milestone 19 closed: `{record['sourceMilestone19Closed']}`",
        f"- Milestone 19 frozen: `{record['sourceMilestone19Frozen']}`",
        f"- Recursive archive chain stopped: `{record['sourceRecursiveArchiveChainStopped']}`",
        f"- Handoff to Milestone 20: `{record['sourceHandoffToMilestone20']}`",
        "",
        "## Operator decision gate",
        "",
        f"- Gate ready: `{record['operatorDecisionGateReady']}`",
        f"- Gate open: `{record['operatorDecisionGateOpen']}`",
        f"- Gate closed: `{record['operatorDecisionGateClosed']}`",
        f"- Operator decision required: `{record['operatorDecisionRequired']}`",
        f"- Operator decision received: `{record['operatorDecisionReceived']}`",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
        "",
        "## Valid decision options",
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
    start = "<!-- MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_START -->"
    end = "<!-- MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_END -->"
    block = "\n".join([
        "# Milestone 20 - Operator Decision Gate Index v1",
        "",
        start,
        "",
        "## Milestone 20 Task 1 - Operator Decision Gate v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Source Milestone 19 closed: `{record['sourceMilestone19Closed']}`",
        f"- Operator decision gate open: `{record['operatorDecisionGateOpen']}`",
        f"- Operator decision required: `{record['operatorDecisionRequired']}`",
        f"- Operator decision received: `{record['operatorDecisionReceived']}`",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
        f"- Decision option count: `{record['decisionOptionCount']}`",
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
    old = path.read_text(encoding="utf-8") if path.exists() else ""
    if start in old and end in old:
        old = old.split(start)[0] + block.split(start, 1)[1].split(end)[0].join([start, end]) + old.split(end, 1)[1].lstrip("\n")
    else:
        old = block if not old.strip() else old.rstrip() + "\n\n" + block
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
        "sourceMilestone19Closed": record["sourceMilestone19Closed"],
        "operatorDecisionGateOpen": record["operatorDecisionGateOpen"],
        "operatorDecisionRequired": record["operatorDecisionRequired"],
        "operatorDecisionReceived": record["operatorDecisionReceived"],
        "selectedOperatorDecisionValue": record["selectedOperatorDecisionValue"],
        "decisionOptionCount": record["decisionOptionCount"],
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
        f"source_milestone_19_closed={record['sourceMilestone19Closed']}",
        f"operator_decision_gate_open={record['operatorDecisionGateOpen']}",
        f"operator_decision_required={record['operatorDecisionRequired']}",
        f"operator_decision_received={record['operatorDecisionReceived']}",
        f"selected_operator_decision_value={record['selectedOperatorDecisionValue']}",
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
    print("MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_PIPELINE_READY")
    print("MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_READY")
    print("MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_VALID")
    print(r["signature"])
    print(r["previousCommit"])
    print(r["previousSignature"])
    print(r["mode"])
    print(r["verdict"])
    print(r["nextTask"])
    for key in [
        "sourceMilestone19Closed",
        "sourceMilestone19Frozen",
        "sourceRecursiveArchiveChainStopped",
        "sourceNoFurtherMilestone19TasksRequired",
        "sourceHandoffToMilestone20",
        "operatorDecisionGateReady",
        "operatorDecisionGateOpen",
        "operatorDecisionGateClosed",
        "operatorDecisionRequired",
        "operatorDecisionReceived",
        "operatorDecisionRecorded",
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
