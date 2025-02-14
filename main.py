import streamlit as st

from Services.task_service import Task_Service
from Services.user_service import User_Service

# Initialize services
task_service = Task_Service()
user_service = User_Service()

st.title("📝 Task Management System")

# Tabs for navigation
tab1, tab2 = st.tabs(["Tasks", "Users"])

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

    # Complete a task
    if st.button("Complete Task"):
        completed_task = task_service.complete_task()
        if completed_task:
            st.success(f"Task '{completed_task[1]}' completed!")
        else:
            st.warning("No pending tasks.")

    # Display Task History
    st.subheader("✅ Completed Tasks")
    task_history = task_service.get_task_history()
    if task_history:
        for task in task_history:
            st.write(
                f"**{task.title}** - Assigned to: {task.assigned_user_id or 'Unassigned'}"
            )
    else:
        st.write("No completed tasks yet.")

# --- USER MANAGEMENT ---
with tab2:
    st.header("👤 User Management")

    # Add a user
    user_id = st.number_input("User ID", min_value=1000, step=1)
    user_name = st.text_input("User Name")
    user_email = st.text_input("User Email")

    if st.button("Add User"):
        user_service.add_user(user_id, user_name, user_email)
        st.success(f"User '{user_name}' added!")

    # Retrieve user details
    fetch_user_id = st.number_input("Get User by ID", min_value=1000, step=1)
    if st.button("Get User"):
        user = user_service.get_users(fetch_user_id)
        if user:
            st.write(f"**Name:** {user.name}")
            st.write(f"**Email:** {user.email}")
        else:
            st.warning("User not found!")
