# Milestone 27 Task 3 - Query Interface Implementation v1

MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTATION_READY=true

MILESTONE_27_TASK_3_SOURCE_TASK_ID=MILESTONE_27_TASK_2_OBJECTIVE_SELECTION_AND_SCOPE_LOCK_V1
MILESTONE_27_TASK_3_SELECTED_OBJECTIVE_ID=CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY
MILESTONE_27_TASK_3_SCOPE_LOCK_ID=MILESTONE_27_SCOPE_CLOSED_MILESTONE_ARCHIVE_INDEX_QUERY_INTERFACE_LOCAL_ONLY

MILESTONE_27_TASK_3_OBJECTIVE_SOURCE_TASK_2_VALID=true
MILESTONE_27_TASK_3_IMPLEMENTATION_STARTED=true
MILESTONE_27_TASK_3_QUERY_INTERFACE_IMPLEMENTED=true
MILESTONE_27_TASK_3_LOCAL_ONLY=true

MILESTONE_27_TASK_3_NETWORK_ACCESS_ALLOWED=false
MILESTONE_27_TASK_3_SHELL_EXECUTION_ALLOWED=false
MILESTONE_27_TASK_3_REPOSITORY_MUTATION_ALLOWED=false
MILESTONE_27_TASK_3_REMOTE_REGISTRY_LOOKUP_ALLOWED=false
MILESTONE_27_TASK_3_DEEP_RECURSIVE_DEPENDENCY_TRAVERSAL_ALLOWED=false

MILESTONE_27_TASK_3_ALLOWED_QUERY_FIELD_COUNT=9
MILESTONE_27_TASK_3_FORBIDDEN_OPERATION_COUNT=10
MILESTONE_27_TASK_3_GENERATED_ARTIFACT_COUNT=5

MILESTONE_27_TASK_3_TASK_BUDGET_MAX=8
MILESTONE_27_TASK_3_CURRENT_TASK_NUMBER=3

MILESTONE_27_TASK_3_PRIMARY_INTERFACE_MODULE=src/hbce_arc_agi3/milestone_27_query_interface.py
MILESTONE_27_TASK_3_PRIMARY_TEST_MODULE=tests/test_milestone_27_query_interface.py
MILESTONE_27_TASK_3_TASK_VALIDATION_TEST=tests/test_milestone_27_task_3_query_interface_implementation.py
MILESTONE_27_TASK_3_ARTIFACT_DIR=examples/milestone-27/query-interface-implementation-v1

MILESTONE_27_TASK_3_NEXT_STAGE=MILESTONE_27_TASK_4_QUERY_INTERFACE_VALIDATION_V1

## Objective

Implement the locally scoped closed milestone archive index query interface selected and locked in Task 2.

## Scope

Allowed:

- bounded local query over closed milestone archive records;
- filtering by milestone id, archive status, technical status, process status and final task count;
- evidence inclusion toggle;
- deterministic result id and signature;
- fail-closed response for non-local or forbidden operations.

Forbidden:

- network access;
- remote registry lookup;
- shell execution;
- repository mutation;
- filesystem write through the query surface;
- deep recursive dependency traversal;
- unbounded scans;
- external index dependency.

## Result

Task 3 turns the Task 2 scope lock into an executable local query interface.

The interface remains local-only and bounded. It provides records for closed milestone archive status without reaching outside the repository, because letting a query layer develop travel ambitions is apparently how software becomes a governance problem.
