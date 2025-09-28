# tasksapp/views.py
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import List, Task
from .serializers import ListSerializer, TaskSerializer
from django.utils.translation import gettext as _
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from boards.models import Board





class ListViewSet(viewsets.ModelViewSet):
    serializer_class = ListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        If called via nested route with board_id in kwargs, filter by that board.
        Always ensure user is owner or accepted member of the board.
        Otherwise return lists for boards user is a member of.
        """
        qs = List.objects.filter(board__memberships__user=self.request.user, board__memberships__status="accepted")

        board_id = self.kwargs.get("board_id")  # provided by nested URL
        if board_id:
            qs = qs.filter(board_id=board_id)

        return qs.distinct()

    def perform_create(self, serializer):
        """
        For nested create (POST /api/boards/<board_id>/lists/), take board from URL.
        For non-nested create (POST /api/lists/), expect 'board' in request data.
        Also enforce membership check.
        """
        board_id = self.kwargs.get("board_id")
        if board_id:
            board = get_object_or_404(Board, pk=board_id)
        else:
            # fallback: client provided board in payload
            board = serializer.validated_data.get("board")
            if board is None:
                raise PermissionDenied("Board must be provided.")

        # permission: only owner or accepted member can create lists
        if not (board.owner == self.request.user or board.memberships.filter(user=self.request.user, status="accepted").exists()):
            raise PermissionDenied("You are not a member of this board.")

        # save the list, ensure board is set
        serializer.save(board=board)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Task.objects.filter(list__board__memberships__user=self.request.user).distinct()

        list_id = self.kwargs.get("list_id")
        if list_id:
            qs = qs.filter(list_id=list_id)

        due = self.request.query_params.get("due")
        if due:
            qs = qs.filter(due_date=due)

        return qs

    def perform_create(self, serializer):
        list_id = self.kwargs.get("list_id")
        if list_id:
            lst = get_object_or_404(List, pk=list_id)
        else:
            lst = serializer.validated_data.get("list")
            if not lst:
                raise ValidationError({"list": "List is required."})

        board = lst.board
        is_owner = (board.owner == self.request.user)
        is_member = board.memberships.filter(user=self.request.user, status="accepted").exists()
        if not (is_owner or is_member):
            raise PermissionDenied("You are not a member of this board.")

        serializer.save(list=lst)

    @action(detail=True, methods=["post"])
    def move(self, request, pk=None):
        """
        POST /api/tasks/{id}/move/  or nested: /api/lists/{list_id}/tasks/{id}/move/
        body: {"list": <new_list_id>, "order": <new_order>}
        """
        task = self.get_object()
        new_list_id = request.data.get("list")
        new_order = request.data.get("order", 0)

        if new_list_id:
            new_list = get_object_or_404(List, pk=new_list_id)
            board = new_list.board
            is_owner = (board.owner == request.user)
            is_member = board.memberships.filter(user=request.user, status="accepted").exists()
            if not (is_owner or is_member):
                return Response({"detail": "You are not a member of the destination board."}, status=status.HTTP_403_FORBIDDEN)
            task.list = new_list

        task.order = new_order
        task.save()
        return Response(TaskSerializer(task).data)

@login_required
def tasks_test_view(request):
    return render(request, "tasksapp/tasks_test.html")

def lists_test_view(request):
    return render(request, "tasksapp/lists_test.html")

def tasks_crud_test_view(request):
    return render(request, "tasksapp/tasks_crud_test.html")