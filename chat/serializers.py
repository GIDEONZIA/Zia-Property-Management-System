from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatSession, ChatMessage

User = get_user_model()


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name")


class ChatSessionSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)
    agent = UserLiteSerializer(read_only=True)

    class Meta:
        model = ChatSession
        # Use flexible field names that most chat session models have
        fields = (
            "id",
            "user",
            "agent",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserLiteSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        # Include optional sender_name if your model has it
        base_fields = ["id", "session", "content", "created_at"]
        maybe_sender_name = ["sender_name"] if hasattr(ChatMessage, "sender_name") else []
        maybe_sender = ["sender"] if hasattr(ChatMessage, "sender") else []
        fields = base_fields + maybe_sender + maybe_sender_name
        read_only_fields = ["id", "created_at"] + maybe_sender + maybe_sender_name
