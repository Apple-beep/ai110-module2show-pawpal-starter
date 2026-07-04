from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    task = Task("Morning walk", "08:00", 30, "high", "daily", "2026-07-04")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True
    assert task.is_pending() is False


def test_pet_add_task():
    pet = Pet("Biscuit", "Dog", 3)
    task = Task("Feeding", "09:00", 10, "medium", "daily", "2026-07-04")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Feeding"


def test_owner_get_all_tasks():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    dog.add_task(Task("Walk", "08:00", 30, "high", "daily", "2026-07-04"))
    cat.add_task(Task("Feeding", "09:00", 10, "medium", "daily", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    all_tasks = owner.get_all_tasks()

    assert len(all_tasks) == 2


def test_scheduler_sorts_tasks_chronologically_across_pets():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    dog.add_task(Task("Later task", "12:00", 30, "low", "once", "2026-07-04"))
    cat.add_task(Task("Earlier task", "08:00", 15, "high", "once", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_due_time()

    assert sorted_tasks[0][1].description == "Earlier task"
    assert sorted_tasks[1][1].description == "Later task"


def test_scheduler_sorts_tasks_across_different_dates():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)

    dog.add_task(Task("Tomorrow task", "07:00", 15, "medium", "once", "2026-07-05"))
    dog.add_task(Task("Today task", "18:00", 15, "medium", "once", "2026-07-04"))

    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_due_time()

    assert sorted_tasks[0][1].description == "Today task"
    assert sorted_tasks[1][1].description == "Tomorrow task"


def test_scheduler_sorts_tasks_by_priority():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)

    dog.add_task(Task("Low priority task", "08:00", 10, "low", "once", "2026-07-04"))
    dog.add_task(Task("High priority task", "09:00", 10, "high", "once", "2026-07-04"))

    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_tasks_by_priority()

    assert sorted_tasks[0][1].description == "High priority task"
    assert sorted_tasks[1][1].description == "Low priority task"


def test_filter_tasks_by_pet_status_and_priority():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    completed_task = Task("Completed walk", "08:00", 30, "high", "once", "2026-07-04")
    completed_task.mark_complete()

    dog.add_task(completed_task)
    cat.add_task(Task("Pending feeding", "09:00", 10, "medium", "daily", "2026-07-04"))
    cat.add_task(Task("Low priority grooming", "10:00", 20, "low", "weekly", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    filtered_tasks = scheduler.filter_tasks(
        pet_name="Mochi",
        completed=False,
        priority="medium"
    )

    assert len(filtered_tasks) == 1
    assert filtered_tasks[0][0].name == "Mochi"
    assert filtered_tasks[0][1].description == "Pending feeding"


def test_filter_pending_tasks_excludes_completed_tasks():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)

    completed_task = Task("Completed task", "08:00", 10, "high", "once", "2026-07-04")
    completed_task.mark_complete()

    pending_task = Task("Pending task", "09:00", 10, "medium", "once", "2026-07-04")

    dog.add_task(completed_task)
    dog.add_task(pending_task)
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    pending_tasks = scheduler.filter_pending_tasks()

    assert len(pending_tasks) == 1
    assert pending_tasks[0][1].description == "Pending task"


def test_conflict_detection_flags_overlapping_tasks():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    dog.add_task(Task("Walk", "08:00", 30, "high", "daily", "2026-07-04"))
    cat.add_task(Task("Feeding", "08:15", 10, "medium", "daily", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_conflict_detection_flags_exact_same_time():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    dog.add_task(Task("Medication", "08:00", 10, "high", "daily", "2026-07-04"))
    cat.add_task(Task("Breakfast", "08:00", 10, "medium", "daily", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1


def test_pet_with_no_tasks_returns_empty_schedule():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)

    owner.add_pet(dog)

    scheduler = Scheduler(owner)

    assert scheduler.get_all_tasks() == []
    assert scheduler.sort_tasks_by_due_time() == []
    assert scheduler.filter_pending_tasks() == []


def test_complete_daily_task_creates_next_occurrence():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    task = Task("Morning walk", "08:00", 30, "high", "daily", "2026-07-04")

    dog.add_task(task)
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(dog, task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == "2026-07-05"
    assert next_task.completed is False
    assert len(dog.tasks) == 2


def test_complete_weekly_task_creates_next_occurrence():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    task = Task("Grooming", "10:00", 45, "low", "weekly", "2026-07-04")

    dog.add_task(task)
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(dog, task)

    assert next_task is not None
    assert next_task.due_date == "2026-07-11"
    assert len(dog.tasks) == 2


def test_complete_once_task_does_not_create_recurring_task():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    task = Task("Vet appointment", "09:00", 60, "high", "once", "2026-07-04")

    dog.add_task(task)
    owner.add_pet(dog)

    scheduler = Scheduler(owner)
    next_task = scheduler.complete_task(dog, task)

    assert task.completed is True
    assert next_task is None
    assert len(dog.tasks) == 1
