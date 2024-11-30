from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth import get_user_model
from django.views.generic.dates import timezone_today

from tasks.forms import TaskSearchForm
from tasks.models import Task, Position, TaskType

User = get_user_model()


class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", is_active=True
        )
        self.client.login(username="testuser", password="testpassword")
        self.position = Position.objects.create(name="Manager")
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test Task",
            is_completed=False,
            deadline=timezone_today(),
            task_type=self.task_type,
        )
        self.task.assignees.add(self.user)

    def test_index_view_status_code(self):
        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_context_data(self):
        response = self.client.get(reverse("tasks:index"))

        self.assertEqual(response.context["total_tasks"], 1)
        self.assertEqual(response.context["user_tasks"], 1)
        self.assertEqual(response.context["total_workers"], 1)
        self.assertEqual(response.context["total_positions"], 1)
        self.assertEqual(response.context["total_task_types"], 1)
        self.assertEqual(response.context["total_visits"], 1)

    def test_index_view_session_updates(self):
        self.client.get(reverse("tasks:index"))
        self.client.get(reverse("tasks:index"))

        response = self.client.get(reverse("tasks:index"))
        self.assertEqual(response.context["total_visits"], 3)


class TaskListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", is_active=True
        )
        self.client.login(username="testuser", password="testpassword")
        self.task_type = TaskType.objects.create(name="Development")
        Task.objects.bulk_create(
            [
                Task(
                    name=f"Task {i}",
                    task_type=self.task_type,
                    deadline=timezone_today(),
                )
                for i in range(7)
            ]
        )

    def test_task_list_view_status_code(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertEqual(response.status_code, 200)

    def test_task_list_view_pagination(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["tasks"]), 5)

    def test_task_list_search_form_in_context(self):
        response = self.client.get(reverse("tasks:task-list"))
        self.assertIsInstance(response.context["search_form"], TaskSearchForm)


class TaskDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", is_active=True
        )
        self.client.login(username="testuser", password="testpassword")
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test Task", task_type=self.task_type, deadline=timezone_today()
        )

    def test_task_detail_view_status_code(self):
        response = self.client.get(reverse("tasks:task-detail", args=[self.task.pk]))
        self.assertEqual(response.status_code, 200)

    def test_task_detail_view_object(self):
        response = self.client.get(reverse("tasks:task-detail", args=[self.task.pk]))
        self.assertEqual(response.context["task"].name, "Test Task")


class TaskDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", password="testpassword", is_active=True
        )
        self.client.login(username="testuser", password="testpassword")
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Task to Delete", task_type=self.task_type, deadline=timezone_today()
        )

    def test_task_delete_view(self):
        response = self.client.post(reverse("tasks:task-delete", args=[self.task.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(pk=self.task.pk).exists())
