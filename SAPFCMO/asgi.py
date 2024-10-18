"""
ASGI config for SAPFCMO project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.conf import settings
from django.urls import path
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SAPFCMO.settings')

django_asgi_app = get_asgi_application()

import webhook_handler.routing


application = ProtocolTypeRouter(
    {
        "http" : django_asgi_app,
        "websocket": AllowedHostsOriginValidator (
    AuthMiddlewareStack(URLRouter(webhook_handler.routing.websocket_urlpatterns))
        )
    }
)