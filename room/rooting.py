from django.urls import re_path
from . import consumers

"""
docstring
"""

websocket_urlpatterns = [
    re_path(r'ws/room/(?P<room_name>\w+)/(?P<player_name>\w+)',
            consumers.ChatConsumer),
    re_path(r'ws/game/(?P<room_name>\w+)/(?P<player_name>\w+)',
            consumers.GameComsumer)
]
