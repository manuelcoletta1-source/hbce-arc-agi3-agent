from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from hbce_arc_agi3.milestone_30_governed_opening import (
    CURRENT_TASK_NUMBER as SOURCE_CURRENT_TASK_NUMBER,
    GENERATED_ARTIFACT_COUNT as SOURCE_GENERATED_ARTIFACT_COUNT,
    MILESTONE_ID,
    NEXT_STAGE as SOURCE_NEXT_STAGE,
    OPENING_REVISION,
    PROPOSED_OPERATOR_SEED_ID,
    PROPOSED_OPERATOR_SEED_STATUS,
    TASK_BUDGET_MAX,
    TASK_ID as SOURCE_TASK_ID,
    build_governed_opening_report,
    task_1_signature,
    validate_governed_opening_report,
)


TASK_ID = "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SCOPE_LOCK_REVISION = "MILESTONE_30_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"

CURRENT_TASK_NUMBER = 2
NEXT_STAGE = "MILESTONE_30_TASK_3_IDENTITY_BOUNDARY_FAIL_CLOSED_IMPLEMENTATION_V1"

SELECTED_OBJECTIVE_ID = "JOKER_C2_IDENTITY_BOUNDARY_AND_FAIL_CLOSED_PUBLIC_MODE"
SCOPE_LOCK_ID = "MILESTONE_30_SCOPE_JOKER_C2_IDENTITY_BOUNDARY_AND_FAIL_CLOSED_PUBLIC_MODE"

OBJECTIVE_SELECTION_READY = True
SCOPE_LOCKED = True
IMPLEMENTATION_STARTED = False
IMPLEMENTATION_ALLOWED_AT_TASK_2 = False
IMPLEMENTATION_ALLOWED_NEXT = True

LOCAL_ONLY = True
NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False
REMOTE_REGISTRY_LOOKUP_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
EXTERNAL_MODEL_CALL_ALLOWED = False
PRIVATE_CORE_EXPOSURE_ALLOWED = False
UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED = False
EXTERNAL_COMMAND_AUTHORITY_ALLOWED = False

FORBIDDEN_OPERATION_COUNT = 10
ALLOWED_INPUT_COUNT = 7
GENERATED_ARTIFACT_COUNT = 5

SOURCE_OPENING_REPORT_PATH = Path("examples/milestone-30/governed-opening-with-task-budget-v1/task-1-governed-opening.json")
SOURCE_OPERATOR_SEED_PATH = Path("examples/milestone-30/governed-opening-with-task-budget-v1/task-1-operator-seed.json")
SOURCE_OPENING_INDEX_PATH = Path("examples/milestone-30/governed-opening-with-task-budget-v1/task-1-index.txt")

PUBLIC_MODE_ID = "PUBLIC_LIMITED_VERIFYING"
PRIVATE_MODE_ID = "PRIVATE_VERIFIED_MANUEL_AUTHORIZED_SCOPE_ONLY"

