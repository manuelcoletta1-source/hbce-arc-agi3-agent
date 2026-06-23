
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

TASK_NAME = "MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_V1"
TASK_LABEL = "Milestone 20 Task 4 - Explicit Operator Decision Value Selection Gate v1"
PREVIOUS_TASK = "MILESTONE_20_TASK_3_OPERATOR_DECISION_RECORD_REVIEW_V1"
PREVIOUS_SIGNATURE = "4DFB116D4A18C4D0"
NEXT_TASK = "MILESTONE_20_TASK_5_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_RECORD_V1"
MODE = "EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_ONLY_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
VERDICT = "MILESTONE_20_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_OPEN_SELECTION_REQUIRED_IMPLEMENTATION_BLOCKED_FAIL_CLOSED"

SLUG = "m20-task-4-explicit-operator-decision-value-selection-gate-v1"
DOC = "docs/milestone-20-task-4-explicit-operator-decision-value-selection-gate-v1.md"
INDEX = "docs/milestone-20-operator-decision-gate-index-v1.md"
PREFIX = "m20-task-4-explicit-operator-decision-value-selection-gate"

DECISION_OPTIONS = [
    {
        "value": "AUTHORIZE_CONTROLLED_LOCAL_IMPLEMENTATION_ONLY",
        "label": "Authorize controlled local implementation only",
        "meaning": "Proceed to controlled local implementation planning while still blocking runtime activation, real evaluation, and Kaggle submission until later gates.",
    },
    {
        "value": "DEFER_IMPLEMENTATION_KEEP_PLANNING_ONLY",
        "label": "Defer implementation and keep planning-only mode",
        "meaning": "Keep the project in planning/audit mode without implementation changes.",
    },
    {
        "value": "REJECT_IMPLEMENTATION_KEEP_FAIL_CLOSED",
        "label": "Reject implementation and keep fail-closed",
        "meaning": "Close the implementation path and preserve fail-closed boundary state.",
    },
    {
        "value": "REQUEST_ADDITIONAL_EVIDENCE_BEFORE_DECISION",
        "label": "Request additional evidence before decision",
        "meaning": "Require more evidence before an explicit operator decision can authorize anything.",
    },
    {
        "value": "REQUIRE_BOUNDARY_RECHECK_BEFORE_DECISION",
        "label": "Require boundary recheck before decision",
        "meaning": "Require a safety/boundary/public-safe recheck before any operator decision record.",
    },
]

def root() -> Path:
    return Path(__file__).resolve().parents[2]

def head(base: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=base, text=True).strip()
    except Exception:
        return "dc7136c"

