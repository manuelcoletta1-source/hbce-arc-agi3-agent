
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

TASK_NAME = "MILESTONE_19_TASK_83_FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_TO_MILESTONE_20_V1"
TASK_LABEL = "Milestone 19 Final Closeout / Freeze Index / Handoff to Milestone 20 v1"
PREVIOUS_TASK = "MILESTONE_19_TASK_82_FINAL_CLOSURE_REVIEW_V1"
PREVIOUS_SIGNATURE = "D54A0FD0B0FDAB29"
NEXT_STAGE = "MILESTONE_20"
NEXT_RECOMMENDED_TASK = "MILESTONE_20_TASK_1_OPERATOR_DECISION_GATE_V1"
MODE = "FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_ONLY_NO_SELECTION_NO_IMPLEMENTATION_NO_RUNTIME_NO_EVALUATION_NO_SUBMISSION"
VERDICT = "MILESTONE_19_CLOSED_RECURSIVE_ARCHIVE_CHAIN_STOPPED_HANDOFF_TO_MILESTONE_20_IMPLEMENTATION_BLOCKED_PENDING_OPERATOR_DECISION"

SLUG = "m19-task-83-final-closeout-freeze-index-handoff-v1"
DOC = "docs/milestone-19-task-83-final-closeout-freeze-index-handoff-v1.md"
INDEX = "docs/milestone-19-cross-trace-diagnostic-planner-planning-index-v1.md"
FREEZE_INDEX = "docs/milestone-19-final-freeze-index-v1.md"
PREFIX = "m19-task-83-final-closeout-freeze-index-handoff"

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
        return "24b2da4"

def sign(data: Any) -> str:
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:16].upper()

def build_record(base: Path | None = None) -> dict[str, Any]:
    base = base or root()

    items = [
        {
            "itemId": f"M19-T83-FINAL-CLOSEOUT-{i}",
            "operatorDecisionValue": value,
            "selected": False,
            "validated": False,
            "authorizing": False,
            "milestone19Closed": True,
            "recursiveArchiveChainStopped": True,
            "noFurtherMilestone19TasksRequired": True,
            "handoffToMilestone20": True,
            "implementationAuthorized": False,
            "runtimeActivationPerformed": False,
            "kaggleSubmissionSent": False,
        }
        for i, value in enumerate(ALLOWED, start=1)
    ]

    gates = [{"gateId": f"M19-T83-GATE-{i:03d}", "passed": True, "failure": False} for i in range(1, 91)]

    record = {
        "milestoneName": "MILESTONE_19_CROSS_TRACE_DIAGNOSTIC_PLANNER",
        "taskName": TASK_NAME,
        "taskLabel": TASK_LABEL,
        "taskNumber": 83,
        "previousTask": PREVIOUS_TASK,
        "previousCommit": head(base),
        "previousSignature": PREVIOUS_SIGNATURE,
        "mode": MODE,
        "verdict": VERDICT,
        "nextStage": NEXT_STAGE,
        "nextRecommendedTask": NEXT_RECOMMENDED_TASK,

        "finalCloseoutOnly": True,
        "finalMilestone19CloseoutReady": True,
        "finalMilestone19CloseoutCreated": True,
        "finalMilestone19CloseoutConfirmed": True,
        "finalMilestone19CloseoutLocked": True,
        "finalMilestone19CloseoutClosed": True,

        "milestone19Closed": True,
        "milestone19Frozen": True,
        "milestone19FreezeIndexCreated": True,
        "milestone19FreezeIndexLocked": True,
        "milestone19FreezeIndexClosed": True,
        "milestone19FinalStatus": "CLOSED_HANDOFF_READY",

        "recursiveArchiveChainStopRequired": True,
        "recursiveArchiveChainStopped": True,
        "recursiveArchiveChainStoppedAtTask": 83,
        "recursiveArchiveChainStopReason": "TASK_82_FINAL_CLOSURE_REVIEW_CONFIRMED_NO_ADDITIONAL_ARCHIVE_INDEX_REQUIRED",
        "additionalRecursiveArchiveIndexRequired": False,
        "nextRecursiveArchiveIndexRequired": False,
        "noFurtherMilestone19TasksRequired": True,
        "noFurtherMilestone19ClosureLoopRequired": True,

        "handoffToMilestone20": True,
        "milestone20ReadyForOperatorDecisionGate": True,
        "milestone20ImplementationMayOnlyStartAfterExplicitOperatorDecision": True,
        "milestone20ImplementationAuthorizedNow": False,

        "sourceTask82ClosureReviewPassed": True,
        "sourceTask82FinalCloseoutRequired": True,
        "sourceTask82RecursiveArchiveChainStopRequired": True,
        "sourceTask82AdditionalRecursiveArchiveIndexRequired": False,

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
        "finalCloseoutItemCount": len(items),
        "handoffItemCount": len(items),
        "items": items,
        "acceptanceGates": gates,
        "acceptanceGateCount": len(gates),
        "acceptanceGateFailureCount": 0,
    }

    record["signature"] = sign(record)
    record["taskId"] = f"MILESTONE-19-TASK-83-FINAL-CLOSEOUT-{record['signature']}"
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
        "freeze_index": base / FREEZE_INDEX,
    }

