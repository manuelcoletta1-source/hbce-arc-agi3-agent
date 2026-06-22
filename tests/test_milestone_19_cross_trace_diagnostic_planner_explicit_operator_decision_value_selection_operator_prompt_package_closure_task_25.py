from __future__ import annotations

import json

from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_authorization_gate_task_3 import (
    ALLOWED_OPERATOR_DECISION_VALUES,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_implementation_operator_decision_record_task_5 import (
    SELECTED_OPERATOR_DECISION_VALUE,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_review_task_24 import (
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_review,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure_task_25 import (
    PREVIOUS_COMMIT,
    PREVIOUS_SIGNATURE,
    TASK_NAME,
    build_boundary_controls,
    build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure,
    build_operator_prompt_package_closure_items,
    write_artifacts,
)
from hbce_arc_agi3.milestone_19_cross_trace_diagnostic_planner_planning_intake_task_1 import (
    build_feature_families,
    build_pipeline_model,
    build_required_output_fields,
    build_test_plan,
)


def test_task_25_ready_valid_prompt_package_closure_created_but_no_selection_or_authorization() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()

    assert data["task"] == TASK_NAME
    assert data["status"] == f"{TASK_NAME}_READY"
    assert data["validation"] == f"{TASK_NAME}_VALID"
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closure_ready"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closure_created"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closure_locked"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closure_review_required"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closure_review_created"] is False
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_created"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_active"] is False
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_closed"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_contains_allowed_values"] is True
    assert data["explicit_operator_decision_value_selection_operator_prompt_package_selected_value_absent"] is True
    assert data["operator_prompt_option_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert data["operator_prompt_item_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert data["operator_prompt_closure_item_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert data["waiting_for_explicit_operator_decision_value"] is True
    assert data["explicit_operator_decision_value_selected"] is False
    assert data["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
    assert data["operator_decision_received"] is False
    assert data["implementation_authorized"] is False
    assert data["acceptance_gate_failure_count"] == 0


def test_task_25_preserves_task_24_baseline() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_review()
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()

    assert data["previous_commit"] == PREVIOUS_COMMIT == "20dd058"
    assert data["previous_signature"] == PREVIOUS_SIGNATURE == "1EE064F87650ECD3"
    assert data["source_explicit_operator_decision_value_selection_operator_prompt_package_review_signature"] == source["signature"] == PREVIOUS_SIGNATURE
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_closure_required"] is True
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_closure_created"] is False
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_review_passed"] is True
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_confirmed"] is True
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_contains_allowed_values"] is True
    assert source["explicit_operator_decision_value_selection_operator_prompt_package_selected_value_absent"] is True
    assert source["operator_prompt_option_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert source["operator_prompt_item_count"] == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert source["waiting_for_explicit_operator_decision_value"] is True
    assert source["explicit_operator_decision_value_selected"] is False
    assert source["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE
    assert source["operator_decision_received"] is False
    assert source["implementation_authorized"] is False


def test_task_25_closure_items_confirm_available_not_selected_and_blocked() -> None:
    source = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_review()
    items = build_operator_prompt_package_closure_items(source)

    assert len(items) == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert all(item["decision_value"] in ALLOWED_OPERATOR_DECISION_VALUES for item in items)
    assert all(
        item["closure_status"] == "OPERATOR_PROMPT_PACKAGE_CLOSURE_CREATED_OPTION_AVAILABLE_NOT_SELECTED"
        for item in items
    )
    assert all(
        item["closure_effect"] == "OPERATOR_PROMPT_PACKAGE_SEGMENT_CLOSED_AWAIT_EXPLICIT_OPERATOR_DECISION_NO_IMPLEMENTATION"
        for item in items
    )
    assert all(item["requires_explicit_operator_selection"] is True for item in items)
    assert not any(item["selected"] for item in items)
    assert not any(item["validated"] for item in items)
    assert not any(item["authorizing"] for item in items)
    assert all(item["selected_operator_decision_value"] == SELECTED_OPERATOR_DECISION_VALUE for item in items)
    assert all(item["waiting_for_explicit_operator_decision_value"] is True for item in items)
    assert not any(item["explicit_operator_decision_value_selected"] for item in items)
    assert not any(item["operator_decision_received"] for item in items)
    assert not any(item["implementation_authorized"] for item in items)
    assert not any(item["runtime_solver_modified"] for item in items)
    assert not any(item["candidate_generator_modified"] for item in items)
    assert not any(item["real_evaluation_performed"] for item in items)
    assert not any(item["kaggle_submission_sent"] for item in items)
    assert not any(item["hidden_label_accessed"] for item in items)
    assert not any(item["private_core_exposure"] for item in items)
    assert all(item["fail_closed_active"] is True for item in items)
    assert not any(item["blocking_issue"] for item in items)


def test_task_25_boundary_closes_prompt_package_but_not_operator_decision() -> None:
    controls = build_boundary_controls()

    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_only"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_ready"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_created"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_locked"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_review_required"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closure_review_created"] is False
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_created"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_active"] is False
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_closed"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_contains_allowed_values"] is True
    assert controls["explicit_operator_decision_value_selection_operator_prompt_package_selected_value_absent"] is True
    assert controls["waiting_for_explicit_operator_decision_value"] is True
    assert controls["explicit_operator_decision_value_selected"] is False
    assert controls["selected_operator_decision_value_pending"] is True
    assert controls["operator_decision_received"] is False
    assert controls["implementation_authorized"] is False
    assert controls["runtime_activation_authorized"] is False
    assert controls["runtime_solver_modified"] is False
    assert controls["candidate_generator_modified"] is False
    assert controls["real_evaluation_authorized"] is False
    assert controls["real_submission_authorized"] is False
    assert controls["kaggle_submission_sent"] is False
    assert controls["hidden_label_accessed"] is False
    assert controls["private_core_exposure"] is False
    assert controls["fail_closed_active"] is True


def test_task_25_operator_prompt_options_still_unselected() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()

    assert len(data["operator_prompt_options"]) == len(ALLOWED_OPERATOR_DECISION_VALUES)
    assert tuple(option["decision_value"] for option in data["operator_prompt_options"]) == ALLOWED_OPERATOR_DECISION_VALUES
    assert not any(option["selected"] for option in data["operator_prompt_options"])
    assert not any(option["validated"] for option in data["operator_prompt_options"])
    assert not any(option["authorizing"] for option in data["operator_prompt_options"])
    assert not any(option["implementation_authorized_by_this_task"] for option in data["operator_prompt_options"])
    assert not any(option["runtime_activation_authorized_by_this_task"] for option in data["operator_prompt_options"])
    assert not any(option["real_evaluation_authorized_by_this_task"] for option in data["operator_prompt_options"])
    assert not any(option["kaggle_submission_authorized_by_this_task"] for option in data["operator_prompt_options"])


def test_task_25_models_remain_unchanged() -> None:
    data = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()

    assert data["pipeline_model"] == build_pipeline_model()
    assert data["feature_families"] == build_feature_families()
    assert data["required_output_fields"] == build_required_output_fields()
    assert data["test_plan"] == build_test_plan()


def test_task_25_acceptance_and_signature_are_deterministic() -> None:
    first = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()
    second = build_cross_trace_diagnostic_planner_explicit_operator_decision_value_selection_operator_prompt_package_closure()

    assert first["signature"] == second["signature"]
    assert len(first["signature"]) == 16
    assert first["explicit_operator_decision_value_selection_operator_prompt_package_closure_id"].endswith(first["signature"])
    assert first["acceptance_gate_count"] > 337
    assert first["acceptance_gate_failure_count"] == 0
    assert first["acceptance_gate_failures"] == []


def test_task_25_artifacts_are_written(tmp_path) -> None:
    paths = write_artifacts(
        artifact_dir=tmp_path / "examples" / "milestone-19" / "task-25",
        docs_path=tmp_path / "docs" / "task-25.md",
        index_path=tmp_path / "docs" / "milestone-19-index.md",
    )

    for path in paths.values():
        assert path.exists(), path

    data = json.loads(paths["json"].read_text(encoding="utf-8"))
    manifest = paths["manifest"].read_text(encoding="utf-8")
    docs = paths["docs"].read_text(encoding="utf-8")
    milestone_index = paths["milestone_index"].read_text(encoding="utf-8")

    assert data["task"] == TASK_NAME
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closure_ready=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closure_created=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closure_locked=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closure_review_required=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closure_review_created=false" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_active=false" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_closed=true" in manifest
    assert "explicit_operator_decision_value_selection_operator_prompt_package_selected_value_absent=true" in manifest
    assert "waiting_for_explicit_operator_decision_value=true" in manifest
    assert "explicit_operator_decision_value_selected=false" in manifest
    assert "selected_operator_decision_value=PENDING_EXPLICIT_OPERATOR_DECISION" in manifest
    assert "operator_decision_received=false" in manifest
    assert "implementation_authorized=false" in manifest
    assert "runtime_solver_modified=false" in manifest
    assert "real_evaluation_authorized=false" in manifest
    assert "kaggle_submission_sent=false" in manifest
    assert "hidden_label_accessed=false" in manifest
    assert "Operator Prompt Package Closure v1" in docs
    assert "Explicit operator decision value selection operator prompt package closure created" in milestone_index
