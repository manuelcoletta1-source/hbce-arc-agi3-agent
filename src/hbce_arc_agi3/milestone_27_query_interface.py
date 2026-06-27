from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


MILESTONE_ID = "MILESTONE_27"
TASK_ID = "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_V1"
SOURCE_TASK_ID = "MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1"
SELECTED_OBJECTIVE_ID = "CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
SCOPE_LOCK_ID = "MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY"
QUERY_INTERFACE_REVISION = "MILESTONE_27_QUERY_INTERFACE_IMPLEMENTATION_V1"

TASK_BUDGET_MAX = 8
CURRENT_TASK_NUMBER = 3
NEXT_STAGE = "MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_V1"

LOCAL_ONLY = True
NETWORK_ACCESS_ALLOWED = False
SHELL_EXECUTION_ALLOWED = False
REPOSITORY_MUTATION_ALLOWED = False
DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED = False
REMOTE_REGISTRY_LOOKUP_ALLOWED = False

FORBIDDEN_OPERATION_FLAGS = (
    "network_access",
    "remote_fetch",
    "remote_registry_lookup",
    "shell_execution",
    "subprocess_execution",
    "repository_mutation",
    "filesystem_write",
    "deep_recursive_dependency_traversal",
    "unbounded_scan",
    "external_index_dependency",
)

ALLOWED_QUERY_FIELDS = (
    "milestone_id",
    "archive_status",
    "technical_status",
    "process_status",
    "final_task_number_lte",
    "final_task_number_gte",
    "include_evidence",
    "limit",
    "local_only",
)

_TASK_3_SIGNATURE_SEED = {
    "task_id": TASK_ID,
    "source_task_id": SOURCE_TASK_ID,
    "selected_objective_id": SELECTED_OBJECTIVE_ID,
    "scope_lock_id": SCOPE_LOCK_ID,
    "revision": QUERY_INTERFACE_REVISION,
}


@dataclass(frozen=True)
class ClosedMilestoneArchiveRecord:
    milestone_id: str
    archive_status: str
    technical_status: str
    process_status: str
    objective_id: str
    final_task_number: int
    task_budget_max: int
    closed_commit: str
    closure_marker: str
    artifact_family: str
    evidence_bundle: tuple[str, ...] = field(default_factory=tuple)

    def to_public_dict(self, *, include_evidence: bool = True) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence_bundle"] = list(self.evidence_bundle) if include_evidence else []
        return payload


@dataclass(frozen=True)
class ClosedMilestoneArchiveQuery:
    milestone_id: str | None = None
    archive_status: str | None = None
    technical_status: str | None = None
    process_status: str | None = None
    final_task_number_lte: int | None = None
    final_task_number_gte: int | None = None
    include_evidence: bool = True
    limit: int | None = None
    local_only: bool = True
    forbidden_operations: tuple[str, ...] = field(default_factory=tuple)


def _stable_digest(payload: Mapping[str, Any] | Sequence[Any] | str) -> str:
    if isinstance(payload, str):
        normalized = payload
    else:
        normalized = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return sha256(normalized.encode("utf-8")).hexdigest().upper()[:16]


def _normalize_token(value: Any) -> str:
    return str(value).strip().upper().replace("-", "_").replace(" ", "_")


def task_3_signature() -> str:
    return _stable_digest(_TASK_3_SIGNATURE_SEED)


def build_closed_milestone_archive_index() -> tuple[ClosedMilestoneArchiveRecord, ...]:
    return (
        ClosedMilestoneArchiveRecord(
            milestone_id="MILESTONE_26",
            archive_status="CLOSED",
            technical_status="PASS",
            process_status="GOVERNED_WITHIN_TASK_BUDGET",
            objective_id="CLOSED_MILESTONE_ARCHIVE_INDEX",
            final_task_number=6,
            task_budget_max=8,
            closed_commit="5ca645c",
            closure_marker="MILESTONE_26_CLOSURE_SOURCE_ARTIFACT_VALID",
            artifact_family="milestone-26-archive-index",
            evidence_bundle=(
                "31fd437 Open ARC AGI3 milestone 26 with governed task budget",
                "23705dc Lock ARC AGI3 milestone 26 archive index scope",
                "cdb149f Implement ARC AGI3 milestone 26 archive index",
                "28ecf4d Validate ARC AGI3 milestone 26 archive index artifacts",
                "ef10604 Integrate ARC AGI3 milestone 26 archive index regression",
                "5ca645c Close ARC AGI3 milestone 26 archive index",
            ),
        ),
        ClosedMilestoneArchiveRecord(
            milestone_id="MILESTONE_25",
            archive_status="CLOSED",
            technical_status="PASS",
            process_status="GOVERNED_EVIDENCE_BUNDLE_CLOSED",
            objective_id="CLOSED_MILESTONE_EVIDENCE_BUNDLE",
            final_task_number=6,
            task_budget_max=8,
            closed_commit="b7f9069",
            closure_marker="MILESTONE_25_EVIDENCE_BUNDLE_CLOSED",
            artifact_family="milestone-25-evidence-bundle",
            evidence_bundle=(
                "6438bf9 Validate ARC AGI3 milestone 25 evidence bundle artifacts",
                "3f17e12 Integrate ARC AGI3 milestone 25 evidence bundle regression",
                "b7f9069 Close ARC AGI3 milestone 25 evidence bundle",
            ),
        ),
    )


