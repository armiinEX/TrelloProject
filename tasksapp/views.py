# tasksapp/views.py
from rest_framework import viewsets, permissions
from .models import List
from .serializers import ListSerializer

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return List.objects.filter(board__memberships__user=self.request.user)

    def perform_create(self, serializer):
        board = serializer.validated_data["board"]
        if not board.memberships.filter(user=self.request.user, status="accepted").exists():
            raise PermissionError("You are not a member of this board.")
        serializer.save()
