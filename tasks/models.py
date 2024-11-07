from django.contrib.auth.models import AbstractUser
from django.db import models


class NamedModel(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class TaskType(NamedModel):
    class Meta:
        verbose_name = "task type"
        verbose_name_plural = "task types"


class Position(NamedModel):
    pass


class Worker(AbstractUser):
    position = models.ForeignKey(
        to=Position, on_delete=models.CASCADE, related_name="workers"
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Task(models.Model):
    class Priority(models.TextChoices):
        LOW = "Low", "Low priority"
        STANDARD = "Standard", "Standard priority"
        HIGH = "High", "High priority"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=Priority.choices)
    task_type = models.ForeignKey(
        to=TaskType, on_delete=models.CASCADE, related_name="tasks"
    )
    assignees = models.ManyToManyField(to=Worker, related_name="tasks")

    class Meta:
        ordering = ["deadline", "-priority"]

    def __str__(self) -> str:
        return (f"{self.name} (Deadline: {self.deadline}, "
                f"Priority: {self.get_priority_display()})")
