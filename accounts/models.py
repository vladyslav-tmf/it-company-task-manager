from django.contrib.auth.models import AbstractUser
from django.db import models


class Worker(AbstractUser):
    email = models.EmailField(unique=True)
    position = models.ForeignKey("Position", on_delete=models.CASCADE, related_name="workers", null=True, blank=True)

    class Meta:
        ordering = ["username"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
