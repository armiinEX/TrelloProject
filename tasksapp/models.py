# tasksapp/models.py
from django.db import models
from boards.models import Board
from django.utils.translation import gettext_lazy as _

class List(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="lists")
    title = models.CharField(_("List Title"), max_length=120)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order","id"]

    def __str__(self):
        return f"{self.board.name} / {self.title}"

class Task(models.Model):
    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(_("Task Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    due_date = models.DateField(_("Due Date"), null=True, blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    is_completed = models.BooleanField(_("Completed"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        ordering = ["order","id"]

    def __str__(self):
        return self.title