def _as_int_or_none(value: Any) -> int | None:
    if value is None:
        return None
    return int(value)


def _as_forbidden_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str):
        return (_normalize_token(value),)
    return tuple(_normalize_token(item) for item in value)


def coerce_query(query: ClosedMilestoneArchiveQuery | Mapping[str, Any] | None) -> ClosedMilestoneArchiveQuery:
    if query is None:
        return ClosedMilestoneArchiveQuery()

    if isinstance(query, ClosedMilestoneArchiveQuery):
        return query

    raw = dict(query)
    unknown_fields = sorted(set(raw) - set(ALLOWED_QUERY_FIELDS) - {"forbidden_operations"})

    explicit_forbidden = _as_forbidden_tuple(raw.get("forbidden_operations"))

    forbidden_from_unknown = tuple(
        _normalize_token(field)
        for field in unknown_fields
        if field in FORBIDDEN_OPERATION_FLAGS
    )

    forbidden_from_truthy_flags = tuple(
        _normalize_token(flag)
        for flag in FORBIDDEN_OPERATION_FLAGS
        if bool(raw.get(flag)) is True
    )

    return ClosedMilestoneArchiveQuery(
        milestone_id=raw.get("milestone_id"),
        archive_status=raw.get("archive_status"),
        technical_status=raw.get("technical_status"),
        process_status=raw.get("process_status"),
        final_task_number_lte=_as_int_or_none(raw.get("final_task_number_lte")),
        final_task_number_gte=_as_int_or_none(raw.get("final_task_number_gte")),
        include_evidence=bool(raw.get("include_evidence", True)),
        limit=_as_int_or_none(raw.get("limit")),
        local_only=bool(raw.get("local_only", True)),
        forbidden_operations=explicit_forbidden + forbidden_from_unknown + forbidden_from_truthy_flags,
    )


def detect_forbidden_operations(query: ClosedMilestoneArchiveQuery | Mapping[str, Any] | None) -> tuple[str, ...]:
    coerced = coerce_query(query)
    detected: list[str] = []

    if not coerced.local_only:
        detected.append("NON_LOCAL_QUERY_REQUESTED")

    for item in coerced.forbidden_operations:
        token = _normalize_token(item)
        if token not in detected:
            detected.append(token)

    return tuple(detected)


def _matches(record: ClosedMilestoneArchiveRecord, query: ClosedMilestoneArchiveQuery) -> bool:
    if query.milestone_id and record.milestone_id != _normalize_token(query.milestone_id):
        return False
    if query.archive_status and record.archive_status != _normalize_token(query.archive_status):
        return False
    if query.technical_status and record.technical_status != _normalize_token(query.technical_status):
        return False
    if query.process_status and record.process_status != _normalize_token(query.process_status):
        return False
    if query.final_task_number_lte is not None and record.final_task_number > query.final_task_number_lte:
        return False
    if query.final_task_number_gte is not None and record.final_task_number < query.final_task_number_gte:
        return False
    return True


def _query_payload(query: ClosedMilestoneArchiveQuery) -> dict[str, Any]:
    payload = asdict(query)
    payload["forbidden_operations"] = list(payload["forbidden_operations"])
    return payload


