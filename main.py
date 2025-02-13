from Services.task_service import Task_Service
from Services.user_service import User_Service


def main():
    task_service = Task_Service()
    user_service = User_Service()

    # Add user
    user_service.add_user(1000, "John Doe", "john@example.com")

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

    # Complete a task
    completed_task = task_service.complete_task()
    if completed_task:
        print(f"Completed Task: {completed_task.id}, {completed_task.title}")

    # Fetch and print task history
    print("\nTask History:")
    for task in task_service.get_task_history():
        print(task.title)


if __name__ == "__main__":
    main()
