from dataclasses import dataclass, field
from datetime import datetime, timedelta


PRIORITY_ORDER = {
    "high": 1,
    "medium": 2,
    "low": 3
}


@dataclass
class Task:
    """Represents one pet care task."""
    description: str
    due_time: str
    duration_minutes: int
    priority: str
    frequency: str = "once"
    completed: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def is_pending(self):
        """Return True when the task is not completed."""
        return not self.completed

    def start_datetime(self):
        """Convert the task due time into a datetime object."""
        return datetime.strptime(self.due_time, "%H:%M")

    def end_datetime(self):
        """Return the task end time based on its duration."""
        return self.start_datetime() + timedelta(minutes=self.duration_minutes)

    def priority_value(self):
        """Return a numeric value for sorting task priority."""
        return PRIORITY_ORDER.get(self.priority.lower(), 4)


@dataclass
class Pet:
    """Stores pet information and care tasks."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a task to this pet."""
        self.tasks.append(task)

    def list_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self):
        """Return incomplete tasks for this pet."""
        return [task for task in self.tasks if task.is_pending()]


@dataclass
class Owner:
    """Stores owner information and manages multiple pets."""
    name: str
    email: str
    pets: list = field(default_factory=list)

    def add_pet(self, pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def list_pets(self):
        """Return all pets owned by this owner."""
        return self.pets

    def get_all_tasks(self):
        """Return all tasks from all owned pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.list_tasks())
        return all_tasks


@dataclass
class Scheduler:
    """Organizes and manages tasks across multiple pets."""
    owner: Owner

    def get_all_tasks(self):
        """Return all tasks across all pets with pet information."""
        all_tasks = []
        for pet in self.owner.list_pets():
            for task in pet.list_tasks():
                all_tasks.append((pet, task))
        return all_tasks

    def sort_tasks_by_due_time(self):
        """Sort all tasks by due time."""
        return sorted(self.get_all_tasks(), key=lambda item: item[1].start_datetime())

    def sort_tasks_by_priority(self):
        """Sort all tasks by priority and then due time."""
        return sorted(
            self.get_all_tasks(),
            key=lambda item: (item[1].priority_value(), item[1].start_datetime())
        )

    def filter_pending_tasks(self):
        """Return all incomplete tasks across all pets sorted by due time."""
        pending_tasks = [
            (pet, task)
            for pet, task in self.get_all_tasks()
            if task.is_pending()
        ]
        return sorted(pending_tasks, key=lambda item: item[1].start_datetime())

    def detect_conflicts(self):
        """Detect overlapping task times across all pets."""
        conflicts = []
        sorted_tasks = self.sort_tasks_by_due_time()

        for i in range(len(sorted_tasks)):
            pet_a, task_a = sorted_tasks[i]

            for j in range(i + 1, len(sorted_tasks)):
                pet_b, task_b = sorted_tasks[j]

                if task_b.start_datetime() < task_a.end_datetime():
                    conflicts.append((pet_a, task_a, pet_b, task_b))
                else:
                    break

        return conflicts
