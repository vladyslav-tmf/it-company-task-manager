from django.contrib import admin

from tasks.models import Position, Task, TaskType


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ["name"]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "task_type", "deadline", "priority", "is_completed"]
    list_editable = ["is_completed"]
    search_fields = ["name"]
    list_filter = ["is_completed", "priority", "task_type", "deadline"]
