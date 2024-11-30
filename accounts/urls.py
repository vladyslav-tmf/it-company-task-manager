from django.urls import include, path
from accounts import views

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register/", views.WorkerRegisterView.as_view(), name="register"),
    path("activate/<str:uid>/<str:token>/", views.WorkerActivateView.as_view(), name="activate")
]
