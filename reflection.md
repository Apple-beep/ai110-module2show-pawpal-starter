# PawPal+ Project Reflection

## 1. System Design

Three core actions a user should be able to perform:

1. Add owner and pet information so the system knows who owns each pet.
2. Add care tasks for each pet, such as feeding, walking, medication, grooming, or appointments.
3. Generate an organized daily schedule that shows pending tasks across multiple pets.

**a. Initial design**

I designed PawPal+ around four main classes: Owner, Pet, Task, and Scheduler.

The Owner class stores identifying information about the pet owner and keeps a list of pets. The Pet class stores each pet’s basic details and manages that pet’s care tasks. The Task class represents one care activity, including its description, due time, duration, priority, and completion status. The Scheduler class works across multiple pets and organizes their tasks using scheduling logic.

This design separates responsibilities clearly. Owner manages pets, Pet manages tasks, Task stores care task details, and Scheduler handles cross-pet planning. This makes the system easier to test and expand later.

**b. Design changes**

After reviewing the design, I kept the system simple and modular. I avoided adding unnecessary classes early because the core project only needs Owner, Pet, Task, and Scheduler. I also added methods like get_pending_tasks, sort_tasks_by_due_time, and filter_pending_tasks because they support the scheduling features required later in the project.



---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers due time, priority, completion status, task duration, and overlapping time conflicts. Due time matters because pet care tasks need to happen at realistic times. Priority matters because important tasks like medication, walks, or vet visits should be handled before lower-priority tasks. Completion status matters because completed tasks should not appear in the pending task list.

**b. Tradeoffs**

One tradeoff is that the scheduler detects conflicts but does not automatically reschedule them yet. This is reasonable for this stage because conflict detection is the first step toward smarter scheduling. It tells the user where the problem is instead of silently moving tasks in a way the owner may not expect.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, adding tasks to pets, sorting tasks by due time, and detecting scheduling conflicts. These tests are important because they verify the main workflow of the system: creating care tasks, assigning them to pets, organizing them, and identifying schedule problems.

**b. Confidence**

I am confident that the basic scheduler works correctly for simple daily tasks. The tests verify the most important behaviors, and the CLI demo shows the system working end-to-end. If I had more time, I would test invalid time formats, tasks with the same start time, empty pet lists, and automatic rescheduling.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
