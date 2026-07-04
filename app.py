from datetime import date

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.write("A smart pet care planner for organizing daily tasks across multiple pets.")


if "owner" not in st.session_state:
    st.session_state.owner = Scheduler.load_from_json("data.json")

if "last_message" in st.session_state:
    st.success(st.session_state.pop("last_message"))


owner = st.session_state.owner
scheduler = Scheduler(owner)


st.sidebar.header("Owner Info")

if st.sidebar.button("Reset Demo Data"):
    st.session_state.owner = Scheduler.load_from_json("data.json")
    st.session_state.last_message = "Demo data reset."
    scheduler.save_to_json("data.json")
                st.rerun()

with st.sidebar.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_email = st.text_input("Owner email", value=owner.email)
    update_owner = st.form_submit_button("Update Owner")

    if update_owner:
        owner.name = owner_name
        owner.email = owner_email
        scheduler.save_to_json("data.json")
        st.success("Owner information updated.")


st.header("1. Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    pet_species = st.text_input("Species", placeholder="Dog, Cat, Rabbit...")
    pet_age = st.number_input("Age", min_value=0, max_value=40, step=1)
    add_pet_button = st.form_submit_button("Add Pet")

    if add_pet_button:
        if not pet_name or not pet_species:
            st.error("Please enter both pet name and species.")
        elif any(pet.name.lower() == pet_name.lower() for pet in owner.list_pets()):
            st.error(f"{pet_name} already exists. Use a different pet name.")
        else:
            new_pet = Pet(pet_name, pet_species, int(pet_age))
            owner.add_pet(new_pet)
            scheduler.save_to_json("data.json")
            st.success(f"Added {pet_name} to {owner.name}'s pets.")


st.header("2. Add a Care Task")

pets = owner.list_pets()

if not pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    pet_names = [pet.name for pet in pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Choose pet", pet_names)
        task_description = st.text_input(
            "Task description",
            placeholder="Morning walk, feeding, medication..."
        )
        due_date = st.date_input("Due date", value=date.today())
        due_time = st.time_input("Due time")
        duration_minutes = st.number_input("Duration in minutes", min_value=5, max_value=240, step=5)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task_button = st.form_submit_button("Add Task")

        if add_task_button:
            selected_pet = next(pet for pet in pets if pet.name == selected_pet_name)

            if task_description:
                task = Task(
                    description=task_description,
                    due_time=due_time.strftime("%H:%M"),
                    duration_minutes=int(duration_minutes),
                    priority=priority,
                    frequency=frequency,
                    due_date=due_date.isoformat()
                )
                selected_pet.add_task(task)
                scheduler.save_to_json("data.json")
                st.success(f"Added task for {selected_pet.name}.")
            else:
                st.error("Please enter a task description.")


st.header("3. Today's Schedule")

if not pets:
    st.warning("No pets added yet.")
else:
    col1, col2, col3 = st.columns(3)

    with col1:
        pet_filter = st.selectbox("Filter by pet", ["All"] + [pet.name for pet in pets])

    with col2:
        status_filter = st.selectbox("Filter by status", ["All", "Pending", "Done"])

    with col3:
        priority_filter = st.selectbox("Filter by priority", ["All", "high", "medium", "low"])

    completed_filter = None
    if status_filter == "Pending":
        completed_filter = False
    elif status_filter == "Done":
        completed_filter = True

    selected_pet_filter = None if pet_filter == "All" else pet_filter
    selected_priority_filter = None if priority_filter == "All" else priority_filter

    schedule_tasks = scheduler.filter_tasks(
        pet_name=selected_pet_filter,
        completed=completed_filter,
        priority=selected_priority_filter
    )

    if not schedule_tasks:
        st.warning("No tasks match the selected filters.")
    else:
        schedule_rows = []

        for pet, task in schedule_tasks:
            schedule_rows.append(
                {
                    "Date": task.due_date,
                    "Start": task.due_time,
                    "End": task.end_datetime().strftime("%H:%M"),
                    "Pet": pet.name,
                    "Species": pet.species,
                    "Task": task.description,
                    "Duration": f"{task.duration_minutes} min",
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Done" if task.completed else "Pending",
                }
            )

        st.dataframe(schedule_rows, width="stretch")


st.header("4. Pending Tasks")

pending_tasks = scheduler.filter_pending_tasks()

if not pending_tasks:
    st.success("No pending tasks. Suspiciously productive, but acceptable.")
else:
    for pet, task in pending_tasks:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{task.due_date} {task.due_time}-{task.end_datetime().strftime('%H:%M')}** | **{pet.name}** | "
                f"{task.description} | {task.duration_minutes} min | "
                f"priority: {task.priority} | frequency: {task.frequency}"
            )

        with col2:
            if st.button("Mark complete", key=f"complete_{id(task)}"):
                next_task = scheduler.complete_task(pet, task)

                if next_task:
                    st.session_state.last_message = (
                        f"Completed task and created next recurring task for "
                        f"{next_task.due_date} at {next_task.due_time}."
                    )
                else:
                    st.session_state.last_message = "Task marked complete."

                st.rerun()


st.header("5. Schedule Conflicts")

conflicts = scheduler.detect_conflicts()

if not conflicts:
    st.success("No conflicts found.")
else:
    for pet_a, task_a, pet_b, task_b in conflicts:
        st.error(
            f"{pet_a.name}'s '{task_a.description}' overlaps with "
            f"{pet_b.name}'s '{task_b.description}'."
        )


st.header("6. Current Pets")

if not pets:
    st.write("No pets added yet.")
else:
    for pet in pets:
        st.subheader(f"{pet.name} the {pet.species}")
        st.write(f"Age: {pet.age}")
        st.write(f"Tasks: {len(pet.tasks)}")
