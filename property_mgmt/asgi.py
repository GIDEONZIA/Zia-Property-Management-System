"""
ASGI config for property_mgmt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "property_mgmt.settings")

django.setup()

import importlib

# import chat.routing (try top-level app name first, fall back to project-relative)
try:
    chat_routing = importlib.import_module('chat.routing')
except ImportError:
    chat_routing = importlib.import_module('property_mgmt.chat.routing')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(chat_routing.websocket_urlpatterns)
    ),
})









