from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_runtime_wiring_plan_review import (
    NEXT_STAGE,
    REVIEW_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_plan_review_report,
    build_runtime_wiring_plan_review_record,
    review_wiring_steps,
    review_wiring_targets,
    validate_runtime_wiring_plan_review_record,
    write_artifacts,
)


def _target(index: int):
    return {
        "target_id": f"WIRING-TARGET-{index:02d}",
        "name": f"target_{index}",
        "planned_module": f"src/module_{index}.py",
        "purpose": "test",
        "runtime_modification_now": False,
        "requires_review_before_implementation": True,
    }


def _step(index: int):
    return {
        "step_id": f"WIRING-PLAN-STEP-{index:02d}",
        "name": f"step_{index}",
        "description": "test step",
        "implementation_allowed_now": False,
    }


def test_runtime_wiring_plan_review_record_is_valid():
    record = build_runtime_wiring_plan_review_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["review_verdict"] == REVIEW_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_plan_ready"] is True
    assert record["source_plan_shape_ok"] is True
    assert record["source_boundaries_ok"] is True
    assert record["runtime_wiring_plan_review_ready"] is True
    assert record["runtime_wiring_plan_review_valid"] is True
    assert record["runtime_wiring_plan_review_passed"] is True
    assert record["controlled_implementation_plan_authorized"] is True
    assert record["controlled_implementation_authorized"] is False
    assert record["wiring_target_count"] == 4
    assert record["wiring_step_count"] == 6
    assert record["source_acceptance_gate_count"] == 15
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
    assert validate_runtime_wiring_plan_review_record(record) == []


def test_review_wiring_targets_passes_for_good_targets():
    targets = [_target(index) for index in range(1, 5)]

    review = review_wiring_targets(targets)

    assert review["wiring_target_count"] == 4
    assert review["target_ids_unique"] is True
    assert review["all_targets_have_names"] is True
    assert review["all_targets_have_planned_modules"] is True
    assert review["all_targets_runtime_modification_blocked"] is True
    assert review["all_targets_require_review"] is True


def test_review_wiring_targets_detects_runtime_modification():
    targets = [_target(index) for index in range(1, 5)]
    targets[0]["runtime_modification_now"] = True

    review = review_wiring_targets(targets)

    assert review["all_targets_runtime_modification_blocked"] is False


def test_review_wiring_steps_passes_for_good_steps():
    steps = [_step(index) for index in range(1, 7)]

    review = review_wiring_steps(steps)

    assert review["wiring_step_count"] == 6
    assert review["step_ids_unique"] is True
    assert review["all_steps_have_names"] is True
    assert review["all_steps_have_descriptions"] is True
    assert review["all_steps_implementation_blocked"] is True


def test_review_wiring_steps_detects_implementation_allowed():
    steps = [_step(index) for index in range(1, 7)]
    steps[0]["implementation_allowed_now"] = True

    review = review_wiring_steps(steps)

    assert review["all_steps_implementation_blocked"] is False


def test_plan_review_report_passes_for_good_source_record():
    source_record = {
        "revision": "SOURCE",
        "task_verdict": "READY",
        "plan_verdict": "PLAN_READY",
        "runtime_wiring_plan_ready": True,
        "runtime_wiring_plan_valid": True,
        "runtime_wiring_plan_review_required": True,
        "controlled_implementation_deferred": True,
        "implementation_allowed_now": False,
        "wiring_target_count": 4,
        "wiring_step_count": 6,
        "acceptance_gate_count": 15,
        "wiring_targets": [_target(index) for index in range(1, 5)],
        "wiring_steps": [_step(index) for index in range(1, 7)],
        "runtime_execution_performed": False,
        "candidate_generator_wiring_authorized": False,
        "runtime_wiring_authorized": False,
        "runtime_solver_modified": False,
        "candidate_generator_modified": False,
        "ranker_runtime_modified": False,
        "real_evaluation_performed": False,
        "real_submission_allowed": False,
        "ready_for_real_kaggle_submission": False,
        "kaggle_authentication_allowed": False,
        "kaggle_authentication_performed": False,
        "kaggle_upload_allowed": False,
        "kaggle_submission_sent": False,
        "private_core_exposure": False,
        "legal_certification": False,
        "next_stage": "MILESTONE_13_TASK_11_PROGRAM_SYNTHESIS_CANDIDATE_GENERATOR_RUNTIME_WIRING_PLAN_REVIEW_V1",
    }

    report = build_plan_review_report(source_record)

    assert report["review_passed"] is True
    assert report["blocking_issue_count"] == 0
    assert report["recommended_next_stage"] == NEXT_STAGE


def test_runtime_wiring_plan_review_fails_if_runtime_wiring_is_mutated():
    record = build_runtime_wiring_plan_review_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_runtime_wiring_plan_review_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_runtime_wiring_plan_review_fails_if_controlled_implementation_is_authorized():
    record = build_runtime_wiring_plan_review_record(baseline_commit="TEST-COMMIT")
    record["controlled_implementation_authorized"] = True

    issues = validate_runtime_wiring_plan_review_record(record)

    assert "controlled_implementation_authorized_NOT_FALSE" in issues


def test_runtime_wiring_plan_review_artifacts_are_written(tmp_path: Path):
    record = build_runtime_wiring_plan_review_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-review-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-review-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-review-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-runtime-wiring-plan-review-v1.md" in written_files
