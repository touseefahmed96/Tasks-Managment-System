from Services.task_service import Task_Service
from Services.user_service import User_Service


def main():
    task_service = Task_Service()
    user_service = User_Service()

    # Add user
    user_service.add_user(1000, "John Doe", "john@example.com")
    # Add users
    user_service.add_user(1001, "Alice", "alice@example.com")
    user_service.add_user(1002, "Bob", "bob@example.com")

    # Create tasks
    task_service.create_task(
        1,
        "Details About Project",
        "Get details from the client",
    )
    task_service.create_task(
        2,
        "Research About Project",
        "Research in depth",
    )
    task_service.create_task(
        3,
        "Complete the Project",
        "Complete the project by Friday",
    )

    # Assign tasks
    task_service.assign_task(1, 1001)  # Assign task 1 to Alice
    task_service.assign_task(2, 1002)  # Assign task 2 to Bob

    # Complete a task
    completed_task = task_service.complete_task()
    if completed_task:
        print(
            f"Completed Task: {completed_task.id}, {completed_task.title}, Assigned to: {completed_task.assigned_user_id}"
        )

    # Fetch and print task history
    print("\nTask History:")
    for task in task_service.get_task_history():
        print(f"{task.title} (Assigned to User ID: {task.assigned_user_id})")


if __name__ == "__main__":
    main()
