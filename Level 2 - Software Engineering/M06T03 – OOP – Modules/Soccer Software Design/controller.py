from __future__ import annotations

from models import Task, TrainingPlan
from storage import FileStorage


class TaskManagerController:
    def __init__(self, storage: FileStorage) -> None:
        self.storage = storage
        self.users = self.storage.load_or_initialize()
        self.current_user = self.users[0]
        self.current_plan = self.current_user.plans[0] if self.current_user.plans else None

    def get_active_plan(self) -> TrainingPlan:
        if self.current_plan is None:
            raise ValueError("No active training plan available.")
        return self.current_plan

    def list_tasks(self) -> list[Task]:
        return list(self.get_active_plan().tasks)

    def add_task(
        self,
        name: str,
        description: str,
        link: str,
        due_date: str,
    ) -> Task:
        plan = self.get_active_plan()
        task_id = self._next_task_id()
        task = Task(
            task_id=task_id,
            name=name,
            description=description,
            link=link,
            due_date=self._parse_due_date(due_date),
            completion=False,
        )
        plan.add_task(task)
        self._save()
        return task

    def edit_task(
        self,
        task_id: int,
        name: str | None = None,
        description: str | None = None,
        link: str | None = None,
        due_date: str | None = None,
        completion: bool | None = None,
    ) -> Task:
        task = self._find_task(task_id)
        if name is not None and name.strip():
            task.name = name.strip()
        if description is not None:
            task.description = description.strip()
        if link is not None:
            task.link = link.strip()
        if due_date is not None and due_date.strip():
            task.due_date = self._parse_due_date(due_date)
        if completion is not None:
            task.completion = completion
        self._save()
        return task

    def delete_task(self, task_id: int) -> bool:
        plan = self.get_active_plan()
        removed = plan.remove_task(task_id)
        if removed:
            self._save()
        return removed

    def mark_task_complete(self, task_id: int) -> Task:
        task = self._find_task(task_id)
        task.complete()
        self._save()
        return task

    def get_progress(self) -> float:
        return self.get_active_plan().get_progress()

    def _find_task(self, task_id: int) -> Task:
        task = self.get_active_plan().get_task(task_id)
        if task is None:
            raise ValueError(f"Task with ID {task_id} not found.")
        return task

    def _next_task_id(self) -> int:
        highest_id = 0
        for plan in self.current_user.plans:
            for task in plan.tasks:
                highest_id = max(highest_id, task.task_id)
        return highest_id + 1

    def _parse_due_date(self, due_date: str):
        from models import parse_date

        return parse_date(due_date)

    def _save(self) -> None:
        self.storage.save(self.users)
