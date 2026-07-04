# PawPal+

PawPal+ is a smart pet care management system built with Python and Streamlit. It helps a pet owner track pets, schedule care tasks, view pending tasks, detect schedule conflicts, handle recurring routines, and save data between app runs.

## Project Overview

A busy pet owner needs a simple way to manage daily care tasks like feeding, walks, medication, grooming, and appointments. PawPal+ uses object-oriented programming to model owners, pets, tasks, and scheduling logic.

The backend logic lives in `pawpal_system.py`, the CLI demo lives in `main.py`, and the Streamlit UI lives in `app.py`.

## Features

- Add owner information.
- Add multiple pets.
- Add care tasks for each pet.
- Store task details including date, time, duration, priority, frequency, and completion status.
- Sort tasks by due date and time.
- Sort tasks by priority.
- Filter tasks by pet, status, and priority.
- Show pending tasks.
- Detect overlapping task conflicts across multiple pets.
- Mark tasks complete.
- Automatically create the next daily or weekly recurring task when a recurring task is completed.
- Save and load owner, pet, and task data using `data.json`.
- Display the schedule in a Streamlit table with warnings and success messages.

## Core Classes

| Class | Responsibility |
|---|---|
| `Owner` | Stores owner details and manages a list of pets |
| `Pet` | Stores pet details and manages that pet tasks |
| `Task` | Represents one care task with due date, due time, duration, priority, frequency, and completion status |
| `Scheduler` | Organizes tasks across all pets using sorting, filtering, conflict detection, recurrence logic, and JSON persistence |

## Smarter Scheduling

| Feature | Method | Description |
|---|---|---|
| Sort by time | `Scheduler.sort_tasks_by_due_time()` | Sorts all pet care tasks by due date and due time |
| Sort by priority | `Scheduler.sort_tasks_by_priority()` | Places high priority tasks before medium and low priority tasks |
| Filter by pet status and priority | `Scheduler.filter_tasks()` | Filters tasks by selected pet, completion status, and priority |
| Pending task filtering | `Scheduler.filter_pending_tasks()` | Shows only incomplete tasks across all pets |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects overlapping task windows across multiple pets |
| Recurring tasks | `Task.next_occurrence()` and `Scheduler.complete_task()` | Creates the next daily or weekly task when a recurring task is completed |
| Data persistence | `Scheduler.save_to_json()` and `Scheduler.load_from_json()` | Saves and loads owner, pet, and task data from `data.json` |

## Project Structure

```text
.
├── app.py
├── main.py
├── pawpal_system.py
├── README.md
├── reflection.md
├── ai_interactions.md
├── diagrams/
│   ├── uml.mmd
│   └── uml_final.mmd
└── tests/
    └── test_pawpal.py
```
## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the CLI Demo

```bash
python main.py
```

## Running the Streamlit App

```bash
streamlit run app.py
```

## Sample CLI Output

```text
Today's Schedule by Time
========================
2026-07-04 08:00 | Biscuit (Dog) | Morning walk | 30 min | priority: high | frequency: daily | Pending
2026-07-04 08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
2026-07-04 09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
2026-07-04 10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Schedule Conflicts
==================
Conflict: Biscuit's 'Morning walk' overlaps with Mochi's 'Breakfast feeding'

Recurring Task Created
======================
Biscuit's next 'Morning walk' is scheduled for 2026-07-05 at 08:00.
```

## Testing PawPal+

Run the test suite:

```bash
python -m pytest
```

The tests cover task completion, adding tasks to pets, owner task collection, sorting by time, sorting by priority, filtering by pet/status/priority, pending task filtering, conflict detection, empty schedules, daily recurrence, weekly recurrence, one-time tasks, and JSON save/load persistence.

Sample passing test output:

```text
collected 15 items

tests/test_pawpal.py ............... [100%]

15 passed
```

## Optional Extension: Data Persistence

PawPal+ supports JSON persistence using a local `data.json` file.

When the Streamlit app starts, it loads saved owner, pet, and task data from `data.json`. If no file exists, it starts with a default demo owner. When the user updates owner info, adds pets, adds tasks, marks tasks complete, or creates recurring tasks, the app saves the updated data back to `data.json`.

Files modified for persistence:

- `pawpal_system.py`
  - Added `to_dict()` and `from_dict()` methods for `Task`, `Pet`, and `Owner`.
  - Added `Scheduler.save_to_json()` and `Scheduler.load_from_json()`.
- `app.py`
  - Loads saved data into `st.session_state`.
  - Saves changes after user actions.
- `tests/test_pawpal.py`
  - Added a test verifying save/load behavior.

## Professional UI and Formatting

The Streamlit UI uses structured formatting through:

- `st.dataframe()` for the schedule table.
- `st.success()` for successful actions.
- `st.warning()` for empty states.
- `st.error()` for schedule conflict warnings.
- Start and end time formatting for pending tasks and conflicts.

This makes the output easier to read and helps users understand scheduling conflicts without reading backend code.

## Rubric Coverage

PawPal+ meets the required features by including a Mermaid UML diagram, four core OOP classes, scheduler algorithms, a CLI demo, pytest coverage, documentation, and reflection.

Stretch features attempted:

- Advanced algorithmic capability through conflict detection and recurrence.
- Data persistence using JSON.
- Advanced scheduling logic through priority sorting and time overlap detection.
- Professional UI formatting through Streamlit tables and status messages.
- Prompt comparison documented in `ai_interactions.md`.