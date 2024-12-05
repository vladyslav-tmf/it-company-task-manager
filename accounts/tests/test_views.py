from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic.dates import timezone_today

from accounts.forms import WorkerRegisterForm
from accounts.services.token_service import account_activation_token
from tasks.models import Position, Task, TaskType

User = get_user_model()


class WorkerRegisterViewTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(name="Developer")

        self.base_form_data = {
            "username": "newuser",
            "password1": "strongpassword",
            "password2": "strongpassword",
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "position": self.position.pk,
        }

    def test_worker_register_view_get(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

    def test_display_registration_form(self):
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")
        self.assertIsInstance(response.context["form"], WorkerRegisterForm)

    def test_successful_worker_registration(self):
        response = self.client.post(reverse("accounts:register"), data=self.base_form_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:login"))

        new_user = User.objects.get(username="newuser")
        self.assertFalse(new_user.is_active)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(
            "Please confirm your activation link in your email.",
            [message.message for message in messages],
        )

    def test_registration_with_mismatched_passwords(self):
        form_data = self.base_form_data.copy()
        form_data["password2"] = "differentpassword"

        response = self.client.post(reverse("accounts:register"), data=form_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertTrue(form.is_bound)
        self.assertFormError(
            form,
            "password2",
            "The two password fields didn’t match.",
        )

    def test_registration_with_existing_email(self):
        User.objects.create_user(
            username="anotheruser",
            password="password",
            email="existing@example.com",
        )

        form_data = self.base_form_data.copy()
        form_data["email"] = "existing@example.com"

        response = self.client.post(reverse("accounts:register"), data=form_data)

        self.assertEqual(response.status_code, 200)

        form = response.context["form"]

        self.assertTrue(form.is_bound)
        self.assertFormError(
            form,
            "email",
            "Worker with this Email already exists.",
        )


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
        self.assertEqual(
            messages[0].message, "Activation link is invalid or has already been used."
        )


class WorkerLoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_active=True,
        )

    def test_login_view_get(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpassword"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("tasks:index"))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Please enter a correct username and password. "
            "Note that both fields may be case-sensitive.",
        )


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

    def test_worker_list_view_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse("accounts:worker-list"))
        self.assertNotEqual(response.status_code, 200)
        self.assertRedirects(response, "/accounts/login/?next=/accounts/workers/")


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

    def test_worker_detail_view_invalid_user(self):
        invalid_user_id = self.user.pk + 1
        response = self.client.get(reverse("accounts:worker-detail", args=[invalid_user_id]))
        self.assertEqual(response.status_code, 404)

    def test_worker_detail_view_no_tasks(self):
        self.user.tasks.clear()
        response = self.client.get(reverse("accounts:worker-detail", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["completed_tasks"]), 0)
        self.assertEqual(len(response.context["pending_tasks"]), 0)


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

    def test_toggle_assign_to_task_view_without_login(self):
        self.client.logout()
        response = self.client.post(
            reverse("accounts:toggle-assign", args=[self.task.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def test_toggle_assign_to_task_with_invalid_task_id(self):
        response = self.client.post(
            reverse("accounts:toggle-assign", args=[9999])
        )
        self.assertEqual(response.status_code, 404)


class WorkerUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.position = Position.objects.create(name="Developer")
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_active=True,
            position=self.position
        )
        self.client.login(username="testuser", password="testpassword")

    def test_update_view_get(self):
        response = self.client.get(reverse("accounts:worker-update", args=[self.user.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/worker_form.html")

    def test_update_view_post(self):
        response = self.client.post(
            reverse("accounts:worker-update", args=[self.user.pk]), {
                "first_name": "Updated",
                "last_name": "User",
                "position": self.position.pk,
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:worker-list"))

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.last_name, "User")


class WorkerDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com",
            is_active=True,
        )
        self.client.login(username="testuser", password="testpassword")

    def test_delete_view(self):
        response = self.client.post(reverse("accounts:worker-delete", args=[self.user.pk]))
        self.assertEqual(response.status_code, 302)
        response = self.client.get(reverse("accounts:worker-list"))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_delete_view_without_authentication(self):
        self.client.logout()

        response = self.client.post(reverse("accounts:worker-delete", args=[self.user.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response.url)

    def test_delete_non_existing_user(self):
        non_existent_user_id = self.user.pk + 999

        response = self.client.post(reverse("accounts:worker-delete", args=[non_existent_user_id]))

        self.assertEqual(response.status_code, 404)