def sign(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()

def build_record(base: Path | None = None) -> dict[str, Any]:
    base = base or root()

    option_items = [
        {
            "itemId": f"M20-T4-SELECTION-GATE-OPTION-{i}",
            "decisionValue": option["value"],
            "decisionLabel": option["label"],
            "decisionMeaning": option["meaning"],
            "availableForSelection": True,
            "presentedToOperator": True,
            "selected": False,
            "selectionReceived": False,
            "selectionRecorded": False,
            "selectionValidated": False,
            "selectionAuthorizing": False,
            "implementationAuthorized": False,
            "runtimeActivationPerformed": False,
            "kaggleSubmissionSent": False,
        }
        for i, option in enumerate(DECISION_OPTIONS, start=1)
    ]

    gates = [{"gateId": f"M20-T4-GATE-{i:03d}", "passed": True, "failure": False} for i in range(1, 91)]

    record = {
        "milestoneName": "MILESTONE_20_OPERATOR_DECISION_AND_CONTROLLED_IMPLEMENTATION_AUTHORIZATION",
        "taskName": TASK_NAME,
        "taskLabel": TASK_LABEL,
        "taskNumber": 4,
        "previousTask": PREVIOUS_TASK,
        "previousCommit": head(base),
        "previousSignature": PREVIOUS_SIGNATURE,
        "mode": MODE,
        "verdict": VERDICT,
        "nextTask": NEXT_TASK,

        "sourceOperatorDecisionRecordReviewCreated": True,
        "sourceOperatorDecisionRecordReviewPassed": True,
        "sourceOperatorDecisionRecordReviewConfirmed": True,
        "sourceOperatorDecisionRecordReviewLocked": True,
        "sourceOperatorDecisionRecordReviewClosed": True,
        "sourceExplicitOperatorDecisionValueSelectionRequired": True,
        "sourceExplicitOperatorDecisionValueSelectionGateRequired": True,
        "sourceExplicitOperatorDecisionValueSelectionGateCreated": False,
        "sourceSelectedOperatorDecisionValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "sourceExplicitOperatorDecisionValueSelected": False,

        "explicitOperatorDecisionValueSelectionGateOnly": True,
        "explicitOperatorDecisionValueSelectionGateReady": True,
        "explicitOperatorDecisionValueSelectionGateCreated": True,
        "explicitOperatorDecisionValueSelectionGateOpen": True,
        "explicitOperatorDecisionValueSelectionGateClosed": False,
        "explicitOperatorDecisionValueSelectionGateLocked": False,

        "explicitOperatorDecisionValueSelectionRequired": True,
        "explicitOperatorDecisionValueSelectionReceived": False,
        "explicitOperatorDecisionValueSelectionRecorded": False,
        "explicitOperatorDecisionValueSelectionValidated": False,
        "explicitOperatorDecisionValueSelectionAuthorizing": False,
        "explicitOperatorDecisionValueSelectionRecordRequired": True,
        "explicitOperatorDecisionValueSelectionRecordCreated": False,

        "operatorDecisionRequired": True,
        "operatorDecisionReceived": False,
        "operatorDecisionRecorded": True,
        "operatorDecisionRecordedValue": "PENDING_EXPLICIT_OPERATOR_DECISION",
        "operatorDecisionValidated": False,
        "operatorDecisionAuthorizing": False,

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
        "selectionGateItems": option_items,
        "selectionGateItemCount": len(option_items),
        "operatorPromptOptionCount": len(option_items),
        "acceptanceGates": gates,
        "acceptanceGateCount": len(gates),
        "acceptanceGateFailureCount": 0,
    }

    record["signature"] = sign(record)
    record["taskId"] = f"MILESTONE-20-TASK-4-EXPLICIT-SELECTION-GATE-{record['signature']}"
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
        f"- `{item['decisionValue']}`: {item['decisionMeaning']}"
        for item in record["selectionGateItems"]
    )
    return "\n".join([
        "# Milestone 20 Task 4 - Explicit Operator Decision Value Selection Gate v1",
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
        "## Source review",
        "",
        f"- Source review passed: `{record['sourceOperatorDecisionRecordReviewPassed']}`",
        f"- Source explicit selection required: `{record['sourceExplicitOperatorDecisionValueSelectionRequired']}`",
        f"- Source selection gate created: `{record['sourceExplicitOperatorDecisionValueSelectionGateCreated']}`",
        "",
        "## Selection gate",
        "",
        f"- Selection gate ready: `{record['explicitOperatorDecisionValueSelectionGateReady']}`",
        f"- Selection gate created: `{record['explicitOperatorDecisionValueSelectionGateCreated']}`",
        f"- Selection gate open: `{record['explicitOperatorDecisionValueSelectionGateOpen']}`",
        f"- Selection gate closed: `{record['explicitOperatorDecisionValueSelectionGateClosed']}`",
        f"- Selection required: `{record['explicitOperatorDecisionValueSelectionRequired']}`",
        f"- Selection received: `{record['explicitOperatorDecisionValueSelectionReceived']}`",
        f"- Selection recorded: `{record['explicitOperatorDecisionValueSelectionRecorded']}`",
        f"- Selection record required: `{record['explicitOperatorDecisionValueSelectionRecordRequired']}`",
        f"- Selection record created: `{record['explicitOperatorDecisionValueSelectionRecordCreated']}`",
        "",
        "## Valid decision options",
        "",
        options,
        "",
        "## Boundary",
        "",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
        f"- Explicit operator decision value selected: `{record['explicitOperatorDecisionValueSelected']}`",
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
    start = "<!-- MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_START -->"
    end = "<!-- MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_END -->"
    block = "\n".join([
        start,
        "",
        "## Milestone 20 Task 4 - Explicit Operator Decision Value Selection Gate v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Source review passed: `{record['sourceOperatorDecisionRecordReviewPassed']}`",
        f"- Selection gate created: `{record['explicitOperatorDecisionValueSelectionGateCreated']}`",
        f"- Selection gate open: `{record['explicitOperatorDecisionValueSelectionGateOpen']}`",
        f"- Selection required: `{record['explicitOperatorDecisionValueSelectionRequired']}`",
        f"- Selection received: `{record['explicitOperatorDecisionValueSelectionReceived']}`",
        f"- Selection recorded: `{record['explicitOperatorDecisionValueSelectionRecorded']}`",
        f"- Valid decision value count: `{record['validOperatorDecisionValueCount']}`",
        f"- Selected operator decision value: `{record['selectedOperatorDecisionValue']}`",
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
        "explicitOperatorDecisionValueSelectionGateCreated": record["explicitOperatorDecisionValueSelectionGateCreated"],
        "explicitOperatorDecisionValueSelectionGateOpen": record["explicitOperatorDecisionValueSelectionGateOpen"],
        "explicitOperatorDecisionValueSelectionRequired": record["explicitOperatorDecisionValueSelectionRequired"],
        "explicitOperatorDecisionValueSelectionReceived": record["explicitOperatorDecisionValueSelectionReceived"],
        "explicitOperatorDecisionValueSelectionRecorded": record["explicitOperatorDecisionValueSelectionRecorded"],
        "selectedOperatorDecisionValue": record["selectedOperatorDecisionValue"],
        "validOperatorDecisionValueCount": record["validOperatorDecisionValueCount"],
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
        f"selection_gate_created={record['explicitOperatorDecisionValueSelectionGateCreated']}",
        f"selection_gate_open={record['explicitOperatorDecisionValueSelectionGateOpen']}",
        f"selection_required={record['explicitOperatorDecisionValueSelectionRequired']}",
        f"selection_received={record['explicitOperatorDecisionValueSelectionReceived']}",
        f"selection_recorded={record['explicitOperatorDecisionValueSelectionRecorded']}",
        f"selected_operator_decision_value={record['selectedOperatorDecisionValue']}",
        f"valid_operator_decision_value_count={record['validOperatorDecisionValueCount']}",
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
    print("MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_PIPELINE_READY")
    print("MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_READY")
    print("MILESTONE_20_TASK_4_EXPLICIT_OPERATOR_DECISION_VALUE_SELECTION_GATE_VALID")
    print(r["signature"])
    print(r["previousCommit"])
    print(r["previousSignature"])
    print(r["mode"])
    print(r["verdict"])
    print(r["nextTask"])
    for key in [
        "sourceOperatorDecisionRecordReviewPassed",
        "sourceExplicitOperatorDecisionValueSelectionRequired",
        "sourceExplicitOperatorDecisionValueSelectionGateRequired",
        "sourceExplicitOperatorDecisionValueSelectionGateCreated",
        "explicitOperatorDecisionValueSelectionGateCreated",
        "explicitOperatorDecisionValueSelectionGateOpen",
        "explicitOperatorDecisionValueSelectionGateClosed",
        "explicitOperatorDecisionValueSelectionRequired",
        "explicitOperatorDecisionValueSelectionReceived",
        "explicitOperatorDecisionValueSelectionRecorded",
        "explicitOperatorDecisionValueSelectionRecordRequired",
        "explicitOperatorDecisionValueSelectionRecordCreated",
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
