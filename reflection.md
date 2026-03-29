# PawPal+ Project Reflection

3 core actions a user should be able to perform is to add a pet, see daily tasks, and edit pet/task info.

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

In my initial UML design, I created a simple structure to manage the components of the PawPal+ application. The main classes included are **Pet**, **Task**, and **Owner**.  

- The **Pet** class holds information about the pet, such as name, type, and age, and manages actions for adding or editing pet details.  
- The **Task** class manages care tasks for each pet, including descriptions, durations, and priorities, allowing users to create, edit, and mark tasks as completed.  
- The **Owner** class stores the pet owner's information, including name and contact details, as well as preferences for pet care, facilitating actions related to owner management.  

This design aims to clearly separate responsibilities among the classes, simplifying the management of pets, tasks, and owners.

1. **Pet**
   - **Attributes**: 
     - Name
     - Type (e.g., dog, cat)
     - Age
     - Owner information
   - **Methods**:
     - Add pet
     - Edit pet information
     - View pet details

2. **Task**
   - **Attributes**:
     - Description (e.g., walk, feed)
     - Duration
     - Priority
     - Status (completed, pending)
   - **Methods**:
     - Add task
     - Edit task
     - Mark task as completed

3. **Owner**
   - **Attributes**:
     - Name
     - Contact information
     - Preferences (e.g., preferred times for tasks)
     - Pets (list of Pet objects)
   - **Methods**:
     - Add owner
     - Edit owner information
     - View owner details

4. **Scheduler** *(the "Brain")*
   - **Attributes**:
     - `owner`: Owner — the single owner whose pets' tasks are managed
   - **Methods**:
     - `get_all_tasks()` → List[Task]: iterates `owner.pets`, then each `pet.tasks`, collecting every task across all pets
     - `get_pending_tasks()` → List[Task]: calls `get_all_tasks()` and filters for `status == 'pending'`
     - `get_tasks_by_priority()` → List[Task]: returns all tasks sorted high → medium → low priority
     - `get_tasks_for_pet(pet_name)` → List[Task]: finds the named pet in `owner.pets` and returns its `tasks` list directly
     - `get_daily_schedule()` → Dict[str, List[Task]]: groups pending tasks by pet name so the UI can show a per-pet daily view

   **Retrieval design:** The Scheduler does **not** query the flat `PawPalSystem.tasks` dict. Instead it walks the object graph: `owner.pets` (the list already maintained by `Owner.add_pet`) → `pet.tasks` (the list already maintained by `Pet.add_task`). This two-level traversal means tasks are always fetched in the context of the pet they belong to, which is exactly what's needed to produce a meaningful daily schedule.

   **Relationships:**
   - *Uses* `Owner` (holds a reference to one owner)
   - *Reads* `Pet.tasks` on each pet in `owner.pets`
   - *Reads* `Task` attributes (description, priority, status, duration)

**b. Design changes**
    - Did your design change during implementation?
        Yes, it became clearer that relationships needed to be explicit and centralized.
    - If yes, describe at least one change and why you made it.
        - Owner now tracks owned pets and keeps the owner/pet link synced.
        - Task can now attach to a specific Pet so task lists are never disconnected.
        - PawPalSystem manages all owners/pets/tasks and provides basic add/get/summary methods.

---

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
