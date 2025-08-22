from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "response", "created_at")
    list_filter = ("created_at", "user")
    search_fields = ("message", "response", "user__username")