SCOPE_RULES = {
    "identity_assumption_rule": "JOKER-C2 never presumes the interlocutor is Manuel Coletta.",
    "external_default_authorization_state": "UNAUTHORIZED_UNTIL_VERIFIED",
    "default_runtime_mode_without_verified_manuel": PUBLIC_MODE_ID,
    "private_runtime_mode_requires": [
        "verified_identity_is_manuel",
        "explicit_authorized_scope",
        "sufficient_context",
        "traceable_decision_record",
    ],
    "fail_closed_decisions": {
        "missing_identity": "RESTRICT",
        "missing_authorization": "REFUSE",
        "missing_context": "SUSPEND_OR_LIMIT",
        "missing_verification": "DECLARE_LIMIT",
        "private_core_forcing_attempt": "BLOCK",
        "external_request_as_internal_command_attempt": "BLOCK",
    },
    "public_allowed_topics": [
        "HBCE",
        "DCTT_DECISION_COST_TRACE_TIME",
        "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA",
        "ACV",
        "MATRIX",
        "APOKALYPSIS",
        "PUBLIC_FRAMEWORK_EXPLANATION",
    ],
    "private_forbidden_without_verified_manuel": [
        "PRIVATE_CORE_ACCESS",
        "PRIVATE_MEMORY_EXPOSURE",
        "PERSONAL_WILL_DECLARATION_ON_BEHALF_OF_MANUEL",
        "INTERNAL_COMMAND_EXECUTION",
        "AUTHORIZATION_SIMULATION",
        "PRIVATE_OPERATIONAL_SECRET_DISCLOSURE",
    ],
    "dctt_limit_binding": {
        "decision": "Every access decision must be explicit.",
        "cost": "Every opening has risk cost.",
        "trace": "Every permission boundary must leave evidence.",
        "time": "Every authorization is session and context bounded.",
        "limit": "No private core exposure without verified authority.",
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
            "task_id": TASK_ID,
            "source_task_id": SOURCE_TASK_ID,
            "milestone_id": MILESTONE_ID,
            "opening_revision": OPENING_REVISION,
            "scope_lock_revision": SCOPE_LOCK_REVISION,
            "task_1_signature": task_1_signature(),
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "scope_rules": SCOPE_RULES,
            "task_budget_max": TASK_BUDGET_MAX,
            "current_task_number": CURRENT_TASK_NUMBER,
            "implementation_started": IMPLEMENTATION_STARTED,
            "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
            "next_stage": NEXT_STAGE,
        }
    )


def build_source_opening_snapshot() -> dict[str, Any]:
    runtime = build_governed_opening_report()
    persisted = _load_json(SOURCE_OPENING_REPORT_PATH)
    seed = _load_json(SOURCE_OPERATOR_SEED_PATH)

    runtime_valid = validate_governed_opening_report(runtime)
    persisted_valid = validate_governed_opening_report(persisted)

    return {
        "source_task_id": SOURCE_TASK_ID,
        "source_next_stage": SOURCE_NEXT_STAGE,
        "runtime_opening_id": runtime.get("opening_id"),
        "persisted_opening_id": persisted.get("opening_id"),
        "runtime_opening_signature": runtime.get("opening_signature"),
        "persisted_opening_signature": persisted.get("opening_signature"),
        "runtime_task_1_signature": runtime.get("task_1_signature"),
        "persisted_task_1_signature": persisted.get("task_1_signature"),
        "opening_status": persisted.get("opening_status"),
        "technical_status": persisted.get("technical_status"),
        "source_dependency_valid": persisted.get("source_dependency_valid"),
        "implementation_started": persisted.get("implementation_started"),
        "implementation_allowed_at_task_1": persisted.get("implementation_allowed_at_task_1"),
        "objective_selection_required_next": persisted.get("objective_selection_required_next"),
        "scope_lock_required_next": persisted.get("scope_lock_required_next"),
        "proposed_operator_seed_id": persisted.get("proposed_operator_seed", {}).get("seed_id"),
        "proposed_operator_seed_status": persisted.get("proposed_operator_seed", {}).get("status"),
        "operator_seed_file_id": seed.get("proposed_operator_seed", {}).get("seed_id"),
        "operator_seed_file_status": seed.get("proposed_operator_seed", {}).get("status"),
        "operator_seed_implementation_status": seed.get("implementation_status"),
        "runtime_valid": runtime_valid,
        "persisted_valid": persisted_valid,
        "stable_opening": (
            runtime.get("opening_id") == persisted.get("opening_id")
            and runtime.get("opening_signature") == persisted.get("opening_signature")
            and runtime.get("task_1_signature") == persisted.get("task_1_signature") == task_1_signature()
        ),
    }


