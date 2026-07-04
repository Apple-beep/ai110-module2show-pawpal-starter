import json
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta


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
    due_date: str = field(default_factory=lambda: date.today().isoformat())
    completed: bool = False

    def mark_complete(self):
        """Mark the task as completed."""
        self.completed = True

    def is_pending(self):
        """Return True if the task has not been completed."""
        return not self.completed

    def start_datetime(self):
        """Return the task start as a datetime using due_date and due_time."""
        return datetime.strptime(f"{self.due_date} {self.due_time}", "%Y-%m-%d %H:%M")

    def end_datetime(self):
        """Return the task end time based on its duration."""
        return self.start_datetime() + timedelta(minutes=self.duration_minutes)

    def priority_value(self):
        """Return a numeric value used for priority sorting."""
        return PRIORITY_ORDER.get(self.priority.lower(), 4)

    def next_occurrence(self):
        """Create the next recurring task if the frequency is daily or weekly."""
        frequency = self.frequency.lower()
        current_date = date.fromisoformat(self.due_date)

        if frequency == "daily":
            next_date = current_date + timedelta(days=1)
        elif frequency == "weekly":
            next_date = current_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            due_time=self.due_time,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            due_date=next_date.isoformat()
        )

    def to_dict(self):
        """Convert this task into a JSON-safe dictionary."""
        return {
            "description": self.description,
            "due_time": self.due_time,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "frequency": self.frequency,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Task object from saved dictionary data."""
        return cls(
            description=data["description"],
            due_time=data["due_time"],
            duration_minutes=data["duration_minutes"],
            priority=data["priority"],
            frequency=data.get("frequency", "once"),
            due_date=data.get("due_date"),
            completed=data.get("completed", False),
        )


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

    def to_dict(self):
        """Convert this pet and its tasks into a JSON-safe dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "age": self.age,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Pet object from saved dictionary data."""
        pet = cls(
            name=data["name"],
            species=data["species"],
            age=data["age"],
        )
        pet.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return pet


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

    def to_dict(self):
        """Convert this owner and all pets into a JSON-safe dictionary."""
        return {
            "name": self.name,
            "email": self.email,
            "pets": [pet.to_dict() for pet in self.pets],
        }

    @classmethod
    def from_dict(cls, data):
        """Create an Owner object from saved dictionary data."""
        owner = cls(
            name=data.get("name", "Demo Owner"),
            email=data.get("email", "owner@example.com"),
        )
        owner.pets = [Pet.from_dict(pet_data) for pet_data in data.get("pets", [])]
        return owner


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

    def sort_tasks_by_due_time(self, tasks=None):
        """Sort tasks by date and time."""
        tasks_to_sort = self.get_all_tasks() if tasks is None else tasks
        return sorted(tasks_to_sort, key=lambda item: item[1].start_datetime())

    def sort_tasks_by_priority(self, tasks=None):
        """Sort tasks by priority and then date/time."""
        tasks_to_sort = self.get_all_tasks() if tasks is None else tasks
        return sorted(
            tasks_to_sort,
            key=lambda item: (item[1].priority_value(), item[1].start_datetime())
        )

    def filter_tasks(self, pet_name=None, completed=None, priority=None):
        """Filter tasks by pet name, completion status, and/or priority."""
        results = self.get_all_tasks()

        if pet_name:
            results = [
                (pet, task)
                for pet, task in results
                if pet.name.lower() == pet_name.lower()
            ]

        if completed is not None:
            results = [
                (pet, task)
                for pet, task in results
                if task.completed == completed
            ]

        if priority:
            results = [
                (pet, task)
                for pet, task in results
                if task.priority.lower() == priority.lower()
            ]

        return self.sort_tasks_by_due_time(results)

    def filter_by_pet(self, pet_name):
        """Return all tasks for one pet."""
        return self.filter_tasks(pet_name=pet_name)

    def filter_pending_tasks(self):
        """Return all incomplete tasks across all pets sorted by due time."""
        return self.filter_tasks(completed=False)

    def complete_task(self, pet, task):
        """Complete a task and create the next recurring task when needed."""
        if task.completed:
            return None

        task.mark_complete()
        next_task = task.next_occurrence()

        if next_task:
            pet.add_task(next_task)

        return next_task


    def save_to_json(self, file_path="data.json"):
        """Save owner, pet, and task data to a JSON file."""
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(self.owner.to_dict(), file, indent=2)

    @staticmethod
    def load_from_json(file_path="data.json"):
        """Load owner, pet, and task data from a JSON file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            return Owner.from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError):
            return Owner("Demo Owner", "owner@example.com")

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
