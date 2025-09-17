from django.urls import path
from .views import tasks_test_view

app_name = "tasksapp"

urlpatterns = [
    path("tasks-test/", tasks_test_view, name="tasks_test"),
]