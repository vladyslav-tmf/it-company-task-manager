from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django.views.generic import TemplateView

from tasks.forms import (
    PositionForm,
    PositionSearchForm,
    TaskForm,
    TaskSearchForm,
    TaskTypeForm,
    TaskTypeSearchForm,
)
from tasks.models import Position, Task, TaskType

User = get_user_model()

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "tasks/index.html"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        user = self.request.user
        total_tasks = Task.objects.count()
        user_tasks = Task.objects.filter(assignees=user, is_completed=False).count()

        total_workers = User.objects.count()
        total_positions = Position.objects.count()
        total_task_types = TaskType.objects.count()

        total_visits = self.request.session.get("total_visits", 1)
        self.request.session["total_visits"] = total_visits + 1

        context.update(
            {
                "total_tasks": total_tasks,
                "total_workers": total_workers,
                "total_positions": total_positions,
                "total_task_types": total_task_types,
                "total_visits": total_visits,
                "user_tasks": user_tasks,
            }
        )

        return context


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5
    context_object_name = "tasks"
    queryset = Task.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskSearchForm()

        return context

    def get_queryset(self) -> QuerySet[Task]:
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskFormMixin:
    def _customize_form(self, form: TaskForm) -> None:
        self._customize_field(form, "name", _("Name"))
        self._customize_field(form, "task_type", _("Task type"))
        self._customize_field(form, "is_completed", _("Is completed"))
        self._customize_field(form, "description", _("Description"))
        self._customize_field(form, "deadline", _("Deadline"))
        self._customize_field(form, "priority", _("Priority"))
        self._customize_field(form, "assignees", _("Assignees"))

    @staticmethod
    def _customize_field(form: TaskForm, field_name: str, label: str) -> None:
        field = form.fields[field_name]
        field.label = label


class TaskCreateView(LoginRequiredMixin, TaskFormMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def get_form(self, form_class=TaskForm) -> TaskForm:
        form = super().get_form(form_class)
        self._customize_form(form)
        return form


class TaskUpdateView(LoginRequiredMixin, TaskFormMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def get_form(self, form_class=TaskForm) -> TaskForm:
        form = super().get_form(form_class)
        self._customize_form(form)
        return form


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("tasks:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    paginate_by = 6
    context_object_name = "task_types"
    template_name = "tasks/task_type_list.html"
    queryset = TaskType.objects.order_by("name")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = TaskTypeSearchForm()

        return context

    def get_queryset(self) -> QuerySet[TaskType]:
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    form_class = TaskTypeForm
    template_name = "tasks/task_type_form.html"
    success_url = reverse_lazy("tasks:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "tasks/task_type_confirm_delete.html"
    success_url = reverse_lazy("tasks:task-type-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    paginate_by = 6
    context_object_name = "positions"
    queryset = Position.objects.order_by("name")

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["search_form"] = PositionSearchForm()

        return context

    def get_queryset(self) -> QuerySet[Position]:
        name = self.request.GET.get("name")

        if name:
            return self.queryset.filter(name__icontains=name)

        return self.queryset


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("tasks:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionForm
    success_url = reverse_lazy("tasks:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("tasks:position-list")
