# from django.db import models
# from django.contrib.auth import get_user_model
#
# User = get_user_model()
#
#
# class ChatRoom(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     # If you want to track the creation date of the room
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Message(models.Model):
#     room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
#     user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.user.username + ": " + self.content

from django.db import models
from doctor.models import Doctor
from user.models import Patient


class ChatSession(models.Model):
    # doctor = models.ForeignKey(
    #     Doctor, related_name="doctor_chat_sessions", on_delete=models.CASCADE
    # )
    # patient = models.ForeignKey(
    #     Patient, related_name="patient_chat_sessions", on_delete=models.CASCADE
    # )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "seshhh"
        # return f"Chat between {self.doctor.name} and {self.patient.name}"


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession, related_name="messages", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        "auth.User", related_name="messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.username}: {self.content[:20]}..."
