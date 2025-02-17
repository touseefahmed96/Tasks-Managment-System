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
    # Due Date Selection
    due_date = st.date_input("Due Date")
    # Priority Selection
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])

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
            task_service.create_task(
                task_id,
                task_title,
                task_desc,
                str(due_date),
                priority,
                assigned_user_id,
            )
            st.success(
                f"Task '{task_title}' created successfully with Priority: {priority} and Due Date: {due_date}"
            )
            st.rerun()
        except ValueError as e:
            st.error(str(e))

    # --- TASK FILTERING SECTION ---
    st.subheader("🔍 Filter Tasks")

    # Dropdown for filtering by user
    user_list = {user.id: user.name for user in user_service.get_all_users().values()}
    user_filter = st.selectbox("Filter by User", ["All"] + list(user_list.values()))

    # Radio button for filtering by status
    status_filter = st.radio("Filter by Status", ["All", "Pending", "Completed"])

    # Get filtered tasks
    if user_filter != "All":
        user_id = next(uid for uid, name in user_list.items() if name == user_filter)
        filtered_tasks = task_service.get_tasks_by_user(user_id)
    else:
        filtered_tasks = (
            task_service.get_tasks_by_status(0 if status_filter == "Pending" else 1)
            if status_filter != "All"
            else task_service.get_pending_tasks()
            + task_service.get_tasks_with_due_dates_and_priority()
        )

    # Display filtered tasks in a DataFrame
    if filtered_tasks:
        df = pd.DataFrame(
            [
                {
                    "Task ID": t.id,
                    "Title": t.title,
                    "Description": t.description,
                    "Status": "Completed" if t.completed else "Pending",
                    "Assigned User": user_list.get(t.assigned_user_id, "Unassigned"),
                }
                for t in filtered_tasks
            ]
        )
        st.dataframe(df)
    else:
        st.write("No tasks match the selected filters.")

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
    task_history = task_service.get_tasks_with_due_dates_and_priority()

    # Convert task history to a DataFrame for display
    if task_history:
        df = pd.DataFrame(
            [
                {
                    "Task ID": task.id,
                    "Title": task.title,
                    "Description": task.description,
                    "Due Date": task.due_date,
                    "Priority": task.priority,
                    "Status": "Completed" if task.completed else "Pending",
                    "Assigned User": str(task.assigned_user_id)
                    if task.assigned_user_id
                    else "Unassigned",
                }
                for task in task_history
            ]
        )
        st.dataframe(df)
    else:
        st.write("No tasks found.")

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
        task_service.get_tasks_with_due_dates_and_priority()
        + task_service.get_pending_tasks()
    )

    if all_tasks:
        task_to_delete = st.selectbox(
            "Select Task to Delete",
            [f"{task.id} - {task.title}" for task in all_tasks],
            key="task_to_delete",
        )

        if "confirm_delete" not in st.session_state:
            st.session_state.confirm_delete = False

        if st.button("Delete Selected Task"):
            st.session_state.confirm_delete = True

        if st.session_state.confirm_delete:
            task_id_to_delete = int(task_to_delete.split(" - ")[0])

            st.warning(f"⚠️ Are you sure you want to delete **{task_to_delete}**?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Confirm Deletion"):
                    task_service.delete_task(task_id_to_delete)
                    st.success(f"✅ Task '{task_to_delete}' has been deleted.")
                    st.session_state.confirm_delete = False
                    st.rerun()

            with col2:
                if st.button("Cancel"):
                    st.session_state.confirm_delete = False
                    st.warning("Deletion cancelled.")

    else:
        st.write("No tasks available for deletion.")