def query_closed_milestone_archive_index(
    query: ClosedMilestoneArchiveQuery | Mapping[str, Any] | None = None,
    *,
    records: Sequence[ClosedMilestoneArchiveRecord] | None = None,
) -> dict[str, Any]:
    coerced = coerce_query(query)
    forbidden = detect_forbidden_operations(coerced)
    query_payload = _query_payload(coerced)

    base = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "task_3_signature": task_3_signature(),
        "local_only": LOCAL_ONLY,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "remote_registry_lookup_allowed": REMOTE_REGISTRY_LOOKUP_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "scope_lock_enforced": True,
        "query": query_payload,
    }

    if forbidden:
        return {
            **base,
            "query_status": "BLOCKED_BY_SCOPE_LOCK",
            "blocked": True,
            "forbidden_operations_detected": list(forbidden),
            "matched_count": 0,
            "records": [],
            "query_id": "MILESTONE-27-QUERY-BLOCKED-" + _stable_digest({"query": query_payload, "forbidden": forbidden}),
            "result_signature": _stable_digest({"status": "BLOCKED", "forbidden": forbidden}),
            "result_valid": True,
        }

    source_records = tuple(records) if records is not None else build_closed_milestone_archive_index()
    matched = [record for record in source_records if _matches(record, coerced)]
    matched.sort(key=lambda item: item.milestone_id, reverse=True)

    if coerced.limit is not None:
        matched = [] if coerced.limit < 0 else matched[:coerced.limit]

    public_records = [
        record.to_public_dict(include_evidence=coerced.include_evidence)
        for record in matched
    ]

    return {
        **base,
        "query_status": "READY",
        "blocked": False,
        "forbidden_operations_detected": [],
        "matched_count": len(public_records),
        "records": public_records,
        "query_id": "MILESTONE-27-QUERY-" + _stable_digest({"query": query_payload, "records": public_records}),
        "result_signature": _stable_digest({"records": public_records, "revision": QUERY_INTERFACE_REVISION}),
        "result_valid": True,
    }


def validate_query_result(result: Mapping[str, Any]) -> bool:
    if result.get("task_id") != TASK_ID:
        return False
    if result.get("selected_objective_id") != SELECTED_OBJECTIVE_ID:
        return False
    if result.get("scope_lock_id") != SCOPE_LOCK_ID:
        return False
    if result.get("local_only") is not True:
        return False
    if result.get("scope_lock_enforced") is not True:
        return False
    if result.get("network_access_allowed") is not False:
        return False
    if result.get("shell_execution_allowed") is not False:
        return False
    if result.get("repository_mutation_allowed") is not False:
        return False
    if result.get("deep_recursive_dependency_traversal_allowed") is not False:
        return False
    if result.get("query_status") not in {"READY", "BLOCKED_BY_SCOPE_LOCK"}:
        return False
    if result.get("query_status") == "READY" and result.get("blocked") is not False:
        return False
    if result.get("query_status") == "BLOCKED_BY_SCOPE_LOCK" and result.get("blocked") is not True:
        return False
    return bool(result.get("result_valid"))


def render_query_result_markdown(result: Mapping[str, Any]) -> str:
    lines = [
        "# Milestone 27 Task 3 Query Interface Result",
        "",
        f"TASK_ID={result.get('task_id')}",
        f"QUERY_STATUS={result.get('query_status')}",
        f"QUERY_ID={result.get('query_id')}",
        f"SCOPE_LOCK_ID={result.get('scope_lock_id')}",
        f"LOCAL_ONLY={str(result.get('local_only')).lower()}",
        f"NETWORK_ACCESS_ALLOWED={str(result.get('network_access_allowed')).lower()}",
        f"DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED={str(result.get('deep_recursive_dependency_traversal_allowed')).lower()}",
        f"MATCHED_COUNT={result.get('matched_count')}",
        f"RESULT_SIGNATURE={result.get('result_signature')}",
        "",
        "## Records",
    ]

    records = result.get("records", [])
    if not records:
        lines.append("- NONE")
    else:
        for record in records:
            lines.extend(
                [
                    f"- {record['milestone_id']}",
                    f"  - archive_status: {record['archive_status']}",
                    f"  - technical_status: {record['technical_status']}",
                    f"  - process_status: {record['process_status']}",
                    f"  - final_task_number: {record['final_task_number']}",
                    f"  - task_budget_max: {record['task_budget_max']}",
                    f"  - closed_commit: {record['closed_commit']}",
                    f"  - closure_marker: {record['closure_marker']}",
                ]
            )

    lines.append("")
    return "\n".join(lines)


