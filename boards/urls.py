from django.urls import path
from .views import accept_invite

app_name = "boards"

urlpatterns = [
    path("accept-invite/<int:board_id>/", accept_invite, name="accept-invite"),
]