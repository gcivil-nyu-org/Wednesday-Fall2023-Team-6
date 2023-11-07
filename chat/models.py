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