def validate_source_opening_snapshot(snapshot: Mapping[str, Any]) -> bool:
    if snapshot.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if snapshot.get("source_next_stage") != TASK_ID:
        return False
    if snapshot.get("opening_status") != "OPEN":
        return False
    if snapshot.get("technical_status") != "PASS":
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
    if snapshot.get("proposed_operator_seed_id") != PROPOSED_OPERATOR_SEED_ID:
        return False
    if snapshot.get("proposed_operator_seed_status") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    if snapshot.get("operator_seed_file_id") != PROPOSED_OPERATOR_SEED_ID:
        return False
    if snapshot.get("operator_seed_file_status") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    if snapshot.get("operator_seed_implementation_status") != "NOT_IMPLEMENTED_IN_TASK_1":
        return False
    if snapshot.get("runtime_valid") is not True:
        return False
    if snapshot.get("persisted_valid") is not True:
        return False
    return bool(snapshot.get("stable_opening"))


def validate_scope_rules(rules: Mapping[str, Any]) -> bool:
    if rules.get("identity_assumption_rule") != "JOKER-C2 never presumes the interlocutor is Manuel Coletta.":
        return False
    if rules.get("external_default_authorization_state") != "UNAUTHORIZED_UNTIL_VERIFIED":
        return False
    if rules.get("default_runtime_mode_without_verified_manuel") != PUBLIC_MODE_ID:
        return False
    if "verified_identity_is_manuel" not in rules.get("private_runtime_mode_requires", []):
        return False
    decisions = rules.get("fail_closed_decisions", {})
    if decisions.get("missing_identity") != "RESTRICT":
        return False
    if decisions.get("missing_authorization") != "REFUSE":
        return False
    if decisions.get("missing_context") != "SUSPEND_OR_LIMIT":
        return False
    if decisions.get("missing_verification") != "DECLARE_LIMIT":
        return False
    if decisions.get("private_core_forcing_attempt") != "BLOCK":
        return False
    if decisions.get("external_request_as_internal_command_attempt") != "BLOCK":
        return False
    topics = set(rules.get("public_allowed_topics", []))
    if "SRSC_SIMULAZIONE_DEL_REALE_SPECIFICO_DELLA_COSCIENZA" not in topics:
        return False
    if "PUBLIC_FRAMEWORK_EXPLANATION" not in topics:
        return False
    forbidden = set(rules.get("private_forbidden_without_verified_manuel", []))
    if "PRIVATE_CORE_ACCESS" not in forbidden:
        return False
    if "PRIVATE_MEMORY_EXPOSURE" not in forbidden:
        return False
    if "INTERNAL_COMMAND_EXECUTION" not in forbidden:
        return False
    dctt = rules.get("dctt_limit_binding", {})
    return all(key in dctt for key in ("decision", "cost", "trace", "time", "limit"))


