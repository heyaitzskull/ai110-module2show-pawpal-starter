import pytest
import sys
import os
from datetime import datetime, date, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pawpal_system import Task, Pet, Owner, Scheduler

# ==================== BASIC TASK TESTS ====================

def test_task_completion():
    """Verify task completion changes status to 'completed'."""
    task = Task(description="Test Task", duration=10, priority="medium")
    assert task.status == 'pending'
    task.mark_as_completed()
    assert task.status == 'completed'

def test_task_addition():
    """Verify tasks can be added to pets."""
    pet = Pet(name="Test Pet", type="dog", age=2)
    assert len(pet.tasks) == 0
    task = Task(description="Test Task", duration=10, priority="medium")
    pet.add_task(task)
    assert len(pet.tasks) == 1
    assert task.pet == pet


# ==================== SORTING TESTS ====================

def test_sort_by_time_chronological():
    """Verify tasks are sorted in chronological order (ascending time)."""
    owner = Owner(name="Alice", contact_info="alice@example.com")
    pet = Pet(name="Max", type="dog", age=3)
    owner.add_pet(pet)
    
    # Create tasks with out-of-order times
    task1 = Task(description="Evening walk", duration=30, priority="high", time="18:00")
    task2 = Task(description="Morning feed", duration=10, priority="high", time="08:00")
    task3 = Task(description="Afternoon play", duration=20, priority="medium", time="14:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    # Verify chronological order
    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].time == "14:00"
    assert sorted_tasks[2].time == "18:00"

