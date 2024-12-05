from django.contrib.admin.sites import site
from django.test import TestCase

from tasks.admin import PositionAdmin, TaskAdmin, TaskTypeAdmin
from tasks.models import Position, Task, TaskType


class PositionAdminTest(TestCase):
    def test_position_admin_search_fields(self) -> None:
        self.position_admin = PositionAdmin(Position, site)
        self.assertIn("name", self.position_admin.search_fields)


class TaskTypeAdminTest(TestCase):
    def test_task_type_admin_search_fields(self) -> None:
        self.task_type_admin = TaskTypeAdmin(TaskType, site)
        self.assertIn("name", self.task_type_admin.search_fields)


class TaskAdminTests(TestCase):
    def setUp(self) -> None:
        self.task_admin = TaskAdmin(Task, site)

    def test_task_admin_list_display(self) -> None:
        for field in ["name", "task_type", "deadline", "priority", "is_completed"]:
            with self.subTest(field=field):
                self.assertIn(field, self.task_admin.list_display)

    def test_task_list_editable(self) -> None:
        self.assertIn("is_completed", self.task_admin.list_editable)

    def test_task_search_fields(self) -> None:
        self.assertIn("name", self.task_admin.search_fields)

    def test_task_admin_list_filter(self) -> None:
        for field in ["is_completed", "priority", "task_type", "deadline"]:
            with self.subTest(field=field):
                self.assertIn(field, self.task_admin.list_filter)
