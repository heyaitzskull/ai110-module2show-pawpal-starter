from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime, date, timedelta
from collections import defaultdict

@dataclass
class Owner:
    name: str
    contact_info: str
    preferences: Dict[str, str] = field(default_factory=dict)
    pets: List['Pet'] = field(default_factory=list)

    def add_pet(self, pet: 'Pet'):
        """Add a pet to this owner and set the ownership reference."""
        if pet not in self.pets:
            self.pets.append(pet)
            pet.owner = self

    def remove_pet(self, pet: 'Pet'):
        """Remove a pet from this owner and clear the ownership reference."""
        if pet in self.pets:
            self.pets.remove(pet)
            pet.owner = None

    def edit_owner_info(self, name: Optional[str] = None, contact_info: Optional[str] = None, preferences: Optional[Dict[str, str]] = None):
        """Update owner fields with any provided values."""
        if name:
            self.name = name
        if contact_info:
            self.contact_info = contact_info
        if preferences is not None:
            self.preferences = preferences

    def view_owner_details(self):
        """Return a serializable dict of the owner's details."""
        return {
            'name': self.name,
            'contact_info': self.contact_info,
            'preferences': self.preferences,
            'pets': [pet.name for pet in self.pets],
        }

@dataclass
class Pet:
    name: str
    type: str  # e.g., dog, cat
    age: int
    owner: Optional[Owner] = None
    tasks: List['Task'] = field(default_factory=list)

    def set_owner(self, owner: Optional[Owner]):
        """Set the pet's owner and update owner-pet relationship."""
        if self.owner is not owner:
            if self.owner:
                self.owner.remove_pet(self)
            self.owner = owner
            if owner:
                owner.add_pet(self)

    def add_task(self, task: 'Task'):
        """Add a task to this pet and associate the task with this pet."""
        if task not in self.tasks:
            self.tasks.append(task)
            task.pet = self

    def edit_pet_info(self, name: Optional[str] = None, type: Optional[str] = None, age: Optional[int] = None):
        """Update pet attributes with provided values."""
        if name:
            self.name = name
        if type:
            self.type = type
        if age is not None:
            self.age = age

    def view_pet_details(self):
        """Return a serializable dict of the pet's details."""
        return {
            'name': self.name,
            'type': self.type,
            'age': self.age,
            'owner': self.owner.name if self.owner else None,
            'tasks': [task.description for task in self.tasks],
        }

@dataclass
class Task:
    description: str
    duration: int
    priority: str
    status: str = 'pending'
    pet: Optional[Pet] = None
    time: str = '00:00'  # HH:MM format
    frequency: str = 'once'  # 'once', 'daily', 'weekly'
    due_date: str = field(default_factory=lambda: date.today().isoformat())  # YYYY-MM-DD

    def assign_to_pet(self, pet: Pet):
        """Assign this task to the given pet."""
        self.pet = pet
        pet.add_task(self)

    def edit_task(self, description: Optional[str] = None, duration: Optional[int] = None, priority: Optional[str] = None):
        """Update task attributes with provided values."""
        if description:
            self.description = description
        if duration is not None:
            self.duration = duration
        if priority:
            self.priority = priority

    def mark_as_completed(self):
        """Mark the task status as completed. If recurring, create next occurrence."""
        self.status = 'completed'
        if self.frequency == 'daily' and self.pet:
            new_due_date = (date.fromisoformat(self.due_date) + timedelta(days=1)).isoformat()
            new_task = Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                time=self.time,
                frequency=self.frequency,
                due_date=new_due_date
            )
            self.pet.add_task(new_task)
        elif self.frequency == 'weekly' and self.pet:
            new_due_date = (date.fromisoformat(self.due_date) + timedelta(days=7)).isoformat()
            new_task = Task(
                description=self.description,
                duration=self.duration,
                priority=self.priority,
                time=self.time,
                frequency=self.frequency,
                due_date=new_due_date
            )
            self.pet.add_task(new_task)

