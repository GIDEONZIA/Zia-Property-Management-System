from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    path("setup/", views.chat_setup, name="chat_setup"),
    path("start/", views.start_chat, name="start_chat"),
    path("room/<int:session_id>/", views.chat_room, name="chat_room"),
    path("bot-reply/", views.bot_reply, name="bot_reply"),
]
