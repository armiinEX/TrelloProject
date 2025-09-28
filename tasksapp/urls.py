# tasksapp/urls.py
from django.urls import path
from .views import tasks_test_view, lists_test_view, tasks_crud_test_view

app_name = "tasksapp"

urlpatterns = [
    path("tasks-test/", tasks_test_view, name="tasks_test"),
    path("lists-test/", lists_test_view, name="lists_test"),
    path("tasks-crud-test/", tasks_crud_test_view, name="tasks_crud_test"),
]