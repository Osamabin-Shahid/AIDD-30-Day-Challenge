---

description: "Task list for Calculator: Evaluate Expression feature implementation"
---

# Tasks: Calculator: Evaluate Expression

**Input**: Design documents from `specs/1-calc-expr-result/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Assumed Technical Context for Tasks (due to unresolved clarifications in plan.md):**
*   Language/Version: Python 3.9+
*   Primary Dependencies: None (standard library only for parsing/evaluation)
*   Testing Framework: pytest
*   Target Platform: CLI

## Format: `[ID] [P?] [Story?] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below assume single project - adjust based on plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create base project directories: `src/lib/`, `src/cli/`, `tests/unit/`
- [X] T002 Initialize Python project with `pyproject.toml` and basic configuration in `pyproject.toml`
- [X] T003 Configure `pytest` for unit testing in `pyproject.toml` and `tests/unit/__init__.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Define `evaluate_expression` function signature in `src/lib/calculator.py`
- [X] T005 Implement basic error handling structure for `evaluate_expression` in `src/lib/calculator.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Evaluate Basic Arithmetic (Priority: P1) 🎯 MVP

**Goal**: Successfully evaluate basic arithmetic expressions (+, -, *, /) with standard operator precedence.

**Independent Test**: Can be fully tested by providing various basic arithmetic expressions and verifying the output.

### Implementation for User Story 1

- [X] T006 [US1] Implement parsing logic for numbers and basic operators (+, -, *, /) in `src/lib/calculator.py`
- [X] T007 [US1] Implement evaluation logic for basic arithmetic operations considering operator precedence (MDAS/BODMAS) in `src/lib/calculator.py`
- [X] T008 [P] [US1] Add unit tests for basic arithmetic operations (e.g., "2+2", "10-5", "3*4", "20/4", "2+3*4") in `tests/unit/test_calculator.py`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Handle Division by Zero (Priority: P2)

**Goal**: Detect and handle division by zero with a clear error message.

**Independent Test**: Can be tested by inputting expressions like "10/0" and verifying the error message.

### Implementation for User Story 2

- [X] T009 [US2] Modify evaluation logic to detect division by zero and raise a specific error in `src/lib/calculator.py`
- [X] T010 [P] [US2] Add unit tests for division by zero scenarios (e.g., "10/0") in `tests/unit/test_calculator.py`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Handle Invalid Input (Priority: P2)

**Goal**: Detect and handle syntactically invalid input with an informative error message.

**Independent Test**: Can be tested by providing syntactically incorrect or non-arithmetic inputs.

### Implementation for User Story 3

- [X] T011 [US3] Enhance parsing/validation logic to identify invalid expression syntax (e.g., "2++2", "abc") and raise a specific error in `src/lib/calculator.py`
- [X] T012 [P] [US3] Add unit tests for invalid input scenarios in `tests/unit/test_calculator.py`

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T013 Implement a simple command-line interface (CLI) to accept expressions and display results/errors in `src/cli/main.py`
- [X] T014 Review and refine error messages for clarity and user-friendliness in `src/lib/calculator.py`
- [X] T015 Add documentation/comments for key functions and modules in `src/lib/calculator.py` and `src/cli/main.py`
- [X] T016 Add integration test for CLI input/output in `tests/integration/test_cli.py`

---

## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **User Stories (Phase 3+)**: All depend on Foundational phase completion
    -   User stories can then proceed in parallel (if staffed)
    -   Or sequentially in priority order (P1 → P2 → P3)
-   **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

-   **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
-   **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
-   **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

-   Tests (if included) MUST be written and FAIL before implementation
-   Models before services
-   Services before endpoints
-   Core implementation before integration
-   Story complete before moving to next priority

### Parallel Opportunities

-   All Setup tasks marked [P] can run in parallel
-   All Foundational tasks marked [P] can run in parallel (within Phase 2)
-   Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
-   All tests for a user story marked [P] can run in parallel
-   Models within a story marked [P] can run in parallel
-   Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together (if tests requested):
Task: "Add unit tests for basic arithmetic operations (e.g., "2+2", "10-5", "3*4", "20/4", "2+3*4") in tests/unit/test_calculator.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Implement parsing logic for numbers and basic operators (+, -, *, /) in src/lib/calculator.py"
Task: "Implement evaluation logic for basic arithmetic operations considering operator precedence (MDAS/BODMAS) in src/lib/calculator.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3.  Complete Phase 3: User Story 1
4.  **STOP and VALIDATE**: Test User Story 1 independently
5.  Deploy/demo if ready

### Incremental Delivery

1.  Complete Setup + Foundational → Foundation ready
2.  Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3.  Add User Story 2 → Test independently → Deploy/Demo
4.  Add User Story 3 → Test independently → Deploy/Demo
5.  Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1.  Team completes Setup + Foundational together
2.  Once Foundational is done:
    -   Developer A: User Story 1
    -   Developer B: User Story 2
    -   Developer C: User Story 3
3.  Stories complete and integrate independently

---

## Notes

-   [P] tasks = different files, no dependencies
-   [Story] label maps task to specific user story for traceability
-   Each user story should be independently completable and testable
-   Verify tests fail before implementing
-   Commit after each task or logical group
-   Stop at any checkpoint to validate story independently
-   Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
