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
from tasksapp.views import TaskViewSet



router = DefaultRouter()
router.register("boards", BoardViewSet, basename="board")
router.register("lists", ListViewSet, basename="list")
router.register("tasks", TaskViewSet, basename="task")



urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/", include(router.urls)),
    path("i18n/", include("django.conf.urls.i18n")),   # برای set-language در روز 5
    path("boards-ui/", board_list_view, name="board_list_ui"),
    path("boards/", include("boards.urls")),  # 👈 این باید باشه

]
