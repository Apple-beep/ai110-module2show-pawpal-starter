from pawpal_system import Owner, Pet, Task, Scheduler


def print_schedule(title, scheduled_tasks):
    print(f"\n{title}")
    print("=" * len(title))

    if not scheduled_tasks:
        print("No tasks found.")
        return

    for pet, task in scheduled_tasks:
        status = "Done" if task.completed else "Pending"
        print(
            f"{task.due_date} {task.due_time} | {pet.name} ({pet.species}) | "
            f"{task.description} | {task.duration_minutes} min | "
            f"priority: {task.priority} | frequency: {task.frequency} | {status}"
        )


def print_conflicts(conflicts):
    print("\nSchedule Conflicts")
    print("==================")

    if not conflicts:
        print("No conflicts found.")
        return

    for pet_a, task_a, pet_b, task_b in conflicts:
        print(
            f"Conflict: {pet_a.name}'s '{task_a.description}' "
            f"overlaps with {pet_b.name}'s '{task_b.description}'"
        )


def main():
    owner = Owner("Musharaf Khan Pathan", "musharaf@example.com")

    dog = Pet("Biscuit", "Dog", 3)
    cat = Pet("Mochi", "Cat", 2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    dog_walk = Task("Morning walk", "08:00", 30, "high", "daily", "2026-07-04")

    dog.add_task(Task("Vet appointment", "09:00", 60, "high", "once", "2026-07-04"))
    cat.add_task(Task("Clean litter box", "10:30", 15, "low", "daily", "2026-07-04"))
    dog.add_task(dog_walk)
    cat.add_task(Task("Breakfast feeding", "08:20", 10, "medium", "daily", "2026-07-04"))

    scheduler = Scheduler(owner)

    print_schedule("Today's Schedule by Time", scheduler.sort_tasks_by_due_time())
    print_schedule("Today's Schedule by Priority", scheduler.sort_tasks_by_priority())
    print_schedule("Pending Tasks", scheduler.filter_pending_tasks())
    print_schedule("Tasks for Mochi", scheduler.filter_by_pet("Mochi"))
    print_conflicts(scheduler.detect_conflicts())

    next_task = scheduler.complete_task(dog, dog_walk)

    print_schedule("Pending Tasks After Completing Morning Walk", scheduler.filter_pending_tasks())

    if next_task:
        print(
            f"\nRecurring Task Created\n"
            f"======================\n"
            f"{dog.name}'s next '{next_task.description}' is scheduled for "
            f"{next_task.due_date} at {next_task.due_time}."
        )


if __name__ == "__main__":
    main()
