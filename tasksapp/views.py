# tasksapp/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer


class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return List.objects.filter(board__memberships__user=self.request.user)

    def perform_create(self, serializer):
        board = serializer.validated_data["board"]
        if not board.memberships.filter(user=self.request.user, status="accepted").exists():
            raise PermissionDenied("You are not a member of this board.")
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Task.objects.filter(list__board__memberships__user=self.request.user)
        due = self.request.query_params.get("due")
        if due:
            qs = qs.filter(due_date=due)
        return qs

    def perform_create(self, serializer):
        lst = serializer.validated_data["list"]
        if not lst.board.memberships.filter(user=self.request.user, status="accepted").exists():
            raise PermissionDenied("You are not a member of this board.")
        serializer.save()
        
    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        task = self.get_object()
        new_list_id = request.data.get("list")
        new_order = request.data.get("order", 0)
        if new_list_id:
            task.list_id = new_list_id
        task.order = new_order
        task.save()
        return Response(TaskSerializer(task).data)