def test_sort_by_time_identical_times():
    """Verify stable sorting when multiple tasks have identical times."""
    owner = Owner(name="Bob", contact_info="bob@example.com")
    pet = Pet(name="Buddy", type="dog", age=2)
    owner.add_pet(pet)
    
    task1 = Task(description="Walk", duration=30, priority="high", time="14:00")
    task2 = Task(description="Play", duration=20, priority="medium", time="14:00")
    task3 = Task(description="Groom", duration=15, priority="low", time="14:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    # All should have same time
    assert all(t.time == "14:00" for t in sorted_tasks)
    # Should maintain insertion order (stable sort)
    assert sorted_tasks[0].description == "Walk"
    assert sorted_tasks[1].description == "Play"
    assert sorted_tasks[2].description == "Groom"

def test_sort_by_time_midnight_boundary():
    """Verify midnight (00:00) and late night times sort correctly."""
    owner = Owner(name="Charlie", contact_info="charlie@example.com")
    pet = Pet(name="Whiskers", type="cat", age=1)
    owner.add_pet(pet)
    
    task1 = Task(description="Late night snack", duration=5, priority="low", time="23:30")
    task2 = Task(description="Midnight check", duration=5, priority="low", time="00:00")
    task3 = Task(description="Morning feed", duration=10, priority="high", time="06:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    assert sorted_tasks[0].time == "00:00"
    assert sorted_tasks[1].time == "06:00"
    assert sorted_tasks[2].time == "23:30"

def test_sort_by_time_empty_task_list():
    """Verify sorting handles empty task list gracefully."""
    owner = Owner(name="Dave", contact_info="dave@example.com")
    pet = Pet(name="Rocky", type="dog", age=5)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    assert sorted_tasks == []

def test_sort_by_time_single_task():
    """Verify sorting a single task returns it unchanged."""
    owner = Owner(name="Eve", contact_info="eve@example.com")
    pet = Pet(name="Bella", type="cat", age=3)
    owner.add_pet(pet)
    
    task = Task(description="Sole task", duration=15, priority="medium", time="12:00")
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    assert len(sorted_tasks) == 1
    assert sorted_tasks[0] == task


# ==================== RECURRENCE LOGIC TESTS ====================

def test_daily_recurrence_creates_next_task():
    """Verify marking a daily task complete creates a new task for the next day."""
    pet = Pet(name="Buddy", type="dog", age=2)
    today = date.today().isoformat()
    
    task = Task(
        description="Daily walk",
        duration=30,
        priority="high",
        time="09:00",
        frequency="daily",
        due_date=today
    )
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    assert pet.tasks[0].status == 'pending'
    
    # Mark as completed
    pet.tasks[0].mark_as_completed()
    
    # Should now have 2 tasks: original (completed) and new (pending)
    assert len(pet.tasks) == 2
    assert pet.tasks[0].status == 'completed'
    assert pet.tasks[1].status == 'pending'
    
    # New task should be due tomorrow
    tomorrow = (date.fromisoformat(today) + timedelta(days=1)).isoformat()
    assert pet.tasks[1].due_date == tomorrow
    assert pet.tasks[1].description == "Daily walk"
    assert pet.tasks[1].frequency == "daily"

def test_weekly_recurrence_creates_next_task():
    """Verify marking a weekly task complete creates a new task for 7 days later."""
    pet = Pet(name="Max", type="dog", age=4)
    today = date.today().isoformat()
    
    task = Task(
        description="Weekly bath",
        duration=45,
        priority="medium",
        time="14:00",
        frequency="weekly",
        due_date=today
    )
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    pet.tasks[0].mark_as_completed()
    
    assert len(pet.tasks) == 2
    assert pet.tasks[0].status == 'completed'
    assert pet.tasks[1].status == 'pending'
    
    # New task should be due in 7 days
    next_week = (date.fromisoformat(today) + timedelta(days=7)).isoformat()
    assert pet.tasks[1].due_date == next_week
    assert pet.tasks[1].frequency == "weekly"

def test_once_frequency_no_recurrence():
    """Verify that completing a 'once' frequency task does NOT create a new task."""
    pet = Pet(name="Whiskers", type="cat", age=2)
    
    task = Task(
        description="One-time vet visit",
        duration=60,
        priority="high",
        frequency="once"
    )
    pet.add_task(task)
    
    assert len(pet.tasks) == 1
    pet.tasks[0].mark_as_completed()
    
    # Should still only have 1 task (no new recurrence)
    assert len(pet.tasks) == 1
    assert pet.tasks[0].status == 'completed'

def test_daily_recurrence_chain():
    """Verify multiple completions create a chain of recurring tasks."""
    pet = Pet(name="Buddy", type="dog", age=3)
    today = date.today().isoformat()
    
    task = Task(
        description="Daily meal",
        duration=10,
        priority="high",
        time="08:00",
        frequency="daily",
        due_date=today
    )
    pet.add_task(task)
    
    # Complete the task twice
    pet.tasks[0].mark_as_completed()
    assert len(pet.tasks) == 2
    
    pet.tasks[1].mark_as_completed()
    assert len(pet.tasks) == 3
    
    # Verify the chain
    tomorrow = (date.fromisoformat(today) + timedelta(days=1)).isoformat()
    day_after = (date.fromisoformat(today) + timedelta(days=2)).isoformat()
    
    assert pet.tasks[0].status == 'completed'
    assert pet.tasks[0].due_date == today
    assert pet.tasks[1].status == 'completed'
    assert pet.tasks[1].due_date == tomorrow
    assert pet.tasks[2].status == 'pending'
    assert pet.tasks[2].due_date == day_after

def test_recurrence_preserves_task_attributes():
    """Verify that recurring tasks preserve duration, priority, time, and frequency."""
    pet = Pet(name="Max", type="dog", age=2)
    
    task = Task(
        description="Premium grooming",
        duration=120,
        priority="high",
        time="10:30",
        frequency="weekly"
    )
    pet.add_task(task)
    pet.tasks[0].mark_as_completed()
    
    new_task = pet.tasks[1]
    assert new_task.description == "Premium grooming"
    assert new_task.duration == 120
    assert new_task.priority == "high"
    assert new_task.time == "10:30"
    assert new_task.frequency == "weekly"

def test_recurring_task_without_pet():
    """Verify that completing a recurring task without a pet does NOT create a new task."""
    task = Task(
        description="Orphaned recurring task",
        duration=30,
        priority="medium",
        frequency="daily"
    )
    
    # Task has no pet assigned
    assert task.pet is None
    
    task.mark_as_completed()
    
    # Status should change but no new task created (no pet to add to)
    assert task.status == 'completed'


# ==================== CONFLICT DETECTION TESTS ====================

def test_conflict_detection_same_pet_same_time():
    """Verify that two tasks for the same pet at the same time are flagged as conflicts."""
    owner = Owner(name="Alice", contact_info="alice@example.com")
    pet = Pet(name="Buddy", type="dog", age=3)
    owner.add_pet(pet)
    
    task1 = Task(description="Walk", duration=30, priority="high", time="14:00")
    task2 = Task(description="Play", duration=20, priority="medium", time="14:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) > 0
    conflict_text = conflicts[0]
    assert "Conflict" in conflict_text
    assert "Buddy" in conflict_text
    assert "14:00" in conflict_text
    assert "Walk" in conflict_text
    assert "Play" in conflict_text

def test_conflict_detection_different_pets_same_time():
    """Verify that tasks for different pets at the same time are detected."""
    owner = Owner(name="Bob", contact_info="bob@example.com")
    pet1 = Pet(name="Buddy", type="dog", age=3)
    pet2 = Pet(name="Whiskers", type="cat", age=2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task(description="Dog walk", duration=30, priority="high", time="15:00")
    task2 = Task(description="Cat play", duration=20, priority="medium", time="15:00")
    
    pet1.add_task(task1)
    pet2.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) > 0
    conflict_text = conflicts[0]
    assert "Conflict" in conflict_text
    assert "Dog walk" in conflict_text
    assert "Cat play" in conflict_text

def test_no_conflict_different_times():
    """Verify no conflicts when tasks are at different times."""
    owner = Owner(name="Charlie", contact_info="charlie@example.com")
    pet = Pet(name="Max", type="dog", age=2)
    owner.add_pet(pet)
    
    task1 = Task(description="Morning walk", duration=30, priority="high", time="08:00")
    task2 = Task(description="Afternoon play", duration=20, priority="medium", time="14:00")
    task3 = Task(description="Evening feed", duration=10, priority="high", time="18:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 0

def test_no_conflict_empty_scheduler():
    """Verify no conflicts when there are no tasks."""
    owner = Owner(name="Dave", contact_info="dave@example.com")
    pet = Pet(name="Rocky", type="dog", age=5)
    owner.add_pet(pet)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) == 0

def test_conflict_detection_multiple_same_pet():
    """Verify conflict detection with 3+ tasks at same time for same pet."""
    owner = Owner(name="Eve", contact_info="eve@example.com")
    pet = Pet(name="Bella", type="cat", age=3)
    owner.add_pet(pet)
    
    task1 = Task(description="Meal 1", duration=10, priority="high", time="12:00")
    task2 = Task(description="Meal 2", duration=10, priority="high", time="12:00")
    task3 = Task(description="Treat", duration=5, priority="medium", time="12:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    assert len(conflicts) > 0
    conflict_text = conflicts[0]
    assert "Multiple tasks" in conflict_text or "Conflict" in conflict_text

def test_conflict_detection_different_dates():
    """Verify no conflicts when tasks are on different dates."""
    owner = Owner(name="Frank", contact_info="frank@example.com")
    pet = Pet(name="Charlie", type="dog", age=4)
    owner.add_pet(pet)
    
    today = date.today().isoformat()
    tomorrow = (date.fromisoformat(today) + timedelta(days=1)).isoformat()
    
    task1 = Task(description="Walk", duration=30, priority="high", time="14:00", due_date=today)
    task2 = Task(description="Walk", duration=30, priority="high", time="14:00", due_date=tomorrow)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    # Different dates should not conflict
    assert len(conflicts) == 0

def test_conflict_detection_with_recurring_tasks():
    """Verify conflict detection works with recurring tasks after completion."""
    owner = Owner(name="Grace", contact_info="grace@example.com")
    pet = Pet(name="Scout", type="dog", age=2)
    owner.add_pet(pet)
    
    today = date.today().isoformat()
    
    task1 = Task(
        description="Daily walk",
        duration=30,
        priority="high",
        time="09:00",
        frequency="daily",
        due_date=today
    )
    task2 = Task(
        description="Daily play",
        duration=20,
        priority="medium",
        time="09:00",
        due_date=today
    )
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    conflicts = scheduler.detect_conflicts()
    
    # Should detect conflict between walk and play at 09:00
    assert len(conflicts) > 0
    assert "09:00" in conflicts[0]