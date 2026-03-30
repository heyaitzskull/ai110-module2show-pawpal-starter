# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest
```

The tests cover three main areas: 

- **Task basics** marking tasks complete, adding tasks to pets
- **Sorting** chronological ordering, stable sort on ties, edge cases like midnight boundaries and empty/single-task lists
- **Recurrence** daily and weekly tasks auto-generating the next occurrence after completion, "once" tasks not recurring, chained completions, and attribute preservation across recurrences
- **Conflict detection** overlapping tasks for the same pet, different pets, and multiple tasks at the same time slot; verifying no false positives for different times or dates

**Confidence Level: 4/5**

The core scheduling logic holds up well across normal and edge cases. Knocked off one star because conflict detection doesn't account for task *duration* where two tasks at 09:00 with different end times won't conflict even if they actually overlap on the calendar.

---

## Features

- **Priority-based sorting**: Tasks are ranked high → medium → low so the most critical care always surfaces first.
- **Chronological sorting**: Tasks can be sorted by scheduled time (HH:MM) to produce a time-ordered daily plan.
- **Status & pet filtering**: Filter the task list by completion status (`pending`/`completed`), by pet name, or both at once for focused views.
- **Per-pet daily schedule**: Groups pending tasks by pet name so care responsibilities for each animal are visible at a glance.
- **Conflict detection**: Identifies scheduling conflicts by grouping tasks with the same due date and start time — flags both same-pet overlaps (multiple tasks for one animal) and cross-pet overlaps (tasks for different animals at the same slot).
- **Daily recurrence**: Completing a `daily` task automatically creates the next occurrence dated one day forward, preserving all original attributes.
- **Weekly recurrence**: Same as daily recurrence but advances the due date by seven days.
- **Cascading delete**: Deleting a pet removes all of its associated tasks from the system registry in one operation.
- **Rename-safe editing**: Renaming a pet or task updates the internal lookup key so existing references remain consistent.
