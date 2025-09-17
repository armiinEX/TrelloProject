# boards/permissions.py
from rest_framework.permissions import BasePermission
from django.utils.translation import gettext_lazy as _

class IsOwnerOrReadOnly(BasePermission):
    message = _("You do not have permission to modify this board.")
    def has_object_permission(self, request, view, obj):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return obj.owner_id == request.user.id
