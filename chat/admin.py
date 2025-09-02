from django.contrib import admin
from .models import ChatSession, ChatMessage


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):

    list_display = ("id", "user", "agent", "created_at", "is_active")
    list_filter = ("is_active", "created_at")
    search_fields = ("user__username", "agent__username")

    def created(self, obj):
        return getattr(obj, "created_at", getattr(obj, "timestamp", None))
    created.short_description = "Created"

    def updated(self, obj):
        return getattr(obj, "updated_at", None)



    def display_user(self, obj):
        return getattr(obj.user, "username", None) if hasattr(obj, "user") else None
    display_user.short_description = "User"

    def display_agent(self, obj):
        return getattr(obj.agent, "username", None) if hasattr(obj, "agent") else None
    display_agent.short_description = "Agent"


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):

    list_display = ("id", "session", "sender", "content", "timestamp")
    list_filter = ("timestamp",)
    search_fields = ("session__id", "sender__username", "content")
    date_hierarchy = "timestamp"   # ✅ FIXED: must match the model field
    
    def created(self, obj):
        return getattr(obj, "created_at", getattr(obj, "timestamp", None))
    created.short_description = "Created"

    def display_user(self, obj):
        # Try sender, then user, then sender_name
        if hasattr(obj, "sender") and obj.sender:
            return getattr(obj.sender, "username", None)
        if hasattr(obj, "user") and obj.user:
            return getattr(obj.user, "username", None)
        if hasattr(obj, "sender_name"):
            return obj.sender_name
        return "Unknown"