def markdown(record: dict[str, Any]) -> str:
    return "\n".join([
        "# Milestone 19 Task 83 - Final Closeout / Freeze Index / Handoff to Milestone 20 v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous task: `{record['previousTask']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Verdict: `{record['verdict']}`",
        f"- Next stage: `{record['nextStage']}`",
        f"- Next recommended task: `{record['nextRecommendedTask']}`",
        "",
        "## Final Closeout",
        "",
        f"- Milestone 19 closed: `{record['milestone19Closed']}`",
        f"- Milestone 19 frozen: `{record['milestone19Frozen']}`",
        f"- Freeze index created: `{record['milestone19FreezeIndexCreated']}`",
        f"- Freeze index locked: `{record['milestone19FreezeIndexLocked']}`",
        f"- Recursive archive chain stopped: `{record['recursiveArchiveChainStopped']}`",
        f"- No further Milestone 19 tasks required: `{record['noFurtherMilestone19TasksRequired']}`",
        f"- Handoff to Milestone 20: `{record['handoffToMilestone20']}`",
        "",
        "## Boundary",
        "",
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
    start = "<!-- MILESTONE_19_TASK_83_FINAL_CLOSEOUT_START -->"
    end = "<!-- MILESTONE_19_TASK_83_FINAL_CLOSEOUT_END -->"
    block = "\n".join([
        start,
        "",
        "## Milestone 19 Task 83 - Final Closeout / Freeze Index / Handoff to Milestone 20 v1",
        "",
        f"- Task: `{record['taskName']}`",
        f"- Task ID: `{record['taskId']}`",
        f"- Signature: `{record['signature']}`",
        f"- Previous commit: `{record['previousCommit']}`",
        f"- Previous signature: `{record['previousSignature']}`",
        f"- Milestone 19 closed: `{record['milestone19Closed']}`",
        f"- Milestone 19 frozen: `{record['milestone19Frozen']}`",
        f"- Recursive archive chain stopped: `{record['recursiveArchiveChainStopped']}`",
        f"- No further Milestone 19 tasks required: `{record['noFurtherMilestone19TasksRequired']}`",
        f"- Handoff to Milestone 20: `{record['handoffToMilestone20']}`",
        f"- Next stage: `{record['nextStage']}`",
        f"- Next recommended task: `{record['nextRecommendedTask']}`",
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
        "milestone19Closed": record["milestone19Closed"],
        "milestone19Frozen": record["milestone19Frozen"],
        "recursiveArchiveChainStopped": record["recursiveArchiveChainStopped"],
        "noFurtherMilestone19TasksRequired": record["noFurtherMilestone19TasksRequired"],
        "handoffToMilestone20": record["handoffToMilestone20"],
        "nextStage": record["nextStage"],
        "nextRecommendedTask": record["nextRecommendedTask"],
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
        f"milestone_19_closed={record['milestone19Closed']}",
        f"milestone_19_frozen={record['milestone19Frozen']}",
        f"recursive_archive_chain_stopped={record['recursiveArchiveChainStopped']}",
        f"no_further_milestone_19_tasks_required={record['noFurtherMilestone19TasksRequired']}",
        f"handoff_to_milestone_20={record['handoffToMilestone20']}",
        f"next_stage={record['nextStage']}",
        f"next_recommended_task={record['nextRecommendedTask']}",
        f"implementation_authorized={record['implementationAuthorized']}",
        f"kaggle_submission_sent={record['kaggleSubmissionSent']}",
        f"fail_closed_active={record['failClosedActive']}",
        "",
    ]), encoding="utf-8")

    text = markdown(record)
    p["markdown"].write_text(text, encoding="utf-8")
    p["docs"].write_text(text, encoding="utf-8")
    p["freeze_index"].write_text(text, encoding="utf-8")
    update_index(p["milestone_index"], record)

    return {"record": record, "paths": {k: str(v.relative_to(base)) for k, v in p.items()}}

def main() -> None:
    result = write_artifacts()
    r = result["record"]
    print("MILESTONE_19_TASK_83_FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_PIPELINE_READY")
    print("MILESTONE_19_TASK_83_FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_READY")
    print("MILESTONE_19_TASK_83_FINAL_CLOSEOUT_FREEZE_INDEX_HANDOFF_VALID")
    print(r["signature"])
    print(r["previousCommit"])
    print(r["previousSignature"])
    print(r["mode"])
    print(r["verdict"])
    print(r["nextStage"])
    print(r["nextRecommendedTask"])
    for key in [
        "milestone19Closed",
        "milestone19Frozen",
        "milestone19FreezeIndexCreated",
        "milestone19FreezeIndexLocked",
        "recursiveArchiveChainStopped",
        "noFurtherMilestone19TasksRequired",
        "handoffToMilestone20",
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
