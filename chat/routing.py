from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    # ws://<host>/ws/chat/<session_id>/
    re_path(r"^ws/chat/(?P<session_id>[\w-]+)/$", ChatConsumer.as_asgi()),
]
