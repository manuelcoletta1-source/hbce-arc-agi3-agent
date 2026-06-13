import subprocess
import sys


def run_script(path: str) -> str:
    completed = subprocess.run(
        [sys.executable, path],
        check=True,
        text=True,
        capture_output=True,
        env={"PYTHONPATH": "src"},
    )
    return completed.stdout


def test_run_local_script_smoke():
    output = run_script("scripts/run_local.py")
    assert "ARC_AGI3_SMOKE_AGENT_READY" in output
    assert "verified=True" in output


def test_run_public_games_script_smoke():
    output = run_script("scripts/run_public_games.py")
    assert "PUBLIC_GAMES_SMOKE_READY" in output
    assert "verified=True" in output


def test_package_submission_script_smoke():
    output = run_script("scripts/package_submission.py")
    assert "PACKAGE_SUBMISSION_SMOKE_READY" in output
    assert "ARC_AGI3_SMOKE_AGENT_READY" in output
