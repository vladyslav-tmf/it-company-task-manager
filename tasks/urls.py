from django.urls import path

from tasks import views

app_name = "tasks"

urlpatterns = [
    # Index url:
    path("", views.IndexView.as_view(), name="index")
]
