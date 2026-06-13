#!/usr/bin/env python3
"""Placeholder public-games runner.

This smoke script intentionally avoids external APIs and internet access.
Real Kaggle integration will be added after local contract tests.
"""

from hbce_arc_agi3.agent import run_agent


def main() -> int:
    result = run_agent({"grid": [[0]], "objects": [], "goal_hint": "explore"})
    print("PUBLIC_GAMES_SMOKE_READY")
    print(f"agent_status={result['status']}")
    print(f"verified={result['verified']}")
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
