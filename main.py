from Services.task_service import Task_Service
from Services.user_service import User_Service


def main():
    task_services = Task_Service()
    user_service = User_Service()

    user_service.add_user(1000, "John Doe", "john@example.com")

    task_services.create_task(
        1,
        "Details About Project",
        "Get details of project from the client",
    )
    task_services.create_task(
        2,
        "Research About Project",
        "Research about the project in detail",
    )
    task_services.create_task(
        3,
        "Complete the Project",
        "Complete the Project by friday",
    )
    print(task_services.complete_task())
    history = task_services.get_task_history()
    while not history.is_empty():
        print(history.pop().title)


if __name__ == "__main__":
    main()
