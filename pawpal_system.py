from dataclasses import dataclass, field


@dataclass
class Task:
    description: str
    due_time: str
    duration_minutes: int
    priority: str
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_pending(self):
        """Return True if the task is not completed."""
        return not self.completed


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        """Add a care task to this pet."""
        self.tasks.append(task)

    def list_tasks(self):
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self):
        """Return only incomplete tasks."""
        return [task for task in self.tasks if task.is_pending()]


@dataclass
class Owner:
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
        """Return all tasks across all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.list_tasks())
        return all_tasks


@dataclass
class Scheduler:
    pets: list = field(default_factory=list)

    def get_all_tasks(self):
        """Collect all tasks across multiple pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.list_tasks())
        return all_tasks

    def sort_tasks_by_due_time(self):
        """Sort tasks by due time."""
        return sorted(self.get_all_tasks(), key=lambda task: task.due_time)

    def filter_pending_tasks(self):
        """Return incomplete tasks across all pets."""
        return [task for task in self.get_all_tasks() if task.is_pending()]

    def detect_conflicts(self):
        """Placeholder for future conflict detection logic."""
        pass
