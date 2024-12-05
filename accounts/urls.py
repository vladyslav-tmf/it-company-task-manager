from django.urls import include, path

from accounts import views

app_name = "accounts"

worker_patterns = [
    path(
        "",
        views.WorkerListView.as_view(),
        name="worker-list",
    ),
    path(
        "<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail",
    ),
    path(
        "<int:pk>/update/",
        views.WorkerUpdateView.as_view(),
        name="worker-update",
    ),
    path(
        "<int:pk>/delete/",
        views.WorkerDeleteView.as_view(),
        name="worker-delete",
    ),
    path(
        "<int:pk>/toggle-assign/",
        views.ToggleAssignToTaskView.as_view(),
        name="toggle-assign",
    ),
]

auth_patterns = [
    path(
        "register/",
        views.WorkerRegisterView.as_view(),
        name="register",
    ),
    path(
        "activate/<str:uid>/<str:token>/",
        views.WorkerActivateView.as_view(),
        name="activate",
    ),
    path(
        "login/",
        views.WorkerLoginView.as_view(),
        name="login",
    ),
    path("", include("django.contrib.auth.urls")),
]

urlpatterns = [
    path("workers/", include(worker_patterns)),
    path("", include(auth_patterns)),
]
