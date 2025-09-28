# boards/serializers.py
from rest_framework import serializers
from .models import Board
from .models import Board, BoardMembership
from django.contrib.auth import get_user_model

User = get_user_model()


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id","name","color","owner","created_at"]
        read_only_fields = ["id","owner","created_at"]

class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name", "preferred_language")

class MemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = BoardMembership
        fields = ["id", "board", "user", "username", "email", "role", "status", "invited_email"]

class InvitationSerializer(serializers.ModelSerializer):
    user = UserBriefSerializer(read_only=True)
    board = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = BoardMembership
        fields = ("id", "board", "user", "invited_email", "role", "status")
        read_only_fields = ("board",)

