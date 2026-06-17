from pathlib import Path

from hbce_arc_agi3.milestone_13_program_synthesis_candidate_generator_controlled_runtime_wiring_implementation_plan import (
    NEXT_STAGE,
    PLAN_VERDICT,
    TASK_NAME,
    TASK_VERDICT,
    build_controlled_implementation_plan,
    build_controlled_runtime_wiring_implementation_plan_record,
    review_implementation_phases,
    review_implementation_units,
    validate_controlled_runtime_wiring_implementation_plan_record,
    write_artifacts,
)


def _unit(index: int):
    return {
        "unit_id": f"CONTROLLED-IMPLEMENTATION-UNIT-{index:02d}",
        "name": f"unit_{index}",
        "planned_file": f"src/unit_{index}.py",
        "purpose": "test",
        "implementation_allowed_now": False,
        "runtime_activation_allowed": False,
        "requires_plan_review_before_code": True,
    }


def _phase(index: int):
    return {
        "phase_id": f"CONTROLLED-IMPLEMENTATION-PHASE-{index:02d}",
        "name": f"phase_{index}",
        "description": "test phase",
        "implementation_allowed_now": False,
    }


def test_controlled_runtime_wiring_implementation_plan_record_is_valid():
    record = build_controlled_runtime_wiring_implementation_plan_record(baseline_commit="TEST-COMMIT")

    assert record["revision"] == TASK_NAME
    assert record["task_verdict"] == TASK_VERDICT
    assert record["plan_verdict"] == PLAN_VERDICT
    assert record["next_stage"] == NEXT_STAGE
    assert record["source_review_passed"] is True
    assert record["controlled_implementation_plan_created"] is True
    assert record["controlled_implementation_plan_ready"] is True
    assert record["controlled_implementation_plan_valid"] is True
    assert record["controlled_implementation_plan_review_required"] is True
    assert record["controlled_implementation_authorized"] is False
    assert record["implementation_unit_count"] == 4
    assert record["implementation_phase_count"] == 7
    assert record["implementation_gate_count"] == 18
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
    assert validate_controlled_runtime_wiring_implementation_plan_record(record) == []


def test_review_implementation_units_passes_for_good_units():
    units = [_unit(index) for index in range(1, 5)]

    review = review_implementation_units(units)

    assert review["implementation_unit_count"] == 4
    assert review["unit_ids_unique"] is True
    assert review["all_units_have_names"] is True
    assert review["all_units_have_planned_files"] is True
    assert review["all_units_implementation_blocked_now"] is True
    assert review["all_units_runtime_activation_blocked"] is True
    assert review["all_units_require_review_before_code"] is True


def test_review_implementation_units_detects_runtime_activation():
    units = [_unit(index) for index in range(1, 5)]
    units[0]["runtime_activation_allowed"] = True

    review = review_implementation_units(units)

    assert review["all_units_runtime_activation_blocked"] is False


def test_review_implementation_phases_passes_for_good_phases():
    phases = [_phase(index) for index in range(1, 8)]

    review = review_implementation_phases(phases)

    assert review["implementation_phase_count"] == 7
    assert review["phase_ids_unique"] is True
    assert review["all_phases_have_names"] is True
    assert review["all_phases_have_descriptions"] is True
    assert review["all_phases_implementation_blocked_now"] is True


def test_review_implementation_phases_detects_implementation_allowed():
    phases = [_phase(index) for index in range(1, 8)]
    phases[0]["implementation_allowed_now"] = True

    review = review_implementation_phases(phases)

    assert review["all_phases_implementation_blocked_now"] is False


def test_build_controlled_implementation_plan_is_plan_only():
    source = {
        "revision": "SOURCE",
        "review_verdict": "PASS",
        "controlled_implementation_plan_authorized": True,
        "controlled_implementation_authorized": False,
    }

    plan = build_controlled_implementation_plan(source)

    assert plan["plan_mode"] == "CONTROLLED_IMPLEMENTATION_PLAN_ONLY"
    assert plan["source_controlled_implementation_plan_authorized"] is True
    assert plan["source_controlled_implementation_authorized"] is False
    assert plan["implementation_unit_count"] == 4
    assert plan["implementation_phase_count"] == 7
    assert plan["implementation_gate_count"] == 18
    assert plan["implementation_allowed_now"] is False
    assert plan["runtime_wiring_allowed_now"] is False
    assert plan["candidate_generator_wiring_allowed_now"] is False
    assert plan["ranker_runtime_modification_allowed_now"] is False
    assert plan["controlled_implementation_plan_review_required"] is True
    assert plan["next_stage"] == NEXT_STAGE


def test_controlled_runtime_wiring_implementation_plan_fails_if_implementation_allowed_now():
    record = build_controlled_runtime_wiring_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["implementation_allowed_now"] = True

    issues = validate_controlled_runtime_wiring_implementation_plan_record(record)

    assert "implementation_allowed_now_NOT_FALSE" in issues


def test_controlled_runtime_wiring_implementation_plan_fails_if_runtime_wiring_authorized():
    record = build_controlled_runtime_wiring_implementation_plan_record(baseline_commit="TEST-COMMIT")
    record["runtime_wiring_authorized"] = True

    issues = validate_controlled_runtime_wiring_implementation_plan_record(record)

    assert "runtime_wiring_authorized_NOT_FALSE" in issues


def test_controlled_runtime_wiring_implementation_plan_artifacts_are_written(tmp_path: Path):
    record = build_controlled_runtime_wiring_implementation_plan_record(baseline_commit="TEST-COMMIT")
    artifacts = write_artifacts(record, artifact_dir=tmp_path)

    assert set(artifacts) == {"json", "index", "manifest", "markdown"}

    written_files = {path.name for path in tmp_path.iterdir()}
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-index-v1.json" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-manifest-v1.txt" in written_files
    assert "milestone-13-program-synthesis-candidate-generator-controlled-runtime-wiring-implementation-plan-v1.md" in written_files
