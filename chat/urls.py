from django.urls import path

from . import views

urlpatterns = [
    # URL to start a new chat session (you might need to create a view for this)
    path(
        "start_chat/",
        views.start_chat,
        name="start_chat",
    ),
    # URL for the chat room
    path("<int:session_id>/", views.chat_room, name="chat_room"),
]
