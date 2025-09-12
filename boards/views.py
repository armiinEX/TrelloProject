# boards/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render

from .models import Board, BoardMembership
from .serializers import BoardSerializer
from .permissions import IsOwnerOrReadOnly


class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
        هفته اول: بردهایی که Owner آن‌ها هستی
        یا عضو شدی (status="accepted")
        """
        qs1 = Board.objects.filter(
            memberships__user=self.request.user,
            memberships__status="accepted"
        )
        qs2 = Board.objects.filter(owner=self.request.user)
        return qs1.union(qs2)  # union → دیگر خطای unique/non-unique نمی‌دهد

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        BoardMembership.objects.get_or_create(
            board=board,
            user=self.request.user,
            defaults={"role": "owner", "status": "accepted"}
        )


def board_list_view(request):
    boards = Board.objects.filter(memberships__user=request.user)
    return render(request, "boards/board_list.html", {"boards": boards})