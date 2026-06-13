"""Trace schema v1 for the HBCE ARC-AGI-3 public baseline.

The trace schema records the agent path from observation to score.
It is deterministic, JSON-serializable and safe for public benchmark evidence.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from hashlib import sha256
from typing import Any, Dict, List


TRACE_SCHEMA_VERSION = "HBCE_ARC_AGI3_TRACE_SCHEMA_v1"

TracePayload = Dict[str, Any]


@dataclass(frozen=True)
class TraceStep:
    stage: str
    status: str
    summary: str
    payload: TracePayload = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AgentTrace:
    status: str
    schema_version: str
    trace_id: str
    task_id: str
    observation: TracePayload
    model: TracePayload
    goal: str
    plan: TracePayload
    action: TracePayload
    verification: TracePayload
    score: TracePayload
    steps: List[TraceStep]
    metadata: TracePayload = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["steps"] = [step.to_dict() for step in self.steps]
        return data


def _canonical_payload(payload: TracePayload) -> str:
    import json

    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def make_trace_id(task_id: str, payload: TracePayload) -> str:
    digest = sha256(f"{task_id}:{_canonical_payload(payload)}".encode("utf-8")).hexdigest()
    return f"ARC-TRACE-{digest[:16].upper()}"


def build_agent_trace(
    *,
    task_id: str,
    observation: TracePayload | None = None,
    model: TracePayload | None = None,
    goal: str = "explore",
    plan: TracePayload | None = None,
    action: TracePayload | None = None,
    verification: TracePayload | None = None,
    score: TracePayload | None = None,
    metadata: TracePayload | None = None,
) -> AgentTrace:
    observation = observation or {}
    model = model or {}
    plan = plan or {}
    action = action or {}
    verification = verification or {"verified": False, "reason": "not_verified_yet"}
    score = score or {"score": 0.0, "reason": "not_scored_yet"}
    metadata = metadata or {}

    trace_payload = {
        "task_id": task_id,
        "observation": observation,
        "model": model,
        "goal": goal,
        "plan": plan,
        "action": action,
        "verification": verification,
        "score": score,
        "schema_version": TRACE_SCHEMA_VERSION,
    }

    steps = [
        TraceStep(
            stage="observation",
            status="TRACE_STAGE_READY",
            summary="Raw or normalized task state was observed.",
            payload=observation,
        ),
        TraceStep(
            stage="model",
            status="TRACE_STAGE_READY",
            summary="A minimal internal world model was recorded.",
            payload=model,
        ),
        TraceStep(
            stage="goal",
            status="TRACE_STAGE_READY",
            summary="A goal hint or objective was recorded.",
            payload={"goal": goal},
        ),
        TraceStep(
            stage="plan",
            status="TRACE_STAGE_READY",
            summary="Candidate plan information was recorded.",
            payload=plan,
        ),
        TraceStep(
            stage="action",
            status="TRACE_STAGE_READY",
            summary="Selected or proposed action information was recorded.",
            payload=action,
        ),
        TraceStep(
            stage="verification",
            status="TRACE_STAGE_READY",
            summary="Verification state was recorded.",
            payload=verification,
        ),
        TraceStep(
            stage="score",
            status="TRACE_STAGE_READY",
            summary="Score state was recorded.",
            payload=score,
        ),
    ]

    return AgentTrace(
        status="TRACE_SCHEMA_READY",
        schema_version=TRACE_SCHEMA_VERSION,
        trace_id=make_trace_id(task_id, trace_payload),
        task_id=task_id,
        observation=observation,
        model=model,
        goal=goal,
        plan=plan,
        action=action,
        verification=verification,
        score=score,
        steps=steps,
        metadata={
            **metadata,
            "source": "trace_schema_v1",
            "stage_count": len(steps),
            "public_safe": True,
        },
    )


def validate_trace_dict(trace: Dict[str, Any]) -> Dict[str, Any]:
    required_keys = {
        "status",
        "schema_version",
        "trace_id",
        "task_id",
        "observation",
        "model",
        "goal",
        "plan",
        "action",
        "verification",
        "score",
        "steps",
        "metadata",
    }

    missing = sorted(required_keys.difference(trace.keys()))
    valid = not missing and trace.get("status") == "TRACE_SCHEMA_READY"

    return {
        "status": "TRACE_SCHEMA_VALID" if valid else "TRACE_SCHEMA_INVALID",
        "valid": valid,
        "missing": missing,
        "schema_version": trace.get("schema_version"),
        "trace_id": trace.get("trace_id"),
    }
