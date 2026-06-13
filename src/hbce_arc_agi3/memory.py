"""Small in-memory state store for public ARC-AGI-3 smoke baseline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AgentMemory:
    observations: List[Dict[str, Any]] = field(default_factory=list)
    decisions: List[Dict[str, Any]] = field(default_factory=list)

    def remember_observation(self, observation: Dict[str, Any]) -> None:
        self.observations.append(observation)

    def remember_decision(self, decision: Dict[str, Any]) -> None:
        self.decisions.append(decision)

    def snapshot(self) -> Dict[str, Any]:
        return {
            "observation_count": len(self.observations),
            "decision_count": len(self.decisions),
        }