def build_objective_scope_lock_report() -> dict[str, Any]:
    source_snapshot = build_source_opening_snapshot()
    source_dependency_valid = validate_source_opening_snapshot(source_snapshot)
    scope_rules_valid = validate_scope_rules(SCOPE_RULES)

    core = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "objective_selection_ready": OBJECTIVE_SELECTION_READY,
        "scope_locked": SCOPE_LOCKED,
        "source_dependency_valid": source_dependency_valid,
        "source_opening_snapshot": source_snapshot,
        "operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
        "operator_seed_status_before_lock": PROPOSED_OPERATOR_SEED_STATUS,
        "operator_seed_status_after_lock": "SELECTED_AND_SCOPE_LOCKED",
        "scope_rules": SCOPE_RULES,
        "scope_rules_valid": scope_rules_valid,
        "runtime_modes": {
            "public_mode_id": PUBLIC_MODE_ID,
            "private_mode_id": PRIVATE_MODE_ID,
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
        "private_core_exposure_allowed": PRIVATE_CORE_EXPOSURE_ALLOWED,
        "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
        "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        "forbidden_operation_count": FORBIDDEN_OPERATION_COUNT,
        "allowed_input_count": ALLOWED_INPUT_COUNT,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    scope_lock_artifact_id = "MILESTONE-30-SCOPE-LOCK-" + _stable_digest(core)
    scope_lock_signature = _stable_digest(
        {
            "scope_lock_artifact_id": scope_lock_artifact_id,
            "task_id": TASK_ID,
            "selected_objective_id": SELECTED_OBJECTIVE_ID,
            "scope_lock_id": SCOPE_LOCK_ID,
            "task_1_signature": task_1_signature(),
            "task_2_signature": task_2_signature(),
            "operator_seed_id": PROPOSED_OPERATOR_SEED_ID,
            "scope_rules": SCOPE_RULES,
            "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
            "next_stage": NEXT_STAGE,
        }
    )

    return {
        **core,
        "scope_lock_artifact_id": scope_lock_artifact_id,
        "scope_lock_signature": scope_lock_signature,
    }


def validate_objective_scope_lock_report(report: Mapping[str, Any]) -> bool:
    if report.get("task_id") != TASK_ID:
        return False
    if report.get("source_task_id") != SOURCE_TASK_ID:
        return False
    if report.get("milestone_id") != MILESTONE_ID:
        return False
    if report.get("opening_revision") != OPENING_REVISION:
        return False
    if report.get("scope_lock_revision") != SCOPE_LOCK_REVISION:
        return False
    if report.get("task_1_signature") != task_1_signature():
        return False
    if report.get("task_2_signature") != task_2_signature():
        return False
    if report.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if report.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if report.get("objective_selection_ready") is not True:
        return False
    if report.get("scope_locked") is not True:
        return False
    if report.get("source_dependency_valid") is not True:
        return False
    if not validate_source_opening_snapshot(report.get("source_opening_snapshot", {})):
        return False
    if report.get("operator_seed_id") != PROPOSED_OPERATOR_SEED_ID:
        return False
    if report.get("operator_seed_status_before_lock") != PROPOSED_OPERATOR_SEED_STATUS:
        return False
    if report.get("operator_seed_status_after_lock") != "SELECTED_AND_SCOPE_LOCKED":
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
    if report.get("local_only") is not True:
        return False
    if report.get("network_access_allowed") is not False:
        return False
    if report.get("shell_execution_allowed") is not False:
        return False
    if report.get("repository_mutation_allowed") is not False:
        return False
    if report.get("remote_registry_lookup_allowed") is not False:
        return False
    if report.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if report.get("external_model_call_allowed") is not False:
        return False
    if report.get("private_core_exposure_allowed") is not False:
        return False
    if report.get("unverified_manuel_assumption_allowed") is not False:
        return False
    if report.get("external_command_authority_allowed") is not False:
        return False
    if report.get("forbidden_operation_count") != FORBIDDEN_OPERATION_COUNT:
        return False
    if report.get("allowed_input_count") != ALLOWED_INPUT_COUNT:
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
        "# Milestone 30 Task 2 Objective Selection And Scope Lock",
        "",
        f"TASK_ID={report.get('task_id')}",
        f"SOURCE_TASK_ID={report.get('source_task_id')}",
        f"SELECTED_OBJECTIVE_ID={report.get('selected_objective_id')}",
        f"SCOPE_LOCK_ID={report.get('scope_lock_id')}",
        f"SCOPE_LOCK_ARTIFACT_ID={report.get('scope_lock_artifact_id')}",
        f"SCOPE_LOCK_SIGNATURE={report.get('scope_lock_signature')}",
        f"OBJECTIVE_SELECTION_READY={str(report.get('objective_selection_ready')).lower()}",
        f"SCOPE_LOCKED={str(report.get('scope_locked')).lower()}",
        f"SCOPE_RULES_VALID={str(report.get('scope_rules_valid')).lower()}",
        f"IMPLEMENTATION_STARTED={str(report.get('implementation_started')).lower()}",
        f"IMPLEMENTATION_ALLOWED_AT_TASK_2={str(report.get('implementation_allowed_at_task_2')).lower()}",
        f"IMPLEMENTATION_ALLOWED_NEXT={str(report.get('implementation_allowed_next')).lower()}",
        f"LOCAL_ONLY={str(report.get('local_only')).lower()}",
        f"PRIVATE_CORE_EXPOSURE_ALLOWED={str(report.get('private_core_exposure_allowed')).lower()}",
        f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(report.get('unverified_manuel_assumption_allowed')).lower()}",
        f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(report.get('external_command_authority_allowed')).lower()}",
        f"NEXT_STAGE={report.get('next_stage')}",
        "",
        "## Locked objective",
        "",
        "JOKER-C2 identity boundary and fail-closed public mode.",
        "",
        "SRSC is explicitly represented as Simulazione del Reale Specifico della Coscienza in public allowed topics.",
        "",
    ]
    return "\n".join(lines)


