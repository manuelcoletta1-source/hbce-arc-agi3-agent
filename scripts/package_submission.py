#!/usr/bin/env python3
"""Package submission smoke check.

This does not create the final Kaggle package yet.
It verifies that the package import path and core agent contract are alive.
"""

from hbce_arc_agi3.agent import run_agent


def main() -> int:
    result = run_agent()
    print("PACKAGE_SUBMISSION_SMOKE_READY")
    print(f"agent_status={result['status']}")
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
