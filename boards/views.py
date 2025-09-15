# boards/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Board, BoardMembership
from .serializers import BoardSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import send_invitation_email
from django.db.models import Q



class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        """
    هفته اول: بردهایی که Owner آن‌ها هستی
    یا عضو شدی (status="accepted")
    """
        return Board.objects.filter(
            Q(owner=self.request.user) |
            Q(memberships__user=self.request.user, memberships__status="accepted")
        ).distinct()

    def perform_create(self, serializer):
        board = serializer.save(owner=self.request.user)
        BoardMembership.objects.get_or_create(
            board=board,
            user=self.request.user,
            defaults={"role": "owner", "status": "accepted"}
        )

    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        board = self.get_object()
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        # ساخت Membership در حالت pending
        membership, created = BoardMembership.objects.get_or_create(
            board=board,
            user=None,  # اگه کاربر هنوز رجیستر نکرده
            defaults={"status": "pending"}
        )

        # ساخت لینک دعوت
        invite_link = request.build_absolute_uri(
            reverse("boards:accept-invite", args=[board.id])
        )

        # ارسال ایمیل async
        send_invitation_email.delay(email, board.name, invite_link)

        return Response({"message": f"Invitation sent to {email}"})


def board_list_view(request):
    boards = Board.objects.filter(memberships__user=request.user)
    return render(request, "boards/board_list.html", {"boards": boards})


@api_view(["GET"])
def accept_invite(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    membership = BoardMembership.objects.filter(board=board, status="pending").first()
    if not membership:
        return Response({"error": "No pending invite found"}, status=400)

    membership.user = request.user
    membership.status = "accepted"
    membership.save()
    return Response({"message": "You have joined the board!"})