"""
ASGI config for taxchatter project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing
from chat import consumers

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taxchatter.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})

# Add this line to create an instance of AIConsumer
# The 'consumers' module is not imported. We need to import it before using it.
# Assuming 'consumers' is in the 'chat' app, we should add an import statement:
ai_application = consumers.AIConsumer.as_asgi()
