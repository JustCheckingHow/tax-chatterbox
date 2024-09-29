from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/v1/chat/<str:multidevice_idx>', consumers.AIConsumer.as_asgi()),
]