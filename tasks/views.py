from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from tasks.models import Task


@login_required
def index(request: HttpRequest) -> HttpResponse:
    user = request.user
    tasks = Task.objects.filter(assignees=user).order_by("-deadline")
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = total_tasks - completed_tasks
    today = timezone.now().date()
    tasks_today = tasks.filter(deadline=today)
    one_week_from_today = today + timedelta(days=7)
    upcoming_tasks = tasks.filter(
        deadline__gt=today, deadline__lte=one_week_from_today
    ).order_by("deadline")

    context = {
        "user": user,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "tasks_today": tasks_today,
        "upcoming_tasks": upcoming_tasks
    }

    return render(request, "index.html", context=context)
