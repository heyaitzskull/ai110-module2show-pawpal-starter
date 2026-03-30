from pawpal_system import Owner, Pet, Task, PawPalSystem, Scheduler
import streamlit as st


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

# persist system objects across reruns
if "pawpal_system" not in st.session_state:
    st.session_state.pawpal_system = PawPalSystem()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, contact_info="", preferences={})
else:
    # Keep the same owner object but update name when changed
    if st.session_state.owner.name != owner_name:
        st.session_state.owner.name = owner_name

# Ensure owner is registered with the system
if owner_name not in st.session_state.pawpal_system.owners:
    st.session_state.pawpal_system.add_owner(st.session_state.owner)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, type=species, age=1)
    st.session_state.pawpal_system.add_pet(new_pet, owner_name=owner_name)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"Added pet: {new_pet.name} ({new_pet.type})")

# Live pets view from the system model (no task details here)
pet_summary = st.session_state.pawpal_system.view_summary().get("pets", [])
if pet_summary:
    st.markdown("### Pets")
    pet_table = [
        {"name": p["name"], "type": p["type"], "owner": p["owner"]}
        for p in pet_summary
    ]
    st.table(pet_table)
else:
    st.info("No pets in system yet. Add a pet to see the list.")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

pawpal_system = st.session_state.pawpal_system

def safe_key(*parts):
    return "_".join(str(p).replace(" ", "_").replace("/", "_").replace(".", "_").replace(":", "_") for p in parts)

def get_task_rows():
    return [
        {
            "description": t.description,
            "duration": t.duration,
            "priority": t.priority,
            "status": t.status,
            "pet": t.pet.name if t.pet else None,
        }
        for t in pawpal_system.tasks.values()
    ]

pet_options = list(pawpal_system.pets.keys())
if pet_options:
    assign_pet = st.selectbox("Assign task to pet", pet_options)
else:
    assign_pet = None
    st.warning("No pets available. Add a pet first.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

col4, col5 = st.columns(2)
with col4:
    task_time = st.text_input("Scheduled time (HH:MM)", value="09:00")
with col5:
    frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

if st.button("Add task"):
    if not assign_pet:
        st.error("Select a pet first before adding a task.")
    else:
        task = Task(description=task_title, duration=int(duration), priority=priority, time=task_time, frequency=frequency)
        pawpal_system.add_task(task, pet_name=assign_pet)
        st.success(f"Added task: {task.description} (for pet: {assign_pet})")

task_rows = get_task_rows()
if task_rows:
    st.write("Current tasks:")
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Manage Pets & Tasks")

if not pawpal_system.pets:
    st.info("No pets available. Add a pet to enable edit/delete actions.")

for pet in list(pawpal_system.pets.values()):
    with st.expander(f"{pet.name} ({pet.type})"):
        st.write(pet.view_pet_details())

        new_pet_name = st.text_input("Pet name", value=pet.name, key=safe_key("edit_pet_name", pet.name))
        new_type = st.selectbox("Species", ["dog", "cat", "other"], index=["dog", "cat", "other"].index(pet.type if pet.type in ["dog","cat","other"] else "other"), key=safe_key("edit_pet_type", pet.name))

        pet_actions = st.columns(2)
        if pet_actions[0].button("Save pet edits", key=safe_key("save_pet", pet.name)):
            success = pawpal_system.edit_pet(pet.name, new_name=new_pet_name.strip(), type=new_type)
            if success:
                st.success(f"Pet '{pet.name}' updated.")
            else:
                st.error("Failed to update pet (duplicate name or missing).")
            st.rerun()

        if pet_actions[1].button("Delete pet", key=safe_key("delete_pet", pet.name)):
            pawpal_system.delete_pet(pet.name)
            st.warning(f"Deleted pet: {pet.name} (and its tasks)")
            st.rerun()

        st.markdown("##### Tasks for this pet")
        if not pet.tasks:
            st.info("No tasks for this pet yet")

        for i, task in enumerate(list(pet.tasks)):
            with st.container():
                task_key = safe_key("task", pet.name, task.description, str(i))
                st.write(f"**{task.description}** — {task.duration} min — priority {task.priority} — status {task.status}")

                if task.status != "completed":
                    if st.button("Mark complete", key=safe_key("complete", task_key)):
                        task.mark_as_completed()
                        st.success(f"Task '{task.description}' marked complete")
                        st.rerun()

                edit_desc = st.text_input("Description", value=task.description, key=safe_key("edit_task_desc", task_key))
                edit_duration = st.number_input("Duration", min_value=1, max_value=240, value=task.duration, key=safe_key("edit_task_duration", task_key))
                edit_priority = st.selectbox("Priority", ["low", "medium", "high"], index=["low", "medium", "high"].index(task.priority if task.priority in ["low","medium","high"] else "low"), key=safe_key("edit_task_priority", task_key))

                task_controls = st.columns(3)
                if task_controls[0].button("Save task edits", key=safe_key("save_task", task_key)):
                    success = pawpal_system.edit_task(task.description, new_description=edit_desc.strip(), duration=int(edit_duration), priority=edit_priority)
                    if success:
                        st.success(f"Task '{task.description}' updated")
                    else:
                        st.error("Failed to update task (duplicate description or missing).")
                    st.rerun()

                if task_controls[1].button("Delete task", key=safe_key("delete_task", task_key)):
                    pawpal_system.delete_task(task.description)
                    st.warning(f"Deleted task: {task.description}")
                    st.rerun()

st.divider()

st.subheader("Build Schedule")

owner = st.session_state.owner
scheduler = Scheduler(owner=owner)

# --- Conflict warnings ---
conflicts = scheduler.detect_conflicts()
if conflicts:
    st.markdown("#### ⚠️ Scheduling Conflicts")
    for conflict in conflicts:
        # Parse out the key parts for a friendlier message
        st.warning(conflict)
    st.caption("Fix conflicts above before relying on this schedule — overlapping tasks mean your pet can't do both at once.")
else:
    st.success("No scheduling conflicts found.")

st.markdown("#### Daily Schedule")

# --- Filter controls ---
filter_col1, filter_col2 = st.columns(2)
with filter_col1:
    status_filter = st.selectbox("Filter by status", ["all", "pending", "completed"])
with filter_col2:
    pet_filter_options = ["all"] + [p.name for p in owner.pets]
    pet_filter = st.selectbox("Filter by pet", pet_filter_options)

# --- Build filtered + sorted task list ---
filtered = scheduler.filter_tasks(
    status=None if status_filter == "all" else status_filter,
    pet_name=None if pet_filter == "all" else pet_filter,
)
sorted_tasks = sorted(
    filtered,
    key=lambda t: (t.due_date, int(t.time.split(":")[0]) * 60 + int(t.time.split(":")[1]))
)

if sorted_tasks:
    rows = [
        {
            "Time": t.time,
            "Due": t.due_date,
            "Task": t.description,
            "Pet": t.pet.name if t.pet else "—",
            "Duration (min)": t.duration,
            "Priority": t.priority,
            "Frequency": t.frequency,
            "Status": t.status,
        }
        for t in sorted_tasks
    ]
    st.table(rows)
else:
    st.info("No tasks match the current filters.")