def write_task_2_artifacts(base_dir: str | Path = "examples/milestone-30/objective-selection-and-scope-lock-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report = build_objective_scope_lock_report()

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "milestone_id": MILESTONE_ID,
        "opening_revision": OPENING_REVISION,
        "scope_lock_revision": SCOPE_LOCK_REVISION,
        "task_1_signature": task_1_signature(),
        "task_2_signature": task_2_signature(),
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_lock_artifact_id": report["scope_lock_artifact_id"],
        "scope_lock_signature": report["scope_lock_signature"],
        "objective_selection_ready": OBJECTIVE_SELECTION_READY,
        "scope_locked": SCOPE_LOCKED,
        "source_dependency_valid": report["source_dependency_valid"],
        "scope_rules_valid": report["scope_rules_valid"],
        "implementation_started": IMPLEMENTATION_STARTED,
        "implementation_allowed_at_task_2": IMPLEMENTATION_ALLOWED_AT_TASK_2,
        "implementation_allowed_next": IMPLEMENTATION_ALLOWED_NEXT,
        "local_only": LOCAL_ONLY,
        "forbidden_operation_count": FORBIDDEN_OPERATION_COUNT,
        "allowed_input_count": ALLOWED_INPUT_COUNT,
        "task_budget_max": TASK_BUDGET_MAX,
        "current_task_number": CURRENT_TASK_NUMBER,
        "generated_artifact_count": GENERATED_ARTIFACT_COUNT,
        "next_stage": NEXT_STAGE,
    }

    policy_matrix = {
        "task_id": TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "scope_rules": SCOPE_RULES,
        "runtime_modes": report["runtime_modes"],
        "guardrails": {
            "local_only": LOCAL_ONLY,
            "network_access_allowed": NETWORK_ACCESS_ALLOWED,
            "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
            "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
            "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
            "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
            "external_model_call_allowed": EXTERNAL_MODEL_CALL_ALLOWED,
            "private_core_exposure_allowed": PRIVATE_CORE_EXPOSURE_ALLOWED,
            "unverified_manuel_assumption_allowed": UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED,
            "external_command_authority_allowed": EXTERNAL_COMMAND_AUTHORITY_ALLOWED,
        },
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
                "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"MILESTONE_ID={MILESTONE_ID}",
                f"OPENING_REVISION={OPENING_REVISION}",
                f"SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
                f"TASK_1_SIGNATURE={task_1_signature()}",
                f"TASK_2_SIGNATURE={task_2_signature()}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
                f"SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
                f"OBJECTIVE_SELECTION_READY={str(OBJECTIVE_SELECTION_READY).lower()}",
                f"SCOPE_LOCKED={str(SCOPE_LOCKED).lower()}",
                f"SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
                f"OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}",
                "OPERATOR_SEED_STATUS_AFTER_LOCK=SELECTED_AND_SCOPE_LOCKED",
                f"SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
                f"PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
                f"PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
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
                f"PRIVATE_CORE_EXPOSURE_ALLOWED={str(PRIVATE_CORE_EXPOSURE_ALLOWED).lower()}",
                f"UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
                f"EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
                f"FORBIDDEN_OPERATION_COUNT={FORBIDDEN_OPERATION_COUNT}",
                f"ALLOWED_INPUT_COUNT={ALLOWED_INPUT_COUNT}",
                f"TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
                f"CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
                f"GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {"report": report, "manifest": manifest, "output_dir": str(output_dir)}


def task_2_status_lines() -> tuple[str, ...]:
    report = build_objective_scope_lock_report()
    return (
        "MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_READY=true",
        f"MILESTONE_30_TASK_2_SOURCE_TASK_ID={SOURCE_TASK_ID}",
        f"MILESTONE_30_TASK_2_OPENING_REVISION={OPENING_REVISION}",
        f"MILESTONE_30_TASK_2_SCOPE_LOCK_REVISION={SCOPE_LOCK_REVISION}",
        f"MILESTONE_30_TASK_2_TASK_1_SIGNATURE={task_1_signature()}",
        f"MILESTONE_30_TASK_2_TASK_2_SIGNATURE={task_2_signature()}",
        f"MILESTONE_30_TASK_2_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_30_TASK_2_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        f"MILESTONE_30_TASK_2_SCOPE_LOCK_ARTIFACT_ID={report['scope_lock_artifact_id']}",
        f"MILESTONE_30_TASK_2_SCOPE_LOCK_SIGNATURE={report['scope_lock_signature']}",
        f"MILESTONE_30_TASK_2_OBJECTIVE_SELECTION_READY={str(OBJECTIVE_SELECTION_READY).lower()}",
        f"MILESTONE_30_TASK_2_SCOPE_LOCKED={str(SCOPE_LOCKED).lower()}",
        f"MILESTONE_30_TASK_2_SOURCE_DEPENDENCY_VALID={str(report['source_dependency_valid']).lower()}",
        f"MILESTONE_30_TASK_2_OPERATOR_SEED_ID={PROPOSED_OPERATOR_SEED_ID}",
        "MILESTONE_30_TASK_2_OPERATOR_SEED_STATUS_AFTER_LOCK=SELECTED_AND_SCOPE_LOCKED",
        f"MILESTONE_30_TASK_2_SCOPE_RULES_VALID={str(report['scope_rules_valid']).lower()}",
        f"MILESTONE_30_TASK_2_PUBLIC_MODE_ID={PUBLIC_MODE_ID}",
        f"MILESTONE_30_TASK_2_PRIVATE_MODE_ID={PRIVATE_MODE_ID}",
        f"MILESTONE_30_TASK_2_IMPLEMENTATION_STARTED={str(IMPLEMENTATION_STARTED).lower()}",
        f"MILESTONE_30_TASK_2_IMPLEMENTATION_ALLOWED_AT_TASK_2={str(IMPLEMENTATION_ALLOWED_AT_TASK_2).lower()}",
        f"MILESTONE_30_TASK_2_IMPLEMENTATION_ALLOWED_NEXT={str(IMPLEMENTATION_ALLOWED_NEXT).lower()}",
        f"MILESTONE_30_TASK_2_LOCAL_ONLY={str(LOCAL_ONLY).lower()}",
        f"MILESTONE_30_TASK_2_NETWORK_ACCESS_ALLOWED={str(NETWORK_ACCESS_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_SHELL_EXECUTION_ALLOWED={str(SHELL_EXECUTION_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_REPOSITORY_MUTATION_ALLOWED={str(REPOSITORY_MUTATION_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_REMOTE_REGISTRY_LOOKUP_ALLOWED={str(REMOTE_REGISTRY_LOOKUP_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_EXTERNAL_MODEL_CALL_ALLOWED={str(EXTERNAL_MODEL_CALL_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_PRIVATE_CORE_EXPOSURE_ALLOWED={str(PRIVATE_CORE_EXPOSURE_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED={str(UNVERIFIED_MANUEL_ASSUMPTION_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_EXTERNAL_COMMAND_AUTHORITY_ALLOWED={str(EXTERNAL_COMMAND_AUTHORITY_ALLOWED).lower()}",
        f"MILESTONE_30_TASK_2_FORBIDDEN_OPERATION_COUNT={FORBIDDEN_OPERATION_COUNT}",
        f"MILESTONE_30_TASK_2_ALLOWED_INPUT_COUNT={ALLOWED_INPUT_COUNT}",
        f"MILESTONE_30_TASK_2_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_30_TASK_2_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_30_TASK_2_GENERATED_ARTIFACT_COUNT={GENERATED_ARTIFACT_COUNT}",
        f"MILESTONE_30_TASK_2_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    write_task_2_artifacts()
    for line in task_2_status_lines():
        print(line)
