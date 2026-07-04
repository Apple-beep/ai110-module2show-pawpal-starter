# PawPal+

PawPal+ is a smart pet care management system built with Python and Streamlit. It helps a pet owner track pets, schedule care tasks, view pending tasks, detect schedule conflicts, and handle recurring routines.

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
- Display the schedule in a Streamlit table with warnings and success messages.

## Core Classes

| Class | Responsibility |
|---|---|
| `Owner` | Stores owner details and manages a list of pets |
| `Pet` | Stores pet details and manages that pet's tasks |
| `Task` | Represents one care task with due date, due time, duration, priority, frequency, and completion status |
| `Scheduler` | Organizes tasks across all pets using sorting, filtering, conflict detection, and recurrence logic |

## Smarter Scheduling

| Feature | Method(s) | Description |
|---|---|---|
| Sort by time | `Scheduler.sort_tasks_by_due_time()` | Sorts all pet care tasks by due date and due time |
| Sort by priority | `Scheduler.sort_tasks_by_priority()` | Places high-priority tasks before medium and low-priority tasks |
| Filter by pet/status/priority | `Scheduler.filter_tasks()` and `Scheduler.filter_by_pet()` | Filters tasks by selected pet, completion status, and priority |
| Pending task filtering | `Scheduler.filter_pending_tasks()` | Shows only incomplete tasks across all pets |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects overlapping task windows across multiple pets |
| Recurring task handling | `Task.next_occurrence()` and `Scheduler.complete_task()` | Creates the next daily or weekly task when a recurring task is completed |

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
