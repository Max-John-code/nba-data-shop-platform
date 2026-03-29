from django.contrib import admin
from .models import Highlight


@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ['title', 'teams', 'match_date', 'views', 'duration', 'is_active', 'created_at']
    list_filter = ['is_active', 'match_date']
    search_fields = ['title', 'teams', 'description']
    ordering = ['-match_date', '-created_at']
