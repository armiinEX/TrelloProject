# boards/admin.py
from django.contrib import admin
from .models import Board, BoardMembership

admin.site.register(BoardMembership)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created_at")

@admin.register(BoardMembership)
class BoardMembershipAdmin(admin.ModelAdmin):
    list_display = ("id", "board", "user", "invited_email", "role", "status")
    list_filter = ("status", "role", "board")
    search_fields = ("invited_email", "user__username", "board__name")
