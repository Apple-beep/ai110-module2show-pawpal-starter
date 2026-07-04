# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform:

1. Add owner and pet information so the system knows who owns each pet.
2. Add care tasks for each pet, such as feeding, walking, medication, grooming, or appointments.
3. Generate an organized daily schedule that shows pending tasks across multiple pets.

**a. Initial design**

I designed PawPal+ around four main classes: Owner, Pet, Task, and Scheduler.

The Owner class stores identifying information about the pet owner and keeps a list of pets. The Pet class stores each pet’s basic details and manages that pet’s care tasks. The Task class represents one care activity, including its description, due date, due time, duration, priority, frequency, and completion status. The Scheduler class works across multiple pets and organizes their tasks using scheduling logic.

This design separates responsibilities clearly. Owner manages pets, Pet manages tasks, Task stores care task details, and Scheduler handles cross-pet planning. This makes the system easier to test and expand later.

**b. Design changes**

After reviewing the design, I kept the system simple and modular. I avoided adding unnecessary classes early because the core project only needs Owner, Pet, Task, and Scheduler. I added methods like `get_pending_tasks`, `sort_tasks_by_due_time`, `filter_tasks`, `complete_task`, and `detect_conflicts` because they directly support the scheduling features required later in the project.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers due date, due time, priority, completion status, task duration, frequency, and overlapping time conflicts. Due time matters because pet care tasks need to happen at realistic times. Priority matters because important tasks like medication, walks, or vet visits should be handled before lower-priority tasks. Completion status matters because completed tasks should not appear in the pending task list. Frequency matters because daily and weekly tasks should continue after the current occurrence is completed.

**b. Tradeoffs**

One tradeoff is that the scheduler detects conflicts but does not automatically reschedule them. This is reasonable because automatic rescheduling could make incorrect assumptions about the owner's real availability. A warning is safer and easier to verify.

Another tradeoff is that recurring tasks are only created after the current task is marked complete. This avoids filling the task list with too many future tasks, but it also means the app does not show a long-term calendar of recurring tasks yet.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to brainstorm the class structure, generate an initial Mermaid UML diagram, scaffold the Python dataclasses, and suggest scheduling methods. The most helpful prompts were specific ones, such as asking how the Scheduler should retrieve all tasks from an Owner's pets and how to sort tasks using a lambda function.

I also used AI to improve the CLI output, add pytest cases, and think through the Streamlit session state problem. This helped connect the backend classes to the UI without losing data every time Streamlit reran the script.

**b. Judgment and verification**

I did not accept every AI suggestion exactly as given. For example, I kept the class design limited to Owner, Pet, Task, and Scheduler instead of adding extra classes too early. This made the project easier to understand and closer to the rubric.

I verified the AI-generated logic by running `python main.py`, checking the printed schedule manually, and running `python -m pytest`. The tests confirmed task completion, task addition, sorting, filtering, conflict detection, and recurring task creation.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding tasks to pets, sorting tasks by due time, filtering tasks by pet and completion status, detecting scheduling conflicts, and creating the next occurrence of a recurring daily task. These tests are important because they verify the main workflow of the system: creating care tasks, assigning them to pets, organizing them, identifying schedule problems, and continuing recurring routines.

**b. Confidence**

I am confident that the basic scheduler works correctly for simple daily pet care planning. The CLI demo shows the system working end-to-end, and the pytest suite verifies the most important behaviors. If I had more time, I would test invalid time formats, tasks with the same start time, weekly recurring tasks, empty owner/pet lists, and automatic rescheduling suggestions.

---

## 5. Reflection

**a. What went well**

I am most satisfied with the Scheduler class because it became the main brain of the system. It can organize tasks across multiple pets, sort by time and priority, filter tasks, detect conflicts, and create recurring tasks.

**b. What you would improve**

If I had another iteration, I would add a stronger scheduling system that suggests the next available time slot when conflicts happen. I would also improve the Streamlit UI so users can edit or delete pets and tasks instead of only adding and completing them.

**c. Key takeaway**

One important thing I learned is that good system design starts with clear responsibilities. Keeping Owner, Pet, Task, and Scheduler separate made the code easier to test, debug, and connect to the UI. I also learned that AI is useful for scaffolding and brainstorming, but the final design still needs human review and testing.
