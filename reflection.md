# PawPal+ Project Reflection

3 core actions a user should be able to perform is to add a pet, see daily tasks, and edit pet/task info.

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

In my initial UML design, I created a simple structure to manage the components of the PawPal+ application. The main classes included are **Pet**, **Task**, **Owner**, **PawPalSystem**, and **Scheduler**.  

- The **Pet** class holds information about the pet, such as name, type, and age, and manages actions for adding or editing pet details.  
- The **Task** class manages care tasks for each pet, including descriptions, durations, priorities, status, time, frequency, and due dates, allowing users to create, edit, and mark tasks as completed, with support for recurring tasks.  
- The **Owner** class stores the pet owner's information, including name and contact details, as well as preferences for pet care, facilitating actions related to owner management.  
- The **PawPalSystem** class acts as the central hub, maintaining dictionaries of owners, pets, and tasks, and providing methods to add, retrieve, edit, and delete these entities.  
- The **Scheduler** class (the "Brain") focuses on querying and organizing tasks for scheduling purposes, like getting pending tasks, sorting by priority, and detecting conflicts.  

This design aims to clearly separate responsibilities among the classes, simplifying the management of pets, tasks, and owners.

1. **Pet**
   - **Attributes**: 
     - Name
     - Type (e.g., dog, cat)
     - Age
     - Owner (reference to Owner)
     - Tasks (list of Task objects)
   - **Methods**:
     - set_owner(owner)
     - add_task(task)
     - edit_pet_info(name, type, age)
     - view_pet_details()

2. **Task**
   - **Attributes**:
     - Description (e.g., walk, feed)
     - Duration
     - Priority
     - Status (completed, pending)
     - Pet (reference to Pet)
     - Time (HH:MM)
     - Frequency ('once', 'daily', 'weekly')
     - Due date (YYYY-MM-DD)
   - **Methods**:
     - assign_to_pet(pet)
     - edit_task(description, duration, priority)
     - mark_as_completed()

3. **Owner**
   - **Attributes**:
     - Name
     - Contact information
     - Preferences (dict)
     - Pets (list of Pet objects)
   - **Methods**:
     - add_pet(pet)
     - remove_pet(pet)
     - edit_owner_info(name, contact_info, preferences)
     - view_owner_details()

4. **PawPalSystem**
   - **Attributes**:
     - owners (dict of Owner)
     - pets (dict of Pet)
     - tasks (dict of Task)
   - **Methods**:
     - add_owner(owner)
     - add_pet(pet, owner_name)
     - add_task(task, pet_name)
     - get_owner(name)
     - get_pet(name)
     - get_task(description)
     - delete_task(description)
     - delete_pet(name)
     - edit_pet(name, ...)
     - edit_task(description, ...)
     - view_summary()

5. **Scheduler** *(the "Brain")*
   - **Attributes**:
     - `owner`: Owner: the single owner whose pets' tasks are managed
   - **Methods**:
     - `get_all_tasks()` → List[Task]: iterates `owner.pets`, then each `pet.tasks`, collecting every task across all pets
     - `get_pending_tasks()` → List[Task]: calls `get_all_tasks()` and filters for `status == 'pending'`
     - `get_tasks_by_priority()` → List[Task]: returns all tasks sorted high → medium → low priority
     - `get_tasks_for_pet(pet_name)` → List[Task]: finds the named pet in `owner.pets` and returns its `tasks` list directly
     - `get_daily_schedule()` → Dict[str, List[Task]]: groups pending tasks by pet name so the UI can show a per-pet daily view
     - `sort_by_time()` → List[Task]: sorts tasks by time
     - `filter_tasks(status, pet_name)` → List[Task]: filters tasks by status or pet
     - `detect_conflicts()` → List[str]: detects and reports scheduling conflicts

   **Retrieval design:** The Scheduler does **not** query the flat `PawPalSystem.tasks` dict. Instead it walks the object graph: `owner.pets` (the list already maintained by `Owner.add_pet`) → `pet.tasks` (the list already maintained by `Pet.add_task`). This two-level traversal means tasks are always fetched in the context of the pet they belong to, which is exactly what's needed to produce a meaningful daily schedule.

   **Relationships:** The links between Owner-Pet and Pet-Task ensure consistency. PawPalSystem provides centralized management, while Scheduler handles scheduling logic.

**b. Design changes**
    - Did your design change during implementation?
        Yes, it became clearer that relationships needed to be explicit and centralized.
    - If yes, describe at least one change and why you made it.
        - Owner now tracks owned pets and keeps the owner/pet link synced.
        - Task can now attach to a specific Pet so task lists are never disconnected.
        - PawPalSystem manages all owners/pets/tasks and provides basic add/get/summary methods.
        - Added PawPalSystem as the central registry to handle CRUD operations and maintain data integrity.
        - Enhanced Task with time, frequency, and due_date for better scheduling, and added recurring task logic.

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

    My scheduler takes into account time like sorting tasks by when they're scheduled and spotting conflicts, priority (ranking them from high to low), status (sticking to pending ones), due dates, and frequency for recurring tasks. I haven't woven in owner preferences yet, since I was zeroing in on the basics of task handling.

- How did you decide which constraints mattered most?
    I went with priority and time as the big ones because they're essential for solid daily planning. High-priority stuff needs to jump the queue, and timing helps dodge overlaps. Status keeps things tidy by hiding completed tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    The scheduler bundles tasks by pet for the daily view, which keeps it neat per-pet but skips global optimization across all pets. Conflicts get flagged on their own.
- Why is that tradeoff reasonable for this scenario?
    This works well here because pet care is all about each individual animal, so focusing one at a time feels natural. Plus, the conflict checker still nabs any issues without messing up the main display.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI throughout most of the project to brainstorming the UML, writing the class logic, building the Streamlit UI, and generating tests. The most useful prompts were specific ones like "implement mark_as_completed with daily/weekly recurrence" or "add conflict detection to the Scheduler." Asking for focused pieces worked better than broad ones.

**b. Judgment and verification**

When AI generated the conflict detection logic, it initially flagged any two tasks at the same time as a conflict even for different owners. I changed it to only flag conflicts within the same owner's pets since that's the actual use case. I verified it by tracing through the logic manually and checking a few test cases by hand.

---

## 4. Testing and Verification

**a. What you tested**

I tested task completion, daily and weekly recurrence, chronological sorting, and conflict detection. I also covered edge cases like empty task lists, single tasks, and tasks at midnight.

These tests mattered because the scheduling logic is the core of the app where if recurrence or sorting breaks, the whole daily plan is wrong.

**b. Confidence**

Confidence is about a 4/5. The main cases all pass. The gap is that conflict detection ignores task duration, so two 30-minute tasks at 09:00 won't conflict even if they actually overlap. I'd test duration-aware conflicts and multi-pet scheduling next.

---

## 5. Reflection

**a. What went well**

The class structure came together cleanly. The Owner-Pet and Pet-Task links stayed consistent throughout, and the Scheduler walking the object graph instead of querying a flat list felt like the right call.

**b. What you would improve**

I feel like I used AI too much on this project and would want to do more on my own next time where I am using AI to help when I'm stuck, not to do the work for me. After all the goal is to learn, not redirect the complete task for AI to complete. I'd also redesign conflict detection to account for task duration instead of just start time.

**c. Key takeaway**

Designing the system on paper first made implementation a lot smoother. When the classes and relationships were clear upfront, writing the actual code was mostly just filling in the blanks.
