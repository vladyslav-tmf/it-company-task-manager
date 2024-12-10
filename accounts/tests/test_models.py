from django.contrib.auth import get_user_model
from django.test import TestCase

from tasks.models import Position


class ModelsTests(TestCase):
    def setUp(self) -> None:
        self.position = Position.objects.create(name="Tester")
        self.worker = get_user_model().objects.create_user(
            username="test_user",
            password="test_password",
            first_name="John",
            last_name="Doe",
            email="johndoe@gmail.com",
            position=self.position,
        )

    def test_worker_str_method(self) -> None:
        self.assertEqual(str(self.worker), "John Doe")

    def test_worker_get_absolute_url(self) -> None:
        self.assertEqual(self.worker.get_absolute_url(), f"/accounts/{self.worker.pk}/")
