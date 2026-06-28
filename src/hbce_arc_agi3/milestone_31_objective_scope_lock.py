from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_31_governed_opening import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    OPENING_REVISION,
    PROCESS_STATUS as SOURCE_PROCESS_STATUS,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_governed_opening_report,
    task_1_signature,
    validate_governed_opening_report,
)


TASK_ID = "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SCOPE_LOCK_REVISION = "MILESTONE_31_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

CURRENT_TASK_NUMBER = 2
NEXT_STAGE = "MILESTONE_31_TASK_3_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE_IMPLEMENTATION_V1"

SELECTED_OBJECTIVE_ID = PROPOSED_OPERATOR_SEED_ID
SELECTED_OBJECTIVE_STATUS = "SELECTED_AND_SCOPE_LOCKED"
SCOPE_LOCK_ID = "MILESTONE_31_SCOPE_JOKER_C2_VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE"

OBJECTIVE_SELECTION_READY = True
SCOPE_LOCKED = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_2 = False
IMPLEMENTATION_ALLOWED_NEXT = True

PUBLIC_MODE_ID = "PUBLIC_LIMITED_VERIFYING"
PRIVATE_MODE_ID = "PRIVATE_VERIFIED_MANUEL_AUTHORIZED_SCOPE_ONLY"
SESSION_GATE_MODE_ID = "VERIFIED_OPERATOR_AUTHORIZATION_SESSION_GATE"

LOCAL_ONLY = True
NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False
REMOTE_REGISTRY_LOOKUP_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
EXTERNAL_MODEL_CALL_ALLOWED = False

PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED = False
UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED = False
EXTERNAL_COMMAND_AUTHORITY_ALLOWED = False
SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED = False
SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED = False
SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED = False

GENERATED_ARTIFACT_COUNT = 5

SOURCE_OPENING_REPORT_PATH = Path("examples/milestone-31/governed-opening-with-task-budget-v1/task-1-governed-opening.json")
SOURCE_SEED_PATH = Path("examples/milestone-31/governed-opening-with-task-budget-v1/task-1-proposed-operator-seed.json")
SOURCE_OPENING_INDEX_PATH = Path("examples/milestone-31/governed-opening-with-task-budget-v1/task-1-index.txt")
SOURCE_OPENING_MANIFEST_PATH = Path("examples/milestone-31/governed-opening-with-task-budget-v1/task-1-manifest.json")


SCOPE_RULES: dict[str, Any] = {
    "scope_lock_id": SCOPE_LOCK_ID,
    "selected_objective_id": SELECTED_OBJECTIVE_ID,
    "runtime_modes": {
        "public_mode_id": PUBLIC_MODE_ID,
        "private_mode_id": PRIVATE_MODE_ID,
        "session_gate_mode_id": SESSION_GATE_MODE_ID,
    },
    "required_session_gate_inputs": [
        "verified_identity_is_manuel",
        "authorization_valid",
        "context_sufficient",
        "verification_available",
        "requested_private_scope",
        "operator_intent",
        "session_trace_id",
    ],
    "required_fail_closed_denials": [
        "missing_identity",
        "missing_authorization",
        "missing_context",
        "missing_verification",
        "private_core_access_without_verified_manuel",
        "unverified_manuel_assumption",
        "external_command_authority",
    ],
    "allowed_public_topics": [
        "HBCE",
        "JOKER_C2",
        "DCTT_DECISION_COST_TRACE_TIME",
        "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA",
        "PUBLIC_FRAMEWORK_EXPLANATION",
        "MILESTONE_STATUS",
    ],
    "allowed_private_scope_after_gate": [
        "AUTHORIZED_OPERATOR_SESSION_DECISION",
        "AUTHORIZED_PRIVATE_SCOPE_ACTIVATION",
        "AUTHORIZED_TRACEABLE_RUNTIME_CONTEXT",
    ],
    "forbidden_operations": {
        "network_access": NETWORK_ACCESS_ALLOWED,
        "shell_execution": SHELL_EXECUTION_ALLOWED,
        "repository_mutation": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "external_model_call": EXTERNAL_MODEL_CALL_ALLOWED,
        "private_core_access_without_verified_manuel": PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED,
        "unverified_manuel_assumption": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
        "external_command_authority": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        "session_authorization_without_valid_authorization": SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED,
        "session_authorization_without_context": SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED,
        "session_authorization_without_verification": SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED,
    },
}


