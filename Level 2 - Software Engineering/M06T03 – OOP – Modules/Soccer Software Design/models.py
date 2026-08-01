from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any

DATE_FORMAT = "%Y-%m-%d"


def parse_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(value, DATE_FORMAT).date()  # noqa: DTZ007


@dataclass
class Task:
    task_id: int
    name: str
    description: str
    link: str
    due_date: date
    completion: bool = False

    def complete(self) -> None:
        self.completion = True

    def update_status(self, completed: bool) -> None:
        self.completion = completed

    def is_overdue(self) -> bool:
        return date.today() > self.due_date and not self.completion  # noqa: DTZ011

    @property
    def status(self) -> str:
        if self.completion:
            return "Completed"
        if self.is_overdue():
            return "Overdue"
        return "Pending"

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "due_date": self.due_date.strftime(DATE_FORMAT),
            "completion": self.completion,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Task:
        return cls(
            task_id=int(data["task_id"]),
            name=str(data["name"]),
            description=str(data.get("description", "")),
            link=str(data.get("link", "")),
            due_date=parse_date(data["due_date"]),
            completion=bool(data.get("completion", False)),
        )


@dataclass
class TrainingPlan:
    plan_id: int
    name: str
    start_date: date
    end_date: date
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> bool:
        for index, task in enumerate(self.tasks):
            if task.task_id == task_id:
                del self.tasks[index]
                return True
        return False

    def get_task(self, task_id: int) -> Task | None:
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def get_progress(self) -> float:
        if not self.tasks:
            return 0.0
        completed = sum(1 for task in self.tasks if task.completion)
        return round(completed / len(self.tasks) * 100.0, 1)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "start_date": self.start_date.strftime(DATE_FORMAT),
            "end_date": self.end_date.strftime(DATE_FORMAT),
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TrainingPlan:
        tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return cls(
            plan_id=int(data["plan_id"]),
            name=str(data["name"]),
            start_date=parse_date(data["start_date"]),
            end_date=parse_date(data["end_date"]),
            tasks=tasks,
        )


@dataclass
class User:
    user_id: int
    name: str
    email: str
    plans: list[TrainingPlan] = field(default_factory=list)

    def add_plan(self, plan: TrainingPlan) -> None:
        self.plans.append(plan)

    def get_plan(self, plan_id: int) -> TrainingPlan | None:
        for plan in self.plans:
            if plan.plan_id == plan_id:
                return plan
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "plans": [plan.to_dict() for plan in self.plans],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> User:
        plans = [TrainingPlan.from_dict(plan_data) for plan_data in data.get("plans", [])]
        return cls(
            user_id=int(data["user_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            plans=plans,
        )
