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


def test_scheduler_sorts_tasks_by_due_time():
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


def test_scheduler_detects_conflicts():
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


def test_filter_tasks_by_pet_and_status():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    completed_task = Task("Completed walk", "08:00", 30, "high", "once", "2026-07-04")
    completed_task.mark_complete()

    dog.add_task(completed_task)
    cat.add_task(Task("Pending feeding", "09:00", 10, "medium", "daily", "2026-07-04"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    filtered_tasks = scheduler.filter_tasks(pet_name="Mochi", completed=False)

    assert len(filtered_tasks) == 1
    assert filtered_tasks[0][0].name == "Mochi"
    assert filtered_tasks[0][1].description == "Pending feeding"


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
