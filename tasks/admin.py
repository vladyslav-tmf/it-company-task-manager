from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import Position, Task, TaskType, Worker


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info", {
                    "fields": ("email", "first_name", "last_name", "position")
                },
            ),
        )
    )
    search_fields = ("username", "first_name", "last_name", "position__name")
    list_filter = ("position__name",)
    list_select_related = ("position",)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name", "task_type", "deadline", "priority", "is_completed"
    )
    list_editable = ("is_completed",)
    search_fields = ("name",)
    list_filter = ("is_completed", "priority", "task_type", "deadline")
    list_select_related = ("task_type",)
