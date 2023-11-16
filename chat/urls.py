from django.urls import path

from . import views

urlpatterns = [
    path("<str:recipient_id>/", views.chat, name="chat-with-user"),
    # Add other chat app URLs here
]
