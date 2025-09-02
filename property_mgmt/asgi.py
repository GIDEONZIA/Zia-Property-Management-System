"""
ASGI config for property_mgmt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chat.routing import websocket_urlpatterns as chat_ws

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    # include chat websocket routes
                    *chat_ws,
                ]
            )
        ),
    }
)




