# accounts/urls.py
from django.urls import path
from .views import RegisterView, MyTokenObtainPairView, ProfileView, auth_test_view, logout_view
from rest_framework_simplejwt.views import TokenRefreshView as SimpleTokenRefreshView


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/refresh/", SimpleTokenRefreshView.as_view(), name="token_refresh"),
    # path("auth/logout/", logout_view.as_view(), name="token_blacklist"),
    path("auth/logout/", logout_view, name="logout"),   # 👈 دیگه .as_view() نمی‌خواد
    path("me/", ProfileView.as_view(), name="profile-me"),
    path("auth/test-ui/", auth_test_view, name="auth_test_ui"),
    # path("users/me/", ProfileView.as_view(), name="profile-me"),
]