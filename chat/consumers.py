import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model

from .models import ChatSession, ChatMessage

User = get_user_model()


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    WebSocket consumer that attaches to a specific chat session:
      ws://<host>/ws/chat/<session_id>/
    - Only the session's user, agent, or staff can join.
    - Guests can join if your app allows anonymous sessions (adjust as needed).
    - Persists messages to ChatMessage.
    - Broadcasts to group 'chat_<session_id>'.
    """

    async def connect(self):
        self.user = self.scope.get("user")
        self.session_id = self.scope["url_route"]["kwargs"]["session_id"]
        self.group_name = f"chat_{self.session_id}"

        # Optional: read ?username=<guest name> from query string for anonymous users
        self.query_params = parse_qs(self.scope.get("query_string", b"").decode() or "")
        self.guest_name = (self.query_params.get("username") or [None])[0]

        # Verify the session exists and the user is allowed to join
        allowed = await self._is_allowed(self.session_id, self.user)
        if not allowed:
            await self.close(code=4001)  # not authorized for this room
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Optional: notify join
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.event",
                "event": "join",
                "user": await self._display_name(self.user, self.guest_name),
                "message": "joined the chat",
            },
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        """
        Expect JSON like:
        {
          "message": "Hello there!",
          "username": "John (guest)",   # optional, for anonymous
        }
        """
        message = (content or {}).get("message", "").strip()
        if not message:
            return

        # Prefer username from payload over querystring if provided
        username_override = (content or {}).get("username") or self.guest_name

        # Save to DB
        msg_obj = await self._save_message(
            session_id=self.session_id,
            user=self.user if (self.user and self.user.is_authenticated) else None,
            sender_name=username_override,
            content=message,
        )

        # Broadcast
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "id": msg_obj.id if msg_obj else None,
                "user": await self._display_name(self.user, username_override),
                "message": message,
                "timestamp": getattr(msg_obj, "created_at", None) or getattr(msg_obj, "timestamp", None),
            },
        )

    # Group event handlers
    async def chat_message(self, event):
        await self.send_json(event)

    async def chat_event(self, event):
        await self.send_json(event)

    # ==============================
    # DB helpers
    # ==============================

    @database_sync_to_async
    def _is_allowed(self, session_id, user):
        session = ChatSession.objects.filter(id=session_id).select_related("user", "agent").first()
        if not session:
            return False

        # Staff always allowed
        if user and user.is_authenticated and (getattr(user, "is_staff", False) or getattr(user, "is_superuser", False)):
            return True

        # If authenticated, must match the session's user or agent
        if user and user.is_authenticated:
            if session.user_id == user.id or session.agent_id == user.id:
                return True
            return False

        # Anonymous allowed only if your app allows guests; adjust logic as needed
        return True

    @database_sync_to_async
    def _save_message(self, session_id, user, sender_name, content):
        session = ChatSession.objects.filter(id=session_id).first()
        if not session:
            return None

        # Supports both authenticated sender or guest sender_name if your model has that field
        kwargs = {"session": session, "content": content}
        if hasattr(ChatMessage, "sender"):
            kwargs["sender"] = user
        if hasattr(ChatMessage, "sender_name") and sender_name:
            kwargs["sender_name"] = sender_name

        return ChatMessage.objects.create(**kwargs)

    @database_sync_to_async
    def _display_name(self, user, guest_name):
        if user and user.is_authenticated:
            return getattr(user, "get_full_name", lambda: None)() or user.username
        return guest_name or "Guest"