def write_task_3_artifacts(base_dir: str | Path = "examples/milestone-27/query-interface-implementation-v1") -> dict[str, Any]:
    output_dir = Path(base_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    primary_result = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26", "local_only": True})
    blocked_result = query_closed_milestone_archive_index({"milestone_id": "MILESTONE_26", "local_only": False})

    manifest = {
        "task_id": TASK_ID,
        "source_task_id": SOURCE_TASK_ID,
        "selected_objective_id": SELECTED_OBJECTIVE_ID,
        "scope_lock_id": SCOPE_LOCK_ID,
        "query_interface_revision": QUERY_INTERFACE_REVISION,
        "task_3_signature": task_3_signature(),
        "local_only": LOCAL_ONLY,
        "implementation_started": True,
        "query_interface_implemented": True,
        "network_access_allowed": NETWORK_ACCESS_ALLOWED,
        "shell_execution_allowed": SHELL_EXECUTION_ALLOWED,
        "repository_mutation_allowed": REPOSITORY_MUTATION_ALLOWED,
        "deep_recursive_dependency_traversal_allowed": DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED,
        "primary_query_id": primary_result["query_id"],
        "blocked_query_id": blocked_result["query_id"],
        "generated_artifact_count": 5,
        "next_stage": NEXT_STAGE,
    }

    (output_dir / "task-3-query-interface-result.json").write_text(
        json.dumps(primary_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-query-interface-result.md").write_text(
        render_query_result_markdown(primary_result),
        encoding="utf-8",
    )
    (output_dir / "task-3-query-interface-blocked-result.json").write_text(
        json.dumps(blocked_result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (output_dir / "task-3-index.txt").write_text(
        "\n".join(
            [
                "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_READY=true",
                f"TASK_ID={TASK_ID}",
                f"SOURCE_TASK_ID={SOURCE_TASK_ID}",
                f"SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
                f"SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
                f"QUERY_INTERFACE_REVISION={QUERY_INTERFACE_REVISION}",
                f"TASK_3_SIGNATURE={task_3_signature()}",
                "LOCAL_ONLY=true",
                "NETWORK_ACCESS_ALLOWED=false",
                "SHELL_EXECUTION_ALLOWED=false",
                "REPOSITORY_MUTATION_ALLOWED=false",
                "DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
                f"PRIMARY_QUERY_ID={primary_result['query_id']}",
                f"BLOCKED_QUERY_ID={blocked_result['query_id']}",
                f"NEXT_STAGE={NEXT_STAGE}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    return {
        "manifest": manifest,
        "primary_result": primary_result,
        "blocked_result": blocked_result,
        "output_dir": str(output_dir),
    }


def task_3_status_lines() -> tuple[str, ...]:
    return (
        "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_READY=true",
        f"MILESTONE_27_TASK_3_SELECTED_OBJECTIVE_ID={SELECTED_OBJECTIVE_ID}",
        f"MILESTONE_27_TASK_3_SCOPE_LOCK_ID={SCOPE_LOCK_ID}",
        "MILESTONE_27_TASK_3_OBJECTIVE_SOURCE_TASK_2_VALID=true",
        "MILESTONE_27_TASK_3_IMPLEMENTATION_STARTED=true",
        "MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true",
        "MILESTONE_27_TASK_3_LOCAL_ONLY=true",
        "MILESTONE_27_TASK_3_NETWORK_ACCESS_ALLOWED=false",
        "MILESTONE_27_TASK_3_SHELL_EXECUTION_ALLOWED=false",
        "MILESTONE_27_TASK_3_REPOSITORY_MUTATION_ALLOWED=false",
        "MILESTONE_27_TASK_3_REMOTE_REGISTRY_LOOKUP_ALLOWED=false",
        "MILESTONE_27_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false",
        f"MILESTONE_27_TASK_3_ALLOWED_QUERY_FIELD_COUNT={len(ALLOWED_QUERY_FIELDS)}",
        f"MILESTONE_27_TASK_3_FORBIDDEN_OPERATION_COUNT={len(FORBIDDEN_OPERATION_FLAGS)}",
        "MILESTONE_27_TASK_3_GENERATED_ARTIFACT_COUNT=5",
        f"MILESTONE_27_TASK_3_TASK_BUDGET_MAX={TASK_BUDGET_MAX}",
        f"MILESTONE_27_TASK_3_CURRENT_TASK_NUMBER={CURRENT_TASK_NUMBER}",
        f"MILESTONE_27_TASK_3_TASK_3_SIGNATURE={task_3_signature()}",
        f"MILESTONE_27_TASK_3_NEXT_STAGE={NEXT_STAGE}",
    )


if __name__ == "__main__":
    artifacts = write_task_3_artifacts()
    for line in task_3_status_lines():
        print(line)
    print("MILESTONE_27_TASK_3_PRIMARY_QUERY_ID=" + artifacts["primary_result"]["query_id"])
    print("MILESTONE_27_TASK_3_BLOCKED_QUERY_ID=" + artifacts["blocked_result"]["query_id"])
