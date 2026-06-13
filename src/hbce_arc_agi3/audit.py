"""Trace and audit helpers for the HBCE ARC-AGI-3 agent."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass(frozen=True)
class AuditTrace:
    event: str
    status: str
    payload: Dict[str, Any]
    legal_certification: bool = False
    opc_boundary: str = "technical research trace only"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp_utc"] = datetime.now(timezone.utc).isoformat()
        return data


def make_trace(event: str, status: str, payload: Dict[str, Any] | None = None) -> Dict[str, Any]:
    return AuditTrace(event=event, status=status, payload=payload or {}).to_dict()
