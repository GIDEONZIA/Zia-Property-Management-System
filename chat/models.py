# chat/models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,      # allow guest users
        blank=True
    )
    sender_name = models.CharField(max_length=100, default="Unkown")  # name displayed in chat
    message = models.TextField()                    # user message
    response = models.TextField(blank=True, null=True)  # bot/agent reply
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender_name}: {self.message[:50]}"
