from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.dates import timezone_today

from accounts.services.token_service import account_activation_token
from tasks.models import Position, Task, TaskType

User = get_user_model()


class WorkerRegisterViewTest(TestCase):
    def test_worker_register_view_get(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")


class WorkerActivateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="inactiveuser",
            password="testpassword",
            email="inactiveuser@example.com",
            is_active=False,
        )
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = account_activation_token.make_token(self.user)

    def test_worker_activate_view_get_valid_link(self):
        response = self.client.get(
            reverse("accounts:activate", args=[self.uid, self.token])
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(
            messages[0].message,
            "Thank you for your email confirmation. Now you can sign in to your account.",
        )

    def test_worker_activate_view_get_invalid_link(self):
        invalid_token = "invalid-token"
        response = self.client.get(
            reverse("accounts:activate", args=[self.uid, invalid_token])
        )
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        self.assertEqual(messages[0].message, "Activation link is invalid or has already been used.")


class WorkerListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_active=True,
        )
        self.client.login(username="testuser", password="testpassword")

    def test_worker_list_view_get(self):
        response = self.client.get(reverse("accounts:worker-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Worker List")


class WorkerDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            position=self.position,
        )
        self.client.login(username="testuser", password="testpassword")
        self.task_type = TaskType.objects.create(name="Development")
        self.completed_task = Task.objects.create(
            name="Completed Task",
            description="Test case",
            deadline=timezone_today(),
            task_type=self.task_type,
            is_completed=True,
            priority=Task.Priority.STANDARD,
        )
        self.pending_task = Task.objects.create(
            name="Pending Task",
            description="Test case",
            deadline=timezone_today(),
            task_type=self.task_type,
            is_completed=False,
            priority=Task.Priority.STANDARD,
        )
        self.user.tasks.add(self.completed_task, self.pending_task)

    def test_worker_detail_view_context(self):
        response = self.client.get(
            reverse("accounts:worker-detail", args=[self.user.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("completed_tasks", response.context)
        self.assertIn("pending_tasks", response.context)
        self.assertIn(self.completed_task, response.context["completed_tasks"])
        self.assertIn(self.pending_task, response.context["pending_tasks"])


class ToggleAssignToTaskViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="togglertest",
            password="testpassword",
            email="togglertest@example.com",
            position=self.position,
        )
        self.task_type = TaskType.objects.create(name="Development")
        self.task = Task.objects.create(
            name="Test",
            description="Test case",
            deadline=timezone_today(),
            is_completed=False,
            priority=Task.Priority.HIGH,
            task_type=self.task_type,
        )
        self.client.login(username="togglertest", password="testpassword")

    def test_toggle_assign_to_task_view(self):
        response = self.client.post(
            reverse("accounts:toggle-assign", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.task, self.user.tasks.all())

        response = self.client.post(
            reverse("accounts:toggle-assign", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.task, self.user.tasks.all())
