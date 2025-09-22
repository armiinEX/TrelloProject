from django.urls import path
from .views import accept_invite, invite_test_view, language_test_view

app_name = "boards"

urlpatterns = [
    path("accept-invite/<int:board_id>/", accept_invite, name="accept-invite"),
    path("invite-test/", invite_test_view, name="invite_test"),
    path("language-test/", language_test_view, name="language_test"),
    path("lang-test/", language_test_view, name="lang-test"),

]