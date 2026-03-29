import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from pawpal_system import Task, Pet

def test_task_completion():
    # Create a task
    task = Task(description="Test Task", duration=10, priority="medium")
    # Initially, status should be 'pending'
    assert task.status == 'pending'
    # Mark as completed
    task.mark_as_completed()
    # Now status should be 'completed'
    assert task.status == 'completed'

def test_task_addition():
    # Create a pet
    pet = Pet(name="Test Pet", type="dog", age=2)
    # Initially, no tasks
    assert len(pet.tasks) == 0
    # Create a task
    task = Task(description="Test Task", duration=10, priority="medium")
    # Add task to pet
    pet.add_task(task)
    # Now pet should have 1 task
    assert len(pet.tasks) == 1