from django.contrib.admin import site
from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.admin import WorkerAdmin


class WorkerAdminTests(TestCase):
    def setUp(self) -> None:
        self.worker_admin = WorkerAdmin(get_user_model(), site)

    def test_worker_admin_list_display(self) -> None:
        self.assertIn("position", self.worker_admin.list_display)

    def test_worker_admin_fieldsets(self) -> None:
        self.assertIn(
            ("Additional info", {"fields": ("position",)}), self.worker_admin.fieldsets
        )

    def test_worker_admin_add_fieldsets(self) -> None:
        self.assertIn(
            ["Personal info", {"fields": ["email", "first_name", "last_name"]}],
            self.worker_admin.add_fieldsets,
        )

    def test_worker_admin_search_fields(self) -> None:
        for field in ["username", "first_name", "last_name", "position__name"]:
            with self.subTest(field=field):
                self.assertIn(field, self.worker_admin.search_fields)

    def test_worker_admin_list_filter(self) -> None:
        self.assertIn("position", self.worker_admin.list_filter)

    def test_worker_admin_list_select_related(self):
        self.assertIn("position", self.worker_admin.list_select_related)
