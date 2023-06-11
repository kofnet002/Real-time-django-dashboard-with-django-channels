from django.urls import path, re_path
from .consumers import DashboardConsumer


websocket_urlpatterns = [
    path('ws/<str:dashboard_slug>/', DashboardConsumer.as_asgi()),
    # path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatRoomConsumer),
]
