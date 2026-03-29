from dataclasses import dataclass, field
from typing import Optional, List, Dict

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
        """Mark the task status as completed."""
        self.status = 'completed'

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

    def view_summary(self):
        """Return a summary view of all owners, pets, and tasks."""
        return {
            'owners': [owner.view_owner_details() for owner in self.owners.values()],
            'pets': [pet.view_pet_details() for pet in self.pets.values()],
            'tasks': [{'description': t.description, 'status': t.status, 'pet': t.pet.name if t.pet else None} for t in self.tasks.values()],
        }

