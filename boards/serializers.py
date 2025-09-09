# boards/serializers.py
from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ["id","name","color","owner","created_at"]
        read_only_fields = ["id","owner","created_at"]
