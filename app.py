import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="wide")

st.title("🐾 PawPal+")
st.write("A smart pet care planner for organizing daily tasks across multiple pets.")


# Streamlit reruns the file after every interaction, so we store the Owner object
# in session_state to keep pets and tasks alive during the browser session.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Demo Owner", "owner@example.com")


owner = st.session_state.owner
scheduler = Scheduler(owner)


st.sidebar.header("Owner Info")

with st.sidebar.form("owner_form"):
    owner_name = st.text_input("Owner name", value=owner.name)
    owner_email = st.text_input("Owner email", value=owner.email)
    update_owner = st.form_submit_button("Update Owner")

    if update_owner:
        owner.name = owner_name
        owner.email = owner_email
        st.success("Owner information updated.")


st.header("1. Add a Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    pet_species = st.text_input("Species")
    pet_age = st.number_input("Age", min_value=0, max_value=40, step=1)
    add_pet_button = st.form_submit_button("Add Pet")

    if add_pet_button:
        if pet_name and pet_species:
            new_pet = Pet(pet_name, pet_species, int(pet_age))
            owner.add_pet(new_pet)
            st.success(f"Added {pet_name} to {owner.name}'s pets.")
        else:
            st.error("Please enter both pet name and species.")


st.header("2. Add a Care Task")

pets = owner.list_pets()

if not pets:
    st.info("Add at least one pet before scheduling tasks.")
else:
    pet_names = [pet.name for pet in pets]

    with st.form("add_task_form"):
        selected_pet_name = st.selectbox("Choose pet", pet_names)
        task_description = st.text_input("Task description", placeholder="Morning walk, feeding, medication...")
        due_time = st.time_input("Due time")
        duration_minutes = st.number_input("Duration in minutes", min_value=5, max_value=240, step=5)
        priority = st.selectbox("Priority", ["high", "medium", "low"])
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        add_task_button = st.form_submit_button("Add Task")

        if add_task_button:
            selected_pet = next(pet for pet in pets if pet.name == selected_pet_name)
            task = Task(
                description=task_description,
                due_time=due_time.strftime("%H:%M"),
                duration_minutes=int(duration_minutes),
                priority=priority,
                frequency=frequency
            )

            if task_description:
                selected_pet.add_task(task)
                st.success(f"Added task for {selected_pet.name}.")
            else:
                st.error("Please enter a task description.")


st.header("3. Today's Schedule")

all_tasks = scheduler.sort_tasks_by_due_time()

if not all_tasks:
    st.warning("No tasks scheduled yet.")
else:
    schedule_rows = []

    for pet, task in all_tasks:
        schedule_rows.append(
            {
                "Time": task.due_time,
                "Pet": pet.name,
                "Species": pet.species,
                "Task": task.description,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Status": "Done" if task.completed else "Pending",
            }
        )

    st.dataframe(schedule_rows, use_container_width=True)


st.header("4. Pending Tasks")

pending_tasks = scheduler.filter_pending_tasks()

if not pending_tasks:
    st.success("No pending tasks. Suspiciously productive, but acceptable.")
else:
    for pet, task in pending_tasks:
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(
                f"**{task.due_time}** | **{pet.name}** | "
                f"{task.description} | {task.duration_minutes} min | "
                f"priority: {task.priority}"
            )

        with col2:
            if st.button("Mark complete", key=f"complete_{pet.name}_{task.description}_{task.due_time}"):
                task.mark_complete()
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
