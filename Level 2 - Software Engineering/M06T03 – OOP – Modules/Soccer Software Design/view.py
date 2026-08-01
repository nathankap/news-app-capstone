from __future__ import annotations

from datetime import date

from models import Task


def display_header(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def display_menu() -> None:
    display_header("Soccer Training Task Manager")
    print("1. View tasks")
    print("2. Add a task")
    print("3. Edit a task")
    print("4. Delete a task")
    print("5. Mark task complete")
    print("6. Show plan progress")
    print("7. Exit")


def prompt_menu_choice() -> str:
    return input("Enter a menu choice (1-7): ").strip()


def prompt_input(prompt_text: str, default: str | None = None) -> str:
    if default is not None:
        raw = input(f"{prompt_text} [{default}]: ").strip()
        return raw or default
    return input(f"{prompt_text}: ").strip()


def prompt_date(prompt_text: str, default: str | None = None) -> str:
    while True:
        value = prompt_input(prompt_text, default)
        try:
            date.fromisoformat(value)
            return value
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def display_tasks(tasks: list[Task], plan_name: str, progress: float) -> None:
    display_header(f"Training Plan: {plan_name}")
    print(f"Current progress: {progress}%")
    if not tasks:
        print("No tasks are available in the current plan.")
        return

    for index, task in enumerate(tasks, start=1):
        print("-" * 60)
        print(f"Task #{index}")
        print(f"ID: {task.task_id}")
        print(f"Name: {task.name}")
        print(f"Status: {task.status}")
        print(f"Due Date: {task.due_date}")
        print(f"Link: {task.link}")
        print(f"Description: {task.description}")


def display_message(message: str) -> None:
    print(f"\n{message}\n")
