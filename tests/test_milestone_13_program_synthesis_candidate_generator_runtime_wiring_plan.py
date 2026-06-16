from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_runtime_wiring_plan import (
    NEXT_STAGE,
    PLAN_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    WIRING_STEPS,
    WIRING_TARGETS,
    build_runtime_wiring_plan_record,
    build_wiring_plan,
    validate_runtime_wiring_plan_record,
    write_artifacts,
)


def test_runtime_wiring_plan_record_is_valid():
    record = build_runtime_wiring_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["plan_verdict"] == PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_review_passed"] is True
    assert record["runtime_wiring_plan_created"] is True
    assert record["runtime_wiring_plan_ready"] is True
    assert record["runtime_wiring_plan_valid"] is True
    assert record["runtime_wiring_plan_review_required"] is True
    assert record["controlled_implementation_deferred"] is True
    assert record["wiring_target_count"] == 4
    assert record["wiring_step_count"] == 6
    assert record["acceptance_gate_count"] == 15
    assert record["implementation_allowed_now"] is False
    assert record["runtime_execution_performed"] is False
    assert record["candidate_generator_wiring_authorized"] is False
    assert record["runtime_wiring_authorized"] is False
    assert record["runtime_solver_modified"] is False
    assert record["candidate_generator_modified"] is False
    assert record["ranker_runtime_modified"] is False
    assert record["real_submission_allowed"] is False
    assert record["kaggle_submission_sent"] is False
    assert record["private_core_exposure"] is False
    assert record["legal_certification"] is False
    assert validate_runtime_wiring_plan_record(record) == []


def test_wiring_targets_are_plan_only():
    assert len(WIRING_TARGETS) == 4
    assert all(target["runtime_modification_now"] is False for target in WIRING_TARGETS)
    assert all(target["requires_review_before_implementation"] is True for target in WIRING_TARGETS)


def test_wiring_steps_are_deferred():
    assert len(WIRING_STEPS) == 6
    assert all(step["implementation_allowed_now"] is False for step in WIRING_STEPS)


def test_build_wiring_plan_is_plan_only():
    source = {
        "revision": "SOURCE",
        "review_verdict": "PASS",
        "runtime_wiring_plan_authorized": True,
        "candidate_count": 12,
        "candidate_family_count": 7,
        "diagnostic_fixture_count": 4,
        "candidate_fixture_matrix_count": 4,
    }

    plan = build_wiring_plan(source)

    assert plan["plan_mode"] == "PLAN_ONLY"
    assert plan["source_runtime_wiring_plan_authorized"] is True
    assert plan["wiring_target_count"] == 4
    assert plan["wiring_step_count"] == 6
    assert plan["runtime_modification_allowed_now"] is False
    assert plan["candidate_generator_runtime_modification_allowed_now"] is False
    assert plan["ranker_runtime_modification_allowed_now"] is False
    assert plan["implementation_deferred_to_next_reviewed_stage"] is True
    assert plan["review_required_before_implementation"] is True
    assert plan["next_stage"] == NEXT_STAGE


def test_runtime_wiring_plan_fails_if_runtime_wiring_is_mutated():
    record = build_runtime_wiring_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_runtime_wiring_plan_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_runtime_wiring_plan_fails_if_implementation_allowed_now():
    record = build_runtime_wiring_plan_record(baseline_commit="TEST-COMMIT")
    record["implementation_allowed_now"] = True

    issues = validate_runtime_wiring_plan_record(record)

    assert "implementation_allowed_now_NOT_FALSE" in issues


def test_runtime_wiring_plan_artifacts_are_written(tmp_path: Path):
    record = build_runtime_wiring_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-v1.md" in written_files
