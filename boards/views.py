# boards/views.py
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext as _

from .models import Board, BoardMembership
from .serializers import BoardSerializer
from .permissions import IsOwnerOrReadOnly
from .tasks import send_invitation_email
from django.db.models import Q
from .serializers import MemberSerializer




class BoardViewSet(viewsets.ModelViewSet):
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


    @action(detail=True, methods=["get"])
    def members(self, request, pk=None):
        board = self.get_object() 
        qs = board.memberships.all().order_by("role", "id")
        serializer = MemberSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def invite(self, request, pk=None):
        board = self.get_object()
        email = request.data.get("email")
        if not email:
            return Response({"error": _("Email is required")}, status=status.HTTP_400_BAD_REQUEST)

        from django.contrib.auth import get_user_model
        User = get_user_model()
        invited_user = User.objects.filter(email__iexact=email).first()

        if invited_user:
            membership, created = BoardMembership.objects.get_or_create(
                board=board,
                user=invited_user,
                defaults={"role": "member", "status": "accepted"}
            )
            if created:
                msg = _("%(email)s added as member") % {"email": email}
            else:
                msg = _("%(email)s is already a member or invite exists") % {"email": email}
        else:
            membership, created = BoardMembership.objects.get_or_create(
                board=board,
                invited_email=email,
                defaults={"user": None, "status": "pending", "role": "member"}
            )
            msg = _("Invitation created for %(email)s") % {"email": email}

        invite_link = request.build_absolute_uri(reverse("boards:accept-invite", args=[board.id]))
        try:
            send_invitation_email.delay(email, board.name, invite_link)
        except Exception:
            pass

        return Response({"message": msg, "invite_id": membership.id})


    def get_queryset(self):

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
            return Response({"error": _("Email is required")}, status=400)

        membership, created = BoardMembership.objects.get_or_create(
            board=board,
            user=None,
            defaults={"status": "pending"}
        )

        invite_link = request.build_absolute_uri(
            reverse("boards:accept-invite", args=[board.id])
        )

        send_invitation_email.delay(email, board.name, invite_link)

        return Response({"message": _("Invitation sent successfully!")})

def board_list_view(request):
    boards = Board.objects.filter(memberships__user=request.user)
    return render(request, "boards/board_list.html", {"boards": boards})

@api_view(["GET"])
def accept_invite(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    membership = BoardMembership.objects.filter(board=board, status="pending").first()
    if not membership:
        return Response({"error": _("No pending invite found")}, status=400)

    membership.user = request.user
    membership.status = "accepted"
    membership.save()
    return Response({"message": _("You have joined the board!")})

def invite_test_view(request):
    return render(request, "boards/invite.html")

def language_test_view(request):
    return render(request, "boards/language_test.html")

def boards_test_view(request):
    return render(request, "boards/boards_test.html")

def invitations_test_view(request):
    return render(request, "boards/invitations_test.html")