from pawpal_system import Owner, Pet, Task, Scheduler


def test_task_completion():
    task = Task("Morning walk", "08:00", 30, "high", "daily")

    assert task.completed is False

    task.mark_complete()

    assert task.completed is True
    assert task.is_pending() is False


def test_pet_add_task():
    pet = Pet("Biscuit", "Dog", 3)
    task = Task("Feeding", "09:00", 10, "medium", "daily")

    assert len(pet.tasks) == 0

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0].description == "Feeding"


def test_scheduler_sorts_tasks_by_due_time():
    owner = Owner("Test Owner", "owner@example.com")
    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    dog.add_task(Task("Later task", "12:00", 30, "low"))
    cat.add_task(Task("Earlier task", "08:00", 15, "high"))

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

    dog.add_task(Task("Walk", "08:00", 30, "high"))
    cat.add_task(Task("Feeding", "08:15", 10, "medium"))

    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
