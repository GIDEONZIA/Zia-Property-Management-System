from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatSession(models.Model):
    """Represents a chat between a user and an agent/bot."""
    user = models.ForeignKey(User, related_name="chat_sessions", on_delete=models.CASCADE)
    agent = models.ForeignKey(
        User, related_name="agent_sessions", on_delete=models.SET_NULL, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)  # 👈 Add this
    updated_at = models.DateTimeField(auto_now=True)      # 👈 for edits
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Session {self.id} ({self.user.username})"


class ChatMessage(models.Model):
    """Stores messages inside a session."""
    session = models.ForeignKey(ChatSession, related_name="messages", on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}"
