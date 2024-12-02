from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from tasks.models import Position


class Worker(AbstractUser):
    email = models.EmailField(unique=True)
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="workers",
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["username"]

    def get_absolute_url(self) -> str:
        return reverse("accounts:worker-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
