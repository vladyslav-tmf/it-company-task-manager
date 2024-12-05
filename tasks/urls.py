from django.urls import include, path

from tasks import views

app_name = "tasks"

task_patterns = [
    path(
        "",
        views.TaskListView.as_view(),
        name="task-list",
    ),
    path(
        "create/",
        views.TaskCreateView.as_view(),
        name="task-create",
    ),
    path(
        "<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail",
    ),
    path(
        "<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update",
    ),
    path(
        "<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete",
    ),
]

task_type_patterns = [
    path(
        "",
        views.TaskTypeListView.as_view(),
        name="task-type-list",
    ),
    path(
        "create/",
        views.TaskTypeCreateView.as_view(),
        name="task-type-create",
    ),
    path(
        "<int:pk>/update/",
        views.TaskTypeUpdateView.as_view(),
        name="task-type-update",
    ),
    path(
        "<int:pk>/delete/",
        views.TaskTypeDeleteView.as_view(),
        name="task-type-delete",
    ),
]

position_patterns = [
    path(
        "",
        views.PositionListView.as_view(),
        name="position-list",
    ),
    path(
        "create/",
        views.PositionCreateView.as_view(),
        name="position-create",
    ),
    path(
        "<int:pk>/update",
        views.PositionUpdateView.as_view(),
        name="position-update",
    ),
    path(
        "<int:pk>/delete/",
        views.PositionDeleteView.as_view(),
        name="position-delete",
    ),
]

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("tasks/", include(task_patterns)),
    path("task-types/", include(task_type_patterns)),
    path("positions/", include(position_patterns)),
]
