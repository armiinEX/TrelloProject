# core/urls.py

"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from boards.views import BoardViewSet, board_list_view
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tasksapp.views import ListViewSet
from tasksapp.views import ListViewSet, TaskViewSet
from django.conf.urls.i18n import i18n_patterns
from .views import home_view
# from boards.views import InvitationViewSet
from django.urls import path
from .views import LanguagesView, UserLanguageUpdateView






router = DefaultRouter()
router.register("boards", BoardViewSet, basename="board")
router.register("lists", ListViewSet, basename="list")
router.register("tasks", TaskViewSet, basename="task")
# router.register("invitations", InvitationViewSet, basename="invitation")


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/", include(router.urls)),

    # nested lists for boards
    path(
        "api/boards/<int:board_id>/lists/",
        ListViewSet.as_view({"get": "list", "post": "create"}),
        name="board-lists",
    ),
    path(
        "api/boards/<int:board_id>/lists/<int:pk>/",
        ListViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="board-list-detail",
    ),

    path(
    "api/lists/<int:list_id>/tasks/",
    TaskViewSet.as_view({"get": "list", "post": "create"}),
    name="list-tasks",
    ),
    path(
        "api/lists/<int:list_id>/tasks/<int:pk>/",
        TaskViewSet.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}),
        name="list-task-detail",
    ),
    
    path("i18n/", include("django.conf.urls.i18n")),
    path("boards-ui/", board_list_view, name="board_list_ui"),
    path("tasksapp/", include("tasksapp.urls")),
    path("", home_view, name="home"),
    path("api/accounts/", include("accounts.urls")),
]

urlpatterns += i18n_patterns(
    path("boards/", include("boards.urls")),
)

urlpatterns += [
    path("languages/", LanguagesView.as_view(), name="languages"),
    path("me/language/", UserLanguageUpdateView.as_view(), name="profile-language"),
]