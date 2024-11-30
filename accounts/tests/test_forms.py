from django import forms
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.test import TestCase

from accounts.forms import WorkerRegisterForm, WorkerSearchForm, WorkerUpdateForm


class WorkerRegisterFormTests(TestCase):
    def setUp(self) -> None:
        self.position_field = WorkerRegisterForm().fields["position"]

    def test_worker_register_form_position_field(self) -> None:
        self.assertIn("position", WorkerRegisterForm().fields)

    def test_worker_register_form_position_field_queryset(self) -> None:
        self.assertIsInstance(self.position_field.queryset, QuerySet[get_user_model()])

    def test_worker_register_form_position_field_text(self) -> None:
        self.assertEqual(self.position_field.help_text, "Please choose a position")

    def test_worker_register_form_position_field_required(self) -> None:
        self.assertTrue(self.position_field.required)

    def test_worker_register_form_meta_model(self) -> None:
        self.assertEqual(WorkerRegisterForm.Meta.model, get_user_model())

    def test_worker_register_form_meta_fields(self) -> None:
        expected_fields = ("username", "email", "first_name", "last_name", "position")
        self.assertEqual(WorkerRegisterForm.Meta.fields, expected_fields)


class WorkerUpdateFormTests(TestCase):
    def test_worker_update_form_meta_model(self) -> None:
        self.assertEqual(WorkerUpdateForm.Meta.model, get_user_model())

    def test_worker_update_form_meta_fields(self) -> None:
        expected_fields = ["first_name", "last_name", "position"]
        self.assertEqual(WorkerUpdateForm.Meta.fields, expected_fields)


class WorkerSearchFormTests(TestCase):
    def setUp(self) -> None:
        self.username_field = WorkerSearchForm().fields["username"]

    def test_worker_search_form_username_field_exists(self) -> None:
        self.assertIn("username", WorkerSearchForm().fields)

    def test_worker_search_form_username_field_widget(self) -> None:
        self.assertEqual(
            self.username_field.widget.attrs["placeholder"], "Search by Username"
        )

    def test_worker_search_form_username_field_label(self) -> None:
        self.assertEqual(self.username_field.label, "")

    def test_worker_search_form_username_field_required(self) -> None:
        self.assertFalse(self.username_field.required)

    def test_worker_search_form_username_field_char_field(self) -> None:
        self.assertIsInstance(self.username_field, forms.CharField)

    def test_worker_search_form_username_field_max_length(self) -> None:
        self.assertEqual(self.username_field.max_length, 255)
