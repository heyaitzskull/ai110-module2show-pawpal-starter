from pawpal_system import Owner, Pet, Task, PawPalSystem, Scheduler

# Create an Owner
owner = Owner(name="John Doe", contact_info="john@example.com")

# Create at least two Pets
pet1 = Pet(name="Buddy", type="dog", age=3)
pet2 = Pet(name="Whiskers", type="cat", age=2)

# Add pets to owner
owner.add_pet(pet1)
owner.add_pet(pet2)

# Create at least three Tasks with different durations and times (out of order)
task1 = Task(description="Walk Buddy", duration=30, priority="high", time="14:00")
task2 = Task(description="Feed Whiskers", duration=10, priority="medium", time="08:00", frequency="daily")
task3 = Task(description="Play with Buddy", duration=20, priority="low", time="10:00")
task4 = Task(description="Groom Whiskers", duration=15, priority="medium", time="12:00")
task5 = Task(description="Brush Buddy", duration=10, priority="medium", time="14:00")  # Same time as Walk Buddy

# Assign tasks to pets
pet1.add_task(task1)
pet1.add_task(task3)
pet1.add_task(task5)  # Same time as task1
pet2.add_task(task2)
pet2.add_task(task4)

# Create Scheduler
scheduler = Scheduler(owner=owner)

# Detect conflicts
conflicts = scheduler.detect_conflicts()
if conflicts:
    print("Scheduling Conflicts Detected:")
    for conflict in conflicts:
        print(f"  - {conflict}")
else:
    print("No scheduling conflicts detected.")

# Mark one task as completed
task2.mark_as_completed()

# Print Today's Schedule again to see recurring task
print("\nAfter marking Feed Whiskers complete:")
for pet in owner.pets:
    print(f"\nPet: {pet.name} ({pet.type})")
    for task in pet.tasks:
        print(f"  - {task.description} (Due: {task.due_date}, Time: {task.time}, Status: {task.status}, Freq: {task.frequency})")

# Print Today's Schedule
print("Today's Schedule:")
for pet in owner.pets:
    print(f"\nPet: {pet.name} ({pet.type})")
    for task in pet.tasks:
        print(f"  - {task.description} (Due: {task.due_date}, Time: {task.time}, Duration: {task.duration} min, Priority: {task.priority}, Status: {task.status}, Freq: {task.frequency})")

# Test sorting by time
print("\nTasks sorted by time:")
sorted_tasks = scheduler.sort_by_time()
for task in sorted_tasks:
    print(f"  - {task.description} at {task.time}")

# Test filtering by status
print("\nPending tasks:")
pending_tasks = scheduler.filter_tasks(status="pending")
for task in pending_tasks:
    print(f"  - {task.description} ({task.status})")

# Test filtering by pet name
print("\nTasks for Buddy:")
buddy_tasks = scheduler.filter_tasks(pet_name="Buddy")
for task in buddy_tasks:
    print(f"  - {task.description} for {task.pet.name if task.pet else 'None'}")