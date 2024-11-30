from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.views.generic.dates import timezone_today


class NameModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class TaskType(NameModel):
    class Meta:
        verbose_name = "task type"
        verbose_name_plural = "task types"


class Position(NameModel):
    pass


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "Low", "Low",
        STANDARD = "Standard", "Standard",
        HIGH = "High", "High"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.STANDARD)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE, related_name="tasks")
    assignees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tasks")

    class Meta:
        ordering = ["deadline", "-priority"]

    def clean(self) -> None:
        if self.deadline < timezone_today():
            raise ValidationError("The deadline cannot be in the past.")

    def get_absolute_url(self) -> str:
        return reverse("tasks:task-detail", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return f"{self.name} (Deadline: {self.deadline}, Priority: {self.get_priority_display()})"
