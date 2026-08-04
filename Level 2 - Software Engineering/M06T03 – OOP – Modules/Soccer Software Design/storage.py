from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

from models import TrainingPlan, User


class FileStorage:
    """JSON-based storage implementation for users, plans, and tasks."""

    def __init__(self, filename: str = "task_data.json") -> None:
        self.path = Path(filename)

    def load(self) -> list[User]:
        """Load user data from storage or return an empty list."""
        if not self.path.exists():
            return []

        with self.path.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        return [User.from_dict(item) for item in payload.get("users", [])]

    def save(self, users: list[User]) -> None:
        """Write the provided users into the storage file."""
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"users": [user.to_dict() for user in users]}
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(payload, file, indent=2)

    def load_or_initialize(self) -> list[User]:
        """Load saved users or initialize with a default user and plan."""
        users = self.load()
        if users:
            return users

        default_plan = TrainingPlan(
            plan_id=1,
            name="Soccer Training Plan",
            start_date=date.today(),  # noqa: DTZ011
            end_date=date.today() + timedelta(days=14),  # noqa: DTZ011
        )
        default_user = User(
            user_id=1,
            name="Soccer Training Manager",
            email="coach@example.com",
            plans=[default_plan],
        )
        self.save([default_user])
        return [default_user]
