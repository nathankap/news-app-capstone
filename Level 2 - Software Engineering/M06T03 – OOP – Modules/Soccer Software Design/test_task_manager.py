from __future__ import annotations

from datetime import date, timedelta

from controller import TaskManagerController
from models import Task, TrainingPlan, User


class FakeStorage:
    def __init__(self, users: list[User]) -> None:
        self._users = users
        self.saved = None

    def load_or_initialize(self) -> list[User]:
        return self._users

    def save(self, users: list[User]) -> None:
        self.saved = users


def test_task_is_overdue_and_status_updates() -> None:
    yesterday = date.today() - timedelta(days=1)  # noqa: DTZ011
    task = Task(
        task_id=1,
        name="Practice",
        description="",
        link="",
        due_date=yesterday,
        completion=False,
    )

    assert task.is_overdue() is True
    assert task.status == "Overdue"

    task.complete()
    assert task.completion is True
    assert task.status == "Completed"


def test_training_plan_progress_calculation() -> None:
    plan = TrainingPlan(
        plan_id=1,
        name="Training Plan",
        start_date=date.today(),  # noqa: DTZ011
        end_date=date.today() + timedelta(days=7),  # noqa: DTZ011
    )
    plan.add_task(
        Task(
            task_id=1,
            name="Warm-up",
            description="",
            link="",
            due_date=date.today(),  # noqa: DTZ011
            completion=False,
        )
    )
    plan.add_task(
        Task(
            task_id=2,
            name="Fitness",
            description="",
            link="",
            due_date=date.today(),  # noqa: DTZ011
            completion=True,
        )
    )

    assert plan.get_progress() == 50.0


def test_controller_add_edit_delete_task() -> None:
    plan = TrainingPlan(
        plan_id=1,
        name="Training Plan",
        start_date=date.today(),  # noqa: DTZ011
        end_date=date.today() + timedelta(days=7),  # noqa: DTZ011
    )
    user = User(user_id=1, name="Coach", email="coach@example.com", plans=[plan])
    controller = TaskManagerController(FakeStorage([user]))

    task = controller.add_task(
        name="Dribbling",
        description="Dribble through cones",
        link="http://example.com/dribbling",
        due_date=date.today().isoformat(),  # noqa: DTZ011
    )

    assert task.task_id == 1
    assert plan.get_task(1) is not None
    assert plan.get_task(1).name == "Dribbling"

    controller.edit_task(
        task_id=1,
        name="Dribbling Session",
        description="Use both feet",
        link="http://example.com/dribbling-session",
        due_date=(
            date.today() + timedelta(days=1)
        ).isoformat(),  # noqa: DTZ011
        completion=True,
    )

    edited_task = plan.get_task(1)
    assert edited_task is not None
    assert edited_task.name == "Dribbling Session"
    assert edited_task.description == "Use both feet"
    assert edited_task.link == "http://example.com/dribbling-session"
    assert edited_task.completion is True

    result = controller.delete_task(1)
    assert result is True
    assert plan.get_task(1) is None


def test_controller_mark_task_complete_updates_progress() -> None:
    plan = TrainingPlan(
        plan_id=1,
        name="Training Plan",
        start_date=date.today(),  # noqa: DTZ011
        end_date=date.today() + timedelta(days=7),  # noqa: DTZ011
    )
    user = User(user_id=1, name="Coach", email="coach@example.com", plans=[plan])
    controller = TaskManagerController(FakeStorage([user]))

    controller.add_task(
        name="Shooting",
        description="Finish shots",
        link="",
        due_date=date.today().isoformat(),  # noqa: DTZ011
    )
    controller.add_task(
        name="Passing",
        description="Short pass drills",
        link="",
        due_date=date.today().isoformat(),  # noqa: DTZ011
    )

    assert controller.get_progress() == 0.0

    controller.mark_task_complete(1)
    assert controller.get_progress() == 50.0
