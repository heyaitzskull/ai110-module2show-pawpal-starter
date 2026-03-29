from pawpal_system import Owner, Pet, Task, PawPalSystem

# Create an Owner
owner = Owner(name="John Doe", contact_info="john@example.com")

# Create at least two Pets
pet1 = Pet(name="Buddy", type="dog", age=3)
pet2 = Pet(name="Whiskers", type="cat", age=2)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create at least three Tasks with different durations
task1 = Task(description="Walk Buddy", duration=30, priority="high")
task2 = Task(description="Feed Whiskers", duration=10, priority="medium")
task3 = Task(description="Play with Buddy", duration=20, priority="low")

# Assign tasks to pets
pet1.add_task(task1)
pet1.add_task(task3)
pet2.add_task(task2)

# Print Today's Schedule
print("Today's Schedule:")
for pet in owner.pets:
    print(f"\nPet: {pet.name} ({pet.type})")
    for task in pet.tasks:
        print(f"  - {task.description} (Duration: {task.duration} min, Priority: {task.priority}, Status: {task.status})")