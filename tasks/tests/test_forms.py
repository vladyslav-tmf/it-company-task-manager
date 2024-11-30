from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.forms import (
    CheckboxSelectMultiple,
    ChoiceField,
    DateField,
    DateInput,
    ModelMultipleChoiceField,
)
from django.test import TestCase
from django.views.generic.dates import timezone_today

from tasks.forms import (
    PositionSearchForm,
    TaskForm,
    TaskSearchForm,
    TaskTypeForm,
    TaskTypeSearchForm,
)
from tasks.models import Position, Task, TaskType


class TaskFormTests(TestCase):
    def setUp(self) -> None:
        self.task_type = TaskType.objects.create(name="Testing")
        self.position = Position.objects.create(name="Tester")
        self.user1 = get_user_model().objects.create_user(
            username="test_user1",
            password="test_password",
            first_name="John",
            last_name="Doe",
            email="johndoe@gmail.com",
            position=self.position,
        )
        self.user2 = get_user_model().objects.create_user(
            username="test_user2",
            password="test_password",
            first_name="Alice",
            last_name="Black",
            email="aliceblack@gmail.com",
            position=self.position,
        )
        self.valid_data = {
            "name": "New task",
            "task_type": self.task_type.id,
            "is_completed": False,
            "description": "Test description",
            "deadline": timezone_today(),
            "priority": Task.Priority.HIGH,
            "assignees": [self.user1.id, self.user2.id],
        }
        self.assignees_field = TaskForm().fields["assignees"]
        self.deadline_field = TaskForm().fields["deadline"]
        self.priority_field = TaskForm().fields["priority"]

    def test_task_form_assignees_field(self) -> None:
        self.assertIsInstance(self.assignees_field, ModelMultipleChoiceField)
        self.assertIsInstance(self.assignees_field.widget, CheckboxSelectMultiple)
        self.assertIsInstance(self.assignees_field.queryset, QuerySet[get_user_model()])

    def test_task_form_deadline_field(self) -> None:
        self.assertIsInstance(self.deadline_field, DateField)
        self.assertIsInstance(self.deadline_field.widget, DateInput)
        self.assertEqual(self.deadline_field.label, "Deadline")

    def test_task_form_priority_field(self) -> None:
        self.assertIsInstance(self.priority_field, ChoiceField)
        self.assertEqual(self.priority_field.label, "Priority")
        self.assertEqual(self.priority_field.choices, list(Task.Priority.choices))
        self.assertEqual(self.priority_field.initial, Task.Priority.STANDARD)

    def test_task_form_invalid_date(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["deadline"] = "2024-11-19"
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("__all__", form.errors)
        self.assertIn("The deadline cannot be in the past.", form.errors["__all__"])

    def test_task_form_assignees_validation(self) -> None:
        invalid_data = self.valid_data.copy()
        invalid_data["assignees"] = [999, 1000]
        form = TaskForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("assignees", form.errors)

    def test_task_form_meta_model(self) -> None:
        self.assertEqual(TaskForm.Meta.model, Task)

    def test_task_form_meta_fields(self) -> None:
        expected_fields = [
            "name",
            "task_type",
            "is_completed",
            "description",
            "deadline",
            "priority",
            "assignees",
        ]
        self.assertEqual(TaskForm.Meta.fields, expected_fields)


class TaskTypeFormTests(TestCase):
    def test_task_type_form_meta_model(self) -> None:
        self.assertEqual(TaskTypeForm.Meta.model, TaskType)

    def test_task_type_form_meta_fields(self) -> None:
        self.assertEqual(TaskTypeForm.Meta.fields, ["name"])


class TaskSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.name_field = TaskSearchForm().fields["name"]

    def test_task_search_form_name_field_char_field(self) -> None:
        self.assertIsInstance(self.name_field, forms.CharField)

    def test_task_search_form_name_field_max_length(self) -> None:
        self.assertEqual(self.name_field.max_length, 255)

    def test_task_search_form_name_field_label(self) -> None:
        self.assertEqual(self.name_field.label, "")

    def test_task_search_form_name_field_required(self) -> None:
        self.assertFalse(self.name_field.required)

    def test_task_search_form_name_field_widget(self) -> None:
        self.assertEqual(
            self.name_field.widget.attrs["placeholder"], "Search by task name"
        )

    def test_task_search_form_name_field_exists(self) -> None:
        self.assertIn("name", TaskSearchForm().fields)


class TaskTypeSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.name_field = TaskTypeSearchForm().fields["name"]

    def test_task_type_search_form_name_field_exists(self) -> None:
        self.assertIn("name", TaskTypeSearchForm().fields)

    def test_task_type_search_form_name_field_char_field(self) -> None:
        self.assertIsInstance(self.name_field, forms.CharField)

    def test_task_type_search_form_name_field_max_length(self) -> None:
        self.assertEqual(self.name_field.max_length, 255)

    def test_task_type_search_form_name_field_label(self) -> None:
        self.assertEqual(self.name_field.label, "")

    def test_task_type_search_form_name_field_required(self) -> None:
        self.assertFalse(self.name_field.required)

    def test_task_type_search_form_name_field_widget(self) -> None:
        self.assertEqual(
            self.name_field.widget.attrs["placeholder"], "Search by task type name"
        )


class PositionSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.name_field = PositionSearchForm().fields["name"]

    def test_position_search_form_name_field_exists(self) -> None:
        self.assertIn("name", PositionSearchForm().fields)

    def test_position_search_form_name_field_char_field(self) -> None:
        self.assertIsInstance(self.name_field, forms.CharField)

    def test_position_search_form_name_field_max_length(self) -> None:
        self.assertEqual(self.name_field.max_length, 255)

    def test_position_search_form_name_field_label(self) -> None:
        self.assertEqual(self.name_field.label, "")

    def test_position_search_form_name_field_required(self) -> None:
        self.assertFalse(self.name_field.required)

    def test_position_search_form_name_field_widget(self) -> None:
        self.assertEqual(
            self.name_field.widget.attrs["placeholder"], "Search by position name"
        )
