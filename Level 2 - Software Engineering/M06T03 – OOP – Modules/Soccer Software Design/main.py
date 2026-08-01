from __future__ import annotations

from controller import TaskManagerController
from storage import FileStorage
from view import (
    display_menu,
    display_message,
    display_tasks,
    prompt_date,
    prompt_input,
    prompt_menu_choice,
)


def main() -> None:
    storage = FileStorage("task_data.json")
    controller = TaskManagerController(storage)

    while True:
        display_menu()
        choice = prompt_menu_choice()

        try:
            if choice == "1":
                tasks = controller.list_tasks()
                display_tasks(tasks, controller.get_active_plan().name, controller.get_progress())

            elif choice == "2":
                name = prompt_input("Task name")
                description = prompt_input("Task description")
                link = prompt_input("Task link")
                due_date = prompt_date("Task due date (YYYY-MM-DD)")
                controller.add_task(name=name, description=description, link=link, due_date=due_date)
                display_message("Task added successfully.")

            elif choice == "3":
                tasks = controller.list_tasks()
                display_tasks(tasks, controller.get_active_plan().name, controller.get_progress())
                task_id = int(prompt_input("Task ID to edit"))
                task = controller._find_task(task_id)
                name = prompt_input("New task name", task.name)
                description = prompt_input("New description", task.description)
                link = prompt_input("New link", task.link)
                due_date = prompt_date("New due date (YYYY-MM-DD)", task.due_date.isoformat())
                completed = prompt_input("Is the task complete? (yes/no)", "yes" if task.completion else "no").lower() in ["yes", "y"]
                controller.edit_task(task_id=task_id, name=name, description=description, link=link, due_date=due_date, completion=completed)
                display_message("Task updated successfully.")

            elif choice == "4":
                task_id = int(prompt_input("Task ID to delete"))
                if controller.delete_task(task_id):
                    display_message("Task deleted successfully.")
                else:
                    display_message("Task not found.")

            elif choice == "5":
                task_id = int(prompt_input("Task ID to mark complete"))
                controller.mark_task_complete(task_id)
                display_message("Task marked complete.")

            elif choice == "6":
                tasks = controller.list_tasks()
                completed_count = sum(1 for task in tasks if task.completion)
                pending_count = len(tasks) - completed_count
                display_message(
                    f"Training plan progress: {controller.get_progress()}%\n"
                    f"Completed tasks: {completed_count}\n"
                    f"Pending tasks: {pending_count}\n"
                    f"Total tasks: {len(tasks)}"
                )

            elif choice == "7":
                display_message("Exiting the task manager. Goodbye!")
                break

            else:
                display_message("Please choose a valid option between 1 and 7.")

        except ValueError as error:
            display_message(f"Error: {error}")


if __name__ == "__main__":
    main()
