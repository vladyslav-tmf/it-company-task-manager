from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.views.generic.dates import timezone_today

from tasks.models import Position, Task, TaskType


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Testing")
        self.position = Position.objects.create(name="Tester")
        self.task = Task.objects.create(
            name="Test",
            description="Test case",
            deadline=timezone_today(),
            is_completed=False,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )

    def test_task_type_str_method(self) -> None:
        self.assertEqual(str(self.task_type), "Testing")

    def test_position_str_method(self) -> None:
        self.assertEqual(str(self.position), "Tester")

    def test_task_str_method(self) -> None:
        self.assertEqual(
            str(self.task), f"Test (Deadline: {self.task.deadline}, " f"Priority: High)"
        )

    def test_task_get_absolute_url(self) -> None:
        self.assertEqual(self.task.get_absolute_url(), f"/tasks/{self.task.pk}/")

    def test_task_clean_with_valid_deadline(self) -> None:
        try:
            self.task.clean()
        except ValidationError:
            self.fail("ValidationError was raised unexpectedly!")

    def test_task_clean_with_invalid_deadline(self) -> None:
        self.task.deadline = timezone_today() - timedelta(days=1)
        with self.assertRaises(ValidationError) as context:
            self.task.clean()
        self.assertEqual(
            str(context.exception.messages[0]), "The deadline cannot be in the past."
        )
