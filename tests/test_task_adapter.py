from hbce_arc_agi3.task_adapter import normalize_task


def test_normalize_task_from_grid_objects_goal():
    raw = {
        "id": "demo-1",
        "grid": [[1, 0], [0, 1]],
        "objects": [{"id": "a", "kind": "cell"}],
        "goal": "solve",
    }

    task = normalize_task(raw)

    assert task.status == "TASK_ADAPTER_READY"
    assert task.task_id == "demo-1"
    assert task.grid == [[1, 0], [0, 1]]
    assert task.objects == [{"id": "a", "kind": "cell"}]
    assert task.goal_hint == "solve"
    assert task.metadata["has_grid"] is True
    assert task.metadata["object_count"] == 1


def test_normalize_task_defaults_are_safe():
    task = normalize_task()

    assert task.status == "TASK_ADAPTER_READY"
    assert task.task_id == "anonymous-task"
    assert task.grid == []
    assert task.objects == []
    assert task.goal_hint == "explore"
    assert task.to_agent_state()["metadata"]["source"] == "task_adapter_v1"
