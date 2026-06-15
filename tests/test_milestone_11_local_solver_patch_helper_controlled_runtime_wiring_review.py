from hbce_arc_agi3.milestone_11_local_solver_patch_helper_controlled_runtime_wiring_review import build_review_record, write_artifacts, NEXT_STAGE


def test_task22_record_ready():
    r = build_review_record()
    assert r["task_22_ready"] is True
    assert r["runtime_wiring_review_passed"] is True
    assert r["runtime_wiring_dry_run_accepted"] is True
    assert r["controlled_runtime_wiring_authorization_gate_recommended"] is True


def test_task22_boundaries_closed():
    r = build_review_record()
    assert r["controlled_runtime_wiring_authorized"] is False
    assert r["runtime_wiring_performed"] is False
    assert r["runtime_solver_modified"] is False
    assert r["ranker_runtime_modified"] is False
    assert r["external_solver_dependency"] is False
    assert r["real_submission_allowed"] is False
    assert r["kaggle_submission_sent"] is False
    assert r["fail_closed_active"] is True


def test_task22_next_stage():
    r = build_review_record()
    assert r["next_stage"] == NEXT_STAGE
    assert NEXT_STAGE == "MILESTONE_11_TASK_23_LOCAL_SOLVER_PATCH_HELPER_CONTROLLED_RUNTIME_WIRING_AUTHORIZATION_GATE_V1"


def test_task22_artifacts_written():
    result = write_artifacts()
    for path in result["files"].values():
        assert path.exists()
        assert path.stat().st_size > 0