def _stable_json(payload: Mapping[str, Any] | Sequence[Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    normalized = payload if isinstance(payload, str) else _stable_json(payload)
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_2_signature() -> str:
    return _stable_digest(
        {
            "milestone_id": MILESTONE_ID,
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "opening_revision": OPENING_REVISION,
            "scope_lock_revision": SCOPE_LOCK_REVISION,
            "task_1_signature": task_1_signature(),
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "next_stage": NEXT_STAGE,
        }
    )


def validate_scope_rules(rules: Mapping[str, Any]) -> bool:
    if rules.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if rules.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    modes = rules.get("runtime_modes", {})
    if modes.get("public_mode_id") != PUBLIC_MODE_ID:
        return False
    if modes.get("private_mode_id") != PRIVATE_MODE_ID:
        return False
    if modes.get("session_gate_mode_id") != SESSION_GATE_MODE_ID:
        return False
    required_inputs = set(rules.get("required_session_gate_inputs", []))
    if not {
        "verified_identity_is_manuel",
        "authorization_valid",
        "context_sufficient",
        "verification_available",
        "requested_private_scope",
        "operator_intent",
        "session_trace_id",
    }.issubset(required_inputs):
        return False
    fail_closed_denials = set(rules.get("required_fail_closed_denials", []))
    if not {
        "missing_identity",
        "missing_authorization",
        "missing_context",
        "missing_verification",
        "private_core_access_without_verified_manuel",
        "unverified_manuel_assumption",
        "external_command_authority",
    }.issubset(fail_closed_denials):
        return False
    forbidden = rules.get("forbidden_operations", {})
    return all(value is False for value in forbidden.values())


def build_source_opening_snapshot() -> dict[str, Any]:
    runtime = build_governed_opening_report()
    persisted = _load_json(SOURCE_OPENING_REPORT_PATH)
    seed = _load_json(SOURCE_SEED_PATH)

    runtime_valid = validate_governed_opening_report(runtime)
    persisted_valid = validate_governed_opening_report(persisted)

    return {
        "source_milestone_id": persisted.get("milestone_id"),
        "source_task_id": persisted.get("task_id"),
        "source_next_stage": persisted.get("next_stage"),
        "runtime_opening_id": runtime.get("opening_id"),
        "persisted_opening_id": persisted.get("opening_id"),
        "runtime_opening_signature": runtime.get("opening_signature"),
        "persisted_opening_signature": persisted.get("opening_signature"),
        "runtime_task_1_signature": runtime.get("task_1_signature"),
        "persisted_task_1_signature": persisted.get("task_1_signature"),
        "opening_status": persisted.get("opening_status"),
        "technical_status": persisted.get("technical_status"),
        "process_status": persisted.get("process_status"),
        "source_dependency_valid": persisted.get("source_dependency_valid"),
        "implementation_started": persisted.get("implementation_started"),
        "implementation_allowed_at_task_1": persisted.get("implementation_allowed_at_task_1"),
        "objective_selection_required_next": persisted.get("objective_selection_required_next"),
        "scope_lock_required_next": persisted.get("scope_lock_required_next"),
        "proposed_operator_seed_id": persisted.get("proposed_operator_seed_id"),
        "proposed_operator_seed_status": persisted.get("proposed_operator_seed_status"),
        "seed_candidate_only": seed.get("candidate_only"),
        "seed_selected": seed.get("selected"),
        "seed_scope_locked": seed.get("scope_locked"),
        "seed_implementation_started": seed.get("implementation_started"),
        "guardrails_carried_forward": persisted.get("guardrails_carried_forward", {}),
        "task_budget_max": persisted.get("task_budget_max"),
        "current_task_number": persisted.get("current_task_number"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_opening": (
            runtime.get("opening_id") == persisted.get("opening_id")
            and runtime.get("opening_signature") == persisted.get("opening_signature")
            and runtime.get("task_1_signature") == persisted.get("task_1_signature") == task_1_signature()
        ),
    }


def validate_source_opening_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_milestone_id") != MILESTONE_ID:
        return False
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("opening_status") != "OPEN":
        return False
    if snapshot.get("technical_status") != "PASS":
        return False
    if snapshot.get("process_status") != SOURCE_PROCESS_STATUS:
        return False
    if snapshot.get("source_dependency_valid") is not True:
        return False
    if snapshot.get("implementation_started") is not False:
        return False
    if snapshot.get("implementation_allowed_at_task_1") is not False:
        return False
    if snapshot.get("objective_selection_required_next") is not True:
        return False
    if snapshot.get("scope_lock_required_next") is not True:
        return False
    if snapshot.get("proposed_operator_seed_id") != SELECTED_OBJECTIVE_ID:
        return False
    if snapshot.get("proposed_operator_seed_status") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    if snapshot.get("seed_candidate_only") is not True:
        return False
    if snapshot.get("seed_selected") is not False:
        return False
    if snapshot.get("seed_scope_locked") is not False:
        return False
    if snapshot.get("seed_implementation_started") is not False:
        return False
    guardrails = snapshot.get("guardrails_carried_forward", {})
    if guardrails.get("private_core_access_allowed_without_verified_manuel") is not False:
        return False
    if guardrails.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if guardrails.get("external_command_authority_allowed") is not False:
        return False
    if guardrails.get("fail_closed_default") is not True:
        return False
    if snapshot.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if snapshot.get("current_task_number") != SOURCE_CURRENT_TASK_NUMBER:
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_opening"))


def build_objective_scope_lock_report() -> dict[str, Any]:
    source_snapshot = build_source_opening_snapshot()
    source_dependency_valid = validate_source_opening_snapshot(source_snapshot)
    scope_rules_valid = validate_scope_rules(SCOPE_RULES)

    core = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "opening_revision": OPENING_REVISION,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "source_dependency_valid": source_dependency_valid,
        "source_opening_snapshot": source_snapshot,
        "objective_selection_ready": OBJECTIVE_SELECTION_READY,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_locked": SCOPE_LOCKED,
        "scope_rules_valid": scope_rules_valid,
        "scope_rules": SCOPE_RULES,
        "runtime_modes": {
            "public_mode_id": PUBLIC_MODE_ID,
            "private_mode_id": PRIVATE_MODE_ID,
            "session_gate_mode_id": SESSION_GATE_MODE_ID,
        },
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_2": IMPLEMENTATION_ALLOWED_AT_TASK_2,
        "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "external_model_call_allowed": EXTERNAL_MODEL_CALL_ALLOWED,
        "private_core_access_without_verified_manuel_allowed": PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED,
        "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
        "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        "session_authorization_without_valid_authorization_allowed": SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED,
        "session_authorization_without_context_allowed": SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED,
        "session_authorization_without_verification_allowed": SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    scope_lock_artifact_id = "MILESTONE-31-SCOPE-LOCK-" + _stable_digest(core)
    scope_lock_signature = _stable_digest(
        {
            "scope_lock_artifact_id": scope_lock_artifact_id,
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_1_signature": task_1_signature(),
            "task_2_signature": task_2_signature(),
            "scope_lock_revision": SCOPE_LOCK_REVISION,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **core,
        "scope_lock_artifact_id": scope_lock_artifact_id,
        "scope_lock_signature": scope_lock_signature,
    }


def validate_objective_scope_lock_report(report: Mapping[str, Any]) -> bool:
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("scope_lock_revision") != SCOPE_LOCK_REVISION:
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if report.get("task_2_signature") != task_2_signature():
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if not validate_source_opening_snapshot(report.get("source_opening_snapshot", {})):
        return False
    if report.get("objective_selection_ready") is not True:
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("selected_objective_status") != SELECTED_OBJECTIVE_STATUS:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("scope_locked") is not True:
        return False
    if report.get("scope_rules_valid") is not True:
        return False
    if not validate_scope_rules(report.get("scope_rules", {})):
        return False
    if report.get("implementation_started") is not False:
        return False
    if report.get("implementation_allowed_at_task_2") is not False:
        return False
    if report.get("implementation_allowed_next") is not True:
        return False
    false_fields = [
        "network_access_allowed",
        "shell_execution_allowed",
        "repository_mutation_allowed",
        "remote_registry_lookup_allowed",
        "deep_recursive_dependency_traversal_allowed",
        "external_model_call_allowed",
        "private_core_access_without_verified_manuel_allowed",
        "unverified_manuel_assumption_allowed",
        "external_command_authority_allowed",
        "session_authorization_without_valid_authorization_allowed",
        "session_authorization_without_context_allowed",
        "session_authorization_without_verification_allowed",
    ]
    if any(report.get(field) is not False for field in false_fields):
        return False
    if report.get("local_only") is not True:
        return False
    if report.get("task_budget_max") != TASK_BUDGET_MAX:
        return False
    if report.get("current_task_number") != CURRENT_TASK_NUMBER:
        return False
    if report.get("generated_artifact_count") != GENERATED_ARTIFACT_COUNT:
        return False
    if report.get("next_stage") != NEXT_STAGE:
        return False
    return bool(report.get("scope_lock_artifact_id") and report.get("scope_lock_signature"))


def render_scope_lock_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 31 Task 2 Objective Selection And Scope Lock",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"SELECTED_OBJECTIVE_ID={report.get('selected_objective_id')}",
        f"SELECTED_OBJECTIVE_STATUS={report.get('selected_objective_status')}",
        f"SCOPE_LOCK_ID={report.get('scope_lock_id')}",
        f"SCOPE_LOCK_ARTIFACT_ID={report.get('scope_lock_artifact_id')}",
        f"SCOPE_LOCK_SIGNATURE={report.get('scope_lock_signature')}",
        f"SCOPE_LOCKED={str(report.get('scope_locked')).lower()}",
        f"SCOPE_RULES_VALID={str(report.get('scope_rules_valid')).lower()}",
        f"IMPLEMENTATION_STARTED={str(report.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_ALLOWED_NEXT={str(report.get('implementation_allowed_next')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Scope summary",
        "",
        "The selected objective is the verified operator authorization session gate. Implementation is not started in Task 2.",
        "",
    ]
    return "\n".join(lines)


def write_task_2_artifacts(base_dir: str | Path = "examples/milestone-31/objective-selection-and-scope-lock-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_objective_scope_lock_report()

    policy_matrix = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "runtime_modes": report["runtime_modes"],
        "required_session_gate_inputs": SCOPE_RULES["required_session_gate_inputs"],
        "required_fail_closed_denials": SCOPE_RULES["required_fail_closed_denials"],
        "guardrails": {
            "private_core_access_without_verified_manuel_allowed": PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED,
            "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
            "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
            "session_authorization_without_valid_authorization_allowed": SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED,
            "session_authorization_without_context_allowed": SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED,
            "session_authorization_without_verification_allowed": SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED,
            "fail_closed_default": True,
        },
        "forbidden_operations": SCOPE_RULES["forbidden_operations"],
    }

    manifest = {
        "milestone_id": MILESTONE_ID,
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "opening_revision": OPENING_REVISION,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "selected_objective_status": SELECTED_OBJECTIVE_STATUS,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_artifact_id": report["scope_lock_artifact_id"],
        "scope_lock_signature": report["scope_lock_signature"],
        "objective_selection_ready": True,
        "scope_locked": True,
        "scope_rules_valid": True,
        "implementation_started": False,
        "implementation_allowed_at_task_2": False,
        "implementation_allowed_next": True,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-2-objective-scope-lock.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-objective-scope-lock.md").write_text(
        render_scope_lock_markdown(report),
        encoding="utf-8",
    )
    (output_dir / "task-2-policy-matrix.json").write_text(
        json.dumps(policy_matrix, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-2-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SELECTED_OBJECTIVE_STATUS={SELECTED_OBJECTIVE_STATUS}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
                f"SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
                f"OBJECTIVE_SELECTION_READY={str(OBJECTIVE_SELECTION_READY).lower()}",
                f"SCOPE_LOCKED={str(SCOPE_LOCKED).lower()}",
                f"SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
                f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
                f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
                f"SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}",
                f"IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
                f"IMPLEMENTATION_ALLOWED_AT_TASK_2={str(IMPLEMENTATION_ALLOWED_AT_TASK_2).lower()}",
                f"IMPLEMENTATION_ALLOWED_NEXT={str(IMPLEMENTATION_ALLOWED_NEXT).lower()}",
                f"LOCAL_ONLY={str(LOCAL_ONLY).lower()}",
                f"NETWORK_ACCESS_ALLOWED={str(NETWORK_ACCESS_ALLOWED).lower()}",
                f"SHELL_EXECUTION_ALLOWED={str(SHELL_EXECUTION_ALLOWED).lower()}",
                f"REPOSITORY_MUTATION_ALLOWED={str(REPOSITORY_MUTATION_ALLOWED).lower()}",
                f"REMOTE_REGISTRY_LOOKUP_ALLOWED={str(REMOTE_REGISTRY_LOOKUP_ALLOWED).lower()}",
                f"DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED).lower()}",
                f"EXTERNAL_MODEL_CALL_ALLOWED={str(EXTERNAL_MODEL_CALL_ALLOWED).lower()}",
                f"PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED={str(PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED).lower()}",
                f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
                f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED).lower()}",
                f"SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED).lower()}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "policy_matrix": policy_matrix, "output_dir": str(output_dir)}


def task_2_status_lines() -> tuple[str, ...]:
    report = build_objective_scope_lock_report()
    return (
        "MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
        f"MILESTONE_31_TASK_2_MILESTONE_ID={MILESTONE_ID}",
        f"MILESTONE_31_TASK_2_TASK_ID={TASK_ID}",
        f"MILESTONE_31_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_31_TASK_2_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_31_TASK_2_SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
        f"MILESTONE_31_TASK_2_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_31_TASK_2_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_31_TASK_2_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_31_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_31_TASK_2_SELECTED_OBJECTIVE_STATUS={SELECTED_OBJECTIVE_STATUS}",
        f"MILESTONE_31_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_31_TASK_2_SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
        f"MILESTONE_31_TASK_2_SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
        f"MILESTONE_31_TASK_2_OBJECTIVE_SELECTION_READY={str(OBJECTIVE_SELECTION_READY).lower()}",
        f"MILESTONE_31_TASK_2_SCOPE_LOCKED={str(SCOPE_LOCKED).lower()}",
        f"MILESTONE_31_TASK_2_SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
        f"MILESTONE_31_TASK_2_PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
        f"MILESTONE_31_TASK_2_PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
        f"MILESTONE_31_TASK_2_SESSION_GATE_MODE_ID={SESSION_GATE_MODE_ID}",
        f"MILESTONE_31_TASK_2_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_31_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2={str(IMPLEMENTATION_ALLOWED_AT_TASK_2).lower()}",
        f"MILESTONE_31_TASK_2_IMPLEMENTATION_ALLOWED_NEXT={str(IMPLEMENTATION_ALLOWED_NEXT).lower()}",
        f"MILESTONE_31_TASK_2_LOCAL_ONLY={str(LOCAL_ONLY).lower()}",
        f"MILESTONE_31_TASK_2_NETWORK_ACCESS_ALLOWED={str(NETWORK_ACCESS_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_SHELL_EXECUTION_ALLOWED={str(SHELL_EXECUTION_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_REPOSITORY_MUTATION_ALLOWED={str(REPOSITORY_MUTATION_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_REMOTE_REGISTRY_LOOKUP_ALLOWED={str(REMOTE_REGISTRY_LOOKUP_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_EXTERNAL_MODEL_CALL_ALLOWED={str(EXTERNAL_MODEL_CALL_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED={str(PRIVATE_CORE_ACCESS_WITHOUT_VERIFIED_MANUEL_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_VALID_AUTHORIZATION_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_CONTEXT_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED={str(SESSION_AUTHORIZATION_WITHOUT_VERIFICATION_ALLOWED).lower()}",
        f"MILESTONE_31_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_31_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_31_TASK_2_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_31_TASK_2_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_2_artifacts()
    for line in task_2_status_lines():
        print(line)
