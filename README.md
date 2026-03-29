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

## Smarter Scheduling

The scheduler now includes advanced features for better task management:
- **Time-based sorting**: Tasks can be sorted by scheduled time to create chronological daily plans.
- **Flexible filtering**: Filter tasks by status (pending/completed) or by specific pet for focused views.
- **Conflict detection**: Automatically identifies overlapping tasks on the same date and time, providing warnings to help avoid scheduling issues.
