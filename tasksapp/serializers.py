# tasksapp/serializers.py
from rest_framework import serializers
from .models import List, Task

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["id", "board", "title", "order"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "board": {"required": False}
        }

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id", "list", "title", "description", "due_date",
            "order", "is_completed", "created_at"
        ]
        read_only_fields = ["id", "created_at"]
        extra_kwargs = {
            "list": {"required": False}  # allow create via nested URL without 'list' in payload
        }