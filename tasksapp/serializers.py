# tasksapp/serializers.py
from rest_framework import serializers
from .models import List
from .models import Task


class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ["id", "board", "title", "order"]
        read_only_fields = ["id"]

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "list", "title", "description", "due_date", "order", "is_completed", "created_at"]
        read_only_fields = ["id", "created_at"]
