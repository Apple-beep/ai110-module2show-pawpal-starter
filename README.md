# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | | e.g., by priority, duration |
| Filtering | | e.g., skip tasks if time runs out |
| Conflict handling | | e.g., overlapping time slots |
| Recurring tasks | | e.g., daily vs. weekly |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

## Phase 2 CLI Demo Output

The backend logic was tested first through `main.py` before connecting it to the Streamlit UI.

```text
Today's Schedule by Time
========================
08:00 | Biscuit (Dog) | Morning walk | 30 min | priority: high | frequency: daily | Pending
08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Today's Schedule by Priority
============================
08:00 | Biscuit (Dog) | Morning walk | 30 min | priority: high | frequency: daily | Pending
09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Pending Tasks
=============
08:00 | Biscuit (Dog) | Morning walk | 30 min | priority: high | frequency: daily | Pending
08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Schedule Conflicts
==================
Conflict: Biscuit's 'Morning walk' overlaps with Mochi's 'Breakfast feeding'

Pending Tasks After Completing Morning Walk
===========================================
08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending
```

## Phase 4 Smarter Scheduling

PawPal+ now includes an algorithmic scheduling layer that works across multiple pets.

| Feature | Method(s) | Description |
|---|---|---|
| Sort by time | `Scheduler.sort_tasks_by_due_time()` | Sorts all pet care tasks by due date and due time |
| Sort by priority | `Scheduler.sort_tasks_by_priority()` | Places high-priority tasks before medium and low-priority tasks |
| Filter by pet/status/priority | `Scheduler.filter_tasks()` and `Scheduler.filter_by_pet()` | Filters tasks by selected pet, completion status, and priority |
| Pending task filtering | `Scheduler.filter_pending_tasks()` | Shows only incomplete tasks across all pets |
| Conflict detection | `Scheduler.detect_conflicts()` | Detects overlapping task windows across pets |
| Recurring task handling | `Task.next_occurrence()` and `Scheduler.complete_task()` | Creates the next daily or weekly task when a recurring task is completed |

### Phase 4 CLI Output

```text
Today's Schedule by Time
========================
2026-07-04 08:00 | Biscuit (Dog) | Morning walk | 30 min | priority: high | frequency: daily | Pending
2026-07-04 08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
2026-07-04 09:00 | Biscuit (Dog) | Vet appointment | 60 min | priority: high | frequency: once | Pending
2026-07-04 10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Tasks for Mochi
===============
2026-07-04 08:20 | Mochi (Cat) | Breakfast feeding | 10 min | priority: medium | frequency: daily | Pending
2026-07-04 10:30 | Mochi (Cat) | Clean litter box | 15 min | priority: low | frequency: daily | Pending

Schedule Conflicts
==================
Conflict: Biscuit's 'Morning walk' overlaps with Mochi's 'Breakfast feeding'

Recurring Task Created
======================
Biscuit's next 'Morning walk' is scheduled for 2026-07-05 at 08:00.
```