class PawPalSystem:
    def __init__(self):
        """Initialize paw pal system with empty owner, pet, and task registries."""
        self.owners: Dict[str, Owner] = {}
        self.pets: Dict[str, Pet] = {}
        self.tasks: Dict[str, Task] = {}

    def add_owner(self, owner: Owner):
        """Register a new owner in the system."""
        self.owners[owner.name] = owner

    def add_pet(self, pet: Pet, owner_name: Optional[str] = None):
        """Register a new pet and optionally attach it to an owner."""
        self.pets[pet.name] = pet
        if owner_name and owner_name in self.owners:
            pet.set_owner(self.owners[owner_name])

    def add_task(self, task: Task, pet_name: Optional[str] = None):
        """Register a new task and optionally assign it to a pet."""
        self.tasks[task.description] = task
        if pet_name and pet_name in self.pets:
            task.assign_to_pet(self.pets[pet_name])

    def get_owner(self, name: str) -> Optional[Owner]:
        """Return owner by name, or None if not found."""
        return self.owners.get(name)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return pet by name, or None if not found."""
        return self.pets.get(name)

    def get_task(self, description: str) -> Optional[Task]:
        """Return task by description, or None if not found."""
        return self.tasks.get(description)

    def delete_task(self, task_description: str) -> bool:
        """Remove a task from the system and from its assigned pet."""
        task = self.get_task(task_description)
        if not task:
            return False
        if task.pet and task in task.pet.tasks:
            task.pet.tasks.remove(task)
        del self.tasks[task_description]
        return True

    def delete_pet(self, pet_name: str) -> bool:
        """Remove a pet and all related tasks from the system."""
        pet = self.get_pet(pet_name)
        if not pet:
            return False
        if pet.owner:
            pet.owner.remove_pet(pet)
        for task in list(pet.tasks):
            self.delete_task(task.description)
        if pet_name in self.pets:
            del self.pets[pet_name]
        return True

    def edit_pet(self, pet_name: str, new_name: Optional[str] = None, type: Optional[str] = None, age: Optional[int] = None) -> bool:
        """Edit pet details and update internal lookup key if name changes."""
        pet = self.get_pet(pet_name)
        if not pet:
            return False
        old_name = pet.name
        pet.edit_pet_info(name=new_name if new_name else None, type=type, age=age)
        if new_name and new_name != old_name:
            if new_name in self.pets:
                return False
            self.pets[new_name] = pet
            del self.pets[old_name]
        return True

    def edit_task(self, task_description: str, new_description: Optional[str] = None, duration: Optional[int] = None, priority: Optional[str] = None) -> bool:
        """Edit task details and update internal lookup key if description changes."""
        task = self.get_task(task_description)
        if not task:
            return False
        old_desc = task.description
        task.edit_task(description=new_description if new_description else None, duration=duration, priority=priority)
        if new_description and new_description != old_desc:
            if new_description in self.tasks:
                return False
            self.tasks[new_description] = task
            del self.tasks[old_desc]
        return True

    def view_summary(self):
        """Return a summary view of all owners, pets, and tasks."""
        return {
            'owners': [owner.view_owner_details() for owner in self.owners.values()],
            'pets': [pet.view_pet_details() for pet in self.pets.values()],
            'tasks': [{'description': t.description, 'status': t.status, 'pet': t.pet.name if t.pet else None} for t in self.tasks.values()],
        }


@dataclass
class Scheduler:
    owner: Owner

    def get_all_tasks(self) -> List[Task]:
        """Iterates owner.pets, then each pet.tasks, collecting every task across all pets."""
        tasks = []
        for pet in self.owner.pets:
            tasks.extend(pet.tasks)
        return tasks

    def get_pending_tasks(self) -> List[Task]:
        """Calls get_all_tasks() and filters for status == 'pending'."""
        return [task for task in self.get_all_tasks() if task.status == 'pending']

    def get_tasks_by_priority(self) -> List[Task]:
        """Returns all tasks sorted high → medium → low priority."""
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        return sorted(self.get_all_tasks(), key=lambda t: priority_order.get(t.priority, 3))

    def get_tasks_for_pet(self, pet_name: str) -> List[Task]:
        """Finds the named pet in owner.pets and returns its tasks list directly."""
        for pet in self.owner.pets:
            if pet.name == pet_name:
                return pet.tasks
        return []

    def get_daily_schedule(self) -> Dict[str, List[Task]]:
        """Groups pending tasks by pet name so the UI can show a per-pet daily view."""
        schedule = {}
        for task in self.get_pending_tasks():
            pet_name = task.pet.name if task.pet else 'Unassigned'
            if pet_name not in schedule:
                schedule[pet_name] = []
            schedule[pet_name].append(task)
        return schedule

    def sort_by_time(self) -> List[Task]:
        """Sort all tasks by their scheduled time in ascending order (HH:MM format)."""
        def time_to_minutes(t):
            h, m = map(int, t.split(':'))
            return h * 60 + m
        return sorted(self.get_all_tasks(), key=lambda t: time_to_minutes(t.time))

    def filter_tasks(self, status: Optional[str] = None, pet_name: Optional[str] = None) -> List[Task]:
        """Return a list of tasks filtered by optional status ('pending' or 'completed') and/or pet name."""
        tasks = self.get_all_tasks()
        if status:
            tasks = [t for t in tasks if t.status == status]
        if pet_name:
            tasks = [t for t in tasks if t.pet and t.pet.name == pet_name]
        return tasks

    def detect_conflicts(self) -> List[str]:
        """Identify scheduling conflicts based on due date and time, returning a list of warning messages for overlapping tasks."""
        warnings = []
        tasks = self.get_all_tasks()
        time_groups = defaultdict(list)
        for task in tasks:
            key = (task.due_date, task.time)
            time_groups[key].append(task)
        for key, group in time_groups.items():
            if len(group) > 1:
                pets = set(t.pet.name for t in group if t.pet)
                if len(pets) == 1:
                    pet_name = list(pets)[0]
                    task_descriptions = [t.description for t in group]
                    warnings.append(f"Conflict: Multiple tasks for pet '{pet_name}' at {key[1]} on {key[0]}: {', '.join(task_descriptions)}")
                else:
                    task_details = [f"{t.description} ({t.pet.name if t.pet else 'No pet'})" for t in group]
                    warnings.append(f"Conflict: Tasks for different pets at {key[1]} on {key[0]}: {', '.join(task_details)}")
        return warnings

