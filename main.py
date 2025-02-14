import pandas as pd
import streamlit as st

from Services.task_service import Task_Service
from Services.user_service import User_Service

# Initialize services
task_service = Task_Service()
user_service = User_Service()

st.title("📝 Task Management System")

# Tabs for navigation
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Tasks", "Users", "Task History", "Complete Tasks", "Delete Tasks"]
)

# --- TASK MANAGEMENT ---
with tab1:
    st.header("📌 Task Management")

    # Fetch the next available Task ID
    next_task_id = task_service.get_next_task_id()

    # Auto-fill the Task ID field
    task_id = st.number_input(
        "Task ID",
        min_value=1,
        step=1,
        value=next_task_id,
        disabled=True,
    )
    task_title = st.text_input("Task Title")
    task_desc = st.text_area("Task Description")
    assigned_user = st.selectbox(
        "Assign Task To",
        ["None"] + [user.name for user in user_service.get_all_users().values()],
    )

    if st.button("Create Task"):
        try:
            assigned_user_id = next(
                (
                    uid
                    for uid, user in user_service.get_all_users().items()
                    if user.name == assigned_user
                ),
                None,
            )
            task_service.create_task(task_id, task_title, task_desc, assigned_user_id)
            st.success(f"Task '{task_title}' created successfully!")
            st.rerun()
        except ValueError as e:
            st.error(str(e))

# --- USER MANAGEMENT ---
with tab2:
    st.header("👤 User Management")

    # Fetch the next available User ID
    next_user_id = user_service.get_next_user_id()

    # Add a user
    user_id = st.number_input(
        "User ID",
        min_value=1000,
        step=1,
        value=next_user_id,
        disabled=True,
    )
    user_name = st.text_input("User Name")
    user_email = st.text_input("User Email")

    if st.button("Add User"):
        user_service.add_user(user_id, user_name, user_email)
        st.success(f"User '{user_name}' added!")
        st.rerun()

    # Retrieve user details
    fetch_user_id = st.number_input("Get User by ID", min_value=1000, step=1)
    if st.button("Get User"):
        user = user_service.get_users(fetch_user_id)
        if user:
            st.write(f"**Name:** {user.name}")
            st.write(f"**Email:** {user.email}")
        else:
            st.warning("User not found!")

# --- TASK HISTORY TAB ---
with tab3:
    st.header("📜 Task History")

    # Fetch completed tasks
    task_history = task_service.get_task_history()

    # Convert task history to a DataFrame for display
    if task_history:
        df = pd.DataFrame(
            [
                {
                    "Task ID": task.id,
                    "Title": task.title,
                    "Description": task.description,
                    "Assigned User ID": str(task.assigned_user_id)
                    if task.assigned_user_id
                    else "Unassigned",
                }
                for task in task_history
            ]
        )
        st.dataframe(df)
    else:
        st.write("No completed tasks yet.")

# --- TASK COMPLETION TAB ---
with tab4:
    st.header("✅ Complete a Task")

    pending_tasks = task_service.get_pending_tasks()

    if pending_tasks:
        selected_task = st.selectbox(
            "Select Task to Complete",
            [f"{task.id} - {task.title}" for task in pending_tasks],
        )

        if st.button("Complete Selected Task"):
            task_id_to_complete = int(selected_task.split(" - ")[0])  # Extract Task ID
            completed_task = task_service.complete_task(task_id_to_complete)

            if completed_task:
                st.success(
                    f"Task '{completed_task.title}' (ID: {completed_task.id}) completed!"
                )
                st.rerun()
            else:
                st.warning("Task not found or already completed.")
    else:
        st.write("No pending tasks to complete.")

# --- TASK DELETION TAB ---
with tab5:
    st.header("🗑 Delete a Task")

    all_tasks = (
        task_service.get_task_history() + task_service.get_pending_tasks()
    )  # Show all tasks for deletion

    if all_tasks:
        task_to_delete = st.selectbox(
            "Select Task to Delete",
            [f"{task.id} - {task.title}" for task in all_tasks],
        )

        if st.button("Delete Selected Task"):
            task_id_to_delete = int(task_to_delete.split(" - ")[0])  # Extract Task ID
            task_service.delete_task(task_id_to_delete)
            st.warning(f"Task '{task_to_delete}' has been deleted.")
            st.rerun()
    else:
        st.write("No tasks available for deletion.")
