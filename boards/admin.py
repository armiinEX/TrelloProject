# boards/admin.py
from django.contrib import admin
from .models import Board, BoardMembership

admin.site.register(Board)
admin.site.register(BoardMembership)
