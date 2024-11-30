from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

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
                "user_tasks": user_tasks
            }
        )

        return context
