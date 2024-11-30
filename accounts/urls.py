from django.urls import include, path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.WorkerRegisterView.as_view(), name="register"),
    path("activate/<str:uid>/<str:token>/", views.WorkerActivateView.as_view(), name="activate"),
    path("workers/", views.WorkerListView.as_view(), name="worker-list"),
    path("<int:pk>/", views.WorkerDetailView.as_view(), name="worker-detail"),
    path("<int:pk>/update/", views.WorkerUpdateView.as_view(), name="worker-update"),
    path("<int:pk>/delete/", views.WorkerDeleteView.as_view(), name="worker-delete")
]
